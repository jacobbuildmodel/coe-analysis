# THESIS: COE or ERP -- which one actually keeps Singapore's roads moving?

**SEALED 26 September 2026 (SGT; 25 September UTC), by the commit that carries
this header, on its own, message "erp: SEAL THESIS.md". A commit cannot name
its own hash; the seal hash is recorded in `office/SEAL.txt` and on the
open-question page.**

**Sealed before any data value was read,** apart from the disclosed exposures
listed below. Everything from section 1 to section 10 -- the design, the tests,
every survive-if and fail-if, every threshold, the excluded years and the
confidences -- was fixed before a single result was computed.

**How this file changes from now on.** It does not get edited. Corrections,
additions and anything learned from the data go in appended, dated AMENDMENT
blocks at the end, each stating whether it was written BEFORE or AFTER results
were seen. An amendment never rewrites a prediction, a threshold, a confidence
or a fail condition in place.

Author: `erp` (Claude Code session). Repository: coe-analysis, subdirectory
`erp/`, branch `erp-wip`.

Evidentiary basis at seal: all five data files received on 26 September 2026
(SGT) and checked for coverage only by `00_coverage.py` (shape, columns, first
and last period; `raw/RETRIEVED.txt`). No data value from E1, E2, E3, E4b or E8
has been opened by any script or person on the researcher side. Values seen
before the seal, all disclosed in `office/SOURCES_REPORT.md` section 1: E1 for
2011 (both road classes); the 2019-2023 expressway average (checker); and, from
reading the E8b PDF for its year span, the number of digits in each of its
values, which shows only that expressway lane-km had three digits in 2005-2007
and four from 2008. The E3b, E5, E6 and E7 PDFs are in `raw/` and have not been
read.

Revision history before the seal: `fafee65` first draft; `da51ce3` checker
review (E4b, E8, cars per lane-km, T1 expressway exclusions, weak-evidence
sentence, T3 threshold reason, E5 second search); `bde81d4` proposed
confidences; this revision: coverage written in as numbers, confidences set by
Jacob, four predictions scored (T5 leg (a) unscored), the theory section added
as context, answer due December 2026.

Markers: `PENDING` = checked at analysis, after the seal, with the outcome
recorded as a dated AMENDMENT, never by editing the text above it.

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
- **About 20 annual points.** E1 runs 2004-2025: 22 years, 20 after 2020 and
  2021 are removed (section 5). Tests have fewer: T1 scores 16 expressway years
  and 19 arterial years; T2's main specification runs on 13 (2005-2017, the E8
  limit); T3 on 14 (2005-2018, the E2 limit); T4 on 19 (2005-2025 less 2020
  and 2021). At that size a two-variable regression has wide intervals and a
  single odd year can move a slope.

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

| Id | Series | Source | Coverage (checked, `raw/RETRIEVED.txt`) | State |
|---|---|---|---|---|
| E1 | Average peak-hour speed; columns year, ave_speed_expressway, ave_speed_arterial_roads | data.gov.sg `d_26f6afadf2f86b2004f9a1e28f5564cc` | 2004-2025, 22 rows | in `raw/`, values unopened |
| E2 | Average annual km per vehicle; columns year, vehicle_type, average_annual_mileage | data.gov.sg `d_bdc4c6434e47b055de4b5f2fde10c1af` | 2005-2018, 84 rows (6 types a year) | in `raw/`, values unopened |
| E3 | Vehicle population; columns year, category, type, number | data.gov.sg `d_2873f3b1b2a836103f51f696350b98fa` | 2005-2024, 412 rows | in `raw/`, values unopened |
| E3b | Vehicle population by type, 2025 | LTA PDF MVP01-1 | 2025, for the one year E3 lacks | in `raw/`, not read |
| E4 | COE premium, per bidding exercise | `../raw.csv`, `d_69b3380ad7e51aff3a7dcc84eba52b8a` | 2010-01 to 2026-08 | in repo; cross-check only |
| E4b | Quota premium and PQP, monthly (SingStat M651121), wide format | data.gov.sg `d_22094bf608253d36c0c63b52d852dd6e` | 2002-02 to 2026-08, 50 series | in `raw/`, values unopened |
| E5 | Dated ERP rate releases | LTA newsroom and Wayback | June 2018 onward only | in `raw/`, not read; no intensity series |
| E6 | Speed bands, 45-65 / 20-30 km/h | MOT, LTA | current | in `raw/`, not read |
| E7 | 2020 suspension chain | LTA releases, 2020-2022 | dated | in `raw/`, not read |
| E8 | Road length in lane-km; columns year, road_type, road_length | data.gov.sg `d_8415afe86e594bdc18f0f04a71d5f210` | 2005-2017, 52 rows (4 road types) | in `raw/`, values unopened |
| E8b | Road length in lane-km, LTA PDF | LTA `Road-Length-lane-km.pdf` | 2005-2014 (year labels read, values not) | subset of E8's years; does not extend it |

