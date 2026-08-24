import pandas as pd, numpy as np, json, statsmodels.formula.api as smf
import warnings; warnings.filterwarnings("ignore")
df = pd.read_csv("analysis.csv")
out={}

# 1. Cat A time series: quota + premium (separate panels, shared x)
a = df[df.cat=="A"].copy()
out["catA_series"] = [{"t":r.month+("b" if r.bidding_no==2 else "a"),"date":r.month,
                       "q":int(r.quota),"p":int(r.premium)} for r in a.itertuples()]

# 2. Annual means for A and B
for c in ["A","B"]:
    s=df[df.cat==c].groupby("year").agg(q=("quota","mean"),p=("premium","mean")).reset_index()
    out[f"annual_{c}"]=[{"year":int(r.year),"q":round(r.q),"p":round(r.p)} for r in s.itertuples()]

# 3. Scatter ln q vs ln p, Cat A and B, with fitted (year-demeaned) values
sc={}
for c in ["A","B"]:
    s=df[df.cat==c].copy()
    m=smf.ols("ln_p ~ ln_q + C(year)",data=s).fit()
    # partial-out year FE for a residual scatter (Frisch-Waugh)
    ry=smf.ols("ln_p ~ C(year)",data=s).fit().resid
    rx=smf.ols("ln_q ~ C(year)",data=s).fit().resid
    b=np.polyfit(rx,ry,1)
    sc[c]={"pts":[{"x":round(x,4),"y":round(y,4)} for x,y in zip(rx,ry)],
           "slope":round(float(b[0]),4),"intercept":round(float(b[1]),4),
           "beta":round(float(m.params["ln_q"]),4)}
out["scatter"]=sc

# 4. Beta by category with CI (Spec 3)
bars=[]
for c in ["A","B","C","D","E"]:
    s=df[df.cat==c]
    m=smf.ols("ln_p ~ ln_q + C(year)",data=s).fit(cov_type="HAC",cov_kwds={"maxlags":8})
    b=m.params["ln_q"]; lo,hi=m.conf_int().loc["ln_q"]
    bars.append({"cat":c,"beta":round(float(b),3),"lo":round(float(lo),3),"hi":round(float(hi),3),
                 "eps":round(float(1/b),2)})
out["betas"]=bars

# 5. era stability
eras=[("2010–13",2010,2013),("2014–19",2014,2019),("2020–22",2020,2022),("2023–26",2023,2026)]
st=[]
for nm,y0,y1 in eras:
    row={"era":nm}
    for c in ["A","B"]:
        d=df[(df.cat==c)&(df.year>=y0)&(df.year<=y1)]
        m=smf.ols("ln_p ~ ln_q + C(year)",data=d).fit(cov_type="HAC",cov_kwds={"maxlags":8})
        row[c]=round(float(m.params["ln_q"]),3)
    st.append(row)
out["eras"]=st

json.dump(out,open("chartdata.json","w"))
print("wrote chartdata.json")
print("betas:",bars)
print("scatter slopes:", {k:v["slope"] for k,v in sc.items()})
print("eras:",st)
