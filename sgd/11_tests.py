"""
11_tests.py -- the five scored tests (T1, T2, T3, T4, T7), gate C, the
sensitivities, the verdict and the scorecard, exactly as THESIS.md fixes them.

  python3 sgd/11_tests.py [--root DIR]

Reads out/ (written by 10_load.py) and THESIS.md (for the confidences only).
Writes:
  out/tests.csv          key, value: every scored number, outcome and verdict
  out/sensitivities.csv  test, variant, key, value: reported, never scored
  out/intervals.csv      T7's intervals: decision, start, end, months, y, g, p
Plain Python (math, random); 15_reproduce.py recomputes the scored numbers
from raw/ by a different path (pandas, numpy).

Conventions (THESIS sections 3 and 5):
  ln cross(X, t) = ln(X per USD) - ln(SGD per USD): units of X per Singapore
  dollar (for USD, X per USD = 1). A window's change is the mean of the log
  over its three end months minus the mean over its three start months.
  b = change in ln cross; s = change in ln NEER(SG); nx = change in
  ln NEER(X's area); e = b - s + nx. Shares S = s/b, P = -nx/b, R = e/b,
  defined only when b > 0.
"""
import math
import os
import random
from collections import defaultdict

import sgdlib as L


# ----------------------------------------------------------------- loading
def load(out):
    def series(name, k1, k2="period"):
        d = defaultdict(dict)
        path = os.path.join(out, name + ".csv")
        if not os.path.exists(path):
            return {}
        for r in L.read_csv(path):
            d[r[k1]][r[k2]] = float(r["value"])
        return dict(d)

    D = {"neer": series("neer", "area"), "reer": series("reer", "area"),
         "usd": series("usd", "currency"), "usd_eop": series("usd_eop", "currency"),
         "masfx": series("masfx", "currency")}
    D["sneer"] = {r["period"]: (float(r["value"]), int(r["n"]))
                  for r in L.read_csv(os.path.join(out, "sneer.csv"))}
    D["gdp"] = {r["quarter"]: float(r["value"]) for r in L.read_csv(os.path.join(out, "gdp.csv"))}
    D["cpi"] = {r["period"]: float(r["value"]) for r in L.read_csv(os.path.join(out, "cpi.csv"))}
    D["mps"] = sorted(L.read_csv(os.path.join(out, "mps.csv")), key=lambda r: r["date"])
    return D


# ----------------------------------------------------------------- helpers
def mean(xs):
    return sum(xs) / len(xs)


def sd(xs):
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def cov(xs, ys):
    mx, my = mean(xs), mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)


def pearson(xs, ys):
    vx, vy = cov(xs, xs), cov(ys, ys)
    if vx <= 0 or vy <= 0:
        return None
    return cov(xs, ys) / math.sqrt(vx * vy)


