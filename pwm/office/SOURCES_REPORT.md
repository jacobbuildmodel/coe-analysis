# SOURCES REPORT -- pwm piece

Researcher: `pwm` (Claude Code session), 27 September 2026, branch `pwm-wip`.
Scope of this task: sources only. No analysis, no charts, no data values
opened. The exact URLs and target filenames are in `pwm/raw/RETRIEVED.txt`.

## 0. The one-paragraph version

Nothing was downloaded. The sandbox proxy refuses every government and
publisher host tried (HTTP 403 at CONNECT, a policy denial). This includes
data.gov.sg, stats.mom.gov.sg, mom.gov.sg, SingStat, SSO, NEA, SPF, BCA, gov.uk
and the Hong Kong Minimum Wage Commission. Every source below was **located
through a web search index, not opened**. What exists:

- **W1, occupational wages.** MOM's Occupational Wage Survey (OWS) publishes
  a table for each June. It gives the 25th percentile, median and 75th
  percentile of basic and gross monthly wages by occupation, for full-time
  residents in private firms with 25 or more employees. The per-year tables
  are confirmed from 2011. Earlier years are probable but unconfirmed, and
  this matters (section 4).
- **W2, employment.** The best series is SingStat's count of workers by
  detailed services industry. It includes foreign workers, whom the wage
  ladders do not cover. Resident employment by detailed occupation is not
  confirmed to exist in public form.
- **W3, PWM dates.** Start dates are pinned to primary pages for cleaning,
  security, retail, food services, and administrators and drivers. Landscape
  and lift have the month or year but not the day. Wage levels sit in
  Commissioner for Labour orders and tripartite cluster reports, located but
  unread.
- **W4, CPI.** Located, including a CPI for the lowest-income 20 per cent of
  households.
- **W5, evidence elsewhere.** Located for Hong Kong, the UK and Germany.

The design survives on sources: three early-covered jobs (cleaners, security
officers, landscape workers) can be set against low-wage jobs that were covered
only from September 2022 (retail, food services, office and driving jobs).
**Two gaps are not closed.** First, how far back the per-year wage tables go.
Second, any resident head count for cleaners, guards and gardeners, as opposed
to industry head counts that include foreign workers. A third is partly
closed: the Local Qualifying Salary, which put a floor under the comparison
jobs before 2022. Its amounts are known from secondary sources, but not its
primary dates (section 2, W3).

## 1. Exposure disclosure (read first)

The seal is only worth something if it is clear what had been seen.

1. **No W1 value was seen.** No occupational wage, percentile or median for
   any occupation or year appeared in any search summary read.
2. **Employment counts seen in search summaries (W2-type, single dates, not
   series).**
   - A secondary release (e2i/NTUC) quoted: by 1 September 2014, 1,001
     licensed cleaning businesses employing 52,000 cleaners, 38,000 of them
     residents, and over 26,000 resident cleaners paid PWM wages.
   - MOM's lower-wage workgroup material quoted how many workers the 2022-2023
     wave would cover: about 28,000 full-time lower-wage workers (10 per cent)
     in the new sectoral ladders and 55,000 (19 per cent) under the
     occupational ones, and up to 234,000 (94 per cent) of full-time
     lower-wage workers covered once all were in place.
   - A 2021 MOM release title: "Up to 3,000 local workers" for waste
     management.

   None of these is a year-by-year series. The two cleaning figures are one
   point in the transition period, which THESIS does not score. They
   establish only that residents were a clear majority of cleaners in 2014,
   and that the second wave covered almost every full-time lower-wage worker
   left, which is why THESIS ends the comparison before it.
3. **W4 values seen.** One summary quoted CPI-All Items inflation by household
   income group for 2023 (lowest 20% 4.3, middle 60% 4.7, highest 20% 5.1 per
   cent) and 2025 (0.6, 0.9, 1.2 per cent). CPI cancels out of every scored
   comparison in THESIS (section 6), because covered and comparison jobs are
   deflated by the same index. It enters only the descriptive real-pay level.
4. **W3 values seen (policy settings, not outcomes).**
   - The retail PWM baseline gross wage for a full-time retail assistant was
     $1,850 from September 2022.
   - PWCS co-funding rates and thresholds.
   - Firms holding 95 per cent of the lift maintenance market committed to
     the lift PWM in 2019.
   - The Hong Kong starting minimum wage was HK$28 an hour.

   These are the rules being tested, not their results.
5. **W5 findings seen (context, not Singapore data).**
   - Germany 2015: wages rose, employment did not fall, and workers moved to
     larger, better-paying firms.
   - UK 2016: large wage gains at the bottom, and a small employment effect
     not statistically different from zero.
   - Hong Kong 2011: mixed findings, including job losses for workers with
     disabilities.

   None of these enters a test.
