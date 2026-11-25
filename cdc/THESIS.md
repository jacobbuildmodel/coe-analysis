# THESIS -- cdc piece: CDC vouchers and hawker food prices

**UNSEALED DRAFT, 24 November 2026.** Not sealed, not scored. Written before any
index value of any row was opened: SingStat was read for labels, codes and
periods only (`00_coverage.py`, output in `office/COVERAGE.txt`). When this file
is sealed, the header changes to SEALED with the date and the commit, and the
file is never edited again; changes go in `THESIS_ADDENDUM.md`, dated, and are
reported, not applied to the scoring.

Confidences are Jacob's alone. Every scored line below carries
"Confidence: (Jacob)" until he sets it.

## 1. The question

**CDC vouchers and hawker food prices**

From 11 June 2026 each Singaporean household could claim S$500 in Community
Development Council (CDC) vouchers, half for hawkers and heartland merchants and
half for supermarkets (CNA, 11 Jun 2026). It was the ninth tranche for all
households since 13 December 2021. Asked in Parliament on 3 March 2026 whether
vouchers for every household feed demand-pull inflation, the Ministry of Finance
(MOF) replied that there was "no evidence", citing annual all-items inflation. A
further S$300 was announced on 29 July 2026 for January 2027.

(a) Explain why a voucher that can be spent only at certain sellers may raise
their prices, using the price elasticity of supply and the incidence of a
demand-side subsidy (who ends up with the money: the buyer, or the seller through
a higher price).

(b) Discuss whether CDC vouchers or untied cash transfers are more effective in
raising households' real purchasing power.

**Sealed question.** Did hawker food prices step up when CDC vouchers were issued?

**Method.** A placebo-month test on the monthly Consumer Price Index (CPI): the
change in hawker prices relative to restaurant and fast-food prices across each
launch, set against the same calendar months in the years before the scheme.

**Decision.** MOF, Budget 2027 (expected February 2027): the tranche after
January 2027, its size, and vouchers against untied cash (the Cost-of-Living
Special Payment, GST Voucher cash). If prices stepped up, part of each voucher
reaches sellers, which counts for cash or tighter targeting. If not, the
demand-pull objection falls and the case for vouchers rests on support for
hawkers and heartland shops. The piece evaluates the policy. It says nothing
about what a household should buy or where.

## 2. My thesis

Hawker prices did not step up when the vouchers were issued. Any step at a
launch, measured against restaurant and fast-food prices, was smaller than 0.5
percentage points over the launch month and the month after.

Why 0.5: it is the smallest effect that matters for the decision, fixed at
Checkpoint 0 (5 November 2026). Below it, even a tranche that moved prices took
back well under one cent in the dollar from a hawker meal.

The rival view, held in Parliament and on the forums: vouchers that must be spent
at hawkers and heartland shops push those sellers' prices up, so part of the
voucher never reaches the household.

## 3. Data

SingStat Table Builder **M213751**, "Consumer Price Index (CPI), 2024 As Base
Year, Monthly", index, not seasonally adjusted. Table span 1961 Jan to 2026 Oct;
last updated 23 November 2026 (metadata endpoint, read 24 November 2026).

| Role | Row | Label | Months with an observation |
|---|---|---|---|
| Hawker row (outcome) | 1.11.3 | Hawker Centres, And Food Courts, Coffee Shops & Kiosks | 2005 Jan to 2026 Oct (262) |
| Comparison 1 | 1.11.1 | Restaurants, Cafes & Pubs | 2005 Jan to 2026 Oct (262) |
| Comparison 2 | 1.11.2 | Fast Food Restaurants | 2005 Jan to 2026 Oct (262) |
| Control | 1.03.2.3 | Electricity | 2015 Jan to 2026 Oct (142) |
| Described only | 1.11.3.1 | Hawker Centres | 2019 Jan to 2026 Oct (94) |
| Described only | 1.11.3.2 | Food Courts, Coffee Shops & Kiosks | 2019 Jan to 2026 Oct (94) |
| Described only | 1.11.1.1 | Restaurants | 2024 Jan to 2026 Oct (34) |

