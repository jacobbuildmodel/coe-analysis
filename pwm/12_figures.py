"""
12_figures.py -- the PWM piece's charts, from ROOT/out/ only.

Same rules as erp/12_figures.py: the shared --fig-* tokens with literal
fallbacks, a prefers-color-scheme block plus :root[data-theme="dark"], a
480-wide canvas, no text below 14px, hairline grids, LF line endings.

  figs/chart1_gap.svg     covered minus comparison, log points, every June,
                          one panel per group, windows marked (T1, T2)
  figs/chart2_rung.svg    25th-percentile basic wage over the entry rung,
                          post-period Junes, against the 0.97 line (T5)
  figs/chart3_pace.svg    comparison set against the middle, change from
                          the 2010-2012 mean, log points (T3)
"""
import math
import os

import pwmlib as L

INK = "var(--fig-ink,#0b0b0b)"
INK3 = "var(--fig-ink-3,#717171)"
RULE = "var(--fig-rule,#e2e1dd)"
SURF = "var(--fig-surface,#fcfcfa)"
SUBJ = "var(--fig-subject,#2873ce)"
CTX = "var(--fig-context,#707379)"
STYLE = ("<style>"
         ":root{--fig-ink:#0b0b0b;--fig-ink-3:#717171;--fig-rule:#e2e1dd;--fig-surface:#fcfcfa;"
         "--fig-subject:#2873ce;--fig-context:#707379;}"
         "@media (prefers-color-scheme: dark){:root{--fig-ink:#ffffff;--fig-ink-3:#9a9a9a;"
         "--fig-rule:#38393a;--fig-surface:#1a1a19;--fig-subject:#3987e5;--fig-context:#93969c;}}"
         ":root[data-theme=\"dark\"]{--fig-ink:#ffffff;--fig-ink-3:#9a9a9a;--fig-rule:#38393a;"
         "--fig-surface:#1a1a19;--fig-subject:#3987e5;--fig-context:#93969c;}"
         "text{font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;}"
         "</style>")
W = 480


def text(s, x, y, body, size=14, fill=INK3, anchor="start", weight=None):
    w = f' font-weight="{weight}"' if weight else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    s.append(f'<text x="{x:.1f}" y="{y:.1f}"{a} font-size="{size}" fill="{fill}"{w}>{body}</text>')


def head(H, alt, title):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{alt}">',
         STYLE, f'<rect x="0" y="0" width="{W}" height="{H}" fill="{SURF}"/>']
    text(s, 16, 28, title, 16, INK, weight="600")
    return s


def write(figs, name, parts):
    os.makedirs(figs, exist_ok=True)
    with open(os.path.join(figs, name), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(parts + ["</svg>"]) + "\n")
    print(f"  figs/{name}")


def nice(lo, hi):
    if lo == hi:
        lo, hi = lo - 1, hi + 1
    span = hi - lo
    step = 10 ** math.floor(math.log10(span / 3))
    for m in (1, 2, 5, 10):
        if span / (step * m) <= 4:
            step *= m
            break
    return math.floor(lo / step) * step, math.ceil(hi / step) * step, step


