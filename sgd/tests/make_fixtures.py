"""
make_fixtures.py -- invented raw files for the sgd analysis, in the exact
formats of the real ones (BIS SDMX CSV, SingStat TableBuilder JSON, MAS chart
JSON, the MPS coding sheet). EVERY NUMBER HERE IS INVENTED. Nothing is read
from sgd/raw/.

  python3 sgd/tests/make_fixtures.py DIR      write a default fixture to DIR

build(dst, **knobs) is what the tests call. The model: each currency c has an
invented log "world value" v_c(t). Units of X per USD = exp(v_USD - v_X).
The broad index of area c is 100 * exp(v_c - mean of the other ten v), so
the BIS identities hold by construction (with equal weights, e = -b/10).

Knobs (defaults give a fixture where every scored test can run):
  seed               random seed
  jpy_scored         total change in v_JPY over 2021-01..2025-12
  myr_scored         total change in v_MYR over the same months
  sgd_vol            monthly noise of v_SG
  mas_bias           log bias of MAS's published JPY and MYR rates (T1 (b))
  sneer_noise        noise of MAS's weekly S$NEER readings (gate C)
  sneer_from         first week of the S$NEER feed ('YYYY-MM-DD')
  k_p, k_g           how much the policy score p and GDP growth g move v_SG
                     (annual log points per unit), for T7
  drop_areas         areas left out of S1 (T4's missing-series rule)
"""
import csv
import datetime
import json
import math
import os
import random
import sys

AREAS = ("SG", "JP", "MY", "KR", "CN", "TH", "ID", "US", "XM", "AU", "HK")
CUR = {"SG": "SGD", "JP": "JPY", "MY": "MYR", "KR": "KRW", "CN": "CNY", "TH": "THB", "ID": "IDR",
       "US": "USD", "XM": "EUR", "AU": "AUD", "HK": "HKD"}
NAME = {"SG": "Singapore", "JP": "Japan", "MY": "Malaysia", "KR": "Korea", "CN": "China", "TH": "Thailand",
        "ID": "Indonesia", "US": "United States", "XM": "Euro area", "AU": "Australia", "HK": "Hong Kong SAR"}
VOL = {"SG": 0.003, "JP": 0.025, "MY": 0.012, "KR": 0.02, "CN": 0.006, "TH": 0.013, "ID": 0.03,
       "US": 0.012, "XM": 0.015, "AU": 0.025, "HK": 0.012}
LEVEL = {"SG": 0.0, "JP": -4.6, "MY": -1.3, "KR": -7.0, "CN": -2.0, "TH": -3.5, "ID": -9.2,
         "US": 0.3, "XM": 0.4, "AU": 0.0, "HK": -1.75}
FIRST, LAST = "1994-01", "2026-08"
MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def dump(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f)


