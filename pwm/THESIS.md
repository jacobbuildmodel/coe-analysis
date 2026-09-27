# THESIS: Minimum wage or the Progressive Wage Model -- which actually lifts Singapore's lowest pay?

**UNSEALED DRAFT, 27 September 2026. Not for publication. Nothing below is
final until Jacob sets the confidences and the file is sealed in a commit of
its own. After the seal it is never edited; changes go in
`THESIS_ADDENDUM.md`, dated, and are reported, not applied to the scoring.**

Author: `pwm` (Claude Code session). Repository: coe-analysis, subdirectory
`pwm/`, branch `pwm-wip`.

Evidentiary basis of this draft: the files received on 27 September 2026
(`raw/RETRIEVED.txt`), checked for coverage only by `00_coverage.py`.
- Occupation titles, SSOC codes and column headers of the OWS tables were
  listed by `01_titles.py`, which reads no wage or head-count column.
- Policy documents (W3, W3b) were read for dates and rung amounts.
- The SSOC correspondence tables and the SSOC 2010 hierarchy (`w1d_*`)
  were read for the occupation links.
- No wage value from W1 and no employment value from W2 has been opened.
- Values that were seen (single-date counts, policy settings, survey
  metadata, CPI figures, two qualitative statements in policy reports) are
  listed in `office/SOURCES_REPORT.md` section 1.

Revision history before the seal:
- `34122a7`/`cb9fe70`: first draft.
- `5359678`, after the checker review of `cb9fe70`:
  - checker disclosure;
  - the Local Qualifying Salary stated as a floor under the comparison jobs
    before 2022, with its leans at T2, T3 and T5;
  - T5 kept as a scored bet;
  - T3 made part of the verdict sentence;
  - thresholds accepted;
  - confidences relabelled as the researcher's proposal, pending Jacob's
    numbers;
  - answer due December 2026.
- This revision, after the checker review of `4a4cdae` (the downloads):
  - year ranges as numbers;
  - 2009-2011 confirmed;
  - the 2007-2008 and 2009 rules;
  - the occupation map and its classification breaks, with a T1 lean;
  - the rung and LQS tables on a 1 June rule;
  - W2c does not exist;
  - CPI tables rebased to 2024.
- `c16f695` and then this revision, after the checker review of `c16f695`:
  - grade splits: the main series keeps only lowest-rung successors, with
    all successors as the sensitivity (section 4, T2, T5);
  - the June 2015 workplace split rule;
  - Number Covered weights as a sensitivity;
  - the averaging step inside cleaning's pre-period added to T1's lean.
- This revision, after the checker review of `41921ee`/`77dd3f3` (last
  pre-seal step):
  - the map's `series` column split into `series` (main, sensitivity or
    excluded) and `series_note`;
  - every occupation link settled from the SSOC tables in `raw/`; the final
    groups in section 4, with 91190 added to cleaning's main series and
    91140 dropped under the missing-year rule;
  - the T2 lean from 91160, a 9113 successor outside the main series;
  - every rung settled from the primaries (T5);
  - the LCR captures of 2019-2021, and both readings for the other Junes;
  - rules fixed now for what the LQS captures do not settle;
  - no `PENDING` left (section 10).
- This revision, after the checker review of `fdb1bf5`:
  - T4 takes T1's minimum of 4 pre-period years: cleaning's employment is
    described, not scored; T4 is scored on security and landscape;
  - the W2a lines named now from the label listing (`01b_w2a_labels.py`,
    `office/w2a_labels.txt`), not after the seal;
  - the listing shows that neither W2a file counts workers: T4 has no
    series in `raw/`, the one item open before the seal (section 10).
- This revision, after the checker's decision on `d292fe9` (option (a),
  with (b) as the fixed fallback), fixed before any new file arrives:
  - T4's series by priority: a count of workers by industry (main); LFS
    employed residents by detailed occupation (sensitivity, or main if it
    is the only one); otherwise T4 is not scored;
  - T4's pre-period starts at the first year the chosen series covers, with
    the 4-year minimum per industry; cleaning is scored if that admits it;
  - the resident-versus-total difference between the two series, stated.

