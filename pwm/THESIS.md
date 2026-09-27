# THESIS: Minimum wage or the Progressive Wage Model -- which actually lifts Singapore's lowest pay?

**UNSEALED DRAFT, 27 September 2026. Not for publication. Nothing below is
final until Jacob sets the confidences and the file is sealed in a commit of
its own. After the seal it is never edited; changes go in
`THESIS_ADDENDUM.md`, dated, and are reported, not applied to the scoring.**

Author: `pwm` (Claude Code session). Repository: coe-analysis, subdirectory
`pwm/`, branch `pwm-wip`.

Evidentiary basis of this draft: no data file received (`raw/RETRIEVED.txt`);
every source located through a search index. No wage value from W1 and no
employment series from W2 has been seen. Values that were seen, all
single-date counts, policy settings or CPI figures, are listed in
`office/SOURCES_REPORT.md` section 1. Year ranges below are written as rules
("every June from the first OWS year to ...") and become numbers once
`00_coverage.py` has run on the received files, before the seal.

Revision history before the seal: `34122a7`/`cb9fe70` first draft; this
revision, after the checker review of `cb9fe70`: checker disclosure; the
Local Qualifying Salary stated as a floor under the comparison jobs before
2022, with its leans at T2, T3 and T5; T5 kept as a scored bet; T3 made part
of the verdict sentence; thresholds accepted; confidences relabelled as the
researcher's proposal pending Jacob's numbers; answer due December 2026.

Markers: `PENDING` = settled before the seal from documents or coverage
checks, never from a wage or employment value. "Researcher's proposal" = the
researcher's confidence, kept for the record; Jacob sets the final one.

---

## 1. The question

Minimum wage or the Progressive Wage Model: which actually lifts Singapore's
lowest pay?

Singapore has no national minimum wage. It went sector by sector instead.
From 2014 it put wage ladders, the Progressive Wage Model (PWM), into
licensing and registration rules for cleaners, then security officers and
landscape workers. The ladders are a floor for each skill level, rising as a
worker is trained and promoted. From 2022 ladders were added for retail,
food services, waste management, office administrators and drivers.
Opposition parties and many economists argue for one national floor instead.

**The yardstick is real pay at the bottom of covered jobs** (the 25th
percentile of monthly gross wage, OWS, deflated by CPI), **and whether
employment in those jobs held up.**

**What this must not become.** Not a case for or against a minimum wage, and
not a ranking of two policies for anyone to act on. It is a reading of what
the record looks like, in past tense.

## 2. The two extremes (thought experiments, labelled as such)

Neither extreme exists. Each is one approach pushed until its logic is plain,
so that the data can be asked which one Singapore's record resembles.

**Extreme minimum wage: one school uniform size for every student.** One
national floor for every job, set high. It fits some, pinches others, and
some leave. Every low-paid job is lifted at once. Where the floor is above
what a job is worth to the employer, that job goes.

**Extreme PWM: a tailor who makes perfect suits, but only for three
classes.** A ladder for a few named jobs, cut to fit each one, and nothing for
anyone else. Covered workers get a floor that suits their job. Everyone else
at the bottom gets no floor at all.

**The model behind the argument.**

- **Competitive labour market.** Employers pay what a worker's output is
  worth, because a worker paid less would leave for a rival. A floor above
  that level costs jobs.
- **Monopsony.** Where employers have wage-setting power (few employers, costly
  job switching, outsourced contracts won on price), pay sits below the
  worker's worth. A floor can then raise both pay and jobs, because more
  workers come forward at the higher wage. Card and Krueger (1994) found no
  job loss when New Jersey raised its minimum wage.

The ladders give the record a chance to say which model Singapore's covered
jobs look like.

**What each extreme predicts for series that can be observed:**

| Observable | Extreme minimum wage (one uniform) | Extreme PWM (tailor) |
|---|---|---|
| Bottom pay in covered jobs, relative to uncovered low-wage jobs, after coverage | no gap opens; all low-paid jobs move together | a gap opens: covered jobs pull away |
| Bottom pay in uncovered low-wage jobs, relative to the middle | pulled up with everyone | left behind |
| Employment where the floor binds | competitive: falls; monopsony: holds or rises | the same, but only in the covered jobs |

