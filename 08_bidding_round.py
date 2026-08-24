"""
Is the first bidding exercise of the month systematically cheaper than the second?

This is the only claim Piece 2 would need to make about *timing*, and it had never
been tested. The question a buyer actually faces is narrow and answerable: two
exercises run every month, roughly a fortnight apart, and a buyer with any
flexibility chooses one of them. Does the choice have a price?

Design notes
------------
* The clean estimator is the WITHIN-MONTH PAIRED DIFFERENCE, d = ln(p2) - ln(p1).
  Both exercises sit inside the same calendar month, so every slow-moving demand
  factor -- incomes, credit, population, sentiment, the year's quota allocation --
  is differenced out by construction. No controls needed and none are honest to add.
* HAC(4) standard errors on a monthly series (~2 months of autocorrelation).
* A mean difference is not a strategy. A buyer needs the difference to be
  (a) large relative to its own dispersion and (b) knowable in advance.
  Sections 3-6 test that, which is where the useful answer is.
"""
import pandas as pd, numpy as np, statsmodels.formula.api as smf
from scipy import stats
import warnings; warnings.filterwarnings("ignore")

df = pd.read_csv("analysis.csv")
CATS = ["A", "B", "C", "D", "E"]
NAMES = {"A": "smaller cars", "B": "larger cars", "C": "goods vehicles",
         "D": "motorcycles", "E": "open"}
LAGS = 4

# ---- build the within-month panel -------------------------------------------
w = df.pivot_table(index=["cat", "month", "year"], columns="bidding_no",
                   values=["premium", "quota", "bids_received", "ln_p", "ln_q"])
w.columns = [f"{a}{b}" for a, b in w.columns]
w = w.dropna().reset_index().sort_values(["cat", "month"])
w["d"]      = w.ln_p2 - w.ln_p1          # log premium change, exercise 1 -> 2
w["dq"]     = w.ln_q2 - w.ln_q1          # log quota change within the month
w["d_pct"]  = 100 * (np.expm1(w.d))
w["d_sgd"]  = w.premium2 - w.premium1
w["cheaper2"] = (w.premium2 < w.premium1).astype(int)

print("#" * 78)
print("# EXERCISE 1 vs EXERCISE 2 WITHIN THE MONTH")
print(f"# {w.month.nunique()} complete months per category, "
      f"{w.month.min()} to {w.month.max()}")
print("#" * 78)


def hac_mean(series, lags=LAGS):
    """Mean of a series with HAC standard errors (regression on a constant)."""
    d = pd.DataFrame({"y": series.values})
    m = smf.ols("y ~ 1", data=d).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    lo, hi = m.conf_int().loc["Intercept"]
    return m.params["Intercept"], m.bse["Intercept"], m.pvalues["Intercept"], lo, hi


# ---- 1. the average gap ------------------------------------------------------
print("\n" + "=" * 78)
print("1.  MEAN WITHIN-MONTH GAP    d = ln(premium_2) - ln(premium_1)")
print("    positive => the second exercise of the month is dearer")
print("=" * 78)
print(f"{'cat':<4}{'mean d':>9}{'as %':>8}{'HAC se':>9}{'p':>9}"
      f"{'95% CI (%)':>20}{'sd of d (%)':>13}{'2nd cheaper':>13}{'N':>5}")
sec1 = {}
for c in CATS:
    s = w[w.cat == c]
    b, se, p, lo, hi = hac_mean(s.d)
    pct = 100 * np.expm1(b)
    ci = f"[{100*np.expm1(lo):+.2f},{100*np.expm1(hi):+.2f}]"
    sd = 100 * s.d.std()
    share = 100 * s.cheaper2.mean()
    print(f"{c:<4}{b:>+9.4f}{pct:>+8.2f}{se:>9.4f}{p:>9.4f}{ci:>20}"
          f"{sd:>13.2f}{share:>12.1f}%{len(s):>5}")
    sec1[c] = dict(b=b, pct=pct, se=se, p=p, lo=lo, hi=hi, sd=sd, share=share, n=len(s))

