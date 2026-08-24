"""
Build the analysis dataset from LTA's raw COE bidding results.

Two documented corrections are applied. Both were found by internal consistency
checks and then verified against an independent published source (motorist.sg,
which mirrors LTA's contemporaneous bidding announcements).
"""
import pandas as pd, numpy as np

df = pd.read_csv("raw.csv")

# 1. Thousands separators appear in bids_success / bids_received from 2023 onward,
#    which silently loads those columns as strings.
for c in ["quota","bids_success","bids_received","premium"]:
    df[c] = pd.to_numeric(df[c].astype(str).str.replace(",","",regex=False), errors="raise")

# 2. CORRECTION 1 -- 2010-01 exercise 2, Category D premium.
#    LTA records 20090, which is byte-identical to Category C's premium in the
#    same exercise. Motorcycle premiums were 889 immediately before and 852
#    immediately after. Published result for 20 Jan 2010: $852.
m1 = (df.month=="2010-01") & (df.bidding_no==2) & (df.vehicle_class=="Category D")
assert df.loc[m1,"premium"].iloc[0] == 20090
df.loc[m1,"premium"] = 852

# 3. CORRECTION 2 -- 2010-02 exercise 1, Category B quota.
#    LTA records 1154, identical to Category A's quota in the same exercise, and
#    ~1.7x Cat B's quota in adjacent exercises. It also produces the dataset's only
#    "undersubscribed" observation (930 bids for 1154 certificates), which cannot
#    happen in a market clearing above the reserve. Published figure: 693.
m2 = (df.month=="2010-02") & (df.bidding_no==1) & (df.vehicle_class=="Category B")
assert df.loc[m2,"quota"].iloc[0] == 1154
df.loc[m2,"quota"] = 693

df["cat"]  = df["vehicle_class"].str.replace("Category ","",regex=False)
df["date"] = pd.to_datetime(df["month"]) + pd.to_timedelta((df.bidding_no-1)*14, unit="D")
df["year"] = df.date.dt.year
df["t"]    = (df.year - 2010) + (df.date.dt.month-1)/12 + (df.bidding_no-1)/24

df["ln_p"] = np.log(df.premium)
df["ln_q"] = np.log(df.quota)
df["oversub"] = df.bids_received / df.quota

df = df.sort_values(["cat","date"]).reset_index(drop=True)
df["d_ln_p"] = df.groupby("cat").ln_p.diff()
df["d_ln_q"] = df.groupby("cat").ln_q.diff()
df["ln_p_lag"] = df.groupby("cat").ln_p.shift(1)

df.to_csv("analysis.csv", index=False)

print("corrections applied and verified.")
print("undersubscribed rows now:", (df.bids_received < df.quota).sum())
print("rows:", len(df), "| period:", df.month.min(), "to", df.month.max())
print("\nlog-log correlation after correction:")
for c in sorted(df.cat.unique()):
    s=df[df.cat==c]; print(f"  Cat {c}: r = {np.corrcoef(s.ln_q,s.ln_p)[0,1]:+.3f}")
