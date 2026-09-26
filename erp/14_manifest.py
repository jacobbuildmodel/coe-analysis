"""
14_manifest.py -- the ERP piece's checksums and number manifest.

  python3 erp/14_manifest.py          regenerate erp/number_manifest.csv and
                                      erp/CHECKSUMS.md5. Manual step, run LAST,
                                      after every other edit.
  python3 erp/14_manifest.py --check  verify both, never write: every md5 in
                                      CHECKSUMS.md5 matches; the manifest,
                                      rebuilt from out/, equals the committed
                                      file; every manifest value appears in
                                      RESULTS.md as printed.

CHECKSUMS.md5 has two labelled sections, paths relative to erp/. INPUTS are the
scripts, the sealed thesis, its addendum and every raw file read; OUTPUTS are
out/, figs/, RESULTS.md and number_manifest.csv. A changed OUTPUT with
unchanged INPUTS means the pipeline is not deterministic.
"""
import csv
import glob
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

INPUTS = ["00_coverage.py", "10_load.py", "11_tests.py", "12_figures.py", "13_results.py",
          "14_manifest.py", "15_reproduce.py", "run_all.sh", "requirements.txt",
          "THESIS.md", "THESIS_ADDENDUM.md",
          "raw/RETRIEVED.txt", "raw/e1_peak_speed.csv", "raw/e2_km_per_vehicle.csv",
          "raw/e3_vehicle_population.csv", "raw/e3b_lta_mvp_by_type_2025.pdf",
          "raw/e4b_quota_premium_monthly.csv", "raw/e8_lane_km.csv",
          "raw/e8b_lta_road_length_lane_km.pdf", "../raw.csv"]

# (id, tests.csv key, printed format, meaning)
NUMBERS = [
    ("T1_art_above", "T1_arterial_above", "{:d}", "scored arterial years above 30 km/h"),
    ("T1_art_below", "T1_arterial_below", "{:d}", "scored arterial years below 20 km/h"),
    ("T1_exp_above", "T1_expressway_above", "{:d}", "scored expressway years above 65 km/h"),
    ("T1_exp_below", "T1_expressway_below", "{:d}", "scored expressway years below 45 km/h"),
    ("T1_exp_share", "T1_expressway_carpop_range_share_pct", "{:.1f}", "car population range, % of mean, expressway scored years"),
    ("T1_art_share", "T1_arterial_carpop_range_share_pct", "{:.1f}", "car population range, % of mean, arterial scored years"),
    ("T2_exp_slope", "T2_expressway_slope", "{:.3f}", "T2 elasticity, expressways, speed on cars per lane-km"),
    ("T2_exp_lo", "T2_expressway_lo", "{:.3f}", "T2 90% interval low, expressways"),
    ("T2_exp_hi", "T2_expressway_hi", "{:.3f}", "T2 90% interval high, expressways"),
    ("T2_exp_r2", "T2_expressway_r2", "{:.2f}", "T2 R-squared, expressways"),
    ("T2_art_slope", "T2_arterial_slope", "{:.3f}", "T2 elasticity, arterial roads"),
    ("T2_art_lo", "T2_arterial_lo", "{:.3f}", "T2 90% interval low, arterial"),
    ("T2_art_hi", "T2_arterial_hi", "{:.3f}", "T2 90% interval high, arterial"),
    ("T2_art_r2", "T2_arterial_r2", "{:.2f}", "T2 R-squared, arterial"),
    ("T3_high_km", "T3_high_mean_km", "{:,.0f}", "mean km per car, 7 highest-premium years"),
    ("T3_low_km", "T3_low_mean_km", "{:,.0f}", "mean km per car, 7 lowest-premium years"),
    ("T3_ratio", "T3_ratio", "{:.3f}", "high / low km per car"),
    ("T3_pct", "T3_pct_lower", "{:.1f}", "per cent by which high-premium years were lower"),
    ("T3_hire_high", "T3_hire_growth_in_high_half", "{:,.0f}", "hire and rental cars added in high-premium years"),
    ("T3_hire_low", "T3_hire_growth_in_low_half", "{:,.0f}", "hire and rental cars added in low-premium years"),
    ("T4_exp_gain", "T4_expressway_gain", "{:.3f}", "T4 adjusted R-squared gain, expressways"),
    ("T4_exp_coef", "T4_expressway_premium_coef", "{:.3f}", "T4 premium coefficient, expressways"),
    ("T4_exp_lo", "T4_expressway_premium_ci_lo", "{:.3f}", "T4 premium 90% interval low, expressways"),
    ("T4_exp_hi", "T4_expressway_premium_ci_hi", "{:.3f}", "T4 premium 90% interval high, expressways"),
    ("T4_art_gain", "T4_arterial_gain", "{:.3f}", "T4 adjusted R-squared gain, arterial"),
    ("T4_art_coef", "T4_arterial_premium_coef", "{:.3f}", "T4 premium coefficient, arterial"),
    ("T4_art_lo", "T4_arterial_premium_ci_lo", "{:.3f}", "T4 premium 90% interval low, arterial"),
    ("T4_art_hi", "T4_arterial_premium_ci_hi", "{:.3f}", "T4 premium 90% interval high, arterial"),
    ("n_held", "n_held", "{:d}", "predictions held"),
    ("expected", "expected_held", "{:.1f}", "expected predictions held, sum of confidences"),
    ("brier", "brier", "{:.3f}", "Brier score, mean over the four scored tests"),
    ("S1_2005", "S1_car_km_billion_first", "{:.2f}", "total car-km 2005, billion"),
    ("S1_max", "S1_car_km_billion_max", "{:.2f}", "total car-km peak, billion"),
    ("S1_2018", "S1_car_km_billion_last", "{:.2f}", "total car-km 2018, billion"),
]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def outputs():
    files = sorted(glob.glob(os.path.join(HERE, "out", "*.csv")) +
                   glob.glob(os.path.join(HERE, "figs", "*.svg")))
    rel = [os.path.relpath(f, HERE).replace(os.sep, "/") for f in files]
    return rel + ["RESULTS.md", "number_manifest.csv"]


