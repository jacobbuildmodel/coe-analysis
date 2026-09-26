"""
15_reproduce.py -- recompute every scored number by a different code path and
assert it agrees with out/tests.csv to the precision RESULTS.md prints.

Different path, on purpose: raw files read with the csv module (no pandas),
regressions by numpy.linalg.lstsq with the HC1 sandwich written out by hand
(no statsmodels), the 90 per cent critical value from statistics.NormalDist,
the T1 band check and the T3 split as plain loops. The only shared input is
erp/raw/. 2025's car count is read from the E3b PDF's text by a regex over
the whole page rather than line by line.
"""
import csv
import os
import re
import statistics

import numpy as np
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
Z90 = statistics.NormalDist().inv_cdf(0.95)


def rows(name):
    with open(os.path.join(RAW, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def hc1(y, X):
    y = np.asarray(y, float)
    X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in X])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    n, k = X.shape
    inv = np.linalg.inv(X.T @ X)
    V = inv @ (X.T * e ** 2) @ X @ inv * n / (n - k)
    se = np.sqrt(np.diag(V))
    tss = ((y - y.mean()) ** 2).sum()
    r2 = 1 - (e ** 2).sum() / tss
    adj = 1 - (1 - r2) * (n - 1) / (n - k)
    return b, b - Z90 * se, b + Z90 * se, r2, adj