Two changes from the Checkpoint 0 design, both forced by coverage and made
before any value was seen:
- The comparison row for restaurants is **1.11.1** (Restaurants, Cafes & Pubs),
  not 1.11.1.1 (Restaurants). Row 1.11.1.1 starts in 2024 Jan, so it has no
  month before the scheme to compare with.
- The Electricity control runs from 2015 Jan, not 2005.

**The hawker gap** is the one named series of every scored test:

    gap(t) = index of row 1.11.3 at t / sqrt(index of row 1.11.1 at t * index of row 1.11.2 at t)

**Launches** (`events.csv`; day, amount and source for each). CDC vouchers for
all Singaporean households: 13 Dec 2021, 11 May 2022, 3 Jan 2023, 3 Jan 2024,
25 Jun 2024, 3 Jan 2025, 13 May 2025, 2 Jan 2026, 11 Jun 2026; announced for
January 2027. The 2020 and January 2021 vouchers went to lower-income households
only and are not launches here.

**Release dates.** The 2026 Oct index was published on 23 November 2026.
SingStat's advance release calendar
(https://www.singstat.gov.sg/data-tools-services/advance-release-calendar,
read 24 November 2026) lists the 2027 Jan index for 23 February 2027 and the
2027 Feb index, which the forward test needs, for 23 March 2027, both as
upcoming releases.

## 4. Computation (the same for every test)

1. **Window.** For a launch in calendar month m of year y, the window runs from
   the month before m to the month after m. The window change is

       W(y, m) = 100 * (gap(m + 1) / gap(m - 1) - 1)     per cent

2. **Placebo years.** For calendar month m, every year p whose window lies
   wholly inside 2005 Jan to 2021 Nov (the month before the first tranche for
   all households). That is 2005 to 2020 for a December launch (16 years), 2005
   to 2021 for a May or June launch (17 years) and 2006 to 2021 for a January
   launch (16 years).
3. **Excess.** X = W at the launch minus the mean of W over the placebo years,
   in percentage points.
4. **Pooled excess.** S = the mean of X over the launches of the test.
5. **Placebo distribution.** Each placebo year's own excess is its W minus the
   mean of the other placebo years' W. The pooled statistic is computed for
   every way of drawing one placebo year per launch (all combinations, exact).
   q95 is the 95th percentile of that distribution; p is the share of
   combinations at or above S, counted as (number + 1) / (combinations + 1).
6. **Gate D (can the test see it).** A step of 0.5 percentage points is added to
   every combination. The share that then lies above q95 is the detection rate.
   A test is scored only if its detection rate is at least 0.80. The smallest
   step the test would see four times in five (q95 minus the 20th percentile
   of the placebo distribution) is reported beside every result.

Scripts: `cdclib.py` (the estimator), `10_load.py`, `11_tests.py`,
`12_alternatives.py`; tested on invented data with a planted step and with none
(`tests/`). Their md5s are in `SEAL_MANIFEST.md`.

## 5. Positive controls (not scored; both must pass)

The test must be able to find steps that are known and dated.

- **C1. Electricity tariffs.** SP Group revises the household tariff on 1
  January, 1 April, 1 July and 1 October. In row 1.03.2.3, the absolute
  one-month change in those four months is larger than in the other eight
  months, 2015 Feb to 2026 Oct: one-sided rank-sum test, p below 0.05.
  C1 is not the placebo-month test the purpose review named: tariffs change
  in the same four months every year, so a placebo-month comparison
  differences them away. C1 shows the index records dated steps; C2 checks
  the estimator.
- **C2. The January 2023 and 2024 steps in the hawker row.** GST rose on 1
  January 2023 and 1 January 2024. For row 1.11.3 alone (not the gap), the
  pooled excess of the two January windows (Dec to Feb) over Januaries 2006 to
  2021 has p below 0.05.
  Most hawkers are not registered for GST, so a C2 that fails may mean the
  hawker row did not step at the GST rises, not that the estimator cannot see
  a step. The piece then scores nothing, reports "the monthly index cannot
  see a step of this size", and says beside it that the GST step C2 looks for
  may not have reached the row. The published GST article reports no figure
  for a 1.11 row in January 2023 or 2024 (section 12).