Singapore ran the tailor, not the uniform, so the first column is never
observed directly. The record can show three things. Did the tailor's suits
fit (did pay rise where the ladder was hung)? Did the jobs survive the
fitting (competitive or monopsony)? Did the rest keep pace?

## 3. Why this is answerable, and how far

**The staggered rollout.** The ladders became binding in different years:

- cleaning (contract cleaners) by September 2015;
- security (agency officers) from September 2016;
- landscape (registered firms) from June 2016;
- retail, food services, and office and driving jobs only from September 2022
  or March 2023.

For about six years, cleaners, guards and gardeners worked under a floor,
while shop assistants, waiters, kitchen helpers, office clerks and drivers did
not. The later-covered jobs are the comparison: low-paid, in services, and
judged by the government itself in 2021 to need a ladder, but without one
until then. No already-covered job is ever used as a comparison, which avoids
the known trap of staggered designs (Goodman-Bacon 2021).

**Causal situation (Method page, "How the economics research works"): the
second one, a conditional claim.** The rollout has the shape of the first
situation, because the dates hold the timing still. But the dates were not set
by chance, so the claim is conditional. **If** covered and comparison jobs
would have kept moving in parallel without the ladders, **then** the gap that
opened after coverage is the ladders' doing. T1 checks the part of that
condition that can be checked: whether they moved in parallel before. It
cannot check the years after, when other things changed at the same time.
Reasons, stated rather than assumed:

- **Selected, not assigned.** Cleaning, security and landscape were singled out
  because their pay was low and not rising, much of it through outsourced
  contracts won on price. Jobs singled out for lagging may have been lagging
  before. That is T1's risk, and it is the reason T1 exists.
- **Announced before binding.** Each ladder was published one to three years
  before it bound (cleaning October 2012; security October 2014; landscape
  April 2015). Firms could move early, so the years between announcement and
  binding are neither before nor after, and are not scored.
- **Other levers moved in the same years:**
  - foreign worker levies and quotas in services were tightened in the early
    2010s;
  - the Wage Credit Scheme from 2013 co-funded wage rises for lower-paid
    Singaporeans in all jobs;
  - National Wages Council guidelines from 2012 asked for dollar increases
    for low-wage workers;
  - the government's "best sourcing" push changed how it bought cleaning and
    security;
  - **the Local Qualifying Salary (LQS)**, earlier the full-time-equivalent
    salary threshold, put a floor under the comparison jobs long before they
    got a ladder. Before September 2022 it was a counting rule: a local paid
    below it did not count, or counted only in part, toward the firm's
    foreign worker quota. Any firm needing that quota had a reason to pay
    every local at least the threshold, and that includes many shops and
    food outlets in comparison set C. As found (secondary sources; primary
    dates `PENDING`, SOURCES_REPORT W3):
    - S$1,000 before July 2017 (start date not found);
    - S$1,100 from July 2017 and S$1,200 from July 2018;
    - S$1,300 in 2019;
    - S$1,400 from 2020.

    In the covered jobs the ladder's entry rung sat at or above it, so the
    LQS added little there; its push falls on the comparison side. So the
    comparison is between a ladder and a lower, looser floor, not between a
    ladder and no floor at all.

  Most of these hit both sides of the comparison; the LQS hit mainly the
  comparison side. Where one hit one side
  harder (levies bite hardest where foreign workers are most used, which
  includes cleaning and food services), it is not separated out.
- **Few groups, few years.** Three covered groups, one comparison set, a
  handful of June surveys on each side. Every estimate is a small-sample
  number and is sized that way.

**How every claim is sized as a result:**

- Verdicts say "covered jobs look more like" one model. Never "PWM caused"
  or "a minimum wage would have", and never a share of any wage rise
  attributed to the ladder.
- Gaps are reported with 90 per cent intervals. No verdict rests on
  statistical significance alone.
- **What the design cannot say, stated in advance.** It cannot say what a
  national floor would have done to jobs that no ladder ever covered: small
  food stalls, own-account workers, jobs in firms under 25 employees. No such
  floor existed. The record speaks to the jobs the tailor measured.