6. **Background knowledge, stated so its influence can be judged.**
   - I know the public outline of the PWM story. NTUC launched the ladder
     in 2012; cleaning, security and landscape became mandatory in the
     mid-2010s; the ladder spread widely in 2022-2023.
   - I also recall, without year-by-year figures, the claim MOM has repeated
     that wages of workers in PWM sectors rose faster than the median in the
     years after coverage.
   - I also recall MOM's Labour Force reports saying that real income at the
     20th percentile of full-time employed residents grew faster than the
     median in the late 2010s.

   Both recollections are aggregate claims, not occupation series. They
   informed two proposed confidences, and THESIS says where.
7. **Checker disclosure (added 27 September 2026, checker review of
   `cb9fe70`).** The checker read a Wikipedia summary stating two things:
   - before PWM, the median wage of cleaners in the civil service was between
     S$675 and S$950;
   - the cleaning ladder's entry basic wage was S$1,000 to S$1,200.

   No OWS table, no LFS income by occupation and no MOM statement on PWM
   wage growth was read. The civil service figure is not OWS data: OWS
   covers private-sector establishments only, so public-sector cleaners are
   outside every series THESIS uses. The entry rung is a policy setting (W3),
   the same kind of number T5 compares against, not an outcome.
8. **LQS amounts seen while locating item 2 of the checker review
   (27 September 2026).** Secondary pages (Fragomen, dollarsandsense.sg) and
   the MOM search snippets gave the history of the salary a local worker
   needs to count toward a firm's foreign worker quota:
   - S$1,000 before July 2017, S$1,100 from July 2017, S$1,200 from July 2018;
   - S$1,400 from 2020 ("raised four times since 2017", MOM LQS page snippet);
   - S$1,600 from 1 July 2024, S$1,800 from 1 July 2026.

   The checker's secondary source gives S$1,300 for 2019. A snippet of an
   MOM wage-practices report showed its own "lower-wage" cut-offs of $1,200
   (2017), $1,300 (2018) and $1,400 (2019 and 2020). These are policy and
   report definitions, not outcomes.
9. **Checker disclosure (27 September 2026): policy pages read, no outcome
   values seen.**
   - **MHA, 12 November 2021:** security wage schedule 2023-2028. Entry gross
     wage about S$2,259 in 2022, rising to S$3,530 in 2028.
   - **Security Tripartite Cluster report, 23 November 2017:**
     - the PWM became a licensing condition for security agencies from
       1 September 2016;
     - security officer basic wage S$1,100;
     - increases of +S$75 in January 2019, +S$75 in January 2020 and +S$150
       in January 2021;
     - at least 3 per cent a year in 2022-2024.
   - **MOM press release, 30 November 2018:** landscape entry basic wage
     +S$150 in July 2020, +S$100 in July 2021 and +S$100 in July 2022; at
     least 3 per cent a year in 2023-2025.
   - **NTUC, 12 December 2016:**
     - cleaning basic wage +S$60 in July 2017, +S$60 in July 2018 and +S$80
       in July 2019, then 3 per cent a year in 2020-2022;
     - new contracts from 1 July 2017, existing contracts by 1 July 2018;
     - enforced through NEA licensing by order of the Commissioner for
       Labour.

     The page carries outcome statistics; they were filtered out and not
     read.
   - **NParks CUGE LCR page:** the PWM has been a condition of LCR listing
     since 2016, and LCR listing is needed to bid for NParks and government
     contracts.
   - **2015 news repost:** the landscape PWM was required for listing and
     renewal on the LCR from June 2016, with a starting basic wage of "at
     least $1,300".
   - **PWCS** (secondary): co-funds wage increases in 2022-2026; first payout
     in Q1 2023.

   **Context note to Jacob before he set his confidences.** The checker sent
   Jacob a note containing:
   - the policy settings above;
   - the rules of each test;
   - published minimum-wage employment studies (Cengiz et al. 2019,
     Dustmann et al. 2022, Dube 2019, Neumark and Shirley 2022);
   - the site's scorecard record;
   - arithmetic only (noise-only pass rates for T1, compound probabilities).

   No confidence number was proposed to him. The researcher's proposals
   (THESIS, beside each test) were not in the note.

   All of these are leads for the W3 wage-schedule table (THESIS section 10,
   item 3). Every amount and date is confirmed from primary documents in the
   design chat's downloads before it enters T5.