def build_manifest():
    with open(os.path.join(HERE, "out", "tests.csv"), newline="", encoding="utf-8") as f:
        T = {r["key"]: r["value"] for r in csv.DictReader(f)}
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["number_id", "value", "meaning", "script", "output_file", "key"])
    for nid, key, fmt, meaning in NUMBERS:
        v = float(T[key])
        val = fmt.format(int(v) if fmt == "{:d}" else v)
        w.writerow([nid, val, meaning, "11_tests.py", "erp/out/tests.csv", key])
    return buf.getvalue()


def build_checksums():
    lines = ["# MD5 checksums, ERP piece. Regenerate with:",
             "#   python3 erp/14_manifest.py",
             "# Never written by run_all.sh, which only runs --check.",
             "# Paths are relative to erp/.", "", "# INPUTS"]
    for p in INPUTS:
        lines.append(f"{md5(os.path.join(HERE, p))}  {p}")
    lines += ["", "# OUTPUTS"]
    for p in outputs():
        lines.append(f"{md5(os.path.join(HERE, p))}  {p}")
    return "\n".join(lines) + "\n"


def check():
    bad = 0
    committed = open(os.path.join(HERE, "number_manifest.csv"), encoding="utf-8", newline="").read()
    if committed != build_manifest():
        print("  MISMATCH number_manifest.csv: rebuilt from out/ differs from the committed file")
        bad += 1
    results = open(os.path.join(HERE, "RESULTS.md"), encoding="utf-8").read()
    for row in csv.DictReader(io.StringIO(committed)):
        if row["value"] not in results:
            print(f"  NOT IN RESULTS.md: {row['number_id']} = {row['value']}")
            bad += 1
    listed = set()
    for line in open(os.path.join(HERE, "CHECKSUMS.md5"), encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        want, path = line.split("  ", 1)
        listed.add(path)
        got = md5(os.path.join(HERE, path))
        if got != want:
            print(f"  MISMATCH {path}: {got} != {want}")
            bad += 1
    missing = set(INPUTS + outputs()) - listed
    for p in sorted(missing):
        print(f"  NOT LISTED in CHECKSUMS.md5: {p}")
        bad += 1
    if bad:
        print(f"  {bad} problem(s)")
        return 1
    print(f"  {len(listed)} checksums verified; {len(NUMBERS)} manifest numbers rebuilt and found in RESULTS.md")
    return 0


def main():
    if "--check" in sys.argv[1:]:
        return check()
    with open(os.path.join(HERE, "number_manifest.csv"), "w", encoding="utf-8", newline="") as f:
        f.write(build_manifest())
    with open(os.path.join(HERE, "CHECKSUMS.md5"), "w", encoding="utf-8", newline="\n") as f:
        f.write(build_checksums())
    print("  wrote erp/number_manifest.csv and erp/CHECKSUMS.md5")
    return 0


if __name__ == "__main__":
    sys.exit(main())
