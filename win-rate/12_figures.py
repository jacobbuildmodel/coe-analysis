"""
One figure for the win-rate piece.

Design rules, same as the parent repository:
  * one axis, never two y-scales. The premium is not plotted, because putting a
    dollar series and a percentage series on one chart would mean two scales and
    an invented correlation. The premium range is stated in the caption instead.
  * the title is the finding and lives in the markdown, not inside the SVG
  * emphasis rather than palette: one series, one colour
  * hairline solid gridlines, no dashes, no broken axes
  * colours come from CSS custom properties with literal fallbacks

Run after 11_winrate.py.  Output: figs/winrate.svg
"""
import pandas as pd
import os

os.makedirs("figs", exist_ok=True)
d = pd.read_csv("winrate_catA.csv")

INK2 = "var(--fig-ink-2,#5b5e64)"
INK3 = "var(--fig-ink-3,#8d9096)"
RULE = "var(--fig-rule,#dfdeda)"
SUBJ = "var(--fig-subject,#a32a1e)"
BAND = "var(--fig-context,#8d9096)"

w, h = 660, 320
L, R, T, B = 56, 512, 44, 248
lo, hi = 0, 100
X = lambda y: L + (R - L) * (y - 2010) / (2026 - 2010)
Y = lambda v: B - (B - T) * (v - lo) / (hi - lo)

rate = 100 * d.rate
mean = rate.mean()

alt = ("Line chart. The share of Category A COE bids that succeed, by year, from 2010 to "
       "2026. The line stays between 54 and 75 percent for the whole period, close to a flat "
       f"average of {mean:.0f} percent, while the premium over the same years moved by a "
       "factor of almost four.")

s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
     f'aria-label="{alt}" font-family="IBM Plex Sans, system-ui, sans-serif">']
ad = s.append

# gridlines
for v in (0, 25, 50, 75, 100):
    ad(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{R}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
    ad(f'<text x="{L-8}" y="{Y(v)+4:.1f}" text-anchor="end" font-size="10.5" fill="{INK3}" '
       f'font-variant-numeric="tabular-nums">{v}%</text>')

# the band the series actually occupies, so "flat" is visible rather than asserted
ad(f'<rect x="{L}" y="{Y(rate.max()):.1f}" width="{R-L}" '
   f'height="{Y(rate.min())-Y(rate.max()):.1f}" fill="{BAND}" opacity="0.13"/>')
ad(f'<text x="{R-6}" y="{Y(rate.max())-7:.1f}" text-anchor="end" font-size="10.5" fill="{INK3}">'
   f'every year sits inside this band</text>')

for y in (2010, 2014, 2018, 2022, 2026):
    ad(f'<text x="{X(y):.1f}" y="{B+19}" text-anchor="middle" font-size="10.5" fill="{INK3}">{y}</text>')

pts = " ".join(f"{X(y):.1f},{Y(v):.1f}" for y, v in zip(d.year, rate))
ad(f'<polyline points="{pts}" fill="none" stroke="{SUBJ}" stroke-width="2.4" '
   f'stroke-linejoin="round" stroke-linecap="round"/>')

last = rate.iloc[-1]
ad(f'<circle cx="{X(2026):.1f}" cy="{Y(last):.1f}" r="4.5" fill="{SUBJ}"/>')
ad(f'<text x="{R+12}" y="{Y(last)+1:.1f}" font-size="12.5" fill="{SUBJ}" font-weight="600">'
   f'{last:.0f}% in 2026</text>')
ad(f'<text x="{R+12}" y="{Y(last)+17:.1f}" font-size="10.5" fill="{INK3}">'
   f'{mean:.0f}% on average</text>')

ad(f'<text x="{L}" y="{h-26}" font-size="11" fill="{INK3}">'
   f'Share of Category A bids that succeeded, annual means of 24 bidding exercises.</text>')
ad(f'<text x="{L}" y="{h-11}" font-size="11" fill="{INK3}">'
   f'Over the same years the average premium ran from $29,907 to $117,548.</text>')
ad("</svg>")

with open("figs/winrate.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(s) + "\n")
print("  figs/winrate.svg")
print(f"  check: mean {mean:.1f}%, min {rate.min():.1f}%, max {rate.max():.1f}%, 2026 {last:.1f}%")
