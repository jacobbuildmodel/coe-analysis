# Is the quota exogenous? The evidence

Closes HANDOFF §7 item 1, or most of it. Script: `10_deregistration.py`.

The objection is the strongest one against the piece. The quota is built from
deregistrations, deregistration responds to price, so supply is not independent of the
thing it is meant to identify.

Three pieces of evidence, then what is left for you.

---

## The institutional fact that does most of the work

From LTA's quota announcement for August to October 2026, the quota is:

> "25% of the replacement COEs from vehicles deregistered in the twelve-month period from
> July 2025 to June 2026", plus a growth provision, plus adjustments for taxis, expired
> temporary COEs and the Early Turnover Scheme.

Two features of that sentence matter, and neither was in the piece.

**It is a twelve-month trailing average.** A price shock reaches the quota smeared across a
year. That is the opposite of a sharp response, and it means the feedback is heavily damped
before it arrives.

**It is announced quarterly, in advance.** Every bidding exercise inside a quarter faces a
quota that was published before the quarter began. Within a quarter the quota is
predetermined by construction. This is not an assumption; it is the announcement schedule.

---

## 1. Most of the identifying variation is predetermined

Splitting the variation in the log quota change into the part inside one quarterly
announcement and the part that crosses announcements:

| Cat | sd of dln(q) | within-quarter | across-quarter | share of variance within |
|---|---|---|---|---|
| A | 0.0742 | 0.0739 | 0.0766 | **83%** |
| B | 0.0575 | 0.0589 | 0.0507 | 87% |
| C | 0.1656 | 0.1773 | 0.0858 | 96% |
| D | 0.0802 | 0.0817 | 0.0721 | 87% |
| E | 0.0922 | 0.0915 | 0.0961 | 82% |

Between 82% and 96% of the movement in the quota happens inside a single announcement. The
Category A quota differs between the first and second exercise of the same month in **92% of
months**, and both of those numbers were published together, before either exercise ran.

The feedback channel can only operate on the remaining 17% for Category A.

---

## 2. The channel is not detectable in the data

Regressing the change in log quota on the change in log premium k exercises earlier. Two
exercises a month, so k = 6 is three months. The formula implies any effect should land
between three and fifteen months.

**Category A:**

| lag (exercises) | months | coef | se | p |
|---|---|---|---|---|
| 2 | 1 | -0.036 | 0.047 | 0.44 |
| 6 | 3 | +0.010 | 0.046 | 0.83 |
| 12 | 6 | -0.050 | 0.043 | 0.25 |
| 18 | 9 | +0.014 | 0.061 | 0.81 |
| 24 | 12 | -0.001 | 0.060 | 0.99 |
| 30 | 15 | -0.052 | 0.029 | 0.07 |

Joint test over lags 6 to 30: **F = 0.85, p = 0.61**, R-squared 0.016. Category B: F = 1.03,
p = 0.42.

The sum of coefficients is -0.238 for A and -0.254 for B. Taken at face value that means a
10% price rise lowers the later quota by about 2.4%, which has the sign the mechanism
predicts and a magnitude that cannot be distinguished from zero.

**Do not oversell this.** A joint test that fails to reject is not proof the channel is
absent. It says that at this sample size the response, if it exists, is too small to see.
That is still useful, because a channel too small to detect is also a channel too small to
generate a large bias.

---

## 3. Shutting the channel off makes the conclusion stronger

Quarter fixed effects discard every comparison that crosses an announcement. What survives
compares bidding exercises facing quotas published together, before any of them ran. Price
movements inside that quarter cannot have touched them.

| Cat | year FE (reported) | quarter FE | se | p |
|---|---|---|---|---|
| A | -0.304 | **-0.153** | 0.050 | 0.0023 |
| B | -0.432 | -0.155 | 0.070 | 0.0267 |
| C | -0.132 | -0.089 | 0.030 | 0.0026 |
| D | -0.703 | -0.397 | 0.098 | 0.0001 |
| E | -0.384 | -0.118 | 0.054 | 0.0289 |

Every category keeps its sign and stays significant at 5%. Every one moves **toward zero**,
Category A by about half.

What that does to the headline:

| | beta | predicted 2010 to 2026 price effect | quota rise needed for a 10% cut |
|---|---|---|---|
| Year FE (reported) | -0.304 | -13.6% | +41% |
| Quarter FE (predetermined only) | -0.153 | -7.1% | **+99%** |

Under the stricter specification the quota explains even less of the rise, and the lever is
even weaker. **The conclusion does not just survive the exogeneity objection. It gets
stronger when you take the objection seriously.**

**The honest caveat.** Quarter fixed effects also throw away real identifying variation, and
a smaller estimate could reflect that rather than removed bias. The two readings are not
separated by this test. What the test does establish is a range: the true beta is somewhere
around -0.15 to -0.30, and both ends give the same answer to the question the piece asks.

---

## 4. The bound that makes the direction argument almost unnecessary

Ask the inverse question. What value of beta would let the quota explain the price rise?

Category A, 2010 to 2026: log quota +0.482, log premium +1.352.

| For the quota to explain | beta would have to be |
|---|---|
| all of the rise | **+2.81** |
| half the rise | +1.40 |
| a quarter of the rise | +0.70 |
| none of it | 0.00 |

Every one of those is positive. A positive beta means issuing more certificates raises the
price, which no demand curve does. So for the conclusion to fail, the bias would have to
flip the sign and then carry it several times past zero. Feedback from deregistration cannot
do that in either direction.

This version of the argument does not depend on knowing the sign of the bias at all.

---

## 5. What is still yours

The direction of the bias in beta itself. Sections 2 and 3 give you the evidence: the
price-to-quota channel has the expected negative sign, is small, and shutting it off moves
beta toward zero. What that implies about whether -0.304 is too large or too small in
magnitude is the inference, and it is not settled here.

The chain to reason along:

> price shock, so owners hold cars longer, so fewer deregistrations, so a smaller quota
> three to fifteen months later

Then ask what a negative price-to-quota path does to the covariance between log quota and
log premium in a regression of premium on quota, and whether it pushes the estimate away
from zero or toward it. Section 3 is a strong hint about the answer, but do not quote it as
the answer until you can derive it.

---

## 6. What to change in the piece

Done in the current draft:

1. The falsification section now reports the 83% figure, the joint test, and the quarter-FE
   estimate instead of naming the problem and moving on.
2. A new aside carries the tables.
3. The identification section states the announcement schedule, which is a stronger claim
   than "the quota does not react to the bidding" and is verifiable from LTA's own release.
4. The policy arithmetic now gives a range rather than a point.

Source for the formula and schedule: LTA, "Certificate of Entitlement (COEs) Quota for
August 2026 to October 2026", retrieved 22 August 2026.
