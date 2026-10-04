"""
12_figures.py -- the sgd piece's charts, from ROOT/out/ only.

Same rules as pwm/12_figures.py: the shared --fig-* tokens with literal
fallbacks, a prefers-color-scheme block plus :root[data-theme="dark"], a
480-wide canvas, no text below 14px, hairline grids, LF line endings.

Titles state the finding, chosen by fixed rules from the sealed outcomes in
out/tests.csv (title1, title2, title3 below; written before the data key,
THESIS_ADDENDUM item 2). Every caption says how to read the chart. Anything
a failed gate or test makes unreadable is drawn muted (MUTED opacity), and
the caption says why.

  figs/sgd_chart1_split.svg   for the yen and the ringgit, January 2021 to
                              December 2025, three moves in per cent: the
                              Singapore dollar against everyone, the partner
                              against everyone, the Singapore dollar against
                              the partner (T2, T3)
  figs/sgd_chart2_steady.svg  month-to-month swing of each currency's broad
                              index, August 2005 on, steadiest first (T4)
  figs/sgd_chart3_path.svg    the Singapore dollar's broad index from 2001,
                              MAS's decisions in a strip below it, and GDP
                              growth over each interval between decisions in
                              a bottom panel, on one time axis (T7)

Presentation only: nothing here computes or changes a tested number.
"""
import html
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
MUTED = 0.35
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


def head(H, key, title, desc):
    """The <svg> root: role="img", labelled by a <title> (the finding title)
    and a <desc> (the how-to-read caption), its first two children
    (THESIS_ADDENDUM item 7). Ids are prefixed by the chart, so they stay
    unique when the three charts are inlined on one page."""
    esc = lambda x: html.escape(x, quote=False)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-labelledby="{key}-title {key}-desc">',
         f'<title id="{key}-title">{esc(title)}</title>', f'<desc id="{key}-desc">{esc(desc)}</desc>',
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


def title_extra(title):
    """Height the title adds beyond its first line."""
    return 21 * (len(textwrap.wrap(title, TITLE_CHARS)) - 1)


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


def clause1(T, t, name):
    o, why = T.get(f"{t}_outcome"), T.get(f"{t}_reason", "")
    if o == "SURVIVE":
        return f"Against the {name}, the {name}'s own fall did most of the work"
    if o == "FAIL":
        return f"Against the {name}, the Singapore dollar's own rise did most of the work"
    if o == "INCONCLUSIVE":
        return f"Against the {name}, neither side did most of the work"
    if why.startswith("premise"):
        return f"The Singapore dollar did not rise against the {name}"
    return f"Against the {name}, the split did not close"


def title1(T):
    return clause1(T, "T2", "yen") + ". " + clause1(T, "T3", "ringgit") + "."


