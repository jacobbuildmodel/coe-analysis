# RESULTS: minimum wage or the Progressive Wage Model

Written by `13_results.py` from `out/`. Tests as sealed in `THESIS.md` (commit e5f877b); failures first. Outcome labels as sealed: SURVIVE, FAIL, INCONCLUSIVE, NOT SCORED.

## Verdict

**The record cannot tell the two models apart; the rest of the bottom kept pace.**

- **Part A, the ladder:** the record cannot tell the two models apart.
- **Part B, the rest of the bottom:** the rest of the bottom kept pace.

Singapore publishes no yearly count of cleaners, security officers or landscape workers, so whether the ladders cost jobs cannot be tested from public data.

- The pay test leans the other way (T2): in-house workers, unbound until 2022 in all three groups, dilute the covered side, and the LQS floor lifted the comparison side. So a pay gain found is strong evidence, and none found is weak.
- Part B leans toward "kept pace" (T3): the LQS was a floor under the uncovered jobs too, and it rose during the window. So "kept pace" is weak evidence, and "fell behind" is strong evidence.
- The record cannot say what a national floor would have done in jobs no ladder reached.
- T4 was not scored: no public series qualifies (THESIS section 4).

## Tests that did not survive

### T1. Parallel before (the design test): FAIL (Jacob's confidence at seal: 28%)

Sealed wording (THESIS.md, verbatim):

> **Prediction.** Every group with at least 4 pre-period Junes has a drift smaller than 1.0 log point a year in absolute value.
>
> **Survive if:** |slope| < 0.010 for every such group.
>
> **Fail if:** |slope| >= 0.010 for any group. **That group fails the design, and the article says so:** it is dropped from T2 and T5 scoring, and its after-minus-before gap is shown as uninterpretable. If every group fails, T2 and T5 are not scored (they drop out of the count and the Brier score). The verdict is then "the record cannot say", and that is published.

- cleaning: drift -0.0308 a year (90% interval -0.1008 to 0.0392), 4 pre-period Junes; line 0.010; fails the design: dropped from T2 and T5 scoring, and its after-minus-before gap is uninterpretable.
- security: drift 0.0244 a year (90% interval 0.0115 to 0.0373), 6 pre-period Junes; line 0.010; fails the design: dropped from T2 and T5 scoring, and its after-minus-before gap is uninterpretable.
- landscape: drift 0.0010 a year (90% interval -0.0147 to 0.0167), 6 pre-period Junes; line 0.010; passes.

### T4. The jobs survived the fitting: NOT SCORED (no confidence: not scored)

Sealed wording (THESIS.md, verbatim):

> **Prediction.** Employment in the covered industries held up: relative change **greater than -5 log points** in every scored industry.
>
> **Survive if:** every scored industry > -0.05.
>
> **Fail if:** any scored industry <= -0.10: jobs fell where the floor bound, the competitive signature.

- no series qualifies (THESIS section 4): Singapore publishes no yearly count of cleaners, security officers or landscape workers, so whether the ladders cost jobs cannot be tested from public data.
- series: none (priority rule, THESIS section 4).

## Tests that survived

### T2. The suit fits: pay rose where the ladder was hung: SURVIVE (Jacob's confidence at seal: 40%)

Sealed wording (THESIS.md, verbatim):

> **Prediction.** Bottom pay in covered jobs rose by **at least 10 log points (about 10.5 per cent) more** than in comparison jobs, pooled, and by more than zero in every scored group.
>
> **Survive if:** pooled >= 0.10 **and** every scored group > 0.
>
> **Fail if:** pooled < 0.05, **or** any scored group <= 0. Either means the ladder did not visibly lift the bottom of the jobs it covered, relative to jobs it did not cover.

- landscape: 0.2201 (90% interval 0.1579 to 0.2822).
- pooled: 0.2201 (90% interval 0.1579 to 0.2822); survive at 0.10 with every group above 0, fail below 0.05 or any group at or below 0.
- groups scored: landscape.

### T3. The rest of the bottom kept pace: SURVIVE (Jacob's confidence at seal: 58%)

Sealed wording (THESIS.md, verbatim):

> **Prediction.** The uncovered bottom kept pace: its growth fell short of the middle's by **less than 5 log points** over the span.
>
> **Survive if:** shortfall < 0.05 (including any case where the uncovered bottom grew faster).
>
> **Fail if:** shortfall >= 0.05: uncovered low-wage jobs fell behind the middle, as the tailor's extreme predicts.

- comparison set C, growth 0.2466 (start mean 7.0556 over 3 Junes, end mean 7.3022 over 3 Junes).
- the middle (LFS median, excluding employer CPF), growth 0.2916.
- shortfall 0.0450; line 0.05. THESIS fixes no interval for T3: it is a difference of two window means.

### T5. The first rung shows up in the survey: SURVIVE (Jacob's confidence at seal: 50%)

Sealed wording (THESIS.md, verbatim):

> **Prediction.** The ratio is at least 0.97 in every post-period June for every scored group.
>
> **Survive if:** every ratio >= 0.97.
>
> **Fail if:** any ratio < 0.97.

- landscape: 2017 1.000, 2018 1.000, 2019 1.038, 2022 1.000.
- lowest ratio 1.000; line 0.97. THESIS fixes no interval for T5: each ratio is a published percentile over a rung.

## Scorecard

