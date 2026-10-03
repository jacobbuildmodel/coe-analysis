"""
sgdlib.py -- what every analysis step (10-15) shares: where things are, the
seal guard, the windows and thresholds THESIS fixes, and the output format.
No tested number is computed here, so 15_reproduce.py stays a separate path.

Every step takes --root DIR (default: sgd/). It reads DIR/raw and
DIR/office/MPS_CODING.csv, and writes DIR/out, DIR/figs, DIR/RESULTS.md,
DIR/number_manifest.csv and DIR/CHECKSUMS.md5. The synthetic fixtures
(tests/fixtures/) run the same way, with --root pointing at a copy of them.

The guard: nothing reads sgd/raw/ unless sgd/SEALED exists. The two scripts
that open raw files (10_load.py, 15_reproduce.py) check it before opening
anything.
"""
import argparse
import csv
import io
import os
import re
import sys

SGD = os.path.dirname(os.path.abspath(__file__))
REAL_RAW = os.path.realpath(os.path.join(SGD, "raw"))
SEALED = os.path.join(SGD, "SEALED")
FLOAT = "%.8g"

# Raw files the analysis reads (raw/RETRIEVED.txt).
F_NEER = "s1_bis_eer_neer_broad_monthly.csv"
F_REER = "s1b_bis_eer_reer_broad_monthly.csv"
F_USD = "s2_bis_xru_usd_monthly_avg.csv"
F_USD_EOP = "s2e_bis_xru_usd_monthly_eop.csv"
F_MASFX = "s3a_mas_fx_monthly_avg_M700051.json"
F_SNEER = "s4_mas_sneer_weekly.json"
F_GDP = "s6a_singstat_gdp_yoy_quarterly_M015631.json"
F_CPI = "s7a_singstat_cpi_monthly_M213751.json"
RAW_FILES = (F_NEER, F_REER, F_USD, F_USD_EOP, F_MASFX, F_SNEER, F_GDP, F_CPI)
CODING = os.path.join("office", "MPS_CODING.csv")

# THESIS section 4: the eleven areas and the ten partners.
AREAS = ("SG", "JP", "MY", "KR", "CN", "TH", "ID", "US", "XM", "AU", "HK")
PARTNERS = (("JPY", "JP"), ("MYR", "MY"), ("KRW", "KR"), ("CNY", "CN"), ("THB", "TH"),
            ("IDR", "ID"), ("USD", "US"), ("EUR", "XM"), ("AUD", "AU"), ("HKD", "HK"))
CUR_AREA = dict(PARTNERS)
QUESTION = ("JPY", "MYR")
MAS_ROWS = {"JPY": ("Japanese Yen", 100.0), "MYR": ("Malaysian Ringgit", 1.0)}
GDP_ROW = "GDP In Chained (2015) Dollars"
CPI_ROW = "All Items"

# THESIS section 5: windows. Endpoints are three-month means of the log.
SCORED_START = ("2021-01", "2021-02", "2021-03")
SCORED_END = ("2025-10", "2025-11", "2025-12")
LONG_FIRST = "2005-08"          # long window: 2005-08 to the last full month in S1
LONG_START = ("2005-08", "2005-09", "2005-10")
T7_FROM_2010 = "20100101"

# THESIS section 6: thresholds.
T1_R, T1_MAD = 0.20, 0.005
T2_P = 0.50
T4_SURVIVE_RANK, T4_MIN_PRESENT = 2, 9
T7_D = 0.20
GATE_R, GATE_MIN, GATE_MIN_READINGS = 0.90, 120, 3
BOOT_N, BOOT_SEED = 10000, 20260929
SCORED = ("T1", "T2", "T3", "T4", "T7")


def args(description, extra=None):
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--root", default=SGD, help="directory holding raw/ (default: sgd/)")
    if extra:
        extra(p)
    a = p.parse_args()
    a.root = os.path.abspath(a.root)
    return a


def paths(root):
    root = os.path.abspath(root)
    thesis = os.path.join(root, "THESIS.md")
    return {"root": root, "raw": os.path.join(root, "raw"), "out": os.path.join(root, "out"),
            "figs": os.path.join(root, "figs"), "results": os.path.join(root, "RESULTS.md"),
            "manifest": os.path.join(root, "number_manifest.csv"),
            "checksums": os.path.join(root, "CHECKSUMS.md5"),
            "coding": os.path.join(root, CODING),
            "thesis": thesis if os.path.exists(thesis) else os.path.join(SGD, "THESIS.md")}


def guard(raw_dir):
    """Refuse to read the real sgd/raw/ before the seal. Returns the path."""
    if os.path.realpath(raw_dir) == REAL_RAW and not os.path.exists(SEALED):
        sys.stderr.write("REFUSED: sgd/raw/ holds the real data and sgd/SEALED does not "
                         "exist. The thesis is not sealed; run on the synthetic fixtures "
                         "with --root, or seal first.\n")
        raise SystemExit(3)
    return raw_dir


def month_add(period, k):
    """'YYYY-MM' plus k months."""
    y, m = int(period[:4]), int(period[5:7])
    n = y * 12 + (m - 1) + k
    return "%04d-%02d" % (n // 12, n % 12 + 1)


def month_diff(a, b):
    """Months from a to b ('YYYY-MM')."""
    return (int(b[:4]) * 12 + int(b[5:7])) - (int(a[:4]) * 12 + int(a[5:7]))


def months(first, last):
    out, p = [], first
    while p <= last:
        out.append(p)
        p = month_add(p, 1)
    return out


def fmt(v):
    """Numbers as %.8g; text as is; missing as empty."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, int):
        return str(v)
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    if f != f:
        return ""
    return FLOAT % f


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    for r in rows:
        w.writerow([fmt(x) for x in r])
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(buf.getvalue())


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def confidences(thesis_path):
    """{test: probability or None} from each test's 'Confidence at seal:' line.
    '[JACOB]' (not yet set) gives None."""
    text = open(thesis_path, encoding="utf-8").read()
    out = {}
    for t in SCORED:
        sec = re.search(rf"^### {t}\..*?(?=^### |^## |\Z)", text, re.S | re.M)
        m = re.search(r"\*\*Confidence at seal: (\d+(?:\.\d+)?)%", sec.group(0)) if sec else None
        out[t] = float(m.group(1)) / 100 if m else None
    return out


# How RESULTS.md prints each scored number; 14_manifest.py checks the same.
def printed(key, value):
    """The printed form of tests.csv value `value` under key `key`, or None
    when the key is not a number RESULTS.md prints."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if re.search(r"_(count|rank|present|steadier_than|changes|intervals)$|^n_", key):
        return "{:d}".format(int(v))
    if re.search(r"^(brier|expected_held)$", key):
        return "{:.3f}".format(v)
    if re.search(r"_(S|P|R|b|s|nx|e|mad|sd|r|rho_p|rho_g|D|D_lo|D_hi)$", key):
        return "{:.4f}".format(v)
    return None
