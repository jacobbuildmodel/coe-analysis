"""
12_figures.py -- the PWM piece's charts, from ROOT/out/ only.

Same rules as erp/12_figures.py: the shared --fig-* tokens with literal
fallbacks, a prefers-color-scheme block plus :root[data-theme="dark"], a
480-wide canvas, no text below 14px, hairline grids, LF line endings. Each
chart carries a caption that says how to read it, and a title that states
the finding, chosen by rule from the sealed outcomes in out/tests.csv (the
rules are written below, before any real value was opened).

  figs/pwm_chart1_gap.svg     the one that settles it: covered minus comparison,
                          log points, every June, one panel per covered
                          group; pre, transition, excluded and post years
                          shaded and labelled; dashed before and after
                          averages (T1, T2)
  figs/pwm_chart2_pace.svg    comparison jobs' bottom pay against the median,
                          change from the 2010-2012 mean (T3)
  figs/pwm_chart3_rung.svg    each scored group's bottom-quarter basic pay over its
                          entry rung, post-period Junes, against the 0.97 line
                          (T5); groups T1 dropped are named in one line


Presentation only: nothing here computes or changes a tested number
(THESIS_ADDENDUM.md, items 2, 3, 7 and 9). Visible text is for readers: per
cent (100 x (exp(x) - 1) of the log-point values in out/), no test labels.
"""
import math
import os
import textwrap

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
LX, RX = 60, W - 24
TITLE_CHARS, CAPTION_CHARS = 44, 54
LINE = 19


def text(s, x, y, body, size=14, fill=INK3, anchor="start", weight=None):
    w = f' font-weight="{weight}"' if weight else ""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    s.append(f'<text x="{x:.1f}" y="{y:.1f}"{a} font-size="{size}" fill="{fill}"{w}>{body}</text>')


def head(H, alt, title):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{alt}">',
         STYLE, f'<rect x="0" y="0" width="{W}" height="{H}" fill="{SURF}"/>']
    y = 28
    for line in textwrap.wrap(title, TITLE_CHARS):
        text(s, 16, y, line, 16, INK, weight="600")
        y += 21
    return s, y


def caption(s, y, body):
    for line in textwrap.wrap(body, CAPTION_CHARS):
        text(s, 16, y, line, 14, INK3)
        y += LINE
    return y


def caption_height(body):
    return LINE * len(textwrap.wrap(body, CAPTION_CHARS))


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


def scale(x0, x1):
    return lambda v: LX + (RX - LX) * (v - x0) / (x1 - x0)


