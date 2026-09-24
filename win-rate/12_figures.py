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

Phase 3 (shared cross-repo figure tokens): same fixes as the parent repo's
09_figures.py -- a real <style> block added (there was none, so this chart
has always rendered light-only regardless of theme), --fig-subject's
fallback changed from red to the shared blue, and font-family changed from
the undeliverable "IBM Plex Sans" declaration to the system-sans stack that
was always actually rendering. Canvas shrunk 660x320 -> 480x270 and base
text 10.5/11px -> 14px, measured 6.2px -> 11.4px effective at 390px. Every
label's wording is unchanged -- only position, size and line-wrapping moved.

Run after 11_winrate.py.  Output: figs/winrate.svg
"""
import pandas as pd
import os

os.makedirs("figs", exist_ok=True)
d = pd.read_csv("winrate_catA.csv")

INK2 = "var(--fig-ink-2,#52514e)"
INK3 = "var(--fig-ink-3,#717171)"
RULE = "var(--fig-rule,#e2e1dd)"
SUBJ = "var(--fig-subject,#2873ce)"
BAND = "var(--fig-context,#707379)"

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

w, h = 480, 310
L, R, T, B = 54, 350, 32, 200
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
     f'aria-label="{alt}">', STYLE]
ad = s.append

# gridlines
for v in (0, 25, 50, 75, 100):
    ad(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{R}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
    ad(f'<text x="{L-8}" y="{Y(v)+5:.1f}" text-anchor="end" font-size="14" fill="{INK3}" '
       f'font-variant-numeric="tabular-nums">{v}%</text>')

# the band the series actually occupies, so "flat" is visible rather than asserted
ad(f'<rect x="{L}" y="{Y(rate.max()):.1f}" width="{R-L}" '
   f'height="{Y(rate.min())-Y(rate.max()):.1f}" fill="{BAND}" opacity="0.13"/>')
ad(f'<text x="{R-6}" y="{Y(rate.max())-9:.1f}" text-anchor="end" font-size="14" fill="{INK3}">'
   f'every year sits inside this band</text>')

for y in (2010, 2015, 2020, 2026):
    ad(f'<text x="{X(y):.1f}" y="{B+20}" text-anchor="middle" font-size="14" fill="{INK3}">{y}</text>')

pts = " ".join(f"{X(y):.1f},{Y(v):.1f}" for y, v in zip(d.year, rate))
ad(f'<polyline points="{pts}" fill="none" stroke="{SUBJ}" stroke-width="2.6" '
   f'stroke-linejoin="round" stroke-linecap="round"/>')

last = rate.iloc[-1]
ad(f'<circle cx="{X(2026):.1f}" cy="{Y(last):.1f}" r="4.5" fill="{SUBJ}"/>')
ad(f'<text x="{R+10}" y="{Y(last)+2:.1f}" font-size="16" fill="{SUBJ}" font-weight="600">'
   f'{last:.0f}% in 2026</text>')
ad(f'<text x="{R+10}" y="{Y(last)+19:.1f}" font-size="14" fill="{INK3}">'
   f'{mean:.0f}% on average</text>')

ad(f'<text x="{L}" y="{B+42}" font-size="14" fill="{INK3}">'
   f'Share of Category A bids that succeeded, annual</text>')
ad(f'<text x="{L}" y="{B+58}" font-size="14" fill="{INK3}">'
   f'means of 24 bidding exercises.</text>')
ad(f'<text x="{L}" y="{B+80}" font-size="14" fill="{INK3}">'
   f'Over the same years the average premium ran from</text>')
ad(f'<text x="{L}" y="{B+96}" font-size="14" fill="{INK3}">'
   f'$29,907 to $117,548.</text>')
ad("</svg>")

with open("figs/winrate.svg", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(s) + "\n")
print("  figs/winrate.svg")
print(f"  check: mean {mean:.1f}%, min {rate.min():.1f}%, max {rate.max():.1f}%, 2026 {last:.1f}%")
