"""
10_load.py -- raw/ into tidy tables in out/, for 11_tests.py.

  python3 sgd/10_load.py [--root DIR]

Refuses the real sgd/raw/ until sgd/SEALED exists (sgdlib.guard).

Writes, each sorted by its keys:
  out/neer.csv      area, period, value      S1, BIS broad nominal, monthly
  out/reer.csv      area, period, value      S1b, BIS broad real (context only)
  out/usd.csv       currency, period, value  S2, units per USD, monthly average
  out/usd_eop.csv   currency, period, value  S2 end of period (sensitivity 3)
  out/masfx.csv     currency, period, value  S3a, SGD per ONE unit (JPY per-100
                                             rates divided by 100)
  out/sneer.csv     period, value, n         S4, mean of the weekly readings in
                                             each calendar month, and their count
  out/gdp.csv       quarter, value           S6a, GDP in chained (2015) dollars,
                                             year-on-year growth, per cent
  out/cpi.csv       period, value            S7a, CPI All Items
  out/mps.csv       date, slope, centre, slope_in_force, recentre_score, p
                                             from office/MPS_CODING.csv
  out/coverage.csv  table, series, first, last, n
It stops (exit 2) if a series the scored tests need is missing or has a
repeated period.
"""
import csv
import json
import os
import sys
from collections import defaultdict

import sgdlib as L

MON = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}


def die(msg):
    sys.stderr.write("LOAD FAILED: " + msg + "\n")
    raise SystemExit(2)


def num(v):
    try:
        f = float(str(v).replace(",", ""))
    except (TypeError, ValueError):
        return None
    return f if f == f else None


def bis_csv(path, keep, key):
    """{series: {period: value}} from a BIS SDMX CSV; keep(row) filters rows,
    key(row) names the series. Values scaled by 10**UNIT_MULT when present."""
    out = defaultdict(dict)
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if not keep(r):
                continue
            v = num(r.get("OBS_VALUE"))
            if v is None:
                continue
            mult = num(r.get("UNIT_MULT")) or 0
            k, p = key(r), r["TIME_PERIOD"]
            if p in out[k]:
                die(f"{os.path.basename(path)}: repeated period {p} for {k}")
            out[k][p] = v * 10 ** mult
    return out


def tablebuilder(path):
    """{rowText: [(key, value)]} from a SingStat TableBuilder JSON; the first
    row with a given rowText wins."""
    with open(path, encoding="utf-8-sig") as f:
        d = json.load(f)
    out = {}
    for r in d["Data"]["row"]:
        out.setdefault(r.get("rowText"), (r.get("uoM", ""), [(c["key"], num(c.get("value")))
                                                          for c in r.get("columns", [])]))
    return out


def sg_month(k):
    y, m = k.split()
    return "%s-%02d" % (y, MON[m[:3]])


def sg_quarter(k):
    y, q = k.split()
    return "%s-Q%s" % (y, q[0])


