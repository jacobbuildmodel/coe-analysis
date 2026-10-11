"""
14_manifest.py -- the sgd piece's checksums and number manifest.

  python3 sgd/14_manifest.py [--root DIR]          regenerate ROOT/number_manifest.csv
                                                   and ROOT/CHECKSUMS.md5. Manual step,
                                                   run LAST.
  python3 sgd/14_manifest.py [--root DIR] --check  verify, never write: every md5
                                                   matches; the manifest, rebuilt from
                                                   out/, equals the file; every
                                                   manifest value appears in RESULTS.md
                                                   as printed.
  python3 sgd/14_manifest.py --seal                write sgd/SEAL_MANIFEST.md: the md5 of
                                                   THESIS.md, the coding sheet and its
                                                   candidates file, RETRIEVED.txt,
                                                   every script, requirements.txt,
                                                   run_all.sh and tests/.

CHECKSUMS.md5 has two sections, paths relative to ROOT. INPUTS: the scripts,
THESIS.md, office/MPS_CODING.csv, THESIS_ADDENDUM.md and the article when
present, FOR_RESEARCHERS.md when present, and every raw file the loader
reads. --check also checks every number in the article (THESIS_ADDENDUM
item 5) and in FOR_RESEARCHERS.md (item 8).
OUTPUTS: out/, figs/, RESULTS.md, number_manifest.csv.
"""
import csv
import glob
import hashlib
import io
import os
import re
import sys

import sgdlib as L

SCRIPTS = ["sgdlib.py", "00_coverage.py", "03_mps_candidates.py", "04_mps_coding.py", "10_load.py",
           "11_tests.py", "11b_postresults.py", "12_figures.py", "13_results.py", "14_manifest.py", "15_reproduce.py",
           "run_all.sh", "requirements.txt", "tests/make_fixtures.py", "tests/test_pipeline.py",
           "16_review.py"]
# Raw files read only by 16_review.py (THESIS_ADDENDUM item 10, not sealed).
REVIEW_RAW = ("s1c_bis_eer_weights_broad.xlsx", "s8_bis_long_cpi_jp_monthly.csv",
              "s9_boj_mps_20240319.html")


ARTICLE = "2026-11-14.md"
RESEARCHERS = "FOR_RESEARCHERS.md"
SEAL_DATE = "3 October 2026"
# Constants the article may print that are sealed design or plain facts, not
# results: THESIS lines (0.90, 120, 0.20, 20 and 50 per cent), the BIS basket of 64
# economies, MAS's 62 statements, the Hong Kong band (7.75, 7.85), the eleven
# currencies, index bases and per-100 quotes (100), the S$1,000 trip budget,
# and the Brier score of an always-50-per-cent forecaster (0.25). Added for
# FOR_RESEARCHERS.md (THESIS_ADDENDUM item 8), all sealed in THESIS: the T1
# and T2 lines (0.005, 0.50), months in a year for y_i (12), T7's reasoning
# for its line (59 degrees of freedom, a standard error of 0.13), and the
# bootstrap's draws and seed (10,000; 20260929).
ALLOW = {0.90, 90, 120, 0.20, 20, 50, 64, 62, 61, 7.75, 7.85, 11, 100, 1000, 0.25,
         0.005, 0.50, 12, 59, 0.13, 10000, 20260929}
ALLOW_INT_MAX = 10
YEAR_LO, YEAR_HI = 1900, 2030


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def inputs(P):
    paths = [os.path.join(L.SGD, s) for s in SCRIPTS] + [P["thesis"], P["coding"]]
    for extra in (os.path.join(P["root"], "THESIS_ADDENDUM.md"), os.path.join(P["root"], ARTICLE),
                  os.path.join(P["root"], RESEARCHERS)):
        if os.path.exists(extra):
            paths.append(extra)
    paths += [os.path.join(P["raw"], f) for f in L.RAW_FILES + REVIEW_RAW if os.path.exists(os.path.join(P["raw"], f))]
    ret = os.path.join(P["raw"], "RETRIEVED.txt")
    if os.path.exists(ret):
        paths.append(ret)
    return paths


def outputs(P):
    files = sorted(glob.glob(os.path.join(P["out"], "*.csv")) + glob.glob(os.path.join(P["figs"], "*.svg")))
    return files + [P["results"], P["manifest"]]


def rel(P, path):
    return os.path.relpath(path, P["root"]).replace(os.sep, "/")