def panel(s, top, bottom, x0, x1, series, label, marks=(), hline=None, bands=()):
    """One panel: series is [(points {x: y}, colour, dashed)]."""
    Lx, Rx = 60, W - 24
    X = lambda v: Lx + (Rx - Lx) * (v - x0) / (x1 - x0)
    ys = [v for pts, _, _ in series for v in pts.values()] + ([hline] if hline is not None else [])
    if not ys:
        text(s, Lx, (top + bottom) / 2, f"{label}: no values", 14)
        return
    lo, hi, st = nice(min(ys), max(ys))
    Y = lambda v: bottom - (bottom - top) * (v - lo) / (hi - lo)
    for a, b in bands:
        s.append(f'<rect x="{X(a - 0.5):.1f}" y="{top}" width="{X(b + 0.5) - X(a - 0.5):.1f}" '
                 f'height="{bottom - top}" fill="{RULE}" opacity="0.5"/>')
    v = lo
    while v <= hi + 1e-9:
        s.append(f'<line x1="{Lx}" x2="{Rx}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, Lx - 6, Y(v) + 5, f"{v:g}", 14, anchor="end")
        v += st
    if hline is not None:
        s.append(f'<line x1="{Lx}" x2="{Rx}" y1="{Y(hline):.1f}" y2="{Y(hline):.1f}" stroke="{INK}" '
                 f'stroke-width="1" stroke-dasharray="4 3"/>')
    for pts, col, dashed in series:
        xs = sorted(pts)
        seg = []
        for x in xs:
            if seg and x - seg[-1] > 1:
                _poly(s, seg, pts, X, Y, col, dashed)
                seg = []
            seg.append(x)
        _poly(s, seg, pts, X, Y, col, dashed)
        for x in xs:
            s.append(f'<circle cx="{X(x):.1f}" cy="{Y(pts[x]):.1f}" r="2.5" fill="{col}"/>')
    text(s, Lx, top - 6, label, 14, INK)
    for x, lab in marks:
        text(s, X(x), bottom + 18, lab, 14, anchor="middle")


def _poly(s, seg, pts, X, Y, col, dashed):
    if len(seg) < 2:
        return
    d = " ".join(f"{X(x):.1f},{Y(pts[x]):.1f}" for x in seg)
    da = ' stroke-dasharray="5 4"' if dashed else ""
    s.append(f'<polyline points="{d}" fill="none" stroke="{col}" stroke-width="2"{da}/>')


def chart1(out, figs):
    gv = L.read_csv(os.path.join(out, "group_values.csv"))
    H = 560
    alt = ("Three panels, one per covered group: bottom pay in covered jobs minus the comparison "
           "jobs, in log points, every June 2009-2025. Shaded: the pre-period and post-period Junes.")
    s = head(H, alt, "Covered minus comparison jobs, log points")
    for k, g in enumerate(L.COVERED):
        pts = {int(r["june"]): 100 * float(r["gap"]) for r in gv if r["group"] == g and r["gap"]}
        top = 70 + k * 165
        bands = [(L.PRE[g][0], L.PRE[g][-1]), (L.POST[g][0], 2019), (2022, 2022)]
        panel(s, top, top + 110, 2008.5, 2025.5, [(pts, SUBJ, False)], g.capitalize(), bands=bands,
              marks=[(2009, "2009"), (2016, "2016"), (2022, "2022")] if k == 2 else ())
    write(figs, "chart1_gap.svg", s)


def chart2(out, figs):
    rows = L.read_csv(os.path.join(out, "t5_ratios.csv"))
    H = 560
    alt = ("Three panels: the 25th percentile of basic pay in each covered group, divided by the "
           "ladder's entry rung on 1 June, in each post-period June; dashed line at 0.97.")
    s = head(H, alt, "Bottom-quarter basic pay over the entry rung")
    for k, g in enumerate(L.COVERED):
        pts = {int(r["june"]): float(r["ratio"]) for r in rows if r["group"] == g}
        top = 70 + k * 165
        panel(s, top, top + 110, 2015.5, 2022.5, [(pts, SUBJ, False)], g.capitalize(), hline=L.T5_LINE,
              marks=[(2016, "2016"), (2019, "2019"), (2022, "2022")] if k == 2 else ())
    write(figs, "chart2_rung.svg", s)


def chart3(out, figs):
    gv = L.read_csv(os.path.join(out, "group_values.csv"))
    lfs = L.read_csv(os.path.join(out, "lfs_median.csv"))
    c = {int(r["june"]): float(r["value"]) for r in gv if r["group"] == "C"}
    m = {int(r["year"]): math.log(float(r["median_excl_emp_cpf"])) for r in lfs if r["median_excl_emp_cpf"]}
    base = lambda d: sum(d[j] for j in (2010, 2011, 2012) if j in d) / max(1, sum(1 for j in (2010, 2011, 2012) if j in d))
    cb, mb = base(c), base(m)
    cp = {j: 100 * (v - cb) for j, v in c.items() if 2009 <= j <= 2022}
    mp = {j: 100 * (v - mb) for j, v in m.items() if 2009 <= j <= 2022}
    H = 330
    alt = ("Comparison jobs' bottom pay (solid) and the median worker's income (dashed), change "
           "from the 2010-2012 mean in log points, 2009-2022.")
    s = head(H, alt, "Uncovered bottom against the middle")
    panel(s, 80, 270, 2008.5, 2022.5, [(cp, SUBJ, False), (mp, CTX, True)],
          "Solid: comparison jobs. Dashed: median.", bands=[(2010, 2012), (2017, 2019)],
          marks=[(2010, "2010"), (2017, "2017"), (2022, "2022")])
    write(figs, "chart3_pace.svg", s)


def main():
    a = L.args("PWM step 12: figures")
    P = L.paths(a.root)
    chart1(P["out"], P["figs"])
    chart2(P["out"], P["figs"])
    chart3(P["out"], P["figs"])


if __name__ == "__main__":
    main()