10. **Researcher exposure while building the title listing, the occupation
    map and the W3 rung table (27 September 2026, after the downloads).** No
    wage or head-count value from W1 or W2 was opened. What was read:
    - **OWS spreadsheets.** Titles, SSOC codes, column headers and table
      titles only, through `01_titles.py`. That script never reads a wage or
      "Number Covered" column. To learn the layout, header cells were first
      printed with every digit masked.
    - **OWS method notes, 2008-2025.** Coverage sentences only. These carry
      survey metadata, not outcomes: the number of establishments and
      employees in each year's sample (for example, 3,225 establishments and
      some 221,400 CPF contributors in June 2009).
    - **W3 policy documents.** Sentences carrying dollar amounts were
      extracted with a filter that dropped any sentence naming a median,
      growth, earnings or a survey. Schedule tables printed as images were
      viewed (cleaning order 2021, landscape 2015 and 2021). The filter let
      through these outcome-type statements, disclosed here:
      - STC 2017: "The wages of resident security officers have increased
        since the introduction of the PWM in October 2014" (no figure).
      - TCL 2021, footnote: "The monthly gross wages of resident landscape
        maintenance employees are marginally higher than their PWM Baseline
        Wages, as they typically work few overtime hours" (no figure). This
        bears on T5 and on the gross-versus-basic choice; it is stated here
        so its influence can be judged.
      - TCL 2015: "In 2014, there were only about 3,000 local landscape
        maintenance workers, out of a total workforce of 6,900", and 270 LCR
        companies (about 90 per cent) at end 2014. TCL 2021: 358 LCR
        companies employing more than 3,000 resident landscape maintenance
        employees on 1 January 2021. NParks, April 2015: an estimated 3,000
        resident workers would benefit. These are single-date head counts,
        not series.
      - TCL 2021 and TWG-LWW material state a policy aim that wage growth in
        PWM sectors "outpace median wage growth". That is an aim, not a
        result.
      - MSE speech: the waste collection crew's baseline wage schedule
        (S$2,210 in 2023 to S$3,260 in 2028), a policy setting.
11. **Researcher exposure in the last pre-seal step (27 September 2026,
    checker review of `41921ee`/`77dd3f3`).** No wage or head-count value
    from W1 or W2 was opened. What was read:
    - **SSOC tables** (`w1d_*`): codes and titles of the correspondence
      tables and the SSOC 2010 hierarchy. Classification only.
    - **W3 primaries**, for dates and rung amounts: the cleaning cluster's
      2016 report (the Annex C schedule images were viewed) and MOM's
      release of 12 December 2016; the Commissioner for Labour's 2019 order
      (schedule image viewed); the landscape cluster's 2018 report (Annex C
      text); the security release of November 2021 (its 2022 gross figure
      is disclosed in item 9); the LCR pages and FAQs captured in 2019-2021;
      the LQS FAQs, for whether the threshold counted basic or gross pay
      (they say only "monthly salary").
    - The same sentence filter as item 10 was used. It let through no
      outcome figure beyond those already disclosed in items 9 and 10.
12. **Researcher exposure in the checker review of `fdb1bf5`.** The
    `DataSeries` column of both W2a files was listed by `01b_w2a_labels.py`
    (industry and indicator labels, text only, `office/w2a_labels.txt`). No
    year column was read and no value was seen.
13. **Checker disclosure (27-28 September 2026): a second context note to
    Jacob, sent before he set his confidences.** It contained:
    - the final test rules;
    - the final rung and LQS tables;
    - the title-change arithmetic: the drift a one-off jump J adds to T1's
      slope, 0.30J or 0.40J over 4 Junes and 0.14J or 0.23J over 6 Junes;
    - the site's scorecard record;
    - compound-probability arithmetic.

    No confidence number was proposed to him.


## 2. Item by item

### W1 -- occupational wages, by occupation and industry, annual (June)

**What exists.** MOM's Occupational Wage Survey:

- Reference month June, run by MRSD and "supplemented with data from
  Administrative Records".
- Private-sector establishments with at least 25 employees.
- Full-time resident employees only.
- Monthly basic and gross wages, excluding bonuses, with the 25th percentile,
  median and 75th percentile per occupation.

The survey covers "over 300" occupations in older editions and "over 500" in
recent ones, according to the index. The 2024 sample was described as more
than 4,000 organisations and more than 200,000 employees.

**Where.**

- stats.mom.gov.sg keeps a page of tables for each year. Pages for 2025, 2024,
  2016 and 2012 were found, and 2011 as Part III of *Report on Wages in
  Singapore 2011*.
- data.gov.sg holds single-year copies for June 2024, and one dataset,
  "Occupational Wages by Industry", whose year span the index did not show.
- An old-portal slug suggests a multi-year "selected occupations within major
  occupational groups by industry" dataset.

**Coverage.** Confirmed by the index: 2011, 2012, 2016, 2024, 2025. The years
in between are very likely published, since the page naming is regular.
Before 2011, the *Report on Wages in Singapore* series probably carried the
OWS tables, but no pre-2011 edition was seen. UNVERIFIED.

**Why it fits the question.**

