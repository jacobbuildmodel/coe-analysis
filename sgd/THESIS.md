# THESIS -- sgd piece

**UNSEALED DRAFT. First draft 29 September 2026 (6f9b6c2); revised 3 October
2026 after the checker review of 6f9b6c2. Not sealed. Written before any data
file was received or opened (`raw/RETRIEVED.txt`: nothing retrieved; the
sandbox could reach no data host). Everything below can still change before
the seal, by Jacob's decision or on receipt of the files. Nothing is scored
against it until it is sealed in a commit that adds only `SEAL_MANIFEST.md`,
as for the pwm piece.**

Author: `sgd` (Claude Code session). Repository: coe-analysis, subdirectory
`sgd/`, branch `sgd-wip`, from `origin/main` at 6e4acf0. The title and the
opening are not part of this file: the Editor chat and Jacob handle them.

Evidentiary basis of this draft: the web search index (29 September 2026)
for titles, series keys, URLs and documented coverage, recorded in
`office/SOURCES_REPORT.md`. Values that were seen (one ringgit index point,
policy settings, policy-decision titles) and the background knowledge held
when the windows were set are listed in `office/SOURCES_REPORT.md` section 1.

Confidences are **the researcher's proposals**, marked as such, with
`[JACOB]` where Jacob's number goes. Jacob sets his; only his are scored.

Revision after the checker review of 6f9b6c2:
- **Five scored tests:** T1 (design), T2 (yen), T3 (ringgit), T4 (steadiest)
  and T7 (policy or growth).