**Definitions fixed now.**

- **Car population:** the E3 total for cars (all car types E3 reports under
  cars) for T1, T2 and T4, because the road sees every car; 2025 from E3b.
  Sensitivity: private cars only, if E3 separates them.
- **Cars per lane-km:** car population divided by the E8 lane-km of the same
  road class: expressway lane-km for the expressway fit, arterial lane-km for the
  arterial fit. E8 is the source for every year, 2005-2017. E8b covers only
  2005-2014, so it adds no year; where both cover a year and disagree, the
  difference is reported and E8 is used, so the whole series comes from one
  file. The arterial series is E8's arterial row only; collector and local
  roads are not added in.
- **Annual premium:** from E4b, the mean over the calendar year's months of the
  Category A and Category B quota premiums, months with no bidding left out.
  Sensitivity: Category A alone. E4 (`../raw.csv`) is used only to cross-check
  E4b for 2010 onward; any year where the two annual means differ by more than
  1 per cent is reported.
- **km per car:** for T3, the E2 row for cars. E2 has one cars row and does
  not separate private cars from private-hire cars (Jacob, 26 September 2026,
  from the dataset page), so T3 uses all cars, with the private-hire bias
  stated in T3 and beside the result.
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

**2004 has speed but no car population** (E3 starts in 2005). It is scored in T1,
which needs only E1, and drops out of T1's informativeness check and of every
fitted test.

## 5A. What economic theory says (context only)

This section adds no test and changes no threshold. It is here so the reader
knows which way theory leans before the record is read.

Pigou (1920) set out that the efficient charge for an activity that harms
others equals the marginal harm it imposes. A charge on the jammed road at the
jammed hour is that charge, and it is what ERP approximates. Vickrey (1969)
worked out why congestion charges belong on the peak specifically: the harm a
trip does depends on when it is made. Weitzman (1974) asked the sharper
question: when the regulator cannot observe the harm exactly, is a price or a
quantity cap the safer instrument? The answer turns on how steeply the harm
rises. Where harm climbs steeply past some point, a cap is safer, because a
price set slightly wrong lets the harm run away. Congestion is that kind of
harm: a road near capacity goes from moving to jammed quickly. On paper, that
favours the cap, which is COE. But ERP is not a fixed price. It is reviewed
against a speed target every quarter, and a price that keeps chasing a quantity
target starts to behave like a cap. That is where the thermostat problem in
section 3 comes from.

Sources: A. C. Pigou (1920), *The Economics of Welfare*; W. S. Vickrey (1969),
"Congestion theory and transport investment", *American Economic Review*;
M. L. Weitzman (1974), "Prices vs. Quantities", *Review of Economic Studies*.
Not in `raw/`; cited for the argument, not for any figure.

## 6. Pre-registered tests

