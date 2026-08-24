# First vs second bidding exercise — results

Closes HANDOFF §7 item 4. Script: `08_bidding_round.py`. Full output: `08_output.txt`.
196 complete months per category, January 2010 to July 2026.

---

## The question and why it is answerable cleanly

Two bidding exercises run every month, about a fortnight apart. A buyer with any
flexibility picks one. Does the choice have a price?

The estimator is the **within-month paired difference**, `d = ln(p₂) − ln(p₁)`. Both
exercises sit inside one calendar month, so incomes, credit, population, sentiment and
the year's quota allocation are differenced out by construction. Nothing needs
controlling for and adding controls would be dishonest. HAC(4) standard errors.

---

## 1. The raw answer

| Cat | mean gap | HAC p | 95% CI | sd of the gap | 2nd exercise cheaper |
|---|---|---|---|---|---|
| A smaller cars | **+0.61%** | 0.178 | [−0.28, +1.50] | 7.24% | 43.9% of months |
| B larger cars | **+1.31%** | **0.003** | [+0.45, +2.17] | 7.30% | 42.9% |
| C goods vehicles | +0.12% | 0.795 | [−0.79, +1.04] | 7.51% | 45.9% |
| D motorcycles | −0.07% | 0.916 | [−1.38, +1.25] | 9.60% | 48.5% |
| E open | **+1.11%** | **0.004** | [+0.35, +1.87] | 5.93% | 37.8% |

Positive = the **second** exercise of the month clears higher.

Five tests were run. Bonferroni threshold is 0.010; B and E survive it, Šidák-adjusted
p on the smallest is 0.013. **But B and E are not independent** — the correlation of
their monthly gaps is **0.81**, because open certificates are bid up for large cars.
This is one finding appearing twice, not two findings. Cat A's correlation with B is
0.48, with E 0.50.

The within-month quota change explains none of it (§2 of the output): the gap is
unchanged when `dq` is controlled for, and mean `dq` is essentially zero.

---

## 2. The test that decides whether it is a round effect at all

In a market drifting upward, the second exercise is dearer purely because it happens
later. Split the monthly drift into two fortnights:

- **within** = ln p₂(m) − ln p₁(m) — the fortnight inside the month
- **between** = ln p₁(m+1) − ln p₂(m) — the fortnight across the month boundary

Under pure drift these are equal. A genuine round effect makes within > between.

| Cat | within | between | difference | p |
|---|---|---|---|---|
| A | +0.63% | +0.37% | +0.25% | 0.74 |
| B | +1.32% | −0.33% | **+1.65%** | **0.024** |
| C | +0.13% | +0.70% | −0.57% | 0.35 |
| D | −0.07% | +1.33% | −1.38% | 0.24 |
| E | +1.11% | −0.14% | **+1.26%** | **0.002** |

For B and E it is a real round effect, not drift. For A, C and D there is nothing to
explain.

---

## 3. It is not stable

Mean gap by era (%):

| Era | A | B | C | D | E |
|---|---|---|---|---|---|
| 2010–13 quota crunch | +1.52 | +3.23* | +0.66 | −1.02 | +2.51* |
| **2014–19 normalisation** | **−0.96** | **−0.59** | **−1.12** | **−0.20** | **−0.21** |
| 2020–22 covid | +1.84* | +2.87* | +1.75* | +0.29 | +2.00* |
| 2023–26 record highs | +1.32 | +1.21 | +0.37 | +0.95 | +1.11* |

\* p < 0.05

**The sign is negative in every category through 2014–2019** — six years, a third of the
sample, and the only stretch when premiums were falling. Same shape as the β instability
in the main piece: the relationship is era-dependent.

Leave-one-era-out for Cat B: dropping 2010–13 takes it to +0.69%, p = 0.14 — the result
does not survive removing its strongest era. Split-half is kinder: B is +1.21% (p=0.07)
in the first 98 months and +1.41% (p=0.007) in the last 98; E is +0.91% and +1.31%.

---

## 4. No mechanism visible in the bid counts

If losers from exercise 1 return in exercise 2, exercise 2 should draw more bids. It
does not — bid counts are flat between exercises in every category (largest change
+1.8% for Cat C, p = 0.053). Around 511 Cat A bidders lose per exercise and the second
exercise does not show them arriving.

*(The output reports a negative correlation between "losers in exercise 1" and "extra
bids in exercise 2". Do not use it: both terms contain `bids_received₁` with opposite
signs, so the negative sign is arithmetic, not behaviour. Same trap as §5 below.)*

---

## 5. It is not forecastable — and the apparent evidence that it is, is an artifact

Regressing `d` on things a buyer knows before exercise 2 opens gives what looks like
strong mean reversion: a big jump into exercise 1 predicts a fall in exercise 2
(Cat A coefficient −0.323, p = 0.0002).