Markers: no `PENDING` marker remains. Every link, rung, date and industry
line is settled from documents in `raw/`, never from a wage or employment
value, or is covered by a rule fixed now. One item is open and blocks the
seal: which T4 series qualifies, under rules already fixed (section 10). `[JACOB]` = the confidence Jacob
sets at the seal. "Researcher's proposal" = the researcher's confidence, kept
for the record.

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
    food outlets in comparison set C. From MOM's own pages (W3b, the
    archived quota FAQs; table in T5):
    - S$1,000 in force by 15 November 2016 (start date not found);
    - S$1,100 from 17 July 2017;
    - S$1,200 from a date not captured (between January 2018 and July 2019);
    - S$1,300 from 30 June 2019;
    - S$1,400 from 1 July 2020, to 30 June 2024.

    **Rule, fixed now:** the threshold in force on 1 June applies to that
    June survey, as for T5's rung.

    **Rule, fixed now, for what the captures do not settle.** The LQS enters
    no computation; it is a stated lean only. Three things are not settled,
    and no further search is made:
    - the Junes to 2016, when the threshold may not yet have existed;
    - June 2018 and June 2019, when it was S$1,100 or S$1,200;
    - whether it counted basic or gross pay (the FAQs say only "monthly
      salary").

    For each, both readings are stated, and every lean is stated in the
    direction that holds under both (T1, T2, T3, T5).

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
| W1a | OWS occupational wages, June: 25th percentile, median, 75th percentile, basic and gross, full-time residents, firms of 25+ | stats.mom.gov.sg, per-year tables (2010-2011 and 2016-2024 via Wayback captures of MOM's pages) | **spreadsheets June 2009-2025**; June 2007 and 2008 in PDF only | in `raw/`, values unopened |
| W1b | OWS on data.gov.sg | data.gov.sg | June 2024 only | in `raw/`, cross-check only |
| W1c | LFS median gross monthly income from work, full-time employed residents, incl. and excl. employer CPF | data.gov.sg `d_9cd9c40f22a4e45cac8f8b9d895fd5ce` | `raw/RETRIEVED.txt` | in `raw/`, values unopened |
| W2a | Key indicators by detailed services industry: establishments, operating revenue, operating expenditure, gross operating surplus, value added. **No count of workers** (label listing) | SingStat M601481 via data.gov.sg; group-level companion table | detailed 2010-2024; group 2000-2024 | in `raw/`, labels listed, values unopened |
| W2b | Employed residents by occupation | LFS, data.gov.sg | `raw/RETRIEVED.txt` | in `raw/`, values unopened |
| W2c | Employment by industry AND residential status | -- | **does not exist**: no public series splits industry employment by residence | -- |
| W3 | PWM start dates and entry-rung schedules | MOM, NEA, SPF, NParks, BCA; S 240/2014 | 2012-2029 | in `raw/`; rungs tabulated at T5 |
| W3b | Local Qualifying Salary (earlier the FTE salary threshold) | MOM pages and archived MOM FAQs, 2016-2021 | S$1,000 (by Nov 2016) to S$1,400 (1 Jul 2020) | in `raw/`; table at T5 |
| W4a/b | CPI all items (M213801); CPI lowest 20% of households (M213911); 2024 = 100, annual | SingStat API, JSON | 1961-2025; 1993-2025 | in `raw/`, values unopened |
| W5 | Hong Kong 2011, UK 2016, Germany 2015 | papers and commission reports | -- | context only |

**Definitions fixed now.**

- **Bottom pay:** the 25th percentile of monthly gross wage, full-time
  residents, from the June OWS. Gross is used because it is what the worker
  takes home before CPF. Basic wage, which is what the cleaning, security and
  landscape ladders set, is reported as a sensitivity, and it is what T5 uses.
- **Groups.** Three covered groups and one comparison set, each built from
  the OWS all-industries occupation table (the table of occupations within
  the industry does not isolate cleaning, security or landscape firms: it is
  "Business Services" to 2020 and "Administrative and Support Services" from
  2021).
  - **Cleaning:** the office and industrial-establishment cleaner line:
    - SSOC 2005 91291 and 91292 (2009);
    - SSOC 2010 91131 and 91132 (2010), then 9113 (2011-2014);
    - its SSOC 2015 and 2020 successors, under the split rules below.
      Main series:
      - 91130 office cleaner, 91151 F&B establishment cleaner and 91190
        cleaner in other establishments (shopping malls, schools, hospitals)
        (2015-2019);
      - 91131 indoor cleaner and 91151 F&B general cleaner (2020-2022).
  - **Security:** private security guard (2009), security guard 5414
    (2010-2019), then, in the main series, private security officer 54144
    (2020-). Senior private security officer 54143, security supervisor
    54142 and senior security supervisor 54141 enter the sensitivity only.
  - **Landscape:** gardener (2009), garden labourer (2010), park and garden
    maintenance worker 9214 (2011-2022).
  - **Comparison set C:** titles first covered on or after 1 September 2022:
    - shop sales assistant, cashier;
    - waiter, kitchen assistant, food/drink stall assistant;
    - general office clerk;
    - van driver, lorry driver.

    Dishwashers left the set: the cleaning ladder names them in its F&B
    group (`raw/w3_cleaning_col_order_2021.pdf`), and the food services
    ladder covers them from 2023. No car-driver title is published. Food
    service counter attendant is absent from June 2009.
  - **The mapping is in `office/OCCUPATION_MAP.csv`**, written from the title
    listing (`01_titles.py`, `office/titles_listing.txt`: titles, codes and
    headers only) before any wage value was opened.
    - **Linking rule, fixed now:** the same title text (ignoring case and
      spacing) is linked. A split or merge is linked only through the
      official SSOC correspondence table, or, within one SSOC version, the
      classification's own hierarchy. The tables are in `raw/`
      (`w1d_ssoc2010_correspondence.xls`, `w1d_ssoc2010_report.pdf`,
      `w1d_ssoc2015_correspondence.xls`,
      `w1d_ssoc2015v2018_correspondence.xls`,
      `w1d_ssoc2020_correspondence.xlsx`). Every link in the map is settled
      from them; the composition changes they show are listed at T1.
    - **Rule for anything the tables cannot settle, fixed now:** it is
      excluded from the main series and listed. Nothing fell under it.
    - A title (or linked line) missing in any scored June of a group's
      window is dropped from that group. A line that continues into new
      codes through the correspondence is not missing. **Applied:**
      - 91140 industrial establishment cleaner is absent from June 2018.
        The rule as written drops a title from its group, so it leaves the
        main series and the sensitivity alike (`series` = excluded).
      - 91170 cleaner in open areas is absent from June 2019, and is
        excluded by the workplace-split rule in any case.
    - **Grade splits, rule fixed now.**
      - The pre-period lines (5414 security guard; 9113 cleaner in offices
        and other establishments) are whole occupations, whose 25th
        percentile sits at the entry grade. Averaging in a successor that
        the ladder places on a higher rung would lift the group
        mechanically after the split, and push T2 and T5 toward SURVIVE.
      - So when a line splits by grade, the **main series keeps only the
        successor(s) that match the sector's lowest rung**, as the ladder
        documents in `raw/` name it. **All successors averaged is the
        sensitivity.**
      - Applied (`office/OCCUPATION_MAP.csv`, column `series`):
        - **Security, June 2020.** Main: 54144 private security officer, the
          Security Officer (SO) rank. Sensitivity only: 54143 senior private
          security officer, the Senior SO rank; 54142 security supervisor
          and 54141 senior security supervisor, the supervisor ranks, which
          come from 2015's 54141 and so from the same 5414 line
          (`w1d_ssoc2020_correspondence.xlsx`). The ranks are from
          `w3_security_stc_2017.pdf` Annex C and
          `w3_security_spf_licensing_conditions_2018.pdf` section 2.
        - **Cleaning, June 2020.**
          - Main: 91131 indoor cleaner, "General / Indoor Cleaners", and
            91151 F&B general cleaner, "General Cleaners". Both are on the
            lowest rung, >= S$1,274 (`w3_cleaning_col_order_2021.pdf`, para
            1.1).
          - Sensitivity only, each on a higher rung in the same schedule:
            91132 outdoor cleaner ("Outdoor Cleaners / Healthcare Cleaners /
            Restroom Cleaners", >= S$1,486); 91133 multi-skilled cleaner cum
            machine operator (>= S$1,698); 91161 residential and open areas
            general cleaner (conservancy group, lowest rung >= S$1,486).
        - **Cleaning, June 2015** (workplace split; grades by the same rule).
          - Main: 91130 office cleaner and 91190 cleaner in other
            establishments (office and commercial group), and 91151 F&B
            establishment cleaner (F&B group). Both groups start on the
            lowest rung, "at least $1,000"
            (`w3_cleaning_tcc_report_2012.pdf`). The ladder's lowest
            office-and-commercial rung names "Offices, Schools, Hospitals and
            Polyclinics" (`w3_cleaning_tcc_2016.pdf`, Annex C), which is
            91190's scope.
          - 91140 industrial establishment cleaner would be main, but is
            dropped by the missing-year rule (above).
          - Sensitivity only: 91160 residential area cleaner. Its title spans
            HDB estates (conservancy group, "at least $1,200", same 2012
            file) and condominiums (office and commercial group,
            `w3_cleaning_mom_page.pdf`), so it does not match the lowest rung
            cleanly.
          - Excluded: 91170 cleaner in open areas (workplace-split rule,
            below).
        - **Landscape:** no grade split inside the scored window (9214
          throughout 2011-2022).
    - **Workplace splits, rule fixed now.** At June 2015, only successors
      that the SSOC 2010-2015 correspondence maps from 9113 stay in the
      cleaning group. Any that it does not are excluded and listed in the
      map before any value is opened. **Applied**
      (`w1d_ssoc2015_correspondence.xls`):
      - 9113's members map to 91130 (from 91131), 91140 (from 91132), and
        91151, 91160 and 91190 (each from part of 91139). All five stay.
      - 91170 comes only from 96130 sweeper and related worker, so it is
        excluded.
      - 91190 also takes part of 96130. It stays, as a 9113 successor.
    - **Weighting.** Equal weights across a group's titles stay the main
      series. Sensitivity, computed after the seal and reported only: titles
      weighted by the OWS "Number Covered" column of each June, read then and
      not before.
    - No title is added or dropped after a wage value has been seen.
- **Group value in a year:** the equal-weight mean, across the group's titles,
  of log 25th-percentile gross wage. **Gap:** a covered group's value minus
  comparison set C's value, same year. Deflating by CPI changes nothing in a
  gap, since both sides share one index.
- **Real pay (level, descriptive):** nominal divided by CPI all items (W4a,
  SingStat M213801, 2024 = 100), for the survey year. Sensitivity: CPI for the
  lowest 20 per cent of households (W4b, M213911).
  - T1, T2 and T3 compare groups that share one index, so the deflator
    cancels in every one of them.
  - CPI is used only for the charts and for descriptive statements of real
    pay.
- **Employment: the industry lines, fixed now** from the W2a label listing
  (`01b_w2a_labels.py`, `office/w2a_labels.txt`: the `DataSeries` text of
  both W2a files, no value). Where an activity has no line of its own, the
  smallest line that contains it is used, and that is stated. Labels exactly
  as published:
  - **Security:** "SSIC 80 - Security And Investigation Activities". There
    is no line for private security activities alone; this one also holds
    investigation and security-systems firms.
  - **Landscape:** "SSIC 813 - Landscape Planting, Care And Maintenance
    Service Activities". It holds planting as well as upkeep.
  - **Cleaning:** "SSIC 812 - Cleaning Activities". Scored in T4 only if the
    4-year minimum admits it (section 5).
  - **Comparison, combined:** "SSIC 47 - Total Retail Trade" plus "SSIC
    55-56 - Total Accommodation & Food Services". Food and beverage services
    have no line of their own: the file splits them into six lines
    (restaurants; cafes and kiosks; fast food; food courts, hawker centres,
    coffee shops and canteens; pubs; caterers) under the 55-56 total. The
    smallest single line holding all of them is 55-56, which also holds
    hotels and other accommodation, uncovered until September 2022 like the
    rest of the comparison.
  - **The listing shows no count of workers.** Both W2a files carry the
    same five indicators over these lines: Establishments, Operating
    Revenue, Operating Expenditure, Gross Operating Surplus and Value Added.
    Neither counts workers. W2d (employment by 13 broad sectors) cannot
    isolate the three industries. So no file in `raw/` yet holds the series
    T4 needs. The design chat is searching (section 10).
- **T4's employment series, by priority, fixed now** (checker's decision on
  `d292fe9`), before any candidate file arrives:
  1. **Main: a count of workers by industry** for the lines named above
     (security SSIC 80, landscape SSIC 813, cleaning SSIC 812; comparison
     SSIC 47 plus SSIC 55-56).
  2. **Employed residents by detailed occupation (LFS)** for the covered
     titles and the comparison titles of `office/OCCUPATION_MAP.csv` (main
     series), each at the most detailed level the table gives, and no
     coarser than the SSOC unit group (4 digits); major groups do not
     qualify. **A sensitivity if series 1 qualifies; the main series if only
     series 2 qualifies.**
  3. **Neither qualifies: T4 is not scored.** It drops out of the count and
     the Brier score, and Part A can no longer separate the two models: with
     T2 surviving it reads "the record cannot tell the two models apart".

  **"Qualifies"** means: it covers the needed lines at the needed detail,
  every post-period year of at least one covered industry, and at least 4
  pre-period years for that industry (section 5). Which series qualifies is
  judged from its labels (listed as in `01b_w2a_labels.py`) and its
  coverage (first and last year, `00_coverage.py`), never from a value.
- **What each series counts, stated now.**
  - **Series 1 counts all workers, foreign workers included.** The ladders
    covered residents only, so a firm that replaced residents with foreign
    workers under its quota shows no fall. That is the existing lean toward
    "jobs held" (T4, section 8).
  - **Series 2 counts residents only**, who are the people the ladders
    covered. It removes that lean. It adds survey noise instead: the LFS is
    a sample survey, and counts at detailed occupation are small and move
    from year to year for reasons of sampling alone, which leans toward an
    inconclusive or a failed pre-trend condition rather than toward either
    verdict.

## 5. Windows and years excluded, fixed now

| Group | First public step | Pre-period Junes | Transition Junes | Bound for all residents in scope | Post-period Junes |
|---|---|---|---|---|---|
| Cleaning | Tripartite Cluster for Cleaners, 19 Oct 2012 | **2009-2012 (4)** | 2013-2015 | 1 Sep 2015 | 2016-2019, 2022 (5) |
| Security | Security Tripartite Cluster, Oct 2014 | **2009-2014 (6)** | 2015-2016 | 1 Sep 2016 | 2017-2019, 2022 (4) |
| Landscape | NParks announcement, 24 Apr 2015 | **2009-2014 (6)** | 2015-2016 | June 2016 (LCR firms) | 2017-2019, 2022 (4) |

- **Pre-period:** every June from 2009, the first June with OWS
  spreadsheets, to the last June before the first public step. At least 4
  Junes are needed; every group has them.
  - **2009-2011 confirmed usable.** The headers of 2009 and 2010 carry "First
    Quartile ($)", and those of 2011 "25th Percentile ($)", for basic and
    gross wage in separate tables.
  - The method notes for 2008-2011 cover "CPF contributors in full-time
    employment". Those for 2012 on cover "full-time resident employees who
    have CPF contributions". CPF contributors are Singapore citizens and
    permanent residents, so the population is the same. No June leaves its
    pre-period.
- **June 2007 and June 2008 (PDF only) are in no scored test.** Sensitivity,
  reported, not scored: T1 and T2 rerun with 2007-2008 added. They are
  extracted after the seal, and only if the title listing shows the same
  measure and titles.
- **Sensitivity, reported, not scored: T1 without June 2009** (the recession
  trough).
- **Sensitivity, reported, not scored: T1 on the Junes after the last
  pre-period classification break** (section 9): security and landscape
  2011-2014 (4 Junes). Cleaning has only 2011-2012 after its break, too few
  for this sensitivity.
- **Transition Junes (not scored, shown):** cleaning 2013-2015, security
  2015-2016, landscape 2015-2016.
- **2020 and 2021 are excluded from every scored test**: the circuit breaker,
  the Jobs Support Scheme wage subsidies and closed borders moved pay and
  jobs for reasons unrelated to the ladders. Shown and labelled.
- **The comparison ends at June 2022.** From 1 September 2022 in-house
  cleaners, guards and landscape workers were covered, retail was covered, and
  the Local Qualifying Salary became a condition for work passes. From March
  2023 food services and office and driving jobs were covered. After that
  almost no uncovered low-wage job was left to compare against: about 94 per
  cent of full-time lower-wage workers, by MOM's count. 2023-2025 are shown,
  not scored.
- **Employment windows** (T4) use calendar years with the same cut points.
  - **Pre-period: from the first year the chosen series covers** (section 4;
    coverage, not values) to 2012 for cleaning and 2014 for security and
    landscape. Post-period: 2016 (cleaning) or 2017 (security, landscape) to
    2019, plus 2022.
  - **Minimum, fixed now (T1's): 4 pre-period years per industry.** An
    industry with fewer is described, not scored. If the chosen series
    starts in 2009 or earlier, cleaning is admitted and scored; if it starts
    in 2010 or 2011, security and landscape are scored and cleaning is
    described; if it starts in 2012 or later, no industry is admitted and T4
    is not scored.

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
- **Classification breaks inside every pre-period, stated now as a further
  lean toward FAIL** (`office/OCCUPATION_MAP.csv`).
  - **June 2010.** The codes move from SSOC 2005 to SSOC 2010. Security
    (private security guard to security guard) and landscape (gardener to
    garden labourer) change title text there. So do three comparison titles
    (office clerk, food/drink stall assistant, cashier).
  - **June 2011.** MOM publishes four-digit aggregates:
    - cleaning's two titles merge into 9113, "Cleaner in offices and other
      establishments";
    - landscape's garden labourer becomes 9214, "Park and garden maintenance
      worker";
    - the comparison cashier splits back out of "Cashiers and ticket clerk".
  - **What the SSOC tables show about composition** (`w1d_*`; column
    `link_and_break_note` of the map). Every link is settled, but some lines
    change their members:
    - June 2010: waiter loses captain waiters (51311) and kitchen assistant
      loses fast food preparers (94103), so both narrow. General office
      clerk becomes the aggregate 4110, which adds filing, personnel and
      other administrative clerks, broader from 2010. Cashier is the
      aggregate 5230 (with cage/count supervisors, office cashiers and
      ticket clerks) for June 2010 only.
    - June 2011: cleaning's 9113 adds 91139, cleaners in other
      establishments not elsewhere classified, to the two 2010 titles.
      Landscape's 9214 adds grass cutters, tree cutters and other park and
      garden maintenance workers to garden labourers.
    - Security's line keeps the same members from 2009 to 2019 (51440 to
      54140, which is 5414, which is 54141 plus 54142 in SSOC 2015).
  - A relabelled or regrouped line can step up or down for reasons of
    classification alone. A step inside the window T1 reads shows up as
    drift, so each group's T1 carries the stated lean.
  - **Cleaning also carries a mechanical step from averaging.** Its 2009-2010
    value is the equal-weight mean of two titles (office cleaner, industrial
    establishment cleaner). Its 2011-2014 value is one aggregate (9113),
    which weights them by their actual numbers and adds 91139. The switch
    can step the series up or down inside the pre-period with no change in
    anyone's pay.
    The Number Covered weighting (section 4) is the sensitivity that shows
    its size.
  - The sensitivity on the Junes after the last break (section 5) checks it,
    reported, not scored.
- **Confidence at seal: `[JACOB]`.** Researcher's proposal:
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
- **Sensitivities, reported, not scored:**
  - basic instead of gross;
  - median instead of 25th percentile;
  - dropping 2022;
  - leaving out each comparison title in turn;
  - the first transition June counted as post-period;
  - all successors of a grade split averaged, instead of the lowest-rung
    successors of the main series: security 54141, 54142, 54143 and 54144
    (2022); cleaning 91130, 91151, 91160 and 91190 (2016-2019), and 91131,
    91132, 91133, 91151 and 91161 (2022). 91140 and 91170 are not in it:
    the missing-year and workplace-split rules drop them from the group;
  - titles weighted by OWS "Number Covered" instead of equal weights;
  - 2007-2008 added (section 5).
- **Leans toward understating, stated now.**
  - In-house workers in all three groups (cleaners, guards and landscape
    workers employed directly rather than through a contractor) were
    unbound until 1 September 2022. They sit inside the occupation titles
    and dilute each group's estimate. Landscape workers in firms not on the
    Landscape Company Register were also unbound.
  - **Who the landscape ladder bound (the LCR).**
    - The captures of 2019-2021 (`w3_landscape_lcr_2019` to
      `w3_landscape_lcr_2021`, `w3_landscape_lcr_faq_2019` to
      `w3_landscape_lcr_faq_2021`) settle those years. Being paid according
      to the PWM was a condition of LCR listing. Listing was needed for
      government contracts (two consecutive years of LCR status, from 1
      January 2019) and NParks grants, and private buyers were "starting to
      state preferences". No capture ties listing to hiring foreign workers.
      So in June 2019, and in the excluded 2020 and 2021, the ladder bound
      listed firms only.
    - For June 2016-2018 no page was archived, and June 2022 has no capture
      in `raw/`. Both readings are stated: (a) as in 2019-2021, listed firms
      only; (b) listing also gated hiring foreign workers, so nearly every
      landscape firm holding work passes was bound.
    - Under either reading, in-house landscape workers were unbound until 1
      September 2022, so the dilution lean holds either way. Reading (a)
      dilutes more.
  - **Cleaning's workplace split.** The SSOC 2010-2015 correspondence keeps
    91160 residential area cleaner, whose scope includes HDB estates
    (conservancy), as a 9113 successor, and the main series excludes it
    after 2015. Conservancy cleaners sat on a higher rung than the lowest
    (at least $1,200 against $1,000, `w3_cleaning_tcc_report_2012.pdf`).
    Leaving them out lowers the post-period value relative to the
    pre-period line, whose 9113 held them: toward FAIL.
  - Comparison jobs were lifted by the same tight market, levies and wage
    guidelines.
  - The LQS put a floor under comparison jobs in firms holding foreign worker
    quota, and it rose in steps during the post-period. On the 1 June rule
    (section 3), the threshold for each post-period June was:
    - 2016: none or S$1,000 (first capture 15 November 2016; start date not
      found);
    - 2017: S$1,000;
    - 2018: S$1,100 or S$1,200 (the S$1,200 step date is not captured);
    - 2019: S$1,100 or S$1,200 (S$1,300 came on 30 June 2019, after 1
      June);
    - 2022: S$1,400.

    Every pre-period June (2009-2014): none, or a threshold no capture
    shows. Both readings are stated (rule in section 3). Under every reading
    the threshold rose inside the post-period, from S$1,000 in June 2017 to
    S$1,400 in June 2022, and no document in `raw/` shows it ever falling. A
    floor lifting the comparison bottom in the post-period narrows the gap
    T2 measures, whichever reading holds.
  - All of these push toward FAIL. So a pass is strong evidence that the ladder
    lifted pay where it applied, and a fail is weak evidence that it did not.
- **Confidence at seal: `[JACOB]`.** Researcher's proposal:
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
  jobs, looser than a ladder, in firms that held foreign worker quota.
  - On the 1 June rule, the end window's Junes carried S$1,000 (2017) and
    S$1,100 or S$1,200 (2018 and 2019); both readings are stated (rule in
    section 3).
  - The start window's Junes (2010-2012): none, or a threshold no capture
    shows. The start date is not found, and no further search is made.
  - Under every reading the floor first appeared or rose between the two
    windows (none shows it falling), so the lean below holds either way.
  - A floor that rose, or first appeared, between the two windows is exactly
    what helps the uncovered bottom keep pace. So "kept pace" is weak
    evidence that jobs without a ladder did not need one. "Fell behind" is
    strong evidence that they did, since it happened despite that floor.
  - Each dated LQS step is marked on the chart.
- **Confidence at seal: `[JACOB]`.** Researcher's proposal:
  60%. A tight labour market, higher foreign worker
  levies and dollar-amount wage guidelines lifted low pay broadly in these
  years, and background knowledge (disclosed) recalls MOM reporting the 20th
  percentile growing faster than the median late in the decade. But
  occupation-level percentiles for retail and food service jobs can lag
  through part-time mix and churn.

### T4. Did the jobs survive the fitting? (competitive or monopsony)

- **Series, fixed now (section 4):** a count of workers by industry if one
  qualifies; otherwise LFS employed residents by detailed occupation;
  otherwise T4 is not scored. When both qualify, the LFS series is a
  sensitivity, reported, not scored.
- **Minimum years, fixed now (T1's minimum).** An industry needs at least 4
  pre-period years in the chosen series to be scored; the pre-period starts
  at the series' first year (section 5). An industry below the minimum is
  computed the same way and printed beside T4, labelled as outside the score
  and outside the verdict. If that admits cleaning, cleaning is scored.
- **Estimate.** For each scored industry (section 4 lines, or its titles in
  the LFS series): mean log workers over its post-period years minus mean
  over its pre-period years, minus the same difference for the comparison
  set combined. Reported with a 90 per cent interval.
- **Employment pre-trend condition, fixed now.** The same drift check as T1,
  on the log-workers gap over pre-period years, with a line of 2.0 log points
  a year. Head counts move more than percentiles, hence the wider line
  (judgement). An industry that fails it is dropped from T4 and reported. If
  every admitted industry fails, T4 is not scored.
- **Prediction.** Employment in the covered industries held up: relative
  change **greater than -5 log points** in every scored industry.
- **Survive if:** every scored industry > -0.05.
- **Fail if:** any scored industry <= -0.10: jobs fell where the floor bound,
  the competitive signature.
- **Between:** inconclusive.
- **Leans toward SURVIVE, stated now.**
  - Buildings must be cleaned, guarded and their grounds kept, by law and in
    practice; much of the demand comes from the government and large
    landlords. Demand that is hard to cut keeps jobs even under a
    competitive market.
  - **If the main series is a count of workers by industry:** it includes
    foreign workers, whom the ladders did not cover. A firm that replaced
    residents with foreign workers under its quota shows no fall here. Both
    leans then point toward "jobs held", and **the substitution cannot be
    checked** from that series: no public series splits employment by
    industry and residence (W2c does not exist). The article says so beside
    the result, and the LFS sensitivity, if it qualifies, is shown beside it.
  - **If the main series is LFS employed residents:** it counts only the
    residents the ladders covered, so the foreign-worker lean falls away and
    only the demand lean remains. Survey noise at detailed occupation is
    added, stated in section 4.
- **One lean the other way:** security. Its industry transformation plan
  pushed technology in place of guards in the late 2010s, which could shrink
  guard numbers for reasons unrelated to pay. Named, not separated.
- **Confidence at seal: `[JACOB]`.** Researcher's proposal:
  60%. Hard-to-cut demand and foreign workers in
  the count both favour holding, but security's technology push could
  produce a relative fall of 5 log points in one scored industry. Proposed
  before the series was known; a resident-only series would weaken the
  second reason.

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

  The W3 schedules are tabulated below from the primaries in `raw/`, since
  they are the policy, not the outcome.
- **Prediction.** The ratio is at least 0.97 in every post-period June for
  every scored group.
- **Survive if:** every ratio >= 0.97.
- **Fail if:** any ratio < 0.97.
- **Why 0.97 (judgement).** Allows for rounding in published percentiles and
  a schedule step falling close to the survey month.
- **Leans toward FAIL for every group, stated now:** in-house cleaners,
  in-house guards and in-house landscape workers were not bound until 1
  September 2022. They sit inside each group's occupation titles, and can
  pull its 25th percentile below the rung. For landscape, workers in firms
  not on the Landscape Company Register were unbound too: in June 2019 by
  the captures, and in June 2017, 2018 and 2022 under reading (a) at T2;
  under reading (b), only non-listed firms without work passes. The lean
  holds under both readings. A fail here says the floor was not the bottom
  of the occupation, which is itself the tailor's point.
- **Entry rungs and the LQS in force on 1 June, fixed from the primary
  documents in `raw/` before the seal (policy, not outcome).**

  | June | Cleaning, lowest rung (basic) | Security officer (basic) | Landscape worker (basic) | LQS (1 June rule) |
  |---|---|---|---|---|
  | 2016 | S$1,000 [a] | transition June; not yet bound (1 Sep 2016) | transition June; S$1,300 [e] | none or S$1,000 [h] |
  | 2017 | S$1,000 [a][b] | S$1,100 [c] | S$1,300 [e] | S$1,000 [h] |
  | 2018 | S$1,000 [b] | S$1,100 [c] | S$1,300 [e][f] | S$1,100 or S$1,200 [h] |
  | 2019 | S$1,120 [b] | S$1,175 [d] | S$1,300 [e][f] | S$1,100 or S$1,200 [h] |
  | 2020 (excluded) | S$1,200 [b] | S$1,250 [d] | S$1,300 [f] | S$1,300 [h] |
  | 2021 (excluded) | S$1,236 [g] | S$1,400 [d] | S$1,450 [f] | S$1,400 [h] |
  | 2022 | S$1,274 [g] | S$1,442 [d] | S$1,550 [f] | S$1,400 [h] |

  [a] `w3_cleaning_tcc_report_2012.pdf`: "a starting basic wage level of at
  least $1,000 for cleaning jobs such as in offices and F&B establishments"
  (conservancy: "at least $1,200"), bound through NEA licensing for all
  resident cleaners of licensed firms by 1 September 2015.

  [b] `w3_cleaning_tcc_2016.pdf`, Annex C (General/Indoor Cleaners and F&B
  General Cleaners, basic monthly wage):
  - Diagram 1: >= S$1,060, "applicable to only new contracts that take
    effect from 1st July 2017 to 30th June 2018";
  - Diagram 2: >= S$1,120, "applicable to all contracts from 1st July 2018
    to 30th June 2019";
  - Diagram 3: >= S$1,200, all contracts from 1 July 2019 to 30 June 2020.

  `w3_cleaning_mom_pr_2016.pdf` (MOM, 12 December 2016): the Commissioner
  for Labour enforces the schedules for new contracts from 1 July 2017;
  existing contracts have until 1 July 2018. So on 1 June 2018 the level
  binding on every licensed firm was S$1,000 (existing contracts), with new
  contracts on S$1,060. On 1 June 2019 every contract was on S$1,120.

  [c] `w3_security_spf_brochure.pdf` ("Security Officer (SO) >=$1,100") and
  `w3_security_stc_2017.pdf` Annex C ("Current $1,100"); SPF licensing
  conditions (`w3_security_spf_licensing_conditions_2018.pdf`) point to the
  2014 schedule until 31 December 2018.

  [d] `w3_security_stc_2017.pdf`, Annex C, "Progressive Wage Model for
  Security Industry with effect from 1 January 2019": SO S$1,175 (2019),
  S$1,250 (2020), S$1,400 (2021), S$1,442 (2022). Table 1 of the same report
  dates the 2019-2021 steps January. The November 2021 release
  (`w3_security_mom_pr_2021.pdf`) sets the schedule for 2023-2028 and does
  not revise 2022. Its "about $2,259 in 2022" is gross pay, "Basic Wage +
  overtime Pay only (assuming 72 overtime hours a month at 1.5x basic
  rate)"; that is S$1,442 basic on the standard hourly rate (S$1,442 x
  (1 + 72 x 1.5 x 12 / (52 x 44)) = S$2,259). **Rule, fixed now:** the 2022
  step is read as in force on 1 June 2022, like the January steps before it.
  If it came after 1 June, the rung that June was S$1,400 and security's
  2022 ratio is understated by 3 per cent: a lean toward FAIL, stated.

  [e] `w3_landscape_tcl_report.pdf` (TCL, 2015): the "entry-level monthly
  basic wage for a landscape worker is $1,300". The requirement applied from
  June 2016 to LCR-listed firms (`w3_landscape_nparks_cuge_news.pdf`,
  NParks, 24 April 2015). The day in June 2016 is not found and needs no
  rule: June 2016 is a transition June for landscape.

  [f] `w3_landscape_tcl_2018.pdf` (TCL, 30 November 2018), Annex C,
  "Progressive Wage Model for Landscape Maintenance Sub-Sector (2020 -
  2022)": Landscape Worker "Current" >= S$1,300, July 2020 >= S$1,450, July
  2021 >= S$1,550, July 2022 >= S$1,650; para 4.8, the adjustments "take
  effect from 1 July". So on 1 June the rung was S$1,300 to 2020, S$1,450
  in 2021 and S$1,550 in 2022. `w3_landscape_tcl_2021.pdf` confirms S$1,650
  from 1 July 2022. It bound LCR-listed firms (T2, "Who the landscape ladder
  bound").

  [g] `w3_cleaning_col_order_2021.pdf`, para 1.1, "PWM Schedule from 1 July
  2021 to 30 June 2022": General/Indoor Cleaners (office and commercial) and
  General Cleaners (F&B) >= S$1,274, basic monthly wage.
  `w3_cleaning_col_order_2019.pdf` is the Commissioner for Labour's order
  of 3 July 2019 (in operation that day). It sets the schedules for 1 July
  2020 to 30 June 2021 (General/Indoor >= S$1,236, the rung on 1 June 2021,
  an excluded June), 1 July 2021 to 30 June 2022 and 1 July 2022 to 30 June
  2023, and the PWM Bonus from 1 January 2020. Its only scored June is
  2022, where it agrees with the 2021 order (S$1,274); it changes no scored
  rung.

  [h] `w3b_lqs_faq_2016` to `w3b_lqs_faq_2021` (MOM's quota-counting FAQ,
  archived):
  - S$1,000 in force on 15 November 2016 and 9 March 2017;
  - S$1,100 on the page updated 17 July 2017;
  - no capture between January 2018 and July 2019;
  - S$1,300 on the page updated 30 June 2019;
  - S$1,400 on the page updated 1 July 2020, still so in the 2021 capture.

  `w3b_lqs_budget2024_factsheet.pdf` raises it "from $1,400 to $1,600" in
  2024, so S$1,400 held on 1 June 2022. Where two amounts are shown, or
  "none", both readings are stated (rule in section 3).

- **Where the LQS sits against the rung** (the LQS is a "monthly salary"
  threshold; basic or gross is not settled, rule in section 3):
  - cleaning: above the rung in June 2022 (S$1,400 against S$1,274) and in
    June 2018 (S$1,100 or S$1,200 against S$1,000), under both readings;
    level with it in June 2017; in June 2019 below it (S$1,100) or above it
    (S$1,200) against S$1,120; in June 2016 level with it or absent;
  - security: below the rung in 2017 and 2022; in June 2018 level (S$1,100)
    or above (S$1,200); in June 2019 below (S$1,100) or above (S$1,200)
    against S$1,175;
  - landscape: below the rung in every post-period June, under every
    reading.

  In a June where the LQS sat above a rung, firms with foreign worker quota
  had a reason to pay above the rung anyway. That lifts the 25th percentile
  and leans T5 toward SURVIVE for reasons other than the ladder: most for
  cleaning in 2018 and 2022. If the LQS counted gross pay, it pushed basic
  pay less, so the lean is weaker; its direction is the same under every
  reading, and it is never toward FAIL.
- **Rule for the rung, fixed now:** the rung is the lowest amount binding on
  every covered employer on 1 June. For cleaning in June 2018 that is the
  existing-contract level.
- **T5 reads the same series as T2.**
  - Main: only the successors on the sector's lowest rung, after a grade
    split (section 4): security 54144 against the Security Officer rung;
    cleaning 91131 and 91151 in 2022 (91130, 91151 and 91190 in 2016-2019)
    against the lowest cleaning rung.
  - Sensitivity, reported, not scored: all successors averaged, against the
    same lowest rung. A higher-grade title in the average would clear the
    entry rung by construction, which is why it is not the main series.
- **A separate bet from T2** (checker review of `cb9fe70`, item 3). T2 is
  relative: covered against comparison jobs. T5 is a level: covered jobs
  against their own rung. Either can hold without the other, so T5 stays
  scored.
- **Confidence at seal: `[JACOB]`.** Researcher's proposal:
  45%. The in-house mix in all three groups (and non-LCR firms in landscape)
  and any year where a scheduled step landed just before the June survey
  make "every group, every year" fragile.

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
  T4, gated by T1. T4's "every scored industry" means the industries its
  4-year minimum admits (section 5); any industry it does not admit is
  described beside the verdict and does not enter it.
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

- demand for cleaning, guarding and grounds upkeep is hard to cut;
- if T4 reads a count of workers by industry, the job counts include
  foreign workers whom the ladders did not cover.

Both keep jobs looking steady whether or not the floor cost resident jobs.
If T4 reads LFS employed residents instead, only the first reason holds;
the sentence is carried unchanged, and the article says which series T4
read.

**Two further leans, stated beside the verdict in the article:**

- **The pay test leans the other way (T2).** In-house workers, unbound until
  2022 in all three groups, dilute the covered side, and the LQS floor lifted
  the comparison side. So a pay gain found is strong evidence, and none found
  is weak.
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
  when no series qualifies, or every admitted industry fails its pre-trend
  condition) drops out of both the
  count and the Brier score, and the article says so. T4 is scored on the
  industries its 4-year minimum admits, or not at all if no series
  qualifies (section 4).

Expected number holding: from Jacob's confidences, written in at the seal.
Under the researcher's proposals it would be 2.55 of 5 (0.40 + 0.50 + 0.60 +
0.60 + 0.45). The predictions are correlated (T1 gates T2 and
T5; T2 and T5 read the same wages), so the actual count spreads wider than
five independent calls would.