def main():
    a = L.args("sgd step 10: load raw/ into tidy tables")
    P = L.paths(a.root)
    raw = L.guard(P["raw"])
    out = P["out"]
    cover = []

    def keep_eer(t):
        return lambda r: r.get("FREQ") == "M" and r.get("EER_BASKET") == "B" and r.get("EER_TYPE") == t

    for name, fname, t in (("neer", L.F_NEER, "N"), ("reer", L.F_REER, "R")):
        path = os.path.join(raw, fname)
        if not os.path.exists(path):
            if name == "neer":
                die(fname + " missing")
            continue
        S = bis_csv(path, keep_eer(t), lambda r: r["REF_AREA"])
        rows = sorted((a_, p, v) for a_, s in S.items() for p, v in s.items() if a_ in L.AREAS)
        L.write_csv(os.path.join(out, name + ".csv"), ["area", "period", "value"], rows)
        for a_ in sorted(S):
            if a_ in L.AREAS:
                ps = sorted(S[a_])
                cover.append([name, a_, ps[0], ps[-1], len(ps)])
        if name == "neer":
            for need in ("SG", "JP", "MY"):
                if need not in S:
                    die(f"S1 has no broad nominal series for {need}")

    for name, fname, coll in (("usd", L.F_USD, "A"), ("usd_eop", L.F_USD_EOP, "E")):
        path = os.path.join(raw, fname)
        if not os.path.exists(path):
            if name == "usd":
                die(fname + " missing")
            continue
        S = bis_csv(path, lambda r, c=coll: r.get("FREQ") == "M" and r.get("COLLECTION") == c,
                    lambda r: r["CURRENCY"])
        rows = sorted((c, p, v) for c, s in S.items() for p, v in s.items())
        L.write_csv(os.path.join(out, name + ".csv"), ["currency", "period", "value"], rows)
        for c in sorted(S):
            ps = sorted(S[c])
            cover.append([name, c, ps[0], ps[-1], len(ps)])
        if name == "usd":
            for need in ("SGD", "JPY", "MYR"):
                if need not in S:
                    die(f"S2 has no monthly-average series for {need}")

    T = tablebuilder(os.path.join(raw, L.F_MASFX))
    rows = []
    for cur, (label, per) in L.MAS_ROWS.items():
        if label not in T:
            die(f"S3a has no row {label!r}")
        uom, obs = T[label]
        if per == 100 and "100" not in uom:
            die(f"S3a {label}: unit {uom!r} is not per 100")
        ps = []
        for k, v in obs:
            if v is not None:
                rows.append((cur, sg_month(k), v / per))
                ps.append(sg_month(k))
        if not ps:
            die(f"S3a {label} is empty")
        ps.sort()
        cover.append(["masfx", cur, ps[0], ps[-1], len(ps)])
    L.write_csv(os.path.join(out, "masfx.csv"), ["currency", "period", "value"], sorted(rows))

    with open(os.path.join(raw, L.F_SNEER), encoding="utf-8-sig") as f:
        d = json.load(f)
    by = defaultdict(list)
    for e in d["elements"]:
        v = num(e.get("value"))
        if v is not None:
            by[str(e["date"])[:7]].append(v)
    rows = [(p, sum(v) / len(v), len(v)) for p, v in sorted(by.items())]
    if not rows:
        die("S4 is empty")
    L.write_csv(os.path.join(out, "sneer.csv"), ["period", "value", "n"], rows)
    cover.append(["sneer", "SG", rows[0][0], rows[-1][0], len(rows)])

    for name, fname, label, conv, head in (("gdp", L.F_GDP, L.GDP_ROW, sg_quarter, "quarter"),
                                           ("cpi", L.F_CPI, L.CPI_ROW, sg_month, "period")):
        T = tablebuilder(os.path.join(raw, fname))
        if label not in T:
            die(f"{fname} has no row {label!r}")
        rows = sorted((conv(k), v) for k, v in T[label][1] if v is not None)
        if not rows:
            die(f"{fname} {label} is empty")
        if len({r[0] for r in rows}) != len(rows):
            die(f"{fname} {label}: repeated period")
        L.write_csv(os.path.join(out, name + ".csv"), [head, "value"], rows)
        cover.append([name, label, rows[0][0], rows[-1][0], len(rows)])

    if not os.path.exists(P["coding"]):
        die("office/MPS_CODING.csv missing")
    C = L.read_csv(P["coding"])
    rows = sorted((r["date"], r["slope"], r["centre"], int(r["slope_in_force"]), int(r["recentre_score"]),
                   int(r["p"])) for r in C)
    if not rows:
        die("office/MPS_CODING.csv has no rows")
    L.write_csv(os.path.join(out, "mps.csv"),
                ["date", "slope", "centre", "slope_in_force", "recentre_score", "p"], rows)
    cover.append(["mps", "decisions", rows[0][0], rows[-1][0], len(rows)])

    L.write_csv(os.path.join(out, "coverage.csv"), ["table", "series", "first", "last", "n"], cover)
    print(f"  loaded {len(cover)} series into {os.path.relpath(out, P['root'])}/")


if __name__ == "__main__":
    main()
