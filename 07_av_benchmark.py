"""
Turn the AV / autonomous-vehicle question from speculation into arithmetic.

If beta tells us how much price responds to supply, it also tells us how big a
DEMAND shift would have to be to produce a given price fall -- because a
proportional loss of bidders is equivalent, in its effect on where the auction
clears, to an increase in quota by the reciprocal factor.

ASSUMPTION (state it in the article): demand falls proportionally at every price,
i.e. the bid distribution keeps its shape and loses a constant fraction of bidders.
This is an approximation, not a theorem.
"""
import numpy as np, pandas as pd, statsmodels.formula.api as smf
import warnings; warnings.filterwarnings("ignore")
df=pd.read_csv("analysis.csv")

betas={}
for c in ["A","B"]:
    s=df[df.cat==c]
    betas[c]=smf.ols("ln_p ~ ln_q + C(year)",data=s).fit().params["ln_q"]

print("="*76)
print("HOW MUCH WOULD DEMAND HAVE TO FALL TO MOVE THE PRICE?")
print("="*76)
print(f"{'price fall':>12}{'equiv. quota rise':>20}{'share of bidders lost':>24}")
for c in ["A","B"]:
    b=betas[c]; print(f"\n  Category {c}   (beta = {b:+.3f})")
    for cut in [0.05,0.10,0.25,0.50]:
        qfac=np.exp(np.log(1-cut)/b)          # quota multiple needed
        share=1-1/qfac                        # equivalent proportional loss of bidders
        print(f"{cut*100:>11.0f}%{(qfac-1)*100:>19.0f}%{share*100:>23.0f}%")

print("\n"+"="*76)
print("REALITY CHECK — how many Cat A bidders are there to lose?")
print("="*76)
a=df[(df.cat=="A")&(df.year>=2025)]
print(f"  Recent Cat A bids received per exercise : {a.bids_received.mean():,.0f}")
print(f"  Recent Cat A quota per exercise         : {a.quota.mean():,.0f}")
print(f"  Bidders who already go home empty       : {a.bids_received.mean()-a.bids_success.mean():,.0f}"
      f"  ({(1-a.bids_success.mean()/a.bids_received.mean())*100:.0f}% of bidders)")
qfac=np.exp(np.log(0.90)/betas["A"]); share=1-1/qfac
print(f"\n  A 10% price cut needs ~{share*100:.0f}% of bidders to disappear")
print(f"  = about {a.bids_received.mean()*share:,.0f} fewer bids per exercise")
print(f"  Note: {(1-a.bids_success.mean()/a.bids_received.mean())*100:.0f}% of bidders ALREADY lose and come back.")
print("  So the question is not 'do people stop wanting cars' but 'do they stop bidding'.")