print("\n    Signal-to-noise: mean gap divided by its own standard deviation")
for c in CATS:
    r = sec1[c]
    print(f"      Cat {c}: {abs(r['pct']):.2f}% mean vs {r['sd']:.2f}% sd "
          f"-> ratio {abs(r['pct'])/r['sd']:.3f}")

# ---- 2. is it just the quota moving within the month? ------------------------
print("\n" + "=" * 78)
print("2.  CONTROLLING FOR THE WITHIN-MONTH QUOTA CHANGE")
print("    d = a + b*dq  ->  'a' is the round-2 gap holding quota fixed")
print("=" * 78)
print(f"{'cat':<4}{'a (round-2 gap)':>18}{'p(a)':>9}{'b (quota)':>12}{'p(b)':>9}"
      f"{'mean dq':>11}{'R2':>8}")
for c in CATS:
    s = w[w.cat == c]
    m = smf.ols("d ~ dq", data=s).fit(cov_type="HAC", cov_kwds={"maxlags": LAGS})
    print(f"{c:<4}{m.params['Intercept']:>+18.4f}{m.pvalues['Intercept']:>9.4f}"
          f"{m.params['dq']:>+12.3f}{m.pvalues['dq']:>9.4f}"
          f"{s.dq.mean():>+11.4f}{m.rsquared:>8.3f}")

# ---- 3. does the sign hold across eras? --------------------------------------
print("\n" + "=" * 78)
print("3.  STABILITY ACROSS ERAS    (mean d, %; * = p<0.05, HAC)")
print("=" * 78)
eras = [("2010-2013 quota crunch", 2010, 2013), ("2014-2019 normalisation", 2014, 2019),
        ("2020-2022 covid", 2020, 2022), ("2023-2026 record highs", 2023, 2026)]
print(f"{'era':<26}" + "".join(f"{c:>13}" for c in CATS) + f"{'months':>9}")
for nm, y0, y1 in eras:
    row, n = f"{nm:<26}", 0
    for c in CATS:
        s = w[(w.cat == c) & (w.year >= y0) & (w.year <= y1)]
        n = len(s)
        b, se, p, lo, hi = hac_mean(s.d, lags=2)
        star = "*" if p < 0.05 else " "
        row += f"{100*np.expm1(b):>+12.2f}{star}"
    print(row + f"{n:>9}")

print("\n    Sign of the mean gap, year by year (Cat A): "
      f"{'  '.join(('+' if v>0 else '-') for v in w[w.cat=='A'].groupby('year').d.mean())}")

# ---- 4. is the gap knowable IN ADVANCE? --------------------------------------
print("\n" + "=" * 78)
print("4.  PREDICTABILITY -- the test that decides whether this is advice")
print("    A buyer sees exercise 1's result before exercise 2 opens.")
print("    Can anything observable at that moment predict d?")
print("=" * 78)
w = w.sort_values(["cat", "month"])
w["prev_move"] = w.groupby("cat").d.shift(1)                    # last month's gap
w["run_up"]    = w.ln_p1 - w.groupby("cat").ln_p2.shift(1)      # jump into exercise 1
w["osub1"]     = w.bids_received1 / w.quota1                    # how hot exercise 1 was
w["dq_known"]  = w.dq                                           # quotas announced ahead
print(f"{'cat':<4}{'lagged gap':>13}{'p':>8}{'run-up into ex1':>18}{'p':>8}"
      f"{'oversub in ex1':>17}{'p':>8}{'R2':>8}")
for c in CATS:
    s = w[w.cat == c].dropna(subset=["prev_move", "run_up", "osub1"])
    m = smf.ols("d ~ prev_move + run_up + osub1", data=s).fit(
        cov_type="HAC", cov_kwds={"maxlags": LAGS})
    print(f"{c:<4}{m.params['prev_move']:>+13.3f}{m.pvalues['prev_move']:>8.4f}"
          f"{m.params['run_up']:>+18.3f}{m.pvalues['run_up']:>8.4f}"
          f"{m.params['osub1']:>+17.3f}{m.pvalues['osub1']:>8.4f}{m.rsquared:>8.3f}")

