"""
make_fixtures.py -- write the synthetic raw files in tests/fixtures/raw/.

Every number here is invented. Nothing in pwm/raw/ is opened. The layouts
come from committed text only:
  office/ows_layout.txt     sheet names, sheet size, header cells and their
                            positions, first data row (01c_ows_layout.py)
  office/titles_listing.txt codes and titles in table order (01_titles.py)
  office/w2a_labels.txt     W2a DataSeries labels (01b_w2a_labels.py)
  RETRIEVED.txt coverage    column names of the CSV files (quoted below)
So the fixtures carry the real files' sheet names, headers, codes and titles,
and made-up values.

The invented wage model (log 25th percentile of gross pay, by title):
  base level by group, +0.03 a year, a post-period lift for covered main
  lines (0.15, transition 0.07), deterministic noise under 0.4 log points.
Basic = gross / 1.12; median = 1.25 x p25; p75 = 1.6 x p25. The base
fixture is built so that T1 passes, T2, T3, T4 and T5 survive; the unit
tests move the numbers to force every other branch.

Two T4 files are assumed layouts, since no real candidate has arrived:
  w2x_workers_by_industry_assumed.csv   the W2a layout with a "Workers" block;
  w2b_lfs_occupation_status.csv the real W2b columns (year, sex, occupation,
                                employment_status, employed), invented
                                occupation labels, lines in T4_LFS_LINES.csv.

  python3 pwm/tests/make_fixtures.py [--out DIR]   (default tests/fixtures)
"""
import argparse
import csv
import hashlib
import json
import math
import os
import re
import shutil

import openpyxl
import xlwt

HERE = os.path.dirname(os.path.abspath(__file__))
PWM = os.path.dirname(HERE)
OFFICE = os.path.join(PWM, "office")

LEVEL = {"cleaning": 850.0, "security": 950.0, "landscape": 1050.0}
LIFT_POST, LIFT_TRANS = 0.15, 0.07
POST0 = {"cleaning": 2016, "security": 2017, "landscape": 2017}
TRANS0 = {"cleaning": 2013, "security": 2015, "landscape": 2015}


def noise(*key, scale=0.004):
    h = int(hashlib.md5("|".join(map(str, key)).encode()).hexdigest()[:8], 16)
    return scale * (h / 0xFFFFFFFF * 2 - 1)


def read_map():
    with open(os.path.join(OFFICE, "OCCUPATION_MAP.csv"), newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["june"]]
    return {(int(r["june"]), r["ssoc_code"], re.sub(r"[^a-z0-9]", "", r["title_as_published"].lower())): r
            for r in rows}


