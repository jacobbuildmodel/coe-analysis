"""
01_titles.py -- list occupation titles, SSOC codes and column headers in the
OWS wage tables, June 2009-2025. Runs before THESIS.md is sealed, so it never
prints a wage or head-count value.

What it prints, per year:
- the header rows of the all-industries table and of the table for the
  industry that holds contract cleaning, security and landscape (Business
  Services to 2022, Administrative and Support Services from 2023); every
  row above the first occupation row, which are labels;
- for every occupation row: the SSOC code (from the column headed "SSOC",
  and only if the cell is a 4- or 5-digit code) and the title text.

What it never prints: any cell of a wage or "Number Covered" column, any
suppression mark, or any note row. Title and code are read from their own
columns only; every other column of a data row is skipped unread.

Output: office/titles_listing.txt (committed, for audit).
"""
import re
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore", message="Cannot parse header or footer")

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OUT = HERE / "office" / "titles_listing.txt"
LETTERS = re.compile(r"[A-Za-z]")
CODE = re.compile(r"^\d{4,5}$")


def read(path):
    engine = "xlrd" if path.suffix == ".xls" else "openpyxl"
    return pd.read_excel(path, sheet_name=None, header=None, dtype=str, engine=engine)


ASCII = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-", "\u00a0": " "})


def text(v):
    """A cell's text if it holds letters, made ASCII (office rule), else None."""
    if not (isinstance(v, str) and LETTERS.search(v)):
        return None
    return v.translate(ASCII).encode("ascii", "replace").decode("ascii").strip()


HEADER_WORDS = re.compile(r"percentile|median|quartile|covered|\(\$\)|wage", re.I)


def layout(df):
    """Return (header_row, code_col, title_col, first_data_row).

    The code column is the one headed "SSOC", or the column right of it when
    MOM merged the header over two columns (2009-2011). The title column is
    the one headed "Occupation", or the column right of it (2009-2011). Only
    those two columns of a data row are ever read; a cell is taken as a title
    only if it holds letters and is not a header label.
    """
    for i in range(min(15, len(df))):
        row = [text(v) or "" for v in df.iloc[i]]
        ssoc = [j for j, c in enumerate(row) if c.upper().startswith("SSOC")]
        occ = [j for j, c in enumerate(row) if c.lower().startswith("occupation")]
        if not (ssoc and occ):
            continue
        code_col, occ_col = ssoc[0], occ[0]
        for k in range(i + 1, min(i + 10, len(df))):
            for tc in (occ_col, occ_col + 1):
                t = text(df.iat[k, tc])
                if t and not HEADER_WORDS.search(t):
                    codes_here = sum(
                        1 for r in range(k, min(k + 40, len(df)))
                        if isinstance(df.iat[r, code_col], str) and CODE.match(df.iat[r, code_col].strip().split(".")[0])
                    )
                    if codes_here == 0 and code_col + 1 < tc:
                        code_col += 1
                    return i, code_col, tc, k
    raise ValueError("no SSOC/Occupation header found")


def list_sheet(df, label, out):
    hdr, code_col, title_col, first = layout(df)
    out.append(f"  [{label}] header rows 0-{first - 1}; code column {code_col}; title column {title_col}")
    for i in range(first):
        cells = [text(v) for v in df.iloc[i]]
        cells = [c for c in cells if c]
        if cells:
            out.append(f"    header {i}: " + " | ".join(cells))
    prev = None
    for i in range(first, len(df)):
        title = text(df.iat[i, title_col])
        if not title or title.lower().startswith(("source", "note")):
            continue
        raw_code = df.iat[i, code_col]
        code = raw_code.strip().split(".")[0] if isinstance(raw_code, str) else ""
        code = code if CODE.match(code) else ""
        if not code and title.startswith("(") and prev is not None:
            out[prev] += " " + title          # continuation line of the title above
            continue
        out.append(f"    {code:>5}  {title}")
        prev = len(out) - 1


def main():
    out = []
    for year in range(2009, 2026):
        out.append(f"=== June {year}")
        if year <= 2011:
            ext = "xls" if year == 2009 else "xlsx"
            for kind in ("gross", "basic"):
                p = RAW / f"w1_ows_{year}_occupation_{kind}.{ext}"
                df = list(read(p).values())[0]
                list_sheet(df, f"{p.name}, all industries", out)
            for kind in ("gross", "basic"):
                p = RAW / f"w1_ows_{year}_industry_{kind}_08.{ext}"
                sheets = read(p)
                name, df = next(iter(sheets.items()))
                list_sheet(df, f"{p.name}, sheet {name}", out)
        else:
            p = RAW / f"w1_ows_{year}_occupation.xlsx"
            sheets = read(p)
            list_sheet(sheets["T4"], f"{p.name}, T4 all industries", out)
            # the industry holding contract cleaning, security and landscape:
            # "Business Services" to 2022, "Administrative and Support
            # Services" from 2023 (MOM split Business Services that year)
            for name, df in sheets.items():
                label = str(df.iat[2, 0]).upper()
                if name != "T4" and ("BUSINESS" in label or "ADMINISTRATIVE AND SUPPORT" in label):
                    list_sheet(df, f"{p.name}, {name}", out)
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(HERE.parent)}: {len(out)} lines")


if __name__ == "__main__":
    main()