**That coefficient is arithmetic.** The predictor `run_up = ln p₁ − ln p₂(prev)` and the
outcome `d = ln p₂ − ln p₁` both contain `ln p₁` with opposite signs. Any transitory
component in the premium — auction noise, a lumpy week of bids — produces a negative
coefficient with no predictability behind it.

Simulated markets containing **no exploitable pattern whatsoever**, 2,000 runs each:

| Simulated market | coefficient | 95% range |
|---|---|---|
| pure random walk, no transitory noise | −0.001 | [−0.14, +0.14] |
| random walk + transitory noise, half variance | −0.167 | [−0.30, −0.03] |
| random walk + transitory noise, equal variance | **−0.333** | [−0.46, −0.21] |

Observed: A = −0.323, B = −0.207, D = −0.332 — all inside the range a market with
nothing in it produces. Cat C (+0.223) and Cat E (+0.305) come out positive, which no
story predicts and which is itself a sign the coefficients are noise. The one predictor that shares no term with `d` — last month's
gap — is insignificant for Cat A (p = 0.12).

**This is the same placebo logic as the EV section of the main piece,** and it is worth
saying so: the mean reversion is the strongest-looking result in the whole exercise and
it is the one that dissolves.

---

## 6. Out of sample, a forecasting rule is a coin

Fit the §5 regression on 2010–2018, then apply it month by month from 2019 using only
information available beforehand:

| Cat | rule vs coin flip | picks the cheaper exercise | binomial p |
|---|---|---|---|
| A | +0.11% | 52.3% | 0.75 |
| B | −0.76% | 59.1% | 0.11 |
| C | +0.36% | 43.2% | 0.24 |
| D | +0.15% | **37.5%** | 0.025 |
| E | −0.48% | **61.4%** | 0.042 |

Two nominally significant results out of five, **pointing in opposite directions** — D
significantly worse than a coin, E significantly better. That is what multiple testing
looks like. Expected count of nominal significances from five actual coins: 0.25.

---

## 7. The one rule that does survive, and how small it is

The unconditional rule needs no forecast. Decide it on 2010–2018 and live with it:

| Cat | 2010–18 gap | rule picked | 2019–26 result | $ per purchase | months it was right |
|---|---|---|---|---|---|
| A | +0.33% | exercise 1 | **−0.55%** | +$402 | 59.1% |
| B | +0.91% | exercise 1 | **−0.83%** | +$733 | 62.5% |
| C | −0.42% | exercise 2 | +0.38% | −$214 | 42.0% |
| D | −0.21% | exercise 2 | +0.09% | −$8 | 52.3% |
| E | +0.78% | exercise 1 | **−0.69%** | +$618 | 64.8% |

It works out of sample in the three car categories and fails in the two where the
pre-2019 sign was noise to begin with.

**The size of it, in the money people actually pay (2023–26):**

| Cat | mean exercise 1 | mean exercise 2 | gap |
|---|---|---|---|
| A | $98,838 | $99,999 | +$1,161 (+1.32%, p = 0.062) |
| B | $115,677 | $117,017 | +$1,340 (+1.21%, p = 0.097) |
| E | $117,373 | $118,763 | +$1,390 (+1.11%, p = 0.047) |

**The ceiling on timing within the month.** Perfect foresight — knowing both prices
before choosing — is worth about **2.25%**, roughly **$1,840** on a recent Cat A
certificate. That is the maximum any within-month timing skill could ever be worth,
and nobody has it.

**For scale against what you cannot control:**

| Cat | mean gap between the month's two exercises | mean move over six months | ratio |
|---|---|---|---|
| A | 5.1% | 15.2% | 3.0× |
| B | 5.3% | 16.6% | 3.1× |

Waiting six months moves the price three times as much as choosing the exercise — and
the main piece shows that direction is not forecastable either.

---

## 8. What Piece 2 §3 can say

**Can be claimed:**

- In the car categories the second exercise of the month tends to clear a little higher
  — around 1%, roughly $400–$1,400 at today's premiums.
- It is a real round effect for B and E, not just a rising market (§2).
- A rule fixed in advance — always bid in the first exercise — would have saved money
  out of sample in A, B and E without requiring any forecast.
- Perfect within-month timing is worth about 2%. That is the ceiling.

**Must not be claimed:**

- That you can *predict* which exercise will be cheaper. Out of sample it is a coin (§6).
- That the pattern is dependable. It reversed for all five categories through 2014–2019,
  and the standard deviation of the gap is ~7% against a mean of ~1% — in any single
  month the rule is close to a coin flip. It shows up over many purchases; a person buys
  a car every several years.
- That B and E are two confirmations. Their gaps correlate 0.81. One finding.

**The honest sentence for the piece:** *the choice between the month's two exercises is
worth about one percent on average and nothing you can count on in the month you happen
to be buying — and it is a third the size of the six-month swing you cannot forecast at
all.*

That is a service to the reader, and it is consistent with the main piece rather than
contradicting it.

---