- The 25th percentile of an occupation's wage is a direct reading of "pay at
  the bottom of covered jobs".
- The resident-only scope matches the PWM, which binds only for Singapore
  citizens and permanent residents.
- Basic wage is what the cleaning, security and landscape ladders set. Gross
  wage is what the worker takes home before CPF.

**Known limits.**

1. **Firms with fewer than 25 employees are left out.** Small cleaning
   contractors, security agencies and food outlets are not in the survey.
2. **Occupation codes changed** (SSOC 2005, 2010, 2015, 2020, 2024). Titles
   are matched by name across editions and any title without a clean match
   is dropped. The matching is done from the title lists alone, before the
   seal (THESIS section 4).
3. **"Supplemented with administrative records"** may mark a method change in
   some year. Settled from the method notes, 2008-2025 (coverage sentences
   only; THESIS section 9): the phrase first appears in June 2024, after the
   scored window. No earlier note states a change in coverage or measure.
4. **The occupation does not say who the employer is.** A cleaner employed by
   a cleaning contractor was covered from 2014-2015. A cleaner employed
   directly by a hotel or hospital (in-house) was covered only from 1
   September 2022. If the OWS table of occupation within industry gives
   detail below the major occupational group, contract cleaners can be
   separated out. If not, the cleaner series mixes covered and uncovered
   workers, which pulls any measured effect toward zero.

**The middle, for T3.** The LFS median gross monthly income from work of
full-time employed residents is on data.gov.sg as an annual series
(W1c). It is used only if the OWS tables carry no all-occupations median.

### W2 -- employment by occupation or industry

**What exists, best first.**

- **W2a. SingStat, "Key Indicators by Detailed Industry in All Services
  Industries"** (table M601481; data.gov.sg `d_38d62de582eb7ee2c58d1bba4cd4132d`).
  - Annual. Expected, when located, to carry the number of workers by
    detailed SSIC industry. **Corrected after the downloads (checker review
    of `fdb1bf5`):** the label listing (`office/w2a_labels.txt`) shows that
    the saved table, and its group-level companion, carry establishments,
    operating revenue, operating expenditure, gross operating surplus and
    value added, and no count of workers. T4 has no series in `raw/`
    (THESIS section 10).
  - Recently moved from SSIC 2020 to SSIC 2025, per the index.
  - Excludes own-account workers.
  - Expected to break out cleaning activities, private security activities and
    landscape care and maintenance at the 4- or 5-digit level. Settled by
    the listing: SSIC 812 cleaning activities, SSIC 813 landscape planting,
    care and maintenance, and SSIC 80 security and investigation activities
    (no private-security line of its own); detailed table 2010-2024.
  - **Includes foreign workers.** The ladders did not cover them, so a firm
    that replaced a resident cleaner with a foreign one leaves this count
    unchanged.
- **W2b. LFS, "Employed Residents by Occupation"** (two data.gov.sg
  datasets).
  - Residents only, June, mapped to SSOC 2024.
  - The level of occupation detail is UNVERIFIED. If it is the nine major
    groups only, it cannot isolate cleaners, guards or gardeners, and is
    context.
  - **Role in T4, fixed before any new file (checker's decision on
    `d292fe9`; THESIS section 4):** LFS employed residents by detailed
    occupation is T4's sensitivity if a count of workers by industry
    qualifies, and its main series if only the LFS qualifies. It counts
    residents only, who are the people the ladders covered, but adds survey
    noise at detailed occupation. The saved W2b files qualify only if their
    labels show the SSOC unit group or finer; that is judged from labels and
    coverage, not values.
- **W2c. Employment by industry AND residential status: does not exist.**
  The dataset ID located by search is invalid on data.gov.sg. The nearest,
  "Changes In Employment By Sector", has no residential split
  (`raw/RETRIEVED.txt`). No public series splits industry employment by
  residence, so the resident-for-foreign swap in T4 cannot be checked.
- **W2d.** Employment by sector at year-end, context only.
- **W2e. MOM Labour Force Survey, employed residents by occupation**
  (design chat `817d62a`; 15 files in `raw/`, checker verified all 270
  md5s). Searched for T4 and judged under the rules fixed before it arrived,
  from its labels and coverage only, no value opened:
  - the finest level is 2-digit SSOC (Protective Services Workers; Cleaners
    and Related Workers; Agricultural, Fishery and Related Labourers),
    2008-2022;
  - 2008, 2011 and 2014 are in PDF reports only; 2009 is in SSOC 2005, with
    no protective services row;
  - the 2-digit groups also hold police and civil defence officers, and
    domestic cleaners, whom no ladder covered.

  Coarser than the 4-digit unit group THESIS requires, so it does not
  qualify. It is used in no test, chart or statement of the result.