## 4. Data (pointers; detail in `office/SOURCES_REPORT.md`)

| Id | Series | Source | Coverage | State |
|---|---|---|---|---|
| W1a | OWS occupational wages, June: 25th percentile, median, 75th percentile, basic and gross, full-time residents, firms of 25+ | stats.mom.gov.sg, per-year tables | 2011 confirmed, earlier PENDING, to 2025 | not received |
| W1b | OWS on data.gov.sg (incl. "Occupational Wages by Industry") | data.gov.sg | PENDING | not received |
| W1c | LFS median gross monthly income from work, full-time employed residents | data.gov.sg `d_9cd9c40f22a4e45cac8f8b9d895fd5ce` | PENDING | not received |
| W2a | Workers by detailed services industry (includes foreign workers) | SingStat M601481 | PENDING | not received |
| W2b | Employed residents by occupation | LFS, data.gov.sg | PENDING; detail level unknown | not received |
| W2c | Employment change by industry and residential status | MOM, data.gov.sg | PENDING | not received |
| W3 | PWM start dates and wage schedules | MOM, NEA, SPF, NParks, BCA; S 240/2014 | 2012-2026 | located, not read |
| W3b | Local Qualifying Salary (earlier the FTE salary threshold): amounts and dates | MOM; archived MOM FAQs | S$1,000 (start PENDING) to S$1,400 (2020) | amounts from secondary sources; primary not saved |
| W4a/b | CPI all items; CPI lowest 20% households; 2019 = 100, annual | SingStat | PENDING | not received |
| W5 | Hong Kong 2011, UK 2016, Germany 2015 | papers and commission reports | -- | context only |

**Definitions fixed now.**

- **Bottom pay:** the 25th percentile of monthly gross wage, full-time
  residents, from the June OWS. Gross is used because it is what the worker
  takes home before CPF. Basic wage, which is what the cleaning, security and
  landscape ladders set, is reported as a sensitivity, and it is what T5 uses.
- **Groups.** Three covered groups and one comparison set, each built from
  OWS occupation titles.
  - **Cleaning:** cleaner titles.
  - **Security:** security guard and officer titles.
  - **Landscape:** gardening and landscape labourer titles.
  - **Comparison set C:** titles first covered on or after 1 September 2022:
    - shop sales assistant and cashier;
    - waiter, kitchen or food preparation assistant, food and drink stall
      assistant, and dishwasher;
    - general office clerk;
    - car, van and lorry drivers, excluding conservancy drivers, whom the
      cleaning ladder covers.
  - **The mapping is written into `office/OCCUPATION_MAP.csv` from the OWS
    title lists alone, before the seal.** A title-listing script prints the
    title column and nothing else. A title missing in any year of a group's
    window is dropped from that group. No title is added or dropped after a
    wage value has been seen. `PENDING`.
- **Group value in a year:** the equal-weight mean, across the group's titles,
  of log 25th-percentile gross wage. **Gap:** a covered group's value minus
  comparison set C's value, same year. Deflating by CPI changes nothing in a
  gap, since both sides share one index.
- **Real pay (level, descriptive):** nominal divided by CPI all items (W4a),
  2019 = 100, for the survey year. Sensitivity: CPI for the lowest 20 per cent
  of households (W4b).
- **Employment:** workers by detailed industry (W2a).
  - Covered: cleaning activities, private security activities, landscape care
    and maintenance.
  - Comparison: retail trade plus food and beverage service activities.
  - SSIC codes are read from the file before the seal.
  - Where a covered activity is not a separate line, the smallest industry
    that contains it is used, and that is stated.

## 5. Windows and years excluded, fixed now

| Group | First public step | Last pre-period June | Bound for all residents in scope | First post-period June | Post-period Junes |
|---|---|---|---|---|---|
| Cleaning | Tripartite Cluster for Cleaners, 19 Oct 2012 | 2012 | 1 Sep 2015 | 2016 | 2016-2019, 2022 |
| Security | Security Tripartite Cluster, Oct 2014 | 2014 | 1 Sep 2016 | 2017 | 2017-2019, 2022 |
| Landscape | NParks announcement, Apr 2015 | 2014 | June 2016 | 2017 | 2017-2019, 2022 |

