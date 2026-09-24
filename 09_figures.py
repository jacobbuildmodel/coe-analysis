"""
Build the three figures for the COE piece as standalone, theme-aware SVG.

Rules applied (from the house style):
  * one axis, never two y-scales  -> both series indexed to 100 at 2010
  * the title is the finding; it lives in the markdown, not inside the SVG
  * direct labels at the line ends, plus a compact key, so identity is never
    carried by colour alone
  * emphasis rather than palette: the subject is coloured, the context is grey
  * hairline solid gridlines, no dashes, no broken axes
  * colours come from CSS custom properties with literal fallbacks, so the
    figures follow the site's light and dark themes

Phase 3 (shared cross-repo figure tokens): the --fig-* variable names below
already matched what hdb-affordability's 07_figures.py has now adopted too,
and what the website's own economics.css independently defines -- this
script did not need renaming. Two things did need fixing:

  1. No <style> block ever existed to actually REDEFINE these variables for
     dark mode -- every colour referenced var(--fig-x, fallback), but
     nothing in the SVG ever set --fig-x to anything else, so every chart
     silently rendered in light-mode colours regardless of theme. Confirmed
     empirically before this fix: zero "prefers-color-scheme" occurrences
     anywhere in this file. Fixed below with STYLE, matching the block
     hdb-affordability and gst-passthrough already carry.
  2. --fig-subject's fallback was #a32a1e (a red), while hdb-affordability
     and gst-passthrough both converged on blue. Changed to the shared
     --fig-subject blue so a reader moving between pieces sees one
     consistent "this is the finding" colour rather than three.

Font-family changed from "IBM Plex Sans, system-ui, sans-serif" (set at the
SVG root) to the system-sans stack the other two repos use. IBM Plex Sans
cannot actually load inside a standalone SVG opened via <img src> -- there
is no way to reach a Google Fonts stylesheet from an isolated embedded
document without inlining the font as base64, which would balloon every
figure and complicate byte-identical rebuilds -- so every reader has always
seen the system-sans fallback regardless of what the font-family attribute
claimed. Declaring what actually renders instead of what was hoped for.

All four figures redrawn this pass (canvas shrunk, base text raised to
14px) -- not just indexed, which was the Phase 3 proposal's one-chart demo.

Output: figs/*.svg
"""
import pandas as pd
import os

os.makedirs("figs", exist_ok=True)
d = pd.read_csv("analysis.csv")
a = d[d.cat == "A"].groupby("year").agg(q=("quota", "mean"), p=("premium", "mean"))
a = a.loc[2010:2026]

INK  = "var(--fig-ink,#0b0b0b)"
INK2 = "var(--fig-ink-2,#52514e)"
INK3 = "var(--fig-ink-3,#717171)"
RULE = "var(--fig-rule,#e2e1dd)"
SUBJ = "var(--fig-subject,#2873ce)"
CTX  = "var(--fig-context,#707379)"
SURF = "var(--fig-surface,#fcfcfa)"

# Shared cross-repo palette (Phase 3). Light values are the fallbacks
# above; dark values re-picked to clear WCAG AA 4.5:1 as text on
# --fig-surface #1a1a19, same methodology as hdb-affordability's
# 07_figures.py (see that file's docstring for the contrast ratios and the
# colour-vision-deficiency check on subject vs context).
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

HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        'role="img" aria-label="{alt}">')


def write(name, parts):
    with open(f"figs/{name}", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(parts) + "\n</svg>\n")
    print(f"  figs/{name}")


