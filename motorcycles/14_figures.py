"""
One figure for the motorcycle piece.

Design rules, same as the rest of the repository:
  * one axis, never two y-scales. A motorcycle premium is under $11,000 and a
    car premium is over $117,000, so plotting the dollars together would need
    two scales. Both series are indexed to 100 in 2022 instead, which is the
    year the motorcycle premium peaked.
  * the title is the finding and lives in the markdown, not inside the SVG
  * two series, so a key is present as well as direct end labels
  * emphasis: motorcycles are the subject and get the accent, cars are context
  * hairline solid gridlines, no dashes, no broken axes

Run after 13_motorcycles.py.  Output: figs/moto_vs_car.svg
"""
import pandas as pd
import os

os.makedirs("figs", exist_ok=True)
d = pd.read_csv("moto_vs_car.csv")

INK2 = "var(--fig-ink-2,#5b5e64)"
INK3 = "var(--fig-ink-3,#8d9096)"
RULE = "var(--fig-rule,#dfdeda)"
SUBJ = "var(--fig-subject,#a32a1e)"
CTX = "var(--fig-context,#8d9096)"

BASE = 2022
a = 100 * d.catA / float(d.loc[d.year == BASE, "catA"].iloc[0])
m = 100 * d.catD / float(d.loc[d.year == BASE, "catD"].iloc[0])

w, h = 660, 330
L, R, T, B = 54, 498, 58, 252
ymax = 180
X = lambda y: L + (R - L) * (y - d.year.min()) / (d.year.max() - d.year.min())
Y = lambda v: B - (B - T) * v / ymax

alt = (f"Line chart. Category A car premiums and Category D motorcycle premiums, both "
       f"indexed to 100 in {BASE}. By 2026 the car index reaches {a.iloc[-1]:.0f} and the "
       f"motorcycle index falls to {m.iloc[-1]:.0f}. The two lines separate after 2022. The "
       f"final point covers 15 exercises rather than a full year.")

s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
     f'aria-label="{alt}" font-family="IBM Plex Sans, system-ui, sans-serif">']
ad = s.append

ad(f'<g font-size="11.5"><rect x="{L}" y="18" width="9" height="9" rx="2" fill="{SUBJ}"/>'
   f'<text x="{L+15}" y="26.5" fill="{INK2}">motorcycles</text>'
   f'<rect x="{L+112}" y="18" width="9" height="9" rx="2" fill="{CTX}"/>'
   f'<text x="{L+127}" y="26.5" fill="{INK2}">smaller cars</text>'
   f'<text x="{L+228}" y="26.5" fill="{INK3}">both = 100 in {BASE}</text></g>')

for v in (20, 40, 60, 80, 100, 120, 140, 160):
    ad(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{R}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
    ad(f'<text x="{L-8}" y="{Y(v)+4:.1f}" text-anchor="end" font-size="10.5" fill="{INK3}" '
       f'font-variant-numeric="tabular-nums">{v}</text>')

# the base year, where both series are pinned
ad(f'<line x1="{X(BASE):.1f}" y1="{T-4}" x2="{X(BASE):.1f}" y2="{B}" stroke="{RULE}" stroke-width="1"/>')
ad(f'<text x="{X(BASE)+6:.1f}" y="{T+8}" font-size="10.5" fill="{INK3}">'
   f'motorcycle premiums peak</text>')

for y in d.year:
    ad(f'<text x="{X(y):.1f}" y="{B+19}" text-anchor="middle" font-size="10.5" fill="{INK3}">{y}</text>')

for series, col, wd in ((a, CTX, 1.9), (m, SUBJ, 2.5)):
    pts = " ".join(f"{X(y):.1f},{Y(v):.1f}" for y, v in zip(d.year, series))
    ad(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{wd}" '
       f'stroke-linejoin="round" stroke-linecap="round"/>')

last = d.year.max()
ad(f'<circle cx="{X(last):.1f}" cy="{Y(a.iloc[-1]):.1f}" r="4.5" fill="{CTX}"/>')
ad(f'<circle cx="{X(last):.1f}" cy="{Y(m.iloc[-1]):.1f}" r="4.5" fill="{SUBJ}"/>')
ad(f'<text x="{R+12}" y="{Y(a.iloc[-1])+1:.1f}" font-size="12.5" fill="{CTX}">'
   f'cars {a.iloc[-1]:.0f}</text>')
ad(f'<text x="{R+12}" y="{Y(a.iloc[-1])+16:.1f}" font-size="10.5" fill="{INK3}">2026 part year</text>')
ad(f'<text x="{R+12}" y="{Y(m.iloc[-1])+1:.1f}" font-size="12.5" fill="{SUBJ}" font-weight="600">'
   f'bikes {m.iloc[-1]:.0f}</text>')
ad(f'<text x="{R+12}" y="{Y(m.iloc[-1])+16:.1f}" font-size="10.5" fill="{INK3}">2026 part year</text>')

ad(f'<text x="{L}" y="{h-26}" font-size="11" fill="{INK3}">'
   f'Annual mean premiums, indexed to 100 in {BASE}. A full year holds 24 bidding '
   f'exercises.</text>')
ad(f'<text x="{L}" y="{h-11}" font-size="11" fill="{INK3}">'
   f'2026 has run 15, so the final point is a part year. Headline figures pool 2025 and '
   f'2026.</text>')
ad("</svg>")

with open("figs/moto_vs_car.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(s) + "\n")
print("  figs/moto_vs_car.svg")
print(f"  check: 2026 index, cars {a.iloc[-1]:.1f}, motorcycles {m.iloc[-1]:.1f}")