def ranks(xs):
    """Average ranks, 1-based."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(xs, ys):
    return pearson(ranks(xs), ranks(ys))


def ln_cross(D, cur, p, usd="usd"):
    U = D[usd]
    sg = U.get("SGD", {}).get(p)
    x = 1.0 if cur == "USD" else U.get(cur, {}).get(p)
    if sg is None or x is None or sg <= 0 or x <= 0:
        return None
    return math.log(x) - math.log(sg)


def ln_eer(D, area, p, eer="neer"):
    v = D[eer].get(area, {}).get(p)
    return math.log(v) if v and v > 0 else None


def endmean(f, months_):
    vals = [f(m) for m in months_]
    return None if any(v is None for v in vals) else mean(vals)


def last_month(D):
    return max(D["neer"]["SG"])


def windows(D):
    """{name: (first, last, start months, end months)} -- THESIS section 5."""
    last = last_month(D)
    long_end = tuple(L.month_add(last, k) for k in (-2, -1, 0))
    return {"scored": (L.SCORED_START[0], L.SCORED_END[-1], L.SCORED_START, L.SCORED_END),
            "long": (L.LONG_FIRST, last, L.LONG_START, long_end)}


def split(D, cur, start, end, usd="usd", eer="neer"):
    """b, s, nx, e and the shares S, P, R (None unless b > 0)."""
    area = L.CUR_AREA[cur]
    vals = []
    for f in (lambda m: ln_cross(D, cur, m, usd), lambda m: ln_eer(D, "SG", m, eer),
              lambda m: ln_eer(D, area, m, eer)):
        a, z = endmean(f, start), endmean(f, end)
        if a is None or z is None:
            return None
        vals.append(z - a)
    b, s, nx = vals
    e = b - s + nx
    out = {"b": b, "s": s, "nx": nx, "e": e, "S": None, "P": None, "R": None}
    if b > 0:
        out.update(S=s / b, P=-nx / b, R=e / b)
    return out


def mad(D, cur, first, last):
    """Mean absolute monthly difference, ln BIS cross minus ln MAS's rate
    (X per SGD = 1 / SGD per unit), over the months both exist."""
    diffs = []
    for m in L.months(first, last):
        bis = ln_cross(D, cur, m)
        mas = D["masfx"].get(cur, {}).get(m)
        if bis is not None and mas:
            diffs.append(abs(bis - math.log(1.0 / mas)))
    return (mean(diffs), len(diffs)) if diffs else (None, 0)


def changes(f, months_):
    """Monthly changes of f over consecutive months where both ends exist."""
    out = []
    for a, z in zip(months_, months_[1:]):
        fa, fz = f(a), f(z)
        if fa is not None and fz is not None:
            out.append(fz - fa)
    return out


# ----------------------------------------------------------------- tests
def t1(D, W, R):
    oks = []
    for w in ("scored", "long"):
        first, last, start, end = W[w]
        for cur in L.QUESTION:
            sp = split(D, cur, start, end)
            m, n = mad(D, cur, first, last)
            k = f"T1_{w}_{cur}"
            if sp is None:
                R[k + "_status"] = "series missing"
                oks.append(False)
                R[k + "_ok"] = False
                continue
            R[k + "_b"], R[k + "_R"] = sp["b"], sp["R"]
            R[k + "_mad"], R[k + "_mad_count"] = m, n
            ok_a = sp["b"] <= 0 or abs(sp["R"]) <= L.T1_R
            ok_b = m is None or m <= L.T1_MAD
            R[k + "_status"] = ("premise false (b <= 0): (a) not defined" if sp["b"] <= 0 else "") + \
                               ("; MAS rate missing: (b) not run" if m is None else "")
            R[k + "_ok"] = ok_a and ok_b
            oks.append(ok_a and ok_b)
    R["T1_outcome"] = "SURVIVE" if all(oks) else "FAIL"


def share_test(D, W, R, t, cur):
    first, last, start, end = W["scored"]
    sp = split(D, cur, start, end)
    if sp is None:
        R[f"{t}_outcome"] = "NOT SCORED"
        R[f"{t}_reason"] = "series missing"
        return
    for k in ("b", "s", "nx", "e", "S", "P", "R"):
        R[f"{t}_{k}"] = sp[k]
    if sp["b"] <= 0:
        R[f"{t}_outcome"], R[f"{t}_reason"] = "NOT SCORED", "premise false: b <= 0"
    elif not R[f"T1_scored_{cur}_ok"]:
        R[f"{t}_outcome"], R[f"{t}_reason"] = "NOT SCORED", "T1 failed for this currency on the scored window"
    elif sp["P"] >= L.T2_P and sp["P"] > sp["S"]:
        R[f"{t}_outcome"] = "SURVIVE"
    elif sp["S"] >= sp["P"]:
        R[f"{t}_outcome"] = "FAIL"
    else:
        R[f"{t}_outcome"] = "INCONCLUSIVE"


def gate_c(D, R):
    S = {p: v for p, (v, n) in D["sneer"].items() if n >= L.GATE_MIN_READINGS}
    ps = sorted(set(S) & set(D["neer"]["SG"]))
    xs, ys = [], []
    for a, z in zip(ps, ps[1:]):
        if L.month_diff(a, z) == 1:
            xs.append(math.log(S[z]) - math.log(S[a]))
            ys.append(math.log(D["neer"]["SG"][z]) - math.log(D["neer"]["SG"][a]))
    r = pearson(xs, ys) if len(xs) >= 3 else None
    R["gateC_r"], R["gateC_changes"] = r, len(xs)
    R["gateC_pass"] = r is not None and len(xs) >= L.GATE_MIN and r >= L.GATE_R
    return R["gateC_pass"]


def vol_table(D, first, last):
    ms = L.months(first, last)
    out = {}
    for a in L.AREAS:
        if a not in D["neer"] or any(D["neer"][a].get(m) is None for m in ms):
            continue
        out[a] = sd(changes(lambda m, a=a: ln_eer(D, a, m), ms))
    return out


def rank_of(vol, area="SG"):
    return 1 + sum(1 for a, v in vol.items() if a != area and v < vol[area])


def t4(D, W, R, gate):
    first, last = W["long"][0], W["long"][1]
    vol = vol_table(D, first, last)
    for a, v in vol.items():
        R[f"T4_{a}_sd"] = v
    present = len(vol)
    R["T4_present"] = present
    if "SG" not in vol or present < L.T4_MIN_PRESENT:
        R["T4_outcome"], R["T4_reason"] = "NOT SCORED", f"{present} of 11 series present"
        return vol
    rank = rank_of(vol)
    partners = present - 1
    steadier_than = sum(1 for a, v in vol.items() if a != "SG" and v > vol["SG"])
    R["T4_rank"], R["T4_steadier_than"] = rank, steadier_than
    if not gate:
        R["T4_outcome"], R["T4_reason"] = "NOT SCORED", "gate C failed: the record cannot say"
    elif rank <= L.T4_SURVIVE_RANK:
        R["T4_outcome"] = "SURVIVE"
    elif steadier_than <= partners // 2:
        R["T4_outcome"] = "FAIL"
    else:
        R["T4_outcome"] = "INCONCLUSIVE"
    return vol


def quarter_end(q):
    return "%s-%02d" % (q[:4], 3 * int(q[-1]))


def quarter_of(m):
    return "%s-Q%d" % (m[:4], (int(m[5:7]) - 1) // 3 + 1)


def intervals(D):
    """T7's units: one per decision. start = month before decision i; end =
    month before decision i+1, or the last full month in S1. Growth: the mean
    of the quarters whose last month is in (start, end]; if none, the quarter
    containing the decision month; an interval with no growth value is
    dropped and counted."""
    last = last_month(D)
    mps = D["mps"]
    out, dropped = [], 0
    for i, r in enumerate(mps):
        dm = r["date"][:4] + "-" + r["date"][4:6]
        start = L.month_add(dm, -1)
        is_last = i + 1 == len(mps)
        end = last if is_last else L.month_add(mps[i + 1]["date"][:4] + "-" + mps[i + 1]["date"][4:6], -1)
        if end > last:
            end = last
        n = L.month_diff(start, end)
        if n < 1 or (is_last and n < 2):
            continue
        a, z = ln_eer(D, "SG", start), ln_eer(D, "SG", end)
        if a is None or z is None:
            dropped += 1
            continue
        qs = [q for q in D["gdp"] if start < quarter_end(q) <= end]
        g = mean([D["gdp"][q] for q in qs]) if qs else D["gdp"].get(quarter_of(dm))
        if g is None:
            dropped += 1
            continue
        lag = [q for q in D["gdp"] if quarter_end(q) <= start]
        g_lag = D["gdp"][max(lag)] if lag else None
        infl = []
        for m in L.months(L.month_add(start, 1), end):
            c, c0 = D["cpi"].get(m), D["cpi"].get(L.month_add(m, -12))
            if c and c0:
                infl.append(100 * (c / c0 - 1))
        out.append({"date": r["date"], "start": start, "end": end, "months": n,
                    "y": 12 * (z - a) / n, "g": g, "g_lag": g_lag,
                    "cpi": mean(infl) if infl else None, "p": int(r["p"]),
                    "slope": r["slope"], "rc": int(r["recentre_score"])})
    return out, dropped


def fine_scores(D):
    """Sensitivity: an ordinal slope, one step per increase or reduction,
    0 at zero, -1 if negative, plus the re-centring score."""
    o, out = None, {}
    for r in D["mps"]:
        s = r["slope"]
        if s == "zero":
            o = 0
        elif s == "negative":
            o = -1
        elif s == "steeper":
            o = 1 if o is None or o < 1 else o + 1
        elif s == "flatter":
            o = (o if o is not None else 1) - 1
        elif s == "same":
            o = 1 if o is None else o
        out[r["date"]] = o + int(r["recentre_score"])
    return out


def rho_d(iv, pkey="p", gkey="g"):
    rows = [x for x in iv if x.get(pkey) is not None and x.get(gkey) is not None]
    if len(rows) < 3:
        return None, None, None, len(rows)
    y = [x["y"] for x in rows]
    rp, rg = spearman(y, [x[pkey] for x in rows]), spearman(y, [x[gkey] for x in rows])
    d = None if rp is None or rg is None else rp - rg
    return rp, rg, d, len(rows)


def bootstrap_d(iv):
    rng = random.Random(L.BOOT_SEED)
    n, ds = len(iv), []
    for _ in range(L.BOOT_N):
        smp = [iv[rng.randrange(n)] for _ in range(n)]
        _, _, d, _ = rho_d(smp)
        if d is not None:
            ds.append(d)
    if not ds:
        return None, None
    ds.sort()

    def q(p):
        k = p * (len(ds) - 1)
        lo = int(math.floor(k))
        hi = min(lo + 1, len(ds) - 1)
        return ds[lo] + (ds[hi] - ds[lo]) * (k - lo)
    return q(0.05), q(0.95)


def t7(D, R, gate, sens):
    iv, dropped = intervals(D)
    rp, rg, d, n = rho_d(iv)
    R["T7_intervals"], R["T7_dropped_count"] = n, dropped
    R["T7_rho_p"], R["T7_rho_g"], R["T7_D"] = rp, rg, d
    lo, hi = bootstrap_d(iv) if n >= 3 else (None, None)
    R["T7_D_lo"], R["T7_D_hi"] = lo, hi
    if not gate:
        R["T7_outcome"], R["T7_reason"] = "NOT SCORED", "gate C failed: the record cannot say"
    elif d is None:
        R["T7_outcome"], R["T7_reason"] = "NOT SCORED", "too few intervals or a constant series"
    elif d >= L.T7_D and rp > 0:
        R["T7_outcome"] = "SURVIVE"
    elif d <= 0:
        R["T7_outcome"] = "FAIL"
    else:
        R["T7_outcome"] = "INCONCLUSIVE"
    fine = fine_scores(D)
    for x in iv:
        x["p_fine"] = fine[x["date"]]
    for variant, sub, pkey, gkey in (("lagged growth", iv, "p", "g_lag"), ("CPI inflation", iv, "p", "cpi"),
                                     ("finer slope coding", iv, "p_fine", "g"),
                                     ("intervals from 2010", [x for x in iv if x["date"] >= L.T7_FROM_2010],
                                      "p", "g")):
        a, b, c, m = rho_d(sub, pkey, gkey)
        for k, v in (("rho_p", a), ("rho_g", b), ("D", c), ("intervals", m)):
            sens.append(["T7", variant, k, v])
    return iv


# ----------------------------------------------------------------- sensitivities
def breadth(D, W, sens):
    for w in ("scored", "long"):
        first, last = W[w][0], W[w][1]
        ms = L.months(first, last)
        count = 0
        for cur, area in L.PARTNERS:
            rows = []
            for a, z in zip(ms, ms[1:]):
                vals = [ln_cross(D, cur, a), ln_cross(D, cur, z), ln_eer(D, "SG", a), ln_eer(D, "SG", z),
                        ln_eer(D, area, a), ln_eer(D, area, z)]
                if None not in vals:
                    rows.append((vals[1] - vals[0], vals[3] - vals[2], vals[5] - vals[4]))
            if len(rows) < 3:
                sens.append(["B", w, f"B_{w}_{cur}_status", "series missing"])
                continue
            db = [r[0] for r in rows]
            vb = cov(db, db)
            pi = cov(db, [-r[2] for r in rows]) / vb
            sigma = cov(db, [r[1] for r in rows]) / vb
            count += pi > sigma
            sens.append(["B", w, f"B_{w}_{cur}_pi", pi])
            sens.append(["B", w, f"B_{w}_{cur}_sigma", sigma])
        sens.append(["B", w, f"B_{w}_partner_larger_count", count])


def q1_sensitivities(D, W, R, sens):
    for cur in L.QUESTION:
        first, last, start, end = W["long"]
        sp = split(D, cur, start, end)
        readable = R.get(f"T1_long_{cur}_ok", False)
        for k in ("b", "S", "P", "R"):
            sens.append(["Q1", "long run" + ("" if readable else " (T1 failed: unreadable)"),
                         f"long_{cur}_{k}", sp[k] if sp else None])
        for w in ("scored", "long"):
            first, last, start, end = W[w]
            for variant, s0, s1, usd, eer in (("single-month endpoints", (start[0],), (end[-1],), "usd", "neer"),
                                              ("end-of-period rates", start, end, "usd_eop", "neer"),
                                              ("real indices", start, end, "usd", "reer")):
                if not D.get(usd) or not D.get(eer):
                    sens.append(["Q1", f"{variant}, {w}", f"{w}_{cur}_status", "not run: series not loaded"])
                    continue
                sp = split(D, cur, s0, s1, usd, eer)
                for k in ("b", "S", "P", "R"):
                    sens.append(["Q1", f"{variant}, {w}", f"{variant.split()[0]}_{w}_{cur}_{k}",
                                 sp[k] if sp else None])


def world_view(D, W, vol, sens):
    if "HK" in vol and "US" in vol:
        sens.append(["world", "long", "HK_US_sd_ratio", vol["HK"] / vol["US"]])
        ms = L.months(W["long"][0], W["long"][1])
        hk = changes(lambda m: ln_eer(D, "HK", m), ms)
        us = changes(lambda m: ln_eer(D, "US", m), ms)
        if len(hk) == len(us):
            sens.append(["world", "long", "HK_US_corr", pearson(hk, us)])
    if "JP" in vol:
        sens.append(["world", "long", "JP_rank", rank_of(vol, "JP")])
    vs = vol_table(D, W["scored"][0], W["scored"][1])
    if "SG" in vs:
        sens.append(["world", "scored", "SG_rank_scored_window", rank_of(vs)])
        sens.append(["world", "scored", "present_scored_window", len(vs)])


# ----------------------------------------------------------------- verdict
def verdict(R):
    parts = []
    for t, cur, name in (("T2", "JPY", "yen"), ("T3", "MYR", "ringgit")):
        o = R[f"{t}_outcome"]
        if o == "NOT SCORED" and R.get(f"{t}_reason", "").startswith("premise"):
            parts.append(f"the Singapore dollar did not rise against the {name}")
        elif o == "NOT SCORED" and "T1" in R.get(f"{t}_reason", ""):
            parts.append(f"the record cannot split the Singapore dollar's rise against the {name}")
        elif o == "SURVIVE":
            parts.append(f"most of the Singapore dollar's rise against the {name} was the {name} "
                         f"falling against everyone")
        elif o == "FAIL":
            parts.append(f"most of the Singapore dollar's rise against the {name} was the Singapore "
                         f"dollar rising against everyone")
        elif o == "INCONCLUSIVE":
            parts.append(f"neither side accounts for most of the Singapore dollar's rise against the {name}")
        else:
            parts.append(f"the record cannot split the Singapore dollar's rise against the {name}")
    R["verdict_A_yen"], R["verdict_A_ringgit"] = parts
    o = R["T7_outcome"]
    if not R["gateC_pass"]:
        b = "the record cannot say whether the broad path followed MAS or growth"
    elif o == "SURVIVE":
        b = "the broad path followed MAS's decisions more closely than growth"
    elif o == "FAIL":
        b = "the broad path followed growth at least as closely as MAS's decisions"
    elif o == "INCONCLUSIVE":
        b = "the broad path followed MAS's decisions a little more closely than growth, by less than the line"
    else:
        b = "the record cannot say whether the broad path followed MAS or growth"
    R["verdict_B"] = b
    R["verdict"] = f"{parts[0][0].upper() + parts[0][1:]}; {parts[1]}; {b}."
    if R["T4_outcome"] == "NOT SCORED" and "gate C" in R.get("T4_reason", ""):
        R["verdict_T4"] = "the record cannot say whether the Singapore dollar was the steadiest"


def scorecard(R, conf):
    scored = [t for t in L.SCORED if R[f"{t}_outcome"] in ("SURVIVE", "FAIL", "INCONCLUSIVE")]
    R["scored_tests"] = " ".join(scored)
    R["n_scored"] = len(scored)
    R["n_held"] = sum(R[f"{t}_outcome"] == "SURVIVE" for t in scored)
    for t in L.SCORED:
        R[f"conf_{t}"] = conf.get(t) if conf.get(t) is not None else "[JACOB]"
    cs = [conf.get(t) for t in scored]
    if scored and all(c is not None for c in cs):
        R["expected_held"] = sum(cs)
        R["brier"] = mean([(c - (R[f"{t}_outcome"] == "SURVIVE")) ** 2 for c, t in zip(cs, scored)])
    else:
        R["expected_held"] = None
        R["brier"] = None


def run(P):
    D = load(P["out"])
    W = windows(D)
    R, sens = {}, []
    R["window_scored"] = f"{W['scored'][0]} to {W['scored'][1]}"
    R["window_long"] = f"{W['long'][0]} to {W['long'][1]}"
    t1(D, W, R)
    share_test(D, W, R, "T2", "JPY")
    share_test(D, W, R, "T3", "MYR")
    gate = gate_c(D, R)
    vol = t4(D, W, R, gate)
    iv = t7(D, R, gate, sens)
    breadth(D, W, sens)
    q1_sensitivities(D, W, R, sens)
    world_view(D, W, vol, sens)
    verdict(R)
    scorecard(R, L.confidences(P["thesis"]))
    L.write_csv(os.path.join(P["out"], "tests.csv"), ["key", "value"], sorted(R.items()))
    L.write_csv(os.path.join(P["out"], "sensitivities.csv"), ["test", "variant", "key", "value"], sens)
    L.write_csv(os.path.join(P["out"], "intervals.csv"),
                ["date", "start", "end", "months", "y", "g", "g_lag", "cpi", "p", "p_fine"],
                [[x["date"], x["start"], x["end"], x["months"], x["y"], x["g"], x["g_lag"], x["cpi"], x["p"],
                  x["p_fine"]] for x in iv])
    return R


def main():
    a = L.args("sgd step 11: the scored tests, gate C, sensitivities, verdict")
    P = L.paths(a.root)
    R = run(P)
    for t in L.SCORED:
        print(f"  {t}: {R[t + '_outcome']}")
    print(f"  gate C: {'pass' if R['gateC_pass'] else 'FAIL'}")


if __name__ == "__main__":
    main()
