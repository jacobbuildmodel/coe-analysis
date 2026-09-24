# THESIS: COE or ERP -- which one actually keeps Singapore's roads moving?

**UNSEALED DRAFT, 24 September 2026. Not sealed. Nothing in this file binds
until Jacob has reviewed it and a seal is committed on its own.**

Author: `erp` (Claude Code session). Repository: coe-analysis, subdirectory
`erp/`, branch `erp-wip`.

Evidentiary basis at draft: no file received. E1, E2, E3, E4b and E8 located
but not downloaded; E4 (COE premium) already in the repository, coverage checked
by dates only, 2010-01 to 2026-08; E5 not closed (searched twice); E6 and E7
located, not read. Expressway and arterial values for 2011, and the 2019-2023
expressway average, were seen before the seal; see `office/SOURCES_REPORT.md`
section 1 and T1 below. The seal is to be committed on its own, after coverage
is known and before any E1, E2, E3, E4b or E8 value is opened by any script
other than `00_coverage.py`, which prints shape and dates only.

Revised 24 September 2026 after the checker's review of `fafee65`: E4b and E8
added, T2's main specification changed to cars per lane-km, T1's expressway
exclusions widened, the weak-evidence sentence added to section 8, T3's
threshold reason replaced, E5 searched again, and the checker's proposed
answers to the section 10 items written in.

Markers: `PENDING` = needs a file or a source. `JACOB` = a judgement call left
open for Jacob before the seal.

---

## 1. The question

COE or ERP: which one actually keeps Singapore's roads moving?

Singapore prices a car twice. The Certificate of Entitlement prices **owning**
one: a fee at the start, paid once, whatever is done with the car afterwards.
Electronic Road Pricing prices **using** one: a charge each time a priced road is
used at a priced hour. Both are said to fight congestion. They do it through
different doors, and the record of peak-hour speeds can say something about
which door the traffic has actually been going through.

**The yardstick is peak-hour road speed** (E1): the congestion part of what a car
costs everyone else. Emissions, accidents and land taken by roads and parking
are the other parts. They are named in section 7 and kept there. They do not
decide the verdict.

**What this must not become.** Not a policy recommendation and not a ranking of
two government schemes for anyone to act on. It is a reading of what the
record looks like, in past tense.

## 2. The two extremes (thought experiments, labelled as such)

Neither extreme exists. Singapore runs both instruments at once. Each extreme is
the pure form of one instrument, pushed until its logic is plain, so that the
data can be asked which one Singapore's record resembles.

**Extreme COE: the buffet.** A very large fee at the door, and every plate free
after that. Few people get in. But once inside, the eighth plate costs nothing,
so each diner eats as much as they like, at the same time as everyone else. In
road terms: few cars, but each 8am trip costs its owner nothing extra, so the
few cars still crowd the same roads at the same hour. And having paid the door
fee, owners have a reason to use the car more, not less, to get their money's
worth; the people willing to pay the most at the door are also likely to be the
heaviest users.

**Extreme ERP: surge pricing.** Anyone may own a car. Each use of a jammed road
at a jammed hour carries a charge that rises until the road moves. Roads move.
But because the charge is on the trip and not the car, car numbers, parking land
and total emissions keep growing: the car that stays off the expressway at 8am
is still owned, still parked and still driven at 11am.

**What each extreme predicts for series that can be observed:**

| Observable | Extreme COE (buffet) | Extreme ERP (surge) |
|---|---|---|
| Peak speed as car numbers move | falls with more cars; speed tracks the quota | held in a band; speed does not track car numbers |
| Peak speed over time | drifts with car population and road supply | pinned inside the operator's band |
| km per car when the door fee spikes | does not fall (may rise: selection, sunk cost) | not applicable; no door fee |
| Car population and total car-km | held down | grow |

## 3. Why this is answerable, and how far

**Causal situation (Method page, "How the economics research works"): the third
one, a correlation, called a correlation.** T4 is written in the form of the
second (a conditional claim), but nothing in the data holds one side still, so it
does not license cause either. Reasons, stated rather than assumed:

- **ERP is set by looking at speed.** LTA raises a rate when speeds fall below
  the band and cuts it when they rise above it (E6). Rates therefore respond to
  speed, and any correlation between rates and speeds runs both ways by design.
  This is why no test below regresses speed on ERP rates.
