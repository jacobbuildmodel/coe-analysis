"""Coverage check for pwm/raw/: bytes, md5, row count, columns, first and last period.

Prints nothing else. It is the only script allowed to open a data file before
THESIS.md is sealed, and it deliberately never prints a data value:

- CSV: shape, column names, and the span of the period column.
- XLSX (MOM occupational wage tables): sheet names and each sheet's row and
  column counts only. Column headers are not printed, because MOM sheets carry
  title and note rows above the header and a header guess could print a value.
- PDF: size and hash only.
"""
import hashlib
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parent / "raw"
PERIOD_HINTS = ("year", "month", "quarter", "period", "date")


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def period_column(df):
    for col in df.columns:
        if any(hint in col.lower() for hint in PERIOD_HINTS):
            return col
    return None


def csv_coverage(path):
    df = pd.read_csv(path, dtype=str)
    print(f"  rows    {len(df)}")
    print(f"  columns {' | '.join(df.columns)}")
    col = period_column(df)
    if col is None:
        print("  period  no column named like year/month/quarter/period/date")
    else:
        span = df[col].dropna().sort_values()
        print(f"  period  {col}: {span.iloc[0]} to {span.iloc[-1]}, {span.nunique()} distinct")


def xlsx_coverage(path):
    sheets = pd.read_excel(path, sheet_name=None, header=None, dtype=str)
    for name, df in sheets.items():
        print(f"  sheet   {name}: {df.shape[0]} rows x {df.shape[1]} columns")


def main():
    files = sorted(p for p in RAW.iterdir() if p.suffix.lower() in (".csv", ".pdf", ".xlsx", ".xls"))
    if not files:
        print("pwm/raw/ holds no .csv, .xlsx or .pdf file")
        return
    for path in files:
        print(f"{path.name}")
        print(f"  bytes   {path.stat().st_size}")
        print(f"  md5     {md5(path)}")
        suffix = path.suffix.lower()
        if suffix == ".csv":
            csv_coverage(path)
        elif suffix in (".xlsx", ".xls"):
            xlsx_coverage(path)


if __name__ == "__main__":
    main()
