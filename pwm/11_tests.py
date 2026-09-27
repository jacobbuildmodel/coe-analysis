"""
11_tests.py -- T1-T5 exactly as THESIS.md states them, every listed
sensitivity, the two-part verdict (section 8) and the scorecard.

Reads only ROOT/out/ (written by 10_load.py) and the confidences in THESIS.md
("Confidence at seal: NN%" under each test; while they read [JACOB], the
Brier score and the expected count are reported as not set).

Method, as THESIS fixes it:
  * group value in a June: equal-weight mean, across the group's titles, of
    log 25th-percentile gross wage; gap: covered group minus comparison set C;
  * missing-year rule: a title missing in any scored June of its group's
    window (pre-period plus post-period Junes; for C, every June any group
    scores) is dropped from that group, in every June;
  * every regression is OLS with HC1 standard errors; the 90 per cent
    interval is statsmodels' conf_int(alpha=0.10) (normal critical value);
  * outcomes: SURVIVE, FAIL, INCONCLUSIVE or NOT SCORED. A prediction holds
    when it SURVIVES; NOT SCORED drops out of the count and the Brier score.

Writes ROOT/out/tests.csv (key, value), group_values.csv, t5_ratios.csv,
t4_panel.csv, sensitivities.csv and dropped_titles.csv.
"""
import math
import os
import re

import numpy as np
import pandas as pd
import statsmodels.api as sm

import pwmlib as L

MEAS = ["p25_gross", "med_gross", "p75_gross", "p25_basic", "med_basic", "p75_basic", "n_covered"]
SURVIVE, FAIL, INCONC, NOTSC = "SURVIVE", "FAIL", "INCONCLUSIVE", "NOT SCORED"


# ------------------------------------------------------------------ inputs
def load(out):
    lines = pd.read_csv(os.path.join(out, "ows_lines.csv"), dtype={"code": str})
    for m in MEAS:
        lines[m] = pd.to_numeric(lines[m], errors="coerce").astype(float)
    lfs = pd.read_csv(os.path.join(out, "lfs_median.csv"))
    t4s = pd.read_csv(os.path.join(out, "t4_series.csv"), dtype={"count": float})
    t4c = dict(pd.read_csv(os.path.join(out, "t4_choice.csv"), dtype=str).values)
    return lines, lfs, t4s, t4c


def confidences(thesis_path):
    text = open(thesis_path, encoding="utf-8").read()
    res = {}
    for t in ("T1", "T2", "T3", "T4", "T5"):
        sec = re.search(rf"^### {t}\..*?(?=^### |\Z)", text, re.S | re.M)
        m = re.search(r"Confidence at seal: `?(\d+(?:\.\d+)?)%", sec.group(0)) if sec else None
        res[t] = float(m.group(1)) / 100 if m else None
    return res


# ------------------------------------------------------------- group values
def scored_junes(group):
    if group in L.COVERED:
        return set(L.PRE[group]) | set(L.POST[group])
    return set().union(*[set(L.PRE[g]) | set(L.POST[g]) for g in L.COVERED])


def select(lines, series=("main",), measure="p25_gross", drop_c=None):
    """Rows in use after the missing-year rule. Returns (rows, dropped)."""
    d = lines[lines["series"].isin(series)].copy()
    d["grp"] = np.where(d["side"] == "comparison", "C", d["group"])
    if drop_c:
        d = d[d["group"] != drop_c]
    dropped = []
    keep = np.ones(len(d), bool)
    for (grp, code, title), sub in d.groupby(["grp", "code", "title"]):
        S = scored_junes(grp if grp != "C" else "C")
        bad = sub[sub["june"].isin(S) & sub[measure].isna()]
        if len(bad):
            keep &= ~((d["grp"] == grp) & (d["code"] == code) & (d["title"] == title)).values
            dropped.append((grp, code, title, measure, ";".join(str(j) for j in sorted(bad["june"]))))
    return d[keep], dropped


def values(rows, measure="p25_gross", weights=False, log=True):
    """{grp: {june: value}}: mean of log measure (or level) across titles."""
    res = {}
    for (grp, june), sub in rows.groupby(["grp", "june"]):
        x = sub[measure].astype(float)
        ok = x.notna() & (x > 0)
        if weights:
            ok &= sub["n_covered"].notna()
        if not ok.any():
            continue
        v = np.log(x[ok]) if log else x[ok]
        w = sub.loc[ok, "n_covered"].astype(float) if weights else None
        res.setdefault(grp, {})[int(june)] = float(np.average(v, weights=w))
    return res