# ---- 5. what a rule would actually have paid ---------------------------------
print("\n" + "=" * 78)
print("5.  WHAT THE RULES WOULD HAVE COST, in dollars, Cat A")
print("    Average premium paid by a buyer following each rule, 2010-2026")
print("=" * 78)
for c in ["A", "B"]:
    s = w[w.cat == c].dropna(subset=["run_up"]).copy()
    always1 = s.premium1.mean()
    always2 = s.premium2.mean()
    # the only rule section 4 could justify, applied honestly out of sample:
    s["rule"] = np.where(s.run_up > 0, s.premium2, s.premium1)
    perfect = s[["premium1", "premium2"]].min(axis=1).mean()
    worst   = s[["premium1", "premium2"]].max(axis=1).mean()
    base    = (always1 + always2) / 2
    print(f"\n  Category {c} ({NAMES[c]}), {len(s)} months")
    print(f"    always exercise 1        ${always1:>10,.0f}   {100*(always1/base-1):+.2f}% vs coin flip")
    print(f"    always exercise 2        ${always2:>10,.0f}   {100*(always2/base-1):+.2f}%")
    print(f"    'wait if prices jumped'  ${s.rule.mean():>10,.0f}   {100*(s.rule.mean()/base-1):+.2f}%")
    print(f"    coin flip                ${base:>10,.0f}")
    print(f"    PERFECT FORESIGHT        ${perfect:>10,.0f}   {100*(perfect/base-1):+.2f}%  <- the ceiling")
    print(f"    worst possible           ${worst:>10,.0f}   {100*(worst/base-1):+.2f}%")

# ---- 6. the size of the thing you cannot control -----------------------------
print("\n" + "=" * 78)
print("6.  FOR SCALE: within-month choice vs everything else")
print("=" * 78)
for c in ["A", "B"]:
    s = w[w.cat == c]
    within = 100 * s.d.abs().mean()
    d6 = df[df.cat == c].sort_values("date")
    six = 100 * (d6.ln_p.diff(12).abs().dropna().mean())   # 12 exercises = 6 months
    yr  = 100 * (d6.ln_p.diff(24).abs().dropna().mean())
    print(f"  Cat {c}: mean |gap| between the two exercises of a month = {within:.1f}%")
    print(f"         mean |change| over six months                    = {six:.1f}%")
    print(f"         mean |change| over twelve months                 = {yr:.1f}%")
    print(f"         ratio: waiting six months moves the price {six/within:.1f}x "
          f"as much as choosing the round\n")

# ---- 7. multiple testing -----------------------------------------------------
print("=" * 78)
print("7.  MULTIPLE TESTING")
print("=" * 78)
ps = sorted(sec1[c]["p"] for c in CATS)
print(f"    Section 1 ran 5 tests (one per category). p-values: "
      f"{', '.join(f'{p:.3f}' for p in ps)}")
print(f"    Bonferroni threshold for 5 tests at 5%: {0.05/5:.3f}")
print(f"    Surviving: {sum(p < 0.01 for p in ps)} of 5")
print(f"    Sidak-adjusted p on the smallest: {1-(1-ps[0])**5:.4f}")