- **Former T5 (breadth)** is sensitivity B, reported and not scored.
- **Former T6 (BIS index against MAS's own)** is check C, printed beside T7
  and gating nothing.
- The researcher's proposals for the former T5 and T6 are withdrawn.
- **T2 and T3 score the reader's window,** January 2021 to December 2025.
  August 2005 to the latest month is their long-run sensitivity. T1 is
  checked on both windows; T4 and T7 keep the long window.
- **The answer is due December 2026,** or January 2027 only if the
  downloads slip.
- **No title or opening.**

## 1. The question

**The belief on trial (approved direction).** The Singapore dollar rises
because Singapore's economy is strong, and a cheap yen or ringgit means the
Singapore dollar got stronger.

**The rival explanation.** MAS steers the Singapore dollar against a basket of
trading partners' currencies on a slow, deliberate path. So most of a move
against one currency is that currency moving, not the Singapore dollar.

**Sealed question 1 (draft wording, window from section 5).** "From January
2021 to December 2025, how much of the Singapore dollar's rise against the
yen and the ringgit came from the Singapore dollar rising against everyone,
and how much from those currencies falling against everyone?"

**Sealed question 2 (draft wording).** "Did the Singapore dollar's broad path
follow MAS's announced policy decisions more closely than Singapore's
growth?"

Question 1 tests the second half of the belief (a cheap yen means a strong
Singapore dollar). Question 2 tests the first half (it rises because the
economy is strong). The two are scored separately, and the verdict has a
part for each (section 8).

## 2. The two extremes (thought experiments, labelled as such)

- **A hard peg (Hong Kong).** The Hong Kong dollar is held between HK$7.75
  and HK$7.85 per US dollar. When it rises against the yen, that is the US
  dollar's rise against the yen, plus nothing. Hong Kong's own economy has
  no channel into the Hong Kong dollar's rate against the yen except
  through the US dollar. In this extreme, every move against a third
  currency is someone else's move.
- **A free float (Japan).** The yen has floated since February 1973, with
  occasional intervention by the Ministry of Finance. When the yen falls
  against the Singapore dollar, a large part may be the yen falling against
  everyone, because Japan's own conditions and flows move it. In this
  extreme, a currency's moves are its own.
- **Singapore sits between them.** MAS's index is kept inside an undisclosed
  band that crawls at an undisclosed slope. The belief reads a Singapore
  dollar that buys more yen as a Singapore dollar that is stronger. The
  rival reads it as the yen moving while the Singapore dollar crawls.

These are pictures of the two ends, not claims about the data.

## 3. Why this is answerable, and how far

**The split.** For a partner currency X and a window:

- `b_X` is the change in the log of units of X per Singapore dollar (from
  BIS US dollar rates: X per USD divided by SGD per USD). Positive means the
  Singapore dollar rose against X.
- `s` is the change in the log of the BIS broad nominal effective exchange
  rate of the Singapore dollar. Positive means it rose against its basket,
  "against everyone".
- `n_X` is the change in the log of the BIS broad nominal index of X.
  Negative means X fell against its basket.
- `e_X = b_X - s + n_X` is what the two broad indices do not account for.
  It would be zero if the two currencies were measured against the same
  basket. They are not: each basket holds the other currency and not
  itself, and the weights differ.

Then `b_X = s + (-n_X) + e_X`, and the three shares of the rise are
- `S_X = s / b_X`, the Singapore dollar rising against everyone;
- `P_X = -n_X / b_X`, the partner falling against everyone;
- `R_X = e_X / b_X`, the part that neither index accounts for.

They add to 1. The question's "how much ... and how much" is `S_X` and
`P_X`, with `R_X` shown beside them.

**How far.**
- The split is an accounting identity, not a causal model. It says whose
  broad index moved, not why.
- Question 2 compares what the Singapore dollar's broad path lined up with.
  It cannot separate "MAS responded to growth, then steered the rate" from
  "growth moved the rate". Section 6, T7 states the lean.
- The band itself (slope, width, centre) is not published (MAS FAQ). So no
  test here asks where the rate sat inside the band.

## 4. Data (pointers; detail in `office/SOURCES_REPORT.md`)

| Id | Series | Used in |
|---|---|---|
| S1 | BIS WS_EER, monthly, nominal, broad basket: SG, JP, MY, KR, CN, TH, ID, US, XM (euro area), AU, HK (key M.N.B.<AREA>) | T1, T2, T3, T4, T7; sensitivity B; check C |
| S2 | BIS WS_XRU, monthly average, units per US dollar: SGD, JPY, MYR, KRW, CNY, THB, IDR, EUR, AUD, HKD (key M.<AREA>.<CUR>.A) | T1, T2, T3; sensitivity B |
| S3 | MAS exchange rates, monthly average (SingStat M700051) | T1 (cross-check); reader numbers |
| S4 | MAS S$NEER, weekly | check C only |
| S5 | MAS Past Monetary Policy Decisions (since 2001) and each Monetary Policy Statement | T7 |
| S6 | SingStat real GDP, year-on-year growth, quarterly | T7 |
| S7 | SingStat CPI, monthly | T7 sensitivity only |

**Comparison set (10 partners).** JPY and MYR (the question), and KRW, CNY,
THB, IDR, USD, EUR, AUD and HKD. These are the region's main currencies,
the three largest reserve currencies, and Hong Kong's peg as the world-view
case. For USD, `n_USD` is the change in the BIS US index and `b_USD` is
the change in the log of US dollars per Singapore dollar.

**If S2 has no monthly-average collection.** End-of-period rates (E) are
used for S2, and the endpoints in section 5 become three-month means of
end-of-month rates. The BIS indices stay monthly averages; the mismatch
enters `e_X` and T1 reads it.

## 5. Windows, fixed now

Two windows, each fixed by a rule stated before any data is opened.

**The scored window for T2 and T3: January 2021 to December 2025.**
- **The rule.** The last five full calendar years before the seal. The seal
  falls in 2026, so the window is January 2021 to December 2025.
- **The window is fixed now.** It does not move if the seal slips into
  2027.
- **Why this window.** The reader's question is about recent years: the
  hook is that Japan got cheaper lately. Five full calendar years is long
  enough to span MAS's tightening and easing and the yen's moves, and short
  enough to be "lately".
- **What was in mind when the rule was set.** It was set by rule, not by any
  outcome. But general knowledge that the yen fell after 2020 was in mind
  when the rule was set (SOURCES_REPORT section 1, item 6).
- **Endpoints.** Each end is the mean of the log over three months: January
  to March 2021 and October to December 2025. This damps a single month's
  noise.

**The long window: August 2005 to the last full month in S1 when the data is
opened.** It is used for T4, for the long-run sensitivity of T2 and T3, and
for T1's second check.
- **Why August 2005.** The ringgit's peg to the US dollar (RM3.80, from 2
  September 1998) and the renminbi's peg both ended on 21 July 2005 (BNM;
  PBOC). The ringgit is half of the question and the renminbi is in the
  comparison set. Before that date, both currencies' moves against the
  Singapore dollar were the US dollar's moves, which would mix a peg into
  the float being tested. August 2005 is the first full month with both
  pegs gone.
