# RESULTS: COE or ERP -- which one actually keeps Singapore's roads moving?

Scored against THESIS.md as sealed in commit `6d2a345` (md5 `2f99e6513de2f5ebe7f578e6a5650f50`, checked by this script before it writes a line). Written by `13_results.py` from `out/`; every number below is in `number_manifest.csv`. Anything learned after the seal is in `THESIS_ADDENDUM.md` and changes no score.

## Summary

| Test | Outcome | Held | Jacob's confidence |
|---|---|---|---|
| T1 | FAIL | no | 35% |
| T3 | FAIL | no | 20% |
| T4 | MIXED | no | 70% |
| T2 | PASS | yes | 65% |

**Held: 1 of 4**, against an expected 1.9 of 4. **Brier score: 0.194** (mean of (confidence - outcome)^2, outcome 1 if held, 0 otherwise; no test dropped out).

**Verdict (section 8): The record cannot tell the two apart.**

> A pass for the ERP reading is weak evidence and a COE-like result is strong evidence, because the design leans toward the ERP reading.

Tests that did not hold come first.

## T1. Thermostat band (the ERP signature): FAIL

Jacob's confidence that it would hold: **35%**. Outcome: **FAIL**.

Sealed wording:

> - **Scored years.** Expressways, 16 years: 2004-2010, 2012-2018, 2024, 2025.
>   Arterials, 19 years: 2004-2010, 2012-2019, 2022-2025 (section 5).
>
> - **Prediction.** In every scored year, expressway peak speed lies within
>   45-65 km/h and arterial peak speed within 20-30 km/h.
>
> - **Survive if:** every scored year, both road classes, inside the band.
>
> - **Fail if:** any scored year, either road class, outside the band. Years below
>   the band and years above it are counted and reported separately, because they
>   mean different things (below: the buffet; above: the charge is higher than
>   congestion needs).
>
> - **Informativeness condition, fixed now.** T1 only says something if the
>   "weather" changed. For each road class, over its scored years, the range of the
>   car population (maximum minus minimum) is computed as a share of its mean,
>   over the scored years that have a car population (2004 has none). If
>   that share is below 10 per cent (judgement), T1 is reported as scored but
>   uninformative for that road class: speeds stayed flat while car numbers also
>   stayed flat. The COE premium range (E4b) over the same years is reported
>   alongside, descriptively.

Result:

- Expressway, 16 scored years, band 45-65 km/h (read as closed, so a value equal to an edge is inside): 0 above, 0 below.
- Arterial, 19 scored years, band 20-30 km/h (read as closed, so a value equal to an edge is inside): 2 above, 0 below (2016 2023).
  - 2016: 30.4 km/h
  - 2023: 31 km/h
- Informativeness: car population range over the scored years with a car count was 38.0 per cent of its mean (expressway years) and 37.3 per cent (arterial years), above the 10 per cent line, so the test was informative.
- No scored year sat below either band, so this failure is on the high side: arterial roads ran faster than the band, the opposite of the buffet.

## T3. Door fee and usage (the COE mechanism): FAIL

Jacob's confidence that it would hold: **20%**. Outcome: **FAIL**.

Sealed wording:

> - **Years.** 2005-2018, every year E2 and E4b both cover (14 points). Split
>   into the 7 years with the highest annual premium and the 7 with the lowest
>   (section 4); a tie at the boundary goes to the high half. The 2010-2013
>   premium run named in the brief falls inside this window.
>
> - **Prediction.** Mean km per car in the high-premium years is **no more than 3
>   per cent below** the mean in the low-premium years.
>
> - **Survive if:** the high-premium mean is at least 97 per cent of the
>   low-premium mean.
>
> - **Fail if:** it is below 97 per cent: owners drove measurably less when the
>   door fee was high, which is the door fee doing some of ERP's work.

Result:

- High-premium years (2011 2012 2013 2014 2015 2016 2017): mean 17,600 km per car.
- Low-premium years (2005 2006 2007 2008 2009 2010 2018): mean 19,772 km per car.
- Ratio 0.890: the high-premium years were 11.0 per cent lower, beyond the 3 per cent line.
- The E2 page's sampling error is not recorded in anything retrieved, so the below-resolution rule did not apply and T3 is scored.
- Hire and rental cars (E3) grew by 54,736 over the high-premium years and by 5,591 over the low-premium years. The private-hire bias named at the seal therefore pushed toward PASS, not FAIL; T3 failed anyway. See THESIS_ADDENDUM.md, item 1.

| Year | Premium (A+B mean, S$) | km per car | Half |
|---|---|---|---|
| 2005 | 16,130 | 20,603 | low |
| 2006 | 11,808 | 21,100 | low |
| 2007 | 15,019 | 20,800 | low |
| 2008 | 12,871 | 19,700 | low |
| 2009 | 12,006 | 19,600 | low |
| 2010 | 35,119 | 19,100 | low |
| 2011 | 56,572 | 19,000 | high |
| 2012 | 74,164 | 18,200 | high |
| 2013 | 76,701 | 17,800 | high |
| 2014 | 70,478 | 17,500 | high |
| 2015 | 63,726 | 17,300 | high |
| 2016 | 50,854 | 16,700 | high |
| 2017 | 48,895 | 16,700 | high |
| 2018 | 34,191 | 17,500 | low |

## T4. The premium adds little once car numbers are known (magnitude): MIXED

Jacob's confidence that it would hold: **70%**. Outcome: **MIXED**.

Sealed wording:

> - **Estimate.** For each road class, over 2005-2025 less 2020 and 2021 (19
>   points; every year E1, E3 or E3b, and E4b all cover): OLS of log(speed) on
>   log(car population), then again with log(annual premium) added. Run on car population rather than cars
>   per lane-km so that the years are not limited by E8; the density version is
>   reported as a sensitivity, not scored.
>
> - **Prediction.** Adding the premium raises adjusted R-squared by less than 0.10,
>   **and** the premium's 90 per cent interval includes zero, for both road classes.
>
> - **Survive if:** both conditions hold for both road classes.
>
> - **Fail if:** for either road class, the adjusted R-squared gain is 0.10 or more
>   **and** the premium's interval excludes zero.
>
> - **Otherwise:** reported as mixed.

Result:

| Road | Adj. R-squared gain | Premium coefficient | 90% interval | Includes zero | Status |
|---|---|---|---|---|---|
| expressway | -0.020 | -0.013 | -0.032 to 0.007 | True | pass |
| arterial | 0.070 | 0.028 | 0.009 to 0.046 | False | mixed |

2005-2025 less 2020 and 2021, 19 points. Expressways pass both conditions. On arterial roads the gain is under 0.10 but the premium's interval excludes zero, which is neither the survive nor the fail condition: mixed, so T4 does not hold.

Density sensitivity, 2005-2017, not scored: premium coefficient expressway -0.001 (-0.012 to 0.011), gain -0.108; arterial 0.043 (0.021 to 0.064), gain 0.370.

On that unscored density version the arterial result meets the sealed fail condition (gain 0.10 or more and an interval that excludes zero). It is not the sealed specification and changes nothing above. It does point the same way as the scored arterial result: on arterial roads the premium carries information about speed beyond the car count.

## T2. Insensitivity to car density (magnitude): PASS

Jacob's confidence that it would hold: **65%**. Outcome: **PASS**.

Sealed wording:

> - **Main specification.** For each road class separately, OLS of log(annual peak
>   speed) on log(cars per lane-km of that road class) (section 4), over
>   2005-2017: every year E1, E3 and E8 all cover (13 points; no excluded year
>   falls inside). The slope is the elasticity: the per cent change in peak
>   speed for a 1 per cent change in cars per lane-km. Reported with a 90 per cent interval (HC1).
>
> - **Prediction.** For both road classes, the main-specification elasticity lies
>   between -0.5 and +0.5.
>
> - **Survive if:** both point estimates lie in [-0.5, +0.5].
>
> - **Fail if:** either point estimate is at or below -1.0 (speed falls at least
>   one for one with car density: the buffet signature).
>
> - **Between -1.0 and -0.5, on either road class:** inconclusive, and published
>   as inconclusive rather than rounded to either side.