def gaps(vals):
    C = vals.get("C", {})
    return {g: {j: v - C[j] for j, v in vals.get(g, {}).items() if j in C} for g in L.COVERED}


# -------------------------------------------------------------- regression
def ols(y, X):
    r = sm.OLS(np.asarray(y, float), np.asarray(X, float)).fit(cov_type="HC1")
    return r.params, r.conf_int(alpha=0.10), r.cov_params()


def slope(years, y):
    b, ci, _ = ols(y, sm.add_constant(np.asarray(years, float)))
    return b[1], ci[1][0], ci[1][1]


def t1(gap, pre=None):
    pre = pre or L.PRE
    res = {}
    for g in L.COVERED:
        yrs = [j for j in pre[g] if j in gap[g]]
        if len(yrs) < L.MIN_PRE:
            res[g] = {"n": len(yrs), "run": False}
            continue
        s, lo, hi = slope(yrs, [gap[g][j] for j in yrs])
        res[g] = {"n": len(yrs), "run": True, "slope": s, "lo": lo, "hi": hi, "pass": bool(abs(s) < L.T1_LINE)}
    ran = [g for g in L.COVERED if res[g]["run"]]
    if not ran:
        outcome = NOTSC
    else:
        outcome = SURVIVE if all(res[g]["pass"] for g in ran) else FAIL
    passing = [g for g in ran if res[g]["pass"]]
    return res, outcome, passing


def did(gap, groups, pre=None, post=None):
    """Per group: mean post gap minus mean pre gap, CI from gap ~ post (HC1);
    pooled: equal-weight mean, CI from the stacked regression."""
    pre, post = pre or L.PRE, post or L.POST
    res, blocks = {}, []
    for g in groups:
        a = [j for j in pre[g] if j in gap[g]]
        b = [j for j in post[g] if j in gap[g]]
        if not a or not b:
            res[g] = None
            continue
        y = [gap[g][j] for j in a + b]
        D = [0.0] * len(a) + [1.0] * len(b)
        est = np.mean([gap[g][j] for j in b]) - np.mean([gap[g][j] for j in a])
        _, ci, _ = ols(y, sm.add_constant(np.asarray(D)))
        res[g] = {"est": est, "lo": ci[1][0], "hi": ci[1][1]}
        blocks.append((g, y, D))
    gs = [g for g, _, _ in blocks]
    if not gs:
        return res, None
    k = len(gs)
    Y, X = [], []
    for i, (g, y, D) in enumerate(blocks):
        for yy, dd in zip(y, D):
            row = [0.0] * (2 * k)
            row[i], row[k + i] = 1.0, dd
            Y.append(yy)
            X.append(row)
    b, _, V = ols(Y, X)
    w = np.r_[np.zeros(k), np.ones(k) / k]
    est = float(w @ b)
    se = math.sqrt(float(w @ np.asarray(V) @ w))
    z = 1.6448536269514722
    return res, {"est": est, "lo": est - z * se, "hi": est + z * se, "groups": gs}


def t2_outcome(res, pooled, groups):
    if not groups or pooled is None:
        return NOTSC
    ests = [res[g]["est"] for g in groups if res.get(g)]
    if pooled["est"] < L.T2_FAIL or any(e <= 0 for e in ests):
        return FAIL
    if pooled["est"] >= L.T2_SURVIVE and all(e > 0 for e in ests):
        return SURVIVE
    return INCONC


def t3(vals_c, lfs):
    C = vals_c
    start = [C[j] for j in (2010, 2011, 2012) if j in C]
    end = [C[j] for j in (2017, 2018, 2019) if j in C]
    mid = {int(r.year): math.log(r.median_excl_emp_cpf) for r in lfs.itertuples()
           if r.median_excl_emp_cpf == r.median_excl_emp_cpf}
    ms = [mid[j] for j in (2010, 2011, 2012) if j in mid]
    me = [mid[j] for j in (2017, 2018, 2019) if j in mid]
    if len(start) < 2 or not end or not ms or not me:
        return {"computable": False}, NOTSC
    gc = np.mean(end) - np.mean(start)
    gm = np.mean(me) - np.mean(ms)
    short = gm - gc
    return ({"computable": True, "start_c": np.mean(start), "end_c": np.mean(end), "growth_c": gc,
             "growth_mid": gm, "shortfall": short, "n_start": len(start), "n_end": len(end)},
            SURVIVE if short < L.T3_LINE else FAIL)