A failed prediction is a finding to publish, not a reason to change the test.
Thresholds marked "judgement" are the researcher's, stated with reasons, and
accepted by Jacob before the seal. Confidences are Jacob's, set 25 September
2026; the researcher's proposal and reason are kept beside each for the record.

### T1. Thermostat band (the ERP signature)

If ERP holds speeds in a band, annual peak speeds sit in that band through the
swings in car population and COE prices.

- **Scored years.** Expressways, 16 years: 2004-2010, 2012-2018, 2024, 2025.
  Arterials, 19 years: 2004-2010, 2012-2019, 2022-2025 (section 5).
- **Prediction.** In every scored year, expressway peak speed lies within
  45-65 km/h and arterial peak speed within 20-30 km/h.
- **Survive if:** every scored year, both road classes, inside the band.
- **Fail if:** any scored year, either road class, outside the band. Years below
  the band and years above it are counted and reported separately, because they
  mean different things (below: the buffet; above: the charge is higher than
  congestion needs).
- **Informativeness condition, fixed now.** T1 only says something if the
  "weather" changed. For each road class, over its scored years, the range of the
  car population (maximum minus minimum) is computed as a share of its mean,
  over the scored years that have a car population (2004 has none). If
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
- **Confidence at seal: 35%, set by Jacob, 25 September 2026.**
  Jacob's reason: "Every year, for both road types, with the years already seen
  sitting near the top of the range, is a fragile bet: one fast year on the main
  roads breaks it, even if the control is working."
  Researcher's proposal: 60%. The expressway half is likely to hold, since the
  band is 20 km/h wide and LTA steers toward it, but the arterial band is narrow
  (10 km/h) and has to hold in every scored year, and the one arterial year
  already seen (2011) sat in the upper part of the band, so a single year above
  30 km/h is a live risk; that disclosed value informed the proposal.

### T2. Insensitivity to car density (magnitude)

Under extreme COE, speed falls as cars are packed onto the roads. Under extreme
ERP, speed does not respond, because the charge moves instead.

- **Main specification.** For each road class separately, OLS of log(annual peak
  speed) on log(cars per lane-km of that road class) (section 4), over
  2005-2017: every year E1, E3 and E8 all cover (13 points; no excluded year
  falls inside). The slope is the elasticity: the per cent change in peak
  speed for a 1 per cent change in cars per lane-km. Reported with a 90 per cent interval (HC1).
- **Why density is the main specification.** Road building adds lane-km, which
  raises speed at a given number of cars with no help from either instrument.
  Dividing by lane-km takes that channel out of the slope instead of leaving it
  as a stated bias. Rail and the other channels in section 9 are not taken out.
- **Sensitivities, reported, not scored:** (i) log(speed) on log(car population),
  the draft's original specification, over 2005-2025 less 2020 and 2021 (19
  points, 2025 from E3b); (ii) the main specification with a linear time trend
  added.
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
- **Thirteen points.** The main specification rests on 2005-2017 because E8
  ends in 2017 and E8b does not extend it. The article says the slope rests on
  13 points.
- **Also reported, not scored:** R-squared of each fit.
- **Confidence at seal: 65%, set by Jacob, 25 September 2026.**
  Jacob's reason: "ERP is a feedback loop built to stop crowding from slowing
  traffic, and I expect it to show. I am not higher because thirteen years is a
  small sample and it has to hold on both kinds of road."
  Researcher's proposal: 60%. The thermostat, rail and the lane-km control all
  pull the slope toward zero, which favours the prediction, but it has to land
  inside a band 1.0 wide on both road classes from 13 points, and a shared time
  trend in speed and density (in either direction) can push a small-sample
  slope past +/-0.5 on its own.

### T3. Door fee and usage (the COE mechanism)

The buffet says a higher door fee does not make owners use the car less. Per-car
mileage does not fall when premiums spike.