- **What it spans.** Several MAS cycles, including zero-slope and
  tightening episodes, wholly inside the BIS broad coverage (from 1994).
- **Endpoints.** Each end is the mean of the log over three months: August
  to October 2005, and the last three full months.

**Sensitivities, question 1 (reported, not scored).**
1. **The long run.** T2 and T3's split over the long window, gated by T1's
   long-window check.
2. **Single-month endpoints** (January 2021 and December 2025; August 2005
   and the last full month).
3. **End-of-period US dollar rates** (S2, collection E), if the average is
   used for the scored run.
4. **Sensitivity B, breadth** (section 7), on both windows.

**Question 2 (T7, and check C beside it).**
- **T7 runs from the first decision in S5a to the last complete interval.**
  S5a lists decisions "since 2001". The unit is the interval between two
  consecutive decisions, on or off cycle.
- **An interval** runs from the month before decision i to the month before
  decision i+1. It carries all of decision i's immediate effect and none of
  decision i+1's.
- **The last interval** ends at the last full month in S1, and is kept only
  if it spans at least two months.
- **Check C** runs on every month in which both S1 and S4 exist.

**Growth vintage (T7).** The current published GDP series is used, not the
advance estimate MAS saw on the day. The question is what the rate's path
lined up with, not what MAS forecast. Revisions to Singapore's GDP growth
are small next to its swings between quarters, which is an assumption, not
a finding, and is stated here.

## 5A. What economic theory says (context only)

- **The "strong economy" channel.** Fast productivity growth in a country's
  traded goods tends to raise its real exchange rate over time (the
  Balassa-Samuelson effect). Strong growth can also draw capital in, which
  pushes the currency up. On this reading, Singapore's growth lifts its
  dollar.
