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

Output: figs/*.svg
"""
import pandas as pd
import os

os.makedirs("figs", exist_ok=True)
d = pd.read_csv("analysis.csv")
a = d[d.cat == "A"].groupby("year").agg(q=("quota", "mean"), p=("premium", "mean"))
a = a.loc[2010:2026]

INK  = "var(--fig-ink,#1a1c20)"
INK2 = "var(--fig-ink-2,#5b5e64)"
INK3 = "var(--fig-ink-3,#8d9096)"
RULE = "var(--fig-rule,#dfdeda)"
SUBJ = "var(--fig-subject,#a32a1e)"
CTX  = "var(--fig-context,#8d9096)"
SURF = "var(--fig-surface,#fbfaf8)"

HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        'role="img" aria-label="{alt}" font-family="IBM Plex Sans, system-ui, sans-serif">')


def write(name, parts):
    with open(f"figs/{name}", "w", encoding="utf-8") as f:
        f.write("\n".join(parts) + "\n</svg>\n")
    print(f"  figs/{name}")


# ---------------------------------------------------------------- figure 1
# The mechanism. No data in it. The clearing points are computed from the
# curve equations so they sit exactly on the curves rather than near them.
def mechanism():
    w, h = 660, 360
    L, R, T, B = 62, 606, 34, 286
    X0, K, C = 60.0, 13929.0, 292.06        # demand 2010: y = C - K/(x - X0)
    SHIFT = 135.0                            # demand 2026 sits this far above it

    def d2010(x):
        return C - K / (x - X0)

    def d2026(x):
        return d2010(x) - SHIFT

    qa, qb = 220, 356                        # supply 2010, supply 2026 (+62%)
    ya = d2010(qa)                           # the 2010 clearing point
    yb_only = d2010(qb)                      # where extra supply alone would land
    yb = d2026(qb)                           # where it actually landed

    alt = ("Diagram of the mechanism. Supply is a vertical line because the quota is "
           "fixed before bidding opens. Between 2010 and 2026 that line moved right by "
           "62 percent, which on its own would have slid the price down the old demand "
           "curve to a lower point. The demand curve moved up and out by more than that, "
           "so the clearing price rose from about 30,000 dollars to about 118,000.")
    s = [HEAD.format(w=w, h=h, alt=alt)]
    ad = s.append

    ad(f'<g stroke="{INK}" stroke-width="1.2" fill="none">'
       f'<path d="M{L} {T} L{L} {B} L{R} {B}"/></g>')
    ad(f'<text x="{L-8}" y="{T+4}" text-anchor="end" font-size="11.5" fill="{INK2}">price</text>')
    ad(f'<text x="{R}" y="{B+20}" text-anchor="end" font-size="11.5" fill="{INK2}">certificates issued</text>')

    def curve(fn, x_from, colour, width):
        pts = []
        x = x_from
        while x <= R - 2:
            y = fn(x)
            if T + 4 <= y <= B - 2:
                pts.append(f"{x:.1f},{y:.1f}")
            x += 4
        return (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{colour}" '
                f'stroke-width="{width}" stroke-linecap="round"/>')

    ad(curve(d2010, 122, CTX, 1.7))
    ad(curve(d2026, 186, SUBJ, 2.3))

    # supply lines
    ad(f'<line x1="{qa}" y1="{T+4}" x2="{qa}" y2="{B}" stroke="{CTX}" stroke-width="1.6"/>')
    ad(f'<line x1="{qb}" y1="{T+4}" x2="{qb}" y2="{B}" stroke="{INK}" stroke-width="2"/>')
    ad(f'<text x="{qa-7}" y="{B-10}" text-anchor="end" font-size="11" fill="{CTX}">supply 2010</text>')
    ad(f'<text x="{qb+8}" y="{T+16}" font-size="11" fill="{INK}" font-weight="600">supply 2026</text>')
    ad(f'<text x="{qb+8}" y="{T+30}" font-size="10.5" fill="{INK3}">quota +62%</text>')

    # curve labels, placed clear of the lines
    ad(f'<text x="{R-4}" y="{d2010(R-4)+16:.1f}" text-anchor="end" font-size="11" '
       f'fill="{CTX}">demand 2010</text>')
    ad(f'<text x="{R-4}" y="{d2026(R-4)-9:.1f}" text-anchor="end" font-size="11" '
       f'fill="{SUBJ}" font-weight="600">demand 2026</text>')

    # price guides
    for y, col, lab, weight in ((ya, CTX, "$30k", "400"), (yb, SUBJ, "$118k", "600")):
        ad(f'<line x1="{L}" y1="{y:.1f}" x2="{qa if col==CTX else qb}" y2="{y:.1f}" '
           f'stroke="{RULE}" stroke-width="1"/>')
        ad(f'<text x="{L-8}" y="{y+4:.1f}" text-anchor="end" font-size="11" fill="{col}" '
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
    ad(f'<path d="M{qa+7} {ya+5:.1f} Q {(qa+qb)/2} {ya+34:.1f} {qb-6} {yb_only-4:.1f}" '
       f'fill="none" stroke="{INK3}" stroke-width="1.2" marker-end="url(#mk)"/>')
    # step 2: the demand shift lifts it past where it started
    ad(f'<line x1="{qb}" y1="{yb_only-9:.1f}" x2="{qb}" y2="{yb+11:.1f}" '
       f'stroke="{SUBJ}" stroke-width="1.6" marker-end="url(#mk2)"/>')

    ad(f'<path d="M{qb+8} {yb_only-2:.1f} L{qb+30} 214" fill="none" '
       f'stroke="{RULE}" stroke-width="1"/>')
    ad(f'<text x="{qb+34}" y="200" font-size="10.5" fill="{INK3}">'
       f'where the extra certificates</text>')
    ad(f'<text x="{qb+34}" y="213" font-size="10.5" fill="{INK3}">'
       f'alone would have left it</text>')

    ad(f'<text x="{L}" y="{h-30}" font-size="11.5" fill="{INK2}">'
       f'Supply is vertical, so the clearing price is a point on the demand curve. '
       f'Moving the line right</text>')
    ad(f'<text x="{L}" y="{h-14}" font-size="11.5" fill="{INK2}">'
       f'slides the price down. It went up instead, so the curve must have moved further '
       f'than the line.</text>')
    write("mechanism.svg", s)


# ---------------------------------------------------------------- figure 2
def indexed():
    w, h = 660, 350
    L, R, T, B = 52, 500, 62, 278
    yrs = list(a.index)
    qi = 100 * a.q / a.q.loc[2010]
    pi = 100 * a.p / a.p.loc[2010]
    ymax = 420
    X = lambda y: L + (R - L) * (y - 2010) / (2026 - 2010)
    Y = lambda v: B - (B - T) * v / ymax
    alt = ("Line chart. Category A quota and premium, both indexed to 100 in 2010. By 2026 "
           "the quota index is 162 and the premium index is 387. The premium runs above the "
           "quota for the whole period, and the two move together only around 2013.")
    s = [HEAD.format(w=w, h=h, alt=alt)]
    ad = s.append

    ad(f'<g font-size="11.5"><rect x="{L}" y="18" width="9" height="9" rx="2" fill="{SUBJ}"/>'
       f'<text x="{L+15}" y="26.5" fill="{INK2}">premium</text>'
       f'<rect x="{L+92}" y="18" width="9" height="9" rx="2" fill="{CTX}"/>'
       f'<text x="{L+107}" y="26.5" fill="{INK2}">quota</text>'
       f'<text x="{L+165}" y="26.5" fill="{INK3}">both = 100 in 2010</text></g>')

    for v in (100, 200, 300, 400):
        ad(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{R}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
        ad(f'<text x="{L-8}" y="{Y(v)+4:.1f}" text-anchor="end" font-size="10.5" '
           f'fill="{INK3}" font-variant-numeric="tabular-nums">{v}</text>')
    ad(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{INK3}" stroke-width="1"/>')
    for y in (2010, 2014, 2018, 2022, 2026):
        ad(f'<text x="{X(y):.1f}" y="{B+18}" text-anchor="middle" font-size="10.5" fill="{INK3}">{y}</text>')

    for series, col, wd in ((qi, CTX, 1.8), (pi, SUBJ, 2.4)):
        pts = " ".join(f"{X(y):.1f},{Y(v):.1f}" for y, v in zip(yrs, series))
        ad(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{wd}" '
           f'stroke-linejoin="round" stroke-linecap="round"/>')

    ad(f'<circle cx="{X(2026):.1f}" cy="{Y(pi.loc[2026]):.1f}" r="4" fill="{SUBJ}"/>')
    ad(f'<circle cx="{X(2026):.1f}" cy="{Y(qi.loc[2026]):.1f}" r="4" fill="{CTX}"/>')
    ad(f'<text x="{R+11}" y="{Y(pi.loc[2026])+1:.1f}" font-size="12.5" fill="{SUBJ}" '
       f'font-weight="600">premium 387</text>')
    ad(f'<text x="{R+11}" y="{Y(pi.loc[2026])+16:.1f}" font-size="10.5" fill="{INK3}">up 287%</text>')
    ad(f'<text x="{R+11}" y="{Y(qi.loc[2026])+1:.1f}" font-size="12.5" fill="{CTX}">quota 162</text>')
    ad(f'<text x="{R+11}" y="{Y(qi.loc[2026])+16:.1f}" font-size="10.5" fill="{INK3}">up 62%</text>')

    ad(f'<line x1="{X(2013):.1f}" y1="{Y(300):.1f}" x2="{X(2013):.1f}" y2="{B}" '
       f'stroke="{RULE}" stroke-width="1"/>')
    ad(f'<text x="{X(2013)+7:.1f}" y="{Y(330):.1f}" font-size="10.5" fill="{INK3}">'
       f'2013: quota at its lowest,</text>')
    ad(f'<text x="{X(2013)+7:.1f}" y="{Y(330)+13:.1f}" font-size="10.5" fill="{INK3}">'
       f'premium near its peak</text>')

    ad(f'<text x="{L}" y="{h-14}" font-size="11" fill="{INK3}">'
       f'Annual means of 24 bidding exercises per year. 2026 covers 15 exercises to August.</text>')
    write("indexed.svg", s)


# ---------------------------------------------------------------- figure 3
# A number line rather than two bars. The scale gap is the point, so it is
# shown honestly on one axis instead of hidden behind a broken bar.
def decomposition():
    w, h = 660, 210
    L, R, Y0 = 96, 596, 108
    lo, hi = -60.0, 300.0
    X = lambda v: L + (R - L) * (v - lo) / (hi - lo)
    alt = ("Number line. What the 62 percent quota increase alone predicts for the "
           "Category A premium is a fall of 13.6 percent, just left of zero. What actually "
           "happened is a rise of 287 percent, at the far right of the scale.")
    s = [HEAD.format(w=w, h=h, alt=alt)]
    ad = s.append

    ad(f'<line x1="{L}" y1="{Y0}" x2="{R}" y2="{Y0}" stroke="{RULE}" stroke-width="1.5"/>')
    for v in (-50, 0, 50, 100, 150, 200, 250, 300):
        ad(f'<line x1="{X(v):.1f}" y1="{Y0-4}" x2="{X(v):.1f}" y2="{Y0+4}" '
           f'stroke="{INK3}" stroke-width="1"/>')
        ad(f'<text x="{X(v):.1f}" y="{Y0+22}" text-anchor="middle" font-size="10.5" '
           f'fill="{INK3}" font-variant-numeric="tabular-nums">{v:+d}%</text>')

    # the span between the two, so the gap is a visible object
    ad(f'<line x1="{X(-13.6):.1f}" y1="{Y0-26}" x2="{X(287):.1f}" y2="{Y0-26}" '
       f'stroke="{RULE}" stroke-width="6" stroke-linecap="round"/>')

    ad(f'<circle cx="{X(-13.6):.1f}" cy="{Y0}" r="7" fill="{SURF}" stroke="{CTX}" stroke-width="2.6"/>')
    ad(f'<circle cx="{X(287):.1f}" cy="{Y0}" r="8.5" fill="{SUBJ}"/>')

    ad(f'<text x="{X(-13.6):.1f}" y="{Y0-44}" text-anchor="middle" font-size="15" '
       f'fill="{INK2}" font-weight="600">-13.6%</text>')
    ad(f'<text x="{X(-13.6):.1f}" y="{Y0-62}" text-anchor="middle" font-size="11" fill="{INK3}">'
       f'what the extra certificates predict</text>')

    ad(f'<text x="{X(287):.1f}" y="{Y0-44}" text-anchor="end" font-size="21" '
       f'fill="{SUBJ}" font-weight="700">+287%</text>')
    ad(f'<text x="{X(287):.1f}" y="{Y0-64}" text-anchor="end" font-size="11" fill="{INK3}">'
       f'what happened</text>')

    ad(f'<text x="{L}" y="{h-30}" font-size="11" fill="{INK3}">'
       f'Category A average premium, 2010 to 2026.</text>')
    ad(f'<text x="{L}" y="{h-14}" font-size="11" fill="{INK3}">'
       f'One axis and no break, so the distance between the two dots is the finding.</text>')
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
def gap_distribution():
    w, h = 660, 348
    L, R, T, B = 56, 604, 44, 250
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
    s = [HEAD.format(w=w, h=h, alt=alt)]
    ad = s.append

    for n in range(0, cmax + 1, 10):
        ad(f'<line x1="{L}" y1="{Y(n):.1f}" x2="{R}" y2="{Y(n):.1f}" stroke="{RULE}" stroke-width="1"/>')
        ad(f'<text x="{L-8}" y="{Y(n)+4:.1f}" text-anchor="end" font-size="10.5" '
           f'fill="{INK3}" font-variant-numeric="tabular-nums">{n}</text>')

    bw = (R - L) / len(counts)
    for a, n in zip(edges[:-1], counts):
        if n == 0:
            continue
        ad(f'<rect x="{X(a)+1:.1f}" y="{Y(n):.1f}" width="{bw-2:.1f}" '
           f'height="{B-Y(n):.1f}" rx="2" fill="{CTX}" opacity="0.55"/>')

    ad(f'<line x1="{L}" y1="{B}" x2="{R}" y2="{B}" stroke="{INK3}" stroke-width="1"/>')
    for v in range(lo, hi + 1, 8):
        ad(f'<text x="{X(v):.1f}" y="{B+18}" text-anchor="middle" font-size="10.5" '
           f'fill="{INK3}">{v:+d}%</text>')

    ad(f'<line x1="{X(mean):.1f}" y1="{T-6}" x2="{X(mean):.1f}" y2="{B}" '
       f'stroke="{SUBJ}" stroke-width="2"/>')
    ad(f'<text x="{X(mean)+7:.1f}" y="{T-10}" font-size="12" fill="{SUBJ}" font-weight="600">'
       f'mean {mean:+.2f}%</text>')

    ad(f'<line x1="{X(mean-sd):.1f}" y1="{B+34}" x2="{X(mean+sd):.1f}" y2="{B+34}" '
       f'stroke="{INK3}" stroke-width="2.5" stroke-linecap="round"/>')
    ad(f'<text x="{X(mean):.1f}" y="{B+50}" text-anchor="middle" font-size="11" fill="{INK2}">'
       f'one standard deviation, {sd:.1f}% either side</text>')

    ad(f'<text x="{L}" y="{h-24}" font-size="11" fill="{INK3}">'
       f'Category A, 196 complete months, January 2010 to July 2026.</text>')
    ad(f'<text x="{L}" y="{h-9}" font-size="11" fill="{INK3}">'
       f'Positive means the second exercise of the month cleared higher.</text>')
    write("gap_distribution.svg", s)


df_all = d.copy()
gap_distribution()
