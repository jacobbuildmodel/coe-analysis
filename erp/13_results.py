"""
13_results.py -- write erp/RESULTS.md from out/ and the sealed THESIS.md.

The sealed wording of each test is quoted from THESIS.md itself, not retyped:
the file is first checked against the md5 recorded at the seal (6d2a345), and
the bullets are cut out of it by label. Tests that did not hold come first.
Every number printed here is formatted from out/tests.csv, out/t2_fits.csv,
out/t4_fits.csv or out/s1.csv, and 14_manifest.py lists each one.
"""
import hashlib
import os
import re

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
THESIS = os.path.join(HERE, "THESIS.md")
SEAL_MD5 = "2f99e6513de2f5ebe7f578e6a5650f50"
SEAL_COMMIT = "6d2a345"

LABELS = ("Scored years.", "Main specification.", "Years.", "Estimate.", "Prediction.",
          "Survive if:", "Fail if:", "Between -1.0 and -0.5, on either road class:",
          "Otherwise:", "Informativeness condition, fixed now.")
TITLES = {"T1": "T1. Thermostat band (the ERP signature)",
          "T2": "T2. Insensitivity to car density (magnitude)",
          "T3": "T3. Door fee and usage (the COE mechanism)",
          "T4": "T4. The premium adds little once car numbers are known (magnitude)"}


def sealed_text():
    raw = open(THESIS, "rb").read()
    got = hashlib.md5(raw).hexdigest()
    assert got == SEAL_MD5, f"THESIS.md md5 {got} is not the sealed {SEAL_MD5}"
    return raw.decode("utf-8")


def section(text, heading):
    i = text.index(f"### {heading}")
    j = text.find("\n### ", i + 4)
    return text[i:j]


def bullets(sec):
    """Every top-level bullet of a test section, keyed by its bold label."""
    out = {}
    for m in re.finditer(r"^- \*\*(.+?)\*\*(.*(?:\n  .*)*)", sec, re.M):
        out[m.group(1).strip()] = m.group(0)
    return out


def quote(b):
    return "\n".join("> " + line if line.strip() else ">" for line in b.splitlines())


