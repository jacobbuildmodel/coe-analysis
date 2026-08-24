import pandas as pd, numpy as np

df = pd.read_csv("raw.csv")

# --- FIX: bids_success / bids_received contain thousands separators ("1,007")
# in later rows, which silently makes those columns strings. Strip and coerce.
for c in ["quota","bids_success","bids_received","premium"]:
    df[c] = pd.to_numeric(df[c].astype(str).str.replace(",","",regex=False), errors="raise")

df["date"] = pd.to_datetime(df["month"]) + pd.to_timedelta((df["bidding_no"]-1)*14, unit="D")
df["cat"]  = df["vehicle_class"].str.replace("Category ","",regex=False)
df["oversub"] = df.bids_received / df.quota
df["fill"]    = df.bids_success  / df.quota
df = df.sort_values(["cat","date"]).reset_index(drop=True)

print("="*72); print("COVERAGE")
print(df.shape, "|", df.month.min(), "to", df.month.max(), "| exercises per cat:", df.cat.value_counts().iloc[0])

print("\n"+"="*72); print("INTEGRITY CHECKS")
print("bids_success > quota          :", (df.bids_success > df.quota).sum())
print("bids_received < bids_success  :", (df.bids_received < df.bids_success).sum())
print("UNDERSUBSCRIBED (recd<quota)  :", (df.bids_received < df.quota).sum())
print("   -> by category:"); print(df[df.bids_received<df.quota].cat.value_counts().to_string())
print("\nmonths missing 2nd exercise   :", df.groupby('month').bidding_no.nunique().pipe(lambda s: s[s!=2]).to_dict())

print("\n"+"="*72); print("PREMIUM (SGD) BY CATEGORY")
print(df.groupby("cat")["premium"].describe().round(0).to_string())
print("\n"+"="*72); print("QUOTA BY CATEGORY")
print(df.groupby("cat")["quota"].describe().round(0).to_string())
print("\n"+"="*72); print("OVERSUBSCRIPTION bids_received/quota")
print(df.groupby("cat")["oversub"].describe().round(2).to_string())

print("\n"+"="*72); print("START -> END")
for c in sorted(df.cat.unique()):
    s=df[df.cat==c]; a,b=s.iloc[0],s.iloc[-1]
    print(f"  {c}: {a.month} ${a.premium:>7,} (Q={a.quota:>5,})  ->  {b.month} ${b.premium:>7,} (Q={b.quota:>5,})   x{b.premium/a.premium:.1f}")

print("\n"+"="*72); print("RECORD HIGH / LOW")
for c in sorted(df.cat.unique()):
    s=df[df.cat==c]; hi,lo=s.loc[s.premium.idxmax()],s.loc[s.premium.idxmin()]
    print(f"  {c}: high ${hi.premium:>7,} {hi.month}#{hi.bidding_no}   |   low ${lo.premium:>7,} {lo.month}#{lo.bidding_no}")

print("\n"+"="*72); print("LOG-LOG CORRELATION  ln(premium) vs ln(quota)")
for c in sorted(df.cat.unique()):
    s=df[df.cat==c]
    print(f"  Cat {c}: r = {np.corrcoef(np.log(s.quota), np.log(s.premium))[0,1]:+.3f}")

df.to_csv("clean.csv", index=False)
print("\nwrote clean.csv  rows:", len(df))
