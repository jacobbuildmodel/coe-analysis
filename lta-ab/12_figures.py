"""
12_figures.py -- Figure 1 of the lta-ab note, from out/ only.

One two-panel figure in the house print style, reproducing the checker's
reference design (office/redesign/fig.py): Source Sans 3 (lta-ab/fonts/, from
the site repo's research/paper-template/fonts), navy line #1f3a5f, accent
#c2410c for exercises in which Category A cleared above Category B, hairline
grid, no top, right or left spines, dashed band-step lines labelled at the
right margin, the last five years shaded. The figure title and the Notes and
Sources lines are in the document, not in the image.

  Panel A  per exercise, Category B's premium minus Category A's
           (out/exercises.csv), January 2010 to the cut-off
  Panel B  per month, the PUBLISHED PQP for Category B minus that for
           Category A (out/pqp_monthly.csv: SingStat M651121, then LTA M11),
           January 2010 to October 2026. Unlike the reference fig.py, the
           PQP is not recomputed here.
  Shading  window 2: since May 2022, exercise 1 (out/facts.csv w2_start_*).

  figs/lta_ab_fig1.png  220 dpi, embedded in NOTE.pdf
  figs/lta_ab_fig1.svg  the same figure as vector (text kept as text)

Annotation numbers come from out/facts.csv. Output is byte-stable for a given
matplotlib version (metadata stripped, fixed SVG hash salt); the version is
pinned in lta-ab/requirements.txt.

Presentation only: nothing here computes a number the note prints.
"""
import csv
import datetime as dt
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.dates import DateFormatter, YearLocator  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FIGS = os.path.join(HERE, "figs")
FONTS = os.path.join(HERE, "fonts")

INK, MUTED, GRID, SHADE = "#1f3a5f", "#6b6a66", "#e4e3df", "#f1f0ec"
ACCENT = "#c2410c"


def setup():
    for f in ("SourceSans3-Regular", "SourceSans3-Semibold", "SourceSans3-Bold"):
        fm.fontManager.addfont(os.path.join(FONTS, f + ".ttf"))
    plt.rcParams.update({
        "font.family": "Source Sans 3", "font.size": 8.5,
        "axes.edgecolor": "#8a8984", "axes.linewidth": 0.6,
        "xtick.color": "#52514e", "ytick.color": "#52514e",
        "xtick.major.width": 0.6, "ytick.major.width": 0, "xtick.major.size": 3,
        "axes.labelcolor": "#52514e", "text.color": "#0b0b0b",
        "svg.fonttype": "none", "pdf.fonttype": 42, "svg.hashsalt": "lta-ab",
    })


def rows(name):
    return list(csv.DictReader(open(os.path.join(OUT, name), encoding="utf-8")))


def ex_date(month, n):
    # the reference figure's convention: exercise 1 on the 8th, exercise 2 on the 22nd
    return dt.date(int(month[:4]), int(month[5:7]), 8 if n == 1 else 22)