def t4(t4s, t4c, which="main"):
    sid = t4c.get(which, "none")
    if sid in (None, "none"):
        return {"series": "none"}, NOTSC, []
    s = t4s[t4s["series"] == sid]
    cnt = {(u, int(y)): float(c) for u, y, c in s[["unit", "year", "count"]].itertuples(index=False)}
    first = int(t4c[f"{sid}_first_year"])
    panel = []
    res = {"series": sid, "first_year": first, "panel": panel}
    for g in L.COVERED:
        pre = [y for y in range(first, L.PRE_END[g] + 1) if (g, y) in cnt and ("comparison", y) in cnt]
        post = [y for y in L.POST[g] if (g, y) in cnt and ("comparison", y) in cnt]
        gap = {y: math.log(cnt[(g, y)]) - math.log(cnt[("comparison", y)]) for y in pre + post}
        for y in sorted(gap):
            panel.append([sid, g, y, "pre" if y in pre else "post", gap[y]])
        admitted = t4c.get(f"{sid}_{g}_admitted") == "True"
        r = {"pre_years": len(pre), "admitted": admitted}
        if pre and post:
            D = [0.0] * len(pre) + [1.0] * len(post)
            _, ci, _ = ols([gap[y] for y in pre + post], sm.add_constant(np.asarray(D)))
            r.update(est=np.mean([gap[y] for y in post]) - np.mean([gap[y] for y in pre]),
                     lo=ci[1][0], hi=ci[1][1])
        if admitted:
            s_, lo_, hi_ = slope(pre, [gap[y] for y in pre])
            r.update(pretrend=s_, pretrend_pass=bool(abs(s_) < L.T4_PRETREND))
            r["status"] = "scored" if r["pretrend_pass"] else "dropped: pre-trend"
        else:
            r["status"] = "described, not scored: fewer than 4 pre-period years"
        res[g] = r
    scored = [g for g in L.COVERED if res[g]["status"] == "scored"]
    if not scored:
        return res, NOTSC, scored
    ests = [res[g]["est"] for g in scored]
    if all(e > L.T4_SURVIVE for e in ests):
        out = SURVIVE
    elif any(e <= L.T4_FAIL for e in ests):
        out = FAIL
    else:
        out = INCONC
    return res, out, scored


def t5(rows, groups):
    """T5 reads T2's rows; a title with no basic wage in any post-period June
    is also dropped here (the missing-year rule on the basic wage). A group
    left with no value in a post-period June has not shown the rung: FAIL."""
    bad = {(grp, c, t) for (grp, c, t), sub in rows.groupby(["grp", "code", "title"])
           if grp in L.POST and (sub["june"].isin(L.POST[grp]) & sub["p25_basic"].isna()).any()}
    keep = [(g, c, t) not in bad for g, c, t in zip(rows["grp"], rows["code"], rows["title"])]
    lv = values(rows[keep], "p25_basic", log=False)
    ratios = {}
    for g in groups:
        for y, rung in L.RUNG[g].items():
            if y in lv.get(g, {}):
                ratios[(g, y)] = lv[g][y] / rung
    if not groups:
        return ratios, NOTSC
    need = [(g, y) for g in groups for y in L.RUNG[g]]
    if any(k not in ratios for k in need):
        return ratios, FAIL
    return ratios, SURVIVE if all(v >= L.T5_LINE for v in ratios.values()) else FAIL


# ----------------------------------------------------------------- verdict
def verdict(o, t1res, t4res, t4scored):
    ran = [g for g in L.COVERED if t1res[g]["run"]]
    if o["T1"] == NOTSC or not any(t1res[g]["pass"] for g in ran):
        a = "the record cannot say what the ladder did"
    elif o["T2"] == FAIL:
        a = "the ladder did not measurably lift pay at the bottom of the jobs it covered"
    elif o["T2"] == SURVIVE and o["T4"] != NOTSC and all(t4res[g]["est"] >= 0 for g in t4scored):
        a = "covered jobs look more like monopsony"
    elif o["T2"] == SURVIVE and o["T4"] == FAIL:
        a = "covered jobs look more like a competitive market"
    else:
        a = "the record cannot tell the two models apart"
    b = {SURVIVE: "the rest of the bottom kept pace", FAIL: "the rest of the bottom fell behind",
         NOTSC: "the record cannot say whether the rest of the bottom kept pace"}[o["T3"]]
    return a, b


