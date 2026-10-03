# SOURCES REPORT -- sgd piece

Researcher: `sgd` (Claude Code session), 29 September 2026, branch `sgd-wip`,
cut from `origin/main` at 6e4acf0. Revised 3 October 2026 after the checker
review of 6f9b6c2:
- five scored tests;
- former T5 is sensitivity B; former T6 is check C;
- T2 and T3 score January 2021 to December 2025;
- answer due December 2026.

Changed sections: 0, 1 (items 2 and 6), 2, 3 (S4), 4 (last line), 5 (item
2), 6, 7.

Scope: Checkpoint 0 (data feasibility), sources and the data check only. No
analysis, no charts, no data value opened. The exact URLs and target filenames
are in `sgd/raw/RETRIEVED.txt`; the coverage lister for the files, once they
arrive, is `sgd/00_coverage.py`. It prints labels and coverage, never a value.

The belief on trial (approved direction): the Singapore dollar rises because
Singapore's economy is strong, and a cheap yen or ringgit means the Singapore
dollar got stronger. The rival: MAS steers the Singapore dollar against a
basket of trading partners' currencies on a slow, deliberate path, so most of
a move against one currency is that currency moving.

## 0. The one-paragraph version

Nothing was downloaded. The session's egress proxy refuses every data host
tried with HTTP 403 at CONNECT, a policy denial. That covers BIS, MAS,
SingStat, data.gov.sg, HKMA, BOJ, Japan's MOF, BNM, FRED, IMF, OECD, the World
Bank and the Wayback Machine. The session's web-fetch tool was refused for
data.bis.org too. Every source below was **located through a web search
index, not opened**. What exists:

- **S1, BIS nominal effective exchange rates, monthly, broad basket.** Series
  pages were seen by label for Singapore, Japan, Malaysia, Korea, Indonesia
  and the euro area. China and the United States were seen for the real
  index. Thailand, Australia and Hong Kong follow the key pattern of the
  64-economy basket, which lists them. Coverage runs from 1994 (BIS
  documentation).
- **S2, BIS bilateral US dollar rates, monthly.** Seen by label for the
  Singapore dollar, the yen and the ringgit (end of period). The monthly
  average collection is expected but was not seen.
- **S3, MAS's own monthly exchange rates, as republished by SingStat.** Found
  as table M700051 (average) and M700041 (end of period), from January 1988.
- **S4, MAS's own S$NEER index, weekly.** It exists, but MAS's page shows only
  the "current and previous years", so the overlap with BIS may be short.
- **S5, MAS policy decisions.** A primary MAS page lists every decision since
  2001 by slope, width and level of the band centre, with a link to each
  statement.
- **S6 and S7, SingStat GDP growth and CPI.** Found.
- **World view.** HKMA (the peg), BOJ and MOF (Japan's float and its
  interventions), BNM and PBOC (the dates the ringgit and renminbi pegs
  ended).

