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
to industry head counts that include foreign workers.

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
7. **No checker disclosure yet.** If the checker has read OWS tables or MOM
   PWM impact figures, that needs recording here before the seal. The same
   was done for the ERP piece.

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
   some year. PENDING: read the method PDF for each year.
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
  - Annual. Carries the number of workers by detailed SSIC industry.
  - Recently moved from SSIC 2020 to SSIC 2025, per the index.
  - Excludes own-account workers.
  - Expected to break out cleaning activities, private security activities and
    landscape care and maintenance at the 4- or 5-digit level. UNVERIFIED:
    detail level and first year.
  - **Includes foreign workers.** The ladders did not cover them, so a firm
    that replaced a resident cleaner with a foreign one leaves this count
    unchanged.
- **W2b. LFS, "Employed Residents by Occupation"** (two data.gov.sg
  datasets).
  - Residents only, June, mapped to SSOC 2024.
  - The level of occupation detail is UNVERIFIED. If it is the nine major
    groups only, it cannot isolate cleaners, guards or gardeners, and is
    context.
- **W2c. MOM, "Employment Change by Industry and Residential Status"**.
  - Resident versus foreign change, December to December.
  - Probably at broad industry level (administrative and support services as
    one line). That is enough for a descriptive substitution check, not a
    test.
- **W2d.** Employment by sector at year-end, context only.

**Not found.** A public series of resident head counts by detailed occupation
(cleaners, security guards, gardeners) per year. The OWS tables may carry the
number of employees behind each wage line. The index did not say, and it is
the first thing to check when the files arrive.

### W3 -- PWM mandatory dates and wage levels, by sector

Primary sources only: MOM sector pages, Commissioner for Labour orders,
tripartite cluster reports, and the licensing agencies (NEA, SPF, NParks,
BCA). Secondary sites (payroll blogs, Wikipedia) were seen in results and not
used for any date.

| Sector | How enforced | First public step | Mandatory for residents | Primary page for the date |
|---|---|---|---|---|
| Cleaning (contract) | NEA cleaning business licence, EPHA; S 240/2014 | Tripartite Cluster for Cleaners report, 19 Oct 2012; voluntary PWM 2012 | Licensing from 1 Apr 2014; new contracts from 1 Apr or 1 Sep 2014 (sources disagree); **all resident cleaners of licensed firms by 1 Sep 2015** | MOM cleaning page; NEA licence page; S 240/2014 |
| Security (agency) | SPF/PLRD security agency licence | Security Tripartite Cluster, Oct 2014 | **1 Sep 2016**, at licence renewal | SPF PWM page; SPF brochure |
| Landscape | NParks Landscape Company Register (registration, public tenders) | NParks announcement, Apr 2015 | **June 2016** (day PENDING), LCR-registered firms only | NParks CUGE pages; MOM landscape page |
| Lift and escalator | BCA registration, workheads RW02B/RW03B | Voluntary 2018; public tenders only to PWM firms from May 2019 | **2022** (day PENDING) | BCA PWM page; BCA-MOM release |
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
2. **The Local Qualifying Salary** is a floor for every local employee of a
   firm that holds work passes. It is not a PWM, but it lifts the bottom of
   comparison jobs too. Its changes from 2022 are one more reason to end the
   comparison before September 2022.

**Wage levels.**

- The ladders are set out in the Commissioner for Labour orders (cleaning),
  SPF licensing conditions and security cluster reports, the landscape
  cluster reports, and the retail and food services cluster reports, all
  listed in RETRIEVED.txt.
- Each schedule has its own effective dates, often yearly steps. They need
  tabulating by sector and rung, with the date each step took effect, from
  the saved PDFs. This can be done before the seal: the ladders are the
  policy, not the outcome.
- Only the entry rung of cleaning, security and landscape enters a test (T5).

**Government co-funding, dated for the record.**

- The Wage Credit Scheme from 2013 and the Progressive Wage Credit Scheme
  (2022-2028) co-funded wage increases for lower-paid Singaporean employees
  in covered and uncovered jobs alike.
- They lift both sides of the comparison and are named in THESIS as things
  the design does not separate.

### W4 -- CPI

- **W4a.** CPI, 2019 as base year, annual (data.gov.sg
  `d_dcb352661fb449c4a4c0ab23aa8d6399`; SingStat M212882, labelled as the
  2019-base table; whether M212882 is the monthly or the annual version is
  UNVERIFIED).
