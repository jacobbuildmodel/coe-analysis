"""
14_manifest.py -- number manifest and checksums for the lta-ab note.

  python3 lta-ab/14_manifest.py          rewrite number_manifest.csv and CHECKSUMS.md5
  python3 lta-ab/14_manifest.py --check  verify both, then check NOTE.md:
        - every number token in NOTE.md is a printed value in the manifest,
          an integer of 10 or less, or a year (1990-2030);
        - pure ASCII; no banned word; the word count of the note body
          of prose (sections 1-4 and Scope: paragraphs only, without the
          Summary box, table, captions, Notes lines and figure block) is at
          most WORD_CAP. The count of everything before "## Data and method"
          is reported alongside it, not capped: the redesign text was fixed
          by the checker's ruling of 12 Oct 2026 at more than 800 words in all.

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
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
NOTE = os.path.join(HERE, "NOTE.md")
FORM = os.path.join(HERE, "FORM_TEXT.md")
ONEPAGER = os.path.join(HERE, "ONEPAGER.md")
REPLY = os.path.join(HERE, "SUBMITTED_REPLY.md")
ONEPAGER_CAP = 800
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
    files += sorted(glob.glob(os.path.join(HERE, "figs", "*.png")))
    files += sorted(glob.glob(os.path.join(HERE, "fonts", "*")))
    files += [NOTE, FORM, ONEPAGER, REPLY]
    return [f for f in files if os.path.isfile(f)]


def build_manifest():
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["key", "printed", "script", "file", "row"])
    for i, r in enumerate(csv.DictReader(open(os.path.join(HERE, "out", "facts.csv"), encoding="utf-8"))):
        w.writerow([r["key"], r["printed"], "10_facts.py", "out/facts.csv", i + 1])
    for i, r in enumerate(csv.DictReader(open(os.path.join(HERE, "out", "checks.csv"), encoding="utf-8"))):
        w.writerow([f"check_{i + 1}", "{:,}".format(int(r["result"])), "10_facts.py", "out/checks.csv", i + 1])
    for i, r in enumerate(csv.DictReader(open(os.path.join(HERE, "office", "LTA_CONSTANTS.csv"), encoding="utf-8"))):
        w.writerow([f"lta_{r['key']}", r["printed"], "LTA consultation paper", "office/LTA_CONSTANTS.csv", i + 1])
    for i, r in enumerate(csv.DictReader(open(os.path.join(HERE, "out", "bands_summary.csv"), encoding="utf-8"))):
        w.writerow([f"bands_{r['key']}", r["printed"], "16_bands.py", "out/bands_summary.csv", i + 1])
    return buf.getvalue()


def build_checksums():
    return "".join(f"{md5(f)}  {Path(os.path.relpath(f, HERE)).as_posix()}\n" for f in tracked()
                   if os.path.basename(f) != "CHECKSUMS.md5")


def note_numbers(text):
    t = re.sub(r"https?://\S+", "", text)
    t = re.sub(r"\]\([^)]*\)", "]", t)
    t = re.sub(r"\bd_[0-9a-f]{32}\b", "", t)
    t = re.sub(r"\b\d+[a-z]?_[\w.-]+", "", t)
    t = re.sub(r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b", "", t)
    t = re.sub(r"\b\d{2}:\d{2}\b", "", t)  # clock times (23:59)
    t = re.sub(r"\(ORCID \d{4}-\d{4}-\d{4}-\d{3}[\dX]\)", "", t)
    t = re.sub(r"\b(?:[Pp]aragraphs?|paras?|footnotes?|Tables?|Figures?)\s+[\d.]+(?:\([a-z]\))?(?:\s*(?:-|to|and|,)\s*[\d.]+(?:\([a-z]\))?)*", "", t)
    t = re.sub(r"\(\s*[a-z]\s*\)", "", t)
    return re.findall(r"(?<![\w.,-])-?\d+(?:,\d{3})*(?:\.\d+)?(?![\w]|,\d)", t)


def body_words(text):
    """(all words before "## Data and method", prose words of sections 1-4 and Scope)."""
    body = text.split("## Data and method")[0]
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body)
    total = len(re.findall(r"\S+", re.sub(r"^:::.*$", "", body, flags=re.M)))
    prose = "## 1." + body.split("## 1.", 1)[1]
    prose = re.sub(r"^::: figure$.*?^:::$", "", prose, flags=re.S | re.M)
    prose = re.sub(r"^:::.*$", "", prose, flags=re.M)
    keep = []
    for para in re.split(r"\n\s*\n", prose):
        p = para.strip()
        if not p or p.startswith(("#", "|", "Table ", "Notes:", "![")):
            continue
        keep.append(p)
    return total, len(re.findall(r"\S+", " ".join(keep)))


def check():
    ok = True
    want = {}
    for line in open(CHECKSUMS, encoding="utf-8"):
        h, f = line.rstrip("\n").split("  ", 1)
        want[f] = h
    have = {Path(os.path.relpath(f, HERE)).as_posix(): md5(f) for f in tracked() if os.path.basename(f) != "CHECKSUMS.md5"}
    for f in sorted(set(want) | set(have)):
        if want.get(f) != have.get(f):
            print(f"  CHECKSUM MISMATCH: {f}")
            ok = False
    if open(MANIFEST, encoding="utf-8").read() != build_manifest():
        print("  number_manifest.csv is stale")
        ok = False
    printed = {r["printed"].lstrip("-") for r in csv.DictReader(open(MANIFEST, encoding="utf-8"))}
    text = open(NOTE, encoding="utf-8").read()
    form = open(FORM, encoding="utf-8").read() if os.path.isfile(FORM) else ""
    nums = note_numbers(text) + note_numbers(form)
    for n in nums:
        v = n.lstrip("-")
        if v in printed:
            continue
        if re.fullmatch(r"\d+", v) and (int(v) <= 10 or YEAR_LO <= int(v) <= YEAR_HI):
            continue
        print(f"  NUMBER NOT IN MANIFEST: {n}")
        ok = False
    bad = [c for c in text + form if ord(c) > 127]
    if bad:
        print(f"  NON-ASCII characters: {sorted(set(bad))}")
        ok = False
    low = (text + form).lower()
    for wd in BANNED_WORDS:
        if re.search(rf"\b{wd}\b", low):
            print(f"  BANNED WORD: {wd}")
            ok = False
    for ph in BANNED_PHRASES:
        if ph in low:
            print(f"  BANNED PHRASE: {ph}")
            ok = False
    total, words = body_words(text)
    if words > WORD_CAP:
        print(f"  WORD COUNT {words} (prose) over {WORD_CAP}")
        ok = False
    ok = check_onepager(printed) and ok
    print(f"  NOTE.md and FORM_TEXT.md: {len(nums)} numbers checked, {words} words of prose (cap {WORD_CAP}), {total} words in all before Data and method")
    print(f"  {len(have)} checksums, {len(printed)} distinct printed values in the manifest")
    return ok


def check_onepager(printed):
    """ONEPAGER.md: numbers, ASCII, banned words, word cap, quotes, model rows."""
    ok = True
    page = open(ONEPAGER, encoding="utf-8").read()
    nums = note_numbers(page)
    for n in nums:
        v = n.lstrip("-")
        if v in printed or (re.fullmatch(r"\d+", v) and (int(v) <= 10 or YEAR_LO <= int(v) <= YEAR_HI)):
            continue
        print(f"  ONEPAGER NUMBER NOT IN MANIFEST: {n}")
        ok = False
    bad = sorted({c for c in page if ord(c) > 127})
    if bad:
        print(f"  ONEPAGER NON-ASCII characters: {bad}")
        ok = False
    low = page.lower()
    for wd in BANNED_WORDS:
        if re.search(rf"\b{wd}\b", low):
            print(f"  ONEPAGER BANNED WORD: {wd}")
            ok = False
    for ph in BANNED_PHRASES:
        if ph in low:
            print(f"  ONEPAGER BANNED PHRASE: {ph}")
            ok = False
    # words: tokens with a letter or digit (table pipes and rules are not words)
    words = sum(1 for t in re.findall(r"\S+", re.sub(r"https?://\S+", "URL", page)) if re.search(r"[A-Za-z0-9]", t))
    if words >= ONEPAGER_CAP:
        print(f"  ONEPAGER WORD COUNT {words}, cap under {ONEPAGER_CAP}")
        ok = False
    # Quotes in "What I sent" must appear verbatim in SUBMITTED_REPLY.md.
    reply = open(REPLY, encoding="utf-8").read()
    sent = page.split("## What I sent", 1)[1].split("\n## ", 1)[0]
    quotes = re.findall(r'"([^"]+)"', sent)
    for q in quotes:
        if q not in reply:
            print(f"  ONEPAGER QUOTE NOT IN SUBMITTED_REPLY.md: {q}")
            ok = False
    # Each table row naming a model must match out/bands.csv.
    bands = {r["model"]: r for r in csv.DictReader(open(os.path.join(HERE, "out", "bands.csv"), encoding="utf-8"))}

    def amt(v):
        v = int(v)
        return "$0" if v == 0 else ("-" if v < 0 else "+") + "${:,}".format(abs(v))
    rows = 0
    for line in page.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
        if cells and cells[0] in bands:
            r = bands[cells[0]]
            want = [f"Band {r['option_A_band']}, {amt(r['option_A_amount'])}",
                    f"Band {r['option_B_band']}, {amt(r['option_B_amount'])}"]
            rows += 1
            if cells[1:3] != want:
                print(f"  ONEPAGER ROW DIFFERS FROM out/bands.csv: {cells} vs {want}")
                ok = False
    print(f"  ONEPAGER.md: {len(nums)} numbers checked, {words} words (cap under {ONEPAGER_CAP}), "
          f"{len(quotes)} quotes found in SUBMITTED_REPLY.md, {rows} model rows match out/bands.csv")
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