- **Pre-period:** every June from the first OWS year to the last pre-period
  June. At least 4 Junes are needed. A group with fewer is dropped from T1,
  T2 and T5 and reported descriptively.
- **Transition Junes (not scored, shown):** cleaning 2013-2015, security
  2015-2016, landscape 2015-2016.
- **2020 and 2021 are excluded from every scored test**: the circuit breaker,
  the Jobs Support Scheme wage subsidies and closed borders moved pay and
  jobs for reasons unrelated to the ladders. Shown and labelled.
- **The comparison ends at June 2022.** From 1 September 2022 in-house
  cleaners, guards and landscape workers were covered, retail was covered, and
  the Local Qualifying Salary became a condition for work passes. From March 2023 food services and
  office and driving jobs were covered. After that almost no uncovered
  low-wage job was left to compare against: about 94 per cent of full-time
  lower-wage workers, by MOM's count. 2023-2025 are shown, not scored.
- **Employment windows** (T4) use calendar years with the same cut points.
  Pre-period: every year to 2012 (cleaning) or 2014 (security, landscape).
  Post-period: 2016 (cleaning) or 2017 (security, landscape) to 2019, plus
  2022.

## 5A. What economic theory says (context only)

This section adds no test and changes no threshold.

In the textbook competitive market, a wage floor above what a job is worth to
an employer removes the job. That was the standard view, set out by Stigler
(1946). Robinson (1933) described the other case. An employer who is one of
few buyers of a kind of labour pays less than the worker is worth, because
raising pay to attract one more worker means raising it for all. Under that
employer, a floor set in the right range raises pay and employment together.
Card and Krueger (1994) compared fast-food restaurants in New Jersey, which
raised its minimum wage in 1992, with neighbouring Pennsylvania, which did
not. They found no fall in employment. Manning (2003) argued that some
wage-setting power is normal, since changing jobs is costly. Later work on
large national floors (Germany 2015, the UK 2016) found clear wage gains with
small or no job losses. Hong Kong's 2011 floor had mixed findings (W5).

One point is particular to Singapore. A floor that covers only resident
workers, in jobs that also employ foreign workers under quota, invites
employers to swap one for the other where the quota leaves room. A national
floor with the same resident-only scope would share that gap. So the question
the record can answer is narrow: in the jobs where a floor was set, did
employers behave as if they had wage-setting power?

Sources: J. Robinson (1933), *The Economics of Imperfect Competition*;
G. Stigler (1946), "The Economics of Minimum Wage Legislation", *American
Economic Review*; D. Card and A. B. Krueger (1994), *American Economic Review*
84(4); A. Manning (2003), *Monopsony in Motion*; A. Goodman-Bacon (2021),
"Difference-in-differences with variation in treatment timing", *Journal of
Econometrics*. Not in `raw/`; cited for the argument, not for any figure.

## 6. Pre-registered tests

A failed prediction is a finding to publish, not a reason to change the test.
Thresholds marked "judgement" are the researcher's, stated with reasons, and
accepted or changed by Jacob before the seal.

### T1. Parallel before (the design test)

If the comparison is fair, covered and comparison jobs moved in parallel
before the ladders were announced.

- **Estimate.** For each covered group, the gap (section 4) in each
  pre-period June; OLS of gap on year. The slope is the pre-period drift in
  log points a year. Reported with a 90 per cent interval (HC1).
- **Prediction.** Every group with at least 4 pre-period Junes has a drift
  smaller than 1.0 log point a year in absolute value.
- **Survive if:** |slope| < 0.010 for every such group.
- **Fail if:** |slope| >= 0.010 for any group. **That group fails the design,
  and the article says so:** it is dropped from T2 and T5 scoring, and its
  after-minus-before gap is shown as uninterpretable. If every group fails,
  T2 and T5 are not scored (they drop out of the count and the Brier score).
  The verdict is then "the record cannot say", and that is published.
- **If no group has 4 pre-period Junes:** T1 cannot be run. It is not scored,
  and neither are T2 and T5. The verdict is "the record cannot say".
