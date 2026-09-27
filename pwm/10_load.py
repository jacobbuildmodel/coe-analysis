"""
10_load.py -- raw/ to tidy tables for the PWM piece (THESIS sections 4 and 5).

Refuses to read pwm/raw/ unless pwm/SEALED exists (pwmlib.guard). Run it on
the synthetic fixtures with --root.

Writes, under ROOT/out/:
  ows_lines.csv   one row per June x OCCUPATION_MAP line whose `series` is
                  main or sensitivity: group, code, title, series, the six
                  wage measures (25th percentile, median, 75th percentile of
                  basic and gross) and Number Covered. Lines are matched on
                  SSOC code plus title text, as 02_occupation_map.py does.
  cpi.csv         CPI all items (W4a) and lowest 20% (W4b), 2024 = 100.
  lfs_median.csv  LFS median gross monthly income from work, full-time
                  employed residents (W1c), excluding and including employer
                  CPF. T3's "middle" is the excluding column (THESIS T3).
  t4_series.csv   every candidate T4 series found, by unit and year.
  t4_choice.csv   the T4 priority rule applied (THESIS section 4): which
                  series qualifies, which is main, which is the sensitivity,
                  and why. Judged from coverage (years present), never from a
                  level.
  load_log.csv    per June: file and sheet read, header cells matched, lines
                  found.

Layouts (office/ows_layout.txt, 01c_ows_layout.py): the column of every
measure is found from the header text, never assumed, and asserted.
"""
import csv
import glob
import json
import math
import os
import re
import warnings

import pandas as pd

import pwmlib as L

warnings.filterwarnings("ignore", message="Cannot parse header or footer")
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

CODE = re.compile(r"^\d{4,5}$")
LETTERS = re.compile(r"[A-Za-z]")
ASCII = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
                       "\u2013": "-", "\u2014": "-", "\u00a0": " "})
MEASURES = ("p25", "med", "p75")


def text(v):
    if not (isinstance(v, str) and LETTERS.search(v)):
        return None
    return re.sub(r"\s+", " ", v.translate(ASCII).encode("ascii", "replace").decode("ascii")).strip()


def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def number(v):
    """A published cell as a float; suppression marks and blanks are NaN."""
    if v is None:
        return math.nan
    s = str(v).strip().replace(",", "").replace("$", "")
    try:
        return float(s)
    except ValueError:
        return math.nan


def code_of(v):
    if not isinstance(v, str):
        return ""
    c = v.strip().split(".")[0]
    return c if CODE.match(c) else ""


def ows_files(raw, year):
    """(path, sheet, kind): kind is gross, basic or both."""
    if year <= 2011:
        ext = "xls" if year == 2009 else "xlsx"
        return [(os.path.join(raw, f"w1_ows_{year}_occupation_{k}.{ext}"), None, k)
                for k in ("gross", "basic")]
    return [(os.path.join(raw, f"w1_ows_{year}_occupation.xlsx"), "T4", "both")]


def read_sheet(path, sheet):
    engine = "xlrd" if path.endswith(".xls") else "openpyxl"
    if sheet is None:
        return next(iter(pd.read_excel(path, sheet_name=None, header=None, dtype=str,
                                       engine=engine).values()))
    return pd.read_excel(path, sheet_name=sheet, header=None, dtype=str, engine=engine)


