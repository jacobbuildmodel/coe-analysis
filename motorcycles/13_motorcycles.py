"""
Motorcycle COEs are the one category that has fallen.

Every car category is at or near its record. Category D peaked in 2022 and has
come down since. This script establishes that the fall is real rather than noise,
and looks at what is different about that category.

Reads ../analysis.csv, built by ../02_clean.py from raw.csv. There is one
cleaning step for the whole repository, so the two source corrections cannot
drift between analyses.

Run:  python3 13_motorcycles.py
"""
import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("../analysis.csv")
CATS = ["A", "B", "C", "D", "E"]
NAMES = {"A": "smaller cars", "B": "larger cars", "C": "goods vehicles",
         "D": "motorcycles", "E": "open"}
g = (df.groupby(["cat", "year"])
       .agg(q=("quota", "mean"), p=("premium", "mean"), br=("bids_received", "mean"))
       .reset_index())

print("#" * 74)
print("# THE ONE COE CATEGORY THAT GOT CHEAPER")
print("#" * 74)

# ---- 1. every category against its own peak ----------------------------
print("\n" + "=" * 74)
print("1.  WHERE EACH CATEGORY SITS RELATIVE TO ITS OWN RECORD")
print("=" * 74)
print(f"{'cat':<5}{'':<16}{'peak year':>11}{'peak':>11}{'2026':>11}{'vs peak':>10}")
for c in CATS:
    s = g[g.cat == c].set_index("year")
    pk = s.p.idxmax()
    print(f"{c:<5}{NAMES[c]:<16}{pk:>11}{s.p[pk]:>11,.0f}{s.p[2026]:>11,.0f}"
          f"{100*(s.p[2026]/s.p[pk]-1):>9.1f}%")

# ---- 2. is the motorcycle fall real? -----------------------------------
print("\n" + "=" * 74)
print("2.  IS THE FALL REAL, OR IS CATEGORY D JUST NOISY?")
print("    Category D has the widest spread of any category, so this needs")
print("    checking rather than asserting.")
print("=" * 74)
d = df[df.cat == "D"]
peak = d[d.year == 2022].premium
now = d[d.year >= 2025].premium
t, p = stats.ttest_ind(peak, now, equal_var=False)
print(f"    2022 exercises      n={len(peak):>3}  mean ${peak.mean():>7,.0f}  sd ${peak.std():>6,.0f}")
print(f"    2025-26 exercises   n={len(now):>3}  mean ${now.mean():>7,.0f}  sd ${now.std():>6,.0f}")
print(f"    difference ${peak.mean()-now.mean():,.0f}, t = {t:.2f}, p = {p:.2e}")
print("\n    Year by year:")
s = g[g.cat == "D"].set_index("year")
for y in range(2019, 2027):
    print(f"      {y}: ${s.p[y]:>7,.0f}   quota {s.q[y]:>5,.0f}   bids {s.br[y]:>5,.0f}")

# ---- 3. what is different about it -------------------------------------
print("\n" + "=" * 74)
print("3.  WHAT MOVED SINCE THE MOTORCYCLE PEAK")
print("    Headline basis: 2022 (24 exercises) against 2025 and 2026 pooled")
print("    (39 exercises). That is the same window as the test in section 2,")
print("    and it avoids resting a ratio on the 15 exercises of a part year.")
print("=" * 74)
base_df = df[df.year == 2022]
rec_df = df[df.year >= 2025]
print(f"    {'cat':<5}{'':<16}{'quota':>10}{'bids':>10}{'premium':>11}")
for c in CATS:
    b, r = base_df[base_df.cat == c], rec_df[rec_df.cat == c]
    print(f"    {c:<5}{NAMES[c]:<16}{100*(r.quota.mean()/b.quota.mean()-1):>9.0f}%"
          f"{100*(r.bids_received.mean()/b.bids_received.mean()-1):>9.0f}%"
          f"{100*(r.premium.mean()/b.premium.mean()-1):>10.0f}%")

print("\n    Sensitivity to the endpoint, Category D and Category A premiums:")
gg = df.groupby(["cat", "year"]).premium.mean().unstack(0)
for lab, val in [("2022 vs 2025 full year", 2025), ("2022 vs 2026 part year", 2026)]:
    print(f"      {lab:<26} D {100*(gg.D[val]/gg.D[2022]-1):>+6.1f}%   "
          f"A {100*(gg.A[val]/gg.A[2022]-1):>+6.1f}%")
print(f"      {'2022 vs 2025-26 pooled':<26} D "
      f"{100*(rec_df[rec_df.cat=='D'].premium.mean()/base_df[base_df.cat=='D'].premium.mean()-1):>+6.1f}%   "
      f"A {100*(rec_df[rec_df.cat=='A'].premium.mean()/base_df[base_df.cat=='A'].premium.mean()-1):>+6.1f}%")
print("\n    The part year understates the motorcycle fall and overstates the")
print("    car rise, so the pooled basis is the conservative one for the")
print("    headline comparison. Annual windows follow as a further check.")