def read_layout():
    lay, cur = {}, None
    for line in open(os.path.join(OFFICE, "ows_layout.txt"), encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("=== "):
            parts = [p.strip() for p in line[4:].split("|")]
            m = re.match(r"(\d+) rows x (\d+) cols", parts[3])
            cur = {"file": parts[0], "sheets": parts[1].split(": ", 1)[1].split(", "),
                   "read": parts[2].split(": ", 1)[1], "nrows": int(m.group(1)), "ncols": int(m.group(2)),
                   "code_col": int(re.search(r"code col (\d+)", line).group(1)),
                   "title_col": int(re.search(r"title col (\d+)", line).group(1)),
                   "first": int(re.search(r"first data row (\d+)", line).group(1)), "cells": []}
            lay[cur["file"]] = cur
        elif line.startswith("  r") and cur is not None:
            m = re.match(r"  r(\d+) c(\d+): (.*)", line)
            cur["cells"].append((int(m.group(1)), int(m.group(2)), m.group(3)))
    return lay


def read_listing():
    """{(file, 'all'): [(code, title), ...]} for the all-industries sections."""
    out, key = {}, None
    for line in open(os.path.join(OFFICE, "titles_listing.txt"), encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("  ["):
            m = re.match(r"  \[([^,\]]+)", line)
            key = m.group(1) if ("all industries" in line) else None
            if key:
                out[key] = []
            continue
        if key is None or line.startswith("=== ") or line.startswith("    header"):
            continue
        if line.startswith("    "):
            out[key].append((line[4:9].strip(), line[11:].strip()))
    return out


def measure_cols(cells, kind):
    """Column of each measure, from the header text, as 10_load.py finds it."""
    cols = {}
    num = [c for r, c, t in cells if t.lower().startswith("number")]
    cols["n"] = num[0] if num else None
    if kind == "both":
        for k, label in (("basic", "Basic Wage"), ("gross", "Gross Wage")):
            b = [c for r, c, t in cells if t == label][0]
            cols[k] = (b, b + 1, b + 2)
    else:
        f = lambda pre: [c for r, c, t in cells if any(t.startswith(p) for p in pre)][0]
        cols[kind] = (f(("First", "25th")), f(("Median",)), f(("Third", "75th")))
    return cols


def wage(year, code, title, mp):
    """Invented p25 gross for a title-year, shaped by the map's group."""
    r = mp.get((year, code, re.sub(r"[^a-z0-9]", "", title.lower())))
    g = r["group"] if r else None
    base = LEVEL.get(g, 1100.0 + 900.0 * (int(hashlib.md5(title.encode()).hexdigest()[:4], 16) / 65535))
    if g and g.startswith("C "):
        base = 1150.0 + 40.0 * (hash_int(g) % 7)
    if r and r["series"] == "sensitivity":
        base *= 1.3
    lg = math.log(base) + 0.03 * (year - 2009) + noise(year, code, title)
    if g in LEVEL and r and r["series"] in ("main", "sensitivity"):
        if year >= POST0[g]:
            lg += LIFT_POST
        elif year >= TRANS0[g]:
            lg += LIFT_TRANS
    return math.exp(lg)


def hash_int(s):
    return int(hashlib.md5(s.encode()).hexdigest()[:6], 16)


def row_values(year, code, title, mp, kind):
    p25g = wage(year, code, title, mp)
    vals = {"gross": (p25g, 1.25 * p25g, 1.6 * p25g)}
    b = p25g / 1.12
    vals["basic"] = (b, 1.25 * b, 1.6 * b)
    n = 100 + hash_int(f"{year}{code}{title}") % 2900
    return {k: tuple(round(x) for x in v) for k, v in vals.items()}, n


def ows_rows(lay, listing, year, fname, mp, kind):
    """Grid (dict of (r, c) -> value) for one all-industries sheet."""
    grid = {(r, c): t for r, c, t in lay["cells"]}
    cols = measure_cols(lay["cells"], kind)
    i = lay["first"]
    for code, title in listing:
        if not code:
            grid[(i, lay["title_col"])] = title
            i += 1
            continue
        vals, n = row_values(year, code, title, mp, kind)
        grid[(i, lay["code_col"])] = code
        grid[(i, lay["title_col"])] = title
        if kind == "both" and lay["code_col"] == 1:
            grid[(i, 0)] = i
        if cols.get("n") is not None:
            grid[(i, cols["n"])] = n
        for k in ("gross", "basic"):
            if k in cols:
                for j, v in zip(cols[k], vals[k]):
                    # a suppression mark on titles outside the map, as MOM prints
                    grid[(i, j)] = "-" if (hash_int(f"s{year}{code}") % 97 == 0 and
                                          (year, code, re.sub(r"[^a-z0-9]", "", title.lower())) not in mp) else v
        i += 1
    return grid


def write_xlsx(path, sheets):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name, grid in sheets:
        ws = wb.create_sheet(name)
        for (r, c), v in sorted(grid.items()):
            ws.cell(row=r + 1, column=c + 1, value=v)
    wb.save(path)


def write_xls(path, name, grid):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(name)
    for (r, c), v in sorted(grid.items()):
        ws.write(r, c, v)
    wb.save(path)


def ows(raw, mp):
    lay, listing = read_layout(), read_listing()
    for year in range(2009, 2026):
        if year <= 2011:
            ext = "xls" if year == 2009 else "xlsx"
            for kind in ("gross", "basic"):
                fname = f"w1_ows_{year}_occupation_{kind}.{ext}"
                L = lay[fname]
                grid = ows_rows(L, listing[fname], year, fname, mp, kind)
                if ext == "xls":
                    write_xls(os.path.join(raw, fname), L["read"], grid)
                else:
                    write_xlsx(os.path.join(raw, fname), [(L["read"], grid)])
        else:
            fname = f"w1_ows_{year}_occupation.xlsx"
            L = lay[fname]
            sheets = []
            for s in L["sheets"]:
                if s == "T4":
                    sheets.append((s, ows_rows(L, listing[fname], year, fname, mp, "both")))
                else:
                    sheets.append((s, {(0, 0): f"{s} (synthetic fixture: not read)"}))
            write_xlsx(os.path.join(raw, fname), sheets)


def csv_write(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def lfs_median(raw):
    # columns as RETRIEVED.txt records them; 2001-2025 less one year
    rows = [[y, round(2800 * math.exp(0.034 * (y - 2009))), round(2500 * math.exp(0.032 * (y - 2009)))]
            for y in range(2001, 2026) if y != 2002]
    csv_write(os.path.join(raw, "w1c_lfs_median_income.csv"),
              ["year", "median_income_incl_emp_cpf", "median_income_excl_emp_cpf"], rows)


def cpi(raw):
    for name, sid, title in (("w4a_cpi_annual_2024base.json", "M213801", "Consumer Price Index (CPI), 2024 As Base Year, Annual"),
                             ("w4b_cpi_lowest20_annual_2024base.json", "M213911",
                              "Consumer Price Index (CPI) By Household Income Group, Lowest 20%, 2024 As Base Year, Annual")):
        rows = []
        for k, (label, rate) in enumerate((("All Items", 0.02), ("Food", 0.025))):
            cols = [{"key": str(y), "value": f"{100 * math.exp(rate * (y - 2024)):.3f}"}
                    for y in range(1961 if sid == "M213801" else 1993, 2026)]
            rows.append({"seriesNo": str(k + 1), "rowText": label, "uoM": "Index", "footnote": "", "columns": cols})
        doc = {"Data": {"id": sid, "title": title, "frequency": "Annual", "row": rows},
               "DataCount": len(rows), "StatusCode": 200, "Message": "synthetic fixture"}
        with open(os.path.join(raw, name), "w", encoding="utf-8") as f:
            json.dump(doc, f)


def w2a_layout_labels():
    labels = []
    for line in open(os.path.join(OFFICE, "w2a_labels.txt"), encoding="utf-8"):
        if line.startswith("=== w2a_services_industry_group"):
            break
        m = re.match(r"\s*\d+  (.*)$", line.rstrip("\n"))
        if m and not line.startswith("==="):
            labels.append(m.group(1))
    return labels


def workers(raw, years=range(2010, 2025)):
    """W2a's real labels and years (DataSeries | 2024 ... 2010), invented
    numbers; plus, for the assumed workers file, a "Workers" block."""
    labels = w2a_layout_labels()
    ys = sorted(years, reverse=True)
    rows = [[lb] + [str(1000 + hash_int(lb + str(y)) % 9000) for y in ys] for lb in labels]
    csv_write(os.path.join(raw, "w2a_services_detailed_industry.csv"), ["DataSeries"] + [str(y) for y in ys], rows)
    first_block = labels[:labels.index("Operating Revenue, Total Services Sector")]
    wrows = []
    for lb in first_block:
        name = "Workers, Total Services Sector" if not lb.startswith(" ") else lb
        unit = next((u for u, lbs in T4_LINES().items() if lb.strip() in lbs), None)
        vals = []
        for y in ys:
            base = {"security": 40000, "landscape": 9000, "cleaning": 60000}.get(unit, 150000)
            vals.append(str(round(base * math.exp(0.01 * (y - 2010) + noise("w", lb, y, scale=0.003)))))
        wrows.append([name] + vals)
    csv_write(os.path.join(raw, "w2x_workers_by_industry_assumed.csv"), ["DataSeries"] + [str(y) for y in ys], wrows)


def T4_LINES():
    import importlib.util
    spec = importlib.util.spec_from_file_location("pwmlib", os.path.join(PWM, "pwmlib.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.T4_LINES


LFS_OCC = {"security": "Security guards (synthetic)", "landscape": "Park and garden workers (synthetic)",
           "cleaning": "Office cleaners (synthetic)", "comparison": "Shop sales and food service (synthetic)"}


def lfs(root, raw):
    rows = []
    for y in range(2010, 2026):
        for unit, occ in LFS_OCC.items():
            base = {"security": 20000, "landscape": 3000, "cleaning": 30000}.get(unit, 90000)
            for sex in ("Total", "Male", "Female"):
                for st in ("Total", "Employees", "Own Account Workers"):
                    share = (1.0 if sex == "Total" else 0.5) * (1.0 if st == "Total" else 0.5)
                    rows.append([y, sex, occ, st, round(base * share * math.exp(0.005 * (y - 2010) + noise("l", occ, y)))])
    csv_write(os.path.join(raw, "w2b_lfs_occupation_status.csv"),
              ["year", "sex", "occupation", "employment_status", "employed"], rows)
    csv_write(os.path.join(root, "T4_LFS_LINES.csv"),
              ["file", "unit", "occupation_column", "occupation", "count_column", "filters"],
              [["w2b_lfs_occupation_status.csv", u, "occupation", o, "employed",
                "sex=Total;employment_status=Total"] for u, o in LFS_OCC.items()])


def thesis_stub(root):
    text = ("# Synthetic fixture thesis stub: confidences only, for 11_tests.py.\n"
            "The real run reads pwm/THESIS.md.\n\n")
    for t, p in (("T1", 40), ("T2", 50), ("T3", 60), ("T4", 60), ("T5", 45)):
        text += f"### {t}.\n- **Confidence at seal: {p}%.**\n\n"
    with open(os.path.join(root, "THESIS.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def build(root):
    raw = os.path.join(root, "raw")
    if os.path.isdir(raw):
        shutil.rmtree(raw)
    os.makedirs(raw)
    mp = read_map()
    ows(raw, mp)
    lfs_median(raw)
    cpi(raw)
    workers(raw)
    lfs(root, raw)
    thesis_stub(root)
    with open(os.path.join(root, "README.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("Synthetic fixtures for the PWM analysis. Every number is invented.\n"
                "Rebuild with: python3 pwm/tests/make_fixtures.py\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "fixtures"))
    build(os.path.abspath(ap.parse_args().out))
    print("fixtures written")