# ---------------------------------------------------------------- figure 1
# The mechanism. No data in it. The clearing points are computed from the
# curve equations so they sit exactly on the curves rather than near them.
# Phase 3: canvas 660x360 -> 480x280 (uniform 0.727 scale on every geometric
# constant, including the curve parameters X0/K/C/SHIFT, so the diagram's
# shape is preserved exactly -- font sizes raised separately, not scaled
# down with the geometry, which is the whole point).
def mechanism():
    w, h = 480, 310
    L, R, T, B = 64, 430, 26, 205
    X0, K, C = 43.6, 7367.0, 212.4          # demand 2010: y = C - K/(x - X0)
    SHIFT = 98.2                             # demand 2026 sits this far above it

    def d2010(x):
        return C - K / (x - X0)

    def d2026(x):
        return d2010(x) - SHIFT

    qa, qb = 160, 259                        # supply 2010, supply 2026 (+62%)
    ya = d2010(qa)                           # the 2010 clearing point
    yb_only = d2010(qb)                      # where extra supply alone would land
    yb = d2026(qb)                           # where it actually landed

    alt = ("Diagram of the mechanism. Supply is a vertical line because the quota is "
           "fixed before bidding opens. Between 2010 and 2026 that line moved right by "
           "62 percent, which on its own would have slid the price down the old demand "
           "curve to a lower point. The demand curve moved up and out by more than that, "
           "so the clearing price rose from about 30,000 dollars to about 118,000.")
    s = [HEAD.format(w=w, h=h, alt=alt), STYLE]
    ad = s.append

    ad(f'<g stroke="{INK}" stroke-width="1.2" fill="none">'
       f'<path d="M{L} {T} L{L} {B} L{R} {B}"/></g>')
    ad(f'<text x="{L-8}" y="{T+4}" text-anchor="end" font-size="14" fill="{INK2}">price</text>')
    ad(f'<text x="{L}" y="{B+18}" text-anchor="start" font-size="14" fill="{INK2}">certificates issued</text>')

    def curve(fn, x_from, colour, width, x_to=R - 2):
        pts = []
        x = x_from
        while x <= x_to:
            y = fn(x)
            if T + 4 <= y <= B - 2:
                pts.append(f"{x:.1f},{y:.1f}")
            x += 3
        return (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{colour}" '
                f'stroke-width="{width}" stroke-linecap="round"/>')

    # d2010's own label sits right after its curve, along the same line, so
    # the curve is stopped a little short of R here -- at the full R-2 it
    # ran straight through the "demand 2010" text, a strikethrough that
    # only showed up once actually rendered at this narrower canvas.
    ad(curve(d2010, 89, CTX, 1.9, x_to=R - 60))
    ad(curve(d2026, 135, SUBJ, 2.5))

    # supply lines
    ad(f'<line x1="{qa}" y1="{T+4}" x2="{qa}" y2="{B}" stroke="{CTX}" stroke-width="1.6"/>')
    ad(f'<line x1="{qb}" y1="{T+4}" x2="{qb}" y2="{B}" stroke="{INK}" stroke-width="2"/>')
    ad(f'<text x="{qa-7}" y="{B-10}" text-anchor="end" font-size="14" fill="{CTX}">supply 2010</text>')
    ad(f'<text x="{qb+8}" y="{T+17}" font-size="14" fill="{INK}" font-weight="600">supply 2026</text>')
    ad(f'<text x="{qb+8}" y="{T+33}" font-size="14" fill="{INK3}">quota +62%</text>')

    # curve labels, placed clear of the lines. The +18 offset from the
    # 660-wide original pushed this past B in the new, more compressed
    # geometry (the curve sits closer to the axis here) -- caught by
    # rendering it, not by the coordinate math. Capped so the label never
    # crosses B-2, the same bound the curve itself is clipped to.
    ad(f'<text x="{R-4}" y="{min(d2010(R-4)+18, B-8):.1f}" text-anchor="end" font-size="14" '
       f'fill="{CTX}">demand 2010</text>')
    ad(f'<text x="{R-4}" y="{d2026(R-4)-11:.1f}" text-anchor="end" font-size="14" '
       f'fill="{SUBJ}" font-weight="600">demand 2026</text>')

    # price guides
    for y, col, lab, weight in ((ya, CTX, "$30k", "400"), (yb, SUBJ, "$118k", "600")):
        ad(f'<line x1="{L}" y1="{y:.1f}" x2="{qa if col==CTX else qb}" y2="{y:.1f}" '
           f'stroke="{RULE}" stroke-width="1"/>')
        ad(f'<text x="{L-8}" y="{y+4:.1f}" text-anchor="end" font-size="14" fill="{col}" '
           f'font-weight="{weight}">{lab}</text>')

    # the three points
    ad(f'<circle cx="{qa}" cy="{ya:.1f}" r="5.5" fill="{SURF}" stroke="{CTX}" stroke-width="2.4"/>')
    ad(f'<circle cx="{qb}" cy="{yb_only:.1f}" r="4.5" fill="{SURF}" stroke="{INK3}" stroke-width="1.6"/>')
    ad(f'<circle cx="{qb}" cy="{yb:.1f}" r="6" fill="{SUBJ}"/>')

    ad(f'<defs><marker id="mk" markerWidth="8" markerHeight="8" refX="7" refY="4" '
       f'orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{INK3}"/></marker>'
       f'<marker id="mk2" markerWidth="8" markerHeight="8" refX="7" refY="4" '
       f'orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{SUBJ}"/></marker></defs>')
    # step 1: slide down the old curve
    ad(f'<path d="M{qa+6} {ya+5:.1f} Q {(qa+qb)/2} {ya+28:.1f} {qb-5} {yb_only-4:.1f}" '
       f'fill="none" stroke="{INK3}" stroke-width="1.2" marker-end="url(#mk)"/>')
    # step 2: the demand shift lifts it past where it started
    ad(f'<line x1="{qb}" y1="{yb_only-9:.1f}" x2="{qb}" y2="{yb+11:.1f}" '
       f'stroke="{SUBJ}" stroke-width="1.6" marker-end="url(#mk2)"/>')

    ad(f'<path d="M{qb+6} {yb_only-2:.1f} L{qb+22} {B-46}" fill="none" '
       f'stroke="{RULE}" stroke-width="1"/>')
    ad(f'<text x="{qb+20}" y="{B-58}" font-size="14" fill="{INK3}">'
       f'where the extra certificates</text>')
    ad(f'<text x="{qb+20}" y="{B-44}" font-size="14" fill="{INK3}">'
       f'alone would have left it</text>')

    ad(f'<text x="{L}" y="{B+42}" font-size="14" fill="{INK2}">'
       f'Supply is vertical, so the clearing price is a</text>')
    ad(f'<text x="{L}" y="{B+58}" font-size="14" fill="{INK2}">'
       f'point on the demand curve. Moving the line right</text>')
    ad(f'<text x="{L}" y="{B+74}" font-size="14" fill="{INK2}">'
       f'slides the price down. It went up instead, so the</text>')
    ad(f'<text x="{L}" y="{B+90}" font-size="14" fill="{INK2}">'
       f'curve must have moved further than the line.</text>')
    write("mechanism.svg", s)


