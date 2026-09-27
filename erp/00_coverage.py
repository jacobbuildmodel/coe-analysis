"""Coverage check for erp/raw/: bytes, md5, row count, columns, first and last period.

Prints nothing else. It is the only script allowed to open a data file before
THESIS.md is sealed, and it deliberately never prints a data value: for each
CSV it reports the shape and the span of the period column, and for each PDF
only its size and hash.
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


def main():
    files = sorted(p for p in RAW.iterdir() if p.suffix.lower() in (".csv", ".pdf"))
    if not files:
        print("erp/raw/ holds no .csv or .pdf file")
        return
    for path in files:
        print(f"{path.name}")
        print(f"  bytes   {path.stat().st_size}")
        print(f"  md5     {md5(path)}")
        if path.suffix.lower() != ".csv":
            continue
        df = pd.read_csv(path, dtype=str)
        print(f"  rows    {len(df)}")
        print(f"  columns {' | '.join(df.columns)}")
        col = period_column(df)
        if col is None:
            print("  period  no column named like year/month/quarter/period/date")
        else:
            span = df[col].dropna().sort_values()
            print(f"  period  {col}: {span.iloc[0]} to {span.iloc[-1]}, {span.nunique()} distinct")


if __name__ == "__main__":
    main()
