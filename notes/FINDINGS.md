# Findings — COE demand elasticity, Jan 2010 to Aug 2026

Everything below is a result. **None of it is your article.** The writing is the part
that has to be yours, and the interesting judgement calls are all still open.

---

## 0. I was wrong in the brief. Say so in the piece.

I told you to expect **inelastic** demand and a large |β|. The data says the opposite:
β is around **−0.3** for Category A, which implies a price elasticity near **−3.3**.
Demand at the margin is *elastic*.

Why my prior was wrong, and this is worth a paragraph in the article because it is the
conceptual heart of the whole thing: I conflated two different questions.

- *"Do Singaporeans badly want cars?"* — a question about the **level** of demand.
- *"If the price moves a little, how many bidders drop out?"* — a question about the
  **slope near the clearing price**.

An elasticity is the second thing. Tens of thousands of potential buyers are spread
across a dense range of willingness-to-pay, and the clearing price sits in the thick
part of that distribution. Nudging the quota slides you a short distance along a
crowded queue, so the price barely moves. Demand for cars can be overwhelming in level
and still be elastic at the margin. Those are not in tension.

The distinction between the two claims is the one most easily lost.

---

## 1. Two errors in LTA's published dataset, found and verified

Both were caught by internal consistency checks, then confirmed against independently
published contemporaneous results.

| Where | LTA publishes | Correct value | How we know |
|---|---|---|---|
| 2010-01 exercise 2, Cat D premium | 20,090 | **852** | Identical to Cat C's premium in the same exercise. Cat D was 889 before and 852 after. Published result for 20 Jan 2010 confirms 852. |
| 2010-02 exercise 1, Cat B quota | 1,154 | **693** | Identical to Cat A's quota in the same exercise, ~1.7× Cat B's neighbours, and it produced the dataset's only "undersubscribed" exercise — 930 bids for 1,154 certificates, which cannot happen in a market clearing above the reserve price. Published figure confirms 693. |

Both have the same signature: a value duplicated from the row above. A systematic scan
found exactly these two and no others.

**Lead the article with this.** It is concrete, it is verifiable, and it demonstrates
something no coursework does — that you checked the government's homework and found it
wanting. Five external cross-checks pass on untouched rows, so the rest of the file is sound.

---

## 2. Headline results

β is the elasticity of the premium with respect to the quota: a 1% quota increase
changes the premium by β%. Specification is `ln(premium) ~ ln(quota) + year fixed
effects`, HAC(8) standard errors, identified off within-year quota variation.

| Category | β | 95% CI | implied ε = 1/β |
|---|---|---|---|
| A — small cars | −0.30 | [−0.44, −0.17] | −3.3 |
| B — large cars | −0.43 | [−0.68, −0.19] | −2.3 |
| C — goods vehicles | −0.13 | [−0.18, −0.08] | −7.6 |
| D — motorcycles | −0.70 | [−0.94, −0.47] | −1.4 |
| E — open | −0.38 | [−0.57, −0.20] | −2.6 |

**Report β, not ε.** The reciprocal is a fragile object: when β is small and imprecisely
estimated, 1/β has enormous asymmetric confidence intervals (one first-difference
specification gave [−162, −2.7], which is not a finding, it is a warning). β is directly
estimated, directly policy-relevant, and honest.

### The comparison you predicted — it holds

Pooling A and B with an interaction term, year fixed effects:

> **β_B − β_A = −0.111  (se 0.038, p = 0.003)**

Category B demand is significantly **more inelastic** than Category A. Wealthier buyers,
certificate a smaller share of total spend, worse outside options — the theory predicted
this and the data agrees at the 1% level.

**But**: in first differences the same gap is −0.030 with p = 0.79. Not significant.
Report both. A result that survives one specification and not another is a real result
with a real limitation, and saying so is what separates you from someone who ran
regressions until something starred.

---

## 3. The finding I did not expect, and your best material