def chart1(T, figs):
    """Moves in per cent, January-March 2021 to October-December 2025: for
    each currency, the Singapore dollar against everyone, the partner against
    everyone, and the Singapore dollar against the partner (THESIS_ADDENDUM
    item 4). The shares stay in the text."""
    cap = ("How to read: each bar is a move in per cent, from the average of January to March 2021 to "
           "the average of October to December 2025. Blue, \"Singapore dollar vs all\": the Singapore "
           "dollar against all its trading partners. Grey, \"yen vs all\" or \"ringgit vs all\": the "
           "other currency against its own trading partners. Outlined, \"Singapore dollar vs yen\" or "
           "\"vs ringgit\": the Singapore dollar against that one currency. The two moves multiply "
           "rather than add, and a small remainder neither index explains makes up the difference. "
           "Right of the line is a rise, left a fall.")
    rows, muted = [], []
    for t, cur, name in (("T2", "JPY", "yen"), ("T3", "MYR", "ringgit")):
        logs = [num(T, f"{t}_{k}") for k in ("s", "nx", "b")]
        vals = [None if x is None else 100 * (math.exp(x) - 1) for x in logs]
        rows.append((name, vals))
        if T.get(f"{t}_outcome") == "NOT SCORED":
            muted.append(name)
    if muted:
        cap += (" Drawn faint: " + " and ".join(f"the {m}" for m in muted) +
                ", where the test was not scored, so the split is not read.")
    allv = [v for _, vs in rows for v in vs if v is not None] + [0]
    lo, hi, st = nice(min(allv), max(allv))
    LX, RX = 214, W - 66
    X = lambda v: LX + (RX - LX) * (v - lo) / (hi - lo)
    labels = ("Singapore dollar vs all", "{0} vs all", "Singapore dollar vs {0}")
    H0 = 92
    H = H0 + 2 * (3 * 26 + 34) + 40 + caption_height(cap) - 12 + title_extra(title1(T))
    s, y = head(H, "sgd-chart1", title1(T), cap)
    top = y + 14
    bottom = top + 2 * (3 * 26 + 34)
    v = lo
    while v <= hi + 1e-9:
        s.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{top}" y2="{bottom}" stroke="{RULE}" stroke-width="1"/>')
        text(s, X(v), bottom + 18, f"{v:g}", 14, anchor="middle")
        v += st
    s.append(f'<line x1="{X(0):.1f}" x2="{X(0):.1f}" y1="{top}" y2="{bottom}" stroke="{INK3}" stroke-width="1"/>')
    yy = top
    for name, vals in rows:
        op = f' opacity="{MUTED}"' if name in muted else ""
        text(s, 16, yy + 16, f"The {name}", 14, INK3 if op else INK, weight="600")
        yy += 26
        # The third bar is outlined, not shaded, so it reads the same in light
        # and dark mode (THESIS_ADDENDUM item 6).
        for i, (lab, val, fill) in enumerate(zip(labels, vals, (SUBJ, CTX, SURF))):
            text(s, LX - 8, yy + 13, lab.format(name), 14, INK3, anchor="end")
            if val is not None:
                x0, x1 = X(0), X(val)
                if i < 2:
                    s.append(f'<rect x="{min(x0, x1):.1f}" y="{yy:.1f}" width="{abs(x1 - x0):.1f}" height="17" '
                             f'fill="{fill}"{op}/>')
                    mag = f"{abs(val):.0f}"
                else:
                    s.append(f'<rect x="{min(x0, x1) + 0.75:.1f}" y="{yy + 0.75:.1f}" '
                             f'width="{max(abs(x1 - x0) - 1.5, 0):.1f}" height="15.5" fill="{fill}" '
                             f'stroke="{INK}" stroke-width="1.5"{op}/>')
                    # The cross rate to one decimal, as the article prints it
                    # ("49.5"); a whole number drops its ".0".
                    mag = f"{abs(val):.1f}".removesuffix(".0")
                word = f"up {mag}%" if val >= 0 else f"down {mag}%"
                text(s, max(x0, x1) + 6, yy + 13, word, 14, INK3 if op else INK)
            yy += 26
        yy += 8
    caption(s, bottom + 44, cap)
    write(figs, "sgd_chart1_split.svg", s)


WORDS = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
         8: "eight", 9: "nine", 10: "ten", 11: "eleven"}
ORDS = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh",
        8: "eighth", 9: "ninth", 10: "tenth", 11: "eleventh"}


def title2(T):
    o, why = T.get("T4_outcome"), T.get("T4_reason", "")
    if o == "NOT SCORED":
        if "gate C" in why:
            return "How steady eleven currencies were: not read, as the BIS index did not track MAS's own"
        return "How steady the currencies were: not scored, too few series"
    rank, st = int(float(T["T4_rank"])), int(float(T["T4_steadier_than"]))
    n = int(float(T["T4_present"]))
    if o == "SURVIVE":
        return (f"The Singapore dollar was the {'steadiest' if rank == 1 else 'second steadiest'} of "
                f"{WORDS[n]} currencies")
    if o == "FAIL":
        if st == 0:
            return f"The Singapore dollar was the least steady of {WORDS[n]} currencies"
        return f"The Singapore dollar was steadier than only {WORDS[st]} of the {WORDS[n - 1]} others"
    return f"The Singapore dollar ranked {ORDS[rank]} of {WORDS[n]} for steadiness"