**If a control fails, no test is scored. If Gate D fails for T1, T2 or T3, that
test is not scored.** The piece then reports "the monthly index cannot see a
step of this size". It never reports "no link".

## 6. Scored predictions

Each has one statistic, one line, one set of periods and one series (the hawker
gap). "Holds" and "fails" are complements.

**T1. The size of the step at the five launches outside January.**
Launches: Dec 2021, May 2022, Jun 2024, May 2025, Jun 2026. Windows: 2021 Nov to
2022 Jan, 2022 Apr to Jun, 2024 May to Jul, 2025 Apr to Jun, 2026 May to Jul.
Placebo years 2005 to 2020 (December), 2005 to 2021 (May and June).
Statistic: the pooled excess S.
Holds if S is below 0.5 percentage points. Fails if S is 0.5 or above.
Confidence: (Jacob)

**T2. Whether any step shows at those five launches.**
Same launches, windows, placebo years and series as T1.
Statistic: the placebo p of S.
Holds if p is 0.05 or above (S is not in the top 5 per cent of the placebo
distribution). Fails if p is below 0.05.
T2 is not independent of T1: both use the same S. When Gate D passes, a T1
that fails almost always means a T2 that fails; T2 can also fail alone, on a step that shows
but is smaller than 0.5.
Confidence: (Jacob)

**T3. The size of the step at the two January launches without a GST rise.**
Launches: Jan 2025, Jan 2026. Windows: 2024 Dec to 2025 Feb, 2025 Dec to 2026
Feb. Placebo Januaries 2006 to 2021.
Statistic: the pooled excess S.
Holds if S is below 0.5 percentage points. Fails if S is 0.5 or above.
Confidence: (Jacob)