Between 2010 and 2026, Category A quota **rose 62%** (781 → 1,264 per exercise, annual
mean). Premiums **rose 287%** ($30,405 → $117,548).

Run that through β = −0.30: the quota change on its own should have pushed premiums
**down about 14%**. They went up nearly 300%.

**Quota explains none of the long-run price rise. It works in the wrong direction.**
Every bit of the increase — and then some — is the demand curve shifting out.

This reframes the public conversation, which treats COE prices as a supply story. They
are a demand story. Population, incomes, credit conditions, the collapse of the
alternative of not owning a car — something moved demand enormously, and the quota
debate is arguing about the small term.

### The policy arithmetic that follows

To cut premiums 10%, holding demand fixed:

| Category | quota increase required |
|---|---|
| A | **+41%** (CI: +27% to +86%) |
| B | +28% |
| C | +122% |
| D | +16% |
| E | +32% |

For scale: the 2024→2025 Cat A quota increase was about +24%, which predicts roughly a
6.5% price fall. Premiums instead rose about 14% over the same period. Demand outran the
injection comfortably. That is a specific, checkable, and slightly uncomfortable claim
about a live policy — exactly what makes a piece worth reading.

---

## 4. The instability is a finding, not a failure

β estimated separately within each era, same specification:

| Era | Cat A | Cat B |
|---|---|---|
| 2010–13 quota crunch | −0.59 | −0.94 |
| 2014–19 normalisation | −0.23 | −0.18 |
| 2020–22 covid | −0.43 | −0.77 |
| 2023–26 record highs | **+0.14** | **+0.25** |

The sign flips positive in the most recent era. Quota and premiums rose *together*
because demand was moving out faster than supply within each year, so within-year
variation no longer traces a demand curve at all.

Do not hide this. It means "the" elasticity is not a single stable structural parameter
over sixteen years, and any headline number is an average across regimes that behave
differently. Stating that plainly is stronger than a clean number would have been.

---

## 5. Things still open — your calls, not mine

1. **Which β do you lead with?** Year FE is the most defensible. First differences are
   cleaner in principle but the high-frequency quota variation is mostly administrative
   noise (R² of 0.01–0.03), so they're weak. Argue for one.
2. **What do you do about 2023–26?** Drop it, split the sample, or make it the story?
3. **The deregistration feedback loop** (Section 5.1 of the brief) is still unaddressed.
   High premiums → owners hold cars longer → fewer certificates return → higher premiums.
   You cannot fix it with this data alone. You can bound it, or you can be explicit that
   your β is biased and say in which direction. Work out the direction yourself — it's a
   good exercise and it is exactly what you'd be asked.
4. **Category E contaminates A and B** through arbitrage. Five separate regressions
   overstate precision. Worth a sentence at minimum.
5. **Nothing controls for income, population or interest rates.** Year fixed effects
   absorb anything common to a year, which is a lot, but not everything.

---

## 6. Files

| File | What it is |
|---|---|
| `raw.csv` | LTA's file exactly as downloaded |
| `01_explore.py` | Data quality checks — this is what caught the errors |
| `02_clean.py` | The two corrections, with assertions so they fail loudly if the source changes |
| `03_regress.py` | Four specifications, the A/B test, the era table |
| `04_decompose.py` | The quota-vs-demand decomposition and policy arithmetic |
| `05_chartdata.py` | Chart data prep |
| `analysis.csv` | Clean analysis dataset |
| `figures.html` | Four charts, self-contained, light/dark, tooltips, table view |

Put the code on GitHub next to the article. The link is worth as much as the piece.

---

## 7. Before you publish

Reconstruct these three numbers from scratch without looking: **β for Cat A**, **the
quota increase needed for a 10% price cut**, and **why quota explains none of the
2010–2026 rise**. If any of them won't come, you don't own the project yet.

Then have someone ask you: *"Your quota isn't exogenous — deregistrations respond to
price. Why should I believe any of this?"* Have the answer ready.
