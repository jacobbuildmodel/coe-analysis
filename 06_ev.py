"""
EV reclassification event study.
From May 2022, EVs rated under 110kW became eligible for Category A COE.
Before that, most EVs' power output pushed them into Category B.
Prediction: demand shifts B -> A, so the A/B premium ratio should JUMP.
"""
import pandas as pd, numpy as np, statsmodels.formula.api as smf
import warnings; warnings.filterwarnings("ignore")
df = pd.read_csv("analysis.csv")

w = df.pivot_table(index=["month","bidding_no"], columns="cat",
                   values=["premium","quota","bids_received"]).reset_index()
w.columns = [a if not b else f"{a}_{b}" for a,b in w.columns]
w["ratio"]   = w.premium_A / w.premium_B          # A premium as share of B
w["ln_ratio"]= np.log(w.ratio)
w["bidratio"]= (w.bids_received_A/w.quota_A) / (w.bids_received_B/w.quota_B)
w["post"]    = (w.month >= "2022-05").astype(int)
w["t"]       = np.arange(len(w))

print("="*74)
print("A/B PREMIUM RATIO — annual means  (1.00 = Cat A as costly as Cat B)")
print("="*74)
w["year"]=w.month.str[:4].astype(int)
s=w.groupby("year").agg(ratio=("ratio","mean"),oversubA=("bidratio","mean")).round(3)
for y,r in s.iterrows():
    mark = "  <-- EV reclassification (May)" if y==2022 else ""
    print(f"  {y}   A/B premium ratio {r.ratio:.3f}   relative oversubscription {r.oversubA:.3f}{mark}")

print("\n"+"="*74)
print("EVENT STUDY — break in ln(A/B premium ratio) at May 2022")
print("="*74)
for nm, d, form in [
    ("Full sample 2010-2026, level shift", w, "ln_ratio ~ post + t"),
    ("Window 2020-2024 only",  w[(w.year>=2020)&(w.year<=2024)], "ln_ratio ~ post + t"),
    ("Window 2021-2023 only",  w[(w.year>=2021)&(w.year<=2023)], "ln_ratio ~ post + t"),
]:
    m = smf.ols(form, data=d).fit(cov_type="HAC", cov_kwds={"maxlags":8})
    b,se,p = m.params["post"], m.bse["post"], m.pvalues["post"]
    print(f"  {nm:<38} shift = {b:+.4f} ({(np.exp(b)-1)*100:+.1f}%)  se {se:.4f}  p = {p:.4f}")

print("\n"+"="*74)
print("MEANS EITHER SIDE OF THE CUTOFF")
print("="*74)
for lo,hi,lab in [("2021-05","2022-04","12 months before"),("2022-05","2023-04","12 months after")]:
    d=w[(w.month>=lo)&(w.month<=hi)]
    print(f"  {lab:<18} A/B ratio {d.ratio.mean():.3f}   Cat A ${d.premium_A.mean():>8,.0f}   Cat B ${d.premium_B.mean():>8,.0f}")

print("\n"+"="*74)
print("PLACEBO — same test at fake break dates (should be smaller / insignificant)")
print("="*74)
for fake in ["2016-05","2018-05","2019-05","2021-05","2023-05","2024-05"]:
    d=w.copy(); d["post"]=(d.month>=fake).astype(int)
    yr=int(fake[:4]); d=d[(d.year>=yr-2)&(d.year<=yr+2)]
    m=smf.ols("ln_ratio ~ post + t",data=d).fit(cov_type="HAC",cov_kwds={"maxlags":8})
    star="*" if m.pvalues["post"]<0.05 else " "
    print(f"  break at {fake}: shift {m.params['post']:+.4f}{star}  p={m.pvalues['post']:.4f}")
print("\n  (real break, same +/-2yr window, shown above as 'Window 2020-2024')")