- **Series (i), a count of workers by services industry: does not exist.**
  SingStat M601481 carries establishments, operating revenue, operating
  expenditure, gross operating surplus and value added only; M601501 carries
  remuneration only, and only for SSIC 68-82 combined.
- **Result: T4 is not scored** (THESIS section 4, rule 3). Singapore
  publishes no yearly count of cleaners, security officers or landscape
  workers, so whether the ladders cost jobs cannot be tested from public
  data. THESIS names this as a finding (section 9).

**Not found.** A public series of resident head counts by detailed occupation
(cleaners, security guards, gardeners) per year. The OWS tables for June
2009-2023 carry a "Number Covered" column: the employees in the sample
behind each wage line. That is a sample count, not employment, and is not
used. `01_titles.py` never reads it. The 2024 and 2025 tables drop it.

### W3 -- PWM mandatory dates and wage levels, by sector

Primary sources only: MOM sector pages, Commissioner for Labour orders,
tripartite cluster reports, and the licensing agencies (NEA, SPF, NParks,
BCA). Secondary sites (payroll blogs, Wikipedia) were seen in results and not
used for any date.

| Sector | How enforced | First public step | Mandatory for residents | Primary page for the date |
|---|---|---|---|---|
| Cleaning (contract) | NEA cleaning business licence, EPHA; S 240/2014 | Tripartite Cluster for Cleaners report, 19 Oct 2012; voluntary PWM 2012 | Licensing from 1 Apr 2014; new contracts from 1 Apr or 1 Sep 2014 (sources disagree); **all resident cleaners of licensed firms by 1 Sep 2015** | MOM cleaning page; NEA licence page; S 240/2014 |
| Security (agency) | SPF/PLRD security agency licence | Security Tripartite Cluster, Oct 2014 | **1 Sep 2016**, at licence renewal | SPF PWM page; SPF brochure |
| Landscape | NParks Landscape Company Register (registration, public tenders) | NParks announcement, Apr 2015 | **June 2016** (day not found; June 2016 is a transition June, so no rule is needed: THESIS T5 note [e]), LCR-registered firms only | NParks CUGE pages; MOM landscape page |
| Lift and escalator | BCA registration, workheads RW02B/RW03B | Voluntary 2018; public tenders only to PWM firms from May 2019 | **2022** (day not found; T6 is descriptive, not scored, and shows the year) | BCA PWM page; BCA-MOM release |
| In-house cleaning, security, landscape | Work pass eligibility | TWG-LWW report, 30 Aug 2021 | **1 Sep 2022** | MOM release 30 Aug 2021 |
| Retail | Work pass eligibility | Tripartite Cluster for Retail report, 15 Aug 2022 | **1 Sep 2022** | MOM retail page |
| Food services | Work pass eligibility | Tripartite Cluster for Food Services report, 15 Feb 2023 | **1 Mar 2023** | MOM food services page |
| Waste management | NEA licence and work pass | MOM release, 26 Jan 2021 | **1 Jul 2023** (one summary said only "2023") | MOM waste management page |
| Administrators and drivers (occupational) | Work pass eligibility | TWG-LWW, 2021 | **1 Mar 2023** | MOM expansion page |

**Two facts shape the design.**

1. **"Mandatory" did not mean the same thing in each wave.** The first wave
   (cleaning, security, landscape) was enforced through business licences or
   registration, so it bound every firm in the licensed activity. From
   September 2022, retail, food services and the occupational ladders were
   enforced through work pass eligibility, so they bound only firms that
   employ foreign workers. A firm with no work pass holders was not legally
   bound. This matters only after 2022, which THESIS does not score.
2. **The Local Qualifying Salary (LQS) put a floor under the comparison jobs
   long before 2022** (checker review of `cb9fe70`, item 2).
   - It was known earlier as the full-time-equivalent salary threshold.
   - Before September 2022 it was a counting rule, not a legal floor. A local
     employee paid less than the threshold did not count, or counted only in
     part, toward the number of foreign workers the firm could hold.
   - So any firm that needed its foreign worker quota had a reason to pay
     every local at least the threshold. That includes many shops and food
     outlets in comparison set C.
   - From 1 September 2022 it became a condition for work passes: every local
     employee of a firm holding work passes had to be paid at least the LQS.

   Amounts and dates, from the archived MOM quota-counting FAQs
   (`raw/w3b_lqs_faq_*`, the design chat's downloads) where captured; THESIS
   T5 note [h] has the detail:

   | Amount | From | Source state |
   |---|---|---|
   | S$1,000 | in force by 15 November 2016; start date not found | primary (archived FAQ) |
   | S$1,100 | page updated 17 July 2017 | primary (archived FAQ) |
   | S$1,200 | not captured (between January 2018 and July 2019) | secondary only (Fragomen: July 2018) |
   | S$1,300 | page updated 30 June 2019 | primary (archived FAQ) |
   | S$1,400 | page updated 1 July 2020 | primary (archived FAQ) |
   | S$1,600 | 1 July 2024 | primary (`w3b_lqs_budget2024_factsheet.pdf`) |
   | S$1,800 | 1 July 2026 | secondary |

   **What the captures do not settle is covered by a rule fixed now** (THESIS
   section 3): the start date, the S$1,200 step date, and whether the
   threshold counted basic or gross pay. The LQS enters no computation. Both
   readings are stated, every lean holds under both, and no further search
   is made.

   The LQS applied to cleaning, security and landscape firms too. There the
   ladder's entry rung sat at or above it from the start (S$1,000 basic for
   cleaning, disclosed in section 1 item 7), so it added little. Its effect
   falls on the comparison jobs. That is the lean THESIS states at T2 and T3.

