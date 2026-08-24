"""
Is the COE quota exogenous?

The objection, and it is the strongest one against the whole piece: the quota is
built from deregistrations, deregistration is a choice that responds to price,
so supply is not independent of the thing it is supposed to identify.

What LTA actually does (August 2026 to October 2026 quota announcement):

    "25% of the replacement COEs from vehicles deregistered in the twelve-month
     period from July 2025 to June 2026", plus a growth provision, plus
     adjustments for taxis, expired temporary COEs and so on.

Two features of that sentence do the work here.

  1. It is a TWELVE-MONTH TRAILING AVERAGE. Any price shock reaches the quota
     smeared across a year, which is the opposite of a sharp response.
  2. It is ANNOUNCED QUARTERLY AND IN ADVANCE. Every bidding exercise inside a
     quarter faces a quota that was fixed before the quarter began. Within a
     quarter the quota is predetermined by construction, not by assumption.

That second point is testable and it is the centre of this script.

Sections
  1. Is the quota really fixed within a quarter?
  2. Does lagged premium predict quota at all, and at what horizon?
  3. Re-estimate beta using ONLY within-quarter variation.
  4. How large would the bias have to be to overturn the conclusion?
"""
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("analysis.csv")
df["date"] = pd.to_datetime(df["date"])
df["quarter"] = df.date.dt.year.astype(str) + "Q" + df.date.dt.quarter.astype(str)
CATS = ["A", "B", "C", "D", "E"]
LAGS = 8

print("#" * 78)
print("# IS THE QUOTA EXOGENOUS?")
print("#" * 78)

# ---- 1. how the quota actually moves ----------------------------------------
print("\n" + "=" * 78)
print("1.  HOW MUCH DOES THE QUOTA MOVE, AND WHERE")
print("    LTA announces a monthly quota for three months at a time, one")
print("    quarter ahead. So variation splits into two kinds:")
print("      within-quarter  : months inside one announcement, fixed in advance")
print("      across-quarter  : between announcements, where feedback could enter")
print("=" * 78)
print(f"{'cat':<4}{'sd of dln(q)':>15}{'within-quarter':>17}{'across-quarter':>17}{'share within':>15}")
for c in CATS:
    s = df[df.cat == c].sort_values("date").copy()
    s["dq"] = s.ln_q.diff()
    s["same_q"] = s.quarter == s.quarter.shift(1)
    within = s.loc[s.same_q, "dq"].dropna()
    across = s.loc[~s.same_q, "dq"].dropna()
    tot = s.dq.dropna()
    share = (within.var() * len(within)) / (tot.var() * len(tot))
    print(f"{c:<4}{tot.std():>15.4f}{within.std():>17.4f}{across.std():>17.4f}{share:>14.0%}")

print("\n    Exercises per quarter, and how often the quota changes between the")
print("    two exercises of the same month:")
s = df[df.cat == "A"].sort_values("date")
same_month_change = (s.groupby("month").quota.nunique() > 1).mean()
print(f"      Cat A: quota differs between exercise 1 and 2 of a month in "
      f"{same_month_change:.0%} of months")

# ---- 2. does price predict future quota? ------------------------------------
print("\n" + "=" * 78)
print("2.  DOES A PRICE SHOCK MOVE THE FUTURE QUOTA?")
print("    Regress the change in log quota on the change in log premium k")
print("    exercises earlier. Two exercises a month, so k = 6 is three months.")
print("    The formula implies any effect should appear between k = 6 and")
print("    k = 30 (three to fifteen months), and should be small because the")
print("    deregistration window is a twelve-month average.")
print("=" * 78)
for c in ["A", "B"]:
    s = df[df.cat == c].sort_values("date").reset_index(drop=True).copy()
    s["dq"] = s.ln_q.diff()
    s["dp"] = s.ln_p.diff()
    print(f"\n  Category {c}")
    print(f"    {'lag (exercises)':<18}{'months':>8}{'coef':>10}{'se':>9}{'p':>9}")
    for k in (2, 6, 12, 18, 24, 30):
        s[f"dp{k}"] = s.dp.shift(k)
        d = s.dropna(subset=["dq", f"dp{k}"])
        m = smf.ols(f"dq ~ dp{k}", data=d).fit(cov_type="HAC", cov_kwds={"maxlags": LAGS})
        star = " *" if m.pvalues[f"dp{k}"] < 0.05 else ""
        print(f"    {k:<18}{k/2:>8.0f}{m.params[f'dp{k}']:>10.4f}"
              f"{m.bse[f'dp{k}']:>9.4f}{m.pvalues[f'dp{k}']:>9.4f}{star}")

    # joint test over the window the formula implies
    lags = list(range(6, 31, 2))
    for k in lags:
        s[f"L{k}"] = s.dp.shift(k)
    d = s.dropna(subset=["dq"] + [f"L{k}" for k in lags])
    f = "dq ~ " + " + ".join(f"L{k}" for k in lags)
    m = smf.ols(f, data=d).fit(cov_type="HAC", cov_kwds={"maxlags": LAGS})
    hyp = ", ".join(f"L{k} = 0" for k in lags)
    ft = m.f_test(hyp)
    total = sum(m.params[f"L{k}"] for k in lags)
    print(f"    joint test, lags 6 to 30: F = {float(ft.fvalue):.2f}, "
          f"p = {float(ft.pvalue):.4f}, R2 = {m.rsquared:.3f}")
    print(f"    sum of coefficients = {total:+.3f}  "
          f"(a 10% price rise moves the later quota by {10*total:+.1f}%)")