**T4. The forward prediction: the January 2027 tranche (S$300).**
Launch: Jan 2027. Window: 2026 Dec to 2027 Feb. Placebo Januaries 2006 to 2021.
Statistic: the excess X of that one window.
Holds if X is at or below the largest of the 16 placebo January excesses (step
5). Fails if X is above all 16.
One launch against 16 placebo years cannot reach p below 0.05 (the smallest
possible p is 1/17) and cannot pass Gate D at 0.5, so T4 has its own line and
no Gate D: January 2027 will not be the largest January excess on record. The
line is a number fixed by the 2006 to 2021 data; it is published when the data
is opened, before January 2027. Scored when the 2027 Feb index is published
(23 March 2027 on SingStat's calendar). If no tranche for all households is
issued in January 2027, T4 is void and drops out.
Confidence: (Jacob)

Expected number holding: (from Jacob's numbers)

Each confidence is the chance the test holds if it is scored. A test that is not
scored (section 5) or void drops out of the count and of the Brier score.

The January 2023 and January 2024 launches are in no scored test: GST rose in
the same month, restaurants and fast-food chains charge GST and most hawkers are
not registered for it, so the gap moves for a reason that is not the voucher.

## 7. Weak-evidence sentence

The design leans toward finding nothing. It sees only a step in the launch
month and the next, while vouchers are spent over as long as 18 months; row
1.11.3 includes food courts and coffee shops, and not every stall in it takes
the vouchers; and a rise that also lifted restaurant and fast-food prices is
differenced away. So "held" is weak evidence that vouchers leave hawker prices
alone: it says no launch step of 0.5 percentage points, not no effect. "Failed"
is the stronger result, and even then the index shows a step in the same
months, not its cause. T4 is weaker still: one January can only show a step
large enough to beat every January from 2006 to 2021. And no test here can see
a slow rise spread over the months in which vouchers are spent, or a lasting
shift since 2021 that every tranche shares. One case leans the other way: a
steady rise of the gap after 2021 that has nothing to do with launches shows
in every window, so T2 can fail with no launch step. A5 measures this; it is
printed beside T2.

## 8. The verdict rule

- The headline answer follows T1. Held: the measured step S is below 0.5
  percentage points. Failed: S is 0.5 percentage points or more.
- T2 says whether a smaller step was visible; T3 and T4 say whether January
  launches behave the same way.
- If T1 is not scored, the answer is "cannot see", and no verdict on vouchers
  is given.
- The alternative specifications in `ALTERNATIVES.md` are run with the tests
  and reported beside them as the share that keeps each result. They never
  make a second verdict.

**Result sentence and title.** Each outcome has a sealed result sentence and a
sealed title, filled and chosen by `11_tests.py` by the rules below; nothing in
them is chosen by hand. The answer article's first paragraph opens with the
filled result sentence, word for word, then the T2 sentence. The title is
published as sealed. Before publication it changes only through
`THESIS_ADDENDUM.md`, dated and reported; after publication, only through a
dated correction on the page. No title or sentence says the vouchers caused,
lifted or moved prices (section 11): hawker prices are the subject, and "when"
places them in the launch months.

Numbers, for T1's five launches: W, the mean launch-window change of the hawker
gap (per cent); P, the mean over the five launches of the placebo years' mean
window change (per cent); S = W - P (percentage points); p, the smallest step
seen four times in five (m) and the detection rate (d), from section 4. W, P, S
and m print as two decimals of their absolute value; p prints to three
decimals. "rose" or "rise" if the value is 0 or above, "fell" or "fall" if
below; "more" if S is 0 or above, "less" if below. If T1 holds and S would
print as 0.50, S prints to three decimals. "Restaurant prices" and
"restaurants" mean rows 1.11.1 (Restaurants, Cafes & Pubs) and 1.11.2 (Fast
Food Restaurants), averaged as in section 3.

Result sentence, T1 held or failed:
"At the five CDC voucher launches outside January (December 2021, May 2022,
June 2024, May 2025 and June 2026), hawker prices [rose|fell] [W] per cent
against restaurant prices (SingStat's restaurants, cafes and pubs and its
fast-food restaurants, averaged) from the month before each launch to the
month after, compared with an average [rise|fall] of [P] per cent in the same
months of the years before the scheme (2005 to 2020 for December, 2005 to 2021
for May and June): [S] percentage points [more|less] than usual, [below|at or
above] the 0.5-point step fixed in advance as the smallest that matters, so the
thesis [held|failed]."
If T1 failed, the next sentence is: "The index shows a step in the months the
vouchers were issued, not its cause."

T2 sentence, after it:
"A difference this large or larger turns up in [100p, one decimal] per cent of
comparisons drawn from the same months of the years before the scheme
(p = [p]), so [a step showed|no step showed beyond the usual swings]; the test
sees a step of [m] percentage points four times in five."

Result sentence, not scored:
- A control failed: "The test was not scored: its [electricity-tariff check|GST
  check|electricity-tariff and GST checks], which show whether this method finds
  a known, dated step in the monthly index, failed, so the monthly index cannot
  see a step of this size, and no verdict on the vouchers is given." If the GST
  check failed, the next sentence is: "The GST rises that check looks for may
  not have reached hawker prices, since most hawkers are not registered for
  GST."
- Gate D failed for T1: "The test was not scored: at the five CDC voucher
  launches outside January it would catch a step of 0.5 percentage points in
  hawker prices against restaurant prices only [100d, whole number] per cent of
  the time, short of the 80 per cent required, so the monthly index cannot see
  a step of this size, and no verdict on the vouchers is given."

Titles (at most 90 characters; fixed now):
- T1 held: "Hawker prices did not gain 0.5% more than usual on restaurants when CDC vouchers came"
- T1 failed, W 0 or above: "Hawker prices gained at least 0.5% more than usual on restaurants when CDC vouchers came"
- T1 failed, W below 0: "Hawker prices lost at least 0.5% less than usual to restaurants when CDC vouchers came"
- T1 not scored: "Hawker prices and CDC vouchers: the monthly price test could not give an answer"

## 9. Described, not scored

- Each launch's own window change and excess, including January 2023 and 2024.
- The SG60 vouchers of July 2025, accepted by the same sellers (window 2025
  Jun to Aug).