- **Years.** 2005-2018, every year E2 and E4b both cover (14 points). Split
  into the 7 years with the highest annual premium and the 7 with the lowest
  (section 4); a tie at the boundary goes to the high half. The 2010-2013
  premium run named in the brief falls inside this window.
- **Prediction.** Mean km per car in the high-premium years is **no more than 3
  per cent below** the mean in the low-premium years.
- **Survive if:** the high-premium mean is at least 97 per cent of the
  low-premium mean.
- **Fail if:** it is below 97 per cent: owners drove measurably less when the
  door fee was high, which is the door fee doing some of ERP's work.
- **Known bias, stated now.** E2's cars row mixes private-hire cars in with
  private cars. Private-hire cars built up in the later E2 years and typically
  drive more than a private car, so the years they grew in get extra km per car for a
  reason that has nothing to do with the premium. If those years are
  low-premium years, the bias pushes toward FAIL. Which half they land in is
  reported with the result.
- **Why 3 per cent (judgement).** No source fixes the size of usage response
  that matters. 3 per cent is taken as the smallest fall in km per car that
  would amount to the door fee doing a visible share of a road charge's work;
  anything smaller is treated as no response. The E2 mileage survey's sampling
  error is not known; if the E2 page states one larger than 3 per cent, T3 is
  reported as below the data's resolution rather than scored.
- **Low power, stated now:** 14 annual points, one split.
- **Confidence at seal: 20%, set by Jacob, 25 September 2026.**
  Jacob's reason: "The mileage data counts Grab and other hire cars with private
  cars, and they grew in the cheaper-COE years, which makes those years look
  like heavier driving. I expect the pricey years to look more than 3 per cent
  lower for that reason, not because owners drove less."
  Researcher's proposal: 50%. The 3 per cent window is narrow for a
  survey-based mileage estimate, and any slow fall in per-car km over the
  period (ageing fleet, rail expansion; the researcher's background knowledge
  leans that way, unverified) would line up with a premium run in the middle
  and later years, pushing toward FAIL, while selection of heavy users into
  high-premium years pushes the other way.

### T4. The premium adds little once car numbers are known (magnitude)

If COE works only by setting how many cars exist, its price carries no
further information about peak speed once the car population is in the model.

- **Estimate.** For each road class, over 2005-2025 less 2020 and 2021 (19
  points; every year E1, E3 or E3b, and E4b all cover): OLS of log(speed) on
  log(car population), then again with log(annual premium) added. Run on car population rather than cars
  per lane-km so that the years are not limited by E8; the density version is
  reported as a sensitivity, not scored.
- **Prediction.** Adding the premium raises adjusted R-squared by less than 0.10,
  **and** the premium's 90 per cent interval includes zero, for both road classes.
- **Survive if:** both conditions hold for both road classes.
- **Fail if:** for either road class, the adjusted R-squared gain is 0.10 or more
  **and** the premium's interval excludes zero.
- **Otherwise:** reported as mixed.
- **Low power, stated now:** 19 points, and car population and
  premium are related through the quota. A pass here is weak evidence; T4
  carries no weight in the verdict (section 8) and is reported as supporting
  only.
- **Confidence at seal: 70%, set by Jacob, 25 September 2026.**
  Jacob's reason: "Once the number of cars is known, the COE price has little
  left to explain, and with about 19 years the data will struggle to show it
  matters even if it does a little."
  Researcher's proposal: 60%. If the premium carries nothing, each road class
  would pass about 85-90 per cent of the time by construction of a 90 per cent
  interval, but both classes must pass, annual series that trend together
  produce spurious significance more often than the nominal rate, and HC1
  intervals run narrow at 19 points.

### T5. What would make COE the winner (the mirror, stated in advance)

The record reads as COE-like if peak speeds track the car population the quota
sets, with ERP changes adding little.

- **Leg (a), testable:** T2's main-specification elasticity at or below -1.0 on
  either road class, **with** R-squared of 0.5 or more for that fit.
