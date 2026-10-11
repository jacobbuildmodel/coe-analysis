"""
12_figures.py -- the lta-ab note's two charts, from out/ only.

Same conventions as the site's other charts (sgd/12_figures.py): the shared
--fig-* tokens with literal fallbacks, a prefers-color-scheme block plus
:root[data-theme="dark"], a 480-wide canvas for phone reading, no text below
14px, hairline grids, LF line endings. Each title states the finding, with its
numbers taken from out/facts.csv; each caption says how to read the chart.

  figs/lta_ab_chart1_gap.svg  per exercise, Category B's premium minus
                              Category A's, January 2010 to the cut-off, with
                              LTA's two example band steps marked (F1)
  figs/lta_ab_chart2_pqp.svg  per month, Category B's PQP minus Category A's,
                              January 2010 to October 2026 (F3)

Presentation only: nothing here computes a number the note prints.
"""
import csv
import html
import os
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FIGS = os.path.join(HERE, "figs")

INK = "var(--fig-ink,#0b0b0b)"
INK3 = "var(--fig-ink-3,#717171)"
RULE = "var(--fig-rule,#e2e1dd)"
SURF = "var(--fig-surface,#fcfcfa)"
SUBJ = "var(--fig-subject,#2873ce)"
CTX = "var(--fig-context,#707379)"
WARN = "var(--fig-accent,#c2410c)"
SHADE = "var(--fig-shade,#efeee9)"
STYLE = ("<style>"
         ":root{--fig-ink:#0b0b0b;--fig-ink-3:#717171;--fig-rule:#e2e1dd;--fig-surface:#fcfcfa;"
         "--fig-subject:#2873ce;--fig-context:#707379;--fig-accent:#c2410c;--fig-shade:#efeee9;}"
         "@media (prefers-color-scheme: dark){:root{--fig-ink:#ffffff;--fig-ink-3:#9a9a9a;"
         "--fig-rule:#38393a;--fig-surface:#1a1a19;--fig-subject:#3987e5;--fig-context:#93969c;"
         "--fig-accent:#f08a4b;--fig-shade:#262624;}}"
         ":root[data-theme=\"dark\"]{--fig-ink:#ffffff;--fig-ink-3:#9a9a9a;--fig-rule:#38393a;"
         "--fig-surface:#1a1a19;--fig-subject:#3987e5;--fig-context:#93969c;--fig-accent:#f08a4b;"
         "--fig-shade:#262624;}"
         "text{font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;}"
         "</style>")
W = 480
TITLE_CHARS, CAPTION_CHARS = 42, 56
LINE = 19
LEFT, RIGHT = 62, 16
PLOT_H = 230


def facts():
    return {r["key"]: r["printed"] for r in csv.DictReader(open(os.path.join(OUT, "facts.csv"), encoding="utf-8"))}


def rows(name):
    return list(csv.DictReader(open(os.path.join(OUT, name), encoding="utf-8")))


def esc(s):
    return html.escape(s, quote=True)


def t_of(month, ex=1, per_month=2):
    y, m = int(month[:4]), int(month[5:])
    return y + (m - 1) / 12 + (ex - 1) / (12 * per_month)


def chart(path, title, desc, caption, series, ymin, ymax, yticks, refs, t_shade, ylab, ref_label=None):
    title_lines = textwrap.wrap(title, TITLE_CHARS)
    cap_lines = []
    for para in caption:
        cap_lines += textwrap.wrap(para, CAPTION_CHARS)
    top = 14 + LINE * len(title_lines) + 22
    plot_top = top + 14
    plot_bot = plot_top + PLOT_H
    axis_bot = plot_bot + 26
    H = axis_bot + 14 + LINE * len(cap_lines) + 10
    x0, x1 = LEFT, W - RIGHT
    t0, t1 = 2010.0, 2027.0

    def X(t):
        return x0 + (t - t0) / (t1 - t0) * (x1 - x0)

    def Y(v):
        return plot_bot - (v - ymin) / (ymax - ymin) * PLOT_H

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-labelledby="t d">', STYLE,
         f"<title id=\"t\">{esc(title)}</title>", f"<desc id=\"d\">{esc(desc)}</desc>",
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="{SURF}"/>']
    y = 14
    for i, line in enumerate(title_lines):
        y += LINE
        o.append(f'<text x="{x0 - LEFT + 12}" y="{y}" font-size="17" font-weight="600" fill="{INK}">{esc(line)}</text>')
    o.append(f'<text x="12" y="{top}" font-size="14" fill="{INK3}">{esc(ylab)}</text>')
    # shaded last-five-years band
    o.append(f'<rect x="{X(t_shade):.1f}" y="{plot_top}" width="{X(t1) - X(t_shade):.1f}" height="{PLOT_H}" fill="{SHADE}"/>')
    o.append(f'<text x="{X(t_shade) + 4:.1f}" y="{plot_bot - 6}" font-size="14" fill="{INK3}">last 5 years</text>')
    for v in yticks:
        o.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="{1.2 if v == 0 else 0.6}"/>')
        lab = "0" if v == 0 else ("-" if v < 0 else "") + "{:,}".format(abs(v) // 1000) + "k"
        o.append(f'<text x="{x0 - 6}" y="{Y(v) + 5:.1f}" font-size="14" fill="{INK3}" text-anchor="end">{lab}</text>')
    for v in refs:
        o.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{INK3}" stroke-width="1" stroke-dasharray="4 3"/>')
    if ref_label:
        # on the axis-label line, right-aligned, clear of the plot
        o.append(f'<text x="{W - RIGHT}" y="{top}" font-size="14" fill="{INK3}" text-anchor="end">{esc(ref_label)}</text>')
        o.append(f'<line x1="{W - RIGHT - 272}" x2="{W - RIGHT - 248}" y1="{top - 5}" y2="{top - 5}" stroke="{INK3}" stroke-width="1" stroke-dasharray="4 3"/>')
    pts = " ".join(f"{X(t):.1f},{Y(v):.1f}" for t, v in series)
    o.append(f'<polyline points="{pts}" fill="none" stroke="{SUBJ}" stroke-width="1.4" stroke-linejoin="round"/>')
    for t, v in series:
        if v < 0:
            o.append(f'<circle cx="{X(t):.1f}" cy="{Y(v):.1f}" r="3" fill="{WARN}"/>')
    for yr in [2010, 2014, 2018, 2022, 2026]:
        o.append(f'<line x1="{X(yr):.1f}" x2="{X(yr):.1f}" y1="{plot_bot}" y2="{plot_bot + 5}" stroke="{INK3}" stroke-width="0.8"/>')
        o.append(f'<text x="{X(yr):.1f}" y="{plot_bot + 21}" font-size="14" fill="{INK3}" text-anchor="middle">{yr}</text>')
    y = axis_bot + 8
    for line in cap_lines:
        y += LINE
        o.append(f'<text x="12" y="{y}" font-size="14" fill="{INK3}">{esc(line)}</text>')
    o.append("</svg>")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(o) + "\n")


