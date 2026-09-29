"""
01b_w2a_labels.py -- list the DataSeries labels of the two W2a tables
(raw/w2a_services_detailed_industry.csv, raw/w2a_services_industry_group.csv).
Runs before THESIS.md is sealed, so it never prints a value: it reads the
DataSeries column alone (usecols), and every year column is left unread.
Labels are text, like the OWS titles listed by 01_titles.py.

Output: office/w2a_labels.txt (committed, for audit): one label per line,
in file order, with its row number; indentation as published.
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
FILES = ["w2a_services_detailed_industry.csv", "w2a_services_industry_group.csv"]
OUT = HERE / "office" / "w2a_labels.txt"


def main():
    out = []
    for name in FILES:
        labels = pd.read_csv(HERE / "raw" / name, usecols=["DataSeries"], dtype=str)["DataSeries"]
        out.append(f"=== {name}: DataSeries column only, {len(labels)} rows")
        for i, lab in enumerate(labels):
            out.append(f"{i:5d}  {str(lab).encode('ascii', 'replace').decode('ascii')}")
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(HERE.parent)}: {len(out)} lines")


if __name__ == "__main__":
    main()
