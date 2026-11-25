"""
cdclib.py -- the one estimator of the cdc piece (THESIS.md, "Computation").

Everything scored, every control and every alternative goes through pooled():
  1. a relative price series: the hawker row divided by the geometric mean of
     the comparison rows (or the hawker row alone);
  2. the change of that series across a launch window (per cent);
  3. the excess of that change over the same calendar window in placebo
     years (percentage points);
  4. the mean excess over the launches of a test, set against every way of
     drawing one placebo year per launch (the placebo distribution).
"""
import csv
import math
from itertools import product

import numpy as np

HAWKER = "1.11.3"
COMPARISON = ("1.11.1", "1.11.2")
ELECTRICITY = "1.03.2.3"
FIRST_MONTH = (2005, 1)          # first month of rows 1.11.1, 1.11.2, 1.11.3
LAST_PLACEBO_MONTH = (2021, 11)  # month before the first universal tranche
LINE = 0.5                       # smallest effect that matters, percentage points
ALPHA = 0.05
POWER = 0.80
EXACT_LIMIT = 3_000_000
MC_DRAWS = 2_000_000
MC_SEED = 20261127



def add(ym, k):
    y, m = ym
    n = y * 12 + (m - 1) + k
    return n // 12, n % 12 + 1


def load_series(path):
    """out/series.csv -> {seriesNo: {(year, month): index}}."""
    out = {}
    with open(path, newline="", encoding="ascii") as f:
        for row in csv.DictReader(f):
            y, m = int(row["period"][:4]), int(row["period"][5:7])
            for k, v in row.items():
                if k != "period" and v != "":
                    out.setdefault(k, {})[(y, m)] = float(v)
    return out


def load_events(path):
    with open(path, newline="", encoding="ascii") as f:
        return list(csv.DictReader(f))


def relative(series, hawker, comps):
    """Hawker row over the geometric mean of the comparison rows."""
    h = series[hawker]
    if not comps:
        return dict(h)
    out = {}
    for ym, v in h.items():
        if all(ym in series[c] for c in comps):
            g = math.exp(sum(math.log(series[c][ym]) for c in comps) / len(comps))
            out[ym] = v / g
    return out


def change(rel, ym, pre, post, detrend=False):
    """Per cent change from `pre` months before the launch month to `post`
    months after it. None if a month is missing."""
    b, e = add(ym, -pre), add(ym, post)
    if b not in rel or e not in rel:
        return None
    w = 100.0 * (rel[e] / rel[b] - 1.0)
    if detrend:
        b0 = add(b, -12)
        if b0 not in rel:
            return None
        w -= 100.0 * ((rel[b] / rel[b0]) ** ((pre + post) / 12.0) - 1.0)
    return w


def placebo_years(month, pre, post, drop_years=(), detrend=False):
    """Years p whose window for calendar `month` lies wholly inside
    FIRST_MONTH..LAST_PLACEBO_MONTH and touches no dropped year: every month
    of the window, its first month included, is checked (A4: "Every placebo
    window with a month in 2007, 2020 or 2021 is dropped")."""
    years = []
    for p in range(FIRST_MONTH[0], LAST_PLACEBO_MONTH[0] + 1):
        b, e = add((p, month), -pre), add((p, month), post)
        first_needed = add(b, -12) if detrend else b
        if first_needed < FIRST_MONTH or e > LAST_PLACEBO_MONTH:
            continue
        months = [add(b, k) for k in range(0, pre + post + 1)]
        if any(y in drop_years for y, _ in months):
            continue
        years.append(p)
    return years


def event_parts(rel, ym, pre, post, drop_years=(), detrend=False):
    """(change at the launch, excess over the placebo mean, leave-one-out
    placebo excesses, placebo years). None if the launch window is missing."""
    w = change(rel, ym, pre, post, detrend)
    years = placebo_years(ym[1], pre, post, drop_years, detrend)
    pw = [change(rel, (p, ym[1]), pre, post, detrend) for p in years]
    if any(v is None for v in pw):
        raise ValueError(f"placebo window missing for month {ym[1]}")
    if w is None:
        return None
    n = len(pw)
    tot = sum(pw)
    loo = [v - (tot - v) / (n - 1) for v in pw]
    return w, w - tot / n, loo, years