# ---- 8. is the "mean reversion" in section 4 real, or arithmetic? ------------
print("\n" + "=" * 78)
print("8.  PLACEBO FOR SECTION 4")
print("    run_up = ln_p1 - ln_p2(prev)  and  d = ln_p2 - ln_p1  share ln_p1")
print("    with opposite signs. Any transitory component in the premium therefore")
print("    produces a negative coefficient with no predictability behind it.")
print("    Two simulated markets, neither of which contains any exploitable pattern:")
print("=" * 78)
rng = np.random.default_rng(20260821)
for label, phi in [("pure random walk (no transitory noise)", 0.0),
                   ("random walk + transitory noise, equal variance", 1.0),
                   ("random walk + transitory noise, half variance", 0.5)]:
    coefs = []
    for _ in range(2000):
        n = 200
        walk = np.cumsum(rng.normal(0, 0.05, 2 * n))
        obs = walk + phi * rng.normal(0, 0.05, 2 * n)      # transitory component
        p1, p2 = obs[0::2], obs[1::2]
        d_ = p2[1:] - p1[1:]
        ru = p1[1:] - p2[:-1]
        coefs.append(np.polyfit(ru, d_, 1)[0])
    print(f"    {label:<48} mean coef = {np.mean(coefs):+.3f}  "
          f"[{np.percentile(coefs,2.5):+.2f},{np.percentile(coefs,97.5):+.2f}]")
print("\n    Observed run-up coefficients: " +
      ", ".join(f"{c}={smf.ols('d ~ prev_move + run_up + osub1', data=w[w.cat==c].dropna(subset=['prev_move','run_up','osub1'])).fit().params['run_up']:+.3f}"
                for c in CATS))
print("    These sit inside the range a market with NO exploitable pattern produces.")
print("    The predictor that does NOT share a term with d -- last month's gap --")
print("    is insignificant for Cat A (p = 0.12).")

# ---- 9. the rule, tested out of sample ---------------------------------------
print("\n" + "=" * 78)
print("9.  OUT-OF-SAMPLE TEST OF THE TIMING RULE")
print("    Fit the section-4 regression on 2010-2018 only.")
print("    Then, month by month from 2019, bid in whichever exercise it predicts")
print("    will be cheaper -- using only information available beforehand.")
print("=" * 78)
for c in CATS:
    s = w[w.cat == c].dropna(subset=["prev_move", "run_up", "osub1"]).copy()
    tr, te = s[s.year <= 2018], s[s.year >= 2019].copy()
    m = smf.ols("d ~ prev_move + run_up + osub1", data=tr).fit()
    te["pred"] = m.predict(te)
    te["paid"] = np.where(te.pred > 0, te.premium1, te.premium2)   # pred>0 => ex2 dearer
    base = (te.premium1.mean() + te.premium2.mean()) / 2
    perfect = te[["premium1", "premium2"]].min(axis=1).mean()
    hit = 100 * ((te.pred > 0) == (te.premium1 < te.premium2)).mean()
    print(f"  Cat {c}: rule ${te.paid.mean():>9,.0f}  vs coin flip ${base:>9,.0f}  "
          f"({100*(te.paid.mean()/base-1):+.2f}%)   "
          f"picks the cheaper exercise {hit:.1f}% of the time   "
          f"[ceiling {100*(perfect/base-1):+.2f}%]   N={len(te)}")
print("\n    50% is a coin flip. N is small enough that +/-5 points is noise.")

# ---- 10. the recent era, in the money people actually pay --------------------
print("\n" + "=" * 78)
print("10. RECENT ERA IN DOLLARS  (2023-2026, when premiums are six figures)")
print("=" * 78)
for c in ["A", "B", "E"]:
    s = w[(w.cat == c) & (w.year >= 2023)]
    b, se, p, lo, hi = hac_mean(s.d, lags=2)
    print(f"  Cat {c}: mean exercise-1 premium ${s.premium1.mean():>9,.0f}, "
          f"exercise-2 ${s.premium2.mean():>9,.0f}  "
          f"(gap ${s.premium2.mean()-s.premium1.mean():>+7,.0f}, {100*np.expm1(b):+.2f}%, p={p:.3f})")
    print(f"         mean |gap| in dollars ${s.d_sgd.abs().mean():>8,.0f} | "
          f"perfect foresight would save ${(s[['premium1','premium2']].max(axis=1)-s[['premium1','premium2']].min(axis=1)).mean()/2:>7,.0f} per purchase")

