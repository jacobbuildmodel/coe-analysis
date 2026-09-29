"""
11b_postresults.py -- checks added after the results, NOT SCORED
(THESIS_ADDENDUM.md item 6). Reads ROOT/out/ (written by 10_load.py and
11_tests.py) and, for the running record, erp/out/tests.csv. Changes no
sealed number; writes ROOT/out/postresults.csv (key, value, printed,
meaning), which 14_manifest.py adds to the number manifest.

  A1. Landscape's T2 with the steepest landscape drift among the sealed T1
      sensitivities carried from the pre-period midpoint to the post-period
      midpoint (the means of the Junes each window scores), and subtracted.
  A2. T3 against the LFS median INCLUDING employer CPF. The sealed measure
      excludes it, because OWS gross wage excludes employer CPF: like for
      like. Reported beside the sealed result, not instead of it.
  Per-cent equivalents, 100 x (exp(x) - 1), of every log-point figure the
  article uses; the levels behind the T5 ratios; the running record.
"""
import math
import os

import pwmlib as L

ERP_TESTS = os.path.join(os.path.dirname(L.PWM), "erp", "out", "tests.csv")


def pct(x):
    return 100 * (math.exp(x) - 1)


def main():
    a = L.args("PWM step 11b: post-results checks, not scored")
    P = L.paths(a.root)
    out = P["out"]
    T = {r["key"]: r["value"] for r in L.read_csv(os.path.join(out, "tests.csv"))}
    S = L.read_csv(os.path.join(out, "sensitivities.csv"))
    rows = []

    def add(key, value, fmt, meaning):
        rows.append([key, value, fmt.format(value), meaning])

    def add_pct(key, x, meaning, whole=True):
        add(f"{key}_pct", pct(x), "{:.1f}", f"{meaning}, per cent (exp(x) - 1)")
        if whole:
            add(f"{key}_pct0", pct(x), "{:.0f}", f"{meaning}, per cent, whole number")

    # ---- per-cent equivalents of the sealed log-point numbers
    for g in L.COVERED:
        if T.get(f"T1_{g}_slope"):
            add_pct(f"T1_{g}_slope", float(T[f"T1_{g}_slope"]), f"T1 {g} drift a year")
    passing = T.get("T1_groups_passing", "").split()
    for g in passing:
        for k in ("est", "lo", "hi"):
            if T.get(f"T2_{g}_{k}"):
                add_pct(f"T2_{g}_{k}", float(T[f"T2_{g}_{k}"]), f"T2 {g} {k}")
    for k in ("growth_c", "growth_mid", "shortfall"):
        if T.get(f"T3_{k}"):
            add_pct(f"T3_{k}", float(T[f"T3_{k}"]), f"T3 {k}")
    for key, x, meaning in (("line_T1", L.T1_LINE, "T1 line, 1.0 log point a year"),
                            ("line_T2_survive", L.T2_SURVIVE, "T2 survive line, 10 log points"),
                            ("line_T2_fail", L.T2_FAIL, "T2 fail line, 5 log points"),
                            ("line_T3", L.T3_LINE, "T3 line, 5 log points")):
        add_pct(key, x, meaning)

    # ---- A1: landscape T2 net of the steepest sensitivity drift
    drifts = {r["variant"]: float(r["value"]) for r in S
              if r["test"] == "T1" and r["key"] == "landscape_slope"
              and r["value"] not in ("",) and not r["value"].startswith("not run")}
    if "landscape" in passing and drifts and T.get("T2_landscape_est"):
        variant, d = max(drifts.items(), key=lambda kv: abs(kv[1]))
        years = sum(L.POST["landscape"]) / len(L.POST["landscape"]) - \
            sum(L.PRE["landscape"]) / len(L.PRE["landscape"])
        est = float(T["T2_landscape_est"])
        adj = est - d * years
        add("A1_drift", d, "{:.4f}", f"A1 steepest landscape drift among T1 sensitivities ({variant})")
        add_pct("A1_drift", d, "A1 steepest landscape drift a year")
        add("A1_years", years, "{:.1f}", "A1 years from pre-period to post-period midpoint (Junes scored)")
        add("A1_carried", d * years, "{:.4f}", "A1 drift carried over those years, log points")
        add_pct("A1_carried", d * years, "A1 drift carried over those years")
        add("A1_T2_landscape_adjusted", adj, "{:.4f}", "A1 landscape T2 net of that drift, log points")
        add_pct("A1_T2_landscape_adjusted", adj, "A1 landscape T2 net of that drift")
        add("A1_clears_T2_line", adj >= L.T2_SURVIVE, "{}", "A1 adjusted estimate still at or above 0.10")

    # ---- A2: T3 against the median including employer CPF
    lfs = L.read_csv(os.path.join(out, "lfs_median.csv"))
    inc = {int(r["year"]): math.log(float(r["median_incl_emp_cpf"])) for r in lfs if r["median_incl_emp_cpf"]}
    ms = [inc[j] for j in (2010, 2011, 2012) if j in inc]
    me = [inc[j] for j in (2017, 2018, 2019) if j in inc]
    if ms and me and T.get("T3_growth_c"):
        gm = sum(me) / len(me) - sum(ms) / len(ms)
        short = gm - float(T["T3_growth_c"])
        add("A2_growth_mid_incl", gm, "{:.4f}", "A2 median growth including employer CPF, log points")
        add_pct("A2_growth_mid_incl", gm, "A2 median growth including employer CPF")
        add("A2_shortfall_incl", short, "{:.4f}", "A2 T3 shortfall against that median, log points")
        add_pct("A2_shortfall_incl", short, "A2 T3 shortfall against that median")
        add("A2_under_T3_line", short < L.T3_LINE, "{}", "A2 shortfall below the 0.05 line")

    # ---- T5 levels: the bottom-quarter basic pay behind each ratio
    ows = L.read_csv(os.path.join(out, "ows_lines.csv"))
    for r in L.read_csv(os.path.join(out, "t5_ratios.csv")):
        g, y = r["group"], int(r["june"])
        lv = [float(x["p25_basic"]) for x in ows
              if x["group"] == g and x["series"] == "main" and int(x["june"]) == y and x["p25_basic"]]
        add(f"T5_{g}_{y}_p25_basic", sum(lv) / len(lv), "{:,.0f}",
            f"{g} 25th-percentile basic wage, June {y}, S$ (mean of the group's main titles)")
        add(f"T5_{g}_{y}_rung", float(r["rung"]), "{:,.0f}", f"{g} entry rung on 1 June {y}, S$")
        add(f"T5_{g}_{y}_ratio_pct", 100 * float(r["ratio"]), "{:.1f}", f"{g} ratio, June {y}, per cent")

    # ---- scorecard in the article's terms, and the running record
    for t in ("T1", "T2", "T3", "T5"):
        c = T.get(f"conf_{t}")
        if c not in (None, "", "[JACOB]", "not scored"):
            add(f"conf_{t}_pct", 100 * float(c), "{:.0f}", f"Jacob's confidence at seal, {t}, per cent")
    if os.path.exists(ERP_TESTS) and T.get("n_scored"):
        E = {r["key"]: r["value"] for r in L.read_csv(ERP_TESTS)}
        n = int(E["n_scored"]) + int(T["n_scored"])
        held = int(E["n_held"]) + int(T["n_held"])
        exp_ = float(E["expected_held"]) + float(T["expected_held"])
        brier = (float(E["brier"]) * int(E["n_scored"]) + float(T["brier"]) * int(T["n_scored"])) / n
        add("record_scored", n, "{:d}", "running record: scored predictions, ERP and PWM")
        add("record_held", held, "{:d}", "running record: held")
        add("record_expected", exp_, "{:.2f}", "running record: expected, sum of confidences")
        add("record_brier", brier, "{:.3f}", "running record: Brier score over all scored predictions")

    # value as %.8g like every other output; printed exactly as formatted
    import csv
    import io
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["key", "value", "printed", "meaning"])
    for key, value, printed, meaning in rows:
        w.writerow([key, L.fmt(value), printed, meaning])
    L.write_text(os.path.join(out, "postresults.csv"), buf.getvalue())
    print(f"  out/postresults.csv: {len(rows)} rows (post-results, not scored)")


if __name__ == "__main__":
    main()
