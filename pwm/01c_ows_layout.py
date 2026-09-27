"""
01c_ows_layout.py -- record the layout of the OWS all-industries tables that
10_load.py reads: sheet names, sheet size, and every header cell (a cell above
the first occupation row that holds letters) with its row and column. Runs
before the seal, so it never prints a value: a cell is printed only if it
holds letters and sits above the first occupation row, exactly the cells
01_titles.py prints; data rows are described by their row numbers and a
count of non-empty cells per column, never by their contents.

Output: office/ows_layout.txt (committed). 10_load.py and the test fixtures
(tests/make_fixtures.py) are written against it.
"""
import importlib.util
import re
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore", message="Cannot parse header or footer")
HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OUT = HERE / "office" / "ows_layout.txt"

spec = importlib.util.spec_from_file_location("titles", HERE / "01_titles.py")
titles = importlib.util.module_from_spec(spec)
spec.loader.exec_module(titles)


def files(year):
    if year <= 2011:
        ext = "xls" if year == 2009 else "xlsx"
        return [(RAW / f"w1_ows_{year}_occupation_{k}.{ext}", None) for k in ("gross", "basic")]
    return [(RAW / f"w1_ows_{year}_occupation.xlsx", "T4")]


def main():
    out = []
    for year in range(2009, 2026):
        for path, sheet in files(year):
            sheets = titles.read(path)
            name = sheet or next(iter(sheets))
            df = sheets[name]
            hdr, code_col, title_col, first = titles.layout(df)
            codes = [i for i in range(first, len(df))
                     if isinstance(df.iat[i, code_col], str)
                     and titles.CODE.match(df.iat[i, code_col].strip().split(".")[0])]
            out.append(f"=== {path.name} | sheets: {', '.join(sheets)} | read: {name} | "
                       f"{df.shape[0]} rows x {df.shape[1]} cols | code col {code_col} | "
                       f"title col {title_col} | first data row {first} | "
                       f"coded rows {len(codes)}, row {codes[0]} to {codes[-1]}")
            # which columns hold anything in the coded rows: a count per
            # column of non-empty cells (never the cells themselves)
            filled = [sum(1 for i in codes if pd.notna(df.iat[i, j]) and str(df.iat[i, j]).strip() != "")
                      for j in range(df.shape[1])]
            out.append("  non-empty cells per column in coded rows: " +
                       ", ".join(f"c{j}={n}" for j, n in enumerate(filled)))
            for i in range(first):
                for j, v in enumerate(df.iloc[i]):
                    t = titles.text(v)
                    if t:
                        t = re.sub(r"\s+", " ", t)
                        out.append(f"  r{i} c{j}: {t}")
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(HERE.parent)}: {len(out)} lines")


if __name__ == "__main__":
    main()