def build_manifest(P):
    T = L.read_csv(os.path.join(P["out"], "tests.csv"))
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["number_id", "value", "script", "output_file", "key"])
    for r in T:
        v = L.printed(r["key"], r["value"])
        if v is not None:
            w.writerow([r["key"], v, "11_tests.py", "out/tests.csv", r["key"]])
    post = os.path.join(P["out"], "postresults.csv")
    if os.path.exists(post):
        for r in L.read_csv(post):
            w.writerow([r["key"], r["printed"], "11b_postresults.py", "out/postresults.csv", r["key"]])
    # Added after outside review, not sealed (THESIS_ADDENDUM item 10).
    for f in sorted(glob.glob(os.path.join(P["out"], "review_*.csv"))):
        if f.endswith("review_rolling_windows.csv"):
            continue
        for r in L.read_csv(f):
            w.writerow([r["key"], r["printed"], "16_review.py", "out/" + os.path.basename(f), r["key"]])
    # The sealed sensitivities, as RESULTS.md prints them: counts and ranks
    # whole, everything else to four decimals (THESIS_ADDENDUM item 8).
    for r in L.read_csv(os.path.join(P["out"], "sensitivities.csv")):
        try:
            v = float(r["value"])
        except (TypeError, ValueError):
            continue
        whole = re.search(r"intervals|_count$|_rank|^present", r["key"])
        slug = re.sub(r"[^a-z0-9]+", "_", f'{r["test"]} {r["variant"]} {r["key"]}'.lower()).strip("_")
        w.writerow([f"sens_{slug}", "{:d}".format(int(v)) if whole else "{:.4f}".format(v),
                    "11_tests.py", "out/sensitivities.csv", r["key"]])
    return buf.getvalue()


