# SOURCES REPORT -- erp piece

Researcher: `erp` (Claude Code session), 24 September 2026, branch `erp-wip`.
Scope of this task: sources only. No analysis, no charts, no data values opened.

## 0. The one-paragraph version

Nothing was downloaded. The sandbox proxy refuses data.gov.sg, lta.gov.sg,
mot.gov.sg, oecd.org and archive.org (HTTP 403 at CONNECT), so every source
below was **located through a web search index, not opened**. Titles, dataset
ids and URLs are confirmed that way; coverage figures quoted from the index are
marked UNVERIFIED and must be re-checked from the files. The exact URLs and
target filenames for Jacob are in `erp/raw/RETRIEVED.txt`. Of the six items,
E1, E2, E3 and E6 have a primary source identified; E7 has a primary chain of
LTA releases for 2020 with one conflict in it; **E5 is not closed: no dated
primary history of ERP rate changes and gantry additions was found for the years
before 2020**, and that removes one leg of the "COE wins" test (section 3).

## 1. Exposure disclosure (read first)

The seal is only worth something if it is clear what had been seen. Three things:

1. **One E1 value was seen, unsolicited.** A search for the LTA "Statistics in
   Brief" series returned, inside the search tool's own summary, the 2011
   peak-hour averages from a third-party copy of *LTA Statistics in Brief 2012*
   (yumpu.com): expressways 62.5 km/h, arterial roads 28.5 km/h. It was not
   sought and the page was not opened, but it was read. Both sit inside the E6
   bands. THESIS.md flags 2011 as not blind in T1, and it is excluded from T1's
   scoring (see THESIS section 6).
2. **No other value from E1, E2 or E3 was seen.** No coverage span from the
   files themselves was seen either, because no file was received.
3. **Background knowledge.** The researcher's general knowledge includes the
   public outline of Singapore motoring policy (the vehicle growth rate being cut
   in steps to zero by 2018, COE premiums rising sharply after 2010, ERP starting
   in 1998). It does not include the E1 or E2 series year by year. The THESIS
   thresholds are written as judgements, and the reasoning for each is stated
   so that a reader can see it does not lean on a remembered value.

## 2. Item by item

### E1 -- average peak-hour speed, expressways and arterials, annual

- **Source:** data.gov.sg `d_26f6afadf2f86b2004f9a1e28f5564cc`, "Average Speed
  During Peak Hours", LTA. Part of the collection "Road Traffic Conditions during
  Peak Hours" (collection 379).
- **Status:** located, NOT downloaded (403).
- **Definition, from the search index, UNVERIFIED:** peak hours are 8-9am and
  6-7pm on weekdays; the arterial figure is "based on key arterial roads".
