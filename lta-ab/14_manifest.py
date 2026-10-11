"""
14_manifest.py -- number manifest and checksums for the lta-ab note.

  python3 lta-ab/14_manifest.py          rewrite number_manifest.csv and CHECKSUMS.md5
  python3 lta-ab/14_manifest.py --check  verify both, then check NOTE.md:
        - every number token in NOTE.md is a printed value in the manifest,
          an integer of 10 or less, or a year (1990-2030);
        - pure ASCII; no banned word; the word count of the note body
          (before "## Method and sources") is at most WORD_CAP.

The manifest holds every printed value from out/facts.csv, the results in
out/checks.csv, and LTA's amounts in office/LTA_CONSTANTS.csv (quoted from the
consultation paper, with paragraphs). Before numbers are checked, NOTE.md loses
URLs, link targets, dataset ids, script names, and paragraph, footnote and
table references to LTA's paper (references, not results).
"""
import csv
import glob
import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTE = os.path.join(HERE, "NOTE.md")
MANIFEST = os.path.join(HERE, "number_manifest.csv")
CHECKSUMS = os.path.join(HERE, "CHECKSUMS.md5")
WORD_CAP = 800
YEAR_LO, YEAR_HI = 1990, 2030
BANNED_WORDS = ["we", "should", "recommend", "choose", "must"]
BANNED_PHRASES = ["better option", "you should", "lta should"]


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def tracked():
    files = sorted(glob.glob(os.path.join(HERE, "raw", "*")))
    files += [os.path.join(HERE, "office", "LTA_CONSTANTS.csv")]
    files += sorted(glob.glob(os.path.join(HERE, "*.py"))) + [os.path.join(HERE, "run_all.sh")]
    files += sorted(glob.glob(os.path.join(HERE, "out", "*.csv")))
    files += sorted(glob.glob(os.path.join(HERE, "figs", "*.svg")))
    files += [NOTE]
    return [f for f in files if os.path.isfile(f)]


def build_manifest():
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["key", "printed", "script", "file"])
    for r in csv.DictReader(open(os.path.join(HERE, "out", "facts.csv"), encoding="utf-8")):
        w.writerow([r["key"], r["printed"], "10_facts.py", "out/facts.csv"])
    for i, r in enumerate(csv.DictReader(open(os.path.join(HERE, "out", "checks.csv"), encoding="utf-8"))):
        w.writerow([f"check_{i + 1}", "{:,}".format(int(r["result"])), "10_facts.py", "out/checks.csv"])
    for r in csv.DictReader(open(os.path.join(HERE, "office", "LTA_CONSTANTS.csv"), encoding="utf-8")):
        w.writerow([f"lta_{r['key']}", r["printed"], "LTA consultation paper", "office/LTA_CONSTANTS.csv"])
    return buf.getvalue()


def build_checksums():
    return "".join(f"{md5(f)}  {os.path.relpath(f, HERE)}\n" for f in tracked()
                   if os.path.basename(f) != "CHECKSUMS.md5")


def note_numbers(text):
    t = re.sub(r"https?://\S+", "", text)
    t = re.sub(r"\]\([^)]*\)", "]", t)
    t = re.sub(r"\bd_[0-9a-f]{32}\b", "", t)
    t = re.sub(r"\b\d+[a-z]?_[\w.-]+", "", t)
    t = re.sub(r"\b(?:paras?|footnotes?|Tables?)\s+[\d.]+(?:\([a-z]\))?(?:\s*(?:-|to|and|,)\s*[\d.]+(?:\([a-z]\))?)*", "", t)
    t = re.sub(r"\(\s*[a-z]\s*\)", "", t)
    return re.findall(r"(?<![\w.,-])-?\d+(?:,\d{3})*(?:\.\d+)?(?![\w]|,\d)", t)


def body_words(text):
    body = text.split("## Method and sources")[0]
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body)
    return len(re.findall(r"\S+", body))


def check():
    ok = True
    want = {}
    for line in open(CHECKSUMS, encoding="utf-8"):
        h, f = line.rstrip("\n").split("  ", 1)
        want[f] = h
    have = {os.path.relpath(f, HERE): md5(f) for f in tracked() if os.path.basename(f) != "CHECKSUMS.md5"}
    for f in sorted(set(want) | set(have)):
        if want.get(f) != have.get(f):
            print(f"  CHECKSUM MISMATCH: {f}")
            ok = False
    if open(MANIFEST, encoding="utf-8").read() != build_manifest():
        print("  number_manifest.csv is stale")
        ok = False
    printed = {r["printed"].lstrip("-") for r in csv.DictReader(open(MANIFEST, encoding="utf-8"))}
    text = open(NOTE, encoding="utf-8").read()
    nums = note_numbers(text)
    for n in nums:
        v = n.lstrip("-")
        if v in printed:
            continue
        if re.fullmatch(r"\d+", v) and (int(v) <= 10 or YEAR_LO <= int(v) <= YEAR_HI):
            continue
        print(f"  NUMBER NOT IN MANIFEST: {n}")
        ok = False
    bad = [c for c in text if ord(c) > 127]
    if bad:
        print(f"  NON-ASCII characters: {sorted(set(bad))}")
        ok = False
    low = text.lower()
    for wd in BANNED_WORDS:
        if re.search(rf"\b{wd}\b", low):
            print(f"  BANNED WORD: {wd}")
            ok = False
    for ph in BANNED_PHRASES:
        if ph in low:
            print(f"  BANNED PHRASE: {ph}")
            ok = False
    words = body_words(text)
    if words > WORD_CAP:
        print(f"  WORD COUNT {words} over {WORD_CAP}")
        ok = False
    print(f"  NOTE.md: {len(nums)} numbers checked, {words} words before Method and sources")
    print(f"  {len(have)} checksums, {len(printed)} distinct printed values in the manifest")
    return ok


def main():
    if "--check" in sys.argv:
        if not check():
            print("FAILED")
            return 1
        print("  all checksums and note numbers verified")
        return 0
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as f:
        f.write(build_manifest())
    with open(CHECKSUMS, "w", encoding="utf-8", newline="\n") as f:
        f.write(build_checksums())
    print("  wrote number_manifest.csv and CHECKSUMS.md5")
    return 0


if __name__ == "__main__":
    sys.exit(main())
