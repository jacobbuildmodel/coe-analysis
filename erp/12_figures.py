"""
12_figures.py -- the two charts for the ERP piece.

Same rules as the parent repository's figures: the shared --fig-* tokens with
literal fallbacks, a prefers-color-scheme block plus :root[data-theme="dark"],
a 480-wide canvas, no text below 14px, one axis per panel, hairline grids,
LF line endings. Every number drawn comes from out/ (10_load.py, 11_tests.py).

  figs/chart1_speed_vs_band.svg   peak speed against LTA's bands, both road
                                  types, with cars per lane-km underneath
  figs/chart2_door_fee.svg        km per car, high- vs low-premium years
"""
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FIGS = os.path.join(HERE, "figs")

INK = "var(--fig-ink,#0b0b0b)"
INK2 = "var(--fig-ink-2,#52514e)"
INK3 = "var(--fig-ink-3,#717171)"
RULE = "var(--fig-rule,#e2e1dd)"
SURF = "var(--fig-surface,#fcfcfa)"
SUBJ = "var(--fig-subject,#2873ce)"
CTX = "var(--fig-context,#707379)"

STYLE = ("<style>"
         ":root{--fig-ink:#0b0b0b;--fig-ink-2:#52514e;--fig-ink-3:#717171;"
         "--fig-rule:#e2e1dd;--fig-surface:#fcfcfa;--fig-subject:#2873ce;"
         "--fig-context:#707379;}"
         "@media (prefers-color-scheme: dark){:root{--fig-ink:#ffffff;"
         "--fig-ink-2:#c3c2b7;--fig-ink-3:#9a9a9a;--fig-rule:#38393a;"
         "--fig-surface:#1a1a19;--fig-subject:#3987e5;--fig-context:#93969c;}}"
         ":root[data-theme=\"dark\"]{--fig-ink:#ffffff;--fig-ink-2:#c3c2b7;"
         "--fig-ink-3:#9a9a9a;--fig-rule:#38393a;--fig-surface:#1a1a19;"
         "--fig-subject:#3987e5;--fig-context:#93969c;}"
         "text{font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,"
         "Roboto,Helvetica,Arial,sans-serif;}"
         "</style>")


def text(s, x, y, body, size=14, fill=INK3, anchor="start", weight=None):
    w = f' font-weight="{weight}"' if weight else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    s.append(f'<text x="{x:.1f}" y="{y:.1f}"{a} font-size="{size}" fill="{fill}"{w}>{body}</text>')


def write(name, parts):
    path = os.path.join(FIGS, name)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(parts) + "\n")
    print(f"  figs/{name}")


