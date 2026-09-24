# THESIS: COE or ERP -- which one actually keeps Singapore's roads moving?

**UNSEALED DRAFT, 24 September 2026. Not sealed. Nothing in this file binds
until Jacob has reviewed it and a seal is committed on its own.**

Author: `erp` (Claude Code session). Repository: coe-analysis, subdirectory
`erp/`, branch `erp-wip`.

Evidentiary basis at draft: no file received. E1, E2, E3 located but not
downloaded; E4 (COE premium) already in the repository, coverage checked by
dates only, 2010-01 to 2026-08; E5 not closed; E6 and E7 located, not read. One
E1 value (2011) was seen unsolicited; see `office/SOURCES_REPORT.md` section 1
and T1 below. The seal is to be committed before any E1, E2 or E3 value is
opened by any script other than `00_coverage.py`, which prints shape and dates
only.

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
  2020 and 2021 are removed (section 5). Some tests have fewer (T3 about 9, T4
  about 10 to 14). At that size a two-variable regression has wide intervals and
  a single odd year can move a slope.

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
| E4 | COE premium | `../raw.csv`, `d_69b3380ad7e51aff3a7dcc84eba52b8a` | 2010-01 to 2026-08, checked | in repo |
| E5 | Dated ERP rate and gantry history | LTA releases, 2020 on only | 2020-03 onward | NOT CLOSED before 2020 |
| E6 | Speed bands, 45-65 / 20-30 km/h | MOT, LTA | current | PENDING PDF |
| E7 | 2020 suspension | LTA releases, 2020 | dated | PENDING PDF; resumption date conflicted |

**Definitions fixed now.**

- **Car population:** the E3 total for cars (all car sub-types E3 reports).
  Sensitivity: private cars only, if E3 separates them. `JACOB`: confirm once
  the columns are seen (columns count as coverage).
- **Annual premium:** the mean of Category A and Category B premiums over every
  bidding exercise in the calendar year, from E4. Sensitivity: Category A alone.
- **km per car:** the E2 row for cars; if E2 splits private cars from other
  cars, the private-car row, because the door-fee story is about owners.
- **Speed:** E1, expressway and arterial treated separately throughout. Neither
  is averaged into the other.

## 5. Years excluded, fixed now

**2020 and 2021 are excluded from every fitted or scored test.** 2020 contains
the ERP suspension (E7) and the circuit breaker, when traffic collapsed for
reasons unrelated to price; 2021 carried remote-work restrictions. Both years are
shown on every chart, labelled, and discussed in words. This exclusion is made
before the data is seen and applies whichever way those years point.

**2011 is excluded from T1's scoring only**, because its E1 values were seen
before the seal (both inside the bands). It stays in T2 and T4, where a single
seen point does not decide the result, and it is flagged in those tables.

## 6. Pre-registered tests

A failed prediction is a finding to publish, not a reason to change the test.
Thresholds marked "judgement" are the researcher's, stated with reasons, and
open to Jacob's change **before** the seal only.

### T1. Thermostat band (the ERP signature)

If ERP holds speeds in a band, annual peak speeds sit in that band through the
swings in car population and COE prices.

- **Prediction.** In every scored E1 year (all E1 years except 2011, 2020, 2021),
  expressway peak speed lies within 45-65 km/h and arterial peak speed within
  20-30 km/h.
- **Survive if:** every scored year, both road classes, inside the band.
- **Fail if:** any scored year, either road class, outside the band. Years below
  the band and years above it are counted and reported separately, because they
  mean different things (below: the buffet; above: the charge is higher than
  congestion needs).
- **Informativeness condition, fixed now.** T1 only says something if the
  "weather" changed. Over the scored years, the range of the car population
  (maximum minus minimum) is computed as a share of its mean. If that share is
  below 10 per cent (judgement), T1 is reported as scored but uninformative:
  speeds stayed flat while car numbers also stayed flat. The COE premium range
  over 2010 onward is reported alongside, descriptively.
- **What this cannot show:** see the thermostat problem, section 3. E1 is also a
  network average and the band applies per gantry per half hour (SOURCES_REPORT
  E1).

### T2. Insensitivity to car numbers (magnitude)

Under extreme COE, speed falls as cars are added. Under extreme ERP, speed does
not respond, because the charge moves instead.

- **Estimate.** For each road class separately, OLS of log(annual peak speed)
  on log(car population), all E1 years that have E3, excluding 2020 and 2021.
  The slope is the elasticity: the per cent change in peak speed for a 1 per
  cent change in car population. Reported with a 90 per cent interval (HC1).
  Sensitivity: the same with a linear time trend added, reported, not scored.
- **Prediction.** For both road classes, the elasticity lies between -0.5 and
  +0.5.
- **Survive if:** both point estimates lie in [-0.5, +0.5].
- **Fail if:** either point estimate is at or below -1.0 (speed falls at least
  one for one with car numbers: the buffet signature).
- **Between -1.0 and -0.5, on either road class:** inconclusive, and published
  as inconclusive rather than rounded to either side.
- **Why -0.5 and -1.0 (judgement).** On an unpriced road near capacity, speed
  falls faster than traffic rises, so a slope of -1 or steeper is what "no
  thermostat" looks like; a slope within half of that of zero means car numbers
  explain little of speed. Car population is not traffic, and road space grew
  over the period, both of which pull the slope toward zero even with no
  thermostat. That bias favours the prediction, and it is why the fail line is
  set at -1.0 rather than nearer zero.