- **W4b.** CPI by household income group, lowest 20 per cent, annual
  (data.gov.sg; SingStat M213921). This is the more honest deflator for
  low-wage pay, and it is used as a sensitivity.

CPI matters only for the level of real pay. Every scored comparison is a
difference between jobs deflated by the same index, so CPI cancels.

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

Titles below are generic. The exact OWS titles are matched from each year's
file before the seal (THESIS section 4), and no title is added or dropped
after a wage value has been seen.

| PWM ladder | OWS occupation titles (generic) | Fit | Reason |
|---|---|---|---|
| Security (agency, 2016) | security guard / security officer | **Good** | Most guards work for licensed agencies, which the 2016 condition bound. In-house guards (covered 2022) are a minority (share UNVERIFIED). |
| Cleaning (contract, 2014-2015) | office/commercial cleaners, other building cleaners | **Partial** | Mixes contract cleaners (covered 2015) with in-house cleaners (covered 2022). Clean only if occupation-within-industry tables isolate cleaners in the cleaning-services industry. Otherwise the effect is diluted toward zero. |
| Landscape (LCR firms, 2016) | gardening and landscape labourers, gardeners | **Weak** | Bound only LCR-registered firms. Registration was needed for public tenders but not to trade. The title may mix nursery and horticulture workers. Scored, with the weakness stated. |
| Lift and escalator (2022; voluntary 2018) | lift/escalator mechanic or technician | **Poor** | Mid-wage, small cell, probably merged with other mechanics in some editions, and no clean start date. Described, not scored. |
| Retail (2022) | shop sales assistant, cashier | Good **as comparison** | Uncovered until 1 Sep 2022. |
| Food services (2023) | waiter, kitchen/food preparation assistant, food and drink stall assistant, dishwasher | Good **as comparison** | Uncovered until 1 Mar 2023. Cooks left out: mostly above the low-wage band. |
| Administrators and drivers (2023) | general office clerk; car and van drivers, lorry drivers | Good **as comparison** | Uncovered until 1 Mar 2023. Conservancy truck drivers are excluded: the cleaning ladder covers them. |
| Waste management (2023) | refuse collectors | **Poor** | Small, and overlaps the cleaning ladder's conservancy roles. Left out. |

**Industries for W2a.**

- Covered: cleaning activities, private security activities, landscape care
  and maintenance.
- Comparison: retail trade, and food and beverage service activities.

The mapping is by activity code, which is cleaner than occupation for
cleaning, because a cleaning contractor's staff are the covered group. The
catch is that head counts include foreign workers.

## 4. What could not be closed, and what it does to the tests

| Gap | Effect on THESIS tests |
|---|---|
| Nothing downloaded (403 on every host) | Every coverage figure is provisional. The design chat downloads; `00_coverage.py` writes coverage into RETRIEVED.txt before the seal. |
| **OWS earliest year unknown (2011 confirmed)** | The pre-trends test (T1) needs at least 4 June surveys before each group's first announcement: 2009-2012 for cleaning, 2011-2014 for security and landscape. If OWS starts in 2011, cleaning has only 2012 and 2011 before its October 2012 announcement, and **drops out of T1 and T2**; the design then rests on security and landscape. |
| Contract vs in-house cleaners not separated at occupation level | Cleaning's pay effect is diluted toward zero unless occupation-within-industry tables are detailed enough. THESIS scores cleaning with the dilution stated. |
| No resident head count by detailed occupation | T4 uses industry workers (W2a), which include foreign workers. A resident-for-foreign swap is invisible. This leans T4 toward "jobs held". W2c gives a broad-industry substitution check, described only. |
| W2a detail level and first year | If cleaning, security and landscape are not separate lines, T4 is run on the smallest industry that contains them and says so. If it starts after 2012, cleaning drops out of T4. |
| Landscape start day; lift start day | Landscape: June 2016 is the survey month itself, so THESIS counts June 2017 as the first post-period survey whatever the day. Lift: not scored. |
| Occupation code changes (SSOC) | Titles are matched by name before the seal, and unmatched titles dropped. A break that cannot be bridged ends that title's series. |
| OWS method change ("administrative records") | PENDING from the per-year method notes. Any break is shown on the chart and handled by amendment. |
| Security announcement document (October 2014) not located | Only the month is used (last pre-period June is 2014). |

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
4. **W5 PDFs**, if convenient. Not needed before the seal.
5. **Checker disclosure.** Before the seal, state whether the checker has
   read OWS tables, LFS income by occupation, or MOM statements on PWM wage
   growth.
6. **Review THESIS.md (unsealed)** and set the confidences.

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
