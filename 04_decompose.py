import pandas as pd, numpy as np, statsmodels.formula.api as smf
import warnings; warnings.filterwarnings("ignore")
df = pd.read_csv("analysis.csv")

print("="*78); print("ANNUAL AVERAGES — quota vs premium"); print("="*78)
for c in ["A","B"]:
    s=df[df.cat==c].groupby("year").agg(quota=("quota","mean"),prem=("premium","mean"),
                                        exercises=("quota","size")).round(0)
    print(f"\n--- Category {c} ---")
    print(s.to_string())

print("\n"+"="*78); print("THE CENTRAL PUZZLE"); print("="*78)
for c in ["A","B","C","D","E"]:
    s=df[df.cat==c]
    q0=s[s.year==2010].quota.mean(); q1=s[s.year==2026].quota.mean()
    p0=s[s.year==2010].premium.mean(); p1=s[s.year==2026].premium.mean()
    print(f"Cat {c}: quota {q0:,.0f} -> {q1:,.0f} ({(q1/q0-1)*100:+.0f}%)   "
          f"premium ${p0:,.0f} -> ${p1:,.0f} ({(p1/p0-1)*100:+.0f}%)")

print("\n"+"="*78)
print("HOW MUCH OF THE 2010->2026 PRICE RISE DOES QUOTA EXPLAIN?")
print("(using beta from Spec 3, year fixed effects)")
print("="*78)
for c in ["A","B","C","D","E"]:
    s=df[df.cat==c]
    m=smf.ols("ln_p ~ ln_q + C(year)",data=s).fit(cov_type="HAC",cov_kwds={"maxlags":8})
    b=m.params["ln_q"]
    dlnq=np.log(s[s.year==2026].quota.mean())-np.log(s[s.year==2010].quota.mean())
    dlnp=np.log(s[s.year==2026].premium.mean())-np.log(s[s.year==2010].premium.mean())
    explained=b*dlnq
    print(f"Cat {c}: beta={b:+.3f} | total dln(P)={dlnp:+.3f} | quota contributes {explained:+.3f} "
          f"= {explained/dlnp*100:+.1f}%  -> demand shift accounts for {(1-explained/dlnp)*100:.1f}%")

print("\n"+"="*78)
print("POLICY ARITHMETIC: quota increase needed to cut premiums 10%")
print("="*78)
for c in ["A","B","C","D","E"]:
    s=df[df.cat==c]
    m=smf.ols("ln_p ~ ln_q + C(year)",data=s).fit(cov_type="HAC",cov_kwds={"maxlags":8})
    b=m.params["ln_q"]; lo,hi=m.conf_int().loc["ln_q"]
    need=lambda bb: (np.exp(np.log(0.90)/bb)-1)*100
    print(f"Cat {c}: need {need(b):+.0f}% more certificates   (95% CI: {need(hi):+.0f}% to {need(lo):+.0f}%)")

print("\n"+"="*78)
print("2010-2013 QUOTA CRUNCH — the natural experiment inside the data")
print("="*78)
s=df[df.cat=="A"]
w=s[(s.year>=2010)&(s.year<=2016)].groupby("year").agg(q=("quota","mean"),p=("premium","mean")).round(0)
print(w.to_string())
qmin=s.loc[s.quota.idxmin()]; qmax=s.loc[s.quota.idxmax()]
print(f"\nCat A quota trough: {qmin.quota:,.0f} in {qmin.month} -> premium ${qmin.premium:,.0f}")
print(f"Cat A quota peak  : {qmax.quota:,.0f} in {qmax.month} -> premium ${qmax.premium:,.0f}")
print(f"quota x{qmax.quota/qmin.quota:.1f}  premium x{qmax.premium/qmin.premium:.2f}  "
      f"=> implied beta over this swing: {np.log(qmax.premium/qmin.premium)/np.log(qmax.quota/qmin.quota):+.3f}")