def scorecard(o, conf):
    scored = [t for t in ("T1", "T2", "T3", "T4", "T5") if o[t] != NOTSC]
    held = [t for t in scored if o[t] == SURVIVE]
    res = {"n_scored": len(scored), "n_held": len(held), "scored_tests": " ".join(scored)}
    if all(conf.get(t) is not None for t in scored) and scored:
        res["expected_held"] = sum(conf[t] for t in scored)
        res["brier"] = float(np.mean([(conf[t] - (1.0 if t in held else 0.0)) ** 2 for t in scored]))
    else:
        res["expected_held"] = "not set: confidences [JACOB]"
        res["brier"] = "not set: confidences [JACOB]"
    return res


# --------------------------------------------------------------------- run
def run(lines, lfs, t4s, t4c, conf):
    T, sens, dropped_all = {}, [], []
    rows, dropped = select(lines)
    dropped_all += dropped
    vals = values(rows)
    gap = gaps(vals)
    t1res, o1, passing = t1(gap)
    groups = passing if o1 != NOTSC else []
    t2res, pooled = did(gap, groups)
    o2 = t2_outcome(t2res, pooled, groups)
    t3res, o3 = t3(vals.get("C", {}), lfs)
    t4res, o4, t4scored = t4(t4s, t4c, "main")
    ratios, o5 = t5(rows, groups)
    o = {"T1": o1, "T2": o2, "T3": o3, "T4": o4, "T5": o5}
    for g in L.COVERED:
        r = t1res[g]
        T[f"T1_{g}_pre_junes"] = r["n"]
        if r["run"]:
            T.update({f"T1_{g}_slope": r["slope"], f"T1_{g}_lo": r["lo"], f"T1_{g}_hi": r["hi"],
                      f"T1_{g}_pass": r["pass"]})
        else:
            T[f"T1_{g}_pass"] = "not run: fewer than 4 pre-period Junes"
    T["T1_groups_passing"] = " ".join(passing)
    for g in groups:
        if t2res.get(g):
            T.update({f"T2_{g}_est": t2res[g]["est"], f"T2_{g}_lo": t2res[g]["lo"], f"T2_{g}_hi": t2res[g]["hi"]})
    if pooled:
        T.update({"T2_pooled": pooled["est"], "T2_pooled_lo": pooled["lo"], "T2_pooled_hi": pooled["hi"]})
    T["T2_groups_scored"] = " ".join(groups)
    for k in ("start_c", "end_c", "growth_c", "growth_mid", "shortfall", "n_start", "n_end"):
        if k in t3res:
            T[f"T3_{k}"] = t3res[k]
    T["T4_series"] = t4res.get("series", "none")
    if T["T4_series"] == "none":
        T["T4_reason"] = "no series qualifies (THESIS section 4): " + L.GAP
    for g in L.COVERED:
        r = t4res.get(g)
        if not r:
            continue
        T[f"T4_{g}_status"] = r["status"]
        T[f"T4_{g}_pre_years"] = r["pre_years"]
        for k in ("est", "lo", "hi", "pretrend"):
            if k in r:
                T[f"T4_{g}_{k}"] = r[k]
    T["T4_industries_scored"] = " ".join(t4scored)
    for (g, y), v in sorted(ratios.items()):
        T[f"T5_{g}_{y}_ratio"] = v
    if ratios and groups:
        T["T5_min_ratio"] = min(v for (g, _), v in ratios.items() if g in groups)
    for t in o:
        T[f"{t}_outcome"] = o[t]
    a, b = verdict(o, t1res, t4res, t4scored)
    T["verdict_A"], T["verdict_B"] = a, b
    T["verdict"] = a[0].upper() + a[1:] + "; " + b + "."
    for t in o:
        T[f"conf_{t}"] = ("not scored" if o[t] == NOTSC else
                          conf.get(t) if conf.get(t) is not None else "[JACOB]")
    T.update(scorecard(o, conf))

    # ---- sensitivities, reported, not scored
    def add(test, variant, key, value):
        sens.append([test, variant, key, value])

    # T1
    pre_no09 = {g: [j for j in L.PRE[g] if j != 2009] for g in L.COVERED}
    r, oo, _ = t1(gap, pre_no09)
    for g in L.COVERED:
        add("T1", "without June 2009", f"{g}_slope", r[g].get("slope", "not run: fewer than 4 Junes"))
    add("T1", "without June 2009", "outcome", oo)
    after = {"cleaning": [2011, 2012], "security": list(range(2011, 2015)), "landscape": list(range(2011, 2015))}
    r, oo, _ = t1(gap, after)
    for g in L.COVERED:
        add("T1", "Junes after the last pre-period break", f"{g}_slope",
            r[g].get("slope", "not run: too few Junes (THESIS section 5)"))
    add("T1", "2007-2008 added", "outcome", "not run: June 2007 and 2008 are PDF only, extracted after the seal")
    add("T2", "2007-2008 added", "outcome", "not run: June 2007 and 2008 are PDF only, extracted after the seal")

    # T2 variants on the same scored groups
    def t2var(variant, vals_v, pre=None, post=None):
        gp = gaps(vals_v)
        rr, pp = did(gp, groups, pre, post)
        for g in groups:
            if rr.get(g):
                add("T2", variant, f"{g}_est", rr[g]["est"])
        add("T2", variant, "pooled", pp["est"] if pp else "not run")
        add("T2", variant, "outcome", t2_outcome(rr, pp, groups))

    rb, _ = select(lines, measure="p25_basic")
    t2var("basic instead of gross", values(rb, "p25_basic"))
    rm, _ = select(lines, measure="med_gross")
    t2var("median instead of 25th percentile", values(rm, "med_gross"))
    t2var("dropping 2022", vals, post={g: [j for j in L.POST[g] if j != 2022] for g in L.COVERED})
    for c in sorted(lines.loc[lines["side"] == "comparison", "group"].unique()):
        rc, _ = select(lines, drop_c=c)
        t2var(f"leaving out {c[2:]}", values(rc))
    t2var("first transition June counted as post", vals,
          post={g: sorted(L.POST[g] + [L.TRANSITION[g][0]]) for g in L.COVERED})
    ra, dra = select(lines, series=("main", "sensitivity"))
    dropped_all += [d + ("all successors",) for d in dra]
    vals_all = values(ra)
    t2var("all successors of a grade split averaged", vals_all)
    t2var("Number Covered weights", values(rows, weights=True))

    # T4 sensitivity: the LFS series, when both qualify
    if t4c.get("sensitivity", "none") != "none":
        r4, o4s, sc4 = t4(t4s, t4c, "sensitivity")
        for g in L.COVERED:
            if g in r4 and "est" in r4[g]:
                add("T4", f"{r4['series']} series", f"{g}_est", r4[g]["est"])
        add("T4", f"{r4['series']} series", "outcome", o4s)
    else:
        add("T4", "LFS residents series", "outcome", "not run: no second series qualifies")

    # T5: all successors against the same lowest rung
    r5, o5s = t5(ra, groups)
    for (g, y), v in sorted(r5.items()):
        add("T5", "all successors averaged", f"{g}_{y}_ratio", v)
    add("T5", "all successors averaged", "outcome", o5s)

    gv = []
    for g in list(L.COVERED) + ["C"]:
        for j, v in sorted(vals.get(g, {}).items()):
            gv.append([j, g, v, gap[g].get(j) if g in gap else None,
                       int(rows[(rows["grp"] == g) & (rows["june"] == j)]["p25_gross"].notna().sum())])
    return T, sens, gv, dropped_all, ratios, t4res.get("panel", [])