- **The car population is set by the quota**, which is closer to outside the
  system than ERP is, but it moved in steps that coincide with rail lines
  opening, roads being built, population and employment growth, and the
  private-hire build-up. Any speed-on-car-population slope carries all of those
  with it.
- **About 20 annual points.** If E1 runs 2004-2025, that is 22 years, 20 after
  2020 and 2021 are removed (section 5). Some tests have fewer: T2's main
  specification is limited by E8 (13 points if only the data.gov.sg file,
  2005-2017, is usable), T3 about 14 (E2, 2005-2018), T4 up to about 19 (E1,
  E3 and E4b, 2005 on). At that size a two-variable regression has wide
  intervals and a single odd year can move a slope.

**How every claim is sized as a result:**

- Verdicts say "the record looks more like" one extreme. Never "COE caused" or
  "ERP caused", and never a share of congestion relief attributed to either.
- Slopes are reported with 90 per cent intervals. No verdict rests on
  statistical significance alone.
- **The thermostat problem, stated in advance.** A good controller makes the
  thing it controls stop moving, so its own effect becomes invisible in the
  data: a thermostat that works leaves room temperature flat whatever the
  weather, and flat temperature looks like "the heating did nothing". The same
  flatness can also come from mild weather. So a flat speed record is
  **necessary, not sufficient** for "ERP keeps the roads moving". The design
  can show the thermostat's signature. It cannot show that ERP, rather than rail,
  road building or the quota itself, is the thermostat. That limit is stated in
  the article, not in a footnote.

## 4. Data (pointers; detail in `office/SOURCES_REPORT.md`)

| Id | Series | Source | Coverage | State |
|---|---|---|---|---|
| E1 | Average peak-hour speed, expressways and arterials, annual | data.gov.sg `d_26f6afadf2f86b2004f9a1e28f5564cc` | UNKNOWN | PENDING download |
| E2 | Average annual km per vehicle, by type | data.gov.sg `d_bdc4c6434e47b055de4b5f2fde10c1af` | 2005-2018 per index, UNVERIFIED | PENDING download |
| E3 | Car population, annual | data.gov.sg `d_2873f3b1b2a836103f51f696350b98fa` | 2005-2024 per index, UNVERIFIED | PENDING download |
| E4 | COE premium, per bidding exercise | `../raw.csv`, `d_69b3380ad7e51aff3a7dcc84eba52b8a` | 2010-01 to 2026-08, checked | in repo; cross-check only |
| E4b | Quota premium and PQP, monthly (SingStat M651121) | data.gov.sg `d_22094bf608253d36c0c63b52d852dd6e` | from 2002 per checker, UNVERIFIED | PENDING download |
| E5 | Dated ERP rate and gantry history | LTA releases, 2020 on only | 2020-03 onward | NOT CLOSED before 2020 |
| E6 | Speed bands, 45-65 / 20-30 km/h | MOT, LTA | current | PENDING PDF |
| E7 | 2020 suspension | LTA releases, 2020 | dated | PENDING PDF; resumption date conflicted |
| E8 | Road length in lane-km, expressway and arterial | data.gov.sg `d_8415afe86e594bdc18f0f04a71d5f210`; LTA `Road-Length-lane-km.pdf` | 2005-2017 per index for the data.gov.sg file, UNVERIFIED; PDF span unknown | PENDING download |

**Definitions fixed now.**

- **Car population:** the E3 total for cars (all car sub-types E3 reports) for
  T1, T2 and T4, because the road sees every car. Sensitivity: private cars
  only, if E3 separates them.
- **Cars per lane-km:** car population divided by the E8 lane-km of the same
  road class: expressway lane-km for the expressway fit, arterial lane-km for the
  arterial fit. If the data.gov.sg file and the LTA PDF both cover a year and
  disagree, the PDF wins and the difference is reported.
- **Annual premium:** from E4b, the mean over the calendar year's months of the
  Category A and Category B quota premiums, months with no bidding left out.
  Sensitivity: Category A alone. E4 (`../raw.csv`) is used only to cross-check
  E4b for 2010 onward; any year where the two annual means differ by more than
  1 per cent is reported.
- **km per car:** for T3, the E2 row for private cars if E2 separates them,
  because the door fee is paid by owners; otherwise the E2 row for all cars,
  with the private-hire bias in T3 stated beside the result.
- **Speed:** E1, expressway and arterial treated separately throughout. Neither
  is averaged into the other.

## 5. Years excluded, fixed now