def parse_ows(df, kind):
    """Return (rows, log): rows are dicts code, title, n_covered and measures."""
    nrow, ncol = df.shape
    cell = lambda i, j: text(df.iat[i, j]) if j < ncol else None
    hdr = next(i for i in range(min(15, nrow))
               if any((cell(i, j) or "").upper().startswith("SSOC") for j in range(ncol))
               and any((cell(i, j) or "").lower().startswith("occupation") for j in range(ncol)))
    code_h = next(j for j in range(ncol) if (cell(hdr, j) or "").upper().startswith("SSOC"))
    occ_h = next(j for j in range(ncol) if (cell(hdr, j) or "").lower().startswith("occupation"))
    below = range(hdr + 1, nrow)
    code_col = max((code_h, code_h + 1), key=lambda j: sum(1 for i in below if j < ncol and code_of(df.iat[i, j])))
    coded = [i for i in below if code_of(df.iat[i, code_col])]
    first = coded[0]
    title_col = max((occ_h, occ_h + 1), key=lambda j: sum(1 for i in coded if cell(i, j)))
    heads = {(i, j): cell(i, j) for i in range(max(0, hdr - 1), first) for j in range(ncol) if cell(i, j)}

    def find(pred, rows=None):
        hits = [(i, j) for (i, j), t in heads.items() if pred(t) and (rows is None or i in rows)]
        assert hits, "header not found"
        return sorted(hits)[0]

    cols = {}
    _, cols["n_covered"] = find(lambda t: t.lower().startswith("number")) \
        if any(t.lower().startswith("number") for t in heads.values()) else (None, None)
    if kind == "both":
        for k, label in (("basic", "basic wage"), ("gross", "gross wage")):
            i, b = find(lambda t, label=label: t.lower() == label)
            subs = [heads.get((i + 1, b + d), "") for d in range(3)]
            assert "25th" in subs[0] and "Median" in subs[1] and "75th" in subs[2], subs
            for d, m in enumerate(MEASURES):
                cols[f"{m}_{k}"] = b + d
    else:
        _, cols[f"p25_{kind}"] = find(lambda t: t.startswith("First") or t.startswith("25th"))
        _, cols[f"med_{kind}"] = find(lambda t: t.startswith("Median"))
        _, cols[f"p75_{kind}"] = find(lambda t: t.startswith("Third") or t.startswith("75th"))
    rows, prev = [], None
    for i in range(first, nrow):
        t = cell(i, title_col)
        c = code_of(df.iat[i, code_col])
        if not t:
            continue
        if not c:
            if t.startswith("(") and prev is not None:
                prev["title"] += " " + t
            continue
        prev = {"code": c, "title": t}
        for k, j in cols.items():
            prev[k] = number(df.iat[i, j]) if j is not None else math.nan
        rows.append(prev)
    log = {"header_row": hdr, "code_col": code_col, "title_col": title_col, "first_row": first,
           "columns": ";".join(f"{k}=c{j}" for k, j in sorted(cols.items()) if j is not None)}
    return rows, log


def ows_year(raw, year):
    table, logs = {}, []
    for path, sheet, kind in ows_files(raw, year):
        rows, log = parse_ows(read_sheet(path, sheet), kind)
        log.update({"june": year, "file": os.path.basename(path), "sheet": sheet or "(first)",
                    "rows": len(rows)})
        logs.append(log)
        for r in rows:
            key = (r["code"], norm(r["title"]))
            entry = table.setdefault(key, {"code": r["code"], "title": r["title"]})
            for k, v in r.items():
                if k in ("code", "title") or (k == "n_covered" and k in entry):
                    continue          # Number Covered from the gross table first
                entry[k] = v
    return table, logs


def lookup(table, code, title):
    key = (code, norm(title))
    if key in table:
        return table[key]
    pre = [v for (c, t), v in table.items() if c == code and t.startswith(norm(title)[:25])]
    assert len(pre) == 1, f"map line not found once: {code} {title}"
    return pre[0]


def load_ows(raw):
    mp = [r for r in L.read_csv(L.MAP) if r["june"] and r["series"] in ("main", "sensitivity")
          and r["in_all_industries_table"] == "yes"]
    out, logs = [], []
    for year in sorted({int(r["june"]) for r in mp}):
        table, lg = ows_year(raw, year)
        logs += lg
        for r in (r for r in mp if int(r["june"]) == year):
            v = lookup(table, r["ssoc_code"], r["title_as_published"])
            side = "covered" if r["group"] in L.COVERED else "comparison"
            out.append([year, r["group"], side, r["ssoc_code"], r["title_as_published"], r["series"],
                        r["june_role"], v.get("n_covered", math.nan)] +
                       [v.get(f"{m}_{k}", math.nan) for k in ("gross", "basic") for m in MEASURES])
    return out, logs


