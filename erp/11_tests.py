"""
11_tests.py -- T1-T4 exactly as sealed in THESIS.md (6d2a345), T5 leg (a)
reported unscored, S1 descriptive, the section 8 verdict and the scorecard.

Reads out/annual.csv (10_load.py). Writes out/t1_years.csv, out/t2_fits.csv,
out/t3_split.csv, out/t4_fits.csv, out/tests.csv, out/s1.csv.

Conventions fixed here and nowhere else:
  * "lies within 45-65 km/h" is read as the closed interval, 45 <= v <= 65.
  * Every regression is OLS with HC1 standard errors; the 90 per cent interval
    is statsmodels' conf_int(alpha=0.10), which with a robust covariance uses
    the normal distribution.
  * A prediction "holds" only when its outcome is PASS (THESIS section 8).
"""
import os

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FLOAT = "%.10g"

BANDS = {"expressway": (45.0, 65.0), "arterial": (20.0, 30.0)}
LANEKM = {"expressway": "lanekm_expressway", "arterial": "lanekm_arterial"}
CLASSES = ("expressway", "arterial")

# THESIS section 6, T1 "Scored years", verbatim as numbers
T1_YEARS = {
    "expressway": list(range(2004, 2011)) + list(range(2012, 2019)) + [2024, 2025],
    "arterial": list(range(2004, 2011)) + list(range(2012, 2020)) + list(range(2022, 2026)),
}
T2_YEARS = list(range(2005, 2018))
T3_YEARS = list(range(2005, 2019))
T4_YEARS = [y for y in range(2005, 2026) if y not in (2020, 2021)]
SEEN = {"expressway": {2011, 2019, 2022, 2023}, "arterial": {2011}}

# Jacob's confidences, THESIS section 6, set 25 September 2026
CONFIDENCE = {"T1": 0.35, "T2": 0.65, "T3": 0.20, "T4": 0.70}


def ols(y, cols):
    X = sm.add_constant(np.column_stack(cols))
    r = sm.OLS(np.asarray(y, float), X).fit(cov_type="HC1")
    ci = r.conf_int(alpha=0.10)
    return r, ci


def fit_row(test, spec, cls, years, y, x_cols, names):
    r, ci = ols(y, x_cols)
    row = {"test": test, "spec": spec, "road": cls, "n": len(years),
           "first_year": min(years), "last_year": max(years),
           "r2": r.rsquared, "adj_r2": r.rsquared_adj}
    for i, nm in enumerate(names, start=1):
        row[f"{nm}_coef"] = r.params[i]
        row[f"{nm}_ci_lo"] = ci[i][0]
        row[f"{nm}_ci_hi"] = ci[i][1]
    return row