- **MAS's framework.** Since 1981 MAS has run monetary policy through the
  exchange rate, not an interest rate. It manages the Singapore dollar
  against an undisclosed basket, inside an undisclosed band, along an
  undisclosed slope, and reviews the three at each statement ("basket,
  band, crawl"; MAS). The stated reason is that trade is so large relative
  to Singapore's economy that the exchange rate is the strongest lever on
  inflation. On this reading, the slope is MAS's choice, informed by the
  outlook for inflation and growth, and the rate follows the choice.
- **A bilateral rate is a ratio.** Whatever the reason the Singapore dollar
  moves against everyone, its rate against one currency also moves with
  that currency's own fortunes. Section 3's split separates the two.

## 6. Pre-registered tests

Five tests are scored: T1, T2, T3, T4 and T7. The numbers T5 and T6 are not
used; their former content is sensitivity B and check C (section 7).

A failed prediction is a finding to publish, not a reason to change the
test. Thresholds marked "judgement" are the researcher's, with reasons. They
are accepted or changed by Jacob before the seal.

### T1. The split closes (the design test)

If the two broad indices describe the two currencies' moves, together they
account for almost all of the bilateral move. And the BIS cross rate matches
the rate Singapore itself publishes.

- **Estimate.** For X = JPY and X = MYR, on each of the two windows (section
  5):
  - (a) `R_X`, the share of `b_X` that neither broad index accounts for
    (section 3).
  - (b) The mean absolute monthly difference between the log of the BIS
    cross rate (S2) and the log of MAS's published monthly average rate
    (S3a, converted to units of X per Singapore dollar).
- **Prediction.** For both currencies and on both windows, the broad
  indices account for at least 80 per cent of the bilateral move, and the
  BIS cross is within 0.5 per cent of MAS's rate on average.
- **Survive if:** |R_X| <= 0.20 and the mean absolute difference (b) <=
  0.005, for both JPY and MYR, on both windows.
- **Fail if:** |R_X| > 0.20 or the mean absolute difference (b) > 0.005,
  for either currency on either window.
- **What a failure gates.**
  - **On the scored window, that currency fails the design.** Its share test
    (T2 for JPY, T3 for MYR) is not scored, and the article says the record
    cannot split that move.
  - **On the long window only,** that currency's long-run sensitivity is
    marked unreadable. T2 or T3 is still scored.
- **If S3a lacks the currency,** (b) is not run and T1 reads (a) alone,
  stated in RESULTS.
- **If the premise fails on a window** (`b_X <= 0`, so the Singapore dollar
  did not rise against X), (a) is not defined for X on that window. T1 then
  reads (b) for X there. On the scored window, X's share test is not scored
  (T2, T3).
- **Why 0.20 and 0.005 (judgement).**
  - A residual under a fifth of the move leaves the larger of `S_X` and
    `P_X` readable. When |R_X| is 0.20 or less, `S_X + P_X` lies between
    0.8 and 1.2, so a share above one half cannot come from the residual
    alone.
  - The two rate sources quote at different times of day (midday in
    Singapore, against the ECB and central-bank sources BIS uses). Monthly
    averages of them differ by far less than half a per cent unless one
    source is wrong.
- **Lean, stated now.** For the ringgit, the baskets overlap heavily:
  Malaysia weighs a lot in Singapore's basket and Singapore in Malaysia's.
  That can leave a larger residual than for the yen. And on the scored
  window a small `b_MYR` would magnify any residual's share. Both lean T1
  toward FAIL for MYR.
- **Confidence at seal: [JACOB].** Researcher's proposal: 60%.
  - Chain-linked BIS indices on broad baskets usually account for most of a
    bilateral move.
  - But T1 now has four chances to fail (two currencies, two windows).
  - The ringgit's move over the five years may be small, which makes its
    residual share large.

### T2. The yen: most of the rise was the yen falling

- **Estimate.** `b_JPY`, `s`, `n_JPY`, and the shares `S_JPY`, `P_JPY` and
  `R_JPY` over the scored window, January 2021 to December 2025 (section
  3).
  - No sampling interval is defined: each share is a ratio of two level
    changes.
  - The endpoint sensitivities (section 5) show how much the shares move
    with the choice of months.
  - The long-run split is reported beside it, not scored.
- **Prediction.** At least half of the Singapore dollar's rise against the
  yen from January 2021 to December 2025 came from the yen falling against
  everyone. And more of it came from the yen falling than from the
  Singapore dollar rising.
- **Survive if:** P_JPY >= 0.50 and P_JPY > S_JPY.
- **Fail if:** S_JPY >= P_JPY.
- **Otherwise** (P_JPY > S_JPY but P_JPY < 0.50): INCONCLUSIVE.
- **Not scored if** T1 fails for JPY on the scored window, or `b_JPY <= 0`.
  The premise "the Singapore dollar's rise against the yen" is then false
  for the window, and the verdict says so.
- **Why 0.50.** The rival says "most"; half is where most begins. This is
  not a judgement.
- **Confidence at seal: [JACOB].** Researcher's proposal: 70%.
  - General knowledge (SOURCES_REPORT section 1, item 5): the yen fell a
    long way against the US dollar over these years.
  - MAS tightened in 2021-2022, so `s` is positive too.
  - The bet is that the yen's own fall is the larger part. Over five years
    of a large yen move, it more likely is than over twenty.

### T3. The ringgit: most of the rise was the ringgit falling

- **Estimate.** As T2, for MYR, over the scored window.
- **Prediction.** At least half of the Singapore dollar's rise against the
  ringgit from January 2021 to December 2025 came from the ringgit falling
  against everyone. And more of it came from the ringgit falling than from
  the Singapore dollar rising.
- **Survive if:** P_MYR >= 0.50 and P_MYR > S_MYR.
- **Fail if:** S_MYR >= P_MYR.
- **Otherwise:** INCONCLUSIVE.
- **Not scored if** T1 fails for MYR on the scored window, or
  `b_MYR <= 0`.
- **Weak evidence, stated now.** Malaysia and Singapore sit heavily in each
  other's baskets. So part of the ringgit's fall shows up as the Singapore
  dollar "rising against everyone", and part of the Singapore dollar's rise
  shows up as the ringgit "falling against everyone". A result either way
  is weaker evidence for the ringgit than for the yen.
- **Confidence at seal: [JACOB].** Researcher's proposal: 25%.
  - The ringgit weakened in 2022-2024 (general knowledge, SOURCES_REPORT
    section 1, item 5).
  - But one index point seen before the seal (SOURCES_REPORT section 1,
    item 2) puts the ringgit's broad index about 13 per cent above its 2020
    average in February 2026. That makes it likely its own index ended the
    scored window near or above where it started.
  - Then `P_MYR` is small or negative, and T3 fails. Or `b_MYR <= 0`, and
    T3 is not scored.

### T4. The slow path: the Singapore dollar is the steadiest in the set

The rival says MAS moves the Singapore dollar slowly and deliberately. The
world view gives the two brackets: a peg to one currency (Hong Kong), whose
broad index swings with the US dollar's, and a free float (Japan).

- **Estimate.** For each of the 11 currencies (SGD and the 10 partners), the
  standard deviation of the monthly change in the log of its BIS broad
  nominal index over the long window (August 2005 to the last full month).
  The Singapore dollar's rank runs from 1 (steadiest) to 11.
- **Why the long window.** Volatility over five years rests on 60 monthly
  changes and on one or two episodes. Over the long window it spans every
  kind of MAS setting.
- **Prediction.** The Singapore dollar's broad index is the steadiest or
  second steadiest of the 11.
- **Survive if:** SGD's rank <= 2.
- **Fail if:** SGD's rank >= 6 (steadier than at most five of the ten
  partners).