- Scored: T1 T2 T3 T5 (4); held: 3.
- T1: FAIL; confidence at seal 28%.
- T2: SURVIVE; confidence at seal 40%.
- T3: SURVIVE; confidence at seal 58%.
- T4: NOT SCORED; confidence at seal not scored.
- T5: SURVIVE; confidence at seal 50%.
- Held 3 of 4 scored, against an expected 1.76 (the sum of the confidences of the scored tests).
- Brier score: 0.216 (mean over the scored tests; tests not scored drop out).

## Sensitivities (reported, not scored)

Every row is a sealed sensitivity. None enters the score or the verdict.

| Test | Variant | Key | Value | Scored |
|---|---|---|---|---|
| T1 | without June 2009 | cleaning_slope | not run: fewer than 4 Junes | not scored |
| T1 | without June 2009 | security_slope | 0.0317 | not scored |
| T1 | without June 2009 | landscape_slope | 0.0110 | not scored |
| T1 | without June 2009 | outcome | FAIL | not scored |
| T1 | Junes after the last pre-period break | cleaning_slope | not run: too few Junes (THESIS section 5) | not scored |
| T1 | Junes after the last pre-period break | security_slope | 0.0127 | not scored |
| T1 | Junes after the last pre-period break | landscape_slope | 0.0118 | not scored |
| T1 | 2007-2008 added | outcome | not run: June 2007 and 2008 are PDF only, extracted after the seal | not scored |
| T2 | 2007-2008 added | outcome | not run: June 2007 and 2008 are PDF only, extracted after the seal | not scored |
| T2 | basic instead of gross | landscape_est | 0.2135 | not scored |
| T2 | basic instead of gross | pooled | 0.2135 | not scored |
| T2 | basic instead of gross | outcome | SURVIVE | not scored |
| T2 | median instead of 25th percentile | landscape_est | 0.1269 | not scored |
| T2 | median instead of 25th percentile | pooled | 0.1269 | not scored |
| T2 | median instead of 25th percentile | outcome | SURVIVE | not scored |
| T2 | dropping 2022 | landscape_est | 0.1961 | not scored |
| T2 | dropping 2022 | pooled | 0.1961 | not scored |
| T2 | dropping 2022 | outcome | SURVIVE | not scored |
| T2 | leaving out cashier | landscape_est | 0.2258 | not scored |
| T2 | leaving out cashier | pooled | 0.2258 | not scored |
| T2 | leaving out cashier | outcome | SURVIVE | not scored |
| T2 | leaving out food/drink stall assistant | landscape_est | 0.2260 | not scored |
| T2 | leaving out food/drink stall assistant | pooled | 0.2260 | not scored |
| T2 | leaving out food/drink stall assistant | outcome | SURVIVE | not scored |
| T2 | leaving out general office clerk | landscape_est | 0.2136 | not scored |
| T2 | leaving out general office clerk | pooled | 0.2136 | not scored |
| T2 | leaving out general office clerk | outcome | SURVIVE | not scored |
| T2 | leaving out kitchen assistant | landscape_est | 0.2278 | not scored |
| T2 | leaving out kitchen assistant | pooled | 0.2278 | not scored |
| T2 | leaving out kitchen assistant | outcome | SURVIVE | not scored |
| T2 | leaving out lorry driver | landscape_est | 0.2087 | not scored |
| T2 | leaving out lorry driver | pooled | 0.2087 | not scored |
| T2 | leaving out lorry driver | outcome | SURVIVE | not scored |
| T2 | leaving out shop sales assistant | landscape_est | 0.2264 | not scored |
| T2 | leaving out shop sales assistant | pooled | 0.2264 | not scored |
| T2 | leaving out shop sales assistant | outcome | SURVIVE | not scored |
| T2 | leaving out van driver | landscape_est | 0.2069 | not scored |
| T2 | leaving out van driver | pooled | 0.2069 | not scored |
| T2 | leaving out van driver | outcome | SURVIVE | not scored |
| T2 | leaving out waiter | landscape_est | 0.2253 | not scored |
| T2 | leaving out waiter | pooled | 0.2253 | not scored |
| T2 | leaving out waiter | outcome | SURVIVE | not scored |
| T2 | first transition June counted as post | landscape_est | 0.1798 | not scored |
| T2 | first transition June counted as post | pooled | 0.1798 | not scored |
| T2 | first transition June counted as post | outcome | SURVIVE | not scored |
| T2 | all successors of a grade split averaged | landscape_est | 0.2201 | not scored |
| T2 | all successors of a grade split averaged | pooled | 0.2201 | not scored |
| T2 | all successors of a grade split averaged | outcome | SURVIVE | not scored |
| T2 | Number Covered weights | landscape_est | 0.2581 | not scored |
| T2 | Number Covered weights | pooled | 0.2581 | not scored |
| T2 | Number Covered weights | outcome | SURVIVE | not scored |
| T4 | LFS residents series | outcome | not run: no second series qualifies | not scored |
| T5 | all successors averaged | landscape_2017_ratio | 1.0000 | not scored |
| T5 | all successors averaged | landscape_2018_ratio | 1.0000 | not scored |
| T5 | all successors averaged | landscape_2019_ratio | 1.0385 | not scored |
| T5 | all successors averaged | landscape_2022_ratio | 1.0000 | not scored |
| T5 | all successors averaged | outcome | SURVIVE | not scored |

## Titles dropped by the missing-year rule

None.