# ---------------------------------------------------------------- figure 2
# Phase 3: canvas 660x350 -> 480x280, base text 10.5/11px -> 14px, matching
# the 480-wide/14px convention. Every label's wording is unchanged from
# before -- only position, size and line-wrapping moved.
def indexed():
    w, h = 480, 280
    L, R, T, B = 44, 344, 40, 220
    yrs = list(a.index)
    qi = 100 * a.q / a.q.loc[2010]
    pi = 100 * a.p / a.p.loc[2010]
    ymax = 420
    X = lambda y: L + (R - L) * (y - 2010) / (2026 - 2010)
    Y = lambda v: B - (B - T) * v / ymax
    alt = ("Line chart. Category A quota and premium, both indexed to 100 in 2010. By 2026 "
           "the quota index is 162 and the premium index is 387. The premium runs above the "
           "quota for the whole period, and the two move together only around 2013.")
    s = [HEAD.format(w=w, h=h, alt=alt), STYLE]
    ad = s.append

    ad(f'<g font-size="14"><rect x="{L}" y="14" width="10" height="10" rx="2" fill="{SUBJ}"/>'
       f'<text x="{L+16}" y="23" fill="{INK2}">premium</text>'
       f'<rect x="{L+92}" y="14" width="10" height="10" rx="2" fill="{CTX}"/>'
       f'<text x="{L+108}" y="23" fill="{INK2}">quota</text>'
       f'<text x="{L+165}" y="23" fill="{INK3}">both = 100 in 2010</text></g>')

    for v in (100, 200, 300, 400):
        ad(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{R}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
        ad(f'<text x="{L-8}" y="{Y(v)+5:.1f}" text-anchor="end" font-size="14" '
           f'fill="{INK3}" font-variant-numeric="tabular-nums">{v}</text>')
    ad(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{INK3}" stroke-width="1"/>')
    for y in (2010, 2015, 2020, 2026):
        ad(f'<text x="{X(y):.1f}" y="{B+22}" text-anchor="middle" font-size="14" fill="{INK3}">{y}</text>')

    for series, col, wd in ((qi, CTX, 2.0), (pi, SUBJ, 2.6)):
        pts = " ".join(f"{X(y):.1f},{Y(v):.1f}" for y, v in zip(yrs, series))
        ad(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{wd}" '
           f'stroke-linejoin="round" stroke-linecap="round"/>')

    ad(f'<circle cx="{X(2026):.1f}" cy="{Y(pi.loc[2026]):.1f}" r="4.5" fill="{SUBJ}"/>')
    ad(f'<circle cx="{X(2026):.1f}" cy="{Y(qi.loc[2026]):.1f}" r="4.5" fill="{CTX}"/>')
    ad(f'<text x="{R+10}" y="{Y(pi.loc[2026])+2:.1f}" font-size="16" fill="{SUBJ}" '
       f'font-weight="600">premium 387</text>')
    ad(f'<text x="{R+10}" y="{Y(pi.loc[2026])+19:.1f}" font-size="14" fill="{INK3}">up 287%</text>')
    ad(f'<text x="{R+10}" y="{Y(qi.loc[2026])+2:.1f}" font-size="16" fill="{CTX}">quota 162</text>')
    ad(f'<text x="{R+10}" y="{Y(qi.loc[2026])+19:.1f}" font-size="14" fill="{INK3}">up 62%</text>')

    ad(f'<line x1="{X(2013):.1f}" y1="{Y(300):.1f}" x2="{X(2013):.1f}" y2="{B}" '
       f'stroke="{RULE}" stroke-width="1"/>')
    ad(f'<text x="{X(2013)+7:.1f}" y="{Y(340):.1f}" font-size="14" fill="{INK3}">'
       f'2013: quota at its lowest,</text>')
    ad(f'<text x="{X(2013)+7:.1f}" y="{Y(340)+16:.1f}" font-size="14" fill="{INK3}">'
       f'premium near its peak</text>')

    ad(f'<text x="{L}" y="{h-24}" font-size="14" fill="{INK3}">'
       f'Annual means of 24 bidding exercises per year.</text>')
    ad(f'<text x="{L}" y="{h-8}" font-size="14" fill="{INK3}">'
       f'2026 covers 15 exercises to August.</text>')
    write("indexed.svg", s)


# ---------------------------------------------------------------- figure 3
# A number line rather than two bars. The scale gap is the point, so it is
# shown honestly on one axis instead of hidden behind a broken bar.
# Phase 3: canvas 660x210 -> 480x220, base text 10.5/11px -> 14px. Wording
# unchanged throughout -- only the bottom caption's line-wrap changed, to
# fit the narrower canvas.
def decomposition():
    w, h = 480, 220
    L, R, Y0 = 80, 434, 100
    lo, hi = -60.0, 300.0
    X = lambda v: L + (R - L) * (v - lo) / (hi - lo)
    alt = ("Number line. What the 62 percent quota increase alone predicts for the "
           "Category A premium is a fall of 13.6 percent, just left of zero. What actually "
           "happened is a rise of 287 percent, at the far right of the scale.")
    s = [HEAD.format(w=w, h=h, alt=alt), STYLE]
    ad = s.append

    ad(f'<line x1="{L}" y1="{Y0}" x2="{R}" y2="{Y0}" stroke="{RULE}" stroke-width="1.5"/>')
    for v in (-50, 0, 50, 100, 150, 200, 250, 300):
        ad(f'<line x1="{X(v):.1f}" y1="{Y0-4}" x2="{X(v):.1f}" y2="{Y0+4}" '
           f'stroke="{INK3}" stroke-width="1"/>')
        ad(f'<text x="{X(v):.1f}" y="{Y0+24}" text-anchor="middle" font-size="14" '
           f'fill="{INK3}" font-variant-numeric="tabular-nums">{v:+d}%</text>')

    # the span between the two, so the gap is a visible object
    ad(f'<line x1="{X(-13.6):.1f}" y1="{Y0-26}" x2="{X(287):.1f}" y2="{Y0-26}" '
       f'stroke="{RULE}" stroke-width="6" stroke-linecap="round"/>')

    ad(f'<circle cx="{X(-13.6):.1f}" cy="{Y0}" r="7" fill="{SURF}" stroke="{CTX}" stroke-width="2.6"/>')
    ad(f'<circle cx="{X(287):.1f}" cy="{Y0}" r="8.5" fill="{SUBJ}"/>')

    ad(f'<text x="{X(-13.6):.1f}" y="{Y0-46}" text-anchor="middle" font-size="16" '
       f'fill="{INK2}" font-weight="600">-13.6%</text>')
    ad(f'<text x="{X(-13.6):.1f}" y="{Y0-66}" text-anchor="middle" font-size="14" fill="{INK3}">'
       f'what the extra certificates predict</text>')

    ad(f'<text x="{X(287):.1f}" y="{Y0-46}" text-anchor="end" font-size="22" '
       f'fill="{SUBJ}" font-weight="700">+287%</text>')
    ad(f'<text x="{X(287):.1f}" y="{Y0-68}" text-anchor="end" font-size="14" fill="{INK3}">'
       f'what happened</text>')

    ad(f'<text x="{L}" y="{h-38}" font-size="14" fill="{INK3}">'
       f'Category A average premium, 2010 to 2026.</text>')
    ad(f'<text x="{L}" y="{h-22}" font-size="14" fill="{INK3}">'
       f'One axis and no break, so the distance between the</text>')
    ad(f'<text x="{L}" y="{h-6}" font-size="14" fill="{INK3}">'
       f'two dots is the finding.</text>')
    write("decomposition.svg", s)


print("building figures:")
mechanism()
indexed()
decomposition()
print(f"\n  check: quota index 2026 = {100*a.q.loc[2026]/a.q.loc[2010]:.0f}, "
      f"premium index 2026 = {100*a.p.loc[2026]/a.p.loc[2010]:.0f}")


# ---------------------------------------------------------------- figure 4
# For piece 2. A distribution, because the point is a shape: the mean gap is
# about 1% and the spread around it is seven times that, so a real effect is
# invisible in any single month.
# Phase 3: canvas 660x348 -> 480x270, base text 10.5/11px -> 14px. Wording
# unchanged.
def gap_distribution():
    w, h = 480, 305
    L, R, T, B = 41, 439, 40, 185
    wd = df_all.pivot_table(index=["cat", "month"], columns="bidding_no", values="ln_p")
    wd = wd.dropna().reset_index()
    g = 100 * (wd[wd.cat == "A"][2] - wd[wd.cat == "A"][1])
    mean, sd = g.mean(), g.std()

    lo, hi, step = -24, 24, 2
    edges = list(range(lo, hi + step, step))
    counts = [((g >= a) & (g < a + step)).sum() for a in edges[:-1]]
    cmax = max(counts)
    X = lambda v: L + (R - L) * (v - lo) / (hi - lo)
    Y = lambda n: B - (B - T) * n / (cmax * 1.15)

    alt = (f"Histogram of the gap between the two Category A bidding exercises of the same "
           f"month, in percent, across 196 months. The distribution is centred close to zero "
           f"with a mean of {mean:.2f} percent and a standard deviation of {sd:.1f} percent, "
           f"so the average difference is far smaller than the month-to-month spread.")
    s = [HEAD.format(w=w, h=h, alt=alt), STYLE]
    ad = s.append

    for n in range(0, cmax + 1, 10):
        ad(f'<line x1="{L}" y1="{Y(n):.1f}" x2="{R}" y2="{Y(n):.1f}" stroke="{RULE}" stroke-width="1"/>')
        ad(f'<text x="{L-8}" y="{Y(n)+5:.1f}" text-anchor="end" font-size="14" '
           f'fill="{INK3}" font-variant-numeric="tabular-nums">{n}</text>')

    bw = (R - L) / len(counts)
    for a, n in zip(edges[:-1], counts):
        if n == 0:
            continue
        ad(f'<rect x="{X(a)+1:.1f}" y="{Y(n):.1f}" width="{bw-2:.1f}" '
           f'height="{B-Y(n):.1f}" rx="2" fill="{CTX}" opacity="0.55"/>')

    ad(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{INK3}" stroke-width="1"/>')
    for v in range(lo, hi + 1, 8):
        ad(f'<text x="{X(v):.1f}" y="{B+20}" text-anchor="middle" font-size="14" '
           f'fill="{INK3}">{v:+d}%</text>')

    ad(f'<line x1="{X(mean):.1f}" y1="{T-6}" x2="{X(mean):.1f}" y2="{B}" '
       f'stroke="{SUBJ}" stroke-width="2"/>')
    ad(f'<text x="{X(mean)+7:.1f}" y="{T-10}" font-size="14" fill="{SUBJ}" font-weight="600">'
       f'mean {mean:+.2f}%</text>')

    ad(f'<line x1="{X(mean-sd):.1f}" y1="{B+38}" x2="{X(mean+sd):.1f}" y2="{B+38}" '
       f'stroke="{INK3}" stroke-width="2.5" stroke-linecap="round"/>')
    ad(f'<text x="{X(mean):.1f}" y="{B+58}" text-anchor="middle" font-size="14" fill="{INK2}">'
       f'one standard deviation, {sd:.1f}% either side</text>')

    ad(f'<text x="{L}" y="{B+80}" font-size="14" fill="{INK3}">'
       f'Category A, 196 complete months, January 2010 to July 2026.</text>')
    ad(f'<text x="{L}" y="{B+96}" font-size="14" fill="{INK3}">'
       f'Positive means the second exercise of the month</text>')
    ad(f'<text x="{L}" y="{B+112}" font-size="14" fill="{INK3}">'
       f'cleared higher.</text>')
    write("gap_distribution.svg", s)


df_all = d.copy()
gap_distribution()
