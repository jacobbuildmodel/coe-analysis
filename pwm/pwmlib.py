"""
pwmlib.py -- what every analysis step (10-15) shares: where things are, the
seal guard, the windows THESIS fixes, and the output format. No computation
of any tested number lives here, so 15_reproduce.py stays a different path.

Every step takes --root DIR (default: pwm/). It reads DIR/raw and writes
DIR/out, DIR/figs, DIR/RESULTS.md, DIR/number_manifest.csv and
DIR/CHECKSUMS.md5. The synthetic fixtures (tests/fixtures/) are run the same
way, with --root pointing at a copy of them.

The guard: nothing reads pwm/raw/ unless the file pwm/SEALED exists. It is
checked by the two scripts that open raw files (10_load.py, 15_reproduce.py)
before they open anything.
"""
import argparse
import csv
import io
import os
import sys

PWM = os.path.dirname(os.path.abspath(__file__))
REAL_RAW = os.path.realpath(os.path.join(PWM, "raw"))
SEALED = os.path.join(PWM, "SEALED")
MAP = os.path.join(PWM, "office", "OCCUPATION_MAP.csv")
FLOAT = "%.8g"

# THESIS section 5: windows, fixed at the seal.
COVERED = ("cleaning", "security", "landscape")
PRE = {"cleaning": list(range(2009, 2013)),
       "security": list(range(2009, 2015)),
       "landscape": list(range(2009, 2015))}
TRANSITION = {"cleaning": [2013, 2014, 2015], "security": [2015, 2016], "landscape": [2015, 2016]}
POST = {"cleaning": [2016, 2017, 2018, 2019, 2022],
        "security": [2017, 2018, 2019, 2022],
        "landscape": [2017, 2018, 2019, 2022]}
EXCLUDED = (2020, 2021)
PRE_END = {g: PRE[g][-1] for g in COVERED}

# THESIS T5 table: entry rung (basic, S$) in force on 1 June, post-period Junes.
RUNG = {"cleaning": {2016: 1000, 2017: 1000, 2018: 1000, 2019: 1120, 2022: 1274},
        "security": {2017: 1100, 2018: 1100, 2019: 1175, 2022: 1442},
        "landscape": {2017: 1300, 2018: 1300, 2019: 1300, 2022: 1550}}

# THESIS section 4: T4 industry lines, labels exactly as published (W2a).
T4_LINES = {"security": ["SSIC 80 - Security And Investigation Activities"],
            "landscape": ["SSIC 813 - Landscape Planting, Care And Maintenance Service Activities"],
            "cleaning": ["SSIC 812 - Cleaning Activities"],
            "comparison": ["SSIC 47 - Total Retail Trade",
                           "SSIC 55-56 - Total Accommodation & Food Services"]}

# THESIS thresholds.
T1_LINE = 0.010
T2_SURVIVE, T2_FAIL = 0.10, 0.05
T3_LINE = 0.05
T4_PRETREND, T4_SURVIVE, T4_FAIL = 0.020, -0.05, -0.10
T5_LINE = 0.97
MIN_PRE = 4


def args(description, extra=None):
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--root", default=PWM, help="directory holding raw/ (default: pwm/)")
    if extra:
        extra(p)
    a = p.parse_args()
    a.root = os.path.abspath(a.root)
    return a


def paths(root):
    root = os.path.abspath(root)
    return {"root": root, "raw": os.path.join(root, "raw"), "out": os.path.join(root, "out"),
            "figs": os.path.join(root, "figs"), "results": os.path.join(root, "RESULTS.md"),
            "manifest": os.path.join(root, "number_manifest.csv"),
            "checksums": os.path.join(root, "CHECKSUMS.md5"),
            "lfs_lines": os.path.join(root, "T4_LFS_LINES.csv"),
            "thesis": (os.path.join(root, "THESIS.md") if os.path.exists(os.path.join(root, "THESIS.md"))
                       else os.path.join(PWM, "THESIS.md"))}


def guard(raw_dir):
    """Refuse to read the real pwm/raw/ before the seal. Returns the path."""
    if os.path.realpath(raw_dir) == REAL_RAW and not os.path.exists(SEALED):
        sys.stderr.write("REFUSED: pwm/raw/ holds the real data and pwm/SEALED does not "
                         "exist. The thesis is not sealed; run on the synthetic fixtures "
                         "with --root, or seal first.\n")
        raise SystemExit(3)
    return raw_dir


def fmt(v):
    """Numbers as %.8g; text as is; missing as empty."""
    if v is None:
        return ""
    if isinstance(v, bool) or type(v).__name__ == "bool_":
        return str(bool(v))
    if isinstance(v, (int,)):
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


# How RESULTS.md prints each scored number; 14_manifest.py checks the same.
def printed(key, value):
    """The printed form of tests.csv value `value` under key `key`, or None
    when the key is not a number RESULTS.md prints."""
    import re as _re
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if _re.search(r"_(pre_junes|pre_years)$|^n_(held|scored)$|^T3_n_(start|end)$", key):
        return "{:d}".format(int(v))
    if _re.search(r"_ratio$|^brier$", key):
        return "{:.3f}".format(v)
    if key == "expected_held":
        return "{:.2f}".format(v)
    if _re.search(r"^T[1-4]_.*_(slope|lo|hi|est|pretrend)$|^T2_pooled(_lo|_hi)?$|"
                  r"^T3_(start_c|end_c|growth_c|growth_mid|shortfall)$", key):
        return "{:.4f}".format(v)
    return None