**Wage levels.**

- The ladders are set out in the Commissioner for Labour orders (cleaning),
  SPF licensing conditions and security cluster reports, the landscape
  cluster reports, and the retail and food services cluster reports, all
  listed in RETRIEVED.txt.
- Each schedule has its own effective dates, often yearly steps. They are
  tabulated by sector and rung, on the 1 June rule, from the saved PDFs at
  THESIS T5, before the seal: the ladders are the policy, not the outcome.
  Every rung is settled from a primary document.
- Only the entry rung of cleaning, security and landscape enters a test (T5).

**Government co-funding, dated for the record.**

- The Wage Credit Scheme from 2013 and the Progressive Wage Credit Scheme
  (2022-2028) co-funded wage increases for lower-paid Singaporean employees
  in covered and uncovered jobs alike.
- They lift both sides of the comparison and are named in THESIS as things
  the design does not separate.

### W4 -- CPI

- **W4a.** CPI, 2024 as base year, annual: SingStat **M213801**, 1961-2025.
  SingStat rebased to 2024; the 2019-base M212882 now returns 404, and the
  data.gov.sg ID located by search is invalid.
- **W4b.** CPI by household income group, lowest 20 per cent, 2024 base,
  annual: SingStat **M213911**, 1993-2025. M213921, located by search, is
  the middle-60-per-cent table. This is the more honest deflator for
  low-wage pay, and it is used as a sensitivity.

Both were saved as the SingStat API's JSON. T1, T2 and T3 are gaps between
groups sharing one index, so the deflator cancels in every one of them. CPI
is used only for the charts and for descriptive statements of real pay.

### W5 -- minimum wages elsewhere (context only)

- **Hong Kong, statutory minimum wage from 1 May 2011.** Minimum Wage
  Commission 2012 report; LegCo paper; one peer-reviewed study using the
  General Household Survey 2011-2019.
- **UK, National Living Wage from April 2016.** Dube (2019), review for HM
  Treasury; Giupponi, Joyce, Lindner, Waters, Wernham and Xu (IFS working
  paper 2021; *Journal of Labor Economics* 2024).
- **Germany, national minimum wage from January 2015.** Dustmann, Lindner,
  Schoenberg, Umkehrer and vom Berge (2022), *QJE* 137(1), 267-328.
- **The model.** Card and Krueger (1994), *AER* 84(4), 772-793.

These give the reader the range of outcomes elsewhere. No figure from them
enters a test, and the article says Singapore's labour market differs in
one way that matters: a large foreign workforce that a sector-specific,
resident-only floor does not touch.

## 3. Which occupations map cleanly to PWM sectors

Titles below are generic. The exact titles and codes for every June
2009-2025, every classification break and where it falls are in
`office/OCCUPATION_MAP.csv` (27 September 2026), built from the title
listing before any wage value was opened.

| PWM ladder | OWS occupation titles (generic) | Fit | Reason |
|---|---|---|---|
| Security (agency, 2016) | security guard / security officer | **Good** | Most guards work for licensed agencies, which the 2016 condition bound. In-house guards (covered 2022) are a minority (share UNVERIFIED). |
| Cleaning (contract, 2014-2015) | office/commercial cleaners, other building cleaners | **Partial** | Mixes contract cleaners (covered 2015) with in-house cleaners (covered 2022). Clean only if occupation-within-industry tables isolate cleaners in the cleaning-services industry. Otherwise the effect is diluted toward zero. |
| Landscape (LCR firms, 2016) | gardening and landscape labourers, gardeners | **Weak** | Bound only LCR-registered firms. Registration was needed for public tenders but not to trade. The title may mix nursery and horticulture workers. Scored, with the weakness stated. |
| Lift and escalator (2022; voluntary 2018) | lift/escalator mechanic or technician | **Poor** | Mid-wage, small cell, probably merged with other mechanics in some editions, and no clean start date. Described, not scored. |
| Retail (2022) | shop sales assistant, cashier | Good **as comparison** | Uncovered until 1 Sep 2022. |
| Food services (2023) | waiter, kitchen assistant, food/drink stall assistant | Good **as comparison** | Uncovered until 1 Mar 2023. Cooks left out: mostly above the low-wage band. Dishwashers left out (27 Sep 2026): the cleaning ladder names them in its F&B group (`w3_cleaning_col_order_2021.pdf`). Food service counter attendant: absent from June 2009. |
| Administrators and drivers (2023) | general office clerk; van drivers, lorry drivers | Good **as comparison** | Uncovered until 1 Mar 2023. No car-driver title is published in OWS. Conservancy and waste truck drivers are excluded: the cleaning and waste ladders cover them. |
| Waste management (2023) | refuse collectors | **Poor** | Small, and overlaps the cleaning ladder's conservancy roles. Left out. |