**All five scored tests survive the feasibility check on sources** (T1, T2,
T3, T4 and T7), pending the keys and coverage on receipt.
- **Sensitivity B (breadth, formerly T5)** is feasible on the same series.
- **Check C (BIS index against MAS's own, formerly T6)** is printed beside
  T7 and gates nothing. MAS's page may show only about two years of its
  S$NEER, which is why it is no longer a scored test.

**Not feasible and not planned:** any test of where the Singapore dollar sat
inside MAS's band. The band's slope, width
and centre are not disclosed, only described in words. Also not feasible:
any claim about how many Singaporeans hold the belief, since no survey was
sought.

## 1. Exposure disclosure (read first)

The seal is only worth something if it is clear what had been seen.

1. **No series file was opened.** No file was received.
2. **Values seen in search summaries.** Each is a single date, not a series.
   - **Ringgit.** One summary said: "as of February 2026, Malaysia's broad
     effective exchange rate stands at 112.93 on an index with 2020=100".
     This is one point of S1 for MY. It says the ringgit's broad index in
     February 2026 was about 13 per cent above its 2020 average.
     - **It bears directly on T3,** whose scored window is now January
       2021 to December 2025. The ringgit's own broad index may have ended
       that window near or above where it started. In that case T3 fails,
       or the Singapore dollar did not rise against the ringgit and T3 is
       not scored.
     - **Where it is used.** It is recorded here because it was seen
       before the seal. The researcher's proposed confidence for T3
       (THESIS section 6) uses it; the window rule does not (item 6).
   - **Renminbi.** One summary gave the renminbi's July 2005 revaluation as
     8.11 per US dollar (2.1 per cent). This is a policy setting on the
     reform date, not a series.
   - **Hong Kong dollar.** HKMA's convertibility undertakings at HK$7.75 and
     HK$7.85 per US dollar are policy settings.
   - **Ringgit peg.** The peg at RM3.80 per US dollar, from 2 September 1998
     to 21 July 2005, is a policy setting.
3. **Policy decisions seen in titles (inputs to T7's coding, not outcomes).**
   - October 2017: "kept the slope, band width and the centre ... unchanged"
     (a bank note's title).
   - January 2025: "slightly reduce the slope".
   - January 2026: "Keeps S$NEER Policy Band on Appreciating Slope".
   - July 2026: "Surprise S$NEER Tightening", "MAS Tightens Policy Again in
     July 2026".
   - October 2026: previews titled "Third Tightening?", and on 29 September
     2026 "MAS tightening expectations support resilience".

   These will be coded from S5a in any case; seeing them in titles changes
   nothing that the coding rule does not already fix.
4. **Context seen in titles, not used in any test.**
   - "Japan Spends Record Amount on Yen-Buying Intervention in October"
     (year not shown).
   - "HKMA steps in again to defend HKD peg" (July 2025).
5. **The researcher's background knowledge, stated because it cannot be
   unseen.** The researcher (a language model) knows the broad shape of
   several moves from training, not from any file of this piece. None is a
   number from S1 to S7. It is general knowledge of the kind found in news
   coverage:
   - the yen weakened a great deal against the US dollar from late 2012,
     and again from 2021 to 2024;
   - the ringgit weakened in 2014-2015 and again in 2022-2024;
   - over the two decades from 2005 the Singapore dollar bought
     substantially more yen and more ringgit at the end than at the start;
   - MAS tightened several times between October 2021 and October 2022;
   - MAS set a zero slope in October 2008 and in March 2020, the second
     with a downward re-centring.

   This knowledge informs the researcher's proposed confidences in THESIS,
   which are marked as such; Jacob sets his own.
6. **What this means for the seal: the windows.**
   - **The scored window for T2 and T3** is the last five full calendar
     years before the seal: January 2021 to December 2025. It is fixed by
     that rule, set at the checker review of 6f9b6c2 because the reader's
     hook is that Japan got cheaper lately.
   - **Stated plainly: general knowledge of the yen's fall since 2021 was in
     mind when the rule was set** (item 5), both the checker's and the
     researcher's. The rule ties the window to the seal date, not to any
     turning point in the yen. It is fixed now and does not move if the
     seal slips. But it was not set blind to the yen's recent path, and the
     article says so.
   - **The ringgit index point** (item 2) was also seen before the rule was
     set. The rule does not depend on it; the researcher's T3 proposal does.
   - **The long window** (August 2005 on) is fixed on the end of the ringgit
     and renminbi pegs on 21 July 2005, not on any outcome. It carries T4,
     T7 (from 2001, the first MAS decision listed), T1's second check, and
     the long-run sensitivity of T2 and T3.

## 2. Checkpoint 0: data feasibility, test by test

Status words:
- **LABEL SEEN**: a series page or table title was seen in the index.
- **BY PATTERN**: the key follows a documented pattern and the area is
  documented in the basket, but the page was not seen.
- **UNVERIFIED**: the coverage comes from a documentation or index summary,
  not from the file.

Every row stays "pending receipt" until `00_coverage.py` lists the file.

| Test (THESIS) | Series needed | Exists? | Coverage (documented) | Feasible? |
|---|---|---|---|---|
| T1 decomposition closes (design) | S1 M.N.B.SG, JP, MY; S2 SGD, JPY, MYR per USD, monthly average; S3a SGD per 100 JPY, per 100 MYR | S1: LABEL SEEN (all three). S2: LABEL SEEN for the end-of-period (E) collection; average (A) UNVERIFIED. S3a: table title seen | S1 from 1994-01; S2 from about 1957; S3a from 1988-01 (UNVERIFIED) | Yes, pending receipt. If S2 has no A collection, S2 E is used and the rule in THESIS T1 applies |
| T2 yen share | S1 M.N.B.SG, JP; S2 SGD, JPY | as T1 | scored window 2021-01 to 2025-12; long-run sensitivity 2005-08 on; both inside all coverage | Yes, pending receipt |
| T3 ringgit share | S1 M.N.B.SG, MY; S2 SGD, MYR | as T1 | as T2 | Yes, pending receipt |
| T4 slow path (volatility rank) | S1 M.N.B for SG, JP, MY, KR, CN, TH, ID, US, XM, AU, HK | LABEL SEEN: SG, JP, MY, KR, ID, XM (and CN, US for the real index). BY PATTERN: TH, AU, HK; CN and US nominal | from 1994-01 (UNVERIFIED) | Yes, pending receipt. THESIS T4 fixes what happens if a comparison series is missing |
| Sensitivity B, breadth (formerly T5; not scored) | S1 as T4; S2 for the ten partner currencies | S1 as T4; S2 LABEL SEEN for SGD, JPY, MYR; others BY PATTERN | as T4 | Yes, pending receipt |
| Check C, BIS index against MAS's own (formerly T6; not scored, gates nothing) | S1 M.N.B.SG; S4 MAS S$NEER weekly | S4: page title seen; the download format is not known | "current and previous years" (MAS page, index summary): possibly only about 2024-2026 | Printed beside T7; "too short to read" under 24 monthly changes |
| T7 policy or growth | S5a decisions table; S5b statements; S1 M.N.B.SG; S6a GDP year-on-year growth, quarterly | S5a: page title seen; layout (Date, Slope, Width, Level) from index summary and a third-party copy. S6a: table title seen (id M015631 UNVERIFIED; fallback M015661 levels) | decisions since 2001; GDP quarterly from the 1970s (UNVERIFIED) | Yes, pending receipt. The slope is coded from words, since MAS publishes no number (section 5) |
| (sensitivity to T7) inflation | S7a CPI monthly | table title seen (M213751) | 2024 base; long history (UNVERIFIED) | Yes, reported and not scored |

**Tests considered and dropped at Checkpoint 0:**

- **Where the S$NEER sat inside MAS's band.** Not feasible: MAS does not
  disclose the slope, the width or the centre of the band (MAS FAQ,
  section 4). Any band drawn would be a third party's estimate.
- **Growth relative to trading partners** (the "strong economy" read as
  growth faster than partners'). It would need GDP for every partner at
  matching quarters, and none was sought. It is listed as an extension, not
  planned.
- **Real-time growth** (the advance GDP estimate as published on each
  decision date). SingStat's advance releases exist as PDFs, but a vintage
  series was not located. T7 uses the current published series (THESIS
  section 5).
- **How many Singaporeans hold the belief.** No survey was sought. The
  article can describe the belief as a common reading, but cannot give its
  share.

## 3. Item by item

### S1 -- BIS nominal effective exchange rates (WS_EER), monthly, broad

- **What it is.** A geometric trade-weighted average of a currency's
  bilateral rates against a basket of 64 economies. The weights come from
  manufacturing trade with double weighting for third markets. They change
  on three-year periods: the index for 2009 uses 2008-2010 weights. Index
  2020 = 100. A rise means the currency strengthened against its basket.
- **Why BIS and not MAS.** MAS's S$NEER basket and weights are not
  disclosed (S5c). BIS computes one method for every economy, so the
  Singapore dollar, the yen and the ringgit are measured the same way. That
  consistency is what the decomposition needs.
- **Keys.** M.N.B.<AREA>, with the euro area as XM. Series pages seen in the
  index: SG, JP, MY, KR, ID, XM (nominal broad); CN, US, JP, SG, MY (real
  broad); PH (nominal broad, not needed).
- **Coverage.** Broad monthly from 1994; daily from 1996. Narrow monthly
  from 1964 for 26 or 27 economies (BIS pages; UNVERIFIED).
- **Download.** API v2 CSV, per-series portal export or bulk zip
  (RETRIEVED.txt S1).
- **Weights.** The broad-basket weights file was located by description
  only. It is optional: it would show how much the yen and the ringgit
  weigh in the Singapore basket, and the Singapore dollar in theirs, which
  bears on the T3 lean.

### S2 -- BIS bilateral exchange rates against the US dollar (WS_XRU)

- **What it is.** Units of each currency per US dollar, monthly, quarterly
  and annual, for about 190 economies, many from about 1957. Compiled from
  ECB, Federal Reserve, central bank and IMF sources (BIS documentation).
- **Keys.** M.<AREA>.<CUR>.<E|A>. E (end of period) was seen for MY
  monthly and for SG and JP annual; A (average) was not seen in the index.
- **Use.** The cross rate, units of X per Singapore dollar, is X per USD
  divided by SGD per USD. It uses the same source family as S1, so the
  identity in THESIS section 4 is tested on consistent data.

### S3 -- MAS exchange rates, monthly (SingStat M700051, M700041)

- **What it is.** SGD per unit of foreign currency, or per 100 units for the
  yen and several others (UNVERIFIED which), average and end of period. It
  is the average of buying and selling interbank rates quoted around midday
  in Singapore (MAS, index summary). Source MAS; republished by SingStat and
  data.gov.sg.
- **Coverage.** January 1988 on (index summary of the data.gov.sg copy,
  which was said to run to November 2024; TableBuilder is likely to be more
  current; UNVERIFIED).
- **Use.** The T1 cross-check: BIS cross rates against the rate Singapore
  itself publishes. Also the reader-facing numbers ("a Singapore dollar
  bought N yen").

### S4 -- MAS S$NEER, weekly

- **What it is.** MAS's own trade-weighted index, the one the policy band is
  set on. Basket and weights undisclosed. MAS releases weekly indexed data
  on a monthly schedule (Advance Release Calendar, index summary).
- **Coverage.** The page shows "current and previous years" (index summary).
  If that is literal, about 2024 to 2026 is available, roughly 30 monthly
  changes. The count is UNVERIFIED.
- **Use.** Check C only (formerly T6): does the BIS broad Singapore index
  move with MAS's own? It is printed beside T7 and gates nothing; under 24
  monthly changes it is printed as "too short to read".

### S5 -- MAS monetary policy decisions and statements

- **S5a, Past Monetary Policy Decisions.**
  - It lists MAS's decisions since 2001, with the Date, Slope, Width and
    Level columns, "-" where unchanged, and each date linking to its
    statement (index summary and a third-party copy of the layout).
  - Statements were semi-annual from 2001; April and October from October
    2003 to October 2023; quarterly (January, April, July, October) from
    2024 (index summary of the page).
  - There were off-cycle statements (a July 2022 statement URL was seen;
    others to be listed from S5a).
- **S5b, the statements themselves.** Used to confirm each date and to read
  the decision paragraph verbatim.
- **S5c, the MAS FAQ.** MAS does not disclose the basket, its weights, or
  the slope, width and centre of the band. When it changes them it
  describes the change in words, for example "a 'slight' increase in the
  slope".
- **S5d, MAS foreign exchange operations.** Net purchases on a six-month
  basis with a three-month lag, released on the first business day of
  April and October (MAS page and a 2020 release). Context only.
- **Feasibility note for T7.** The decisions are policy inputs, like the
  rung amounts in the pwm piece. They can be read and coded before the
  seal, once S5a is received, without opening any exchange-rate or GDP
  value. The coding rule is fixed in THESIS T7. The coding sheet
  (`office/MPS_CODING.csv`) is to be produced from S5a after receipt and
  before the seal.

### S6 -- SingStat GDP growth

- **S6a.** "Gross Domestic Product Year On Year Growth Rate, Quarterly",
  chained (2015) dollars. The index gave TableBuilder id M015631
  (UNVERIFIED).
- **S6b.** Levels by industry, M015661, as a fallback: growth is computed
  from the total.
- **S6c.** The data.gov.sg copy, d_a5ff719648a0e6d4b4c623ee383ab686.
- **Vintage.** These are the current published figures, revised since each
  decision date. MAS decided on the advance estimate. See THESIS section 5
  for why the test still reads the current series.

### S7 -- SingStat CPI

- **S7a.** CPI, 2024 as base year, monthly (M213751;
  d_bdaff844e3ef89d39fceb962ff8f0791). It is used for one T7 sensitivity:
  inflation is what MAS's policy targets, so the path might follow it rather
  than growth. Reported, not scored.
- **S7b.** MAS core inflation, monthly, is published in MAS's "Consumer
  Price Developments" PDFs. No TableBuilder id was located. Not needed.

## 4. World view: two economies that chose differently

| | Hong Kong | Singapore | Japan |
|---|---|---|---|
| Regime | Hard peg to the US dollar since 1983; convertibility undertakings at HK$7.75 and HK$7.85 (HKMA) | Crawling band against an undisclosed basket; slope, width and centre reviewed at each statement (MAS) | Free float since February 1973; occasional intervention ordered by MOF, executed by BOJ (BOJ, MOF) |
| What a move against the yen is, in the extreme | The US dollar's move against the yen, since HK$ follows US$ | Partly the Singapore dollar's band path, partly the yen | For the yen: Japan's own move, by definition |
| Series in this piece | S1 M.N.B.HK; S2 HKD | S1 M.N.B.SG; S2 SGD; S3; S4 | S1 M.N.B.JP; S2 JPY |
| Primary pages | `w1_hkma_lers_how_it_works` | S5a-S5c | `w2a`-`w2c` (BOJ outline; MOF intervention pages) |

The peg and the float bracket Singapore's choice. THESIS uses them in T4:
the Singapore dollar's broad index is predicted to be steadier month to month
than both. They also serve as descriptive checks, reported and not scored:
- the Hong Kong dollar's broad index tracks the US dollar's;
- the yen's broad index is among the most variable in the set.

Malaysia and China are in the set as partners. Their pegs to the US dollar
ended on the same day, 21 July 2005 (BNM milestones page; PBOC spokesman's
statement). That date fixes the start of the long window (THESIS section 5).

## 5. What could not be closed, and what it does to the tests

1. **Nothing was downloaded.** Every row of section 2 is "pending receipt".
   A key that turns out missing is handled by the rules in THESIS; no rule
   is changed after a file arrives.
2. **The S$NEER's overlap.** If MAS shows only the current and previous
   years, check C rests on about 30 monthly changes; with fewer than 24 it is
   printed as "too short to read". T7 is read on the BIS index either way;
   check C gates nothing (THESIS section 7).
3. **The band is undisclosed.** T7 codes the stance from MAS's words. This
   is coarse by design: a "slight" increase and a larger one both count as
   a positive slope in the scored coding. A finer ordinal coding is a
   sensitivity.
4. **The yen's and ringgit's weights in the Singapore basket, and the
   Singapore dollar's in theirs.** Located by description only. Without them
   the T3 lean (Malaysia and Singapore sit heavily in each other's baskets)
   is stated in words, not sized.
5. **GDP vintages.** T7 compares the path with growth as now published, not
   as MAS saw it on the day.
6. **The belief's prevalence.** Unsourced. The piece tests the belief's
   claim, not how many hold it.

## 6. Which tests survive the feasibility check

- **Scored, all feasible pending receipt:** T1 (design), T2 (yen), T3
  (ringgit), T4 (slow path), T7 (policy or growth).
- **Reported, not scored:**
  - sensitivity B (breadth, formerly T5);
  - check C (BIS against MAS's own index, formerly T6), printed beside T7
    and gating nothing.
- **Dropped:** position in the band; growth relative to partners; real-time
  growth; prevalence of the belief (section 2).

THESIS.md is drafted, unsealed, for the tests that survive.

## 7. Asks of Jacob (one list)

1. **The downloads.** Everything in `raw/RETRIEVED.txt`, under the suggested
   filenames, in `sgd/raw/` on `sgd-wip`. Then the output of
   `python3 sgd/00_coverage.py` goes into RETRIEVED.txt's RECEIVED section.
   - **Who fetches.** If Jacob opens network access for this environment,
     the researcher fetches. Otherwise the design chat does, from Jacob's
     machine.
   - **Status on 3 October 2026:** still blocked.
   - Nothing is to be opened in a spreadsheet program or previewed.
2. **S4, MAS's S$NEER page.** How many years the download offers. One line
   is enough; it decides whether check C is readable.
3. **S5a, the decisions table.** Saved as served and printed to PDF. Coding
   (`office/MPS_CODING.csv`) follows from it before the seal.
4. **Confidences.** For T1, T2, T3, T4 and T7 (THESIS section 6). The
   researcher's proposals are marked as such.
5. **The windows.** Accept or change the scored window for T2 and T3
   (January 2021 to December 2025), the long window (August 2005 on), and the
   sensitivities (THESIS section 5).
6. **The answer date.** December 2026; January 2027 only if the downloads
   slip.

## Sources used to locate the above (search index, 29 September 2026)

- BIS: [effective exchange rates overview](https://www.bis.org/statistics/eer.htm);
  [EER data portal](https://data.bis.org/topics/EER);
  [SG broad nominal](https://data.bis.org/topics/EER/BIS,WS_EER,1.0/M.N.B.SG);
  [MY broad nominal](https://data.bis.org/topics/EER/BIS,WS_EER,1.0/M.N.B.MY);
  [JP broad nominal](https://data.bis.org/topics/EER/BIS,WS_EER,1.0/M.N.B.JP);
  [KR broad nominal](https://data.bis.org/topics/EER/BIS,WS_EER,1.0/M.N.B.KR);
  [ID broad nominal](https://data.bis.org/topics/EER/BIS,WS_EER,1.0/M.N.B.ID);
  [euro area broad nominal](https://data.bis.org/topics/EER/BIS,WS_EER,1.0/M.N.B.XM);
  [CN broad real](https://data.bis.org/topics/EER/BIS,WS_EER,1.0/M.R.B.CN);
  [US broad real](https://data.bis.org/topics/EER/BIS,WS_EER,1.0/M.R.B.US);
  [The new BIS effective exchange rate indices (2006)](https://www.bis.org/publ/qtrpdf/r_qt0603e.pdf);
  [Asian EER technical note](https://www.bis.org/publ/work217.pdf);
  [bilateral rates portal](https://data.bis.org/topics/XRU);
  [MYR per USD, monthly, end of period](https://data.bis.org/topics/XRU/BIS,WS_XRU,1.0/M.MY.MYR.E);
  [bilateral rates documentation](https://www.bis.org/statistics/xrusd/xrusd_doc.pdf);
  [Stats API v2](https://stats.bis.org/api-doc/v2/);
  [bulk downloads](https://data.bis.org/bulkdownload).
- MAS: [Past Monetary Policy Decisions](https://www.mas.gov.sg/monetary-policy/past-monetary-policy-decisions);
  [Monetary Policy Statements](https://www.mas.gov.sg/monetary-policy/mas-monetary-policy-statements);
  [FAQ section 4](https://www.mas.gov.sg/monetary-policy/singapores-monetary-policy-framework/faqs/section-4);
  [FAQ PDF](https://www.mas.gov.sg/-/media/mas-media-library/monetary-policy/singapores-monetary-policy-framework/faqs/mp_faqs.pdf);
  [S$NEER index page](https://www.mas.gov.sg/statistics/exchange-rates/s$neer);
  [exchange rates](https://www.mas.gov.sg/statistics/exchange-rates);
  [eServices exchange rates](https://eservices.mas.gov.sg/Statistics/msb/ExchangeRates.aspx);
  [foreign exchange operations](https://www.mas.gov.sg/statistics/reserve-statistics/foreign-exchange-operations);
  [Advance Release Calendar](https://www.mas.gov.sg/monetary-policy/advance-release-calendar);
  [MAS Press Statement, July 2005](https://www.mas.gov.sg/news/monetary-policy-statements/2005/mas-press-statement);
  [The BBC Framework](https://www.mas.gov.sg/who-we-are/mas-gallery/explore-our-gallery/zone-b/sustained-non-inflationary-economic-growth/the-bbc-framework).
- SingStat and data.gov.sg: [M700051](https://tablebuilder.singstat.gov.sg/table/TS/M700051);
  [M700041](https://tablebuilder.singstat.gov.sg/table/TS/M700041);
  [monthly average rates, data.gov.sg](https://data.gov.sg/datasets/d_3c62d5eed03c40aeafbb6d0fa324e976/view);
  [M015661](https://tablebuilder.singstat.gov.sg/table/TS/M015661);
  [GDP year-on-year, quarterly, data.gov.sg](https://data.gov.sg/datasets/d_a5ff719648a0e6d4b4c623ee383ab686/view);
  [CPI 2024 base, M213751](https://tablebuilder.singstat.gov.sg/table/TS/M213751);
  [TableBuilder developer API](https://tablebuilder.singstat.gov.sg/view-api/for-developers).
- World view: [HKMA, How does the LERS work?](https://www.hkma.gov.hk/eng/key-functions/money/linked-exchange-rate-system/how-does-the-lers-work/);
  [BOJ, outline of foreign exchange intervention](https://www.boj.or.jp/en/intl_finance/outline/expkainyu.htm);
  [MOF, foreign exchange intervention operations](https://www.mof.go.jp/english/policy/international_policy/reference/feio/index.html);
  [BNM, milestones in the foreign exchange market](https://www.bnm.gov.my/significant-milestones-in-the-malaysian-foreign-exchange-market);
  [PBOC spokesman on the 2005 reform](https://www.pbc.gov.cn/english/130721/2025080815062860021/index.html).
