"""
01_download.py -- fetch the CPI rows this piece names and record provenance.

  python3 cdc/01_download.py

Refuses to run until the thesis is sealed (cdc/SEALED exists): this is the
first script that puts index values on disk. Writes one file per row,
raw/M213751_<seriesNo>.json (the SingStat response, byte for byte), and
raw/RETRIEVED.txt (time, URL, bytes and md5 of each file).

The forward test (T4) needs the months 2026 Dec to 2027 Feb: run again with
--update after the February 2027 index is published. --update writes
raw/update_<YYYY-MM>/ and leaves the first download untouched.

Standard library only.
"""
import hashlib
import json
import pathlib
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
TABLE = "M213751"
BASE = "https://tablebuilder.singstat.gov.sg/api/table"
ROWS = ["1.11.3", "1.11.1", "1.11.2", "1.03.2.3", "1.11.3.1", "1.11.3.2",
        "1.11.1.1", "1.11", "1"]


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (research download)",
        "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def main():
    if not (HERE / "SEALED").exists():
        print("cdc/SEALED is absent: the thesis is not sealed, nothing is downloaded.")
        return 1
    stamp = datetime.now(timezone.utc)
    raw = HERE / "raw"
    if "--update" in sys.argv:
        raw = raw / f"update_{stamp:%Y-%m}"
    elif (raw / "RETRIEVED.txt").exists():
        print("raw/RETRIEVED.txt exists: the first download is never overwritten "
              "(use --update).")
        return 1
    raw.mkdir(parents=True, exist_ok=True)
    lines = ["cdc piece - raw data provenance",
             f"retrieved  {stamp:%Y-%m-%d %H:%M:%S} UTC",
             f"source     SingStat Table Builder {TABLE}, Consumer Price Index "
             "(CPI), 2024 As Base Year, Monthly",
             "licence    Singapore Open Data Licence version 1.0", ""]
    for s in ROWS:
        q = urllib.parse.urlencode({"seriesNoORrowNo": s, "limit": 2000})
        url = f"{BASE}/tabledata/{TABLE}?{q}"
        body = fetch(url)
        rows = json.loads(body.decode("utf-8"))["Data"]["row"]
        if not any(str(r.get("seriesNo")) == s for r in rows):
            print(f"row {s} is not in the response; stopping")
            return 1
        name = f"{TABLE}_{s}.json"
        (raw / name).write_bytes(body)
        lines += [f"file  {name}", f"  url    {url}", f"  bytes  {len(body)}",
                  f"  md5    {hashlib.md5(body).hexdigest()}"]
        print(f"wrote {name}")
    (raw / "RETRIEVED.txt").write_text("\n".join(lines) + "\n", encoding="ascii",
                                       newline="\n")
    print("wrote RETRIEVED.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