**Industries for W2a.**

- Covered: cleaning activities, private security activities, landscape care
  and maintenance.
- Comparison: retail trade, and food and beverage service activities.

The mapping is by activity code, which is cleaner than occupation for
cleaning, because a cleaning contractor's staff are the covered group. The
catch is that head counts include foreign workers.

## 4. What could not be closed, and what it does to the tests

Written before the downloads. The state after them is in THESIS section 10:
every item below is settled, or covered by a rule fixed there.

| Gap | Effect on THESIS tests |
|---|---|
| Nothing downloaded (403 on every host) | Every coverage figure is provisional. The design chat downloads; `00_coverage.py` writes coverage into RETRIEVED.txt before the seal. |
| **OWS earliest year unknown (2011 confirmed)** | The pre-trends test (T1) needs at least 4 June surveys before each group's first announcement: 2009-2012 for cleaning, 2011-2014 for security and landscape. If OWS starts in 2011, cleaning has only 2012 and 2011 before its October 2012 announcement, and **drops out of T1 and T2**; the design then rests on security and landscape. |
| Contract vs in-house cleaners not separated at occupation level | Cleaning's pay effect is diluted toward zero unless occupation-within-industry tables are detailed enough. THESIS scores cleaning with the dilution stated. |
| No resident head count by detailed occupation | T4 uses industry workers (W2a), which include foreign workers. A resident-for-foreign swap is invisible. This leans T4 toward "jobs held". W2c gives a broad-industry substitution check, described only. |
| W2a detail level and first year | If cleaning, security and landscape are not separate lines, T4 is run on the smallest industry that contains them and says so. If it starts after 2012, cleaning drops out of T4. |
| Landscape start day; lift start day | Landscape: June 2016 is the survey month itself, so THESIS counts June 2017 as the first post-period survey whatever the day. Lift: not scored. |
| Occupation code changes (SSOC) | Titles are matched by name before the seal, and unmatched titles dropped. A break that cannot be bridged ends that title's series. |
| OWS method change ("administrative records") | Settled: first stated in June 2024, after the scored window (THESIS section 9). |
| Security announcement document (October 2014) not located | Only the month is used (last pre-period June is 2014). |
| LQS history before 2020: primary sources not saved; start date of the S$1,000 threshold unknown | THESIS states the LQS as a lean at T2 and T3 either way. If the S$1,000 threshold began inside a pre-period, T1 reads a window with a floor change in it, and the chart marks the date. Every LQS step is marked on the charts. |

## 5. Asks of Jacob (one consolidated list)

