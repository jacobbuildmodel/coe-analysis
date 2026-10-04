"""
11b_postresults.py -- the numbers the article prints, derived from out/,
NOT SCORED (THESIS_ADDENDUM.md item 5). Changes no sealed number. Writes
ROOT/out/postresults.csv (key, value, printed, meaning), which 14_manifest.py
adds to the number manifest, so every number in the article has a script.

  python3 sgd/11b_postresults.py [--root DIR]

  * The specimen: MAS's monthly-average rate, Singapore dollars per 100 yen,
    January 2021 and December 2025 (out/masfx.csv), and what a S$1,000 trip
    budget bought in yen at each.
  * Per-cent moves, 100 x (exp(x) - 1), of every log change the article
    uses: the Singapore dollar against the yen and the ringgit, its broad
    index, the partners' broad indices, the long-run split.
  * The shares of the rise in per cent.
  * Rounded forms of tested numbers as the article prints them (correlations
    to two decimals, the scorecard), each beside its unrounded source key.
  * Jacob's confidences in per cent.
Downs are printed as positive numbers with the word "down" in the meaning;
the article says "down".
"""
import math
import os

import sgdlib as L

BUDGET = 1000            # S$, the specimen's trip budget


def main():
    a = L.args("sgd step 11b: the article's numbers, not scored")
    P = L.paths(a.root)
    out = P["out"]
    T = {r["key"]: r["value"] for r in L.read_csv(os.path.join(out, "tests.csv"))}
    S = {r["key"]: r["value"] for r in L.read_csv(os.path.join(out, "sensitivities.csv"))}
    fx = {(r["currency"], r["period"]): float(r["value"]) for r in L.read_csv(os.path.join(out, "masfx.csv"))}
    rows = []

    def add(key, value, fmt, meaning):
        rows.append([key, value, fmt.format(value), meaning])

    def f(src, key):
        v = src.get(key)
        return None if v in (None, "") else float(v)

    def pct(key, x, meaning):
        """Per-cent move of log change x: one decimal and whole, absolute."""
        if x is None:
            return
        v = 100 * (math.exp(x) - 1)
        word = "up" if v >= 0 else "down"
        add(key + "_pct", abs(v), "{:.1f}", f"{meaning}, per cent, {word}")
        add(key + "_pct0", abs(v), "{:.0f}", f"{meaning}, per cent, {word}, whole")

    def share(key, x, meaning):
        if x is None:
            return
        v = 100 * x
        word = "" if v >= 0 else ", negative (printed without sign)"
        add(key + "_share", abs(v), "{:.1f}", f"{meaning}, per cent of the rise{word}")
        add(key + "_share0", abs(v), "{:.0f}", f"{meaning}, per cent of the rise{word}, whole")

    # ---- the specimen
    for m, label in (("2021-01", "January 2021"), ("2025-12", "December 2025")):
        v = fx.get(("JPY", m))
        if v:
            tag = m.replace("-", "_")
            add(f"spec_sgd_per_100jpy_{tag}", 100 * v, "{:.2f}",
                f"MAS monthly average, S$ per 100 yen, {label}")
            add(f"spec_yen_per_budget_{tag}", round(BUDGET / v, -3), "{:,.0f}",
                f"yen bought by a S${BUDGET:,} budget, {label}, to the nearest 1,000")

    # ---- the scored window, in per cent (T2 yen, T3 ringgit)
    for t, cur in (("T2", "yen"), ("T3", "ringgit")):
        pct(f"{t}_b", f(T, f"{t}_b"), f"the Singapore dollar against the {cur}, Jan 2021 to Dec 2025")
        pct(f"{t}_s", f(T, f"{t}_s"), "the Singapore dollar's broad index (against everyone)")
        pct(f"{t}_nx", f(T, f"{t}_nx"), f"the {cur}'s broad index (against everyone)")
        share(f"{t}_S", f(T, f"{t}_S"), "share: the Singapore dollar rising against everyone")
        share(f"{t}_P", f(T, f"{t}_P"), f"share: the {cur} falling against everyone")
        share(f"{t}_R", f(T, f"{t}_R"), "share: neither broad index (the residual)")

    # ---- T1's ringgit residual, the long-run split (sensitivity)
    share("T1_scored_MYR_R", f(T, "T1_scored_MYR_R"), "T1: the ringgit's residual, scored window")
    pct("long_JPY_b", f(S, "long_JPY_b"), "the Singapore dollar against the yen, Aug 2005 on (sensitivity)")
    share("long_JPY_S", f(S, "long_JPY_S"), "long run: the Singapore dollar rising against everyone")
    share("long_JPY_P", f(S, "long_JPY_P"), "long run: the yen falling against everyone")

    # ---- gate C, T4, world view, T7, rounded as the article prints them
    for key, src, meaning in (("gateC_r", T, "gate C correlation"),
                              ("T7_rho_p", T, "T7: rank correlation with MAS's decisions"),
                              ("T7_rho_g", T, "T7: rank correlation with growth"),
                              ("T7_D", T, "T7: D"), ("T7_D_lo", T, "T7: D, 90% interval, low"),
                              ("T7_D_hi", T, "T7: D, 90% interval, high"),
                              ("HK_US_sd_ratio", S, "world view: Hong Kong dollar's swing over the US dollar's"),
                              ("HK_US_corr", S, "world view: Hong Kong and US broad indices, correlation")):
        v = f(src, key)
        if v is not None:
            add(key + "_2dp", v, "{:.2f}", meaning + ", two decimals")
    for key, meaning in (("rho_g", "T7 with CPI inflation in place of growth: rank correlation with inflation"),
                         ("D", "T7 with CPI inflation in place of growth: D")):
        sens = [r for r in L.read_csv(os.path.join(out, "sensitivities.csv"))
                if r["test"] == "T7" and r["variant"] == "CPI inflation" and r["key"] == key]
        if sens:
            add(f"T7_cpi_{key}_2dp", float(sens[0]["value"]), "{:.2f}", meaning + " (not scored)")
    for a_ in ("SG", "HK", "US", "JP"):
        v = f(T, f"T4_{a_}_sd")
        if v is not None:
            add(f"T4_{a_}_sd_pct", 100 * v, "{:.2f}", f"T4: typical monthly move of {a_}'s broad index, per cent")

    # ---- scorecard in the article's terms
    for k, fmt, meaning in (("expected_held", "{:.2f}", "expected held, sum of Jacob's confidences"),):
        v = f(T, k)
        if v is not None:
            add(k + "_2dp", v, fmt, meaning)
    for t in L.SCORED:
        c = f(T, f"conf_{t}")
        if c is not None:
            add(f"conf_{t}_pct", 100 * c, "{:.0f}", f"Jacob's confidence at seal, {t}, per cent")

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