- **Direction reported.** A negative drift (covered jobs falling behind before)
  means T2 understates the ladder; a positive drift (already catching up)
  means T2 overstates it.
- **Why 1.0 log point a year (judgement).** The post-period sits about five
  years after the middle of the pre-period. A drift of 1.0 a year carried
  forward is about 5 log points, half of T2's survive line. A drift larger
  than that could produce or erase T2's result on its own.
- **Leans toward FAIL, stated now.** The groups were picked because their pay
  lagged, and single-occupation percentiles are noisy over few years; all
  groups must pass.
- **Confidence at seal: set by Jacob (PENDING).** Researcher's proposal:
  40%. Selection on lagging pay makes a drift
  likely, and with three groups and short noisy series one of them will
  probably cross a 1.0-a-year line even if the underlying trends were
  parallel.

### T2. The suit fits: pay rose where the ladder was hung (magnitude)

- **Estimate.** For each covered group that passed T1: mean gap over its
  post-period Junes minus mean gap over its pre-period Junes, in log points.
  **Pooled:** the equal-weight mean across those groups. Reported with 90 per
  cent intervals (regression of gap on a post-period indicator, HC1).
- **Prediction.** Bottom pay in covered jobs rose by **at least 10 log points
  (about 10.5 per cent) more** than in comparison jobs, pooled, and by more
  than zero in every scored group.
- **Survive if:** pooled >= 0.10 **and** every scored group > 0.
- **Fail if:** pooled < 0.05, **or** any scored group <= 0. Either means the
  ladder did not visibly lift the bottom of the jobs it covered, relative to
  jobs it did not cover.
- **Between (pooled in [0.05, 0.10) with every group positive):**
  inconclusive, published as inconclusive.
- **Why 10 and 5 log points (judgement).** No source fixes the size of gain
  that matters. The ladders were meant to lift pay that had not moved, so a
  relative gain under 5 log points over four to six years is within what
  year-to-year noise in an occupation percentile could produce, and counts
  as no visible lift. Ten log points is the smallest gain that would amount
  to the ladder visibly lifting the bottom.
- **Sensitivities, reported, not scored:** basic instead of gross; median
  instead of 25th percentile; dropping 2022; leaving out each comparison
  title in turn; the first transition June counted as post-period.
- **Leans toward understating, stated now.**
  - Cleaners employed in-house (covered only from 2022) sit inside the
    cleaner titles and dilute the cleaning estimate.
  - Comparison jobs were lifted by the same tight market, levies and wage
    guidelines.
  - The LQS put a floor under comparison jobs in firms holding foreign worker
    quota, and it rose in steps during the post-period. The June surveys
    fell under S$1,000 in 2016-2017, S$1,100 in 2018, S$1,200 in 2019 and
    S$1,400 in 2022, dates `PENDING`. A floor lifting the comparison bottom
    narrows the gap T2 measures.
  - All three push toward FAIL. So a pass is strong evidence that the ladder
    lifted pay where it applied, and a fail is weak evidence that it did not.
- **Confidence at seal: set by Jacob (PENDING).** Researcher's proposal:
  50%. The ladders were set to bite, and MOM's
  public claims (background knowledge, disclosed) point to faster wage growth
  in PWM jobs. But dilution, the 25-employee floor of the survey and a
  comparison set lifted by the same forces make 10 log points on the pooled
  measure, with every group positive, a close call.

### T3. The rest of the bottom: did uncovered jobs keep pace? (the tailor's cost)

The tailor's extreme says jobs without a ladder are left behind.

- **Estimate.** Growth of comparison set C's value (section 4) from start to
  end, minus growth of the middle over the same span.
  - **Start:** the mean of the June 2010-2012 values available, at least two.
  - **End:** the mean of June 2017-2019.
  - **The middle:** the OWS all-occupations median gross wage if the tables
    carry one, otherwise the LFS median gross monthly income from work of
    full-time employed residents (W1c).
  - This window is the years when only the three early ladders existed, and
    ends before 2020.
- **Prediction.** The uncovered bottom kept pace: its growth fell short of
  the middle's by **less than 5 log points** over the span.