1. **Download W1a first.** Open the stats.mom.gov.sg occupational wage pages
   by year, as far back as they go (try 2005-2010 through the "Report on
   Wages in Singapore" publications), and save the occupation table, the
   occupation-within-industry table and the method PDF for each year. Do not
   open the sheets.
2. **Download W1b-W1c, W2a-W2d and W4a-W4b** from data.gov.sg (CSV button)
   or SingStat Table Builder, and note each page's "last updated" date and
   stated coverage.
3. **Save the W3 pages and PDFs** listed in RETRIEVED.txt, especially the
   Commissioner for Labour orders and cluster reports that carry the wage
   schedules, and the SPF and NParks pages that carry the start dates.
4. **Save the LQS history (W3b)** from MOM primary pages, including the
   archived versions of MOM's quota-counting FAQ on web.archive.org, to date
   each step: S$1,000 (start), S$1,100, S$1,200, S$1,300, S$1,400.
5. **W5 PDFs**, if convenient. Not needed before the seal.
6. **Checker disclosure:** received 27 September 2026, recorded in section
   1, item 7.
7. **Review THESIS.md (unsealed)** and set the confidences.

## Sources used to locate the above (search index, 27 September 2026)

- https://data.gov.sg/datasets/d_670c3c6cecbcd24e48034a3428bd306e/view
- https://data.gov.sg/datasets/d_9917e751f7498502f70052a940a3f312/view
- https://data.gov.sg/datasets/d_ec5d0e4ebdd2baee2a5aa1322a3156a5/view
- https://data.gov.sg/datasets/d_6750b687badf6e0c7a93a7a2e2712b2a/view
- https://data.gov.sg/dataset/monthly-basic-and-gross-wages-of-selected-occupations-within-major-occupational-groups-by-industry
- https://stats.mom.gov.sg/iMAS_Tables1/Wages/Wages_2024/Coverage-and-Methodology-of-OWS-2024.pdf
- https://stats.mom.gov.sg/Pages/Occupational-Wages-Tables2025.aspx
- https://stats.mom.gov.sg/Pages/Occupational-Wages-Tables2024.aspx
- https://stats.mom.gov.sg/Pages/Occupational-Wages-Tables2016.aspx
- https://stats.mom.gov.sg/Pages/Occupational-Wages-Tables-2012.aspx
- https://stats.mom.gov.sg/Pages/Report-on-Wages-in-Singapore-2011-Part-III-Occupational-Wages-from-Occupational-Wage-Survey.aspx
- https://stats.mom.gov.sg/SL/Pages/Occupational-Wages-Source-and-Coverage.aspx
- https://data.gov.sg/datasets/d_9cd9c40f22a4e45cac8f8b9d895fd5ce/view
- https://data.gov.sg/datasets/d_3ba99a6cc9f643bacb63bdab296d7bff/view
- https://data.gov.sg/datasets/d_9392faa714d5e5809b07b10fbff2993e/view
- https://data.gov.sg/datasets/d_38d62de582eb7ee2c58d1bba4cd4132d/view
- https://tablebuilder.singstat.gov.sg/table/TS/M601481
- https://data.gov.sg/datasets/d_a99730f2ed37e5dd4dba9d6a779fdc9f/view
- https://data.gov.sg/datasets/d_dda4a6de2712669acbbf161653e96a73/view
- https://data.gov.sg/datasets/d_d2518fed6cc2014f0cd061b4570a9592/view
- https://www.mom.gov.sg/employment-practices/progressive-wage-model (and the eight sector pages)
- https://www.mom.gov.sg/-/media/mom/documents/press-releases/2012/tripartiteclusterforcleaners_report-(191012).pdf
- https://sso.agc.gov.sg/SL/EPHA1987-S240-2014
- https://www.nea.gov.sg/our-services/public-cleanliness/cleaning-industry/cleaning-business-licence
- https://www.police.gov.sg/~/media/spf/files/e-services/wda_se_dl_brochure.pdf
- https://www.police.gov.sg/E-Services/Apply-for-Security-Officer-Licence/Security-Progressive-Wage-Model-Requirements
- https://www.nparks.gov.sg/news/2015/4/implementation-of-progressive-wage-model-for-landscape-sector-to
- https://cuge.nparks.gov.sg/landscape-company-register/lcr-requirements-and-faqs/
- https://www1.bca.gov.sg/safety-and-standards/lifts-escalators-and-mechanised-car-parking-systems/progressive-wage-model-pwm/
- https://www1.bca.gov.sg/resources/newsroom/bca-mom-joint-media-release-government-accepts-recommendations-to-uplift-lift-escalator-technicians-with-sustained-wage-increases-and-annual-bonus/
- https://www.mom.gov.sg/newsroom/press-releases/2021/0830-government-accepts-twg-lww-recommendations
- https://www.mom.gov.sg/employment-practices/progressive-wage-model/local-qualifying-salary
- https://www.iras.gov.sg/schemes/disbursement-schemes/progressive-wage-credit-scheme
- https://data.gov.sg/datasets/d_dcb352661fb449c4a4c0ab23aa8d6399/view
- https://tablebuilder.singstat.gov.sg/table/TS/M212882
- https://tablebuilder.singstat.gov.sg/table/TS/M213921
- https://www.mwc.org.hk/en/downloadable_materials/2012MWCReport-Eng.pdf
- https://assets.publishing.service.gov.uk/media/5dc0312940f0b637a03ffa96/impacts_of_minimum_wages_review_of_the_international_evidence_Arindrajit_Dube_web.pdf
- https://assets.publishing.service.gov.uk/media/61b0c5a2e90e070448c520fb/IFS_WP202148-The-distributional-and-employment-impacts-of-nationwide-Minimum-Wage-changes.pdf
- https://academic.oup.com/qje/article/137/1/267/6355463
- Secondary, seen and not used for any date or figure: e2i.com.sg and
  ntuc.org.sg release on cleaning licensing (2014); staffany.com,
  hashmicro.com, wikipedia "Progressive wage", and several payroll-guide
  sites.