def months(a, b):
    out, (y, m) = [], (int(a[:4]), int(a[5:]))
    while "%04d-%02d" % (y, m) <= b:
        out.append("%04d-%02d" % (y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def decisions():
    """Invented MAS decisions: April and October, 2001 to 2026, with slope
    codes and re-centrings in the coding sheet's vocabulary."""
    rng = random.Random(7)
    out, sif = [], 1
    for y in range(2001, 2027):
        for mo in (4, 10):
            if (y, mo) > (2026, 4):
                break
            slope = rng.choice(["same", "same", "steeper", "flatter", "zero"])
            if slope == "zero":
                sif = 0
            elif slope in ("steeper", "flatter"):
                sif = 1
            rc = rng.choice([0, 0, 0, 1, -1])
            centre = {1: "up", -1: "down", 0: "unchanged"}[rc]
            out.append(("%04d%02d14" % (y, mo), slope, centre, sif, rc, sif + rc))
    return out


def build(dst, seed=1, jpy_scored=-0.8, myr_scored=-0.5, sgd_vol=0.003, mas_bias=0.0,
          sneer_noise=0.0005, sneer_from="1999-01-08", k_p=0.03, k_g=0.0, drop_areas=()):
    rng = random.Random(seed)
    ms = months(FIRST, LAST)
    scored = set(months("2021-01", "2025-12"))
    mps = decisions()
    # quarterly GDP growth, invented
    quarters = ["%d-Q%d" % (y, q) for y in range(1976, 2027) for q in (1, 2, 3, 4)
                if (y, q) <= (2026, 2)]
    gdp = {q: 3.0 + 3.0 * math.sin(i / 5.0) + rng.gauss(0, 1.5) for i, q in enumerate(quarters)}

    def p_at(m):
        cur = None
        for d in mps:
            if d[0][:4] + "-" + d[0][4:6] <= m:
                cur = d
        return cur[5] if cur else 0

    v = {a: [LEVEL[a]] for a in AREAS}
    for i, m in enumerate(ms[1:], 1):
        q = "%s-Q%d" % (m[:4], (int(m[5:]) - 1) // 3 + 1)
        g = gdp.get(q, 3.0)
        for a in AREAS:
            step = rng.gauss(0, sgd_vol if a == "SG" else VOL[a])
            if a == "SG":
                step += (k_p * p_at(m) + k_g * (g - 3.0)) / 12
            if a == "HK":
                step = (v["US"][i] - v["US"][i - 1]) if len(v["US"]) > i else step
            if m in scored and a == "JP":
                step += jpy_scored / len(scored)
            if m in scored and a == "MY":
                step += myr_scored / len(scored)
            v[a].append(v[a][-1] + step)
        # HK follows US exactly (the peg): recompute after US is known
        v["HK"][i] = v["HK"][i - 1] + (v["US"][i] - v["US"][i - 1])
    V = {a: dict(zip(ms, v[a])) for a in AREAS}

    def neer(a, m):
        others = [V[k][m] for k in AREAS if k != a]
        return 100 * math.exp(V[a][m] - sum(others) / len(others))

    raw = os.path.join(dst, "raw")
    office = os.path.join(dst, "office")
    os.makedirs(raw, exist_ok=True)
    os.makedirs(office, exist_ok=True)

    for fname, typ, label in (("s1_bis_eer_neer_broad_monthly.csv", "N", "Nominal"),
                              ("s1b_bis_eer_reer_broad_monthly.csv", "R", "Real")):
        with open(os.path.join(raw, fname), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["FREQ", "EER_TYPE", "EER_BASKET", "REF_AREA", "UNIT_MEASURE", "TIME_FORMAT", "COLLECTION",
                        "TITLE_TS", "TIME_PERIOD", "OBS_VALUE", "OBS_STATUS", "OBS_CONF", "OBS_PRE_BREAK"])
            for a in AREAS:
                if a in drop_areas:
                    continue
                for j, m in enumerate(ms):
                    val = neer(a, m) * (1 if typ == "N" else math.exp(0.0002 * j))
                    w.writerow(["M", typ, "B", a, "628", "", "A", f"{NAME[a]} - {label} - Broad (64 economies)",
                                m, "%.6f" % val, "A", "F", ""])

    for fname, coll, eps in (("s2_bis_xru_usd_monthly_avg.csv", "A", 0.0),
                             ("s2e_bis_xru_usd_monthly_eop.csv", "E", 0.002)):
        with open(os.path.join(raw, fname), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["FREQ", "REF_AREA", "CURRENCY", "COLLECTION", "UNIT_MULT", "DECIMALS", "AVAILABILITY",
                        "TITLE", "TIME_PERIOD", "OBS_VALUE", "OBS_STATUS", "OBS_PRE_BREAK", "OBS_CONF"])
            r2 = random.Random(seed + 11)
            for a in AREAS:
                if a == "US":
                    continue
                for m in ms:
                    val = math.exp(V["US"][m] - V[a][m] + (r2.gauss(0, eps) if eps else 0))
                    w.writerow(["M", a, CUR[a], coll, "0", "4", "A",
                                f" Exchange rates against USD {NAME[a]} - invented", m, "%.8f" % val, "A", "", "F"])

    r3 = random.Random(seed + 22)

    def tb(title, tid, rows):
        return {"Data": {"id": tid, "title": title, "dataLastUpdated": "01/01/2026", "row": rows},
                "DataCount": 0, "StatusCode": 200, "Message": ""}

    def mrow(no, text, uom, pts):
        return {"seriesNo": no, "rowText": text, "uoM": uom,
                "columns": [{"key": k, "value": "%.6f" % val} for k, val in pts]}

    def sgkey(m):
        return "%s %s" % (m[:4], MON[int(m[5:]) - 1])

    fx = []
    for a, per, text, uom in (("US", 1, "US Dollar", "Singapore Dollar Per US Dollar"),
                              ("JP", 100, "Japanese Yen", "Singapore Dollar Per 100 Japanese Yen"),
                              ("MY", 1, "Malaysian Ringgit", "Singapore Dollar Per Malaysian Ringgit")):
        pts = []
        for m in months("1988-01", LAST):
            if m < FIRST:
                continue
            sgd_per_unit = math.exp(V[a][m] - V["SG"][m])
            bias = mas_bias if a in ("JP", "MY") else 0.0
            pts.append((sgkey(m), per * sgd_per_unit * math.exp(bias + r3.gauss(0, 0.0005))))
        fx.append(mrow(str(len(fx) + 1), text, uom, pts))
    dump(tb("Exchange Rates (Average For Period), Monthly", "M700051", fx),
         os.path.join(raw, "s3a_mas_fx_monthly_avg_M700051.json"))

    els, d = [], datetime.date.fromisoformat(sneer_from)
    r4 = random.Random(seed + 33)
    while d <= datetime.date(2026, 8, 28):
        m = d.isoformat()[:7]
        if m in V["SG"]:
            els.append({"date": d.isoformat(), "value": round(neer("SG", m) * math.exp(r4.gauss(0, sneer_noise)), 4),
                        "updatedat": "2026-09-07T00:00:00", "no_of_rec": 1})
        d += datetime.timedelta(days=7)
    dump({"name": "invented_sneer", "elements": els, "links": []},
         os.path.join(raw, "s4_mas_sneer_weekly.json"))

    dump(tb("Gross Domestic Product, Year On Year Growth Rate, Quarterly", "M015631",
            [mrow("1", "GDP At Current Market Prices", "Per Cent",
                  [("%s %sQ" % (q[:4], q[-1]), g + 2) for q, g in gdp.items()]),
             mrow("2", "GDP In Chained (2015) Dollars", "Per Cent",
                  [("%s %sQ" % (q[:4], q[-1]), g) for q, g in gdp.items()])]),
         os.path.join(raw, "s6a_singstat_gdp_yoy_quarterly_M015631.json"))

    cpi, lvl = [], 40.0
    for m in months("1961-01", LAST):
        lvl *= math.exp(0.0018 + r3.gauss(0, 0.002))
        cpi.append((sgkey(m), lvl))
    dump(tb("Consumer Price Index (CPI), 2024 As Base Year, Monthly", "M213751",
            [mrow("1", "All Items", "Index", cpi)]),
         os.path.join(raw, "s7a_singstat_cpi_monthly_M213751.json"))

    with open(os.path.join(office, "MPS_CODING.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["date", "statement_file", "slope", "width", "centre", "centre_statement", "centre_source",
                    "recentre_no_direction", "slope_in_force", "recentre_score", "p", "source_para",
                    "quote_slope", "quote_width", "quote_centre", "s5a_slope", "s5a_width", "s5a_level",
                    "checker_review", "note"])
        for date, slope, centre, sif, rc, p in mps:
            w.writerow([date, "invented", slope, "same", centre, centre, "statement", "no", sif, rc, p,
                        "", "", "", "", "", "", "", "no", "INVENTED"])
    return dst


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "fixture_out"))
