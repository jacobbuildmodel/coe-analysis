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

Phase 3 (shared cross-repo figure tokens): same fixes as the parent repo's
09_figures.py -- a real <style> block added (there was none: every colour
referenced var(--fig-x, fallback) with nothing to ever redefine --fig-x for
dark mode, so this chart has always rendered light-only regardless of
theme), --fig-subject's fallback changed from red to the shared blue, and
font-family changed from the undeliverable "IBM Plex Sans" declaration to
the system-sans stack that was always actually rendering. Canvas shrunk
660x330 -> 480x270 and base text 10.5/11px -> 14px, measured 6.2px -> 11.4px
effective at 390px. Every label's wording is unchanged -- only position,
size and line-wrapping moved.

Run after 13_motorcycles.py.  Output: figs/moto_vs_car.svg
"""
import pandas as pd
import os

os.makedirs("figs", exist_ok=True)
d = pd.read_csv("moto_vs_car.csv")

INK2 = "var(--fig-ink-2,#52514e)"
INK3 = "var(--fig-ink-3,#717171)"
RULE = "var(--fig-rule,#e2e1dd)"
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

BASE = 2022
a = 100 * d.catA / float(d.loc[d.year == BASE, "catA"].iloc[0])
m = 100 * d.catD / float(d.loc[d.year == BASE, "catD"].iloc[0])

w, h = 480, 300
L, R, T, B = 44, 358, 40, 200
ymax = 180
X = lambda y: L + (R - L) * (y - d.year.min()) / (d.year.max() - d.year.min())
Y = lambda v: B - (B - T) * v / ymax

alt = (f"Line chart. Category A car premiums and Category D motorcycle premiums, both "
       f"indexed to 100 in {BASE}. By 2026 the car index reaches {a.iloc[-1]:.0f} and the "
       f"motorcycle index falls to {m.iloc[-1]:.0f}. The two lines separate after 2022. The "
       f"final point covers 15 exercises rather than a full year.")

s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
     f'aria-label="{alt}">', STYLE]
ad = s.append

ad(f'<g font-size="14"><rect x="{L}" y="14" width="10" height="10" rx="2" fill="{SUBJ}"/>'
   f'<text x="{L+16}" y="23" fill="{INK2}">motorcycles</text>'
   f'<rect x="{L+118}" y="14" width="10" height="10" rx="2" fill="{CTX}"/>'
   f'<text x="{L+134}" y="23" fill="{INK2}">smaller cars</text></g>')
ad(f'<text x="{L}" y="42" font-size="14" fill="{INK3}">both = 100 in {BASE}</text>')

for v in (20, 40, 60, 80, 100, 120, 140, 160):
    ad(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{R}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
    ad(f'<text x="{L-8}" y="{Y(v)+5:.1f}" text-anchor="end" font-size="14" fill="{INK3}" '
       f'font-variant-numeric="tabular-nums">{v}</text>')

# the base year, where both series are pinned
ad(f'<line x1="{X(BASE):.1f}" y1="{T-4}" x2="{X(BASE):.1f}" y2="{B}" stroke="{RULE}" stroke-width="1"/>')
ad(f'<text x="{X(BASE)+6:.1f}" y="{T+10}" font-size="14" fill="{INK3}">'
   f'motorcycle premiums peak</text>')

for y in d.year:
    ad(f'<text x="{X(y):.1f}" y="{B+20}" text-anchor="middle" font-size="14" fill="{INK3}">{y}</text>')

for series, col, wd in ((a, CTX, 2.0), (m, SUBJ, 2.6)):
    pts = " ".join(f"{X(y):.1f},{Y(v):.1f}" for y, v in zip(d.year, series))
    ad(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{wd}" '
       f'stroke-linejoin="round" stroke-linecap="round"/>')

last = d.year.max()
ad(f'<circle cx="{X(last):.1f}" cy="{Y(a.iloc[-1]):.1f}" r="4.5" fill="{CTX}"/>')
ad(f'<circle cx="{X(last):.1f}" cy="{Y(m.iloc[-1]):.1f}" r="4.5" fill="{SUBJ}"/>')
ad(f'<text x="{R+10}" y="{Y(a.iloc[-1])+2:.1f}" font-size="16" fill="{CTX}">'
   f'cars {a.iloc[-1]:.0f}</text>')
ad(f'<text x="{R+10}" y="{Y(a.iloc[-1])+19:.1f}" font-size="14" fill="{INK3}">2026 part year</text>')
ad(f'<text x="{R+10}" y="{Y(m.iloc[-1])+2:.1f}" font-size="16" fill="{SUBJ}" font-weight="600">'
   f'bikes {m.iloc[-1]:.0f}</text>')
ad(f'<text x="{R+10}" y="{Y(m.iloc[-1])+19:.1f}" font-size="14" fill="{INK3}">2026 part year</text>')

ad(f'<text x="{L}" y="{B+42}" font-size="14" fill="{INK3}">'
   f'Annual mean premiums, indexed to 100 in {BASE}. A full</text>')
ad(f'<text x="{L}" y="{B+58}" font-size="14" fill="{INK3}">'
   f'year holds 24 bidding exercises.</text>')
ad(f'<text x="{L}" y="{B+80}" font-size="14" fill="{INK3}">'
   f'2026 has run 15, so the final point is a part year.</text>')
ad(f'<text x="{L}" y="{B+96}" font-size="14" fill="{INK3}">'
   f'Headline figures pool 2025 and 2026.</text>')
ad("</svg>")

with open("figs/moto_vs_car.svg", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(s) + "\n")
print("  figs/moto_vs_car.svg")
print(f"  check: 2026 index, cars {a.iloc[-1]:.1f}, motorcycles {m.iloc[-1]:.1f}")
