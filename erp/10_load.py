"""
10_load.py -- read erp/raw/ into one tidy annual table.

Every input is checked against erp/raw/RETRIEVED.txt before a value is used:
the md5, the row count and the first and last period recorded there by
00_coverage.py at retrieval. A file that has changed since retrieval stops
the run.

Definitions follow THESIS.md section 4 as sealed at 6d2a345:

  cars          E3 total for category "Cars and Station-wagons" (every car
                type E3 reports under cars; taxis and tax-exempted vehicles
                are separate categories and are not cars here). 2025 from
                E3b, LTA's MVP01-1 PDF. E3b's 2015-2024 totals are asserted
                equal to E3's, so the 2025 figure comes from a file that
                agrees with E3 wherever the two overlap.
  cars_private  E3 type "Private cars" (sensitivity only).
  lanekm_*      E8 lane-km, Expressway and Arterial Road rows, 2005-2017.
                E8b (PDF, 2005-2014) is compared, not used.
  km_per_car    E2 vehicle_type "Cars", 2005-2018.
  premium_*     E4b monthly Category A ("Cars Up To 1600cc And 97kW") and
                Category B ("Cars Above 1600cc Or 97kW") quota premiums. Each
                month is the mean of the exercises held that month; months
                with no bidding ("-") are left out; the year is the mean of
                its months; premium_ab is the mean of the A and B annual means.
                E4 (../raw.csv) is used only to cross-check 2010-2025.

Writes out/annual.csv, out/crosscheck_premium.csv, out/crosscheck_e3_e8.csv.
"""
import hashlib
import os
import re
import sys

import numpy as np
import pandas as pd
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "out")
ROOT_RAW = os.path.join(os.path.dirname(HERE), "raw.csv")
FLOAT = "%.10g"

CAT_A = "Cars Up To 1600cc And 97kW"
CAT_B = "Cars Above 1600cc Or 97kW"


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def retrieved_records():
    """Parse the per-file blocks 00_coverage.py wrote into RETRIEVED.txt."""
    text = open(os.path.join(RAW, "RETRIEVED.txt"), encoding="utf-8").read()
    recs = {}
    for m in re.finditer(r"^(\S+\.(?:csv|pdf))\n((?:  .*\n)+)", text, re.M):
        body = m.group(2)
        rec = {}
        for key in ("bytes", "md5", "rows"):
            k = re.search(rf"^  {key}\s+(\S+)", body, re.M)
            if k:
                rec[key] = k.group(1)
        p = re.search(r"^  period\s+year: (\d{4}) to (\d{4})", body, re.M)
        if p:
            rec["first"], rec["last"] = int(p.group(1)), int(p.group(2))
        recs[m.group(1)] = rec
    return recs


def check(name, recs, df=None, year_col="year"):
    path = os.path.join(RAW, name)
    rec = recs[name]
    got = md5(path)
    assert got == rec["md5"], f"{name}: md5 {got} != RETRIEVED {rec['md5']}"
    assert os.path.getsize(path) == int(rec["bytes"]), f"{name}: size changed"
    if df is not None:
        assert len(df) == int(rec["rows"]), f"{name}: rows {len(df)} != {rec['rows']}"
        if "first" in rec:
            assert df[year_col].min() == rec["first"], f"{name}: first year"
            assert df[year_col].max() == rec["last"], f"{name}: last year"
    print(f"  {name:36s} md5 ok, {len(df) if df is not None else '-'} rows")


def e3b_table():
    """Cars & Station-wagons row of LTA MVP01-1, 2015-2025, from the PDF text."""
    text = PdfReader(os.path.join(RAW, "e3b_lta_mvp_by_type_2025.pdf")).pages[0].extract_text()
    lines = text.splitlines()
    head = next(l for l in lines if l.startswith("End of Period (Year)"))
    years = [int(y) for y in re.findall(r"\b(20\d\d)\b", head)]

    def row(label):
        line = next(l for l in lines if l.startswith(label))
        nums = [int(n.replace(",", "")) for n in re.findall(r"\d{1,3}(?:,\d{3})+|\d+", line[len(label):])]
        assert len(nums) == len(years), f"E3b row '{label}': {len(nums)} values for {len(years)} years"
        return pd.Series(nums, index=years)

    return row("1 Cars & Station-wagons"), row("i) Private cars")