def main():
    a = L.args("PWM step 11: tests")
    P = L.paths(a.root)
    out = P["out"]
    lines, lfs, t4s, t4c = load(out)
    T, sens, gv, dropped, ratios, panel = run(lines, lfs, t4s, t4c, confidences(P["thesis"]))
    L.write_csv(os.path.join(out, "tests.csv"), ["key", "value"], [[k, v] for k, v in T.items()])
    L.write_csv(os.path.join(out, "sensitivities.csv"), ["test", "variant", "key", "value"], sens)
    L.write_csv(os.path.join(out, "group_values.csv"), ["june", "group", "value", "gap", "n_titles"], gv)
    L.write_csv(os.path.join(out, "t5_ratios.csv"), ["group", "june", "rung", "ratio"],
                [[g, y, L.RUNG[g][y], v] for (g, y), v in sorted(ratios.items())])
    L.write_csv(os.path.join(out, "dropped_titles.csv"), ["group", "code", "title", "measure", "missing_junes", "variant"],
                [list(d) + ([] if len(d) == 6 else ["main"]) for d in dropped])
    L.write_csv(os.path.join(out, "t4_panel.csv"), ["series", "industry", "year", "window", "log_gap"], panel)
    for t in ("T1", "T2", "T3", "T4", "T5"):
        print(f"  {t}: {T[f'{t}_outcome']}")
    print(f"  verdict: {T['verdict']}")


if __name__ == "__main__":
    main()
