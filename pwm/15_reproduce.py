"""
15_reproduce.py -- recompute every scored number by a different code path and
assert it agrees with out/tests.csv as RESULTS.md prints it.

Different path, on purpose:
  * raw OWS workbooks read cell by cell with openpyxl / xlrd (no pandas); the
    measure columns found by scanning header rows for their words, the line
    matched through OCCUPATION_MAP.csv read with the csv module;
  * group values, the missing-year rule and every mean as plain loops;
  * regressions by numpy.linalg.lstsq with the HC1 sandwich written out, the
    90 per cent critical value from statistics.NormalDist (no statsmodels);
  * T4 re-discovers its candidate series in raw/ and re-applies the priority
    rule from scratch.
Shared with 10-14: only raw/, the map, T4_LFS_LINES.csv and pwmlib's
constants (windows, rungs, thresholds, labels) and the guard.
"""
import csv
import math
import os
import re
import statistics
import sys

import numpy as np
import openpyxl
import xlrd

import pwmlib as L

Z90 = statistics.NormalDist().inv_cdf(0.95)


def cells(path):
    """Sheet as a list of rows of raw cell values."""
    if path.endswith(".xls"):
        sh = xlrd.open_workbook(path).sheet_by_index(0)
        return [[sh.cell_value(i, j) for j in range(sh.ncols)] for i in range(sh.nrows)]
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["T4"] if "T4" in wb.sheetnames else wb[wb.sheetnames[0]]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    wb.close()
    return rows


def s(v):
    return re.sub(r"\s+", " ", str(v)).strip() if v is not None else ""


def key(t):
    t = t.replace("\u2019", "'").replace("\u2018", "'").replace("\u2013", "-").replace("\u2014", "-")
    return "".join(ch for ch in t.lower() if ch.isalnum() and ord(ch) < 128)


def num(v):
    try:
        return float(str(v).replace(",", "").strip())
    except ValueError:
        return None


def table(raw, year):
    """{(code, key(title)): {measure: value}} for the all-industries table."""
    out = {}
    if year <= 2011:
        ext = "xls" if year == 2009 else "xlsx"
        files = [(os.path.join(raw, f"w1_ows_{year}_occupation_{k}.{ext}"), k) for k in ("gross", "basic")]
    else:
        files = [(os.path.join(raw, f"w1_ows_{year}_occupation.xlsx"), None)]
    for path, kind in files:
        rows = cells(path)
        width = max(len(r) for r in rows)
        rows = [list(r) + [None] * (width - len(r)) for r in rows]
        top = [i for i, r in enumerate(rows[:15]) if any(s(c).upper().startswith("SSOC") for c in r)][0]
        col = {}
        for i in range(top, top + 3):
            for j, c in enumerate(rows[i]):
                t = s(c).lower()
                if kind is None:
                    for k in ("basic", "gross"):
                        if t == f"{k} wage":
                            col[f"p25_{k}"], col[f"p50_{k}"], col[f"p75_{k}"] = j, j + 1, j + 2
                else:
                    if t.startswith(("first", "25th")):
                        col[f"p25_{kind}"] = j
                    elif t.startswith("median"):
                        col[f"p50_{kind}"] = j
                    elif t.startswith(("third", "75th")):
                        col[f"p75_{kind}"] = j
                if t.startswith("number"):
                    col.setdefault("n", j)
        # code and title columns: the columns right of or under the headers
        # that actually hold 4-5 digit codes and titles
        def is_code(v):
            return bool(re.fullmatch(r"\d{4,5}", s(v).split(".")[0])) and s(v) != ""
        ccol = max(range(3), key=lambda j: sum(1 for r in rows[top + 1:] if is_code(r[j])))
        tcol = max(range(ccol + 1, ccol + 3),
                   key=lambda j: sum(1 for r in rows[top + 1:] if is_code(r[ccol]) and re.search("[A-Za-z]", s(r[j]))))
        last = None
        for r in rows[top + 1:]:
            code = s(r[ccol]).split(".")[0]
            title = s(r[tcol])
            if not re.fullmatch(r"\d{4,5}", code):
                if title.startswith("(") and last is not None:
                    new = (last[0], key(last[1] + " " + title))
                    out[new] = out.pop((last[0], key(last[1])))
                    last = (last[0], last[1] + " " + title)
                continue
            d = out.setdefault((code, key(title)), {})
            for m, j in col.items():
                if m == "n" and "n" in d:
                    continue
                d[m] = num(r[j])
            last = (code, title)
    return out