- Untied cash: the Cost-of-Living Special Payments of September 2024 and
  September 2026 (windows Aug to Oct). Two clean payouts are too few to score;
  the December Assurance Package payouts fall in windows that hold a GST rise
  or a January voucher launch. The comparison of vouchers with cash in part (b)
  therefore rests on T1 to T4 and on incidence reasoning, not on a scored test
  of cash.
- Rows 1.11.3.1 and 1.11.3.2 (from 2019: three placebo years at most) and row
  1.11.1.1 (from 2024: none).
- The CPI for the lowest 20 per cent of households (M213941, half-yearly) is
  too coarse for a launch-month test and is not used.

## 10. Confounds named in advance

- GST, 1 July 2007: inside the June placebo window of 2007.
- The pandemic: dining-in was barred for parts of April to June 2020 and May to
  August 2021, inside the May and June placebo windows of those years.
- The energy shock of 28 February 2026, three months before the June 2026
  launch.
- The trend: if hawker prices rose faster (or slower) than restaurant prices
  throughout 2022 to 2026 for reasons that are not the vouchers, every launch
  window carries that drift.
- Late launch: the June 2024 tranche opened on 25 June, when most of that
  month's prices had been collected.
- Cash paid in the same season: Assurance Package cash each December from 2022.
- Chinese New Year falls in January or February; the Dec to Feb window always
  holds it, for launches and placebo years alike.
- Vouchers for lower-income households in June 2020 and January 2021 sit in the
  placebo years.

`ALTERNATIVES.md` holds the alternative specifications (eight for T1 and T2,
six for T3 and T4), each answering a named objection, most of them from this
list.

## 11. What this piece will not do

It will not say whether vouchers are good policy, what MOF should do, or what
anyone should buy. It will not call a step in the index the effect of the
vouchers; it will say whether prices stepped in the months they were issued. It
will not report a null as "no link" when a control or Gate D fails.

## 12. What was seen before the seal

- No index value of any CPI row. `00_coverage.py` asked SingStat for the rows
  and kept, in memory, only which months have an observation; it prints no
  value.
- The method scripts of the published GST piece (`gst-passthrough`,
  `04_placebo_and_window.py`, `10_lownoise.py`, `11_lownoise_placebo.py`) were
  read for the method. Their comments quote two All Items results of that piece
  (a January 2023 excess and a July 2007 excess). Neither is a row of this
  piece. The published GST article is public and Jacob has read it.
- MOF's reply of 3 March 2026 cites annual all-items inflation (seen at
  Checkpoint 0).
- The published GST article (`content/economics/2026-09-08.md` on the site;
  `2026-09-08.md` in `gst-passthrough`) and that piece's THESIS, RESULTS,
  README and addendum were searched on 24 November 2026 by a script that
  printed flags, never text. They report no figure for a 1.11 row in January
  2023 or 2024: the sentences that name hawkers or restaurants carry no figure
  and no date, and the article's three charts carry no food-serving label.
- `sgd/raw/` in this repository holds `s7a_singstat_cpi_monthly_M213751.json`,
  from the published exchange-rate piece: table M213751, 1961 Jan to 2026 Aug,
  the first 22 series as served, starting with row 1 (All Items)
  (`sgd/office/SOURCES_REPORT.md`). `sgd/out/cpi.csv` holds row 1 alone, as
  that piece loaded it (`sgd/10_load.py`). Row 1 is A2's comparison. The
  checker, placing this note, read the labels and period counts in
  `sgd/raw/RETRIEVED.txt` with every line holding a decimal filtered out, and
  found rows 1 (All Items) and 1.0 (Food), the list ending at row 1.01.3.3: no
  1.11 row and no 1.03.2.3 row. The drafting mission and the fix pass read
  code and documents only. Apart from the checker's label read, no file in
  `sgd/raw/` or `sgd/out/` was opened for this piece, and no value in them was
  seen. `pwm/raw/` and `pwm/out/` hold annual CPI files of another piece;
  they were not opened either.