- **Also reported, not scored:** R-squared of each fit.

### T3. Door fee and usage (the COE mechanism)

The buffet says a higher door fee does not make owners use the car less. Per-car
mileage does not fall when premiums spike.

- **Years.** 2010 to the last E2 year (2018 if the index is right): the overlap
  of E2 and E4. Split into a high-premium half and a low-premium half by annual
  premium (section 4). With an odd number of years, the median year goes to the
  high half.
- **Prediction.** Mean km per car in the high-premium years is **no more than 3
  per cent below** the mean in the low-premium years.
- **Survive if:** the high-premium mean is at least 97 per cent of the
  low-premium mean.
- **Fail if:** it is below 97 per cent: owners drove measurably less when the
  door fee was high, which is the door fee doing some of ERP's work.
- **Known bias, stated now.** Private-hire cars built up in the later E2 years,
  when premiums were lower. If E2 mixes them in with other cars, low-premium
  years get extra km per car for a reason that has nothing to do with the
  premium, which pushes toward FAIL. Reported with the result, in either
  direction.
- **Why 3 per cent (judgement).** The same verdict threshold the site used in the
  HDB pieces; small enough that a real usage response would clear it, large
  enough that survey noise in a mileage estimate would not.
- **Low power, stated now:** about 9 annual points, one split.

### T4. The premium adds little once car numbers are known (magnitude)

If COE works only by setting how many cars exist, its price carries no
further information about peak speed once the car population is in the model.

- **Estimate.** For each road class, over 2010 to the last E1 year excluding
  2020 and 2021: OLS of log(speed) on log(car population), then again with
  log(annual premium) added.
- **Prediction.** Adding the premium raises adjusted R-squared by less than 0.10,
  **and** the premium's 90 per cent interval includes zero, for both road classes.
- **Survive if:** both conditions hold for both road classes.
- **Fail if:** for either road class, the adjusted R-squared gain is 0.10 or more
  **and** the premium's interval excludes zero.
- **Otherwise:** reported as mixed.
- **Low power, stated now:** 10 to 14 points, and car population and premium are
  related through the quota. A pass here is weak evidence; T4 carries no weight
  in the verdict (section 8) and is reported as supporting only.

### T5. What would make COE the winner (the mirror, stated in advance)

The record reads as COE-like if peak speeds track the car population the quota
sets, with ERP changes adding little.

- **Leg (a), testable:** T2's elasticity at or below -1.0 on either road class,
  **with** R-squared of 0.5 or more for that fit.
- **Leg (b), NOT testable as things stand:** "ERP changes adding little" needs a
  year-by-year measure of ERP intensity (rate levels, increases, gantries). E5
  is not closed before 2020. `PENDING`: if E5 closes before the seal, leg (b) is
  written here as a test; if it does not, the article says the COE case was only
  half testable and which half.
- **So:** the strongest COE-side claim the design allows is "speeds tracked car
  numbers, as the buffet predicts". It cannot say "and ERP did not matter".

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

Whatever the verdict, the article carries the thermostat problem (section 3)
next to it, and says that the design shows a signature, not a cause.

## 9. What would prove the framing wrong, and what it leaves out

- **E1 method changes.** If "key arterial roads" or the expressway set changed
  over the period, a level shift in E1 is a measurement change, not traffic.
  `PENDING`: check the data.gov.sg page notes when the file arrives.
- **Road supply.** Lane-km grew. More road at the same car numbers raises speed
  with no help from either instrument. Not measured in this piece.
- **Rail.** New lines opened across the period. Same effect, not measured.
- **The band itself.** If E6's bands changed within the period, T1 is scored
  against the band in force each year, which needs a dated source (`PENDING`).
- **ERP 2.0.** The switch from gantries to satellite-based charging began within
  the window's last years. Charging points and the rate rule were reported as
  unchanged; treated as no break unless a source says otherwise.
- **2022 deferral.** If the MOT release confirms that increases due under the
  speed rule were held back in 2022, that year's thermostat was partly off by
  choice; noted on the chart.

## 10. Open items before the seal (for Jacob)

1. `PENDING` E1, E2, E3 files (RETRIEVED.txt). Once received, only
   `00_coverage.py` runs, and its output (shape, columns, first and last period)
   is pasted into RETRIEVED.txt. Year ranges in T1-T4 are then written in as
   numbers, not "all E1 years".
2. `JACOB` The thresholds: T1's 10 per cent informativeness share; T2's -0.5 /
   +0.5 survive band and -1.0 fail line; T3's 3 per cent; T4's 0.10 R-squared
   gain; T5's 0.5 R-squared. All judgements, reasons given above.
3. `JACOB` Whether 2011 is excluded from T1 (as drafted) or T1 is scored with it
   and flagged. Excluding costs one point; keeping it scores a year already
   seen.
4. `JACOB` Car population definition (all cars vs private cars) once E3's
   columns are seen.
5. `PENDING` E5: whether any pre-2020 dated rate history turns up. Decides
   whether T5 leg (b) exists.
6. `PENDING` E6: the band's history and the speed measure LTA uses.
7. `JACOB` The seal: committed on its own, before any value is opened, as in
   the HDB financing piece.