def chart2(T, figs):
    vols = sorted(((100 * float(v), k.split("_")[1]) for k, v in T.items()
                   if k.startswith("T4_") and k.endswith("_sd") and v not in ("", None)))
    cap = ("How to read: each bar is the typical month-to-month move of a currency's broad index "
           "against its trading partners, August 2005 on, in per cent. Shorter is steadier; the "
           "Singapore dollar is in blue.")
    muted = T.get("T4_outcome") == "NOT SCORED"
    if muted:
        cap += " Drawn faint: the ranking was not scored, so it is not read."
    H = 70 + 24 * len(vols) + 40 + caption_height(cap) + 12 + title_extra(title2(T))
    s, y = head(H, "sgd-chart2", title2(T), cap)
    LX, RX = 170, W - 24
    hi = nice(0, max([v for v, _ in vols] + [0.1]))[1]
    X = lambda v: LX + (RX - LX) * v / hi
    top = y + 10
    for i, (v, a) in enumerate(vols):
        yy = top + 24 * i
        fill = SUBJ if a == "SG" else CTX
        text(s, LX - 8, yy + 14, NAMES.get(a, a), 14, INK if a == "SG" else INK3, anchor="end",
             weight="600" if a == "SG" else None)
        op = f' opacity="{MUTED}"' if muted else ""
        s.append(f'<rect x="{LX}" y="{yy + 2:.1f}" width="{X(v) - LX:.1f}" height="16" fill="{fill}"{op}/>')
    bottom = top + 24 * len(vols)
    s.append(f'<line x1="{LX}" x2="{RX}" y1="{bottom}" y2="{bottom}" stroke="{RULE}" stroke-width="1"/>')
    text(s, LX, bottom + 18, "0", 14, anchor="middle")
    text(s, RX, bottom + 18, f"{hi:g}", 14, anchor="middle")
    caption(s, bottom + 44, cap)
    write(figs, "sgd_chart2_steady.svg", s)


def title3(T):
    o = T.get("T7_outcome")
    if o == "SURVIVE":
        return "The Singapore dollar's path followed MAS's decisions more closely than growth"
    if o == "FAIL":
        return "The Singapore dollar's path followed growth at least as closely as MAS's decisions"
    if o == "INCONCLUSIVE":
        return "The Singapore dollar's path followed MAS's decisions only a little more closely than growth"
    return "The Singapore dollar's broad index and MAS's decisions: not read"