## 9. What would prove the framing wrong, and what it leaves out

- **OWS coverage.** Settled: spreadsheets for every June 2009-2025, so every
  group has its pre-period (section 5).
- **Occupation codes.** A line that cannot be bridged across a
  classification break ends there, which can thin a group. The breaks and
  where they fall (`office/OCCUPATION_MAP.csv`):
  - **June 2010, SSOC 2005 to SSOC 2010.** Pre-period, all groups. The 2010
    header carries no version; the codes show it.
  - **June 2011, five-digit lines replaced by four-digit aggregates**
    (cleaning, landscape, cashier). Pre-period, all groups.
  - **June 2015, SSOC 2010 to SSOC 2015.** Cleaning's 9113 splits into six
    titles. Transition June for every group; security, landscape and every
    comparison title keep their text.
  - **June 2018 and June 2019.** The industrial-establishment cleaner (2018)
    and the open-area cleaner (2019) are missing from the table. Post-period;
    by the missing-year rule they leave the cleaning group.
  - **June 2020, SSOC 2015 to SSOC 2020.** An excluded June, but inside the
    post-period window, between 2019 and 2022. Security splits into officer
    and senior officer, landscape's title text changes, cleaning regroups.
    Every comparison title keeps its code and text.
  - **June 2023, June 2025.** Titles change again, and SSOC 2024 arrives in
    June 2025. Both fall after the window.

  Links across the 2010, 2011, 2015 and 2020 splits and merges are settled
  from the SSOC correspondence tables and the SSOC 2010 hierarchy in `raw/`
  (section 4; T1 lists the composition changes). SSOC 2015 (v2018) changes
  none of the lines used, apart from folding 41102 into 41101 inside the
  clerk aggregate (`w1d_ssoc2015v2018_correspondence.xls`).
