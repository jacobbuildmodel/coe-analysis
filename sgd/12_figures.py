"""
12_figures.py -- the sgd piece's charts, from ROOT/out/ only.

Same rules as pwm/12_figures.py: the shared --fig-* tokens with literal
fallbacks, a prefers-color-scheme block plus :root[data-theme="dark"], a
480-wide canvas, no text below 14px, hairline grids, LF line endings. Titles
describe what is drawn; they state no finding (reader titles come at
Checkpoint 2, after the results).

  figs/sgd_chart1_split.svg   the Singapore dollar's rise against the yen and
                              the ringgit, January 2021 to December 2025,
                              split three ways in per cent of the rise
                              (T2, T3)
  figs/sgd_chart2_steady.svg  month-to-month swing of each currency's broad
                              index, August 2005 on, steadiest first (T4)
  figs/sgd_chart3_path.svg    the Singapore dollar's broad index from 2001,
                              with a tick at each MAS decision, raised for a
                              tighter score and lowered for a looser one (T7)

Presentation only: nothing here computes or changes a tested number.
"""
import math
import os
import textwrap

import sgdlib as L

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
TITLE_CHARS, CAPTION_CHARS = 44, 54
LINE = 19
NAMES = {"SG": "Singapore dollar", "JP": "Japanese yen", "MY": "Malaysian ringgit", "KR": "Korean won",
         "CN": "Chinese renminbi", "TH": "Thai baht", "ID": "Indonesian rupiah", "US": "US dollar",
         "XM": "Euro", "AU": "Australian dollar", "HK": "Hong Kong dollar"}


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


def num(T, k):
    try:
        return float(T[k])
    except (KeyError, ValueError, TypeError):
        return None


def chart1(T, figs):
    cap = ("Each bar is a share of the Singapore dollar's rise against that currency, January 2021 to "
           "December 2025, in per cent: the Singapore dollar rising against all its trading partners, "
           "that currency falling against all of its own, or neither. The three add to 100.")
    rows = []
    for t, cur, name in (("T2", "JPY", "yen"), ("T3", "MYR", "ringgit")):
        vals = [num(T, f"{t}_{k}") for k in ("S", "P", "R")]
        rows.append((name, vals))
    allv = [100 * v for _, vs in rows for v in vs if v is not None] + [0, 100]
    lo, hi, st = nice(min(allv), max(allv))
    LX, RX = 190, W - 24
    X = lambda v: LX + (RX - LX) * (v - lo) / (hi - lo)
    labels = ("Singapore dollar rose", "{0} fell", "neither index")
    H0 = 92
    H = H0 + 2 * (3 * 26 + 34) + 40 + caption_height(cap) + 12
    s, y = head(H, "Split of the Singapore dollar's rise against the yen and the ringgit",
                "Where the Singapore dollar's rise against the yen and the ringgit came from")
    top = y + 14
    bottom = top + 2 * (3 * 26 + 34)
    v = lo
    while v <= hi + 1e-9:
        s.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{top}" y2="{bottom}" stroke="{RULE}" stroke-width="1"/>')
        text(s, X(v), bottom + 18, f"{v:g}", 14, anchor="middle")
        v += st
    yy = top
    for name, vals in rows:
        text(s, 16, yy + 16, f"Against the {name}", 14, INK, weight="600")
        yy += 26
        if vals[0] is None:
            text(s, LX, yy + 12, "did not rise over these years", 14, INK3)
            yy += 3 * 26 + 8 - 26
            continue
        for lab, val, fill in zip(labels, vals, (SUBJ, CTX, RULE)):
            text(s, LX - 8, yy + 13, lab.format(name), 14, INK3, anchor="end")
            x0, x1 = X(0), X(100 * val)
            s.append(f'<rect x="{min(x0, x1):.1f}" y="{yy:.1f}" width="{abs(x1 - x0):.1f}" height="17" fill="{fill}"/>')
            yy += 26
        yy += 8
    caption(s, bottom + 44, cap)
    write(figs, "sgd_chart1_split.svg", s)