- **Survive if:** shortfall < 0.05 (including any case where the uncovered
  bottom grew faster).
- **Fail if:** shortfall >= 0.05: uncovered low-wage jobs fell behind the
  middle, as the tailor's extreme predicts.
- **Why 5 log points (judgement).** About 0.7 log points a year over seven
  years; a smaller shortfall is within the drift that a different survey
  (if W1c is used) and composition change could produce.
- **Leans toward SURVIVE, stated now.** The LQS was a floor under these
  jobs, looser than a ladder, in firms that held foreign worker quota. It
  rose from S$1,000 to S$1,200 between the start and end of the window
  (dates `PENDING`). A rising floor under the uncovered bottom is exactly
  what helps it keep pace. So "kept pace" is weak evidence that jobs without
  a ladder did not need one, and "fell behind" is strong evidence that they
  did, since it happened despite that floor. If the S$1,000 threshold began
  inside the window, that is marked on the chart.
- **Confidence at seal: set by Jacob (PENDING).** Researcher's proposal:
  60%. A tight labour market, higher foreign worker
  levies and dollar-amount wage guidelines lifted low pay broadly in these
  years, and background knowledge (disclosed) recalls MOM reporting the 20th
  percentile growing faster than the median late in the decade. But
  occupation-level percentiles for retail and food service jobs can lag
  through part-time mix and churn.

### T4. Did the jobs survive the fitting? (competitive or monopsony)

- **Estimate.** For each covered industry (section 4): mean log workers over
  its post-period years minus mean over its pre-period years, minus the same
  difference for the comparison industries combined. Reported with a 90 per
  cent interval.
- **Employment pre-trend condition, fixed now.** The same drift check as T1,
  on the log-workers gap over pre-period years, with a line of 2.0 log points
  a year. Head counts move more than percentiles, hence the wider line
  (judgement). An industry that fails it is dropped from T4 and reported. If
  all three fail, T4 is not scored.
- **Prediction.** Employment in covered industries held up: relative change
  **greater than -5 log points** in every scored industry.
- **Survive if:** every scored industry > -0.05.
- **Fail if:** any scored industry <= -0.10: jobs fell where the floor bound,
  the competitive signature.
- **Between:** inconclusive.
- **Leans toward SURVIVE, stated now.**
  - Buildings must be cleaned and guarded, by law and in practice; much of the
    demand comes from the government and large landlords. Demand that is hard
    to cut keeps jobs even under a competitive market.
  - W2a counts foreign workers, whom the ladders did not cover. A firm that
    replaced residents with foreign workers under its quota shows no fall
    here.
  - Both lean toward "jobs held". A resident-versus-foreign check (W2c) is
    described beside the result, not scored.
- **One lean the other way:** security. Its industry transformation plan
  pushed technology in place of guards in the late 2010s, which could shrink
  guard numbers for reasons unrelated to pay. Named, not separated.
- **Confidence at seal: set by Jacob (PENDING).** Researcher's proposal:
  60%. Hard-to-cut demand and foreign workers in
  the count both favour holding, but security's technology push and the
  cleaning industry's own productivity drive could produce a relative fall of
  5 log points in one of three industries.

### T5. The first rung shows up in the survey

If the ladder bound, the bottom quarter of covered workers in the survey was
paid at least the ladder's first rung.

- **Estimate.** In each post-period June, each scored group's 25th-percentile
  **basic** wage (averaged across its titles, not logged) divided by the
  entry-rung basic wage in force on 1 June of that year, from the W3
  schedules:
  - cleaning: the lowest of the cleaner schedules;
  - security: the entry grade (security officer);
  - landscape: the entry grade.

  The W3 schedules are tabulated before the seal (`PENDING`), since they are
  the policy, not the outcome.
- **Prediction.** The ratio is at least 0.97 in every post-period June for
  every scored group.
- **Survive if:** every ratio >= 0.97.
- **Fail if:** any ratio < 0.97.
- **Why 0.97 (judgement).** Allows for rounding in published percentiles and
  a schedule step falling close to the survey month.