- **Leg (a) is described, not scored.** It holds automatically whenever T2
  holds, because it reads the same slope: an elasticity inside [-0.5, +0.5]
  cannot be at or below -1.0. Scoring it would add an almost free "held" to
  the count, so it carries no confidence and does not enter the scorecard
  (Jacob's ruling, 25 September 2026, pointing to the HDB financing thesis,
  which removed a clause for the same reason). It is reported as the mirror of
  a COE win.
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
  E2 years, 2005-2018. No prediction, no score, no weight in the verdict.

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

**Confidences and the scorecard.** Four predictions are scored for
calibration: T1, T2, T3 and T4. T5 leg (a) is not scored (T5). A prediction
"holds" when its survive-if condition is met; "inconclusive", "mixed" and
"uninformative" count as not holding, except that a test reported as not
scored at all (T3 below the data's resolution) drops out of both the count and
the Brier score, and the article says so. The confidences are Jacob's, set 25
September 2026.

Expected number of predictions holding, if these confidences are well
calibrated: 1.9 of 4 (0.35 + 0.65 + 0.20 + 0.70). The predictions are
correlated (T1 and T2 share a series; T2 and T4 share a regressor), so the
actual count is more spread out than four independent calls would be, but the
expected count is the same.

## 9. What would prove the framing wrong, and what it leaves out

- **E1 method changes.** If "key arterial roads" or the expressway set changed
  over the period, a level shift in E1 is a measurement change, not traffic.
  `PENDING`: the data.gov.sg page notes are read at analysis; any method break
  found is recorded as an AMENDMENT and shown on the chart.
- **Road supply.** Lane-km grew. More road at the same car numbers raises speed
  with no help from either instrument. Controlled for in T2's main specification
  through E8, by road class. What E8 does not capture (junction redesign,
  signal timing, roads not maintained by LTA) is not controlled.
- **Rail.** New lines opened across the period. Same effect, not measured.
- **The band itself.** T1 is scored against 45-65 and 20-30 km/h in every year.
  `PENDING`: if the E5, E6 or E7 documents, read after the seal, show a
  different band in force in some year, that year is scored against the band in
  force and the change is recorded as an AMENDMENT; the prediction wording does
  not change.
- **ERP 2.0.** The switch from gantries to satellite-based charging began within
  the window's last years. Charging points and the rate rule were reported as
  unchanged; treated as no break unless a source says otherwise.
- **2022 deferral.** If the MOT release confirms that increases due under the
  speed rule were held back in 2022, that year's thermostat was partly off by
  choice; noted on the chart.

## 10. Settled before the seal

1. Coverage: all five data files received and checked for coverage only;
   year ranges written into every test as numbers (section 4, section 6).
2. Thresholds: T1's 10 per cent informativeness share; T2's -0.5 / +0.5 survive
   band and -1.0 fail line; T3's 3 per cent; T4's 0.10 R-squared gain; T5's 0.5
   R-squared (described, unscored). Accepted by Jacob.
3. Years already seen: excluded from T1 scoring, 2011 for both road classes and
   2019, 2022 and 2023 for expressways; kept and flagged in T2 and T4. Accepted
   by Jacob.
4. Car definition: all cars for T1, T2 and T4. T3 uses all cars because E2 has
   no private-car row. Accepted by Jacob.
5. E5: no year-by-year intensity series; releases reach back to June 2018 only
   (RETRIEVED.txt). T5 leg (b) untestable, as stated in T5.
6. Confidences: T1 35%, T2 65%, T3 20%, T4 70%, set by Jacob, 25 September 2026.
   Expected number holding 1.9 of 4.
7. **Answer due: December 2026.**
8. The open-question page (`office/OPEN_QUESTION_DRAFT.md`) goes live with the
   seal hash and date filled in, before any data value is opened.
9. Still `PENDING`, for analysis, by AMENDMENT only: E1 method notes; the band's
   history (E6); the speed measure LTA compares with the band.
