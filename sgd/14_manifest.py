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
THESIS.md, office/MPS_CODING.csv and every raw file the loader reads.
OUTPUTS: out/, figs/, RESULTS.md, number_manifest.csv.
"""
import csv
import glob
import hashlib
import io
import os
import sys

import sgdlib as L

SCRIPTS = ["sgdlib.py", "00_coverage.py", "03_mps_candidates.py", "04_mps_coding.py", "10_load.py",
           "11_tests.py", "12_figures.py", "13_results.py", "14_manifest.py", "15_reproduce.py",
           "run_all.sh", "requirements.txt", "tests/make_fixtures.py", "tests/test_pipeline.py"]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def inputs(P):
    paths = [os.path.join(L.SGD, s) for s in SCRIPTS] + [P["thesis"], P["coding"]]
    paths += [os.path.join(P["raw"], f) for f in L.RAW_FILES if os.path.exists(os.path.join(P["raw"], f))]
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
    return buf.getvalue()


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
