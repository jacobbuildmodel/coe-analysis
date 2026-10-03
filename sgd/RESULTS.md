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