def chart1(t, tests):
    W, H = 480, 500
    L, R = 46, 348
    x0, x1 = 2004, 2025
    X = lambda y: L + (R - L) * (y - x0) / (x1 - x0)
    # panel A: speed
    aT, aB, alo, ahi = 104, 282, 15, 70
    YA = lambda v: aB - (aB - aT) * (v - alo) / (ahi - alo)
    # panel B: cars per lane-km, 2005 = 100
    bT, bB, blo, bhi = 350, 432, 95, 130
    YB = lambda v: bB - (bB - bT) * (v - blo) / (bhi - blo)

    exp_out = tests["T1_expressway_outside_years"]
    art_out = tests["T1_arterial_outside_years"].split()
    alt = ("Two-panel chart. Top: average peak-hour speed on expressways and arterial "
           "roads each year from 2004 to 2025, against LTA's target bands of 45 to 65 "
           "and 20 to 30 km/h. Expressway speed stays inside its band every year. "
           f"Arterial speed runs above 30 km/h in {' and '.join(art_out)} among the "
           "scored years, and in 2020 and 2021, which are not scored. Bottom: cars per "
           "lane-kilometre, 2005 = 100, rising by about a quarter on both road types "
           "from 2005 to 2017.")
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="{alt}">', STYLE,
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="{SURF}"/>']

    text(s, 12, 24, "Roads filled up; peak speeds stayed", 17, INK, weight="600")
    text(s, 12, 45, "near LTA's targets", 17, INK, weight="600")
    text(s, 12, 68, "Average peak-hour speed, km/h, 2004-2025,")
    text(s, 12, 86, "against LTA's target bands")

    # 2020-2021 greyed
    gx0, gx1 = X(2019.5), X(2021.5)
    s.append(f'<rect x="{gx0:.1f}" y="{aT}" width="{gx1-gx0:.1f}" height="{aB-aT}" '
             f'fill="{CTX}" opacity="0.18"/>')
    text(s, (gx0 + gx1) / 2, aT - 6, "2020-21", anchor="middle")

    # bands
    for lo, hi in ((45, 65), (20, 30)):
        s.append(f'<rect x="{L}" y="{YA(hi):.1f}" width="{R-L}" height="{YA(lo)-YA(hi):.1f}" '
                 f'fill="{CTX}" opacity="0.12"/>')
    for v in (20, 30, 45, 65):
        s.append(f'<line x1="{L}" y1="{YA(v):.1f}" x2="{R}" y2="{YA(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, L - 6, YA(v) + 5, str(v), anchor="end")

    for col, colr, lab in (("speed_expressway", INK2, "expressways"),
                           ("speed_arterial", SUBJ, "arterial roads")):
        pts = " ".join(f"{X(y):.1f},{YA(v):.1f}" for y, v in t[col].items())
        s.append(f'<polyline points="{pts}" fill="none" stroke="{colr}" stroke-width="2.4" '
                 f'stroke-linejoin="round" stroke-linecap="round"/>')
        last = t[col].iloc[-1]
        text(s, R + 8, YA(last) + 5, lab, 14, colr, weight="600")

    # the answer: scored arterial years above the band
    for y in art_out:
        y = int(y)
        v = t.speed_arterial.loc[y]
        s.append(f'<circle cx="{X(y):.1f}" cy="{YA(v):.1f}" r="4.5" fill="{SUBJ}"/>')
    text(s, L + 6, YA(41), f"arterial above the band in {art_out[0]}", 14, INK2)
    text(s, L + 6, YA(41) + 17, f"and {art_out[1]} (dots): bet 1 lost", 14, INK2)

    for y in (2004, 2010, 2015, 2020, 2025):
        text(s, X(y), aB + 20, str(y), anchor="middle")

    # panel B
    text(s, 12, bT - 16, "Cars per lane-km, 2005 = 100 (lane-km data end 2017)")
    for v in (100, 125):
        s.append(f'<line x1="{L}" y1="{YB(v):.1f}" x2="{R}" y2="{YB(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, L - 6, YB(v) + 5, str(v), anchor="end")
    yrs = list(range(2005, 2018))
    for lk, colr, lab in (("lanekm_expressway", INK2, "expressways"),
                          ("lanekm_arterial", SUBJ, "arterial roads")):
        d = t.cars.loc[yrs] / t[lk].loc[yrs]
        idx = 100 * d / d.iloc[0]
        pts = " ".join(f"{X(y):.1f},{YB(v):.1f}" for y, v in idx.items())
        s.append(f'<polyline points="{pts}" fill="none" stroke="{colr}" stroke-width="2.4" '
                 f'stroke-linejoin="round" stroke-linecap="round"/>')
    last_a = 100 * (t.cars.loc[2017] / t.lanekm_arterial.loc[2017]) / (t.cars.loc[2005] / t.lanekm_arterial.loc[2005])
    last_e = 100 * (t.cars.loc[2017] / t.lanekm_expressway.loc[2017]) / (t.cars.loc[2005] / t.lanekm_expressway.loc[2005])
    text(s, X(2017) + 8, YB(max(last_a, last_e)) + 2, f"+{max(last_a, last_e)-100:.0f}%", 14, INK2, weight="600")
    text(s, X(2017) + 8, YB(min(last_a, last_e)) + 16, f"+{min(last_a, last_e)-100:.0f}%", 14, INK2, weight="600")
    for y in (2005, 2010, 2015):
        text(s, X(y), bB + 20, str(y), anchor="middle")

    text(s, 12, H - 12, "Source: LTA via data.gov.sg. 2020-21 not scored.")
    s.append("</svg>")
    write("chart1_speed_vs_band.svg", s)
    return last_e, last_a


def chart2(t, tests, split):
    W, H = 480, 390
    L, R, T, B = 60, 372, 118, 316
    yrs = list(split.index)
    n = len(yrs)
    bw = (R - L) / n
    lo, hi = 0, 22000
    Y = lambda v: B - (B - T) * (v - lo) / (hi - lo)

    hi_km = tests["T3_high_mean_km"]
    lo_km = tests["T3_low_mean_km"]
    pct = tests["T3_pct_lower"]
    alt = ("Bar chart. Average kilometres driven per car each year, 2005 to 2018. The seven "
           f"years with the highest COE premium average {hi_km:,.0f} km, the seven with the "
           f"lowest {lo_km:,.0f} km, {pct:.0f} per cent more. All seven high-premium years "
           "fall between 2011 and 2017.")
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="{alt}">', STYLE,
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="{SURF}"/>']
    text(s, 12, 24, f"In the dear-COE years, cars were", 17, INK, weight="600")
    text(s, 12, 45, f"driven {pct:.0f}% less", 17, INK, weight="600")
    text(s, 12, 68, "Average km per car per year, 2005-2018")
    s.append(f'<rect x="12" y="80" width="12" height="12" rx="2" fill="{SUBJ}"/>')
    text(s, 30, 91, "7 dearest-COE years")
    s.append(f'<rect x="200" y="80" width="12" height="12" rx="2" fill="{CTX}"/>')
    text(s, 218, 91, "7 cheapest")

    for v in (0, 10000, 20000):
        s.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{R}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, L - 6, Y(v) + 5, f"{v:,}", anchor="end")
    for i, y in enumerate(yrs):
        v = split.km_per_car.loc[y]
        colr = SUBJ if split.half.loc[y] == "high" else CTX
        x = L + i * bw + 3
        s.append(f'<rect x="{x:.1f}" y="{Y(v):.1f}" width="{bw-6:.1f}" height="{B-Y(v):.1f}" fill="{colr}"/>')
    for y in (2005, 2010, 2015, 2018):
        i = yrs.index(y)
        text(s, L + (i + 0.5) * bw, B + 20, str(y), anchor="middle")

    # the answer: the two means
    for m in (lo_km, hi_km):
        s.append(f'<line x1="{L}" y1="{Y(m):.1f}" x2="{R + 4}" y2="{Y(m):.1f}" stroke="{INK}" '
                 f'stroke-width="1.5"/>')
    text(s, R + 8, Y(lo_km) - 2, f"cheapest 7:", 14, INK2)
    text(s, R + 8, Y(lo_km) + 14, f"{lo_km:,.0f} km", 14, INK, weight="600")
    text(s, R + 8, Y(hi_km) + 22, f"dearest 7:", 14, INK2)
    text(s, R + 8, Y(hi_km) + 38, f"{hi_km:,.0f} km", 14, SUBJ, weight="600")

    text(s, 12, H - 30, "The dear years all fall in 2011-2017, so the gap")
    text(s, 12, H - 12, "also runs with time. Source: LTA, SingStat.")
    s.append("</svg>")
    write("chart2_door_fee.svg", s)


def main():
    os.makedirs(FIGS, exist_ok=True)
    t = pd.read_csv(os.path.join(OUT, "annual.csv")).set_index("year")
    tests = pd.read_csv(os.path.join(OUT, "tests.csv")).set_index("key").value
    num = lambda k: float(tests[k])
    tv = {k: tests[k] for k in tests.index}
    for k in ("T3_high_mean_km", "T3_low_mean_km", "T3_pct_lower"):
        tv[k] = num(k)
    split = pd.read_csv(os.path.join(OUT, "t3_split.csv")).set_index("year")
    e, a = chart1(t, tv)
    chart2(t, tv, split)
    print(f"  cars per lane-km 2005-2017: expressways +{e-100:.1f}%, arterial +{a-100:.1f}%")


if __name__ == "__main__":
    main()
