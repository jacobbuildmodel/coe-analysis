"""
03_mps_candidates.py -- the decision paragraphs of MAS's monetary policy
statements, found mechanically by the MPS coding rule (THESIS section 5),
before any statement is read.

  python3 sgd/03_mps_candidates.py --counts   counts only, no text
  python3 sgd/03_mps_candidates.py            write office/MPS_CANDIDATES.txt

For each raw/s5b_mas_mps_<YYYYMMDD>.html, the paragraphs (<p> and <li>) inside
MAS's statement text blocks (<div> with class "mas-rte-content", found by
counting <div> depth) are split into:

  candidate  contains a decision phrase AND a band word, and no outcome marker
  excluded   contains a decision phrase AND a band word, but also an outcome
             marker (a paragraph describing how the S$NEER or the economy
             moved); its text is never written, only counted
  other      everything else; never written, only counted

MPS_CANDIDATES.txt holds the candidate paragraphs only, verbatim, in page
order. That file is what the researcher reads to code office/MPS_CODING.csv.
"""
import glob
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "office", "MPS_CANDIDATES.txt")

DECISION = ["MAS will", "MAS has decided", "MAS decided", "MAS has", "will maintain",
            "will re-centre", "will set", "will continue"]
BAND = ["slope", "policy band", "appreciation", "re-centre", "centre", "width"]
OUTCOME = ["S$NEER has", "S$NEER was", "has appreciated", "has depreciated", "appreciated by",
           "depreciated by", "strengthened", "weakened", "traded", "GDP", "year-on-year"]


def rte_blocks(t):
    """Inner HTML of every <div> whose class contains mas-rte-content, found by
    counting <div> depth (MAS's statement text blocks)."""
    out = []
    for m in re.finditer(r'<div[^>]*class="[^"]*mas-rte-content[^"]*"[^>]*>', t):
        i, depth = m.end(), 1
        for d in re.finditer(r"<(/?)div\b[^>]*>", t[i:]):
            depth += -1 if d.group(1) else 1
            if depth == 0:
                out.append(t[i:i + d.start()])
                break
    return out


def paragraphs(t):
    """Text of each <p> and <li> in the statement text blocks, in page order."""
    out = []
    for b in rte_blocks(t):
        for m in re.finditer(r"<(p|li)\b[^>]*>(.*?)</\1\s*>", b, re.S | re.I):
            text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", m.group(2))).split())
            if text:
                out.append(text)
    return out


def norm(s):
    return s.replace("\u2019", "'").replace("\u2013", "-").replace("\u2014", "-").replace("\xa0", " ")


def classify(p):
    q = norm(p)
    low = q.lower()
    dec = any(d in q for d in DECISION)
    band = any(b in low for b in BAND)
    outcome = any(o.lower() in low for o in OUTCOME)
    if dec and band and not outcome:
        return "candidate"
    if dec and band:
        return "excluded"
    return "other"


def main():
    counts_only = "--counts" in sys.argv
    files = sorted(glob.glob(os.path.join(RAW, "s5b_mas_mps_*.html")))
    lines = ["# MPS_CANDIDATES.txt -- written by sgd/03_mps_candidates.py",
             "# Decision-paragraph candidates only, verbatim (THESIS section 5, MPS coding rule).",
             "# Paragraphs with an outcome marker, and all other paragraphs, are not written.", ""]
    for f in files:
        date = re.search(r"(\d{8})", os.path.basename(f)).group(1)
        paras = list(dict.fromkeys(paragraphs(open(f, encoding="utf-8", errors="replace").read())))
        kinds = [classify(p) for p in paras]
        n = {k: kinds.count(k) for k in ("candidate", "excluded", "other")}
        print(f"{date}  paragraphs {len(paras):3d}  candidate {n['candidate']}  "
              f"excluded {n['excluded']}  other {n['other']}")
        if not counts_only:
            lines.append(f"=== {date}  ({os.path.basename(f)})  candidates {n['candidate']}, "
                         f"excluded-as-outcome {n['excluded']}")
            for i, (p, k) in enumerate(zip(paras, kinds)):
                if k == "candidate":
                    lines.append(f"[para {i + 1}] " + norm(html.unescape(p)))
            lines.append("")
    if not counts_only:
        with open(OUT, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        print("wrote", os.path.relpath(OUT, HERE))


if __name__ == "__main__":
    main()