**2020 and 2021 are excluded from every fitted or scored test.** 2020 contains
the ERP suspension (E7) and the circuit breaker, when traffic collapsed for
reasons unrelated to price; 2021 carried remote-work restrictions. Both years are
shown on every chart, labelled, and discussed in words. This exclusion is made
before the data is seen and applies whichever way those years point.

**Years already seen are excluded from T1's scoring only.** For expressways:
2011, 2019, 2022 and 2023. For arterials: 2011. 2011's values for both road
classes were seen in a search summary; the 2019-2023 expressway average (about
60 km/h, MOT written reply, 6 February 2024) was read by the checker, which puts
each of those expressway years effectively inside the band. All of these years
stay in T2 and T4, where a single seen point does not decide the result, and
they are flagged in those tables.

## 6. Pre-registered tests

A failed prediction is a finding to publish, not a reason to change the test.
Thresholds marked "judgement" are the researcher's, stated with reasons, and
open to Jacob's change **before** the seal only.

### T1. Thermostat band (the ERP signature)

If ERP holds speeds in a band, annual peak speeds sit in that band through the
swings in car population and COE prices.

- **Scored years.** Expressways: every E1 year except 2011, 2019, 2020, 2021,
  2022 and 2023. Arterials: every E1 year except 2011, 2020 and 2021 (section 5).
- **Prediction.** In every scored year, expressway peak speed lies within
  45-65 km/h and arterial peak speed within 20-30 km/h.
- **Survive if:** every scored year, both road classes, inside the band.
- **Fail if:** any scored year, either road class, outside the band. Years below
  the band and years above it are counted and reported separately, because they
  mean different things (below: the buffet; above: the charge is higher than
  congestion needs).
- **Informativeness condition, fixed now.** T1 only says something if the
  "weather" changed. For each road class, over its scored years, the range of the
  car population (maximum minus minimum) is computed as a share of its mean. If
  that share is below 10 per cent (judgement), T1 is reported as scored but
  uninformative for that road class: speeds stayed flat while car numbers also
  stayed flat. The COE premium range (E4b) over the same years is reported
  alongside, descriptively.
- **Leans toward the ERP reading, stated now.** LTA adjusts rates precisely to
  keep speeds in the band, and an annual network average smooths the priced
  stretches toward the middle of a wide band. A pass is expected under a working
  thermostat and also under much weaker ones (section 8).
- **What this cannot show:** see the thermostat problem, section 3. E1 is also a
  network average and the band applies per gantry per half hour (SOURCES_REPORT
  E1).

### T2. Insensitivity to car density (magnitude)

Under extreme COE, speed falls as cars are packed onto the roads. Under extreme
ERP, speed does not respond, because the charge moves instead.

- **Main specification.** For each road class separately, OLS of log(annual peak
  speed) on log(cars per lane-km of that road class) (section 4), over every
  year that E1, E3 and E8 all cover, excluding 2020 and 2021. The slope is the
  elasticity: the per cent change in peak speed for a 1 per cent change in cars
  per lane-km. Reported with a 90 per cent interval (HC1).
- **Why density is the main specification.** Road building adds lane-km, which
  raises speed at a given number of cars with no help from either instrument.
  Dividing by lane-km takes that channel out of the slope instead of leaving it
  as a stated bias. Rail and the other channels in section 9 are not taken out.
- **Sensitivities, reported, not scored:** (i) log(speed) on log(car population),
  the draft's original specification, over every E1 and E3 year excluding 2020
  and 2021; (ii) the main specification with a linear time trend added.
- **Prediction.** For both road classes, the main-specification elasticity lies
  between -0.5 and +0.5.
- **Survive if:** both point estimates lie in [-0.5, +0.5].
- **Fail if:** either point estimate is at or below -1.0 (speed falls at least
  one for one with car density: the buffet signature).
- **Between -1.0 and -0.5, on either road class:** inconclusive, and published
  as inconclusive rather than rounded to either side.
- **Why -0.5 and -1.0 (judgement), unchanged from the draft.** On an unpriced
  road near capacity, speed falls faster than density rises, so a slope of -1 or
  steeper is what "no thermostat" looks like; a slope within half of that of
  zero means density explains little of speed. The move from car population to
  cars per lane-km makes the -1.0 line a closer match to that reasoning, since
  density is what the speed-flow relationship is written in, so the lines are
  kept. Car population is still not traffic, and rail still pulls the slope
  toward zero even with no thermostat. That residual bias favours the
  prediction, and it is why the fail line is set at -1.0 rather than nearer zero.
