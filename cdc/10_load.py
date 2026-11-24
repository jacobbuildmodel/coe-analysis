"""
10_load.py -- raw SingStat responses to one tidy table.

  python3 cdc/10_load.py [--raw DIR] [--out DIR]

Reads every M213751_<seriesNo>.json in the raw directory (and in any
update_* directory inside it; a later file adds months, and a month present
in both must agree or the script stops) and writes out/series.csv: one line
per month, one column per row code, index values as published.

Refuses cdc/raw/ until the thesis is sealed (cdc/SEALED exists). The tests
pass --raw with invented data. Standard library only.
"""
import argparse
import csv
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
MONTHS = {m: i + 1 for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
EMPTY = {"", "na", "n.a.", "-", "null", "none"}


def read_file(path):
    code = path.stem.split("_", 1)[1]
    rows = json.loads(path.read_text(encoding="utf-8"))["Data"]["row"]
    out = {}
    for r in rows:
        if str(r.get("seriesNo")) != code:
            continue
        for c in r.get("columns", []):
            v = str(c.get("value", "")).strip()
            if v.lower() in EMPTY:
                continue
            y, m = c["key"].split()
            out[(int(y), MONTHS[m])] = v
    if not out:
        raise SystemExit(f"{path.name}: no observation for row {code}")
    return code, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(HERE / "raw"))
    ap.add_argument("--out", default=str(HERE / "out"))
    a = ap.parse_args()
    raw, out = pathlib.Path(a.raw).resolve(), pathlib.Path(a.out)
    if raw == (HERE / "raw").resolve() and not (HERE / "SEALED").exists():
        print("cdc/SEALED is absent: the thesis is not sealed, cdc/raw/ is not read.")
        return 1
    files = sorted(raw.glob("M213751_*.json"))
    for d in sorted(p for p in raw.glob("update_*") if p.is_dir()):
        files += sorted(d.glob("M213751_*.json"))
    if not files:
        print(f"no M213751_*.json in {raw}")
        return 1
    data = {}
    for f in files:
        code, obs = read_file(f)
        have = data.setdefault(code, {})
        for ym, v in obs.items():
            if ym in have and float(have[ym]) != float(v):
                raise SystemExit(f"{f.name}: {ym} differs from the first download "
                                 "(a revision): stop and report it")
            have.setdefault(ym, v)
    codes = sorted(data)
    months = sorted({ym for c in codes for ym in data[c]})
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "series.csv", "w", newline="", encoding="ascii") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["period"] + codes)
        for ym in months:
            w.writerow([f"{ym[0]}-{ym[1]:02d}"] + [data[c].get(ym, "") for c in codes])
    for c in codes:
        ks = sorted(data[c])
        print(f"  {c:9s} {len(ks):4d} months, {ks[0][0]}-{ks[0][1]:02d} to "
              f"{ks[-1][0]}-{ks[-1][1]:02d}")
    print(f"wrote {out / 'series.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