def main():
    os.makedirs(FIGS, exist_ok=True)
    F = facts()
    ex = rows("exercises.csv")
    s1 = [(t_of(r["month"], int(r["bidding_no"])), int(r["gap"])) for r in ex]
    start5 = ex[-120]
    t5 = t_of(start5["month"], int(start5["bidding_no"]))
    chart(os.path.join(FIGS, "lta_ab_chart1_gap.svg"),
          title=(f"Category B cleared a median ${F['gap_median_full']} above A from 2010, "
                 f"and ${F['gap_median_5y']} over the last five years"),
          desc=(f"Line chart, one point per COE bidding exercise from January 2010 to "
                f"{F['cutoff_label']}: Category B's premium minus Category A's. The median gap was "
                f"${F['gap_median_full']} over the {F['n_ex_full']} exercises and ${F['gap_median_5y']} over the "
                f"last {F['n_ex_5y']}. Category A cleared above B in {F['a_above_b_full']} exercises, "
                f"{F['a_above_b_2026']} of them in 2026. Dashed lines mark the steps between adjacent bands in "
                f"LTA's two examples, $7,500 and $15,000."),
          caption=["How to read: each point is one bidding exercise, Category B's premium minus "
                   "Category A's. Orange dots, below zero: A cleared above B. Dashed lines: the steps "
                   "between adjacent bands in LTA's examples (Option B $7,500, Option A $15,000). "
                   "Nominal dollars.",
                   f"Source: LTA via data.gov.sg, January 2010 to {F['cutoff_label']}."],
          series=s1, ymin=-20000, ymax=60000, yticks=[-20000, 0, 20000, 40000, 60000],
          refs=[7500, 15000], ref_label="LTA's band steps: $7,500, $15,000",
          t_shade=t5, ylab="B minus A, $")
    pq = rows("pqp_monthly.csv")
    s2 = [(t_of(r["month"], 1, 1), int(r["gap"])) for r in pq]
    chart(os.path.join(FIGS, "lta_ab_chart2_pqp.svg"),
          title=(f"Renewal prices for B and A were ${F['pqp_gap_oct2026']} apart in October 2026, "
                 f"against a five-year median of ${F['pqp_gap_median_5y']}"),
          desc=(f"Line chart, one point per month from January 2010 to October 2026: the Prevailing Quota "
                f"Premium for Category B minus that for Category A. The gap was ${F['pqp_gap_oct2026']} in "
                f"October 2026, a median ${F['pqp_gap_median_12m']} over the last 12 months, "
                f"${F['pqp_gap_median_5y']} over the last five years and ${F['pqp_gap_median_full']} from 2010."),
          caption=["How to read: each point is one month, the PQP that renewing Category B owners paid "
                   "minus the PQP for Category A. PQP is the average premium over the latest three "
                   "months with bidding (LTA). Below zero: A's PQP was higher. Nominal dollars.",
                   "Source: SingStat M651121 and LTA M11, January 2010 to October 2026."],
          series=s2, ymin=-10000, ymax=40000, yticks=[-10000, 0, 10000, 20000, 30000, 40000],
          refs=[], t_shade=t_of(pq[-60]["month"], 1, 1), ylab="B minus A, $")
    print("  wrote figs/lta_ab_chart1_gap.svg, figs/lta_ab_chart2_pqp.svg")


if __name__ == "__main__":
    main()