def load_cpi(raw):
    res = {}
    for col, name in (("cpi_all", "w4a_cpi_annual_2024base.json"),
                      ("cpi_low20", "w4b_cpi_lowest20_annual_2024base.json")):
        with open(os.path.join(raw, name), encoding="utf-8") as f:
            rows = json.load(f)["Data"]["row"]
        row = next(r for r in rows if r["rowText"].strip() == "All Items")
        for c in row["columns"]:
            res.setdefault(int(c["key"]), {})[col] = number(c["value"])
    return [[y, res[y].get("cpi_all", math.nan), res[y].get("cpi_low20", math.nan)] for y in sorted(res)]


def load_lfs_median(raw):
    rows = L.read_csv(os.path.join(raw, "w1c_lfs_median_income.csv"))
    return [[int(r["year"]), number(r["median_income_excl_emp_cpf"]), number(r["median_income_incl_emp_cpf"])]
            for r in rows]


# ---------------------------------------------------------------- T4 series
def workers_candidates(raw):
    """Wide DataSeries tables (the W2a layout) with a block whose top-level
    label names workers or employment, holding every T4 line."""
    found = []
    for path in sorted(glob.glob(os.path.join(raw, "*.csv"))):
        with open(path, newline="", encoding="utf-8") as f:
            rd = csv.reader(f)
            head = next(rd, [])
            if not head or head[0] != "DataSeries":
                continue
            years = [(k, int(h)) for k, h in enumerate(head) if re.fullmatch(r"\d{4}", h.strip())]
            block, got = None, {}
            for row in rd:
                label = row[0]
                if label and not label.startswith(" "):
                    block = label if re.search(r"worker|employ", label, re.I) else None
                    continue
                if block is None:
                    continue
                for unit, labels in L.T4_LINES.items():
                    if label.strip() in labels:
                        got[(unit, label.strip())] = {y: number(row[k]) for k, y in years}
        want = {(u, lb) for u, lbs in L.T4_LINES.items() for lb in lbs}
        if want <= set(got):
            series = {}
            for (unit, _), vals in got.items():
                for y, v in vals.items():
                    series.setdefault(unit, {}).setdefault(y, 0.0)
                    series[unit][y] += v
            found.append((os.path.basename(path), series))
    assert len(found) <= 1, f"more than one workers-by-industry candidate: {[f for f, _ in found]}"
    return found[0] if found else None


def lfs_candidate(raw, lines_path):
    """Long LFS tables (the W2b layout: year, filters, occupation, count),
    lines fixed in T4_LFS_LINES.csv before the seal."""
    if not os.path.exists(lines_path):
        return None
    spec = L.read_csv(lines_path)
    if not spec:
        return None
    files = {s["file"] for s in spec}
    assert len(files) == 1, "T4_LFS_LINES.csv must name one file"
    name = files.pop()
    rows = L.read_csv(os.path.join(raw, name))
    series = {}
    for s in spec:
        filt = dict(kv.split("=", 1) for kv in s["filters"].split(";") if kv)
        for r in rows:
            if r[s["occupation_column"]].strip() != s["occupation"]:
                continue
            if any(r[k].strip() != v for k, v in filt.items()):
                continue
            v = number(r[s["count_column"]])
            if v == v:
                series.setdefault(s["unit"], {}).setdefault(int(r["year"]), 0.0)
                series[s["unit"]][int(r["year"])] += v
    return name, series