- **Otherwise** (rank 3 to 5): INCONCLUSIVE.
- **Missing series.** If a partner's S1 series is missing, the rank is taken
  among those present:
  - survive at rank 2 or better, as before;
  - fail if the Singapore dollar is steadier than at most half the partners
    present, rounded down (with all 10, that is rank 6 or worse, as above).

  This applies only if at least 9 of the 11 are present. Below that, T4 is
  not scored.
- **Why rank 2 (judgement).** The renminbi was also managed against a
  reference basket from July 2005. It could be as steady on its own
  policy, so second place is allowed. Below the median is a plain
  contradiction of "slow and deliberate".
- **Reported beside it, not scored (world view).**
  - The ratio of the Hong Kong dollar's volatility to the US dollar's. The
    peg predicts it is close to 1.
  - The yen's rank. The float predicts it is among the least steady.
  - The same ranking over the scored window, January 2021 to December 2025.
- **Confidence at seal: [JACOB].** Researcher's proposal: 65%. A crawling
  band damps month-to-month moves by design. The main risk is the renminbi
  and the ringgit, both managed, sitting close.

### T7. Policy or growth: what the broad path followed

- **Units.** Every interval between consecutive MAS decisions, from the first
  in S5a (section 5).
- **The path in each interval, `y_i`.** The annualised change in the log of
  S1 M.N.B.SG from the month before decision i to the month before
  decision i+1: `y_i = 12 x change / months`.
- **The policy score, `p_i`.** The coding rule is fixed now, and is applied
  to S5a's Slope and Level columns before the seal, in
  `office/MPS_CODING.csv`. The statement's decision paragraph (S5b) is read
  wherever S5a is blank or ambiguous.
  - **Slope in force after decision i:** 1 if the band appreciates at any
    rate. That covers "modest and gradual appreciation", "increase
    slightly", "reduce slightly" and "maintain the rate of appreciation"
    when the prevailing rate is positive. It is 0 for "zero per cent
    appreciation" or a zero slope, and -1 for any depreciating slope. A
    decision that leaves the slope unchanged carries the previous value.
  - **Re-centring at decision i:** +1 for upward, -1 for downward, 0 for
    none. "At the prevailing level" with no direction word also counts 0.
    "Downward to the prevailing level" counts -1.
  - **Width** is not coded: it is about how much movement MAS tolerates,
    not which way the rate goes.
  - `p_i` = slope in force + re-centring, from -2 to 2.