def axes(s, top, bottom, ys, extra=()):
    lo, hi, st = nice(min(list(ys) + list(extra)), max(list(ys) + list(extra)))
    Y = lambda v: bottom - (bottom - top) * (v - lo) / (hi - lo)
    v = lo
    while v <= hi + 1e-9:
        s.append(f'<line x1="{LX}" x2="{RX}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, LX - 6, Y(v) + 5, f"{v:g}", 14, anchor="end")
        v += st
    return Y


def band(s, X, top, bottom, a, b, kind):
    x, w = X(a - 0.5), X(b + 0.5) - X(a - 0.5)
    if kind == "scored":
        s.append(f'<rect x="{x:.1f}" y="{top}" width="{w:.1f}" height="{bottom - top}" fill="{RULE}" opacity="0.9"/>')
    elif kind == "transition":
        s.append(f'<rect x="{x:.1f}" y="{top}" width="{w:.1f}" height="{bottom - top}" fill="{RULE}" opacity="0.35"/>')
    else:   # excluded
        s.append(f'<rect x="{x + 0.5:.1f}" y="{top + 0.5}" width="{w - 1:.1f}" height="{bottom - top - 1}" '
                 f'fill="none" stroke="{INK3}" stroke-width="1" stroke-dasharray="3 3"/>')


def line(s, pts, X, Y, col, dashed=False, dots=True, opacity=1.0):
    xs = sorted(pts)
    seg = []
    for x in xs + [None]:
        if x is None or (seg and x - seg[-1] > 1):
            if len(seg) > 1:
                d = " ".join(f"{X(v):.1f},{Y(pts[v]):.1f}" for v in seg)
                da = ' stroke-dasharray="5 4"' if dashed else ""
                op = f' stroke-opacity="{opacity}"' if opacity < 1 else ""
                s.append(f'<polyline points="{d}" fill="none" stroke="{col}" stroke-width="2"{da}{op}/>')
            seg = []
        if x is not None:
            seg.append(x)
    if dots:
        for x in xs:
            op = f' fill-opacity="{opacity}"' if opacity < 1 else ""
            s.append(f'<circle cx="{X(x):.1f}" cy="{Y(pts[x]):.1f}" r="2.5" fill="{col}"{op}/>')


def tests(out):
    return {r["key"]: r["value"] for r in L.read_csv(os.path.join(out, "tests.csv"))}


def num(T, k):
    try:
        return float(T[k])
    except (KeyError, ValueError):
        return None


WORKERS = {"cleaning": "cleaners", "security": "security guards", "landscape": "landscape workers"}


def names(groups, cap=True):
    g = [WORKERS[x] for x in L.COVERED if x in groups]
    if not g:
        return ""
    s = g[0] if len(g) == 1 else ", ".join(g[:-1]) + " and " + g[-1]
    return s[0].upper() + s[1:] if cap else s


def pct(x):
    return 100 * (math.exp(x) - 1)


# ------------------------------------------------------------------ chart 1
def title1(T):
    """The finding in plain words, by rule from the sealed outcomes."""
    passing = T.get("T1_groups_passing", "").split()
    if T["T1_outcome"] == "NOT SCORED" or not passing:
        return "Before the ladders, covered and comparison jobs were already drifting apart"
    p = pct(num(T, "T2_pooled"))
    failed = [g for g in L.COVERED if g not in passing]
    if T["T2_outcome"] == "SURVIVE" and failed:
        return (f"{names(passing)}' pay pulled about {p:.0f} per cent ahead once the ladder "
                f"bound. For {names(failed, False)}, pay was already moving before it")
    if T["T2_outcome"] == "SURVIVE":
        return f"After the ladders, bottom pay in covered jobs pulled about {p:.0f} per cent ahead"
    if T["T2_outcome"] == "INCONCLUSIVE":
        return f"Covered jobs' bottom pay pulled only about {p:.0f} per cent ahead"
    below = [g for g in passing if (num(T, f"T2_{g}_est") or 0) <= 0]
    if below:
        return f"Bottom pay did not pull ahead for {names(below, False)}"
    return f"Bottom pay in covered jobs pulled only about {p:.0f} per cent ahead"


def chart1(out, figs):
    T = tests(out)
    gv = L.read_csv(os.path.join(out, "group_values.csv"))
    passing = T.get("T1_groups_passing", "").split()
    cap = ("Each panel is one covered job: how far its pay at the one-in-four mark (the 25th "
           "percentile of gross pay: a quarter of workers earned this or less) sat above or "
           "below the same mark in jobs with no ladder, in per cent, one dot per June. Dark "
           "bands: the years compared, before and after the ladder. Pale band: the transition, "
           "left out. Dashed box: 2020-21, left out. Dashed lines: the before and after "
           "averages; look for the step between the dark bands. Grey panels failed the design "
           "test: pay was already moving before the ladder, so their step is not read.")
    title = title1(T)
    top0 = 40 + 21 * len(textwrap.wrap(title, TITLE_CHARS))
    block = 188
    H = top0 + 3 * block + 26 + caption_height(cap) + 10
    alt = ("Three panels, one per covered job, showing bottom pay in covered jobs compared "
           "with jobs that had no ladder, in per cent, each June 2009-2025, with the before, "
           "transition, 2020-21 and after years shaded. " + title + ".")
    s, _ = head(H, alt, title)
    X = scale(2008.5, 2025.5)
    for k, g in enumerate(L.COVERED):
        top = top0 + 60 + k * block
        bottom = top + 110
        pts = {int(r["june"]): pct(float(r["gap"])) for r in gv if r["group"] == g and r["gap"]}
        logs = {int(r["june"]): float(r["gap"]) for r in gv if r["group"] == g and r["gap"]}
        ok = g in passing
        label = WORKERS[g].capitalize() + ("" if ok else ": failed the design test: step not read")
        text(s, 16, top - 42, label, 14, INK if ok else INK3, weight="600")
        post = L.POST[g]
        for a, b, kind, lab, row in ((L.PRE[g][0], L.PRE[g][-1], "scored", "before", 22),
                                     (L.TRANSITION[g][0], L.TRANSITION[g][-1], "transition", "transition", 6),
                                     (post[0], 2019, "scored", "after", 22),
                                     (2020, 2021, "excluded", "2020-21 excluded", 6),
                                     (2022, 2022, "scored", None, 0)):
            band(s, X, top, bottom, a, b, kind)
            if lab:
                text(s, X((a + b) / 2), top - row, lab, 14, INK3, anchor="middle")
        if not pts:
            text(s, LX + 8, (top + bottom) / 2, "no values", 14)
            continue
        Y = axes(s, top, bottom, pts.values())
        if not ok:          # failed the design test: muted, no before and after averages
            line(s, pts, X, Y, CTX, opacity=0.6)
            continue
        for yrs in (L.PRE[g], post):
            v = [logs[j] for j in yrs if j in logs]
            if v:
                m = pct(sum(v) / len(v))
                s.append(f'<line x1="{X(yrs[0] - 0.4):.1f}" x2="{X(yrs[-1] + 0.4):.1f}" y1="{Y(m):.1f}" '
                         f'y2="{Y(m):.1f}" stroke="{CTX}" stroke-width="1.5" stroke-dasharray="5 4"/>')
        line(s, pts, X, Y, SUBJ)
    base = top0 + 60 + 2 * block + 110
    for y in (2009, 2014, 2019, 2025):
        text(s, X(y), base + 18, str(y), 14, anchor="middle")
    caption(s, base + 44, cap)
    write(figs, "pwm_chart1_gap.svg", s)


# ------------------------------------------------------------------ chart 2
def title2(T):
    if T["T3_outcome"] == "NOT SCORED":
        return "Too few years to say whether jobs without a ladder kept pace"
    x = num(T, "T3_shortfall")
    if x <= 0:
        return "Jobs without a ladder kept pace with the median, and more"
    verb = "fell behind" if T["T3_outcome"] == "FAIL" else "kept pace"
    return f"Jobs without a ladder {verb}: their bottom pay grew {pct(x):.1f} per cent less than the median"


def chart2(out, figs):
    T = tests(out)
    gv = L.read_csv(os.path.join(out, "group_values.csv"))
    lfs = L.read_csv(os.path.join(out, "lfs_median.csv"))
    c = {int(r["june"]): float(r["value"]) for r in gv if r["group"] == "C"}
    m = {int(r["year"]): math.log(float(r["median_excl_emp_cpf"])) for r in lfs if r["median_excl_emp_cpf"]}
    start = (2010, 2011, 2012)

    def base(d):
        v = [d[j] for j in start if j in d]
        return sum(v) / len(v) if v else None

    cb, mb = base(c), base(m)
    cp = {j: pct(v - cb) for j, v in c.items() if 2009 <= j <= 2019} if cb is not None else {}
    mp = {j: pct(v - mb) for j, v in m.items() if 2009 <= j <= 2019} if mb is not None else {}
    cap = ("Blue line: pay at the one-in-four mark (the 25th percentile of gross pay) in the "
           "jobs that had no ladder until 2022. Grey dashed line: the median worker's income. Both show the "
           "change from their 2010-12 average, in per cent. Shaded: the start (2010-12) and end "
           "(2017-19) years compared. A blue line that ends below the grey one fell behind; the "
           "bet failed if the gap at the end reached about 5 per cent.")
    title = title2(T)
    top = 40 + 21 * len(textwrap.wrap(title, TITLE_CHARS)) + 30
    bottom = top + 200
    H = bottom + 26 + caption_height(cap) + 30
    alt = ("Line chart, 2009-2019: bottom pay in jobs without a ladder and the median income, "
           "both as the change from their 2010-12 average, in per cent. " + title + ".")
    s, _ = head(H, alt, title)
    X = scale(2008.5, 2019.5)
    for a, b, lab in ((2010, 2012, "start"), (2017, 2019, "end")):
        band(s, X, top, bottom, a, b, "scored")
        text(s, X((a + b) / 2), top - 6, lab, 14, INK3, anchor="middle")
    if cp or mp:
        Y = axes(s, top, bottom, list(cp.values()) + list(mp.values()))
        line(s, mp, X, Y, CTX, dashed=True)
        line(s, cp, X, Y, SUBJ)
    else:
        text(s, LX + 8, (top + bottom) / 2, "no values", 14)
    for y in (2009, 2012, 2017, 2019):
        text(s, X(y), bottom + 18, str(y), 14, anchor="middle")
    caption(s, bottom + 46, cap)
    write(figs, "pwm_chart2_pace.svg", s)


# ------------------------------------------------------------------ chart 3
def title3(T):
    if T["T5_outcome"] == "NOT SCORED":
        return "No covered job could be checked against its entry rung"
    groups = T.get("T2_groups_scored", "").split()
    rows = {k: num(T, k) for k in T if k.startswith("T5_") and k.endswith("_ratio") and k != "T5_min_ratio"}
    mine = {k: v for k, v in rows.items() if any(k.startswith(f"T5_{g}_") for g in groups)}
    at = sum(1 for v in mine.values() if v is not None and abs(v - 1) < 0.0005)
    low = [g for g in groups if any(v is not None and v < L.T5_LINE for k, v in rows.items()
                                    if k.startswith(f"T5_{g}_"))]
    if T["T5_outcome"] == "SURVIVE" and at:
        return (f"{names(groups)}: at the one-in-four mark, pay sat exactly on the entry rung "
                f"in {at} of {len(mine)} years")
    if T["T5_outcome"] == "SURVIVE":
        return f"{names(groups)}: at the one-in-four mark, pay was at least the entry rung every year"
    if low:
        return f"At the one-in-four mark, pay fell below the entry rung for {names(low, False)}"
    return "The entry rung could not be shown in every year"


def chart3(out, figs):
    T = tests(out)
    rows = L.read_csv(os.path.join(out, "t5_ratios.csv"))
    scored = T.get("T2_groups_scored", "").split()
    cap = ("Each panel is one covered job: its basic pay at the one-in-four mark (the 25th "
           "percentile: a quarter of workers earned this or less), as a share of the ladder's "
           "entry rung in force on 1 June, one dot per year compared. "
           "Solid line: 100 per cent, pay exactly at the rung. Dashed line: 97 per cent; a dot "
           "below it would have failed the bet.")
    title = title3(T)
    top0 = 40 + 21 * len(textwrap.wrap(title, TITLE_CHARS))
    shown = [g for g in L.COVERED if g in scored]
    others = [g for g in L.COVERED if g not in scored]
    note = f"{names(others)}: not checked (failed the design test)." if others else ""
    if note:
        top0 += 14 + LINE * len(textwrap.wrap(note, CAPTION_CHARS))
    block = 150
    n = max(1, len(shown))
    H = top0 + n * block + 26 + caption_height(cap) + 20
    alt = ("Basic pay at the one-in-four mark as a share of the entry rung, each year compared, against "
           "lines at 100 and 97 per cent. " + title + ".")
    s, y = head(H, alt, title)
    if note:
        caption(s, y + 10, note)
    X = scale(2015.5, 2022.5)
    for k, g in enumerate(shown):
        top = top0 + 34 + k * block
        bottom = top + 100
        pts = {int(r["june"]): 100 * float(r["ratio"]) for r in rows if r["group"] == g}
        text(s, LX, top - 12, WORKERS[g].capitalize(), 14, INK, weight="600")
        if not pts:
            text(s, LX + 8, (top + bottom) / 2, "no values", 14)
            continue
        Y = axes(s, top, bottom, pts.values(), extra=(100 * L.T5_LINE, 100.0))
        s.append(f'<line x1="{LX}" x2="{RX}" y1="{Y(100 * L.T5_LINE):.1f}" y2="{Y(100 * L.T5_LINE):.1f}" '
                 f'stroke="{INK}" stroke-width="1" stroke-dasharray="4 3"/>')
        s.append(f'<line x1="{LX}" x2="{RX}" y1="{Y(100.0):.1f}" y2="{Y(100.0):.1f}" stroke="{CTX}" stroke-width="1"/>')
        line(s, pts, X, Y, SUBJ)
    base = top0 + 34 + (n - 1) * block + 100
    for yr in (2016, 2019, 2022):
        text(s, X(yr), base + 18, str(yr), 14, anchor="middle")
    caption(s, base + 44, cap)
    write(figs, "pwm_chart3_rung.svg", s)


def main():
    a = L.args("PWM step 12: figures")
    P = L.paths(a.root)
    chart1(P["out"], P["figs"])
    chart2(P["out"], P["figs"])
    chart3(P["out"], P["figs"])


if __name__ == "__main__":
    main()
