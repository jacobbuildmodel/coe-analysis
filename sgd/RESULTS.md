# RESULTS: the Singapore dollar, the yen and the ringgit

Written by `13_results.py` from `out/`. Tests as sealed in `THESIS.md` (commit 9e46034); failures first. Outcome labels as sealed: SURVIVE, FAIL, INCONCLUSIVE, NOT SCORED. Confidences are Jacob's, set at the seal.

Windows: scored 2021-01 to 2025-12; long 2005-08 to 2026-08.

## What did not hold (failures first)

- T3. The ringgit: most of the rise was the ringgit falling: FAIL (Jacob's confidence 8%).

## Gate C. The BIS index stands in for MAS's own: PASS

A gate, not a scored test: no confidence, not in the scorecard. Sealed wording (THESIS.md, verbatim):

> **Pass if:** the correlation >= 0.90, on at least 120 monthly changes.

- correlation of monthly log changes, BIS broad index against MAS's S$NEER: 0.9240, on 331 monthly changes (lines 0.90 and 120). THESIS fixes no interval for it.
- T4 and T7 are read as sealed.

## The scored tests, failures first

### T3. The ringgit: most of the rise was the ringgit falling: FAIL (Jacob's confidence at seal: 8%)

Sealed wording (THESIS.md, verbatim):

> **Prediction.** At least half of the Singapore dollar's rise against the ringgit from January 2021 to December 2025 came from the ringgit falling against everyone. And more of it came from the ringgit falling than from the Singapore dollar rising.
>
> **Survive if:** P_MYR >= 0.50 and P_MYR > S_MYR.
>
> **Fail if:** S_MYR >= P_MYR.

- change in the cross rate b 0.0486; Singapore dollar's broad index s 0.1234; partner's broad index 0.0829; residual 0.0081.
- shares of the rise: Singapore dollar rising 2.5386, partner falling -1.7058, neither 0.1672. No sampling interval: each share is a ratio of two level changes.

### T1. The split closes (the design test): SURVIVE (Jacob's confidence at seal: 55%)

Sealed wording (THESIS.md, verbatim):

> **Prediction.** For both currencies and on both windows, the broad indices account for at least 80 per cent of the bilateral move, and the BIS cross is within 0.5 per cent of MAS's rate on average.
>
> **Survive if:** |R_X| <= 0.20 and the mean absolute difference (b) <= 0.005, for both JPY and MYR, on both windows.
>
> **Fail if:** |R_X| > 0.20 or the mean absolute difference (b) > 0.005, for either currency on either window.

- JPY, January 2021 to December 2025: change in the cross rate 0.4018; residual share -0.0392 (line 0.20 in size), BIS against MAS 0.0006 on 60 months (line 0.005); passes.
- MYR, January 2021 to December 2025: change in the cross rate 0.0486; residual share 0.1672 (line 0.20 in size), BIS against MAS 0.0003 on 60 months (line 0.005); passes.
- JPY, August 2005 on: change in the cross rate 0.6263; residual share -0.0782 (line 0.20 in size), BIS against MAS 0.0007 on 253 months (line 0.005); passes.
- MYR, August 2005 on: change in the cross rate 0.3449; residual share -0.0663 (line 0.20 in size), BIS against MAS 0.0004 on 253 months (line 0.005); passes.
- THESIS fixes no interval for T1: each check is a comparison of levels.

### T2. The yen: most of the rise was the yen falling: SURVIVE (Jacob's confidence at seal: 90%)

Sealed wording (THESIS.md, verbatim):

> **Prediction.** At least half of the Singapore dollar's rise against the yen from January 2021 to December 2025 came from the yen falling against everyone. And more of it came from the yen falling than from the Singapore dollar rising.
>
> **Survive if:** P_JPY >= 0.50 and P_JPY > S_JPY.
>
> **Fail if:** S_JPY >= P_JPY.

- change in the cross rate b 0.4018; Singapore dollar's broad index s 0.1234; partner's broad index -0.2942; residual -0.0157.
- shares of the rise: Singapore dollar rising 0.3070, partner falling 0.7321, neither -0.0392. No sampling interval: each share is a ratio of two level changes.

### T4. The slow path: the Singapore dollar is the steadiest in the set: SURVIVE (Jacob's confidence at seal: 80%)

Sealed wording (THESIS.md, verbatim):

> **Prediction.** The Singapore dollar's broad index is the steadiest or second steadiest of the 11.
>
> **Survive if:** SGD's rank <= 2.
>
> **Fail if:** SGD's rank >= 6 (steadier than at most five of the ten partners).

- monthly swing of each broad index (standard deviation of the monthly log change): SG 0.0047, HK 0.0100, CN 0.0110, XM 0.0111, MY 0.0115, US 0.0128, TH 0.0129, KR 0.0186, ID 0.0195, AU 0.0208, JP 0.0216.
- 11 of 11 present; the Singapore dollar ranks 1 and is steadier than 10 partners. THESIS fixes no interval for T4: it is a rank.

### T7. Policy or growth: what the broad path followed: SURVIVE (Jacob's confidence at seal: 35%)

Sealed wording (THESIS.md, verbatim):

> **Prediction.** The broad path lines up with MAS's decisions clearly better than with growth.
>
> **Survive if:** D >= 0.20 and rho_p > 0.
>
> **Fail if:** D <= 0 (growth lines up at least as well).

- 61 intervals (1 dropped for a missing value).
- rho with MAS's decisions 0.4653; rho with growth 0.1127; D 0.3526 (90% bootstrap interval 0.1117 to 0.5867, reported, not used in the rule).
- gate C beside it: correlation 0.9240 on 331 monthly changes.

## Scorecard

- Scored: T1 T2 T3 T4 T7 (5); held: 4. Gate C is not counted; a test not scored drops out of the count and the Brier score.
- T1: SURVIVE; Jacob's confidence at seal 55%.
- T2: SURVIVE; Jacob's confidence at seal 90%.
- T3: FAIL; Jacob's confidence at seal 8%.
- T4: SURVIVE; Jacob's confidence at seal 80%.
- T7: SURVIVE; Jacob's confidence at seal 35%.
- Held 4 of 5 scored, against an expected 2.680 (the sum of Jacob's confidences for the tests scored; 2.68 if all five are scored).
- Brier score: 0.136 (mean over the scored tests).

## Verdict (THESIS section 8)

**Most of the Singapore dollar's rise against the yen was the yen falling against everyone; most of the Singapore dollar's rise against the ringgit was the Singapore dollar rising against everyone; the broad path followed MAS's decisions more closely than growth.**

- **Part A, the yen:** most of the Singapore dollar's rise against the yen was the yen falling against everyone.
- **Part A, the ringgit:** most of the Singapore dollar's rise against the ringgit was the Singapore dollar rising against everyone.
  - Weak evidence, stated at the seal (T3): Malaysia and Singapore sit heavily in each other's baskets. So part of the ringgit's fall shows up as the Singapore dollar "rising against everyone", and part of the Singapore dollar's rise shows up as the ringgit "falling against everyone". A result either way is weaker evidence for the ringgit than for the yen.
- The long-run split (August 2005 on) is reported with the sensitivities and does not change Part A.
- **Part B, the broad path:** the broad path followed MAS's decisions more closely than growth.
  - Weak evidence, stated at the seal (T7): The design leans toward the rival. The band is the path MAS keeps the index on, so a score that describes the band will match the index's path wherever MAS held the index inside it. A result that the path followed MAS's decisions is weak evidence that MAS rather than the economy moved the Singapore dollar. A result that it followed growth at least as closely is strong evidence against the rival.
- Gate C beside Part B: correlation 0.9240 on 331 monthly changes.
- T4 is reported with the verdict and does not change its wording: SURVIVE.

## Sensitivities and descriptive checks (reported, NOT SCORED)

Every row is a sealed sensitivity or descriptive check (THESIS sections 5, 6 and 7). None enters the score or the verdict.

| Test | Variant | Key | Value | Scored |
|---|---|---|---|---|
| T7 | lagged growth | rho_p | 0.4653 | not scored |
| T7 | lagged growth | rho_g | 0.1924 | not scored |
| T7 | lagged growth | D | 0.2729 | not scored |
| T7 | lagged growth | intervals | 61.0000 | not scored |
| T7 | CPI inflation | rho_p | 0.4653 | not scored |
| T7 | CPI inflation | rho_g | 0.5074 | not scored |
| T7 | CPI inflation | D | -0.0421 | not scored |
| T7 | CPI inflation | intervals | 61.0000 | not scored |
| T7 | finer slope coding | rho_p | 0.4587 | not scored |
| T7 | finer slope coding | rho_g | 0.1127 | not scored |
| T7 | finer slope coding | D | 0.3460 | not scored |
| T7 | finer slope coding | intervals | 61.0000 | not scored |
| T7 | intervals from 2010 | rho_p | 0.5490 | not scored |
| T7 | intervals from 2010 | rho_g | 0.0335 | not scored |
| T7 | intervals from 2010 | D | 0.5155 | not scored |
| T7 | intervals from 2010 | intervals | 41.0000 | not scored |
| B | scored | B_scored_JPY_pi | 1.0103 | not scored |
| B | scored | B_scored_JPY_sigma | 0.0679 | not scored |
| B | scored | B_scored_MYR_pi | 0.9060 | not scored |
| B | scored | B_scored_MYR_sigma | 0.1680 | not scored |
| B | scored | B_scored_KRW_pi | 1.0248 | not scored |
| B | scored | B_scored_KRW_sigma | 0.0320 | not scored |
| B | scored | B_scored_CNY_pi | 1.0305 | not scored |
| B | scored | B_scored_CNY_sigma | 0.2716 | not scored |
| B | scored | B_scored_THB_pi | 0.9059 | not scored |
| B | scored | B_scored_THB_sigma | 0.0688 | not scored |
| B | scored | B_scored_IDR_pi | 0.9565 | not scored |
| B | scored | B_scored_IDR_sigma | 0.0799 | not scored |
| B | scored | B_scored_USD_pi | 1.0001 | not scored |
| B | scored | B_scored_USD_sigma | 0.0023 | not scored |
| B | scored | B_scored_EUR_pi | 0.6334 | not scored |
| B | scored | B_scored_EUR_sigma | 0.1130 | not scored |
| B | scored | B_scored_AUD_pi | 0.9641 | not scored |
| B | scored | B_scored_AUD_sigma | 0.0205 | not scored |
| B | scored | B_scored_HKD_pi | 0.9110 | not scored |
| B | scored | B_scored_HKD_sigma | 0.0062 | not scored |
| B | scored | B_scored_partner_larger_count | 10.0000 | not scored |
| B | long | B_long_JPY_pi | 1.0099 | not scored |
| B | long | B_long_JPY_sigma | 0.0739 | not scored |
| B | long | B_long_MYR_pi | 1.0429 | not scored |
| B | long | B_long_MYR_sigma | 0.0378 | not scored |
| B | long | B_long_KRW_pi | 1.0504 | not scored |
| B | long | B_long_KRW_sigma | 0.0383 | not scored |
| B | long | B_long_CNY_pi | 0.9221 | not scored |
| B | long | B_long_CNY_sigma | 0.2859 | not scored |
| B | long | B_long_THB_pi | 0.9196 | not scored |
| B | long | B_long_THB_sigma | 0.1129 | not scored |
| B | long | B_long_IDR_pi | 1.0090 | not scored |
| B | long | B_long_IDR_sigma | 0.0444 | not scored |
| B | long | B_long_USD_pi | 0.9677 | not scored |
| B | long | B_long_USD_sigma | 0.2115 | not scored |
| B | long | B_long_EUR_pi | 0.6998 | not scored |
| B | long | B_long_EUR_sigma | 0.1154 | not scored |
| B | long | B_long_AUD_pi | 1.0240 | not scored |
| B | long | B_long_AUD_sigma | -0.0209 | not scored |
| B | long | B_long_HKD_pi | 0.7939 | not scored |
| B | long | B_long_HKD_sigma | 0.2121 | not scored |
| B | long | B_long_partner_larger_count | 10.0000 | not scored |
| Q1 | long run | long_JPY_b | 0.6263 | not scored |
| Q1 | long run | long_JPY_S | 0.5724 | not scored |
| Q1 | long run | long_JPY_P | 0.5058 | not scored |
| Q1 | long run | long_JPY_R | -0.0782 | not scored |
| Q1 | single-month endpoints, scored | single-month_scored_JPY_b | 0.4333 | not scored |
| Q1 | single-month endpoints, scored | single-month_scored_JPY_S | 0.2921 | not scored |
| Q1 | single-month endpoints, scored | single-month_scored_JPY_P | 0.7537 | not scored |
| Q1 | single-month endpoints, scored | single-month_scored_JPY_R | -0.0459 | not scored |
| Q1 | end-of-period rates, scored | end-of-period_scored_JPY_b | 0.4024 | not scored |
| Q1 | end-of-period rates, scored | end-of-period_scored_JPY_S | 0.3066 | not scored |
| Q1 | end-of-period rates, scored | end-of-period_scored_JPY_P | 0.7311 | not scored |
| Q1 | end-of-period rates, scored | end-of-period_scored_JPY_R | -0.0377 | not scored |
| Q1 | real indices, scored | real_scored_JPY_b | 0.4018 | not scored |
| Q1 | real indices, scored | real_scored_JPY_S | 0.3419 | not scored |
| Q1 | real indices, scored | real_scored_JPY_P | 0.7680 | not scored |
| Q1 | real indices, scored | real_scored_JPY_R | -0.1098 | not scored |
| Q1 | single-month endpoints, long | single-month_long_JPY_b | 0.6260 | not scored |
| Q1 | single-month endpoints, long | single-month_long_JPY_S | 0.5688 | not scored |
| Q1 | single-month endpoints, long | single-month_long_JPY_P | 0.5122 | not scored |
| Q1 | single-month endpoints, long | single-month_long_JPY_R | -0.0810 | not scored |
| Q1 | end-of-period rates, long | end-of-period_long_JPY_b | 0.6226 | not scored |
| Q1 | end-of-period rates, long | end-of-period_long_JPY_S | 0.5758 | not scored |
| Q1 | end-of-period rates, long | end-of-period_long_JPY_P | 0.5089 | not scored |
| Q1 | end-of-period rates, long | end-of-period_long_JPY_R | -0.0846 | not scored |
| Q1 | real indices, long | real_long_JPY_b | 0.6263 | not scored |
| Q1 | real indices, long | real_long_JPY_S | 0.4740 | not scored |
| Q1 | real indices, long | real_long_JPY_P | 1.0349 | not scored |
| Q1 | real indices, long | real_long_JPY_R | -0.5089 | not scored |
| Q1 | long run | long_MYR_b | 0.3449 | not scored |
| Q1 | long run | long_MYR_S | 1.0394 | not scored |
| Q1 | long run | long_MYR_P | 0.0269 | not scored |
| Q1 | long run | long_MYR_R | -0.0663 | not scored |
| Q1 | single-month endpoints, scored | single-month_scored_MYR_b | 0.0399 | not scored |
| Q1 | single-month endpoints, scored | single-month_scored_MYR_S | 3.1752 | not scored |
| Q1 | single-month endpoints, scored | single-month_scored_MYR_P | -2.3901 | not scored |
| Q1 | single-month endpoints, scored | single-month_scored_MYR_R | 0.2149 | not scored |
| Q1 | end-of-period rates, scored | end-of-period_scored_MYR_b | 0.0410 | not scored |
| Q1 | end-of-period rates, scored | end-of-period_scored_MYR_S | 3.0098 | not scored |
| Q1 | end-of-period rates, scored | end-of-period_scored_MYR_P | -2.0224 | not scored |
| Q1 | end-of-period rates, scored | end-of-period_scored_MYR_R | 0.0126 | not scored |
| Q1 | real indices, scored | real_scored_MYR_b | 0.0486 | not scored |
| Q1 | real indices, scored | real_scored_MYR_S | 2.8266 | not scored |
| Q1 | real indices, scored | real_scored_MYR_P | -0.7849 | not scored |
| Q1 | real indices, scored | real_scored_MYR_R | -1.0416 | not scored |
| Q1 | single-month endpoints, long | single-month_long_MYR_b | 0.3426 | not scored |
| Q1 | single-month endpoints, long | single-month_long_MYR_S | 1.0393 | not scored |
| Q1 | single-month endpoints, long | single-month_long_MYR_P | 0.0287 | not scored |
| Q1 | single-month endpoints, long | single-month_long_MYR_R | -0.0680 | not scored |
| Q1 | end-of-period rates, long | end-of-period_long_MYR_b | 0.3500 | not scored |
| Q1 | end-of-period rates, long | end-of-period_long_MYR_S | 1.0241 | not scored |
| Q1 | end-of-period rates, long | end-of-period_long_MYR_P | 0.0265 | not scored |
| Q1 | end-of-period rates, long | end-of-period_long_MYR_R | -0.0506 | not scored |
| Q1 | real indices, long | real_long_MYR_b | 0.3449 | not scored |
| Q1 | real indices, long | real_long_MYR_S | 0.8609 | not scored |
| Q1 | real indices, long | real_long_MYR_P | 0.1323 | not scored |
| Q1 | real indices, long | real_long_MYR_R | 0.0068 | not scored |
| world | long | HK_US_sd_ratio | 0.7798 | not scored |
| world | long | HK_US_corr | 0.9248 | not scored |
| world | long | JP_rank | 11.0000 | not scored |
| world | scored | SG_rank_scored_window | 1.0000 | not scored |
| world | scored | present_scored_window | 11.0000 | not scored |

## Post-results numbers for the article (NOT SCORED)

Written by `11b_postresults.py` from `out/` (THESIS_ADDENDUM item 5): per-cent forms (100 x (exp(x) - 1)) of log changes, shares in per cent, rounded forms of tested numbers, and the specimen. None changes a sealed number, outcome or the verdict.

| Key | Printed | Meaning |
|---|---|---|
| spec_sgd_per_100jpy_2021_01 | 1.28 | MAS monthly average, S$ per 100 yen, January 2021 |
| spec_yen_per_budget_2021_01 | 78,000 | yen bought by a S$1,000 budget, January 2021, to the nearest 1,000 |
| spec_sgd_per_100jpy_2025_12 | 0.83 | MAS monthly average, S$ per 100 yen, December 2025 |
| spec_yen_per_budget_2025_12 | 121,000 | yen bought by a S$1,000 budget, December 2025, to the nearest 1,000 |
| T2_b_pct | 49.5 | the Singapore dollar against the yen, Jan 2021 to Dec 2025, per cent, up |
| T2_b_pct0 | 49 | the Singapore dollar against the yen, Jan 2021 to Dec 2025, per cent, up, whole |
| T2_s_pct | 13.1 | the Singapore dollar's broad index (against everyone), per cent, up |
| T2_s_pct0 | 13 | the Singapore dollar's broad index (against everyone), per cent, up, whole |
| T2_nx_pct | 25.5 | the yen's broad index (against everyone), per cent, down |
| T2_nx_pct0 | 25 | the yen's broad index (against everyone), per cent, down, whole |
| T2_S_share | 30.7 | share: the Singapore dollar rising against everyone, per cent of the rise |
| T2_S_share0 | 31 | share: the Singapore dollar rising against everyone, per cent of the rise, whole |
| T2_P_share | 73.2 | share: the yen falling against everyone, per cent of the rise |
| T2_P_share0 | 73 | share: the yen falling against everyone, per cent of the rise, whole |
| T2_R_share | 3.9 | share: neither broad index (the residual), per cent of the rise, negative (printed without sign) |
| T2_R_share0 | 4 | share: neither broad index (the residual), per cent of the rise, negative (printed without sign), whole |
| T3_b_pct | 5.0 | the Singapore dollar against the ringgit, Jan 2021 to Dec 2025, per cent, up |
| T3_b_pct0 | 5 | the Singapore dollar against the ringgit, Jan 2021 to Dec 2025, per cent, up, whole |
| T3_s_pct | 13.1 | the Singapore dollar's broad index (against everyone), per cent, up |
| T3_s_pct0 | 13 | the Singapore dollar's broad index (against everyone), per cent, up, whole |
| T3_nx_pct | 8.6 | the ringgit's broad index (against everyone), per cent, up |
| T3_nx_pct0 | 9 | the ringgit's broad index (against everyone), per cent, up, whole |
| T3_S_share | 253.9 | share: the Singapore dollar rising against everyone, per cent of the rise |
| T3_S_share0 | 254 | share: the Singapore dollar rising against everyone, per cent of the rise, whole |
| T3_P_share | 170.6 | share: the ringgit falling against everyone, per cent of the rise, negative (printed without sign) |
| T3_P_share0 | 171 | share: the ringgit falling against everyone, per cent of the rise, negative (printed without sign), whole |
| T3_R_share | 16.7 | share: neither broad index (the residual), per cent of the rise |
| T3_R_share0 | 17 | share: neither broad index (the residual), per cent of the rise, whole |
| T1_scored_MYR_R_share | 16.7 | T1: the ringgit's residual, scored window, per cent of the rise |
| T1_scored_MYR_R_share0 | 17 | T1: the ringgit's residual, scored window, per cent of the rise, whole |
| long_JPY_b_pct | 87.1 | the Singapore dollar against the yen, Aug 2005 on (sensitivity), per cent, up |
| long_JPY_b_pct0 | 87 | the Singapore dollar against the yen, Aug 2005 on (sensitivity), per cent, up, whole |
| long_JPY_S_share | 57.2 | long run: the Singapore dollar rising against everyone, per cent of the rise |
| long_JPY_S_share0 | 57 | long run: the Singapore dollar rising against everyone, per cent of the rise, whole |
| long_JPY_P_share | 50.6 | long run: the yen falling against everyone, per cent of the rise |
| long_JPY_P_share0 | 51 | long run: the yen falling against everyone, per cent of the rise, whole |
| gateC_r_2dp | 0.92 | gate C correlation, two decimals |
| T7_rho_p_2dp | 0.47 | T7: rank correlation with MAS's decisions, two decimals |
| T7_rho_g_2dp | 0.11 | T7: rank correlation with growth, two decimals |
| T7_D_2dp | 0.35 | T7: D, two decimals |
| T7_D_lo_2dp | 0.11 | T7: D, 90% interval, low, two decimals |
| T7_D_hi_2dp | 0.59 | T7: D, 90% interval, high, two decimals |
| HK_US_sd_ratio_2dp | 0.78 | world view: Hong Kong dollar's swing over the US dollar's, two decimals |
| HK_US_corr_2dp | 0.92 | world view: Hong Kong and US broad indices, correlation, two decimals |
| T7_cpi_rho_g_2dp | 0.51 | T7 with CPI inflation in place of growth: rank correlation with inflation (not scored) |
| T7_cpi_D_2dp | -0.04 | T7 with CPI inflation in place of growth: D (not scored) |
| T4_SG_sd_pct | 0.47 | T4: typical monthly move of SG's broad index, per cent |
| T4_HK_sd_pct | 1.00 | T4: typical monthly move of HK's broad index, per cent |
| T4_US_sd_pct | 1.28 | T4: typical monthly move of US's broad index, per cent |
| T4_JP_sd_pct | 2.16 | T4: typical monthly move of JP's broad index, per cent |
| expected_held_2dp | 2.68 | expected held, sum of Jacob's confidences |
| conf_T1_pct | 55 | Jacob's confidence at seal, T1, per cent |
| conf_T2_pct | 90 | Jacob's confidence at seal, T2, per cent |
| conf_T3_pct | 8 | Jacob's confidence at seal, T3, per cent |
| conf_T4_pct | 80 | Jacob's confidence at seal, T4, per cent |
| conf_T7_pct | 35 | Jacob's confidence at seal, T7, per cent |

## After outside review (added after outside review, not sealed, NOT SCORED)

Written by `16_review.py` from `out/` and raw/s1c, raw/s8 (THESIS_ADDENDUM item 10). None changes a sealed number, outcome, threshold or the verdict.

### review_a1_usd.csv

| Key | Printed | Meaning |
|---|---|---|
| A1_scored_JPY_b | 0.4018 | scored window: ln(X per SGD) change, = d ln(X per USD) - d ln(SGD per USD) |
| A1_scored_JPY_sgd_vs_usd_pct | 2.7 | scored window: the Singapore dollar against the US dollar, per cent, up |
| A1_scored_JPY_sgd_vs_usd_pct0 | 3 | scored window: the Singapore dollar against the US dollar, per cent, up, whole |
| A1_scored_JPY_x_vs_usd_pct | 31.3 | scored window: JPY against the US dollar, per cent, down |
| A1_scored_JPY_x_vs_usd_pct0 | 31 | scored window: JPY against the US dollar, per cent, down, whole |
| A1_scored_JPY_share_sgd | 0.0670 | scored window, JPY: the Singapore dollar's own move against the US dollar, share of the log change |
| A1_scored_JPY_share_sgd_pct0 | 7 | scored window, JPY: the Singapore dollar's own move against the US dollar, per cent of the log change, whole |
| A1_scored_JPY_share_x | 0.9330 | scored window, JPY: JPY's own fall against the US dollar, share of the log change |
| A1_scored_JPY_share_x_pct0 | 93 | scored window, JPY: JPY's own fall against the US dollar, per cent of the log change, whole |
| A1_scored_MYR_b | 0.0486 | scored window: ln(X per SGD) change, = d ln(X per USD) - d ln(SGD per USD) |
| A1_scored_MYR_sgd_vs_usd_pct | 2.7 | scored window: the Singapore dollar against the US dollar, per cent, up |
| A1_scored_MYR_sgd_vs_usd_pct0 | 3 | scored window: the Singapore dollar against the US dollar, per cent, up, whole |
| A1_scored_MYR_x_vs_usd_pct | 2.1 | scored window: MYR against the US dollar, per cent, down |
| A1_scored_MYR_x_vs_usd_pct0 | 2 | scored window: MYR against the US dollar, per cent, down, whole |
| A1_scored_MYR_share_sgd | 0.5543 | scored window, MYR: the Singapore dollar's own move against the US dollar, share of the log change |
| A1_scored_MYR_share_sgd_pct0 | 55 | scored window, MYR: the Singapore dollar's own move against the US dollar, per cent of the log change, whole |
| A1_scored_MYR_share_x | 0.4457 | scored window, MYR: MYR's own fall against the US dollar, share of the log change |
| A1_scored_MYR_share_x_pct0 | 45 | scored window, MYR: MYR's own fall against the US dollar, per cent of the log change, whole |
| A1_long_JPY_b | 0.6263 | long window: ln(X per SGD) change, = d ln(X per USD) - d ln(SGD per USD) |
| A1_long_JPY_sgd_vs_usd_pct | 30.6 | long window: the Singapore dollar against the US dollar, per cent, up |
| A1_long_JPY_sgd_vs_usd_pct0 | 31 | long window: the Singapore dollar against the US dollar, per cent, up, whole |
| A1_long_JPY_x_vs_usd_pct | 30.2 | long window: JPY against the US dollar, per cent, down |
| A1_long_JPY_x_vs_usd_pct0 | 30 | long window: JPY against the US dollar, per cent, down, whole |
| A1_long_JPY_share_sgd | 0.4263 | long window, JPY: the Singapore dollar's own move against the US dollar, share of the log change |
| A1_long_JPY_share_sgd_pct0 | 43 | long window, JPY: the Singapore dollar's own move against the US dollar, per cent of the log change, whole |
| A1_long_JPY_share_x | 0.5737 | long window, JPY: JPY's own fall against the US dollar, share of the log change |
| A1_long_JPY_share_x_pct0 | 57 | long window, JPY: JPY's own fall against the US dollar, per cent of the log change, whole |
| A1_long_MYR_b | 0.3449 | long window: ln(X per SGD) change, = d ln(X per USD) - d ln(SGD per USD) |
| A1_long_MYR_sgd_vs_usd_pct | 30.6 | long window: the Singapore dollar against the US dollar, per cent, up |
| A1_long_MYR_sgd_vs_usd_pct0 | 31 | long window: the Singapore dollar against the US dollar, per cent, up, whole |
| A1_long_MYR_x_vs_usd_pct | 7.5 | long window: MYR against the US dollar, per cent, down |
| A1_long_MYR_x_vs_usd_pct0 | 7 | long window: MYR against the US dollar, per cent, down, whole |
| A1_long_MYR_share_sgd | 0.7741 | long window, MYR: the Singapore dollar's own move against the US dollar, share of the log change |
| A1_long_MYR_share_sgd_pct0 | 77 | long window, MYR: the Singapore dollar's own move against the US dollar, per cent of the log change, whole |
| A1_long_MYR_share_x | 0.2259 | long window, MYR: MYR's own fall against the US dollar, share of the log change |
| A1_long_MYR_share_x_pct0 | 23 | long window, MYR: MYR's own fall against the US dollar, per cent of the log change, whole |

### review_a2_expair.csv

| Key | Printed | Meaning |
|---|---|---|
| A2_scored_JPY_w_in_sg | 6.1 | scored window: weight of JPY in Singapore's basket, per cent |
| A2_scored_JPY_w_sg_in_x | 2.7 | scored window: weight of SGD in JP's basket, per cent |
| A2_scored_JPY_s_ex | 0.1053 | scored window: SGD broad index without JPY, log change |
| A2_scored_JPY_n_ex | -0.2912 | scored window: JP broad index without SGD, log change |
| A2_scored_JPY_S | 0.2620 | scored window, JPY, ex-pair: the Singapore dollar rising, share of the log change |
| A2_scored_JPY_S_pct0 | 26 | scored window, JPY, ex-pair: the Singapore dollar rising, per cent of the log change, whole |
| A2_scored_JPY_P | 0.7246 | scored window, JPY, ex-pair: JPY falling, share of the log change |
| A2_scored_JPY_P_pct0 | 72 | scored window, JPY, ex-pair: JPY falling, per cent of the log change, whole |
| A2_scored_JPY_R | 0.0133 | scored window, JPY, ex-pair: the remainder, share of the log change |
| A2_scored_JPY_R_pct0 | 1 | scored window, JPY, ex-pair: the remainder, per cent of the log change, whole |
| A2_scored_MYR_w_in_sg | 13.1 | scored window: weight of MYR in Singapore's basket, per cent |
| A2_scored_MYR_w_sg_in_x | 12.6 | scored window: weight of SGD in MY's basket, per cent |
| A2_scored_MYR_s_ex | 0.1346 | scored window: SGD broad index without MYR, log change |
| A2_scored_MYR_n_ex | 0.1019 | scored window: MY broad index without SGD, log change |
| A2_scored_MYR_S | 2.7703 | scored window, MYR, ex-pair: the Singapore dollar rising, share of the log change |
| A2_scored_MYR_S_pct0 | 277 | scored window, MYR, ex-pair: the Singapore dollar rising, per cent of the log change, whole |
| A2_scored_MYR_P | -2.0960 | scored window, MYR, ex-pair: MYR falling, share of the log change |
| A2_scored_MYR_P_pct0 | 210 | scored window, MYR, ex-pair: MYR falling, per cent of the log change, whole, negative |
| A2_scored_MYR_R | 0.3257 | scored window, MYR, ex-pair: the remainder, share of the log change |
| A2_scored_MYR_R_pct0 | 33 | scored window, MYR, ex-pair: the remainder, per cent of the log change, whole |
| A2_long_JPY_w_in_sg | 8.4 | long window: weight of JPY in Singapore's basket, per cent |
| A2_long_JPY_w_sg_in_x | 2.7 | long window: weight of SGD in JP's basket, per cent |
| A2_long_JPY_s_ex | 0.3339 | long window: SGD broad index without JPY, log change |
| A2_long_JPY_n_ex | -0.3084 | long window: JP broad index without SGD, log change |
| A2_long_JPY_S | 0.5332 | long window, JPY, ex-pair: the Singapore dollar rising, share of the log change |
| A2_long_JPY_S_pct0 | 53 | long window, JPY, ex-pair: the Singapore dollar rising, per cent of the log change, whole |
| A2_long_JPY_P | 0.4924 | long window, JPY, ex-pair: JPY falling, share of the log change |
| A2_long_JPY_P_pct0 | 49 | long window, JPY, ex-pair: JPY falling, per cent of the log change, whole |
| A2_long_JPY_R | -0.0256 | long window, JPY, ex-pair: the remainder, share of the log change |
| A2_long_JPY_R_pct0 | 3 | long window, JPY, ex-pair: the remainder, per cent of the log change, whole, negative |
| A2_long_MYR_w_in_sg | 9.3 | long window: weight of MYR in Singapore's basket, per cent |
| A2_long_MYR_w_sg_in_x | 10.5 | long window: weight of SGD in MY's basket, per cent |
| A2_long_MYR_s_ex | 0.3599 | long window: SGD broad index without MYR, log change |
| A2_long_MYR_n_ex | 0.0300 | long window: MY broad index without SGD, log change |
| A2_long_MYR_S | 1.0435 | long window, MYR, ex-pair: the Singapore dollar rising, share of the log change |
| A2_long_MYR_S_pct0 | 104 | long window, MYR, ex-pair: the Singapore dollar rising, per cent of the log change, whole |
| A2_long_MYR_P | -0.0868 | long window, MYR, ex-pair: MYR falling, share of the log change |
| A2_long_MYR_P_pct0 | 9 | long window, MYR, ex-pair: MYR falling, per cent of the log change, whole, negative |
| A2_long_MYR_R | 0.0434 | long window, MYR, ex-pair: the remainder, share of the log change |
| A2_long_MYR_R_pct0 | 4 | long window, MYR, ex-pair: the remainder, per cent of the log change, whole |

### review_a3_real.csv

| Key | Printed | Meaning |
|---|---|---|
| A3_scored_JPY_cpi_sg_pct | 17.1 | scored window: Singapore's CPI (S7), per cent, up |
| A3_scored_JPY_cpi_sg_pct0 | 17 | scored window: Singapore's CPI (S7), per cent, up, whole |
| A3_scored_JPY_cpi_jp_pct | 13.1 | scored window: Japan's CPI (BIS long CPI), per cent, up |
| A3_scored_JPY_cpi_jp_pct0 | 13 | scored window: Japan's CPI (BIS long CPI), per cent, up, whole |
| A3_scored_JPY_b_real | 0.4367 | scored window: real yen per SGD, log change |
| A3_scored_JPY_b_real_pct | 54.8 | scored window: the Singapore dollar against the yen, real, per cent, up |
| A3_scored_JPY_b_real_pct0 | 55 | scored window: the Singapore dollar against the yen, real, per cent, up, whole |
| A3_scored_JPY_s_real_pct | 14.7 | scored window: the Singapore dollar's real broad index, per cent, up |
| A3_scored_JPY_s_real_pct0 | 15 | scored window: the Singapore dollar's real broad index, per cent, up, whole |
| A3_scored_JPY_n_real_pct | 26.6 | scored window: the yen's real broad index, per cent, down |
| A3_scored_JPY_n_real_pct0 | 27 | scored window: the yen's real broad index, per cent, down, whole |
| A3_scored_JPY_S | 0.3146 | scored window, real: the Singapore dollar rising, share of the log change |
| A3_scored_JPY_S_pct0 | 31 | scored window, real: the Singapore dollar rising, per cent of the log change, whole |
| A3_scored_JPY_P | 0.7067 | scored window, real: the yen falling, share of the log change |
| A3_scored_JPY_P_pct0 | 71 | scored window, real: the yen falling, per cent of the log change, whole |
| A3_scored_JPY_R | -0.0212 | scored window, real: the remainder, share of the log change |
| A3_scored_JPY_R_pct0 | 2 | scored window, real: the remainder, per cent of the log change, whole, negative |

### review_a4_rolling.csv

| Key | Printed | Meaning |
|---|---|---|
| A4_windows | 65 | rolling five-year windows, August 2005 on, in three-month steps |
| A4_rose | 46 | windows in which the Singapore dollar rose against the yen |
| A4_not_rose | 19 | windows in which it did not |
| A4_yen_larger | 39 | of the windows where it rose, those where the yen's own fall was the larger part |
| A4_sgd_larger | 7 | of the windows where it rose, those where the Singapore dollar's own rise was larger |
| A4_first_start_year | 2005 | first window starts (year) |
| A4_last_end_year | 2026 | last window ends (year) |

### review_a5_t7.csv

| Key | Printed | Meaning |
|---|---|---|
| A5_block2_lo | 0.10 | T7 D, moving-block bootstrap, block 2, 90% range, low |
| A5_block2_hi | 0.63 | T7 D, moving-block bootstrap, block 2, 90% range, high |
| A5_block4_lo | 0.09 | T7 D, moving-block bootstrap, block 4, 90% range, low |
| A5_block4_hi | 0.69 | T7 D, moving-block bootstrap, block 4, 90% range, high |
| A5_block8_lo | 0.14 | T7 D, moving-block bootstrap, block 8, 90% range, low |
| A5_block8_hi | 0.71 | T7 D, moving-block bootstrap, block 8, 90% range, high |
| A5_g_lead1_rho_p | 0.48 | T7 with growth led 1 quarter(s): rho with MAS's decisions |
| A5_g_lead1_rho | 0.04 | T7 with growth led 1 quarter(s): rho with growth |
| A5_g_lead1_D | 0.44 | T7 with growth led 1 quarter(s): D |
| A5_g_lead1_n | 60 | T7 with growth led 1 quarter(s): intervals with data |
| A5_cpi_lead1_rho_p | 0.48 | T7 with CPI inflation led 1 quarter(s): rho with MAS's decisions |
| A5_cpi_lead1_rho | 0.49 | T7 with CPI inflation led 1 quarter(s): rho with CPI inflation |
| A5_cpi_lead1_D | -0.01 | T7 with CPI inflation led 1 quarter(s): D |
| A5_cpi_lead1_n | 60 | T7 with CPI inflation led 1 quarter(s): intervals with data |
| A5_g_lead2_rho_p | 0.48 | T7 with growth led 2 quarter(s): rho with MAS's decisions |
| A5_g_lead2_rho | -0.18 | T7 with growth led 2 quarter(s): rho with growth |
| A5_g_lead2_D | 0.66 | T7 with growth led 2 quarter(s): D |
| A5_g_lead2_n | 59 | T7 with growth led 2 quarter(s): intervals with data |
| A5_cpi_lead2_rho_p | 0.48 | T7 with CPI inflation led 2 quarter(s): rho with MAS's decisions |
| A5_cpi_lead2_rho | 0.40 | T7 with CPI inflation led 2 quarter(s): rho with CPI inflation |
| A5_cpi_lead2_D | 0.08 | T7 with CPI inflation led 2 quarter(s): D |
| A5_cpi_lead2_n | 59 | T7 with CPI inflation led 2 quarter(s): intervals with data |
| A5_n | 61 | T7 intervals |
| A5_r1_y | 0.14 | lag-1 autocorrelation of the path y_i |
| A5_r1_p | 0.52 | lag-1 autocorrelation of MAS's score p_i |
| A5_r1_g | 0.57 | lag-1 autocorrelation of growth g_i |
| A5_neff_p | 53 | effective sample size for rho(y, p), Bartlett lag-1 |
| A5_se_p | 0.14 | approximate standard error of rho(y, p) at that size |
| A5_neff_g | 52 | effective sample size for rho(y, g), Bartlett lag-1 |
| A5_se_g | 0.14 | approximate standard error of rho(y, g) at that size |

### review_article.csv

| Key | Printed | Meaning |
|---|---|---|
| art_sgd_per_100jpy_2021_01 | 1.278 | MAS monthly average, S$ per 100 yen, 2021-01, three decimals |
| art_yen_per_budget_2021_01 | 78,200 | yen bought by S$1,000, 2021-01, to the nearest 100 |
| art_sgd_per_100jpy_2025_12 | 0.829 | MAS monthly average, S$ per 100 yen, 2025-12, three decimals |
| art_yen_per_budget_2025_12 | 120,600 | yen bought by S$1,000, 2025-12, to the nearest 100 |
| art_single_month_JPY_pct0 | 54 | the Singapore dollar against the yen, single-month endpoints, per cent, whole |
| art_finer_D_3dp | 0.346 | T7 with the finer slope coding: D, three decimals |