def main():
    thesis = sealed_text()
    T = pd.read_csv(os.path.join(OUT, "tests.csv")).set_index("key").value
    f2 = pd.read_csv(os.path.join(OUT, "t2_fits.csv"))
    f4 = pd.read_csv(os.path.join(OUT, "t4_fits.csv"))
    s1 = pd.read_csv(os.path.join(OUT, "s1.csv")).set_index("year")
    t1y = pd.read_csv(os.path.join(OUT, "t1_years.csv"))
    split = pd.read_csv(os.path.join(OUT, "t3_split.csv")).set_index("year")
    fl = lambda k: float(T[k])
    weak = re.search(r'verbatim:\*\*\n"(.+?)"', thesis, re.S).group(1).replace("\n", " ")

    outcome = {k: T[f"{k}_outcome"] for k in TITLES}
    conf = {k: fl(f"{k}_confidence") for k in TITLES}
    order = [k for k in TITLES if outcome[k] != "PASS"] + [k for k in TITLES if outcome[k] == "PASS"]

    L = []
    ad = L.append
    ad("# RESULTS: COE or ERP -- which one actually keeps Singapore's roads moving?")
    ad("")
    ad(f"Scored against THESIS.md as sealed in commit `{SEAL_COMMIT}` (md5 `{SEAL_MD5}`, "
       "checked by this script before it writes a line). Written by `13_results.py` from "
       "`out/`; every number below is in `number_manifest.csv`. Anything learned after the "
       "seal is in `THESIS_ADDENDUM.md` and changes no score.")
    ad("")
    held = int(T["n_held"])
    ad("## Summary")
    ad("")
    ad("| Test | Outcome | Held | Jacob's confidence |")
    ad("|---|---|---|---|")
    for k in order:
        ad(f"| {k} | {outcome[k]} | {'yes' if outcome[k] == 'PASS' else 'no'} | {conf[k]:.0%} |")
    ad("")
    ad(f"**Held: {held} of {int(T['n_scored'])}**, against an expected {fl('expected_held'):.1f} "
       f"of {int(T['n_scored'])}. **Brier score: {fl('brier'):.3f}** (mean of (confidence - outcome)^2, "
       "outcome 1 if held, 0 otherwise; no test dropped out).")
    ad("")
    ad(f"**Verdict (section 8): {T['verdict']}.**")
    ad("")
    ad(f"> {weak}")
    ad("")
    ad("Tests that did not hold come first.")
    ad("")

    for k in order:
        sec = section(thesis, TITLES[k])
        b = bullets(sec)
        ad(f"## {TITLES[k]}: {outcome[k]}")
        ad("")
        ad(f"Jacob's confidence that it would hold: **{conf[k]:.0%}**. Outcome: **{outcome[k]}**.")
        ad("")
        ad("Sealed wording:")
        ad("")
        for lab in LABELS:
            if lab in b:
                ad(quote(b[lab]))
                ad(">")
        L[-1] = ""
        ad("Result:")
        ad("")
        if k == "T1":
            for c, band in (("expressway", "45-65"), ("arterial", "20-30")):
                ad(f"- {c.capitalize()}, {int(fl(f'T1_{c}_scored_years'))} scored years, band {band} km/h "
                   f"(read as closed, so a value equal to an edge is inside): "
                   f"{int(fl(f'T1_{c}_above'))} above, {int(fl(f'T1_{c}_below'))} below"
                   + (f" ({T[f'T1_{c}_outside_years']})." if T[f'T1_{c}_outside_years'] != 'none' else "."))
            for _, r in t1y[(t1y.road == "arterial") & (t1y.position == "above") & t1y.scored].iterrows():
                ad(f"  - {int(r.year)}: {r.speed:g} km/h")
            ad(f"- Informativeness: car population range over the scored years with a car count was "
               f"{fl('T1_expressway_carpop_range_share_pct'):.1f} per cent of its mean (expressway years) and "
               f"{fl('T1_arterial_carpop_range_share_pct'):.1f} per cent (arterial years), above the 10 per cent "
               "line, so the test was informative.")
            ad("- No scored year sat below either band, so this failure is on the high side: arterial "
               "roads ran faster than the band, the opposite of the buffet.")
        if k == "T2":
            ad("| Road | Elasticity | 90% interval | R-squared | Status |")
            ad("|---|---|---|---|---|")
            for c in ("expressway", "arterial"):
                ad(f"| {c} | {fl(f'T2_{c}_slope'):.3f} | {fl(f'T2_{c}_lo'):.3f} to {fl(f'T2_{c}_hi'):.3f} | "
                   f"{fl(f'T2_{c}_r2'):.2f} | {T[f'T2_{c}_status']} |")
            ad("")
            ad("Main specification: log(peak speed) on log(cars per lane-km of the same road class), "
               "2005-2017, 13 points, OLS with HC1 errors. Both elasticities sit inside [-0.5, +0.5]. "
               "On arterial roads the slope is positive: speeds rose while crowding rose. Over the "
               f"same years cars per lane-km rose {fl('T2_expressway_density_rise_pct'):.0f} per cent on "
               f"expressways and {fl('T2_arterial_density_rise_pct'):.0f} per cent on arterial roads.")
            ad("")
            ad("Sensitivities, reported, not scored:")
            ad("")
            ad("| Specification | Road | n | Elasticity | 90% interval | R-squared |")
            ad("|---|---|---|---|---|---|")
            for _, r in f2[f2.spec != "main: log cars per lane-km"].iterrows():
                ad(f"| {r.spec} | {r.road} | {r.n} | {r.x_coef:.3f} | {r.x_ci_lo:.3f} to {r.x_ci_hi:.3f} | {r.r2:.2f} |")
            ad("")
            tr = f2[(f2.road == "arterial") & (f2.spec == "sens ii: main + linear trend")].iloc[0]
            ad(f"With a linear trend added the arterial slope turns negative ({tr.x_coef:.3f}) and the "
               f"fit's R-squared rises to {tr.r2:.2f}: arterial speeds rose steadily over time, and "
               "crowding cannot be separated from that drift in 13 annual points.")
        if k == "T3":
            ad(f"- High-premium years ({T['T3_high_years']}): mean {fl('T3_high_mean_km'):,.0f} km per car.")
            ad(f"- Low-premium years ({T['T3_low_years']}): mean {fl('T3_low_mean_km'):,.0f} km per car.")
            ad(f"- Ratio {fl('T3_ratio'):.3f}: the high-premium years were {fl('T3_pct_lower'):.1f} per cent "
               "lower, beyond the 3 per cent line.")
            ad("- The E2 page's sampling error is not recorded in anything retrieved, so the "
               "below-resolution rule did not apply and T3 is scored.")
            ad(f"- Hire and rental cars (E3) grew by {fl('T3_hire_growth_in_high_half'):,.0f} over the "
               f"high-premium years and by {fl('T3_hire_growth_in_low_half'):,.0f} over the low-premium years. "
               "The private-hire bias named at the seal therefore pushed toward PASS, not FAIL; T3 "
               "failed anyway. See THESIS_ADDENDUM.md, item 1.")
            ad("")
            ad("| Year | Premium (A+B mean, S$) | km per car | Half |")
            ad("|---|---|---|---|")
            for y, r in split.iterrows():
                ad(f"| {y} | {r.premium_ab:,.0f} | {r.km_per_car:,.0f} | {r.half} |")
        if k == "T4":
            ad("| Road | Adj. R-squared gain | Premium coefficient | 90% interval | Includes zero | Status |")
            ad("|---|---|---|---|---|---|")
            for c in ("expressway", "arterial"):
                ad(f"| {c} | {fl(f'T4_{c}_gain'):.3f} | {fl(f'T4_{c}_premium_coef'):.3f} | "
                   f"{fl(f'T4_{c}_premium_ci_lo'):.3f} to {fl(f'T4_{c}_premium_ci_hi'):.3f} | "
                   f"{T[f'T4_{c}_ci_includes_zero']} | {T[f'T4_{c}_status']} |")
            ad("")
            ad("2005-2025 less 2020 and 2021, 19 points. Expressways pass both conditions. On arterial "
               "roads the gain is under 0.10 but the premium's interval excludes zero, which is "
               "neither the survive nor the fail condition: mixed, so T4 does not hold.")
            ad("")
            dens = f4[f4.spec.str.startswith("sens: full")]
            base = f4[f4.spec.str.startswith("sens: base")].set_index("road").adj_r2
            ad("Density sensitivity, 2005-2017, not scored: premium coefficient "
               + "; ".join(f"{r.road} {r.premium_coef:.3f} ({r.premium_ci_lo:.3f} to {r.premium_ci_hi:.3f}), "
                           f"gain {r.adj_r2 - base[r.road]:.3f}" for _, r in dens.iterrows()) + ".")
            meets = [r.road for _, r in dens.iterrows()
                     if r.adj_r2 - base[r.road] >= 0.10 and not (r.premium_ci_lo <= 0 <= r.premium_ci_hi)]
            if meets:
                ad("")
                ad(f"On that unscored density version the {' and '.join(meets)} result meets the sealed "
                   "fail condition (gain 0.10 or more and an interval that excludes zero). It is not the "
                   "sealed specification and changes nothing above. It does point the same way as the "
                   "scored arterial result: on arterial roads the premium carries information about "
                   "speed beyond the car count.")
        ad("")

    ad("## Verdict")
    ad("")
    rule = thesis[thesis.index("## 8. The verdict rule"):thesis.index("**Weak-evidence sentence")]
    for line in rule.splitlines()[2:]:
        ad("> " + line if line.strip() else ">")
    ad("")
    ad(f"T1 failed, but with {int(fl('T1_expressway_below'))} expressway and "
       f"{int(fl('T1_arterial_below'))} arterial years below the band, not 3 or more; T2 passed on both "
       "road classes. Neither the ERP condition (which needs T1 to survive) nor the COE condition is "
       f"met, so: **{T['verdict']}.**")
    ad("")
    ad(f"> {weak}")
    ad("")
    ad("And the thermostat problem, as the seal requires: the design shows a signature, not a cause.")
    ad("")

    ad("## T5 leg (a), reported, not scored")
    ad("")
    ad(f"Leg (a) met: **{'yes' if T['T5a_met'] == 'True' else 'no'}**. Neither road class shows an elasticity "
       "at or below -1.0 (expressway "
       f"{fl('T2_expressway_slope'):.3f}, arterial {fl('T2_arterial_slope'):.3f}), so the COE-win mirror "
       "did not appear. Leg (b) was untestable, as sealed.")
    ad("")
    ad("## S1, total car-km, descriptive")
    ad("")
    ad(f"Cars x km per car, 2005-2018: {fl('S1_car_km_billion_first'):.2f} billion km in 2005, a peak of "
       f"{fl('S1_car_km_billion_max'):.2f} billion in {int(fl('S1_car_km_billion_max_year'))}, "
       f"{fl('S1_car_km_billion_last'):.2f} billion in 2018. No prediction, no score, no weight in the verdict.")
    ad("")
    ad("## T6, 2020 and 2021, descriptive")
    ad("")
    t = t1y.set_index(["road", "year"]).speed
    ad(f"Peak speed in 2020 and 2021: expressways {t['expressway', 2020]:g} and {t['expressway', 2021]:g} km/h, "
       f"arterial roads {t['arterial', 2020]:g} and {t['arterial', 2021]:g} km/h. Not scored; the circuit "
       "breaker emptied the roads in the same weeks that ERP charging stopped.")
    ad("")
    ad("## Charts")
    ad("")
    ad("- `figs/chart1_speed_vs_band.svg`: peak speed against LTA's bands, both road types, with "
       "cars per lane-km underneath.")
    ad("- `figs/chart2_door_fee.svg`: km per car in the 7 highest- and 7 lowest-premium years.")
    ad("")

    with open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L).rstrip("\n") + "\n")
    print("  RESULTS.md written")


if __name__ == "__main__":
    main()