def qualify(series):
    """THESIS section 4 and 5: per covered industry, every post-period year
    present, and at least 4 pre-period years from the series' first year.
    Presence only: a year is present if the count exists for the industry
    and for the comparison set."""
    have = lambda u: {y for y, v in series.get(u, {}).items() if v == v and v > 0}
    comp = have("comparison")
    first = min((y for u in series for y in have(u)), default=None)
    res = {}
    for g in L.COVERED:
        yrs = have(g) & comp
        pre = [y for y in yrs if first is not None and first <= y <= L.PRE_END[g]]
        post_ok = all(y in yrs for y in L.POST[g])
        res[g] = {"pre_years": len(pre), "post_complete": post_ok,
                  "admitted": post_ok and len(pre) >= L.MIN_PRE}
    return first, res


def load_t4(raw, lines_path):
    cands = []
    w = workers_candidates(raw)
    if w:
        cands.append(("workers", w[0], w[1]))
    lf = lfs_candidate(raw, lines_path)
    if lf:
        cands.append(("lfs", lf[0], lf[1]))
    choice, series_rows = [], []
    q = {}
    for sid, fname, series in cands:
        first, res = qualify(series)
        q[sid] = any(r["admitted"] for r in res.values())
        for g, r in res.items():
            choice.append([sid, fname, first, g, r["pre_years"], r["post_complete"], r["admitted"]])
        for unit, vals in sorted(series.items()):
            for y, v in sorted(vals.items()):
                series_rows.append([sid, unit, y, v])
    main = "workers" if q.get("workers") else ("lfs" if q.get("lfs") else "none")
    sens = "lfs" if main == "workers" and q.get("lfs") else "none"
    roles = [["main", main], ["sensitivity", sens],
             ["workers_found", "workers" in q], ["workers_qualifies", q.get("workers", False)],
             ["lfs_found", "lfs" in q], ["lfs_qualifies", q.get("lfs", False)]]
    return series_rows, choice, roles


def main():
    a = L.args("PWM step 10: raw/ to tidy tables")
    P = L.paths(a.root)
    raw = L.guard(P["raw"])
    out = P["out"]
    rows, logs = load_ows(raw)
    L.write_csv(os.path.join(out, "ows_lines.csv"),
                ["june", "group", "side", "code", "title", "series", "june_role", "n_covered"] +
                [f"{m}_{k}" for k in ("gross", "basic") for m in MEASURES], rows)
    L.write_csv(os.path.join(out, "load_log.csv"),
                ["june", "file", "sheet", "rows", "header_row", "code_col", "title_col", "first_row", "columns"],
                [[g[k] for k in ("june", "file", "sheet", "rows", "header_row", "code_col", "title_col",
                                 "first_row", "columns")] for g in logs])
    L.write_csv(os.path.join(out, "cpi.csv"), ["year", "cpi_all", "cpi_low20"], load_cpi(raw))
    L.write_csv(os.path.join(out, "lfs_median.csv"), ["year", "median_excl_emp_cpf", "median_incl_emp_cpf"],
                load_lfs_median(raw))
    srows, choice, roles = load_t4(raw, P["lfs_lines"])
    L.write_csv(os.path.join(out, "t4_series.csv"), ["series", "unit", "year", "count"], srows)
    L.write_csv(os.path.join(out, "t4_choice.csv"), ["key", "value"],
                roles + [[f"{sid}_{g}_{k}", v] for sid, _, _, g, *vals in choice
                         for k, v in zip(("pre_years", "post_complete", "admitted"), vals)] +
                [[f"{sid}_file", f] for sid, f in dict((c[0], c[1]) for c in choice).items()] +
                [[f"{sid}_first_year", fy] for sid, fy in dict((c[0], c[2]) for c in choice).items()])
    n_main = sum(1 for r in rows if r[5] == "main")
    print(f"  ows_lines.csv: {len(rows)} lines ({n_main} main) over {len({r[0] for r in rows})} Junes")
    print(f"  T4 series: main = {roles[0][1]}, sensitivity = {roles[1][1]}")


if __name__ == "__main__":
    main()