- **OWS method change.** From June 2024 the method note adds "Survey results
  are also supplemented with data from Administrative Records". That is after
  the scored window; 2024 and 2025 are shown with the change marked. No
  earlier method note (2008-2023) states a change in coverage or measure.
- **Contract versus in-house.** Settled: the occupation-within-industry
  tables do not isolate cleaning firms. The industry is "Business Services"
  to June 2020 and "Administrative and Support Services" from June 2021, a
  break inside the post-period window. So the all-industries table is the
  series, and the in-house dilution stands as stated in T2 and T5.
- **Workfare.** Singapore's other tool for low pay tops up income through
  the state rather than the employer. It is not in wages and not measured
  here. The article names it, because "which lifts lowest pay" in Singapore
  has three answers, not two.
- **The LQS start date.** Not found in the archived MOM FAQs (first
  capture 15 November 2016), and no further search is made. Both readings
  are stated (rule in section 3). If the threshold began inside a
  pre-period (2009-2014), the comparison side had a floor change inside the
  window T1 reads, which raises the comparison bottom and moves the gap
  down: a lean toward FAIL at T1. If it began before 2009 or after 2014, T1
  is untouched. So the lean is toward FAIL or nothing, never toward
  SURVIVE. It does not move any window.
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

Settled before the seal from the downloads (27 September 2026, checker
review of `4a4cdae`):

