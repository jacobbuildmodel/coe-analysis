"""
14_manifest.py -- the ERP piece's checksums and number manifest.

  python3 erp/14_manifest.py          regenerate erp/number_manifest.csv and
                                      erp/CHECKSUMS.md5. Manual step, run LAST,
                                      after every other edit.
  python3 erp/14_manifest.py --check  verify both, never write: every md5 in
                                      CHECKSUMS.md5 matches; the manifest,
                                      rebuilt from out/, equals the committed
                                      file; every manifest value appears in
                                      RESULTS.md as printed; every number the
                                      article prints is in the manifest or on
                                      the short allowlist of sealed design
                                      constants; the article's method-strip
                                      front matter matches the scorecard.

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
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

INPUTS = ["00_coverage.py", "10_load.py", "11_tests.py", "12_figures.py", "13_results.py",
          "14_manifest.py", "15_reproduce.py", "run_all.sh", "requirements.txt",
          "THESIS.md", "THESIS_ADDENDUM.md", "2026-10-17.md",
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
    ("T1_exp_n", "T1_expressway_scored_years", "{:d}", "scored expressway years"),
    ("T1_art_n", "T1_arterial_scored_years", "{:d}", "scored arterial years"),
    ("T2_exp_rise", "T2_expressway_density_rise_pct", "{:.0f}", "per cent rise in cars per expressway lane-km, 2005-2017"),
    ("T2_art_rise", "T2_arterial_density_rise_pct", "{:.0f}", "per cent rise in cars per arterial lane-km, 2005-2017"),
    ("T3_pct_int", "T3_pct_lower", "{:.0f}", "per cent by which high-premium years were lower, whole number"),
    ("n_held", "n_held", "{:d}", "predictions held"),
    ("expected", "expected_held", "{:.1f}", "expected predictions held, sum of confidences"),
    ("brier", "brier", "{:.3f}", "Brier score, mean over the four scored tests"),
    ("S1_2005", "S1_car_km_billion_first", "{:.2f}", "total car-km 2005, billion"),
    ("S1_max", "S1_car_km_billion_max", "{:.2f}", "total car-km peak, billion"),
    ("S1_2018", "S1_car_km_billion_last", "{:.2f}", "total car-km 2018, billion"),
]


ARTICLE = "2026-10-17.md"
# Design constants fixed by the sealed thesis or by the shape of the argument.
# Everything else the article prints must come from the manifest.
ALLOW = {
    45, 65, 20, 30,        # LTA's target bands, km/h (THESIS section 4, E6)
    35, 70,                # Jacob's sealed confidences for T1 and T4 (65 and 20 are bands)
    3,                     # T3's sealed threshold, per cent
    0.25, 50,              # Brier score of an always-50-per-cent forecaster
    90,                    # sealed interval width, per cent (THESIS section 6)
}
ALLOW_INT_MAX = 10         # list numbers, "7 years", clock hours, bet numbers
YEAR_LO, YEAR_HI = 1900, 2030


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
    for nid, val, meaning, src in speeds_rows():
        w.writerow([nid, val, meaning, "11_tests.py", f"erp/{src}", "speed"])
    return buf.getvalue()


def speeds_rows():
    """The two scored arterial years above the band, from out/t1_years.csv."""
    rows = []
    with open(os.path.join(HERE, "out", "t1_years.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["road"] == "arterial" and r["position"] == "above" and r["scored"] == "True":
                rows.append((f"T1_art_{r['year']}", "{:g}".format(float(r["speed"])),
                             f"arterial peak speed {r['year']}, km/h", "out/t1_years.csv"))
    return rows


def article_numbers():
    text = open(os.path.join(HERE, ARTICLE), encoding="utf-8").read()
    front, body = text.split("---", 2)[1:]
    body = re.sub(r"\]\([^)]*\)", "]", body)                  # link targets
    body = re.sub(r"\bd_[0-9a-f]{32}\b", "", body)            # dataset ids
    body = re.sub(r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|"
                  r"September|October|November|December) \d{4}\b", "", body)  # dates
    body = re.sub(r"[A-Za-z_]+\d[\w-]*", "", body)            # tokens like MVP01-1
    return front, re.findall(r"(?<![\w.,])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?", body)


def check_article(manifest_values):
    bad = 0
    front, nums = article_numbers()
    for tok in nums:
        if tok in manifest_values:
            continue
        v = float(tok.replace(",", ""))
        if v in ALLOW or (v == int(v) and (v <= ALLOW_INT_MAX or YEAR_LO <= v <= YEAR_HI)):
            continue
        print(f"  ARTICLE number not in manifest or allowlist: {tok}")
        bad += 1
    with open(os.path.join(HERE, "out", "tests.csv"), newline="", encoding="utf-8") as f:
        T = {r["key"]: r["value"] for r in csv.DictReader(f)}
    outs = [T[f"T{i}_outcome"] for i in (1, 2, 3, 4)]
    want = {"testsPassed": outs.count("PASS"), "testsFailed": outs.count("FAIL"),
            "testsOther": 4 - outs.count("PASS") - outs.count("FAIL"), "testsTotal": 4}
    for k, v in want.items():
        m = re.search(rf"^{k}: (\d+)$", front, re.M)
        if not m or int(m.group(1)) != v:
            print(f"  FRONT MATTER {k} expected {v}")
            bad += 1
    if 'thesisSealed: "26 September 2026"' not in front:
        print("  FRONT MATTER thesisSealed is not the seal date")
        bad += 1
    print(f"  article: {len(nums)} numbers checked, front matter checked")
    return bad


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
    values = set()
    for row in csv.DictReader(io.StringIO(committed)):
        values.add(row["value"])
        if row["value"] not in results:
            print(f"  NOT IN RESULTS.md: {row['number_id']} = {row['value']}")
            bad += 1
    bad += check_article(values)
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
