"""
16_bands.py -- LTA's example feebate bands (consultation paper Tables 1-2), per model.

  python3 lta-ab/16_bands.py          write out/bands.csv and out/bands_summary.csv, then check
  python3 lta-ab/16_bands.py --check  check only: both files equal what this script writes,
                                      and the checks below hold

Source: raw/coe-public-consult.pdf, page 11 (Table 1, Option A, three bands) and
page 12 (Table 2, Option B, five bands), both "based on 2025 registrations".
The bands, their OMV percentile ranges and amounts, and every model named in
either table are keyed in by hand below, as printed. The tables list "Typical
Models (non-exhaustive)", so the 30 models are LTA's examples, not every model.
Amounts are LTA's examples: as proposed, not final.

Checks (asserted):
  - the same 30 models appear in both tables, once each;
  - each model's Option A band agrees with its Option B band: B1-B2 -> A1,
    B3 -> A2, B4-B5 -> A3 (the percentile ranges nest: 0-10-35 | 35-50 | 50-75-100);
  - for each option, the registration-weighted average adjustment, from the
    percentile ranges (a band's share of 2025 registrations is the width of its
    percentile range), is +$2,250 a car: surcharges exceed rebates at that mix.

out/bands.csv          model, option_A_band, option_A_amount, option_B_band,
                       option_B_amount, source (amounts: negative = rebate)
out/bands_summary.csv  key, value, printed, definition: the numbers ONEPAGER.md uses
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
BANDS_CSV = os.path.join(OUT, "bands.csv")
SUMMARY_CSV = os.path.join(OUT, "bands_summary.csv")
SRC_A = "raw/coe-public-consult.pdf p.11, Table 1"
SRC_B = "raw/coe-public-consult.pdf p.12, Table 2"

# band: (percentile from, percentile to, amount in dollars; negative = rebate)
OPTION_A = {1: (0, 35, -15000), 2: (35, 50, 0), 3: (50, 100, 15000)}            # page 11
OPTION_B = {1: (0, 10, -15000), 2: (10, 35, -7500), 3: (35, 50, 0),              # page 12
            4: (50, 75, 7500), 5: (75, 100, 15000)}

# Models as printed in each table, by band.
TABLE_A = {  # page 11, Table 1
    1: ["BYD Atto 3", "BYD E6", "Honda Freed", "Honda Jazz", "Hyundai Kona 1.6 HEV", "Mazda 3",
        "MG S5", "Nissan Note", "Suzuki Swift", "Toyota Noah", "Toyota Sienta", "Volvo EX30 110kW"],
    2: ["Audi A3", "BYD Sealion 7 Dynamic", "Honda Civic 1.5 Turbo", "Nissan Serena",
        "Toyota Corolla Altis", "Xpeng G6 RWD (STD Range)"],
    3: ["Audi Q3", "B.M.W. 216", "B.M.W. iX2", "BYD Sealion 7 Performance", "Denza D9",
        "Honda Civic Type R", "Honda Odyssey", "Mercedes Benz A180", "Mercedes Benz GLC",
        "Tesla Model 3 RWD 110", "Tesla Model Y RWD", "Toyota Alphard"],
}
TABLE_B = {  # page 12, Table 2
    1: ["BYD E6", "Honda Jazz", "Mazda 3", "MG S5", "Nissan Note", "Suzuki Swift"],
    2: ["BYD Atto 3", "Honda Freed", "Hyundai Kona 1.6 HEV", "Toyota Noah", "Toyota Sienta",
        "Volvo EX30 110kW"],
    3: ["Audi A3", "BYD Sealion 7 Dynamic", "Honda Civic 1.5 Turbo", "Nissan Serena",
        "Toyota Corolla Altis", "Xpeng G6 RWD (STD Range)"],
    4: ["Audi Q3", "B.M.W. 216", "BYD Sealion 7 Performance", "Honda Odyssey",
        "Mercedes Benz A180", "Tesla Model 3 RWD 110"],
    5: ["B.M.W. iX2", "Denza D9", "Honda Civic Type R", "Mercedes Benz GLC", "Tesla Model Y RWD",
        "Toyota Alphard"],
}
B_TO_A = {1: 1, 2: 1, 3: 2, 4: 3, 5: 3}
EXPECTED_AVG = 2250
SEALION = ("BYD Sealion 7 Dynamic", "BYD Sealion 7 Performance")


def dollars(x):
    return "{:,}".format(abs(int(x)))


def by_model(table):
    m = {}
    for band, models in table.items():
        for name in models:
            assert name not in m, f"{name} listed twice"
            m[name] = band
    return m


def build():
    a, b = by_model(TABLE_A), by_model(TABLE_B)
    assert set(a) == set(b), sorted(set(a) ^ set(b))
    for name in a:
        assert B_TO_A[b[name]] == a[name], f"{name}: Option B band {b[name]} vs Option A band {a[name]}"
    rows = sorted(a, key=lambda n: (b[n], n))

    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["model", "option_A_band", "option_A_amount", "option_B_band", "option_B_amount", "source"])
    for n in rows:
        w.writerow([n, a[n], OPTION_A[a[n]][2], b[n], OPTION_B[b[n]][2], f"{SRC_A}; {SRC_B}"])

    S = []

    def fact(key, value, printed, definition):
        S.append([key, value, printed, definition])
    fact("n_models", len(rows), str(len(rows)), "models named in Tables 1-2 (the same in both)")
    for opt, bands in (("A", OPTION_A), ("B", OPTION_B)):
        assert sum(hi - lo for lo, hi, _ in bands.values()) == 100
        tot = sum((hi - lo) * amt for lo, hi, amt in bands.values())
        assert tot % 100 == 0
        avg = tot // 100
        assert avg == EXPECTED_AVG, (opt, avg)
        fact(f"avg_adjustment_{opt}", avg, dollars(avg),
             f"Option {opt}: registration-weighted average adjustment at the 2025 mix, dollars a car (positive: surcharges exceed rebates)")
        sur = sum(hi - lo for lo, hi, amt in bands.values() if amt > 0)
        reb = sum(hi - lo for lo, hi, amt in bands.values() if amt < 0)
        fact(f"surcharge_share_{opt}", sur, str(sur), f"Option {opt}: per cent of 2025 registrations in surcharge bands")
        fact(f"rebate_share_{opt}", reb, str(reb), f"Option {opt}: per cent of 2025 registrations in rebate bands")
        fact(f"zero_share_{opt}", 100 - sur - reb, str(100 - sur - reb), f"Option {opt}: per cent in the $0 band")
        s_avg = sum((hi - lo) * amt for lo, hi, amt in bands.values() if amt > 0) / 100
        r_avg = sum((hi - lo) * -amt for lo, hi, amt in bands.values() if amt < 0) / 100
        assert s_avg - r_avg == avg
        fact(f"surcharge_avg_{opt}", s_avg, dollars(s_avg),
             f"Option {opt}: surcharges per car, averaged over all 2025 registrations, dollars")
        fact(f"rebate_avg_{opt}", r_avg, dollars(r_avg),
             f"Option {opt}: rebates per car, averaged over all 2025 registrations, dollars")
    gap_a = OPTION_A[a[SEALION[1]]][2] - OPTION_A[a[SEALION[0]]][2]
    gap_b = OPTION_B[b[SEALION[1]]][2] - OPTION_B[b[SEALION[0]]][2]
    fact("sealion_gap_A", gap_a, dollars(gap_a), "Option A: Sealion 7 Performance minus Dynamic, dollars")
    fact("sealion_gap_B", gap_b, dollars(gap_b), "Option B: Sealion 7 Performance minus Dynamic, dollars")
    for opt, bands in (("A", OPTION_A), ("B", OPTION_B)):
        for band, (lo, hi, amt) in bands.items():
            fact(f"pct_from_{opt}{band}", lo, str(lo), f"Option {opt} band {band}: OMV percentile from")
            fact(f"pct_to_{opt}{band}", hi, str(hi), f"Option {opt} band {band}: OMV percentile to")
    sbuf = io.StringIO()
    csv.writer(sbuf, lineterminator="\n").writerows([["key", "value", "printed", "definition"]] + S)
    return buf.getvalue(), sbuf.getvalue()


def main():
    bands, summary = build()
    if "--check" in sys.argv:
        ok = (open(BANDS_CSV, encoding="utf-8").read() == bands
              and open(SUMMARY_CSV, encoding="utf-8").read() == summary)
        print("  out/bands.csv and out/bands_summary.csv " + ("match the tables" if ok else "are STALE"))
        return 0 if ok else 1
    os.makedirs(OUT, exist_ok=True)
    with open(BANDS_CSV, "w", encoding="utf-8", newline="\n") as f:
        f.write(bands)
    with open(SUMMARY_CSV, "w", encoding="utf-8", newline="\n") as f:
        f.write(summary)
    n = bands.count("\n") - 1
    print(f"  wrote out/bands.csv ({n} models) and out/bands_summary.csv; "
          f"both options average +${EXPECTED_AVG:,} a car at the 2025 mix; A and B bands agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