def article_numbers(path):
    """Front matter, and every number token in the body, with link targets,
    URLs, written dates, year spans, labels, script names, commit and md5
    hashes, and a closing "References" section (bibliographic volumes and
    pages, not results) removed. A file without front matter has an empty one."""
    text = open(path, encoding="utf-8").read()
    front, body = text.split("---", 2)[1:] if text.startswith("---") else ("", text)
    body = re.split(r"^## (?:\d+\. )?References\s*$", body, flags=re.M)[0]
    body = re.sub(r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b", "", body)
    body = re.sub(r"\b\d+[a-z]?_[\w.-]+", "", body)          # script names, 14_manifest.py
    body = re.sub(r"\]\([^)]*\)", "]", body)
    body = re.sub(r"https?://\S+", "", body)
    body = re.sub(r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|"
                  r"September|October|November|December) \d{4}\b", "", body)
    body = re.sub(r"\b(?:19|20)\d\d-(?:\d\d)\b", "", body)
    body = re.sub(r"[A-Za-z_]+\d[\w-]*", "", body)
    return front, re.findall(r"(?<![\w.,])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?", body)


def check_article(P, values, name=ARTICLE):
    """Every number in the article (or FOR_RESEARCHERS.md) is a manifest
    value as printed, or a listed constant, a small integer or a year; the
    article's front matter counts match the scorecard."""
    path = os.path.join(P["root"], name)
    if not os.path.exists(path):
        return 0
    bad = 0
    front, nums = article_numbers(path)
    for tok in nums:
        if tok in values or "-" + tok in values:
            continue
        v = float(tok.replace(",", ""))
        if v in ALLOW or (v == int(v) and (v <= ALLOW_INT_MAX or YEAR_LO <= v <= YEAR_HI)):
            continue
        print(f"  {name}: number not in manifest or allowlist: {tok}")
        bad += 1
    if name != ARTICLE:
        print(f"  {name}: {len(nums)} numbers checked")
        return bad
    T = {r["key"]: r["value"] for r in L.read_csv(os.path.join(P["out"], "tests.csv"))}
    outs = [T[f"{t}_outcome"] for t in L.SCORED if T[f"{t}_outcome"] != "NOT SCORED"]
    want = {"testsPassed": outs.count("SURVIVE"), "testsFailed": outs.count("FAIL"),
            "testsOther": len(outs) - outs.count("SURVIVE") - outs.count("FAIL"), "testsTotal": len(outs)}
    for k, v in want.items():
        m = re.search(rf"^{k}: (\d+)$", front, re.M)
        if not m or int(m.group(1)) != v:
            print(f"  FRONT MATTER {k} expected {v}")
            bad += 1
    if f'thesisSealed: "{SEAL_DATE}"' not in front:
        print("  FRONT MATTER thesisSealed is not the seal date")
        bad += 1
    print(f"  article: {len(nums)} numbers checked, front matter checked")
    return bad


def build_checksums(P):
    lines = ["# MD5 checksums, sgd piece. Regenerate with:", "#   python3 sgd/14_manifest.py [--root DIR]",
             "# Never written by run_all.sh, which only runs --check.", "# Paths are relative to the run's root.",
             "", "# INPUTS"]
    lines += [f"{md5(p)}  {rel(P, p)}" for p in inputs(P)]
    lines += ["", "# OUTPUTS"]
    lines += [f"{md5(p)}  {rel(P, p)}" for p in outputs(P)]
    return "\n".join(lines) + "\n"


def check(P):
    bad = 0
    committed = open(P["manifest"], encoding="utf-8", newline="").read()
    if committed != build_manifest(P):
        print("  MISMATCH number_manifest.csv: rebuilt from out/ differs")
        bad += 1
    results = open(P["results"], encoding="utf-8").read()
    rows = list(csv.DictReader(io.StringIO(committed)))
    for r in rows:
        if r["value"] not in results:
            print(f"  NOT IN RESULTS.md: {r['number_id']} = {r['value']}")
            bad += 1
    bad += check_article(P, {r["value"] for r in rows})
    bad += check_article(P, {r["value"] for r in rows}, RESEARCHERS)
    listed = {}
    for line in open(P["checksums"], encoding="utf-8"):
        line = line.rstrip("\n")
        if line and not line.startswith("#"):
            h, p = line.split("  ", 1)
            listed[p] = h
    for p, h in listed.items():
        full = os.path.normpath(os.path.join(P["root"], p))
        if not os.path.exists(full):
            print(f"  MISSING {p}")
            bad += 1
        elif md5(full) != h:
            print(f"  MISMATCH {p}")
            bad += 1
    for p in sorted({rel(P, x) for x in inputs(P) + outputs(P)} - set(listed)):
        print(f"  NOT LISTED {p}")
        bad += 1
    print(f"  {len(listed)} checksums, {len(rows)} manifest numbers checked")
    return bad


def seal_files():
    rels = ["THESIS.md", "office/MPS_CODING.csv", "office/MPS_CANDIDATES.txt", "raw/RETRIEVED.txt"]
    rels += sorted(os.path.basename(p) for p in glob.glob(os.path.join(L.SGD, "*.py")))
    rels += ["requirements.txt", "run_all.sh"]
    for d, dirs, files in sorted(os.walk(os.path.join(L.SGD, "tests"))):
        dirs[:] = sorted(x for x in dirs if x != "__pycache__")
        rels += sorted(os.path.relpath(os.path.join(d, f), L.SGD).replace(os.sep, "/")
                       for f in files if not f.endswith(".pyc"))
    return rels


def seal():
    rels = seal_files()
    lines = ["# SEAL MANIFEST: sgd piece", "",
             "The md5 of every file the seal fixes, taken in the commit \"sgd: SEAL\",",
             "which adds this file and nothing else. Paths are relative to `sgd/`.",
             "Regenerate with `python3 sgd/14_manifest.py --seal` and compare.", "", "```"]
    lines += [f"{md5(os.path.join(L.SGD, r))}  {r}" for r in rels]
    lines += ["```", ""]
    L.write_text(os.path.join(L.SGD, "SEAL_MANIFEST.md"), "\n".join(lines))
    print(f"  sgd/SEAL_MANIFEST.md: {len(rels)} files")


def main():
    a = L.args("sgd step 14: checksums and number manifest",
               lambda p: (p.add_argument("--check", action="store_true"),
                          p.add_argument("--seal", action="store_true")))
    if a.seal:
        seal()
        return
    P = L.paths(a.root)
    if a.check:
        bad = check(P)
        if bad:
            print(f"  {bad} problem(s)")
            sys.exit(1)
        print("  all checksums and manifest numbers verified")
        return
    L.write_text(P["manifest"], build_manifest(P))
    L.write_text(P["checksums"], build_checksums(P))
    print(f"  wrote {rel(P, P['manifest'])} and {rel(P, P['checksums'])}")


if __name__ == "__main__":
    main()