- **Coverage: UNKNOWN.** The index did not report it. This is the largest open
  risk in the piece. The brief assumes 2004-2025. If the dataset stops early
  (the collection's older URL form suggests a legacy series), the fallback for
  expressways only is an MOT written parliamentary reply giving peak-hour
  expressway speeds for 2019 to 2023 (URL in RETRIEVED.txt). No arterial
  fallback was found.
- **Measurement caveat that survives any coverage outcome:** E1 is one network
  average per road class per year. ERP rates are set per gantry per half-hour.
  The annual figure can sit inside the band while individual priced stretches
  sit outside it, and the reverse.

### E2 -- average annual km per vehicle, by type

- **Source:** data.gov.sg `d_bdc4c6434e47b055de4b5f2fde10c1af`, "Average Annual
  Kilometres Travelled Per Vehicle", LTA; collection 311 "Annual Mileage for
  Private Motor Vehicles".
- **Status:** located, NOT downloaded (403).
- **Coverage, from the search index, UNVERIFIED:** January 2005 to December
  2018, last updated 6 June 2024. Method as described on the page: estimated
  from a mileage survey of in-use vehicles at mandatory periodic inspections.
- **If that coverage holds:** 14 annual points. 2010-2013 is inside, as the
  brief expects. Nothing after 2018, so the whole post-2018 zero-growth period
  and 2020 are outside E2. Whether private-hire cars are split out from private
  cars is unknown until the columns are seen; the private-hire build-up starts
  inside the E2 window and could move km per car on its own.

### E3 -- annual car population

- **Source found:** data.gov.sg `d_2873f3b1b2a836103f51f696350b98fa`, "Annual
  Motor Vehicle Population by Vehicle Type", LTA.
- **Status:** located, NOT downloaded (403).
- **Coverage, from the search index, UNVERIFIED:** 2005 to 2024, 4 columns.
- **Gaps:** if 2025 is missing, LTA's own *Annual Vehicle Statistics 2025*,
  "Motor Vehicle Population by Vehicle Type" (PDF MVP01-1) is the primary backup.
  If E1 starts in 2004 and E3 in 2005, 2004 drops out of every test that uses
  both. A monthly dataset (`d_2ecb009f1e1ec5a816a454944dec4022`) exists as a
  second route.

### E4 -- COE premium (not in the brief's list; needed by the door-fee test)

- **Source:** already in the repository, `raw.csv`, data.gov.sg
  `d_69b3380ad7e51aff3a7dcc84eba52b8a`, md5 `7b68a001709821c71ece5b8ed209d4d3`
  (matches README.md).
- **Coverage, checked 24 Sep 2026 by dates and columns only:** month 2010-01 to
  2026-08; 1,965 data rows; columns month, bidding_no, vehicle_class, quota,
  bids_success, bids_received, premium.
- **Gap:** no premium before 2010. Any test that uses the premium runs from 2010,
  not 2004. The brief's "through the swings in ... COE prices, 2004-2025" can be
  read against premiums only from 2010. A pre-2010 series would need another
  source; none was sought in this task.

### E5 -- dated history of ERP rate changes and gantry additions

**NOT CLOSED.**

- **LTA newsroom releases** are the primary route and they exist from March 2020
  onward: the search index returned LTA releases dated 2020-03, 2020-04 (two),
  2020-05, 2020-07, 2020-10, 2021-02, 2022-02, 2022-03, 2022-05, 2022-11, 2023-03,
  2023-08, 2024-09, 2025-05, 2025-08, 2025-11, 2026-03, 2026-05 and 2026-08.
  **The earliest LTA-hosted release found is March 2020.** Searches targeted at
  2005-2009 and 2014-2018 returned no LTA release. That is evidence that the
  current newsroom does not index them, not proof that they are gone; the
  newsroom's own year filter settles it and Jacob is asked to note the earliest
  year it offers.
- **Pre-2020:** the old LTA site (`lta.gov.sg/apps/news/...`) is the likely home
  of 2004-2019 releases. The only route found is the Wayback Machine, which this
  session could not reach.
- **No data.gov.sg or DataMall series of historical ERP rates exists** as far as
  the search could establish. DataMall's ERP Rates API gave current rates only
  and was removed on 30 September 2024 (third-party report, unverified).
  data.gov.sg holds a gantry location file (`d_753090823cc9920ac41efaa6530c5893`,
  GeoJSON), which is a current snapshot, not a history.
- **Gantry additions, secondary only:** NLB Infopedia ("Electronic Road Pricing:
  Developments after phase I") and press retrospectives date individual
  additions (for example BKE in 2007, the Singapore River line in 2008). These
  can date events for a timeline; they cannot supply a figure under the site's
  source rule.
- **Academic secondary:** W. Theseira, "Congestion Control in Singapore",
  ITF/OECD discussion paper, 2020. Useful for method and history; not a source
  for any number in the piece.

**What E5 not closing means:** there is no year-by-year measure of how hard ERP
was pushing (rate levels, number of increases, gantry count) across 2004-2025.
See section 3.

### E6 -- speed bands that trigger ERP rate changes

- **Primary sources located:** MOT, "How ERP works as a speed booster"; MOT,
  written reply to a parliamentary question on the rationale for higher ERP
  rates; current LTA "Revised ERP Rates" releases (for example 7 September 2026).
- **What they state, per the search index, UNVERIFIED until the PDFs are read:**
  45-65 km/h on expressways and 20-30 km/h on arterial roads. Rates are cut when
  speeds are above the upper bound and raised when below the lower bound. Rates
  are set in half-hour blocks and reviewed quarterly. A secondary ADB case study
  adds that the arterial band also covers roads crossing the Restricted Zone
  cordon.
- **The quoted bands are confirmed as the ones LTA and MOT cite today.** Two
  things are NOT confirmed: (a) that the bands were the same across 2004-2025
  (no dated source for a change was found, and none for their absence); (b) what
  speed measure LTA compares with the band (which percentile, which segment,
  which half-hour). (b) matters because E1 is a different measure (section 2,
  E1).

### E7 -- periods ERP charges were suspended or cut sitewide

Primary chain, all LTA releases, located but not opened:

| Date (from index) | Release | What the index says it did |
|---|---|---|
| March 2020 | "Electronic Road Pricing (ERP) Review" | review brought forward; rates cut at 96 per cent of gantries, some to $0, effective 6 April 2020 |
| April 2020 | "Cessation of ERP Charging ... from 7 April to 4 May 2020" | charging ceased at all gantries from 6 April 2020, 0000 hours |
| April 2020 | "ERP Charging and COE Bidding Continue to be Suspended During Extended Circuit Breaker Measures" | suspension extended with the circuit breaker |
| 31 May 2020 | "LTA to Resume ERP Rate Reviews" | reviews resume from 2 June 2020; review cycle shortened to four weeks |
| July 2020 | "Second ERP Rate Review Post-Circuit Breaker" | (not summarised by the index) |
| October 2020 | "ERP Rate Review" | (not summarised by the index) |
| February 2021, February 2022 | "Revised ERP Rates ..." | (not summarised by the index) |

- **Conflict, unresolved:** the date charging resumed. The index offers 29 June
  2020 (first post-circuit-breaker review), "no charges until 28 June", and a
  press report of "no charges until at least 26 July". Only the releases settle
  it. The sitewide $0 period may also have ended gantry by gantry rather than on
  one date.
- **2022:** an MOT release, "Reviewing Implementation of Increase in ERP Rates
  Amid Rising Petrol and Fuel Costs", suggests increases due under the speed rule
  were held back. If so, that is a period when the thermostat was deliberately
  switched off in one direction.
- **Routine cuts:** LTA lowers rates in June and December school holidays every
  year. Within-year and seasonal; invisible in an annual series.
- **The circuit-breaker confound:** the 2020 suspension coincided with workplace
  closure and full home-based learning. Traffic collapsed for reasons that had
  nothing to do with price. 2020 speeds therefore say nothing about what removing
  ERP does, and 2021 is likely contaminated by remote work. Annual data also
  averages the suspension with charged months. E7 is useful as a dated label on
  the chart, not as a natural experiment.

## 3. What could not be closed, and what it does to the tests

| Gap | Effect on THESIS tests |
|---|---|
| E1 coverage unknown | Every test's year range is provisional. If E1 is short (under about 12 years), T2 and T4 lose most of their power and are reported as descriptive. |
| E5 not closed | No ERP intensity series. The "COE wins" condition "with ERP changes adding little" cannot be tested; only its car-population leg can. The piece can show whether speeds behave like a thermostat, not that ERP is the thermostat. |
| E6 bands' history and measure | T1 scores E1 against today's bands. If the bands changed, T1 is scored against the band in force each year, which needs a dated source. |
| E4 starts 2010 | T4 (premium beyond car population) runs on at most 2010 to the end of E1, minus 2020-2021: roughly 10-14 points. |
| E2 ends 2018 (if index is right) | T3 runs on 2010-2018 for the premium split; S1 total car-km stops at 2018. |
| E7 resumption date | Affects only the chart label and the exclusion of 2020; 2020 and 2021 are excluded from fitted tests either way. |

## 4. Asks of Jacob (one consolidated list)

1. Download the three CSVs (E1, E2, E3) and the PDFs listed in
   `erp/raw/RETRIEVED.txt`, upload to `erp/raw/` on `erp-wip` through github.com.
   Sizes are small: three CSVs well under 1 MB; roughly 15 PDFs.
2. Note the "last updated" date and coverage shown on each data.gov.sg page.
3. On the LTA newsroom, note the earliest year its filter offers for ERP
   releases (settles how far back E5 route 1 goes).
4. Review THESIS.md (unsealed) and rule on the open items in its section 10.

## Sources used to locate the above (search index, 24 September 2026)

- https://data.gov.sg/datasets/d_26f6afadf2f86b2004f9a1e28f5564cc/view
- https://data.gov.sg/collections/379/view
- https://data.gov.sg/datasets/d_bdc4c6434e47b055de4b5f2fde10c1af/view
- https://data.gov.sg/collections/311/view
- https://data.gov.sg/datasets/d_2873f3b1b2a836103f51f696350b98fa/view
- https://data.gov.sg/datasets/d_2ecb009f1e1ec5a816a454944dec4022/view
- https://data.gov.sg/datasets/d_753090823cc9920ac41efaa6530c5893/view
- https://www.lta.gov.sg/content/dam/ltagov/who_we_are/statistics_and_publications/statistics/pdf/MVP01-1_MVP_by_type.pdf
- https://www.mot.gov.sg/news-resources/resources/how-erp-works-as-a-speed-booster/
- https://mot.gov.sg/news/details/written-reply-to-parliamentary-question-on-rationale-for-and-impact-of-higher-erp-rates-on-traffic-volumes
- https://www.mot.gov.sg/news/details/written-reply-to-parliamentary-questions-on-data-on-average-speed-of-vehicles-on-expressways-during-peak-hours-from-2019-to-2023
- https://www.mot.gov.sg/news-resources/newsroom/reviewing-implementation-of-increase-in-erp-rates-amid-rising-petrol-and-fuel-costs/
- LTA newsroom releases 2020-03 to 2026-08, full URLs in `erp/raw/RETRIEVED.txt`
- https://www.nlb.gov.sg/main/article-detail?cmsuuid=7d61ae5c-869e-41ac-9e76-28392219c249 (secondary)
- https://development.asia/case-study/case-electronic-road-pricing (secondary)
- https://www.oecd.org/content/dam/oecd/en/publications/reports/2020/10/congestion-control-in-singapore_c3005a82/7d266609-en.pdf (secondary, academic)
- https://www.yumpu.com/en/document/view/11484644/statistics-in-brief-2012-land-transport-authority (third-party copy; source of the disclosed 2011 value; not used)
