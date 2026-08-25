"""
Do COE bidders usually win?

The common belief is that a COE is something you queue for and rarely get. The
bidding file records how many bids arrived and how many succeeded in every
exercise, so the question is directly answerable without modelling anything.

Reads ../analysis.csv, which 02_clean.py in the parent directory builds from
raw.csv. Nothing here re-cleans the source; there is one cleaning step for the
whole repository so the two corrections cannot drift between analyses.

Run:  python3 11_winrate.py
"""
import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("../analysis.csv")
df["rate"] = df.bids_success / df.bids_received
CATS = ["A", "B", "C", "D", "E"]
NAMES = {"A": "smaller cars", "B": "larger cars", "C": "goods vehicles",
         "D": "motorcycles", "E": "open"}

print("#" * 74)
print("# HOW OFTEN DOES A COE BID SUCCEED?")
print(f"# {len(df)//5} exercises per category, {df.month.min()} to {df.month.max()}")
print("#" * 74)

# ---- 1. the headline ---------------------------------------------------
print("\n" + "=" * 74)
print("1.  SHARE OF BIDS THAT SUCCEED, WHOLE PERIOD")
print("=" * 74)
print(f"{'cat':<5}{'':<16}{'mean':>9}{'sd':>8}{'lowest yr':>12}{'highest yr':>13}")
for c in CATS:
    s = df[df.cat == c]
    yr = s.groupby("year").rate.mean()
    print(f"{c:<5}{NAMES[c]:<16}{100*s.rate.mean():>8.1f}%{100*s.rate.std():>7.1f}"
          f"{100*yr.min():>11.1f}%{100*yr.max():>12.1f}%")

# ---- 2. the point: price moves, the queue does not ---------------------
print("\n" + "=" * 74)
print("2.  WHAT ACTUALLY ADJUSTS WHEN THE MARKET TIGHTENS")
print("    A fixed quota has to ration certificates somehow. Either fewer")
print("    bidders win, or the price rises. Compare how much each one moves.")
print("=" * 74)
print(f"{'cat':<5}{'win rate high/low':>20}{'premium high/low':>20}"
      f"{'CV win rate':>14}{'CV premium':>13}")
for c in CATS:
    g = df[df.cat == c].groupby("year").agg(rate=("rate", "mean"), p=("premium", "mean"))
    print(f"{c:<5}{g.rate.max()/g.rate.min():>19.2f}x{g.p.max()/g.p.min():>19.2f}x"
          f"{100*g.rate.std()/g.rate.mean():>13.1f}%{100*g.p.std()/g.p.mean():>12.1f}%")
print("\n    CV is the standard deviation as a share of the mean, on annual")
print("    averages. A larger CV means that series does more of the moving.")

# ---- 3. is the win rate really independent of price? -------------------
print("\n" + "=" * 74)
print("3.  DOES THE WIN RATE FALL WHEN PREMIUMS ARE HIGH?")
print("    If price did all the rationing the answer would be no. It is")
print("    'a little', and reporting that honestly matters.")
print("=" * 74)
print(f"{'cat':<5}{'r, all exercises':>19}{'p':>9}{'r, annual means':>18}{'p':>9}")
for c in CATS:
    s = df[df.cat == c]
    r1, p1 = stats.pearsonr(s.rate, np.log(s.premium))
    g = s.groupby("year").agg(rate=("rate", "mean"), p=("premium", "mean"))
    r2, p2 = stats.pearsonr(g.rate, np.log(g.p))
    print(f"{c:<5}{r1:>+19.3f}{p1:>9.4f}{r2:>+18.3f}{p2:>9.3f}")
print("\n    Negative means a lower win rate when premiums are high. The")
print("    relationship is weak, and it survives at exercise level while")
print("    disappearing on annual means, where there are only 17 points.")

# ---- 4. the extremes ---------------------------------------------------
print("\n" + "=" * 74)
print("4.  THE WORST AND BEST EXERCISES ON RECORD, CATEGORY A")
print("=" * 74)
a = df[df.cat == "A"]
for lab, row in (("hardest", a.loc[a.rate.idxmin()]), ("easiest", a.loc[a.rate.idxmax()])):
    print(f"  {lab}: {row.month} exercise {int(row.bidding_no)}  "
          f"{int(row.bids_success):,} of {int(row.bids_received):,} bids won "
          f"({100*row.rate:.1f}%), premium ${int(row.premium):,}")

# ---- 5. bidders who go home empty --------------------------------------
print("\n" + "=" * 74)
print("5.  HOW MANY LOSE, IN PEOPLE RATHER THAN PERCENTAGES")
print("=" * 74)
recent = df[(df.year >= 2024)]
for c in ["A", "D"]:
    s = recent[recent.cat == c]
    print(f"  Cat {c} ({NAMES[c]}), 2024 onward: {s.bids_received.mean():,.0f} bids per "
          f"exercise, {s.bids_success.mean():,.0f} win, {(s.bids_received-s.bids_success).mean():,.0f} do not")

# ---- 6. output for the figure ------------------------------------------
out = (df[df.cat == "A"].groupby("year")
       .agg(rate=("rate", "mean"), premium=("premium", "mean")).reset_index())
out.to_csv("winrate_catA.csv", index=False)
print(f"\n  wrote winrate_catA.csv ({len(out)} rows)")

print("\n" + "#" * 74)
print("# BOTTOM LINE")
print("#" * 74)
print("""
  Two in three Category A bids succeed, and that has been true for sixteen
  years. Across the same years the premium moved by a factor of nearly four
  while the win rate moved by a factor of 1.4.

  So the auction rations certificates mainly through price, not through luck.
  A failed bid is not bad fortune. It is a bid below the clearing price.

  The one honest complication: the win rate is weakly lower when premiums are
  high, so price is not doing quite all of the work.
""")