Result:

| Road | Elasticity | 90% interval | R-squared | Status |
|---|---|---|---|---|
| expressway | -0.016 | -0.107 to 0.076 | 0.00 | survive |
| arterial | 0.254 | 0.158 to 0.350 | 0.26 | survive |

Main specification: log(peak speed) on log(cars per lane-km of the same road class), 2005-2017, 13 points, OLS with HC1 errors. Both elasticities sit inside [-0.5, +0.5]. On arterial roads the slope is positive: speeds rose while crowding rose. Over the same years cars per lane-km rose 22 per cent on expressways and 25 per cent on arterial roads.

Sensitivities, reported, not scored:

| Specification | Road | n | Elasticity | 90% interval | R-squared |
|---|---|---|---|---|---|
| sens ii: main + linear trend | expressway | 13 | 0.088 | -0.026 to 0.203 | 0.21 |
| sens iii: private cars per lane-km | expressway | 13 | 0.051 | -0.098 to 0.201 | 0.03 |
| sens i: log car population | expressway | 19 | -0.164 | -0.275 to -0.054 | 0.26 |
| sens ii: main + linear trend | arterial | 13 | -0.085 | -0.172 to 0.001 | 0.92 |
| sens iii: private cars per lane-km | arterial | 13 | 0.211 | 0.054 to 0.369 | 0.12 |
| sens i: log car population | arterial | 19 | 0.304 | 0.202 to 0.406 | 0.60 |
| sens iv: E8b's 2008 arterial lane-km | arterial | 13 | 0.252 | 0.157 to 0.347 | 0.26 |

With a linear trend added the arterial slope turns negative (-0.085) and the fit's R-squared rises to 0.92: arterial speeds rose steadily over time, and crowding cannot be separated from that drift in 13 annual points.

## Verdict

> Scored on T1 and T2 only. T3 and T4 test the COE mechanism and are reported
> beside the verdict, not inside it.
>
> - **"The record looks more like extreme ERP"**: T1 survives (and is informative)
>   **and** T2 survives on both road classes.
> - **"The record looks more like extreme COE"**: T1 fails with 3 or more scored
>   years below the band on either road class, **or** T2 fails on either road
>   class.
> - **Anything else: "the record cannot tell the two apart"**, and that is the
>   published finding, stated as plainly as either of the other two.
>

T1 failed, but with 0 expressway and 0 arterial years below the band, not 3 or more; T2 passed on both road classes. Neither the ERP condition (which needs T1 to survive) nor the COE condition is met, so: **The record cannot tell the two apart.**

> A pass for the ERP reading is weak evidence and a COE-like result is strong evidence, because the design leans toward the ERP reading.

And the thermostat problem, as the seal requires: the design shows a signature, not a cause.

## T5 leg (a), reported, not scored

Leg (a) met: **no**. Neither road class shows an elasticity at or below -1.0 (expressway -0.016, arterial 0.254), so the COE-win mirror did not appear. Leg (b) was untestable, as sealed.

## S1, total car-km, descriptive

Cars x km per car, 2005-2018: 9.03 billion km in 2005, a peak of 11.47 billion in 2011, 10.77 billion in 2018. No prediction, no score, no weight in the verdict.

## T6, 2020 and 2021, descriptive

Peak speed in 2020 and 2021: expressways 64 and 63 km/h, arterial roads 31 and 32 km/h. Not scored; the circuit breaker emptied the roads in the same weeks that ERP charging stopped.

## Charts

- `figs/chart1_speed_vs_band.svg`: peak speed against LTA's bands, both road types, with cars per lane-km underneath.
- `figs/chart2_door_fee.svg`: km per car in the 7 highest- and 7 lowest-premium years.