- OWS coverage: June 2009-2025 (section 5);
- 2009-2011 carry the measure (section 5);
- the title listing and the occupation map (section 4, section 9);
- the rung and LQS tables (T5);
- CPI tables: M213801 and M213911 (section 4);
- W2c does not exist (T4).

Settled before the seal in the checker review of `41921ee`/`77dd3f3`
(27 September 2026, last pre-seal step):

- every occupation link, from the SSOC tables in `raw/` (section 4); the
  map's `series` column holds only main, sensitivity or excluded, with the
  reason in `series_note`;
- the final groups (section 4): 91190 in cleaning's main series; 91140
  dropped by the missing-year rule as written; 91170 excluded by the
  workplace-split rule; 91160 a sensitivity, with its T2 lean;
- every rung, from the primaries (T5): cleaning June 2018 and 2019, security
  June 2022, landscape June 2021 and 2022; the 2019 cleaning order labelled;
- the LCR for June 2019-2021, from the captures (T2).

Covered by a rule fixed now, not by a further search:

1. **The LCR in June 2016-2018 and June 2022** (never archived; no capture
   in `raw/`): both readings stated at T2 and T5; the dilution lean holds
   under either.
2. **The LQS**: its start date, its amount on 1 June 2018 and 2019, and
   whether it counted basic or gross pay. It enters no computation; both
   readings are stated and every lean holds under both (section 3, T1, T2,
   T3, T5).