- **Leans toward FAIL for cleaning, stated now:** in-house cleaners, not
  bound until 2022, sit inside the cleaner titles and can pull the 25th
  percentile below the contract rung. A fail here says the floor was not the
  bottom of the occupation, which is itself the tailor's point.
- **The LQS sits near the entry rungs.** The cleaning ladder's entry basic
  wage was S$1,000 to S$1,200 (checker disclosure, SOURCES_REPORT section 1
  item 7), and the LQS was S$1,000 to S$1,400 over the post-period Junes.
  - In a year when the LQS sat above a rung, firms with foreign worker quota
    had a reason to pay above the rung anyway. That lifts the 25th
    percentile and leans T5 toward SURVIVE for reasons other than the
    ladder.
  - The LQS is a monthly salary threshold, and whether it counted basic or
    gross pay in each year is `PENDING`. T5 reads basic, so the lean is
    smaller if the LQS counted gross pay.
  - The years in which the LQS exceeded each entry rung are marked in the
    T5 table, from the W3 and W3b schedules, before the seal.
- **A separate bet from T2** (checker review of `cb9fe70`, item 3). T2 is
  relative: covered against comparison jobs. T5 is a level: covered jobs
  against their own rung. Either can hold without the other, so T5 stays
  scored.
- **Confidence at seal: set by Jacob (PENDING).** Researcher's proposal:
  45%. Security and landscape probably clear their
  entry rung, but cleaning's in-house mix and any year where a scheduled step
  landed just before the June survey make "every group, every year" fragile.

### T6. Lift and escalator, waste management, and the 2022-2023 wave (descriptive only, no prediction)

Shown on the chart with their dates. Not scored:

- Lift and escalator: mid-wage, a small cell, no clean start date.
- Waste management: small, and overlaps the cleaning ladder.
- The 2022-2023 wave: after it, almost no uncovered comparison job remained,
  and the Local Qualifying Salary and Progressive Wage Credit Scheme changed
  at the same time.

The article says in words what the second wave can and cannot show.

## 7. The side section: what the ladder does not cover (bounded)

One descriptive fact, not a test: the share of full-time lower-wage workers
covered by any ladder, before and after 2022, as MOM states it (W3). And one
sentence naming what the design cannot reach:

- workers in firms under 25 employees (outside OWS);
- own-account workers;
- foreign workers (outside every ladder).

Capped at about 150 words in the article.

## 8. The verdict rule (fixed at seal)

The headline question asks "minimum wage or PWM", but the record can test
only the ladder directly. So the verdict has two parts in one sentence
(checker review of `cb9fe70`, item 4):

- **Part A, the ladder:** which model the covered jobs look like, from T2 and
  T4, gated by T1.
- **Part B, the rest of the bottom:** whether uncovered low-wage jobs kept
  pace with the middle, from T3. This is the evidence on the minimum-wage
  side of the argument: a floor for everyone is the answer to a bottom that
  a ladder for a few leaves behind.

**Part A. Exactly one of these:**

- **"the record cannot say what the ladder did"**: T1 fails for every group
  or cannot be run. Stated plainly: covered and comparison jobs were already
  drifting apart, or there are too few years before the ladders to tell.
- **"covered jobs look more like monopsony"**: T2 survives **and** every
  scored industry in T4 shows a relative employment change of zero or more.
  Pay rose where the floor bound, and jobs did not fall.
- **"covered jobs look more like a competitive market"**: T2 survives
  **and** T4 fails. Pay rose and jobs fell.
- **"the ladder did not measurably lift pay at the bottom of the jobs it
  covered"**: T2 fails.
- **anything else: "the record cannot tell the two models apart"**,
  published as plainly as the others.

**Part B. Exactly one of these:**

- **"the rest of the bottom kept pace"**: T3 survives.
- **"the rest of the bottom fell behind"**: T3 fails.
- **"the record cannot say whether the rest of the bottom kept pace"**: T3
  cannot be computed (fewer than two start-window Junes).

T3 does not read the covered groups, so T1 does not gate it. T5 is scored
for calibration and reported beside the verdict; it does not enter it.

**The verdict sentence is Part A, a semicolon, then Part B**, for example:
"Covered jobs look more like monopsony; the rest of the bottom fell behind."
Both parts are printed whatever they say. Neither is dropped because the
other is more striking.