def null_distribution(loos, stat="mean"):
    """The pooled statistic for every way of drawing one placebo year per
    launch: exact when the count allows, otherwise a fixed-seed sample."""
    total = 1
    for l in loos:
        total *= len(l)
    arrs = [np.asarray(l, dtype=float) for l in loos]
    if total <= EXACT_LIMIT:
        if stat == "mean":
            acc = np.zeros(1)
            for a in arrs:
                acc = (acc[:, None] + a[None, :]).ravel()
            return acc / len(arrs), "exact", total
        grid = np.array(list(product(*loos)), dtype=float)
        return np.median(grid, axis=1), "exact", total
    rng = np.random.default_rng(MC_SEED)
    draws = np.stack([a[rng.integers(0, len(a), MC_DRAWS)] for a in arrs], axis=1)
    f = np.mean if stat == "mean" else np.median
    return f(draws, axis=1), "sampled", MC_DRAWS


def pooled(series, launches, hawker=HAWKER, comps=COMPARISON, pre=1, post=1,
           drop_years=(), detrend=False, stat="mean", line=LINE):
    """The estimator. Returns a dict, or None when a launch window is not in
    the data yet (the forward test before its month is published)."""
    rel = relative(series, hawker, comps)
    parts = [event_parts(rel, ym, pre, post, drop_years, detrend) for ym in launches]
    if any(p is None for p in parts):
        return None
    excess = [p[1] for p in parts]
    s = float(np.mean(excess) if stat == "mean" else np.median(excess))
    null, how, n = null_distribution([p[2] for p in parts], stat)
    q95 = float(np.quantile(null, 1 - ALPHA, method="inverted_cdf"))
    p_value = (int(np.sum(null >= s - 1e-12)) + 1) / (len(null) + 1)
    detect = float(np.mean(null + line > q95 + 1e-12))
    mde = q95 - float(np.quantile(null, 1 - POWER, method="inverted_cdf"))
    return dict(s=s, excess=excess, changes=[p[0] for p in parts],
                placebo_n=[len(p[3]) for p in parts], q95=q95, p=p_value,
                detect=detect, mde=mde, null_max=float(np.max(null)), null_how=how, null_n=n, line=line)


def monthly_abs_changes(row, first, last):
    """{(y, m): |one-month per cent change|} for months first..last."""
    out, ym = {}, first
    while ym <= last:
        b = add(ym, -1)
        if ym in row and b in row:
            out[ym] = abs(100.0 * (row[ym] / row[b] - 1.0))
        ym = add(ym, 1)
    return out


def rank_sum_p(a, b):
    """One-sided Mann-Whitney p (a larger than b), normal approximation with
    tie correction and continuity correction."""
    vals = sorted([(v, 0) for v in a] + [(v, 1) for v in b])
    n, na, nb = len(vals), len(a), len(b)
    ranks, i, ties = [0.0] * n, 0, 0.0
    while i < n:
        j = i
        while j + 1 < n and abs(vals[j + 1][0] - vals[i][0]) < 1e-12:
            j += 1
        r = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[k] = r
        t = j - i + 1
        ties += t ** 3 - t
        i = j + 1
    ra = sum(r for r, (_, g) in zip(ranks, vals) if g == 0)
    u = ra - na * (na + 1) / 2.0
    mu = na * nb / 2.0
    var = na * nb / 12.0 * ((n + 1) - ties / (n * (n - 1)))
    if var <= 0:
        return 1.0
    z = (u - mu - 0.5) / math.sqrt(var)
    return 0.5 * math.erfc(z / math.sqrt(2.0))


# ---------------------------------------------------------------------------
# THESIS section 8: the sealed result sentence, T2 sentence and title. One pure
# function, called by 11_tests.py and by the synthetic tests; nothing is chosen
# by hand.