def main():
    speed = {"expressway": {}, "arterial": {}}
    for r in rows("e1_peak_speed.csv"):
        speed["expressway"][int(r["year"])] = float(r["ave_speed_expressway"])
        speed["arterial"][int(r["year"])] = float(r["ave_speed_arterial_roads"])

    cars = {}
    for r in rows("e3_vehicle_population.csv"):
        if r["category"] == "Cars and Station-wagons":
            cars[int(r["year"])] = cars.get(int(r["year"]), 0) + int(r["number"])
    page = PdfReader(os.path.join(RAW, "e3b_lta_mvp_by_type_2025.pdf")).pages[0].extract_text()
    m = re.search(r"1 Cars & Station-wagons((?:\s+[\d,]+){11})", page)
    cars[2025] = int(m.group(1).split()[-1].replace(",", ""))

    lane = {"expressway": {}, "arterial": {}}
    for r in rows("e8_lane_km.csv"):
        key = {"Expressway": "expressway", "Arterial Road": "arterial"}.get(r["road_type"])
        if key:
            lane[key][int(r["year"])] = float(r["road_length"])

    km = {int(r["year"]): float(r["average_annual_mileage"])
          for r in rows("e2_km_per_vehicle.csv") if r["vehicle_type"] == "Cars"}

    prem = {}
    q = {r["DataSeries"]: r for r in rows("e4b_quota_premium_monthly.csv")}
    for cat in ("Cars Up To 1600cc And 97kW", "Cars Above 1600cc Or 97kW"):
        by_year = {}
        r1 = q[f"{cat}, Quota Premium, 1st Bidding"]
        r2 = q[f"{cat}, Quota Premium, 2nd Bidding"]
        for col in r1:
            if col == "DataSeries":
                continue
            vals = [float(v) for v in (r1[col], r2[col]) if v != "-"]
            if vals:
                by_year.setdefault(int(col[:4]), []).append(sum(vals) / len(vals))
        for y, v in by_year.items():
            prem.setdefault(y, []).append(sum(v) / len(v))
    prem = {y: sum(v) / 2 for y, v in prem.items()}

    got = {}
    # T1
    scored = {"expressway": [y for y in range(2004, 2026) if y not in (2011, 2019, 2020, 2021, 2022, 2023)],
              "arterial": [y for y in range(2004, 2026) if y not in (2011, 2020, 2021)]}
    band = {"expressway": (45, 65), "arterial": (20, 30)}
    for c in scored:
        lo, hi = band[c]
        got[f"T1_{c}_above"] = sum(speed[c][y] > hi for y in scored[c])
        got[f"T1_{c}_below"] = sum(speed[c][y] < lo for y in scored[c])
        cp = [cars[y] for y in scored[c] if y in cars]
        got[f"T1_{c}_carpop_range_share_pct"] = 100 * (max(cp) - min(cp)) / (sum(cp) / len(cp))
    t1_pass = all(got[f"T1_{c}_above"] + got[f"T1_{c}_below"] == 0 for c in scored)
    got["T1_outcome"] = "PASS" if t1_pass else "FAIL"

    # T2
    ys = list(range(2005, 2018))
    st2 = []
    for c in ("expressway", "arterial"):
        b, lo, hi, r2, _ = hc1([np.log(speed[c][y]) for y in ys],
                               [[np.log(cars[y] / lane[c][y]) for y in ys]])
        got[f"T2_{c}_slope"], got[f"T2_{c}_lo"], got[f"T2_{c}_hi"], got[f"T2_{c}_r2"] = b[1], lo[1], hi[1], r2
        st2.append("survive" if -0.5 <= b[1] <= 0.5 else "fail" if b[1] <= -1 else "inconclusive")
    for c in ("expressway", "arterial"):
        got[f"T2_{c}_density_rise_pct"] = 100 * ((cars[2017] / lane[c][2017]) / (cars[2005] / lane[c][2005]) - 1)
    got["T2_outcome"] = ("PASS" if all(s == "survive" for s in st2) else
                         "FAIL" if "fail" in st2 else "INCONCLUSIVE")

    # T3
    ys3 = list(range(2005, 2019))
    order = sorted(ys3, key=lambda y: -prem[y])
    high = [y for y in ys3 if prem[y] >= prem[order[6]]]
    low = [y for y in ys3 if y not in high]
    hm = sum(km[y] for y in high) / len(high)
    lm = sum(km[y] for y in low) / len(low)
    got.update({"T3_high_mean_km": hm, "T3_low_mean_km": lm, "T3_ratio": hm / lm,
                "T3_pct_lower": 100 * (1 - hm / lm), "T3_outcome": "PASS" if hm / lm >= 0.97 else "FAIL"})

    # T4
    ys4 = [y for y in range(2005, 2026) if y not in (2020, 2021)]
    st4 = []
    for c in ("expressway", "arterial"):
        yv = [np.log(speed[c][y]) for y in ys4]
        lc = [np.log(cars[y]) for y in ys4]
        lp = [np.log(prem[y]) for y in ys4]
        *_, adj0 = hc1(yv, [lc])
        b, lo, hi, _, adj1 = hc1(yv, [lc, lp])
        gain = adj1 - adj0
        got[f"T4_{c}_gain"] = gain
        got[f"T4_{c}_premium_coef"], got[f"T4_{c}_premium_ci_lo"], got[f"T4_{c}_premium_ci_hi"] = b[2], lo[2], hi[2]
        inc = lo[2] <= 0 <= hi[2]
        st4.append("pass" if gain < 0.10 and inc else "fail" if gain >= 0.10 and not inc else "mixed")
    got["T4_outcome"] = "PASS" if all(s == "pass" for s in st4) else "FAIL" if "fail" in st4 else "MIXED"

    # scorecard and verdict
    conf = {"T1": 0.35, "T2": 0.65, "T3": 0.20, "T4": 0.70}
    held = {k: 1 if got[f"{k}_outcome"] == "PASS" else 0 for k in conf}
    got["n_held"] = sum(held.values())
    got["expected_held"] = sum(conf.values())
    got["brier"] = sum((conf[k] - held[k]) ** 2 for k in conf) / 4
    below3 = any(got[f"T1_{c}_below"] >= 3 for c in scored)
    if got["T1_outcome"] == "PASS" and got["T2_outcome"] == "PASS":
        got["verdict"] = "The record looks more like extreme ERP"
    elif (got["T1_outcome"] == "FAIL" and below3) or got["T2_outcome"] == "FAIL":
        got["verdict"] = "The record looks more like extreme COE"
    else:
        got["verdict"] = "The record cannot tell the two apart"

    # S1
    s1 = {y: cars[y] * km[y] / 1e9 for y in ys3}
    got["S1_car_km_billion_first"] = s1[2005]
    got["S1_car_km_billion_last"] = s1[2018]
    got["S1_car_km_billion_max"] = max(s1.values())

    # compare at published precision
    with open(os.path.join(HERE, "out", "tests.csv"), newline="", encoding="utf-8") as f:
        pub = {r["key"]: r["value"] for r in csv.DictReader(f)}
    places = {"slope": 3, "_lo": 3, "_hi": 3, "_r2": 2, "gain": 3, "coef": 3, "ci_lo": 3, "ci_hi": 3,
              "mean_km": 0, "ratio": 3, "pct_lower": 1, "share_pct": 1, "brier": 3,
              "expected_held": 1, "billion": 2, "rise_pct": 1}
    n = 0
    for k, v in got.items():
        if isinstance(v, str):
            assert pub[k] == v, f"{k}: reproduce {v!r} vs published {pub[k]!r}"
        elif isinstance(v, (int, np.integer)) and not isinstance(v, bool):
            assert int(float(pub[k])) == int(v), f"{k}: reproduce {v} vs published {pub[k]}"
        else:
            d = next(p for s, p in places.items() if s in k)
            assert round(float(pub[k]), d) == round(float(v), d), \
                f"{k}: reproduce {float(v):.{d + 3}f} vs published {float(pub[k]):.{d + 3}f}"
        n += 1
    print(f"  {n} scored numbers and outcomes reproduced independently, all agree")


if __name__ == "__main__":
    main()