**Weak-evidence sentence, carried next to the verdict in the article,
verbatim:** "A monopsony-like result is weak evidence and a competitive result
is strong evidence, because the design leans toward the monopsony reading."
The reasons, stated now:

- demand for cleaning and guarding is hard to cut;
- the job counts include foreign workers whom the ladders did not cover.

Both keep jobs looking steady whether or not the floor cost resident jobs.

**Two further leans, stated beside the verdict in the article:**

- **The pay test leans the other way (T2).** In-house cleaners dilute the
  covered side, and the LQS floor lifted the comparison side. So a pay gain
  found is strong evidence, and none found is weak.
- **Part B leans toward "kept pace" (T3).** The LQS was a floor under the
  uncovered jobs too, and it rose during the window. So "kept pace" is weak
  evidence, and "fell behind" is strong evidence.

Beside the verdict the article also carries the limit in section 3: the
record cannot say what a national floor would have done in jobs no ladder
reached.

**Confidences and the scorecard.**

- Five predictions are scored for calibration: T1, T2, T3, T4, T5.
- A prediction "holds" when its survive-if condition is met.
- "Inconclusive" counts as not holding.
- A test reported as not scored (T2 and T5 when T1 removes every group; T4
  when every industry fails its pre-trend condition) drops out of both the
  count and the Brier score, and the article says so.

Expected number holding: from Jacob's confidences, written in at the seal.
Under the researcher's proposals it would be 2.55 of 5 (0.40 + 0.50 + 0.60 +
0.60 + 0.45). The predictions are correlated (T1 gates T2 and
T5; T2 and T5 read the same wages), so the actual count spreads wider than
five independent calls would.

## 9. What would prove the framing wrong, and what it leaves out

- **OWS coverage.** If the per-year tables start in 2011, cleaning has too
  few pre-period Junes and drops out. The design then rests on security and
  landscape. `PENDING` until the files arrive.
- **Occupation codes.** A title that cannot be bridged across a SSOC revision
  ends that title's series, which can thin a group. Fixed from titles before
  the seal.
- **OWS method change.** If a year's method note shows a break (for example,
  more use of administrative records), the level shift is a measurement
  change. `PENDING`: recorded by amendment, shown on the chart.
- **Contract versus in-house.** If occupation-within-industry tables isolate
  cleaners in the cleaning industry, that becomes the cleaning series. The
  choice is made from the table structure before the seal, not from values.
- **Workfare.** Singapore's other tool for low pay tops up income through
  the state rather than the employer. It is not in wages and not measured
  here. The article names it, because "which lifts lowest pay" in Singapore
  has three answers, not two.
- **The LQS start date.** If the S$1,000 threshold began inside a
  pre-period (2009-2014), the comparison side had a floor change inside the
  window T1 reads. `PENDING` from the archived MOM FAQs. It is marked on the
  chart, and it does not move any window.
- **Foreign workers.** Outside every ladder and outside OWS's resident
  scope. A national floor that also left them out would share the gap. The
  article says so.

## 10. Open before the seal

Settled in the checker review of `cb9fe70` (27 September 2026):

- thresholds accepted as drafted;
- T5 stays scored;
- T3 is part of the verdict sentence (section 8);
- checker disclosure recorded (SOURCES_REPORT section 1, item 7);
- the LQS is stated as a lean (section 3, T2, T3, T5);
- **answer due December 2026**, subject to the downloads.

Still open:

1. Coverage: download and run `00_coverage.py`; write every year range in
   sections 5 and 6 as numbers.
2. Occupation map: title-listing script, then `office/OCCUPATION_MAP.csv`,
   before any wage value is opened.
3. W3 schedules: tabulate entry-rung basic wages by date for cleaning,
   security and landscape, for T5.
4. W3b: date each LQS step from MOM primary pages (archived FAQs), and
   whether it counted basic or gross pay. Mark in the T5 table the years in
   which the LQS exceeded each entry rung.
5. Dates `PENDING`: landscape day in June 2016 (does not move any window);
   the October 2014 security report itself.
6. Confidences: Jacob sets the final numbers, sent through the checker.