def chart2(T, figs):
    vols = sorted(((100 * float(v), k.split("_")[1]) for k, v in T.items()
                   if k.startswith("T4_") and k.endswith("_sd") and v not in ("", None)))
    cap = ("Typical month-to-month move of each currency's broad index against its trading partners, "
           "August 2005 on, in per cent. Shorter is steadier.")
    H = 70 + 24 * len(vols) + 40 + caption_height(cap) + 12
    s, y = head(H, "Month-to-month swing of eleven currencies' broad indices",
                "How much each currency's broad index swings from month to month")
    LX, RX = 170, W - 24
    hi = nice(0, max([v for v, _ in vols] + [0.1]))[1]
    X = lambda v: LX + (RX - LX) * v / hi
    top = y + 10
    for i, (v, a) in enumerate(vols):
        yy = top + 24 * i
        fill = SUBJ if a == "SG" else CTX
        text(s, LX - 8, yy + 14, NAMES.get(a, a), 14, INK if a == "SG" else INK3, anchor="end",
             weight="600" if a == "SG" else None)
        s.append(f'<rect x="{LX}" y="{yy + 2:.1f}" width="{X(v) - LX:.1f}" height="16" fill="{fill}"/>')
    bottom = top + 24 * len(vols)
    s.append(f'<line x1="{LX}" x2="{RX}" y1="{bottom}" y2="{bottom}" stroke="{RULE}" stroke-width="1"/>')
    text(s, LX, bottom + 18, "0", 14, anchor="middle")
    text(s, RX, bottom + 18, f"{hi:g}", 14, anchor="middle")
    caption(s, bottom + 44, cap)
    write(figs, "sgd_chart2_steady.svg", s)


def chart3(out, figs):
    neer = {r["period"]: float(r["value"]) for r in L.read_csv(os.path.join(out, "neer.csv")) if r["area"] == "SG"}
    mps = L.read_csv(os.path.join(out, "mps.csv"))
    first = "2001-01"
    ps = [p for p in sorted(neer) if p >= first]
    base = neer[ps[0]]
    ys = [100 * neer[p] / base for p in ps]
    cap = ("The Singapore dollar's broad index, January 2001 = 100. Each tick is a MAS decision: above "
           "the line for a tighter score, below for a looser one, on the line for no change.")
    H = 70 + 220 + 40 + caption_height(cap) + 12
    s, y = head(H, "The Singapore dollar's broad index and MAS's decisions",
                "The Singapore dollar's broad index and MAS's decisions")
    LX, RX = 60, W - 24
    top, bottom = y + 10, y + 210
    lo, hi, st = nice(min(ys), max(ys))
    X = lambda i: LX + (RX - LX) * i / max(1, len(ps) - 1)
    Y = lambda v: bottom - (bottom - top) * (v - lo) / (hi - lo)
    v = lo
    while v <= hi + 1e-9:
        s.append(f'<line x1="{LX}" x2="{RX}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, LX - 6, Y(v) + 5, f"{v:g}", 14, anchor="end")
        v += st
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(ys))
    s.append(f'<polyline points="{pts}" fill="none" stroke="{SUBJ}" stroke-width="2"/>')
    idx = {p: i for i, p in enumerate(ps)}
    for r in mps:
        m = r["date"][:4] + "-" + r["date"][4:6]
        if m in idx:
            p = int(r["p"])
            x = X(idx[m])
            y0 = bottom + 14
            s.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{y0:.1f}" y2="{y0 - 5 * p:.1f}" stroke="{CTX}" '
                     f'stroke-width="2"/>' if p else
                     f'<circle cx="{x:.1f}" cy="{y0:.1f}" r="1.5" fill="{CTX}"/>')
    for yr in range(int(ps[0][:4]), int(ps[-1][:4]) + 1, 5):
        p = f"{yr}-01"
        if p in idx:
            text(s, X(idx[p]), bottom + 40, str(yr), 14, anchor="middle")
    caption(s, bottom + 64, cap)
    write(figs, "sgd_chart3_path.svg", s)


def main():
    a = L.args("sgd step 12: charts")
    P = L.paths(a.root)
    T = {r["key"]: r["value"] for r in L.read_csv(os.path.join(P["out"], "tests.csv"))}
    chart1(T, P["figs"])
    chart2(T, P["figs"])
    chart3(P["out"], P["figs"])


if __name__ == "__main__":
    main()