TITLE_HELD = ("Hawker prices did not gain 0.5% more than usual on restaurants "
              "when CDC vouchers came")
TITLE_FAILED_UP = ("Hawker prices gained at least 0.5% more than usual on restaurants "
                   "when CDC vouchers came")
TITLE_FAILED_DOWN = ("Hawker prices lost at least 0.5% less than usual to restaurants "
                     "when CDC vouchers came")
TITLE_NOT_SCORED = "Hawker prices and CDC vouchers: the monthly price test could not give an answer"


def _two(x):
    return f"{abs(x):.2f}"


def headline(verdict, W=None, P=None, S=None, p=None, m=None, d=None,
             failed_controls=()):
    """verdict: "HOLDS", "FAILS" or "NOT SCORED" (T1 alone picks it).
    W, P, S in per cent / percentage points; p the placebo p; m the smallest
    step seen four times in five; d the detection rate (0 to 1);
    failed_controls: ids among "C1" (electricity tariff) and "C2" (GST).
    Returns dict(result, t2, title). t2 is "" when T1 is not scored. The title
    follows T1; for FAILS the sign of W picks between the two failed titles."""
    if verdict == "NOT SCORED":
        if failed_controls:
            names = {"C1": "electricity-tariff", "C2": "GST"}
            fc = [names[c] for c in ("C1", "C2") if c in failed_controls]
            what = (f"{fc[0]} check" if len(fc) == 1 else f"{fc[0]} and {fc[1]} checks")
            res = (f"The test was not scored: its {what}, which show whether this method "
                   f"finds a known, dated step in the monthly index, failed, so the "
                   f"monthly index cannot see a step of this size, and no verdict on the "
                   f"vouchers is given.")
            if "C2" in failed_controls:
                res += (" The GST rises that check looks for may not have reached hawker "
                        "prices, since most hawkers are not registered for GST.")
        else:
            # Rounded down: Gate D fails below 80, so the printed figure must
            # stay below 80 as well.
            res = (f"The test was not scored: at the five CDC voucher launches outside "
                   f"January it would catch a step of 0.5 percentage points in hawker "
                   f"prices against restaurant prices only {int(math.floor(100 * d + 1e-9))} "
                   f"per cent of the time, short of the 80 per cent required, so the "
                   f"monthly index cannot see a step of this size, and no verdict on the "
                   f"vouchers is given.")
        return dict(result=res, t2="", title=TITLE_NOT_SCORED)
    held = verdict == "HOLDS"
    s_txt = f"{abs(S):.3f}" if held and _two(S) == "0.50" else _two(S)
    res = (f"At the five CDC voucher launches outside January (December 2021, May 2022, "
           f"June 2024, May 2025 and June 2026), hawker prices {'rose' if W >= 0 else 'fell'} "
           f"{_two(W)} per cent against restaurant prices (SingStat's restaurants, cafes "
           f"and pubs and its fast-food restaurants, averaged) from the month before each "
           f"launch to the month after, compared with an average "
           f"{'rise' if P >= 0 else 'fall'} of {_two(P)} per cent in the same months of "
           f"the years before the scheme (2005 to 2020 for December, 2005 to 2021 for May "
           f"and June): {s_txt} percentage points {'more' if S >= 0 else 'less'} than "
           f"usual, {'below' if held else 'at or above'} the 0.5-point step fixed in "
           f"advance as the smallest that matters, so the thesis "
           f"{'held' if held else 'failed'}.")
    if not held:
        res += " The index shows a step in the months the vouchers were issued, not its cause."
    t2 = (f"A difference this large or larger turns up in {100 * p:.1f} per cent of "
          f"comparisons drawn from the same months of the years before the scheme "
          f"(p = {p:.3f}), so "
          f"{'a step showed' if p < ALPHA else 'no step showed beyond the usual swings'}; "
          f"the test sees a step of {_two(m)} percentage points four times in five.")
    title = TITLE_HELD if held else (TITLE_FAILED_UP if W >= 0 else TITLE_FAILED_DOWN)
    return dict(result=res, t2=t2, title=title)
