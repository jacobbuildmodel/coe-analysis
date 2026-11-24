"""
00_coverage.py -- the cdc piece's coverage listing. Labels, codes and periods
only; never an index value.

  python3 cdc/00_coverage.py            metadata, then per-row period coverage
  python3 cdc/00_coverage.py --meta     metadata endpoint only

It is the only script allowed to touch SingStat before THESIS.md is sealed.

1. Metadata endpoint of table M213751 (no values are served by it): title,
   frequency, first and last period, last-updated stamp, and the label of
   every row this piece names.
2. Per-row coverage. The metadata endpoint gives the span of the table, not
   of a row. For each named row the script asks the data endpoint for the
   row and keeps, in memory only, the list of period keys and whether each
   period has an observation. It prints the count, the first and last period
   with an observation and the number of gaps. No value is printed, written
   to disk or returned; an error prints its type only, never a response body.

Output is pasted into raw/RETRIEVED.txt under COVERAGE (CHECKPOINTS, seal).
Standard library only.
"""
import json
import sys
import urllib.parse
import urllib.request

TABLE = "M213751"
BASE = "https://tablebuilder.singstat.gov.sg/api/table"
ROWS = ["1", "1.11", "1.11.1", "1.11.1.1", "1.11.2", "1.11.3", "1.11.3.1",
        "1.11.3.2", "1.03.2.3"]
MONTHS = {m: i + 1 for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
EMPTY = {"", "na", "n.a.", "-", "null", "none"}


def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (research coverage listing)",
        "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode("utf-8"))


def ym(key):
    """'2005 Jan' -> (2005, 1)."""
    y, m = key.split()
    return int(y), MONTHS[m]


def metadata():
    rec = get(f"{BASE}/metadata/{TABLE}")["Data"]["records"]
    print(f"table        {TABLE}")
    for k in ("title", "frequency", "datasource", "startPeriod", "endPeriod",
              "dataLastUpdated"):
        print(f"{k:12s} {rec.get(k)}")
    labels = {r.get("seriesNo"): (r.get("rowText"), r.get("uoM"))
              for r in rec.get("row", [])}
    print("rows named by this piece (seriesNo | label | unit):")
    for s in ROWS:
        lab = labels.get(s)
        print(f"  {s:9s} | {lab[0] if lab else 'NOT IN TABLE'} | "
              f"{lab[1] if lab else ''}")
    return labels


def row_coverage(series_no):
    """Period keys with an observation, for one row. Values never leave here."""
    keys, offset = [], 0
    while True:
        q = urllib.parse.urlencode({"seriesNoORrowNo": series_no,
                                    "offset": offset, "limit": 2000})
        rows = get(f"{BASE}/tabledata/{TABLE}?{q}")["Data"].get("row", [])
        got = 0
        for r in rows:
            if str(r.get("seriesNo")) != series_no:
                continue
            for c in r.get("columns", []):
                got += 1
                present = str(c.get("value", "")).strip().lower() not in EMPTY
                keys.append((ym(c["key"]), present))
        if got < 2000:
            break
        offset += 2000
    return sorted(set(keys))


def main():
    try:
        metadata()
    except Exception as exc:                      # never print a body
        print(f"metadata request failed: {type(exc).__name__}")
        return 1
    if "--meta" in sys.argv:
        return 0
    print("per-row coverage (periods with an observation; no values):")
    bad = 0
    for s in ROWS:
        try:
            cov = row_coverage(s)
        except Exception as exc:
            print(f"  {s:9s} request failed: {type(exc).__name__}")
            bad += 1
            continue
        have = [k for k, p in cov if p]
        if not have:
            print(f"  {s:9s} no observation in {len(cov)} period keys")
            bad += 1
            continue
        (y0, m0), (y1, m1) = have[0], have[-1]
        span = (y1 - y0) * 12 + (m1 - m0) + 1
        print(f"  {s:9s} {len(have):4d} months, {y0}-{m0:02d} to {y1}-{m1:02d}, "
              f"gaps inside the span: {span - len(have)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
