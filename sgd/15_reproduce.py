"""
15_reproduce.py -- an independent reproduction of every scored number and
outcome, straight from raw/ and office/MPS_CODING.csv, by a different path
from 10_load.py and 11_tests.py: pandas for parsing, numpy for the
arithmetic, scipy.stats.spearmanr for the rank correlations. It imports
nothing from 10 or 11 and shares only the constants in sgdlib.

  python3 sgd/15_reproduce.py [--root DIR]

Refuses the real sgd/raw/ until sgd/SEALED exists. Compares with out/tests.csv
and exits 1 on any difference larger than 1e-6 (relative, or absolute below
1). out/ stores numbers to 8 significant digits (sgdlib.FLOAT) and this path
reads raw/ at full precision, so differences of order 1e-7 are rounding;
RESULTS.md prints 4 decimals. The bootstrap
interval for T7's D is not reproduced (it is reported, not scored).
"""
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

import sgdlib as L

MON = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}


def bis(path, **flt):
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    for k, v in flt.items():
        df = df[df[k] == v]
    df = df[df["OBS_VALUE"] != ""]
    mult = pd.to_numeric(df["UNIT_MULT"], errors="coerce").fillna(0) if "UNIT_MULT" in df else 0
    df = df.assign(v=pd.to_numeric(df["OBS_VALUE"]) * 10.0 ** mult)
    return df


def tb_row(path, label):
    with open(path, encoding="utf-8-sig") as f:
        d = json.load(f)
    row = next(r for r in d["Data"]["row"] if r["rowText"] == label)
    s = pd.Series({c["key"]: pd.to_numeric(c["value"], errors="coerce") for c in row["columns"]})
    return s.dropna()


