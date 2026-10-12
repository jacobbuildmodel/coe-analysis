"""Figure 1 for the LTA evidence note: house style (print), two panels.

Reads lta-ab/raw/d1_coe_bidding_results_20261011.csv. PQP is recomputed as the
mean premium over the latest three months with bidding, rounded up (matches
LTA's published PQP to within $1 in all 392 months, per lta-ab/10_facts.py).
"""
import csv, math, sys
from collections import defaultdict, OrderedDict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.dates import YearLocator, DateFormatter
import datetime as dt

RAW = sys.argv[1]
OUT = sys.argv[2]
FONTS = sys.argv[3]
for f in ("SourceSans3-Regular", "SourceSans3-Semibold", "SourceSans3-Bold"):
    fm.fontManager.addfont(f"{FONTS}/{f}.ttf")
plt.rcParams.update({
    "font.family": "Source Sans 3", "font.size": 8.5,
    "axes.edgecolor": "#8a8984", "axes.linewidth": 0.6,
    "xtick.color": "#52514e", "ytick.color": "#52514e",
    "xtick.major.width": 0.6, "ytick.major.width": 0, "xtick.major.size": 3,
    "axes.labelcolor": "#52514e", "text.color": "#0b0b0b",
    "svg.fonttype": "none", "pdf.fonttype": 42,
})
INK, MUTED, GRID, SHADE = "#1f3a5f", "#6b6a66", "#e4e3df", "#f1f0ec"
ACCENT = "#c2410c"

P = defaultdict(dict)
for r in csv.DictReader(open(RAW)):
    c = r["vehicle_class"]
    if c in ("Category A", "Category B"):
        P[(r["month"], int(r["bidding_no"]))][c[-1]] = int(r["premium"])
ex = sorted(k for k in P if len(P[k]) == 2)
d = lambda m, n: dt.date(int(m[:4]), int(m[5:7]), 8 if n == 1 else 22)
xa = [d(*k) for k in ex]
ga = [(P[k]["B"] - P[k]["A"]) / 1000 for k in ex]
cross = [(x, g) for x, g in zip(xa, ga) if g < 0]

# PQP per month: mean premium over the latest three months with bidding before m
bym = OrderedDict()
for k in ex:
    bym.setdefault(k[0], []).append(k)
months = list(bym)
def nxt(m):
    y, mo = int(m[:4]), int(m[5:7]) + 1
    return f"{y + (mo > 12)}-{(mo - 1) % 12 + 1:02d}"
pq = []
allm = []
m = months[3]
while m <= months[-1]:
    prior = [x for x in months if x < m][-3:]
    if len(prior) == 3:
        a = math.ceil(sum(P[k]["A"] for x in prior for k in bym[x]) / sum(len(bym[x]) for x in prior))
        b = math.ceil(sum(P[k]["B"] for x in prior for k in bym[x]) / sum(len(bym[x]) for x in prior))
        if m >= "2010-01":
            pq.append((dt.date(int(m[:4]), int(m[5:7]), 15), (b - a) / 1000))
    m = nxt(m)

start5 = d(*ex[-120])
end = dt.date(2026, 12, 31)
fig, axes = plt.subplots(2, 1, figsize=(6.6, 4.4), sharex=True,
                         gridspec_kw={"hspace": 0.42})
panels = [
    (axes[0], xa, ga, "A.  Premium: Category B minus Category A, each bidding exercise", (-20, 60), [-20, 0, 20, 40, 60]),
    (axes[1], [p[0] for p in pq], [p[1] for p in pq], "B.  Renewal price (PQP): Category B minus Category A, each month", (-10, 40), [-10, 0, 10, 20, 30, 40]),
]
for ax, x, y, title, ylim, yt in panels:
    ax.axvspan(start5, end, color=SHADE, lw=0, zorder=0)
    for t in yt:
        ax.axhline(t, color=GRID, lw=0.6, zorder=1)
    ax.axhline(0, color="#52514e", lw=0.8, zorder=2)
    ax.plot(x, y, color=INK, lw=1.1, zorder=3, solid_joinstyle="round")
    ax.set_ylim(*ylim); ax.set_yticks(yt)
    ax.set_yticklabels([f"{t:g}" for t in yt])
    ax.set_xlim(dt.date(2010, 1, 1), end)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=4)
    ax.set_title(title, loc="left", fontsize=9, fontweight="semibold", pad=14, color="#0b0b0b")
    ax.text(0, 1.015, "S$ thousand", transform=ax.transAxes, fontsize=7.5, color=MUTED, va="bottom")
    if ax is axes[0]:
        ax.text(start5 + dt.timedelta(days=40), ylim[1] * 0.97, "Last five years", fontsize=7.5,
                color=MUTED, va="top")

ax = axes[0]
for v, lab in ((15, "Option A step, $15,000"), (7.5, "Option B step, $7,500")):
    ax.axhline(v, color="#8a8984", lw=0.7, ls=(0, (3, 2)), zorder=2)
    ax.text(end + dt.timedelta(days=60), v, lab, fontsize=7, color=MUTED, va="center",
            clip_on=False, linespacing=1.1)
ax.scatter([c[0] for c in cross], [c[1] for c in cross], s=10, color=ACCENT, zorder=4,
           edgecolors="white", linewidths=0.6)
ax.annotate("Category A above B in 21 of 397 exercises", xy=(dt.date(2013, 3, 8), -16.6),
            xytext=(dt.date(2013, 11, 1), -16.6), fontsize=7, color=MUTED, va="center",
            arrowprops=dict(arrowstyle="-", color="#8a8984", lw=0.5))
last = pq[-1]
axes[1].annotate(f"Oct 2026: {last[1]*1000:,.0f}".replace("Oct 2026: ", "Oct 2026: $"),
                 xy=last, xytext=(last[0] + dt.timedelta(days=60), -6.5), fontsize=7, color=MUTED, ha="center",
                 arrowprops=dict(arrowstyle="-", color="#8a8984", lw=0.5))
axes[1].xaxis.set_major_locator(YearLocator(2))
axes[1].xaxis.set_major_formatter(DateFormatter("%Y"))
fig.savefig(OUT + ".pdf", bbox_inches="tight")
fig.savefig(OUT + ".svg", bbox_inches="tight")
fig.savefig(OUT + ".png", bbox_inches="tight", dpi=220)
print("pqp last", pq[-1], "n crossings", len(cross))