def find(tab, code, title):
    k = (code, key(title))
    if k in tab:
        return tab[k]
    hits = [v for (c, t), v in tab.items() if c == code and t.startswith(key(title)[:25])]
    return hits[0]


def lines(raw):
    with open(L.MAP, newline="", encoding="utf-8") as f:
        mp = [r for r in csv.DictReader(f) if r["june"] and r["series"] in ("main", "sensitivity")
              and r["in_all_industries_table"] == "yes"]
    tabs, res = {}, []
    for r in mp:
        y = int(r["june"])
        if y not in tabs:
            tabs[y] = table(raw, y)
        v = find(tabs[y], r["ssoc_code"], r["title_as_published"])
        res.append({"june": y, "grp": "C" if r["group"].startswith("C ") else r["group"],
                    "group": r["group"], "line": (r["ssoc_code"], r["title_as_published"]),
                    "series": r["series"], **v})
    return res


def window(grp):
    if grp == "C":
        return set().union(*[set(L.PRE[g]) | set(L.POST[g]) for g in L.COVERED])
    return set(L.PRE[grp]) | set(L.POST[grp])


def gvalues(ls, series, measure="p25_gross", log=True):
    use = [x for x in ls if x["series"] in series]
    bad = {(x["grp"], x["line"]) for x in use if x["june"] in window(x["grp"]) and not x.get(measure)}
    out = {}
    for x in use:
        if (x["grp"], x["line"]) in bad or not x.get(measure):
            continue
        out.setdefault(x["grp"], {}).setdefault(x["june"], []).append(
            math.log(x[measure]) if log else x[measure])
    return {g: {j: sum(v) / len(v) for j, v in d.items()} for g, d in out.items()}


def hc1(y, X):
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    n, k = X.shape
    inv = np.linalg.inv(X.T @ X)
    V = inv @ (X.T * e ** 2) @ X @ inv * n / (n - k)
    return b, V