- **If E8 covers too few years.** If fewer than 10 years remain for the main
  specification after exclusions, it is still estimated and reported, T2 is
  scored on it, and the article says the slope rests on that many points.
- **Also reported, not scored:** R-squared of each fit.

### T3. Door fee and usage (the COE mechanism)

The buffet says a higher door fee does not make owners use the car less. Per-car
mileage does not fall when premiums spike.

- **Years.** Every year that E2 and E4b both cover (2005-2018 if the index is
  right for E2 and the checker for E4b). Split into a high-premium half and a
  low-premium half by annual premium (section 4). With an odd number of years,
  the median year goes to the high half. The 2010-2013 premium run named in the
  brief falls inside this window.
- **Prediction.** Mean km per car in the high-premium years is **no more than 3
  per cent below** the mean in the low-premium years.
- **Survive if:** the high-premium mean is at least 97 per cent of the
  low-premium mean.
- **Fail if:** it is below 97 per cent: owners drove measurably less when the
  door fee was high, which is the door fee doing some of ERP's work.
- **Known bias, stated now.** Private-hire cars built up in the later E2 years.
  If E2 mixes them in with other cars, those years get extra km per car for a
  reason that has nothing to do with the premium. Which half they land in, and
  so which way the bias pushes, is reported with the result.
- **Why 3 per cent (judgement).** No source fixes the size of usage response
  that matters. 3 per cent is taken as the smallest fall in km per car that
  would amount to the door fee doing a visible share of a road charge's work;
  anything smaller is treated as no response. The E2 mileage survey's sampling
  error is not known; if the E2 page states one larger than 3 per cent, T3 is
  reported as below the data's resolution rather than scored.
- **Low power, stated now:** about 14 annual points, one split.

### T4. The premium adds little once car numbers are known (magnitude)

If COE works only by setting how many cars exist, its price carries no
further information about peak speed once the car population is in the model.

- **Estimate.** For each road class, over every year that E1, E3 and E4b all
  cover, excluding 2020 and 2021: OLS of log(speed) on log(car population), then
  again with log(annual premium) added. Run on car population rather than cars
  per lane-km so that the years are not limited by E8; the density version is
  reported as a sensitivity, not scored.
- **Prediction.** Adding the premium raises adjusted R-squared by less than 0.10,
  **and** the premium's 90 per cent interval includes zero, for both road classes.
- **Survive if:** both conditions hold for both road classes.
- **Fail if:** for either road class, the adjusted R-squared gain is 0.10 or more
  **and** the premium's interval excludes zero.
- **Otherwise:** reported as mixed.
- **Low power, stated now:** up to about 19 points, and car population and
  premium are related through the quota. A pass here is weak evidence; T4
  carries no weight in the verdict (section 8) and is reported as supporting
  only.

### T5. What would make COE the winner (the mirror, stated in advance)

The record reads as COE-like if peak speeds track the car population the quota
sets, with ERP changes adding little.

- **Leg (a), testable:** T2's main-specification elasticity at or below -1.0 on
  either road class, **with** R-squared of 0.5 or more for that fit.
- **Leg (b), NOT testable, confirmed after a second search.** "ERP changes adding
  little" needs a year-by-year measure of ERP intensity. Two crude dated
  measures were searched for on 24 September 2026: annual ERP revenue and the
  gantry count by year. Neither exists for most years from a primary source.
  Revenue turned up for a handful of scattered years, mostly through press
  reports of parliamentary answers; the gantry count for four or five
  scattered years, from secondary sources (SOURCES_REPORT E5). Interpolating
  between those points would manufacture the series the test is meant to read.
  Revenue would also be a poor measure even if complete, because it rises when
  rates rise, and rates rise when speeds fall.
- **So:** the strongest COE-side claim the design allows is "speeds tracked car
  density, as the buffet predicts". It cannot say "and ERP did not matter", and
  the article says the COE case was only half testable and which half.

### T6. 2020 (descriptive only, no prediction)

Shown on the chart with the suspension dates from E7. Not scored. The article
says in words why it cannot be read as "what happens without ERP": the
circuit breaker removed the traffic at the same moment the charge was removed.

## 7. The side section: emissions, accidents, land (bounded)