3. **The month of security's 2022 step**: read as in force on 1 June 2022,
   with the lean toward FAIL stated if it came later (T5, note [d]).
4. **Days not found**: the landscape day in June 2016 (a transition June;
   T5, note [e]); the October 2014 security report itself (only the month
   is used, section 5); the lift ladder's day in 2022 (T6, not scored).
5. **Anything the SSOC tables cannot settle** is excluded from the main
   series and listed (section 4). Nothing fell under it.
6. **The W2a industry lines** are named now, from the label listing, under
   the smallest-line rule (section 4).
7. **T4's series, years and fallback** (checker's decision on `d292fe9`):
   the priority order, the pre-period from the chosen series' first year
   with the 4-year minimum per industry, and "not scored" if no series
   qualifies (section 4, section 5, T4).

**Open before the seal: which T4 series qualifies.** The label listing
(checker review of `fdb1bf5`) showed that both W2a files carry
establishments, operating revenue, operating expenditure, gross operating
surplus and value added by industry, and no count of workers; W2d has only 13
broad sectors. Decision (checker, with Jacob): the design chat searches for a
count of workers by industry and for LFS employed residents by detailed
occupation. The rules for whatever arrives are fixed now (section 4, section
5, T4). When the search ends, each candidate's labels and coverage are
listed, with no value opened, and the rules name the series, or mark T4 not
scored. No rule changes after a file arrives.

Also open at the seal: the five confidences (`[JACOB]`), which Jacob sets,
through the checker.