def main():
    os.makedirs(OUT, exist_ok=True)
    recs = retrieved_records()

    e1 = pd.read_csv(os.path.join(RAW, "e1_peak_speed.csv"))
    check("e1_peak_speed.csv", recs, e1)
    e2 = pd.read_csv(os.path.join(RAW, "e2_km_per_vehicle.csv"))
    check("e2_km_per_vehicle.csv", recs, e2)
    e3 = pd.read_csv(os.path.join(RAW, "e3_vehicle_population.csv"))
    check("e3_vehicle_population.csv", recs, e3)
    e4b = pd.read_csv(os.path.join(RAW, "e4b_quota_premium_monthly.csv"), dtype=str)
    check("e4b_quota_premium_monthly.csv", recs, e4b)
    e8 = pd.read_csv(os.path.join(RAW, "e8_lane_km.csv"))
    check("e8_lane_km.csv", recs, e8)
    for pdf in ("e3b_lta_mvp_by_type_2025.pdf", "e8b_lta_road_length_lane_km.pdf"):
        check(pdf, recs)

    # coverage stated in THESIS section 4, asserted
    assert (e1.year.min(), e1.year.max(), e1.year.nunique()) == (2004, 2025, 22)
    assert (e2.year.min(), e2.year.max()) == (2005, 2018)
    assert (e3.year.min(), e3.year.max()) == (2005, 2024)
    assert (e8.year.min(), e8.year.max()) == (2005, 2017)
    months = [c for c in e4b.columns if c != "DataSeries"]
    assert months[0] == "2026Aug" and months[-1] == "2002Feb", (months[0], months[-1])

    # E1
    speed = e1.set_index("year").rename(columns={
        "ave_speed_expressway": "speed_expressway",
        "ave_speed_arterial_roads": "speed_arterial"})

    # E3 + E3b
    carcat = e3[e3.category == "Cars and Station-wagons"]
    cars = carcat.groupby("year").number.sum()
    priv = carcat[carcat.type == "Private cars"].set_index("year").number
    b_cars, b_priv = e3b_table()
    overlap = [y for y in b_cars.index if y in cars.index]
    assert overlap == list(range(2015, 2025)), overlap
    assert (cars.loc[overlap] == b_cars.loc[overlap]).all(), "E3 vs E3b cars differ"
    assert (priv.loc[overlap] == b_priv.loc[overlap]).all(), "E3 vs E3b private cars differ"
    cars.loc[2025] = b_cars.loc[2025]
    priv.loc[2025] = b_priv.loc[2025]

    # E8
    lk = e8.pivot(index="year", columns="road_type", values="road_length")
    lanekm = lk[["Expressway", "Arterial Road"]].rename(columns={
        "Expressway": "lanekm_expressway", "Arterial Road": "lanekm_arterial"})

    # E2
    km = e2[e2.vehicle_type == "Cars"].set_index("year").average_annual_mileage
    assert len(km) == 14

    # E4b
    q = e4b.set_index("DataSeries")

    def annual(cat):
        rows = q.loc[[f"{cat}, Quota Premium, 1st Bidding",
                      f"{cat}, Quota Premium, 2nd Bidding"]]
        vals = rows.replace("-", np.nan).astype(float)
        monthly = vals.mean(axis=0, skipna=True).dropna()
        yr = pd.Index([int(c[:4]) for c in monthly.index], name="year")
        g = monthly.groupby(yr)
        return g.mean(), g.size()

    pa, na_ = annual(CAT_A)
    pb, nb = annual(CAT_B)
    assert (na_ == nb).all()

    t = pd.DataFrame(index=pd.Index(range(2004, 2026), name="year"))
    t = t.join(speed).join(cars.rename("cars")).join(priv.rename("cars_private"))
    t = t.join(lanekm).join(km.rename("km_per_car"))
    t["premium_a"] = pa
    t["premium_b"] = pb
    t["premium_ab"] = (pa + pb) / 2
    t["premium_months"] = na_
    t.to_csv(os.path.join(OUT, "annual.csv"), float_format=FLOAT, lineterminator="\n")

    # cross-check E4b against E4 (../raw.csv), 2010-2025, same annual rule
    r = pd.read_csv(ROOT_RAW)
    r = r[r.vehicle_class.isin(["Category A", "Category B"])].copy()
    r["premium"] = r.premium.astype(str).str.replace(",", "").astype(float)
    r["year"] = r.month.str[:4].astype(int)
    m = r.groupby(["vehicle_class", "month"]).premium.mean().reset_index()
    m["year"] = m.month.str[:4].astype(int)
    e4 = m.groupby(["vehicle_class", "year"]).premium.mean().unstack(0)
    e4_ab = (e4["Category A"] + e4["Category B"]) / 2
    xc = pd.DataFrame({"e4b_premium_ab": t.premium_ab.loc[2010:2025],
                       "e4_premium_ab": e4_ab.loc[2010:2025]})
    xc["diff_pct"] = 100 * (xc.e4_premium_ab / xc.e4b_premium_ab - 1)
    xc["over_1pct"] = xc.diff_pct.abs() > 1
    xc.to_csv(os.path.join(OUT, "crosscheck_premium.csv"), float_format=FLOAT, lineterminator="\n")

    # E8b against E8, and E3b against E3 (already asserted), recorded
    text = PdfReader(os.path.join(RAW, "e8b_lta_road_length_lane_km.pdf")).pages[0].extract_text()
    rows = []
    for line in text.splitlines():
        mm = re.match(r"\s*((?:19|20)\d\d)\s+(.*)", line)
        if mm:
            nums = [int(x.replace(",", "")) for x in re.findall(r"\d{1,3}(?:,\d{3})*", mm.group(2))]
            y = int(mm.group(1))
            rows.append({"year": y, "e8b_expressway": nums[0], "e8b_arterial": nums[1],
                         "e8_expressway": int(lanekm.loc[y, "lanekm_expressway"]),
                         "e8_arterial": int(lanekm.loc[y, "lanekm_arterial"])})
    x8 = pd.DataFrame(rows).set_index("year")
    x8["agree"] = (x8.e8b_expressway == x8.e8_expressway) & (x8.e8b_arterial == x8.e8_arterial)
    x8.to_csv(os.path.join(OUT, "crosscheck_e3_e8.csv"), lineterminator="\n")

    print(f"  annual.csv: {len(t)} years, 2004-2025")
    print(f"  E3b 2015-2024 equals E3 in every year; 2025 cars {int(cars.loc[2025])}")
    print(f"  E8b vs E8: {int(x8.agree.sum())} of {len(x8)} years agree")
    n_over = int(xc.over_1pct.sum())
    print(f"  E4b vs E4 premium, 2010-2025: {n_over} year(s) differ by more than 1 per cent"
          f" (largest {xc.diff_pct.abs().max():.3f} per cent)")


if __name__ == "__main__":
    sys.exit(main())