The extreme-ERP thought experiment predicts that car numbers and total driving
keep growing when roads are priced by use rather than by ownership. One
descriptive series is built for this and nothing else:

- **S1. Total car-km** = car population (E3) x km per car (E2), by year, over the
  E2 years. No prediction, no score, no weight in the verdict.

Emissions, road deaths and injuries, and land for roads and parking are named as
the other parts of the car externality and are not measured. No source was
sought for them in this task. The section is capped at about 150 words in the
article and says plainly that a verdict on speed is not a verdict on the whole
cost of a car.

## 8. The verdict rule (fixed at seal)

Scored on T1 and T2 only. T3 and T4 test the COE mechanism and are reported
beside the verdict, not inside it.

- **"The record looks more like extreme ERP"**: T1 survives (and is informative)
  **and** T2 survives on both road classes.
- **"The record looks more like extreme COE"**: T1 fails with 3 or more scored
  years below the band on either road class, **or** T2 fails on either road
  class.
- **Anything else: "the record cannot tell the two apart"**, and that is the
  published finding, stated as plainly as either of the other two.

**Weak-evidence sentence, carried next to the verdict in the article, verbatim:**
"A pass for the ERP reading is weak evidence and a COE-like result is strong
evidence, because the design leans toward the ERP reading." The reasons, stated
now: T1 leans that way because LTA adjusts rates precisely to keep speeds in the
band and an annual network average smooths toward the middle of a wide band; T2
leans that way because rail, and any road supply E8 misses, pull the slope toward
zero. Neither lean runs the other way, so an ERP-like result is what the design
expects even under a weak thermostat, and a COE-like result has to overcome both.

Whatever the verdict, the article also carries the thermostat problem (section
3) next to it, and says that the design shows a signature, not a cause.

## 9. What would prove the framing wrong, and what it leaves out

- **E1 method changes.** If "key arterial roads" or the expressway set changed
  over the period, a level shift in E1 is a measurement change, not traffic.
  `PENDING`: check the data.gov.sg page notes when the file arrives.
- **Road supply.** Lane-km grew. More road at the same car numbers raises speed
  with no help from either instrument. Controlled for in T2's main specification
  through E8, by road class. What E8 does not capture (junction redesign,
  signal timing, roads not maintained by LTA) is not controlled.
- **Rail.** New lines opened across the period. Same effect, not measured.
- **The band itself.** If E6's bands changed within the period, T1 is scored
  against the band in force each year, which needs a dated source (`PENDING`).
- **ERP 2.0.** The switch from gantries to satellite-based charging began within
  the window's last years. Charging points and the rate rule were reported as
  unchanged; treated as no break unless a source says otherwise.
- **2022 deferral.** If the MOT release confirms that increases due under the
  speed rule were held back in 2022, that year's thermostat was partly off by
  choice; noted on the chart.

## 10. Open items before the seal

The checker's proposed answers to the `JACOB` items of the draft, dated 24
September 2026, are written in below as **ACCEPTED unless Jacob says otherwise**.

1. `PENDING` E1, E2, E3, E4b and E8 files (RETRIEVED.txt). Once received, only
   `00_coverage.py` runs, and its output (shape, columns, first and last period)
   is pasted into RETRIEVED.txt. Year ranges in T1-T4 are then written in as
   numbers, not "all E1 years".
2. Thresholds: T1's 10 per cent informativeness share; T2's -0.5 / +0.5 survive
   band and -1.0 fail line (kept for the density specification, reason in T2);
   T3's 3 per cent (reason replaced, see T3); T4's 0.10 R-squared gain; T5's 0.5
   R-squared. **ACCEPTED as drafted, unless Jacob says otherwise.**
3. Years already seen: excluded from T1 scoring, 2011 for both road classes and
   2019, 2022 and 2023 for expressways; kept and flagged in T2 and T4.
   **ACCEPTED, unless Jacob says otherwise.**
4. Car definition: all cars for T1, T2 and T4; private cars for T3 if E2
   separates them. **ACCEPTED, unless Jacob says otherwise.**
5. E5: searched twice; T5 leg (b) is untestable and the article says so.
   CLOSED as untestable, unless a dated primary series turns up before the seal.
6. `PENDING` E6: the band's history and the speed measure LTA uses.
7. Seal: committed on its own, after coverage is known and before any value is
   opened, as in the HDB financing piece. **ACCEPTED, unless Jacob says
   otherwise.** Not sealed by this revision.