def main():
    a = L.args("sgd step 15: independent reproduction of every scored number")
    P = L.paths(a.root)
    raw = L.guard(P["raw"])
    n = bis(os.path.join(raw, L.F_NEER), FREQ="M", EER_TYPE="N", EER_BASKET="B")
    N = np.log(n.pivot(index="TIME_PERIOD", columns="REF_AREA", values="v"))
    u = bis(os.path.join(raw, L.F_USD), FREQ="M", COLLECTION="A")
    U = np.log(u.pivot(index="TIME_PERIOD", columns="CURRENCY", values="v"))
    U["USD"] = 0.0
    CROSS = U.sub(U["SGD"], axis=0)                    # ln(X per SGD)
    last = N["SG"].dropna().index.max()
    W = {"scored": (L.SCORED_START, L.SCORED_END, L.SCORED_START[0], L.SCORED_END[-1]),
         "long": (L.LONG_START, tuple(L.month_add(last, k) for k in (-2, -1, 0)), L.LONG_FIRST, last)}

    mas = {}
    for cur, (label, per) in L.MAS_ROWS.items():
        s = tb_row(os.path.join(raw, L.F_MASFX), label) / per
        s.index = [f"{k.split()[0]}-{MON[k.split()[1][:3]]:02d}" for k in s.index]
        mas[cur] = -np.log(s)                           # ln(X per SGD)

    R = {}

    def chg(series, w):
        st, en = W[w][0], W[w][1]
        return series.loc[list(en)].mean() - series.loc[list(st)].mean()

    oks = []
    for w in ("scored", "long"):
        for cur in L.QUESTION:
            area = L.CUR_AREA[cur]
            b, s_, nx = chg(CROSS[cur], w), chg(N["SG"], w), chg(N[area], w)
            e = b - s_ + nx
            k = f"T1_{w}_{cur}"
            R[k + "_b"] = b
            R[k + "_R"] = e / b if b > 0 else None
            rng = [m for m in CROSS.index if W[w][2] <= m <= W[w][3]]
            d = (CROSS[cur].reindex(rng) - mas[cur].reindex(rng)).abs().dropna()
            R[k + "_mad"] = d.mean() if len(d) else None
            R[k + "_mad_count"] = len(d)
            ok = (b <= 0 or abs(e / b) <= L.T1_R) and (not len(d) or d.mean() <= L.T1_MAD)
            oks.append(ok)
            if w == "scored":
                R[f"_ok_{cur}"] = ok
    R["T1_outcome"] = "SURVIVE" if all(oks) else "FAIL"
    for t, cur in (("T2", "JPY"), ("T3", "MYR")):
        area = L.CUR_AREA[cur]
        b, s_, nx = chg(CROSS[cur], "scored"), chg(N["SG"], "scored"), chg(N[area], "scored")
        R[f"{t}_b"], R[f"{t}_s"], R[f"{t}_nx"], R[f"{t}_e"] = b, s_, nx, b - s_ + nx
        if b > 0:
            S, Pp, Rr = s_ / b, -nx / b, (b - s_ + nx) / b
            R[f"{t}_S"], R[f"{t}_P"], R[f"{t}_R"] = S, Pp, Rr
            if not R[f"_ok_{cur}"]:
                R[f"{t}_outcome"] = "NOT SCORED"
            elif Pp >= L.T2_P and Pp > S:
                R[f"{t}_outcome"] = "SURVIVE"
            elif S >= Pp:
                R[f"{t}_outcome"] = "FAIL"
            else:
                R[f"{t}_outcome"] = "INCONCLUSIVE"
        else:
            R[f"{t}_outcome"] = "NOT SCORED"

    # gate C
    with open(os.path.join(raw, L.F_SNEER), encoding="utf-8-sig") as f:
        feed = json.load(f)["elements"]
    sw = pd.DataFrame(feed)
    sw["m"] = sw["date"].astype(str).str[:7]
    sw["value"] = pd.to_numeric(sw["value"], errors="coerce")
    g = sw.dropna(subset=["value"]).groupby("m")["value"].agg(["mean", "count"])
    g = g[g["count"] >= L.GATE_MIN_READINGS]
    both = sorted(set(g.index) & set(N["SG"].dropna().index))
    pairs = [(x, y) for x, y in zip(both, both[1:]) if L.month_diff(x, y) == 1]
    dx = np.array([np.log(g.loc[y, "mean"]) - np.log(g.loc[x, "mean"]) for x, y in pairs])
    dy = np.array([N["SG"][y] - N["SG"][x] for x, y in pairs])
    r = float(np.corrcoef(dx, dy)[0, 1]) if len(pairs) >= 3 else None
    R["gateC_r"], R["gateC_changes"] = r, len(pairs)
    gate = r is not None and len(pairs) >= L.GATE_MIN and r >= L.GATE_R

    # T4
    rng = [m for m in N.index if L.LONG_FIRST <= m <= last]
    block = N.reindex(columns=[a_ for a_ in L.AREAS if a_ in N.columns]).loc[rng]
    block = block.loc[:, block.notna().all()]
    sds = block.diff().iloc[1:].std(ddof=1)
    for a_, v in sds.items():
        R[f"T4_{a_}_sd"] = v
    R["T4_present"] = len(sds)
    if "SG" in sds and len(sds) >= L.T4_MIN_PRESENT:
        rank = int((sds.drop("SG") < sds["SG"]).sum()) + 1
        st = int((sds.drop("SG") > sds["SG"]).sum())
        R["T4_rank"], R["T4_steadier_than"] = rank, st
        R["T4_outcome"] = ("NOT SCORED" if not gate else "SURVIVE" if rank <= L.T4_SURVIVE_RANK
                           else "FAIL" if st <= (len(sds) - 1) // 2 else "INCONCLUSIVE")
    else:
        R["T4_outcome"] = "NOT SCORED"

    # T7
    mps = pd.read_csv(P["coding"], dtype=str).sort_values("date").reset_index(drop=True)
    gdp = tb_row(os.path.join(raw, L.F_GDP), L.GDP_ROW)
    gdp.index = [f"{k.split()[0]}-{3 * int(k.split()[1][0]):02d}" for k in gdp.index]   # quarter -> end month
    ys, gs, ps = [], [], []
    dropped = 0
    for i in range(len(mps)):
        d = mps.loc[i, "date"]
        dm = f"{d[:4]}-{d[4:6]}"
        start = L.month_add(dm, -1)
        if i + 1 < len(mps):
            d2 = mps.loc[i + 1, "date"]
            end = L.month_add(f"{d2[:4]}-{d2[4:6]}", -1)
            need = 1
        else:
            end, need = last, 2
        end = min(end, last)
        k = L.month_diff(start, end)
        if k < need:
            continue
        if start not in N.index or end not in N.index or pd.isna(N["SG"].get(start)) or pd.isna(N["SG"].get(end)):
            dropped += 1
            continue
        inside = gdp[(gdp.index > start) & (gdp.index <= end)]
        if len(inside):
            gv = inside.mean()
        else:
            qend = f"{dm[:4]}-{3 * ((int(dm[5:7]) - 1) // 3 + 1):02d}"
            gv = gdp.get(qend)
            if gv is None or pd.isna(gv):
                dropped += 1
                continue
        ys.append(12 * (N["SG"][end] - N["SG"][start]) / k)
        gs.append(gv)
        ps.append(int(mps.loc[i, "p"]))
    R["T7_intervals"], R["T7_dropped_count"] = len(ys), dropped
    rp = spearmanr(ys, ps).statistic
    rg = spearmanr(ys, gs).statistic
    R["T7_rho_p"], R["T7_rho_g"], R["T7_D"] = rp, rg, rp - rg
    D_ = rp - rg
    R["T7_outcome"] = ("NOT SCORED" if not gate else "SURVIVE" if D_ >= L.T7_D and rp > 0
                       else "FAIL" if D_ <= 0 else "INCONCLUSIVE")

    T = {r_["key"]: r_["value"] for r_ in L.read_csv(os.path.join(P["out"], "tests.csv"))}
    bad, n_ok = 0, 0
    for k, v in sorted(R.items()):
        if k.startswith("_"):
            continue
        got = T.get(k, "")
        if v is None:
            ok = got == ""
        elif isinstance(v, str):
            ok = got == v
        else:
            try:
                g_ = float(got)
                ok = abs(g_ - float(v)) <= 1e-6 * max(1.0, abs(float(v)))
            except ValueError:
                ok = False
        if ok:
            n_ok += 1
        else:
            print(f"  DIFFERS {k}: reproduced {v!r}, tests.csv {got!r}")
            bad += 1
    print(f"  {n_ok} numbers and outcomes reproduced, {bad} differ")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