for base in (2022, 2023):
    print(f"\n    {base} to 2026")
    print(f"    {'cat':<5}{'':<16}{'quota':>10}{'bids':>10}{'premium':>11}")
    for c in CATS:
        s = g[g.cat == c].set_index("year")
        print(f"    {c:<5}{NAMES[c]:<16}{100*(s.q[2026]/s.q[base]-1):>9.0f}%"
              f"{100*(s.br[2026]/s.br[base]-1):>9.0f}%{100*(s.p[2026]/s.p[base]-1):>10.0f}%")
print("\n    Motorcycles are the only category where the number of bids did not")
print("    grow, and the only category where the premium fell. Everywhere else")
print("    bids rose by between 68% and 157% and the premium rose with them.")
print("\n    Note category C, which does not fit a mechanical reading. Its quota")
print("    rose 237% against bids up 156%, so supply outgrew bidding, and the")
print("    premium still rose 44%. The relationship is not an identity.")

# ---- 4. how stable is motorcycle demand --------------------------------
print("\n" + "=" * 74)
print("4.  BIDS PER EXERCISE, INDEXED TO 2021")
print("=" * 74)
print(f"    {'year':<7}" + "".join(f"{c:>9}" for c in CATS))
for y in range(2021, 2027):
    row = f"    {y:<7}"
    for c in CATS:
        s = g[g.cat == c].set_index("year")
        row += f"{100*s.br[y]/s.br[2021]:>9.0f}"
    print(row)
print("\n    Motorcycle bidding has sat in a narrow band since 2021 while car")
print("    bidding roughly doubled.")

# ---- 5. the estimated slope, for context -------------------------------
print("\n" + "=" * 74)
print("5.  FOR CONTEXT: THE ESTIMATED SLOPE PER CATEGORY")
print("    From 03_regress.py in the parent directory, year fixed effects.")
print("    Beta is the percentage change in premium per 1% change in quota.")
print("=" * 74)
betas = {"A": -0.304, "B": -0.432, "C": -0.132, "D": -0.703, "E": -0.384}
print(f"    {'cat':<5}{'':<16}{'beta':>9}{'quota rise for a 10% cut':>27}")
for c in CATS:
    b = betas[c]
    print(f"    {c:<5}{NAMES[c]:<16}{b:>9.3f}{100*(np.exp(np.log(0.9)/b)-1):>26.0f}%")
print("\n    Motorcycles are the most responsive category and cars the least.")
print("    That is an input to the story, not the story. The 2022 to 2026")
print("    change is visible in the raw figures without any model.")

# ---- 6. a check that did not work --------------------------------------
print("\n" + "=" * 74)
print("6.  A MECHANISM THAT DID NOT HOLD UP, REPORTED ANYWAY")
print("    Tempting idea: the premium tracks how many people chase each")
print("    certificate. If true it would explain all five categories at once.")
print("=" * 74)
df["osub"] = df.bids_received / df.quota
print(f"    {'cat':<5}{'levels r':>11}{'p':>11}{'first-diff r':>15}{'p':>11}")
for c in CATS:
    s = df[df.cat == c].sort_values("date").copy()
    r1, p1 = stats.pearsonr(np.log(s.osub), np.log(s.premium))
    s["do"] = np.log(s.osub).diff()
    s["dp"] = np.log(s.premium).diff()
    s2 = s.dropna(subset=["do", "dp"])
    r2, p2 = stats.pearsonr(s2.do, s2.dp)
    print(f"    {c:<5}{r1:>+11.3f}{p1:>11.2e}{r2:>+15.3f}{p2:>11.2e}")
print("\n    It does not hold. In levels every correlation is under 0.16. In")
print("    first differences it works for A and B and is indistinguishable")
print("    from zero for C and E. So bids per certificate is not a general")
print("    mechanism, and this piece does not claim one.")

# ---- 7. output for the figure ------------------------------------------
out = g[g.cat.isin(["A", "D"])].pivot(index="year", columns="cat", values="p").reset_index()
out.columns = ["year", "catA", "catD"]
out = out[out.year >= 2019]
out.to_csv("moto_vs_car.csv", index=False)
print(f"\n  wrote moto_vs_car.csv ({len(out)} rows)")

print("\n" + "#" * 74)
print("# BOTTOM LINE")
print("#" * 74)
print("""
  Motorcycle premiums peaked in 2022 at $10,945 and averaged $9,133 across
  2025 and 2026. The gap is decisive rather than noise, at p below 0.0001.
  Every car category is within 2% of its own record.

  Between 2022 and 2026 the motorcycle quota rose 11% and the number of bids
  did not move. Over the same years the Category A quota rose 130% and bids
  rose 157%.

  Motorcycles are the only category where bidding did not grow, and the only
  one where the premium fell. Everywhere else bids rose 68% to 157%.

  What this describes is what happened. It is not a controlled comparison.
  Category C is a live counter-example: its quota outgrew its bidding and the
  premium rose anyway. Section 6 is a mechanism that failed outright.
""")
