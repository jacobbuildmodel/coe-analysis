"""
Estimate the inverse demand slope beta in  ln(premium) = a + beta*ln(quota) + ...
Implied price elasticity of demand: epsilon = 1/beta.

Four specifications, deliberately ordered from naive to defensible.
Newey-West (HAC) standard errors throughout: these are time series and the
residuals are autocorrelated.
"""
import pandas as pd, numpy as np, statsmodels.api as sm, statsmodels.formula.api as smf
import warnings; warnings.filterwarnings("ignore")

df = pd.read_csv("analysis.csv")
CATS = ["A","B","C","D","E"]
LAGS = 8   # ~4 months at 2 exercises/month

def fit(formula, data):
    m = smf.ols(formula, data=data).fit(cov_type="HAC", cov_kwds={"maxlags":LAGS})
    return m

def report(name, formula, key="ln_q", diff=False):
    print("\n" + "="*78)
    print(name)
    print("  " + formula)
    print("="*78)
    print(f"{'cat':<5}{'beta':>9}{'se':>8}{'t':>8}{'p':>9}{'  95% CI beta':>20}{'  implied eps':>22}{'R2':>8}{'N':>6}")
    out={}
    for c in CATS:
        d = df[df.cat==c].dropna(subset=[key,"d_ln_p" if diff else "ln_p"])
        m = fit(formula, d)
        b, se, t, p = m.params[key], m.bse[key], m.tvalues[key], m.pvalues[key]
        lo, hi = m.conf_int().loc[key]
        # elasticity = 1/beta; 1/x is monotone decreasing on beta<0, so invert & swap
        e, elo, ehi = 1/b, 1/hi, 1/lo
        ci  = f"[{lo:+.2f},{hi:+.2f}]"
        eci = f"{e:+.2f} [{elo:+.2f},{ehi:+.2f}]" if hi < 0 else f"{e:+.2f} (unstable)"
        print(f"{c:<5}{b:>9.3f}{se:>8.3f}{t:>8.2f}{p:>9.4f}{ci:>20}{eci:>22}{m.rsquared:>8.3f}{int(m.nobs):>6}")
        out[c]=(b,se,lo,hi)
    return out

print("#"*78)
print("# COE DEMAND ELASTICITY — Singapore, Jan 2010 to Aug 2026")
print("# 393 bidding exercises per category. HAC(8) standard errors.")
print("#"*78)

s1 = report("SPEC 1  Naive levels — NOT credible, shown for contrast",
            "ln_p ~ ln_q")

s2 = report("SPEC 2  Quadratic time trend (absorbs slow demand drift)",
            "ln_p ~ ln_q + t + I(t**2)")

s3 = report("SPEC 3  Year fixed effects — identified off WITHIN-YEAR quota variation",
            "ln_p ~ ln_q + C(year)")

s4 = report("SPEC 4  First differences — removes all trends and fixed levels",
            "d_ln_p ~ d_ln_q", key="d_ln_q", diff=True)

# ---- The headline comparison: is Cat B demand more inelastic than Cat A? ----
print("\n" + "#"*78)
print("# HEADLINE TEST: Category A vs Category B  (pooled, interaction)")
print("#"*78)
for label, formula, key in [
    ("Year FE      ", "ln_p ~ ln_q * catB + C(year)", "ln_q:catB"),
    ("First diffs  ", "d_ln_p ~ d_ln_q * catB",        "d_ln_q:catB"),
]:
    d = df[df.cat.isin(["A","B"])].copy()
    d["catB"] = (d.cat=="B").astype(int)
    d = d.dropna(subset=["d_ln_p","d_ln_q"]) if "d_ln" in formula else d
    m = fit(formula, d)
    diff_, se_, p_ = m.params[key], m.bse[key], m.pvalues[key]
    print(f"{label} beta_B - beta_A = {diff_:+.3f}  (se {se_:.3f}, p = {p_:.4f})"
          f"   -> {'B MORE inelastic' if diff_<0 else 'B LESS inelastic'}, "
          f"{'significant' if p_<0.05 else 'NOT significant'} at 5%")

# ---- Structural stability ----
print("\n" + "#"*78)
print("# STABILITY: does beta hold across sub-periods?  (first differences)")
print("#"*78)
eras = [("2010-2013 quota crunch",2010,2013), ("2014-2019 normalisation",2014,2019),
        ("2020-2022 covid",2020,2022), ("2023-2026 record highs",2023,2026)]
print(f"{'era':<26}" + "".join(f"{c:>13}" for c in CATS))
for nm,y0,y1 in eras:
    row=f"{nm:<26}"
    for c in CATS:
        d=df[(df.cat==c)&(df.year>=y0)&(df.year<=y1)].dropna(subset=["d_ln_q"])
        m=fit("d_ln_p ~ d_ln_q", d)
        star = "*" if m.pvalues["d_ln_q"]<0.05 else " "
        row+=f"{m.params['d_ln_q']:>12.2f}{star}"
    print(row)
print("\n* = significant at 5%")