- **Growth, `g_i`.** The mean year-on-year growth of real GDP (S6) over
  the quarters whose last month falls inside interval i. If none does, the
  quarter containing the month of decision i is used.
- **Statistic.** Spearman rank correlations, ties at average rank:
  - `rho_p = rho(y, p)`;
  - `rho_g = rho(y, g)`;
  - the difference `D = rho_p - rho_g`.

  A 90 per cent interval for D, by bootstrap over intervals (10,000 draws,
  seed 20260929), is reported and not used in the rule.
- **Printed beside it, gating nothing:** check C, the BIS index against
  MAS's own S$NEER (section 7).
- **Prediction.** The broad path lines up with MAS's decisions clearly
  better than with growth.
- **Survive if:** D >= 0.20 and rho_p > 0.
- **Fail if:** D <= 0 (growth lines up at least as well).
- **Otherwise** (0 < D < 0.20, or rho_p <= 0 with D > 0): INCONCLUSIVE.
- **Why 0.20 (judgement).** With about 60 intervals, the standard error of
  one Spearman coefficient is about 1/sqrt(59), roughly 0.13. A lead of
  0.20 is one and a half of those. Smaller leads sit inside the noise that
  a score of at most five values, with many ties, adds.
- **Weak evidence, stated now.** The design leans toward the rival. The
  band is the path MAS keeps the index on, so a score that describes the
  band will match the index's path wherever MAS held the index inside it.
  A result that the path followed MAS's decisions is weak evidence that MAS
  rather than the economy moved the Singapore dollar. A result that it
  followed growth at least as closely is strong evidence against the
  rival.
- **A second lean, the other way.** `p_i` takes few values with many ties,
  which lowers `rho_p`. And MAS set its slope partly on the growth outlook,
  so the two predictors share a cause. Both lean toward FAIL or
  INCONCLUSIVE.
- **Sensitivities (reported, not scored).**
  - Growth in the last quarter completed before decision i, not during the
    interval.
  - Headline CPI inflation (S7) in place of growth.
  - A finer slope coding: an ordinal step up for each "increase", down for
    each "reduce", reset to 0 at "zero per cent".
  - Intervals from 2010 only.
- **Confidence at seal: [JACOB].** Researcher's proposal: 65%. The band
  makes the prediction likely by construction (the lean above). The
  coarse score and the shared cause are what could hold D under 0.20.

### Computation, fixed with the analysis scripts (before the seal)

As for the pwm piece:
- scripts 10 to 15 are written blind, before the seal;
- a synthetic test suite on invented data forces every outcome branch;
- a `SEALED` guard file stops the loader reading `raw/` before the seal;
- every number printed goes through one function;
- an independent reproduction script re-derives every scored number.

No script is written at Checkpoint 0, apart from the coverage lister.

## 7. Sensitivity B, check C, and other descriptive output (not scored)

**Sensitivity B. Breadth: month to month, is a move against one currency
mostly that currency?** (Formerly T5; no prediction, no confidence.)
- **Computation.** For each of the 10 partners X, on both windows, a split
  of the monthly change in `b_X` into covariance shares:
  - `pi_X = cov(d b_X, -d n_X) / var(d b_X)`, the partner's own move;
  - `sigma_X = cov(d b_X, d s) / var(d b_X)`, the Singapore dollar's move;
  - the rest is the residual's share.

  The three add to 1.
- **Reported.** The count of partners with `pi_X > sigma_X`, and every
  share.
- **How to read it.** MAS damps the Singapore dollar's month-to-month moves
  inside its band, so monthly moves overstate how much of a longer move is
  the partner's. That is why question 1 rests on T2 and T3, which read the
  whole window, and this only shows breadth.

**Check C. Does the BIS index move with MAS's own S$NEER?** (Formerly T6;
no prediction, no confidence; gates nothing.)
- **Computation.** Monthly means of MAS's weekly S$NEER (S4), counting only
  months with at least three weekly readings. Then the Pearson correlation
  between the monthly change in its log and the monthly change in the log
  of S1 M.N.B.SG, over every month both exist.