def reproduce(root):
    P = L.paths(root)
    raw = L.guard(P["raw"])
    R = {}
    ls = lines(raw)
    V = gvalues(ls, ("main",))
    gap = {g: {j: v - V["C"][j] for j, v in V.get(g, {}).items() if j in V["C"]} for g in L.COVERED}
    passing, ran = [], []
    for g in L.COVERED:
        yrs = [j for j in L.PRE[g] if j in gap[g]]
        R[f"T1_{g}_pre_junes"] = len(yrs)
        if len(yrs) < L.MIN_PRE:
            continue
        ran.append(g)
        b, Vc = hc1([gap[g][j] for j in yrs], [[1.0, j] for j in yrs])
        se = math.sqrt(Vc[1, 1])
        R[f"T1_{g}_slope"], R[f"T1_{g}_lo"], R[f"T1_{g}_hi"] = b[1], b[1] - Z90 * se, b[1] + Z90 * se
        if abs(b[1]) < L.T1_LINE:
            passing.append(g)
    R["T1_outcome"] = "NOT SCORED" if not ran else ("SURVIVE" if len(passing) == len(ran) else "FAIL")
    groups = passing
    ests, Y, X = {}, [], []
    k = len(groups)
    for i, g in enumerate(groups):
        pre = [gap[g][j] for j in L.PRE[g] if j in gap[g]]
        post = [gap[g][j] for j in L.POST[g] if j in gap[g]]
        ests[g] = sum(post) / len(post) - sum(pre) / len(pre)
        b, Vc = hc1(pre + post, [[1.0, 0.0]] * len(pre) + [[1.0, 1.0]] * len(post))
        se = math.sqrt(Vc[1, 1])
        R[f"T2_{g}_est"], R[f"T2_{g}_lo"], R[f"T2_{g}_hi"] = ests[g], b[1] - Z90 * se, b[1] + Z90 * se
        for yv, d in [(v, 0.0) for v in pre] + [(v, 1.0) for v in post]:
            row = [0.0] * (2 * k)
            row[i], row[k + i] = 1.0, d
            Y.append(yv)
            X.append(row)
    if groups:
        b, Vc = hc1(Y, X)
        w = np.r_[np.zeros(k), np.ones(k) / k]
        pooled, se = float(w @ b), math.sqrt(float(w @ Vc @ w))
        R["T2_pooled"], R["T2_pooled_lo"], R["T2_pooled_hi"] = pooled, pooled - Z90 * se, pooled + Z90 * se
        if pooled < L.T2_FAIL or any(e <= 0 for e in ests.values()):
            R["T2_outcome"] = "FAIL"
        elif pooled >= L.T2_SURVIVE:
            R["T2_outcome"] = "SURVIVE"
        else:
            R["T2_outcome"] = "INCONCLUSIVE"
    else:
        R["T2_outcome"] = "NOT SCORED"

    # T3
    C = V["C"]
    with open(os.path.join(raw, "w1c_lfs_median_income.csv"), newline="", encoding="utf-8") as f:
        mid = {int(r["year"]): math.log(float(r["median_income_excl_emp_cpf"]))
               for r in csv.DictReader(f) if r["median_income_excl_emp_cpf"].strip()}
    st = [C[j] for j in (2010, 2011, 2012) if j in C]
    en = [C[j] for j in (2017, 2018, 2019) if j in C]
    if len(st) >= 2 and en:
        gc = sum(en) / len(en) - sum(st) / len(st)
        ms = [mid[j] for j in (2010, 2011, 2012) if j in mid]
        me = [mid[j] for j in (2017, 2018, 2019) if j in mid]
        gm = sum(me) / len(me) - sum(ms) / len(ms)
        R.update({"T3_growth_c": gc, "T3_growth_mid": gm, "T3_shortfall": gm - gc,
                  "T3_outcome": "SURVIVE" if gm - gc < L.T3_LINE else "FAIL"})
    else:
        R["T3_outcome"] = "NOT SCORED"

    # T4: rediscover and re-apply the priority rule
    series = {}
    for name in sorted(os.listdir(raw)):
        if not name.endswith(".csv"):
            continue
        with open(os.path.join(raw, name), newline="", encoding="utf-8") as f:
            rd = list(csv.reader(f))
        if not rd or rd[0][0] != "DataSeries":
            continue
        yrs = [(i, int(h)) for i, h in enumerate(rd[0]) if h.strip().isdigit() and len(h.strip()) == 4]
        inblock, got = False, {}
        for row in rd[1:]:
            if not row[0].startswith(" "):
                inblock = bool(re.search("worker|employ", row[0], re.I))
            elif inblock:
                for unit, labels in L.T4_LINES.items():
                    if row[0].strip() in labels:
                        for i, y in yrs:
                            v = num(row[i])
                            if v is not None:
                                got.setdefault(unit, {}).setdefault(y, 0.0)
                                got[unit][y] += v
        if set(got) == set(L.T4_LINES):
            series["workers"] = got
    if os.path.exists(P["lfs_lines"]):
        with open(P["lfs_lines"], newline="", encoding="utf-8") as f:
            spec = list(csv.DictReader(f))
        if spec:
            with open(os.path.join(raw, spec[0]["file"]), newline="", encoding="utf-8") as f:
                data = list(csv.DictReader(f))
            got = {}
            for sp in spec:
                cond = [kv.split("=", 1) for kv in sp["filters"].split(";") if kv]
                for r in data:
                    if r[sp["occupation_column"]].strip() == sp["occupation"] and all(r[a].strip() == b for a, b in cond):
                        v = num(r[sp["count_column"]])
                        if v is not None:
                            got.setdefault(sp["unit"], {}).setdefault(int(r["year"]), 0.0)
                            got[sp["unit"]][int(r["year"])] += v
            series["lfs"] = got

    def admitted(sr):
        comp = {y for y, v in sr.get("comparison", {}).items() if v > 0}
        first = min(y for u in sr.values() for y, v in u.items() if v > 0)
        adm = {}
        for g in L.COVERED:
            have = {y for y, v in sr.get(g, {}).items() if v > 0} & comp
            pre = sorted(y for y in have if first <= y <= L.PRE_END[g])
            adm[g] = (pre, all(y in have for y in L.POST[g]) and len(pre) >= L.MIN_PRE)
        return adm

    main = next((sid for sid in ("workers", "lfs") if sid in series and
                 any(a for _, a in admitted(series[sid]).values())), None)
    if main is None:
        R["T4_outcome"] = "NOT SCORED"
    else:
        sr, scored = series[main], []
        for g, (pre, ok) in admitted(sr).items():
            gp = {y: math.log(sr[g][y]) - math.log(sr["comparison"][y]) for y in pre + L.POST[g]
                  if y in sr.get(g, {}) and y in sr["comparison"]}
            post = [y for y in L.POST[g] if y in gp]
            if pre and post:
                R[f"T4_{g}_est"] = sum(gp[y] for y in post) / len(post) - sum(gp[y] for y in pre) / len(pre)
            if ok:
                b, _ = hc1([gp[y] for y in pre], [[1.0, y] for y in pre])
                R[f"T4_{g}_pretrend"] = b[1]
                if abs(b[1]) < L.T4_PRETREND:
                    scored.append(g)
        if not scored:
            R["T4_outcome"] = "NOT SCORED"
        else:
            e = [R[f"T4_{g}_est"] for g in scored]
            R["T4_outcome"] = ("SURVIVE" if all(x > L.T4_SURVIVE for x in e) else
                               "FAIL" if any(x <= L.T4_FAIL for x in e) else "INCONCLUSIVE")

    # T5
    # T5 reads T2's titles, less any with no basic wage in a post-period June
    gross_bad = {(x["grp"], x["line"]) for x in ls if x["series"] == "main"
                 and x["june"] in window(x["grp"]) and not x.get("p25_gross")}
    basic_bad = {(x["grp"], x["line"]) for x in ls if x["series"] == "main" and x["grp"] in L.POST
                 and x["june"] in L.POST[x["grp"]] and not x.get("p25_basic")}
    lv = gvalues([x for x in ls if (x["grp"], x["line"]) not in gross_bad | basic_bad],
                 ("main",), "p25_basic", log=False)
    ok5 = True
    for g in groups:
        for y, rung in L.RUNG[g].items():
            if y in lv.get(g, {}):
                R[f"T5_{g}_{y}_ratio"] = lv[g][y] / rung
                ok5 &= R[f"T5_{g}_{y}_ratio"] >= L.T5_LINE
            else:
                ok5 = False
    R["T5_outcome"] = "NOT SCORED" if not groups else ("SURVIVE" if ok5 else "FAIL")
    return R


def main():
    a = L.args("PWM step 15: independent reproduction")
    P = L.paths(a.root)
    L.guard(P["raw"])
    T = {r["key"]: r["value"] for r in L.read_csv(os.path.join(P["out"], "tests.csv"))}
    R = reproduce(a.root)
    bad = n = 0
    for k, v in R.items():
        if k not in T:
            print(f"  MISSING in tests.csv: {k}")
            bad += 1
            continue
        n += 1
        if isinstance(v, str):
            same = v == T[k]
        else:
            pr = L.printed(k, v)
            same = (pr == L.printed(k, T[k])) if pr is not None else abs(float(T[k]) - v) <= 1e-6 * max(1, abs(v))
            same = same and abs(float(T[k]) - v) <= 1e-6 * max(1.0, abs(v))
        if not same:
            print(f"  DIFFERS {k}: tests.csv {T[k]}, reproduced {v}")
            bad += 1
    print(f"  {n} numbers and outcomes reproduced, {bad} differ")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