def main():
    t = pd.read_csv(os.path.join(OUT, "annual.csv")).set_index("year")
    speed = {c: t[f"speed_{c}"] for c in CLASSES}
    tests = []

    # ---------------- T1 ----------------
    rows, t1 = [], {}
    for c in CLASSES:
        lo, hi = BANDS[c]
        for y in range(2004, 2026):
            v = speed[c].loc[y]
            scored = y in T1_YEARS[c]
            pos = "below" if v < lo else ("above" if v > hi else "inside")
            rows.append({"road": c, "year": y, "speed": v, "band_lo": lo, "band_hi": hi,
                         "position": pos, "scored": scored,
                         "excluded_reason": ("" if scored else
                                             "2020-2021" if y in (2020, 2021) else "seen before seal")})
        d = pd.DataFrame([r for r in rows if r["road"] == c and r["scored"]])
        cp = t.loc[[y for y in T1_YEARS[c] if not np.isnan(t.cars.loc[y])], "cars"]
        share = 100 * (cp.max() - cp.min()) / cp.mean()
        t1[c] = {"n": len(d), "above": int((d.position == "above").sum()),
                 "below": int((d.position == "below").sum()), "share": share,
                 "informative": share >= 10,
                 "outside_years": " ".join(str(int(y)) for y in d[d.position != "inside"].year)}
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "t1_years.csv"), index=False,
                              float_format=FLOAT, lineterminator="\n")
    inside_all = all(t1[c]["above"] + t1[c]["below"] == 0 for c in CLASSES)
    informative_all = all(t1[c]["informative"] for c in CLASSES)
    t1_outcome = ("FAIL" if not inside_all else "PASS" if informative_all else "UNINFORMATIVE")
    for c in CLASSES:
        tests.append({"key": f"T1_{c}_scored_years", "value": t1[c]["n"]})
        tests.append({"key": f"T1_{c}_above", "value": t1[c]["above"]})
        tests.append({"key": f"T1_{c}_below", "value": t1[c]["below"]})
        tests.append({"key": f"T1_{c}_outside_years", "value": t1[c]["outside_years"] or "none"})
        tests.append({"key": f"T1_{c}_carpop_range_share_pct", "value": t1[c]["share"]})
        tests.append({"key": f"T1_{c}_informative", "value": t1[c]["informative"]})
    tests.append({"key": "T1_outcome", "value": t1_outcome})

    # ---------------- T2 ----------------
    fits = []
    for c in CLASSES:
        ys = T2_YEARS
        dens = np.log(t.cars.loc[ys] / t[LANEKM[c]].loc[ys])
        y = np.log(speed[c].loc[ys])
        fits.append(fit_row("T2", "main: log cars per lane-km", c, ys, y, [dens], ["x"]))
        fits.append(fit_row("T2", "sens ii: main + linear trend", c, ys, y,
                            [dens, np.array(ys, float)], ["x", "trend"]))
        densp = np.log(t.cars_private.loc[ys] / t[LANEKM[c]].loc[ys])
        fits.append(fit_row("T2", "sens iii: private cars per lane-km", c, ys, y, [densp], ["x"]))
        ys4 = T4_YEARS
        fits.append(fit_row("T2", "sens i: log car population", c, ys4, np.log(speed[c].loc[ys4]),
                            [np.log(t.cars.loc[ys4])], ["x"]))
        if c == "arterial":
            # E8b prints 2923 arterial lane-km for 2008 where E8 has 2932; E8 is
            # the sealed source, this refit only shows what the other value does
            lk = t[LANEKM[c]].loc[ys].copy()
            lk.loc[2008] = 2923
            fits.append(fit_row("T2", "sens iv: E8b's 2008 arterial lane-km", c, ys, y,
                                [np.log(t.cars.loc[ys] / lk)], ["x"]))
    f2 = pd.DataFrame(fits)
    t2 = {}
    for c in CLASSES:
        m = f2[(f2.road == c) & (f2.spec == "main: log cars per lane-km")].iloc[0]
        s = m.x_coef
        t2[c] = {"slope": s, "lo": m.x_ci_lo, "hi": m.x_ci_hi, "r2": m.r2,
                 "status": "survive" if -0.5 <= s <= 0.5 else "fail" if s <= -1.0 else "inconclusive"}
        for k in ("slope", "lo", "hi", "r2", "status"):
            tests.append({"key": f"T2_{c}_{k}", "value": t2[c][k]})
    st = [t2[c]["status"] for c in CLASSES]
    t2_outcome = "PASS" if all(s == "survive" for s in st) else "FAIL" if "fail" in st else "INCONCLUSIVE"
    tests.append({"key": "T2_outcome", "value": t2_outcome})

    # ---------------- T3 ----------------
    d3 = t.loc[T3_YEARS, ["premium_ab", "km_per_car"]].copy()
    ranked = d3.sort_values("premium_ab", ascending=False)
    cut = ranked.premium_ab.iloc[6]
    d3["half"] = np.where(d3.premium_ab >= cut, "high", "low")
    assert (d3.half == "high").sum() == 7 and (d3.half == "low").sum() == 7
    ph = pd.read_csv(os.path.join(HERE, "raw", "e3_vehicle_population.csv"))
    ph = ph[ph.type.isin(["Private Hire (Chauffeur) cars", "Private Hire (Self-Drive) cars",
                          "Rental cars"])].groupby("year").number.sum()
    d3["hire_and_rental_cars"] = ph.reindex(d3.index)
    d3["hire_and_rental_change"] = d3.hire_and_rental_cars.diff()
    d3.to_csv(os.path.join(OUT, "t3_split.csv"), float_format=FLOAT, lineterminator="\n")
    hi_km = d3[d3.half == "high"].km_per_car.mean()
    lo_km = d3[d3.half == "low"].km_per_car.mean()
    ratio = hi_km / lo_km
    t3_outcome = "PASS" if ratio >= 0.97 else "FAIL"
    grow = d3[d3.hire_and_rental_change > 0]
    for k, v in [("T3_high_years", " ".join(str(y) for y in d3[d3.half == "high"].index)),
                 ("T3_low_years", " ".join(str(y) for y in d3[d3.half == "low"].index)),
                 ("T3_high_mean_km", hi_km), ("T3_low_mean_km", lo_km),
                 ("T3_ratio", ratio), ("T3_pct_lower", 100 * (1 - ratio)),
                 ("T3_hire_growth_in_high_half", float(grow[grow.half == "high"].hire_and_rental_change.sum())),
                 ("T3_hire_growth_in_low_half", float(grow[grow.half == "low"].hire_and_rental_change.sum())),
                 ("T3_outcome", t3_outcome)]:
        tests.append({"key": k, "value": v})

    # ---------------- T4 ----------------
    f4, t4 = [], {}
    for c in CLASSES:
        ys = T4_YEARS
        y = np.log(speed[c].loc[ys])
        lc = np.log(t.cars.loc[ys])
        lp = np.log(t.premium_ab.loc[ys])
        base = fit_row("T4", "base: log cars", c, ys, y, [lc], ["cars"])
        full = fit_row("T4", "full: log cars + log premium", c, ys, y, [lc, lp], ["cars", "premium"])
        f4 += [base, full]
        gain = full["adj_r2"] - base["adj_r2"]
        inc0 = full["premium_ci_lo"] <= 0 <= full["premium_ci_hi"]
        status = ("pass" if gain < 0.10 and inc0 else "fail" if gain >= 0.10 and not inc0 else "mixed")
        t4[c] = status
        for k, v in [("gain", gain), ("premium_coef", full["premium_coef"]),
                     ("premium_ci_lo", full["premium_ci_lo"]), ("premium_ci_hi", full["premium_ci_hi"]),
                     ("ci_includes_zero", inc0), ("status", status)]:
            tests.append({"key": f"T4_{c}_{k}", "value": v})
        # density sensitivity, not scored
        ys2 = T2_YEARS
        y2 = np.log(speed[c].loc[ys2])
        ld = np.log(t.cars.loc[ys2] / t[LANEKM[c]].loc[ys2])
        f4.append(fit_row("T4", "sens: base, density", c, ys2, y2, [ld], ["cars"]))
        f4.append(fit_row("T4", "sens: full, density + premium", c, ys2, y2,
                          [ld, np.log(t.premium_ab.loc[ys2])], ["cars", "premium"]))
    pd.DataFrame(f4).to_csv(os.path.join(OUT, "t4_fits.csv"), index=False,
                            float_format=FLOAT, lineterminator="\n")
    s4 = list(t4.values())
    t4_outcome = "PASS" if all(s == "pass" for s in s4) else "FAIL" if "fail" in s4 else "MIXED"
    tests.append({"key": "T4_outcome", "value": t4_outcome})

    f2.to_csv(os.path.join(OUT, "t2_fits.csv"), index=False, float_format=FLOAT, lineterminator="\n")

    # ---------------- T5 leg (a), unscored ----------------
    met = any(t2[c]["slope"] <= -1.0 and t2[c]["r2"] >= 0.5 for c in CLASSES)
    tests.append({"key": "T5a_met", "value": met})

    # ---------------- S1, descriptive ----------------
    s1 = t.loc[T3_YEARS, ["cars", "km_per_car"]].copy()
    s1["car_km_billion"] = s1.cars * s1.km_per_car / 1e9
    s1.to_csv(os.path.join(OUT, "s1.csv"), float_format=FLOAT, lineterminator="\n")
    tests.append({"key": "S1_car_km_billion_first", "value": s1.car_km_billion.iloc[0]})
    tests.append({"key": "S1_car_km_billion_last", "value": s1.car_km_billion.iloc[-1]})
    tests.append({"key": "S1_car_km_billion_max", "value": s1.car_km_billion.max()})
    tests.append({"key": "S1_car_km_billion_max_year", "value": int(s1.car_km_billion.idxmax())})

    # ---------------- scorecard ----------------
    outcomes = {"T1": t1_outcome, "T2": t2_outcome, "T3": t3_outcome, "T4": t4_outcome}
    scored = {k: v for k, v in outcomes.items() if v != "NOT SCORED"}
    held = {k: int(v == "PASS") for k, v in scored.items()}
    brier = np.mean([(CONFIDENCE[k] - held[k]) ** 2 for k in scored])
    expected = sum(CONFIDENCE[k] for k in scored)
    for k in outcomes:
        tests.append({"key": f"{k}_confidence", "value": CONFIDENCE[k]})
        tests.append({"key": f"{k}_held", "value": held.get(k, "")})
    tests += [{"key": "n_scored", "value": len(scored)},
              {"key": "n_held", "value": sum(held.values())},
              {"key": "expected_held", "value": expected},
              {"key": "brier", "value": brier}]

    # ---------------- verdict, section 8 ----------------
    t1_below3 = any(t1[c]["below"] >= 3 for c in CLASSES)
    if t1_outcome == "PASS" and t2_outcome == "PASS":
        verdict = "The record looks more like extreme ERP"
    elif (t1_outcome == "FAIL" and t1_below3) or t2_outcome == "FAIL":
        verdict = "The record looks more like extreme COE"
    else:
        verdict = "The record cannot tell the two apart"
    tests.append({"key": "verdict", "value": verdict})

    pd.DataFrame(tests).to_csv(os.path.join(OUT, "tests.csv"), index=False,
                               float_format=FLOAT, lineterminator="\n")
    for k, v in outcomes.items():
        print(f"  {k}: {v}  (confidence {CONFIDENCE[k]:.2f})")
    print(f"  held {sum(held.values())} of {len(scored)}, expected {expected:.1f}; Brier {brier:.4f}")
    print(f"  verdict: {verdict}")


if __name__ == "__main__":
    main()