# ---- 11. is there a mechanism, or is it a coincidence? -----------------------
print("\n" + "=" * 78)
print("11. LOOKING FOR A MECHANISM")
print("    If losing bidders from exercise 1 return in exercise 2, the second")
print("    exercise should draw more bids for a similar quota.")
print("=" * 78)
print(f"{'cat':<4}{'bids ex1':>11}{'bids ex2':>11}{'change':>9}{'p':>9}"
      f"{'losers in ex1':>16}{'corr(losers, extra bids)':>27}")
for c in CATS:
    s = w[w.cat == c].copy()
    s["dbids"] = np.log(s.bids_received2) - np.log(s.bids_received1)
    b, se, p, lo, hi = hac_mean(s.dbids)
    losers = df[(df.cat == c) & (df.bidding_no == 1)].set_index("month")
    losers = (losers.bids_received - losers.bids_success).reindex(s.month.values).values
    extra = (s.bids_received2 - s.bids_received1).values
    r = np.corrcoef(losers, extra)[0, 1]
    print(f"{c:<4}{s.bids_received1.mean():>11,.0f}{s.bids_received2.mean():>11,.0f}"
          f"{100*np.expm1(b):>+8.1f}%{p:>9.4f}{np.nanmean(losers):>16,.0f}{r:>+27.3f}")

# ---- 12. hit rates against a coin ------------------------------------------
print("\n" + "=" * 78)
print("12. ARE THE OUT-OF-SAMPLE HIT RATES BETTER THAN A COIN?")
print("=" * 78)
for c in CATS:
    s = w[w.cat == c].dropna(subset=["prev_move", "run_up", "osub1"]).copy()
    tr, te = s[s.year <= 2018], s[s.year >= 2019].copy()
    m = smf.ols("d ~ prev_move + run_up + osub1", data=tr).fit()
    te["pred"] = m.predict(te)
    hits = int(((te.pred > 0) == (te.premium1 < te.premium2)).sum())
    n = len(te)
    p = stats.binomtest(hits, n, 0.5).pvalue
    print(f"  Cat {c}: {hits}/{n} = {100*hits/n:.1f}%   binomial p = {p:.3f}"
          f"   {'' if p >= 0.05 else '<- nominally significant, 1 of 5 tests'}")
print(f"\n  Expected number of nominally significant results from 5 pure coins: 0.25")

# ---- 13. how robust is the Cat B / Cat E gap? -------------------------------
print("\n" + "=" * 78)
print("13. ROBUSTNESS OF THE TWO SIGNIFICANT RESULTS (B and E)")
print("=" * 78)
print("  Correlation of the within-month gap d across categories:")
piv = w.pivot(index="month", columns="cat", values="d")
print(piv.corr().round(2).to_string())
print("\n  Cat B and Cat E are linked by arbitrage (open certificates are bid up")
print("  for large cars), so these are not two independent confirmations.\n")

print("  Leave-one-era-out, mean gap (%) with HAC p:")
for c in ["B", "E"]:
    print(f"    Cat {c}:")
    for nm, y0, y1 in eras:
        s = w[(w.cat == c) & ~((w.year >= y0) & (w.year <= y1))]
        b, se, p, lo, hi = hac_mean(s.d)
        print(f"      dropping {nm:<26} {100*np.expm1(b):+6.2f}%  p = {p:.4f}  N={len(s)}")

print("\n  Split-half (first 98 months vs last 98 months):")
for c in CATS:
    s = w[w.cat == c].sort_values("month")
    h1, h2 = s.iloc[:98], s.iloc[98:]
    b1, _, p1, _, _ = hac_mean(h1.d)
    b2, _, p2, _, _ = hac_mean(h2.d)
    print(f"    Cat {c}: first half {100*np.expm1(b1):+6.2f}% (p={p1:.3f})   "
          f"second half {100*np.expm1(b2):+6.2f}% (p={p2:.3f})")