def chart3(T, out, figs):
    """The broad index since 2001 (top), MAS's decisions (middle strip) and
    GDP growth over each interval between decisions (bottom), on one time
    axis, so both things T7 ranked against the path are drawn
    (THESIS_ADDENDUM item 4)."""
    neer = {r["period"]: float(r["value"]) for r in L.read_csv(os.path.join(out, "neer.csv")) if r["area"] == "SG"}
    mps = L.read_csv(os.path.join(out, "mps.csv"))
    iv = L.read_csv(os.path.join(out, "intervals.csv"))
    first = "2001-01"
    ps = [p for p in sorted(neer) if p >= first]
    base = neer[ps[0]]
    ys = [100 * neer[p] / base for p in ps]
    cap = ("How to read: top, the Singapore dollar's broad index, January 2001 = 100. Middle, each MAS "
           "decision: a bar up for a tighter score, down for a looser one, a dot for none. Bottom, "
           "Singapore's GDP growth, year on year, in per cent, averaged over each stretch between "
           "decisions. The test ranked each stretch's move in the index against the two.")
    muted = T.get("T7_outcome") == "NOT SCORED"
    if muted:
        cap += " Drawn faint: the comparison was not scored, so the path is not read against MAS."
    op = f' opacity="{MUTED}"' if muted else ""
    P1, STRIP, P2 = 160, 64, 150
    H = 70 + P1 + STRIP + P2 + 40 + caption_height(cap) + 4 + title_extra(title3(T))
    s, y = head(H, "sgd-chart3", title3(T), cap)
    LX, RX = 60, W - 24
    idx = {p: i for i, p in enumerate(ps)}
    X = lambda i: LX + (RX - LX) * i / max(1, len(ps) - 1)
    Xm = lambda m: X(idx[m]) if m in idx else (X(0) if m < ps[0] else X(len(ps) - 1))
    # panel 1: the index
    top, bottom = y + 10, y + 10 + P1
    lo, hi, st = nice(min(ys), max(ys))
    Y = lambda v: bottom - (bottom - top) * (v - lo) / (hi - lo)
    v = lo
    while v <= hi + 1e-9:
        s.append(f'<line x1="{LX}" x2="{RX}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, LX - 6, Y(v) + 5, f"{v:g}", 14, anchor="end")
        v += st
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(ys))
    s.append(f'<polyline points="{pts}" fill="none" stroke="{SUBJ}" stroke-width="2"{op}/>')
    # strip: decisions
    mid = bottom + 30
    s.append(f'<line x1="{LX}" x2="{RX}" y1="{mid:.1f}" y2="{mid:.1f}" stroke="{RULE}" stroke-width="1"/>')
    text(s, LX - 6, mid + 5, "MAS", 14, anchor="end")
    for r in mps:
        m = r["date"][:4] + "-" + r["date"][4:6]
        if m in idx:
            p = int(r["p"])
            x = X(idx[m])
            s.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{mid:.1f}" y2="{mid - 8 * p:.1f}" stroke="{CTX}" '
                     f'stroke-width="3"{op}/>' if p else
                     f'<circle cx="{x:.1f}" cy="{mid:.1f}" r="2.5" fill="{CTX}"{op}/>')
    # panel 2: growth over each interval
    text(s, 16, bottom + STRIP + 14, "GDP growth over each stretch, per cent", 14, INK3)
    top2, bottom2 = bottom + STRIP + 30, bottom + STRIP + P2
    gs = [float(r["g"]) for r in iv if r["g"] not in ("", None)]
    glo, ghi, gst = nice(min(gs + [0]), max(gs + [0]))
    while (ghi - glo) / gst > 3:
        gst *= 2
        glo = math.floor(glo / gst) * gst
        ghi = math.ceil(ghi / gst) * gst
    Yg = lambda v: bottom2 - (bottom2 - top2) * (v - glo) / (ghi - glo)
    v = glo
    while v <= ghi + 1e-9:
        s.append(f'<line x1="{LX}" x2="{RX}" y1="{Yg(v):.1f}" y2="{Yg(v):.1f}" stroke="{RULE}" stroke-width="1"/>')
        text(s, LX - 6, Yg(v) + 5, f"{v:g}", 14, anchor="end")
        v += gst
    s.append(f'<line x1="{LX}" x2="{RX}" y1="{Yg(0):.1f}" y2="{Yg(0):.1f}" stroke="{INK3}" stroke-width="1"/>')
    for r in iv:
        if r["g"] in ("", None):
            continue
        x0, x1, gy = Xm(r["start"]), Xm(r["end"]), Yg(float(r["g"]))
        s.append(f'<line x1="{x0:.1f}" x2="{x1:.1f}" y1="{gy:.1f}" y2="{gy:.1f}" stroke="{CTX}" '
                 f'stroke-width="3"{op}/>')
    for yr in range(int(ps[0][:4]), int(ps[-1][:4]) + 1, 5):
        p = f"{yr}-01"
        if p in idx:
            text(s, X(idx[p]), bottom2 + 20, str(yr), 14, anchor="middle")
    caption(s, bottom2 + 44, cap)
    write(figs, "sgd_chart3_path.svg", s)


def main():
    a = L.args("sgd step 12: charts")
    P = L.paths(a.root)
    T = {r["key"]: r["value"] for r in L.read_csv(os.path.join(P["out"], "tests.csv"))}
    chart1(T, P["figs"])
    chart2(T, P["figs"])
    chart3(T, P["out"], P["figs"])


if __name__ == "__main__":
    main()