# ---- 3. beta using only predetermined quota variation -----------------------
print("\n" + "=" * 78)
print("3.  BETA USING ONLY WITHIN-QUARTER VARIATION")
print("    Quarter fixed effects throw away every comparison that crosses an")
print("    announcement. What is left compares bidding exercises facing quotas")
print("    that were published together, before any of them ran. Feedback from")
print("    prices in this quarter cannot have touched them.")
print("=" * 78)
print(f"{'cat':<4}{'year FE (reported)':>21}{'quarter FE':>14}{'se':>8}{'p':>9}{'N':>7}")
res = {}
for c in CATS:
    s = df[df.cat == c]
    m1 = smf.ols("ln_p ~ ln_q + C(year)", data=s).fit(cov_type="HAC", cov_kwds={"maxlags": LAGS})
    m2 = smf.ols("ln_p ~ ln_q + C(quarter)", data=s).fit(cov_type="HAC", cov_kwds={"maxlags": LAGS})
    res[c] = (m1.params["ln_q"], m2.params["ln_q"])
    print(f"{c:<4}{m1.params['ln_q']:>21.3f}{m2.params['ln_q']:>14.3f}"
          f"{m2.bse['ln_q']:>8.3f}{m2.pvalues['ln_q']:>9.4f}{int(m2.nobs):>7}")

print("\n    If the reported estimate were being driven by supply responding to")
print("    price, the quarter-FE estimate would move toward zero, because the")
print("    channel is shut off. Compare the two columns.")

# ---- 4. how much bias would it take? ----------------------------------------
print("\n" + "=" * 78)
print("4.  HOW WRONG WOULD BETA HAVE TO BE?")
print("    The conclusion is that the quota does not explain the price rise.")
print("    Ask the inverse: what value of beta WOULD explain it?")
print("=" * 78)
a = df[df.cat == "A"].groupby("year").agg(q=("quota", "mean"), p=("premium", "mean"))
dlq = np.log(a.q.loc[2026] / a.q.loc[2010])
dlp = np.log(a.p.loc[2026] / a.p.loc[2010])
print(f"    Category A, 2010 to 2026:")
print(f"      change in log quota    {dlq:+.3f}   ({100*np.expm1(dlq):+.0f}%)")
print(f"      change in log premium  {dlp:+.3f}   ({100*np.expm1(dlp):+.0f}%)")
print(f"      estimated beta         -0.304")
for share, label in [(1.00, "all of the rise"), (0.50, "half the rise"),
                     (0.25, "a quarter of the rise"), (0.0, "none of it")]:
    need = share * dlp / dlq
    print(f"      for the quota to explain {label:<22} beta must be {need:+.2f}")
print("\n    A positive beta means issuing MORE certificates raises the price.")
print("    No demand curve does that. So the bias would have to do two things:")
print("    flip the sign, and then carry it several times past zero. Feedback")
print("    from deregistration cannot do either, whatever its direction.")

print("\n" + "=" * 78)
print("5.  WHAT THIS DOES AND DOES NOT SETTLE")
print("=" * 78)
print("""
    Settled: the headline conclusion is not sensitive to this. Section 4 shows
    the quota would need a large POSITIVE beta to explain the rise, and no
    amount of supply-side feedback produces that.

    Not settled by this script: the DIRECTION of the bias in beta itself, and
    therefore whether -0.304 is too large or too small in magnitude. Section 2
    gives the sign and size of the price-to-quota channel and section 3 gives an
    estimate with that channel shut off. Those two are the evidence. What they
    imply for the direction of the bias is not settled here.

    The chain to reason along:
      price shock  ->  owners hold cars longer  ->  fewer deregistrations
                   ->  smaller quota, 3 to 15 months later
    Then ask what that does to cov(ln_q, ln_p) in a regression of p on q, and
    whether it pushes the estimate away from zero or toward it.
""")