- **Printed beside T7.** The correlation and the number of monthly changes
  it rests on.
- **If fewer than 24 changes overlap,** it is printed with the words "too
  short to read". MAS's page may show only the current and previous years
  (SOURCES_REPORT section 3, S4).

**World view (with T4).**
- The Hong Kong dollar's broad index against the US dollar's: the monthly
  correlation, and the volatility ratio.
- The yen's volatility rank.
- Japan's intervention dates (MOF), marked on the yen's series.

**Reader numbers.** How many yen and how many ringgit a Singapore dollar
bought at the start and the end of each window (S3a, MAS's own rates).

**Real rates, if S1b is received.** The same split on the BIS real indices,
to show how much of the nominal story survives price differences. Context
only.

## 8. The verdict rule (fixed at seal)

The verdict has two parts in one sentence.

**Part A, the yen and the ringgit (question 1, January 2021 to December
2025).** For each of the two, X, exactly one of these:

- **"the Singapore dollar did not rise against the X"**: `b_X <= 0` over the
  scored window.
- **"the record cannot split the Singapore dollar's rise against the X"**:
  T1 fails for X on the scored window.
- **"most of the Singapore dollar's rise against the X was the X falling
  against everyone"**: T2 (yen) or T3 (ringgit) survives.
- **"most of the Singapore dollar's rise against the X was the Singapore
  dollar rising against everyone"**: T2 or T3 fails.
- **"neither side accounts for most of the Singapore dollar's rise against
  the X"**: T2 or T3 is INCONCLUSIVE.

The long-run split (August 2005 on) is reported beside Part A, and does not
change its wording.

**Part B, the broad path (question 2).** Exactly one of these:

- **"the broad path followed MAS's decisions more closely than growth"**: T7
  survives. The weak-evidence sentence of T7 is printed beside it.
- **"the broad path followed growth at least as closely as MAS's
  decisions"**: T7 fails.
- **"the broad path followed MAS's decisions a little more closely than
  growth, by less than the line"**: T7 is INCONCLUSIVE.

Check C's correlation and overlap are printed beside Part B.

T4 is scored and reported with the verdict, but does not change its
wording.

**The scorecard.** Five tests: T1, T2, T3, T4 and T7. Held against expected
is counted over the tests scored, and the Brier score is the mean over
them. A test not scored drops out of both.

## 9. What would prove the framing wrong, and what it leaves out

- **The premise.** If the Singapore dollar did not rise against the yen or
  the ringgit over the scored window, the belief's "cheap yen" (or cheap
  ringgit) is not a Singapore dollar story for those years. Part A says so.
- **The rival's own claim.** If `S_X` exceeds `P_X` for the yen, the
  Singapore dollar's own crawl did more of the work than the yen's fall.
  The rival is then wrong for the currency the belief names first.
- **Left out.**
  - **Why MAS set the slopes it set.** Question 2 asks what the path lined
    up with, not what drove MAS.
  - **Interest rates and capital flows.**
  - **Prices.** For a traveller, a cheap yen is about what the yen buys,
    including Japanese prices. The split here is nominal; the real indices
    are context (section 7).
  - **How many Singaporeans hold the belief.** No survey was sought.

## 10. Open before the seal

1. **The downloads** (`raw/RETRIEVED.txt`) and the coverage listing
   (`00_coverage.py`).
   - Every "pending receipt" row in SOURCES_REPORT section 2 closes here, or
     its missing-series rule applies.
   - The sandbox still could not reach any data host on 3 October 2026. If
     Jacob opens network access for this environment, the researcher
     fetches from RETRIEVED.txt; otherwise the design chat does.
2. **`office/MPS_CODING.csv`**, from S5a by the rule in T7, before the seal.
3. **Jacob's confidences** for T1, T2, T3, T4 and T7.
4. **The windows and the sensitivities** (section 5): accepted or changed.
5. **The analysis scripts, the synthetic suite, the SEALED guard and the
   seal manifest**, as for the pwm piece.
6. **The answer date: December 2026.** The data is monthly and quick to
   run. January 2027 only if the downloads slip.