def main():
    setup()
    os.makedirs(FIGS, exist_ok=True)
    F = {r["key"]: r["printed"] for r in rows("facts.csv")}
    ex = rows("exercises.csv")
    xa = [ex_date(r["month"], int(r["bidding_no"])) for r in ex]
    ga = [int(r["gap"]) / 1000 for r in ex]
    cross = [(x, g) for x, g in zip(xa, ga) if g < 0]
    lo = min(range(len(ga)), key=lambda i: ga[i])
    pq = rows("pqp_monthly.csv")
    xp = [dt.date(int(r["month"][:4]), int(r["month"][5:7]), 15) for r in pq]
    gp = [int(r["gap"]) / 1000 for r in pq]

    # shading: window 2, from the 2022 change to Category A's power threshold
    start5 = ex_date(F["w2_start_month"], 1)
    end = dt.date(2026, 12, 31)
    fig, axes = plt.subplots(2, 1, figsize=(6.6, 4.4), sharex=True, gridspec_kw={"hspace": 0.42})
    panels = [
        (axes[0], xa, ga, "A.  Premium: Category B minus Category A, each bidding exercise",
         (-20, 60), [-20, 0, 20, 40, 60]),
        (axes[1], xp, gp, "B.  Renewal price (PQP): Category B minus Category A, each month",
         (-10, 40), [-10, 0, 10, 20, 30, 40]),
    ]
    for ax, x, y, title, ylim, yt in panels:
        ax.axvspan(start5, end, color=SHADE, lw=0, zorder=0)
        for t in yt:
            ax.axhline(t, color=GRID, lw=0.6, zorder=1)
        ax.axhline(0, color="#52514e", lw=0.8, zorder=2)
        ax.plot(x, y, color=INK, lw=1.1, zorder=3, solid_joinstyle="round")
        ax.set_ylim(*ylim)
        ax.set_yticks(yt)
        ax.set_yticklabels([f"{t:g}" for t in yt])
        ax.set_xlim(dt.date(2010, 1, 1), end)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.tick_params(axis="y", length=0, pad=4)
        ax.set_title(title, loc="left", fontsize=9, fontweight="semibold", pad=14, color="#0b0b0b")
        ax.text(0, 1.015, "S$ thousand", transform=ax.transAxes, fontsize=7.5, color=MUTED, va="bottom")
        if ax is axes[0]:
            ax.text(start5 + dt.timedelta(days=40), ylim[1] * 0.97, f"Since {F['w2_start_label'].split(',')[0]}", fontsize=7.5,
                    color=MUTED, va="top")

    ax = axes[0]
    C = {r["key"]: r for r in csv.DictReader(open(os.path.join(HERE, "office", "LTA_CONSTANTS.csv"), encoding="utf-8"))}
    for v, lab in ((int(C["step_option_a"]["value"]) / 1000, f"Option A step, ${C['step_option_a']['printed']}"),
                   (int(C["step_option_b"]["value"]) / 1000, f"Option B step, ${C['step_option_b']['printed']}")):
        ax.axhline(v, color="#8a8984", lw=0.7, ls=(0, (3, 2)), zorder=2)
        ax.text(end + dt.timedelta(days=60), v, lab, fontsize=7, color=MUTED, va="center",
                clip_on=False, linespacing=1.1)
    ax.scatter([c[0] for c in cross], [c[1] for c in cross], s=10, color=ACCENT, zorder=4,
               edgecolors="white", linewidths=0.6)
    ax.annotate(f"Category A above B in {F['a_above_b_w1']} of {F['n_ex_w1']} exercises",
                xy=(xa[lo], ga[lo]), xytext=(xa[lo] + dt.timedelta(days=238), ga[lo]),
                fontsize=7, color=MUTED, va="center",
                arrowprops=dict(arrowstyle="-", color="#8a8984", lw=0.5))
    axes[1].annotate(f"Oct 2026: ${F['pqp_gap_oct2026']}", xy=(xp[-1], gp[-1]),
                     xytext=(xp[-1] + dt.timedelta(days=60), -6.5), fontsize=7, color=MUTED, ha="center",
                     arrowprops=dict(arrowstyle="-", color="#8a8984", lw=0.5))
    axes[1].xaxis.set_major_locator(YearLocator(2))
    axes[1].xaxis.set_major_formatter(DateFormatter("%Y"))
    base = os.path.join(FIGS, "lta_ab_fig1")
    fig.savefig(base + ".png", bbox_inches="tight", dpi=220, metadata={"Software": None})
    fig.savefig(base + ".svg", bbox_inches="tight", metadata={"Date": None, "Creator": None})
    print(f"  wrote figs/lta_ab_fig1.png, figs/lta_ab_fig1.svg ({len(cross)} A-above-B markers, "
          f"panel B from the published PQP, {len(pq)} months)")


if __name__ == "__main__":
    main()