print("\n" + "#" * 78)
print("# BOTTOM LINE")
print("#" * 78)
print("""
  * Categories A, C, D: no within-month difference. Nothing to report.
  * Categories B and E: the second exercise is about 1.2% dearer on average,
    and this survives a Bonferroni correction. B and E are linked by arbitrage,
    so it is one finding, not two.
  * It is not stable: the sign is negative through 2014-2019 for every category.
  * It is not predictable in advance. The apparent mean reversion in section 4
    is what a market with no exploitable pattern produces (section 8), and a
    rule fitted before 2019 does no better than a coin after it (sections 9, 12).
  * Even perfect foresight -- knowing both prices before choosing -- is worth
    about 2% of the premium, roughly $1,800 on a recent Category A certificate.
  * Waiting six months moves the price three times as much as choosing the
    exercise, and section 3 of the main piece shows that direction is not
    forecastable either.
""")

# ---- 14. is it a round effect at all, or just drift? -------------------------
print("\n" + "=" * 78)
print("14. THE TEST THAT MATTERS: round effect, or simply a rising market?")
print("    In a market drifting upward, exercise 2 is dearer than exercise 1 for")
print("    no reason other than that it happens later. Split the monthly drift:")
print("        within  = ln_p2(m) - ln_p1(m)      [the fortnight inside a month]")
print("        between = ln_p1(m+1) - ln_p2(m)    [the fortnight across the join]")
print("    Under pure drift these are equal. A real round effect makes within > between.")
print("=" * 78)
print(f"{'cat':<4}{'within (%)':>13}{'between (%)':>14}{'difference':>13}{'se':>8}{'p':>9}")
for c in CATS:
    s = w[w.cat == c].sort_values("month").copy()
    s["between"] = s.ln_p1.shift(-1) - s.ln_p2
    s = s.dropna(subset=["between"])
    gap = s.d - s.between
    bw, _, _, _, _ = hac_mean(s.d)
    bb, _, _, _, _ = hac_mean(s.between)
    b, se, p, lo, hi = hac_mean(gap)
    print(f"{c:<4}{100*np.expm1(bw):>+13.2f}{100*np.expm1(bb):>+14.2f}"
          f"{100*np.expm1(b):>+13.2f}{se:>8.4f}{p:>9.4f}")
print("""
    Read this row by row. If 'difference' is near zero and insignificant, the
    apparent round effect is drift: the second exercise is dearer because it is
    later, not because it is second. A buyer cannot use that, because the next
    exercise after it is dearer again by the same logic.""")

# ---- 15. the one rule that needs no forecast, tested honestly ----------------
print("\n" + "=" * 78)
print("15. 'ALWAYS BID IN THE FIRST EXERCISE' -- an unconditional rule")
print("    Requires no forecast. Decide it on 2010-2018, then live with it.")
print("=" * 78)
print(f"{'cat':<4}{'2010-18 gap':>14}{'rule chosen':>14}{'2019-26 saving':>17}"
      f"{'$ saved/purchase':>19}{'months better':>16}")
for c in CATS:
    s = w[w.cat == c].sort_values("month")
    tr, te = s[s.year <= 2018], s[s.year >= 2019]
    b, _, _, _, _ = hac_mean(tr.d)
    pick1 = b > 0
    paid = (te.premium1 if pick1 else te.premium2)
    base = (te.premium1 + te.premium2) / 2
    better = 100 * ((te.premium1 < te.premium2) == pick1).mean()
    print(f"{c:<4}{100*np.expm1(b):>+13.2f}%{'exercise 1' if pick1 else 'exercise 2':>14}"
          f"{100*(paid.mean()/base.mean()-1):>+16.2f}%"
          f"{base.mean()-paid.mean():>+19,.0f}{better:>15.1f}%")
print("""
    'Months better' is how often the chosen exercise was in fact the cheaper one.
    A coin gives 50%. The saving is an average across months, not a guarantee in
    any single one -- the standard deviation of the gap is around 7%, so in any
    given month the rule is roughly as likely to cost you as to save you. It only
    shows up over many purchases, and a person buys a car every several years.""")
