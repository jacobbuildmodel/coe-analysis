# THESIS ADDENDUM -- sgd piece

THESIS.md is sealed at 9e46034 (3 October 2026, SGT) and never edited again.
Every change after the seal is listed here, dated, with the md5 of each file
before and after. Nothing here changes a rule, a threshold, a window, the
MPS coding or a score.

## 1. 13_results.py: RESULTS.md layout for Checkpoint 1 (3 October 2026, before the data key)

Presentation only, written before `sgd/SEALED` existed and before any real
value was read.

- **Layout.**
  - A failures-first list at the top.
  - Gate C next, with its sealed wording, the correlation and the number of
    monthly changes.
  - The five scored tests, failures first, each with its sealed wording
    verbatim, its numbers, a line saying whether THESIS defines an interval,
    the outcome label and Jacob's confidence.
  - The scorecard: held against the expected count (2.68 if all five are
    scored), and the Brier score.
  - The verdict as section 8 fixes it. Beside Part A's ringgit and Part B
    it carries the "Weak evidence, stated now." bullets of T3 and T7,
    quoted from THESIS at run time.
  - The sealed sensitivities, marked NOT SCORED.
- **Removed:** the hand-written short form of T7's weak-evidence sentence,
  replaced by the verbatim quotation.
- **Computation:** none changed. It reads `out/tests.csv` and
  `out/sensitivities.csv` as before.
- **md5:** f35f7add0fe2a6877d9fdcf93af39daa -> 66ebecd0c414b713b8ab12008fdaea63
- **Tests:** the synthetic suite passes (20 tests).

## 2. 12_figures.py: titles, captions and muting for Checkpoint 1 (3 October 2026, before the data key)

Presentation only, written before `sgd/SEALED` existed and before any real
value was read.

- **Titles state the finding,** chosen by fixed rules from the sealed
  outcomes in `out/tests.csv`:
  - `title1`: one clause each for the yen and the ringgit (the partner's own
    fall did most of the work; the Singapore dollar's own rise did; neither
    did; the Singapore dollar did not rise; the split did not close).
  - `title2`: steadiest or second steadiest of N; ranked K-th of N;
    steadier than only K of the others, or least steady; not read when gate
    C failed.
  - `title3`: followed MAS's decisions more closely than growth; growth at
    least as closely; only a little more closely; not read.
- **Captions** now begin "How to read" and say what each mark is.
- **Muting.** Anything a failed gate or a test not scored makes unreadable
  is drawn at 0.35 opacity, and the caption says so:
  - chart 1: the currency whose share test was not scored;
  - chart 2: the ranking, when T4 is not scored;
  - chart 3: the path and the decision ticks, when T7 is not scored.
- **Heights** allow for titles that wrap; two charts lose spare space at
  the bottom.
- **Checks.** All 24 fixture charts (eight outcome fixtures) pass
  `tools/check_figure_overflow.py`, which includes the bold face. LF line
  endings. Rendered at 390 px and 1280 px in light and dark mode and looked
  at.
- **Computation:** none changed.
- **md5:** 63dc2b90f5db6b62a3ce9c358782036a -> 5f5f848f70bbf4b240f7523b36ca9f44
- **Tests:** the synthetic suite passes (20 tests).

## 3. Opening the data (3 October 2026): no fix was needed

- **The key.** `sgd/SEALED` was created in 59789e4, a commit of its own,
  after items 1 and 2.
- **The run.** `sgd/run_all.sh` read every real file with the scripts as
  sealed and as amended by items 1 and 2. No change was needed to read the
  real data. No rule, threshold, window, coding row or script changed after
  the key.
- **The only stop was by design.** The first real run stopped at
  `14_manifest.py --check`, because `CHECKSUMS.md5` and
  `number_manifest.csv` did not exist yet. They are written by hand, last
  (`python3 sgd/14_manifest.py`), and the second run verified them.
- **Results** are in 1e14611 (`RESULTS.md`, `out/`, `figs/`, the number
  manifest and the checksums).
- **One presentation note, not changed after the key.** The sensitivity
  table in `RESULTS.md` prints integer counts (intervals, ranks) with four
  decimals, for example 61.0000. The values are exact.
- **One reading note on the "real indices" sensitivity.** It sets the BIS
  real broad indices against the nominal cross rate, since BIS publishes no
  real bilateral rate. Its residual therefore absorbs the inflation
  differentials. It is context only, as THESIS section 7 says.

## 4. 12_figures.py: charts 1 and 3 for the answer article (3 October 2026, after the data was opened)

Presentation only. No computation, rule, threshold, window, coding row or
score changed. The title rules of item 2 are unchanged.

- **Chart 1** shows moves in per cent, not shares. For each currency it draws
  three bars, each 100 x (exp(log change) - 1) of a change already in
  `out/tests.csv`: the Singapore dollar against everyone, the partner against
  everyone, and the Singapore dollar against the partner. Right of the zero
  line is a rise, so the ringgit's rise against everyone is drawn as a rise.
  The shares stay in the text and in `RESULTS.md`.
- **Chart 3** gains growth. Below the index and the MAS decision strip, a
  second panel draws GDP growth over each stretch between decisions, on the
  same intervals T7 scored (`out/intervals.csv`, column g). The decision ticks
  are taller and labelled "MAS". There are at most three tick intervals per
  axis, so the ticks stay readable at 390 px.
- **Captions** of both still begin "How to read" and now say what each panel
  and colour is.
- **Checks.** The three real charts and all 24 fixture charts (eight outcome
  fixtures) pass `tools/check_figure_overflow.py`, bold included. Rendered at
  390 px and 1280 px in light and dark mode and looked at.
- **md5:** 5f5f848f70bbf4b240f7523b36ca9f44 -> c5f61ff717eb1023160d21820ca02f58
- **Tests:** the synthetic suite passes.

## 5. The article's numbers: 11b_postresults.py and the article check (3 October 2026, after the data was opened)

Machinery only, not scored. No computation of a scored number, rule,
threshold, window, coding row or score changed.

- **New script, `11b_postresults.py`.** It writes `out/postresults.csv`, the
  numbers the article prints, each derived from `out/` with its meaning:
  - the specimen: MAS's monthly average rate, S$ per 100 yen, for January
    2021 and December 2025, and the yen that a S$1,000 budget bought at each
    (to the nearest 1,000);
  - every move in per cent, 100 x (exp(log change) - 1), never typed by hand;
  - the shares in per cent;
  - rounded forms of tested numbers, each beside its unrounded source key;
  - the CPI sensitivity of T7 to two decimals;
  - Jacob's confidences in per cent.
  - md5: (new) 436f2967fba5a64fd8cfb44cec169dee
- **`14_manifest.py`.** It adds those rows to `number_manifest.csv` with
  their script. It lists `11b_postresults.py`, `THESIS_ADDENDUM.md` and the
  article among the inputs. `--check` now also checks the article. Every
  number in it must be a manifest value as printed, or a listed sealed
  constant (THESIS lines, the 64-economy basket, the Hong Kong band, the
  trip budget, the 0.25 coin-flip Brier score), a small integer or a year.
  The front matter's test counts must match the scorecard, and its seal
  date must match the seal.
  - md5: cbf89d662a0d9f95dedaa87120f192b6 -> 45408a7f0fe63f0b152bec162a853d6f
- **`13_results.py`.** It prints the post-results rows in a table marked NOT
  SCORED, so every manifest value appears in `RESULTS.md`.
  - md5: 66ebecd0c414b713b8ab12008fdaea63 -> 0554f69be0c8ccec930d07a13d315ef9
- **`run_all.sh`.** It runs `11b_postresults.py` after step 11.
  - md5: 17005d2a75d4818c1c0be59509e82970 -> abe15c405be256ed53386bfbc27c6105
- **`tests/test_pipeline.py`.** The end-to-end fixture run includes step 11b.
  - md5: 8496283a9a9ec871e0e247ea050a5311 -> db3c95c08109f0f68176d082a24055aa
- **Tests:** the synthetic suite passes.

## 6. 12_figures.py: chart 1's third bar and caption (4 October 2026)

Presentation only. No computation, rule, threshold, window, coding row,
title rule or score changed. Charts 2 and 3 are unchanged.

- **The third bar is outlined.** "Singapore dollar vs yen" and "vs ringgit"
  were drawn in the ink-3 grey, which is nearly the context grey in light
  mode and slightly lighter than it in dark mode. So the caption's "Dark"
  was false in dark mode, and the two partner bars looked alike. The bar is now outlined in the ink colour
  with an empty fill, which reads the same in light and dark mode.
- **The caption names each bar by its label,** with its colour or outline:
  blue, grey, outlined. "Grey: the other currency against all of its own"
  now reads "against its own trading partners". A sentence was added: the two
  moves multiply rather than add, and a small remainder neither index
  explains makes up the difference.
- **The cross-rate label has one decimal,** as the article prints it ("up
  49.5%"). A whole number drops its ".0" ("up 5%"). The other bars stay whole,
  as in the text.
- **Checks.** The three real charts and all 24 fixture charts pass
  `tools/check_figure_overflow.py`, bold included. Rendered at 390 px and
  1280 px in light and dark mode and looked at.
- **md5, 12_figures.py:** c5f61ff717eb1023160d21820ca02f58 -> 153f2dce250de868f726f5e6546585eb
- **md5, figs/sgd_chart1_split.svg:** 3381c6149eac382817b411487eda4c11 -> 8aac7d8c7d81a6021b6cda983c7c838e

## 7. 12_figures.py: a title and a description in each chart, for screen readers (4 October 2026)

Presentation only. No computation, rule, threshold, window, coding row,
title rule or score changed, and no visible text changed: each SVG's body,
everything after the new elements, is byte-for-byte as before.

- **What was added.** Each of the three SVGs now has a `<title>` (its
  finding title, as drawn) and a `<desc>` (its how-to-read caption, as
  drawn) as its first two children. The root has `role="img"` and
  `aria-labelledby` pointing at both. The ids carry the chart's name
  (`sgd-chart1-title` and so on), so they stay unique when the charts sit
  on one page.
- **What was removed.** The old `aria-label` alt strings. `aria-labelledby`
  replaces them.
- **Checks.** The three real charts and all 24 fixture charts pass
  `tools/check_figure_overflow.py`, bold included. Each SVG parses as XML,
  with `title` and `desc` first.
- **md5, 12_figures.py:** 153f2dce250de868f726f5e6546585eb -> fa2583a5cd8821df7d12f61b8febecc8
- **md5, figs/sgd_chart1_split.svg:** 8aac7d8c7d81a6021b6cda983c7c838e -> aff30e6b87da39568d4c902b554e4f87
- **md5, figs/sgd_chart2_steady.svg:** 52eea1ce317096ffba5ee252021aef20 -> 1bbf1c4e5eb9568b07cf43f7473ac08e
- **md5, figs/sgd_chart3_path.svg:** f759a95c9496db7c1a54f3b297d58b76 -> cf9d81a104932771e93eb60f6dfe9ae7

## 8. The researchers' page and its number check (4 October 2026)

Machinery and a new page, not scored. No computation, rule, threshold,
window, coding row or score changed.

- **New page, `FOR_RESEARCHERS.md`.** It sets out the derivation, every test
  with its sealed Survive and Fail lines, every sealed sensitivity, the
  design's limits, data provenance and how to rerun. It is listed among the
  checksum inputs. The article links to it in one line before its Sources.
- **`14_manifest.py`.**
  - The sealed sensitivities (`out/sensitivities.csv`) join the number
    manifest as `sens_*` rows, printed as `RESULTS.md` prints them: counts
    and ranks whole, everything else to four decimals.
  - `--check` checks every number in `FOR_RESEARCHERS.md` as it does the
    article's. The front-matter test counts are checked for the article
    only.
  - Before numbers are read, the check also removes:
    - commit and md5 hashes;
    - script names such as `14_manifest.py`;
    - a closing "References" section, since bibliographic volumes and pages
      are not results.
  - New allowed constants, all sealed in THESIS:
    - the T1 and T2 lines (0.005, 0.50);
    - months in a year for y_i (12);
    - T7's reasoning for its line (59, 0.13);
    - the bootstrap's draws and seed (10,000; 20260929).
  - md5: 45408a7f0fe63f0b152bec162a853d6f -> 97a3d014fd064e8cde419e5709eff24b
- **Check of the check.** Changing one printed value on the page (rho_p
  0.4653 to 0.4654) makes `--check` fail, naming the number.
- **Tests:** the synthetic suite passes.

## 9. 12_figures.py: chart wording from the Editor's chart review (4 October 2026)

Presentation only, every change made in `12_figures.py` and no SVG edited
by hand. No computation, rule, threshold, window, coding row or score
changed, and no article text changed. The article's alt texts do not quote
the chart titles, so none needed a change.

- **Chart 1, title.** One short clause per currency. The branch that
  occurred (T2 SURVIVE, T3 FAIL) reads "Yen: mostly the yen's own fall.
  Ringgit: mostly the Singapore dollar's own rise." The other branches keep
  their rules in the same short form:
  - "<Currency>: neither side did most" (INCONCLUSIVE);
  - "<Currency>: the Singapore dollar did not rise" (premise failed);
  - "<Currency>: the split did not close" (T1 failed).
- **Chart 1, caption.** "The moves compound rather than add, and a
  remainder that neither "vs all" move explains makes up the difference."
  "Small" was dropped, since the ringgit's remainder was 17 per cent of its
  move. "Compound" replaces "multiply", since the partner's fall divides.
- **Chart 2, title.** On the rank-1 branch, when the Hong Kong dollar is in
  the set: "The Singapore dollar was steadier than all ten others, Hong
  Kong's peg included". Other branches are unchanged.
- **Chart 2, caption.** It now reads: "each bar is how much a currency's
  value against all its trading partners typically moved in a month".
- **Chart 2, value labels** on the Singapore dollar, Hong Kong dollar and
  yen bars, at each bar's end in chart 1's label style. They are read as
  printed from `out/postresults.csv` (`T4_<AREA>_sd_pct`), so each is a row
  of `number_manifest.csv`. The plot's right edge moved in by 46 px to
  leave room for a label on the longest bar.
- **Chart 3, caption.** The middle and last sentences now say what the strip
  draws: p_i, MAS's setting after each decision. A dot is a band held flat
  (p_i = 0), not "no change". The last sentence says what the test asked.
- **Chart 3, a conditional last sentence.** "Inflation, not drawn, lined up
  with the path about as well as MAS's decisions did." It is added only when
  the sealed CPI sensitivity's D, read from `out/sensitivities.csv`, is 0 or
  less. On the real data it is -0.0421, so the sentence is drawn.
- **Checks.** The three real charts and all 24 fixture charts pass
  `tools/check_figure_overflow.py`, bold included, after rebuilding each
  fixture's `out/postresults.csv`. Rendered at 390 px and 1280 px in light
  and dark mode and looked at.
- **md5, 12_figures.py:** fa2583a5cd8821df7d12f61b8febecc8 -> 4c63044358ccd53dc6720ff6452e18f8
- **md5, figs/sgd_chart1_split.svg:** aff30e6b87da39568d4c902b554e4f87 -> 11a36cebf01e23ed484f29a14a8aee90
- **md5, figs/sgd_chart2_steady.svg:** 1bbf1c4e5eb9568b07cf43f7473ac08e -> 77f2ea041862e4ddbbde9c9d154eb74c
- **md5, figs/sgd_chart3_path.svg:** cf9d81a104932771e93eb60f6dfe9ae7 -> da66e8cbfa2a72a3e65d25013e614968

## 10. After outside review (10 October 2026): added after outside review, not sealed

Four outside readers read the piece in two rounds:
- round 4: a lecturer and an economics faculty member (reviewers 1 and 2);
- round 5: a reader with no economics training and a reader who works in
  currency markets (readers 3 and 4).

Reviewers 1 and 2 confirmed the arithmetic and asked for the meaning to be
tightened. Readers 3 and 4 also confirmed it: 78,125 and 120,482 yen;
31 + 73 - 4 = 100; 2.68; 0.136.

Every change below was **added after outside review, not sealed**, and none
is scored. No sealed number, outcome, threshold or verdict-rule wording
changed.

The round-4 brief relayed the reviewers' comments as asks A1-A5, article items
1-8 and the FOR_RESEARCHERS section. Each line cites the brief's label for the
comment it answers. Reviewers 1 and 2 raised the same points; the brief
consolidated them, so asks are not split by reviewer.

**Analyses (new script `16_review.py`, outputs `out/review_*.csv`, every
printed number in `number_manifest.csv`):**

- **A1, the US dollar as numeraire (an exact identity).** Answers ask A1. It
  confirmed the checker's 2021-25 figures: SGD up 2.7%, JPY down 31.3%
  (shares 7/93), MYR down 2.1% (55/45).
- **A2, the ex-pair split, using raw/s1c period weights** (a first-order
  approximation for a chain-linked index). Answers ask A2.
- **A3, the real split of the yen cross, with Japan's CPI from BIS
  WS_LONG_CPI** (stats.bis.org). Answers ask A3. The long window was not
  computed, because Japan's series ends in July 2026.
- **A4, rolling five-year windows, and the new chart 4.** Answers ask A4. It
  corrected the checker's count to 39 of 46. The checker's 38 of 45 is the
  same count without the last window, which ends in August 2026.
- **A5, T7.** Answers ask A5:
  - (a) a moving-block bootstrap with blocks of 2, 4 and 8;
  - (b) growth and CPI inflation led by 1 and 2 quarters;
  - (c) the effective sample size.

**Data:**

- **`raw/s8_bis_long_cpi_jp_monthly.csv`, retrieved 10 October 2026** and
  recorded in `raw/RETRIEVED.txt` by an appended block. The sealed text above
  it is unchanged. Answers ask A3.
  - md5 (new): 7fcc997a6e726449913ff18adc2d2d6f
  - md5, RETRIEVED.txt: 8550c0cfcad82fe8771fc14ac4f9ef92 -> 11e68bd861c8fd882fda1213b8eb23b9

**Machinery:**

- **`16_review.py` (new).** It reuses `11_tests.py`'s sealed definitions and
  is guarded like 10 and 15. Answers asks A1-A5.
  - md5 (new): 7bd3e63dd228006118d5d9725b7c2459
- **`12_figures.py`: chart 4.** It has a rule-based finding title and a "How
  to read" caption, and is drawn only when the review outputs exist. Charts 1
  to 3 are unchanged. Answers ask A4.
  - md5: 4c63044358ccd53dc6720ff6452e18f8 -> f785232aed80b6b1ee343ef41fce830e
- **`13_results.py`.** It prints the review rows in a section marked
  "added after outside review, not sealed, NOT SCORED", so every manifest
  value appears in RESULTS.md. Answers the brief's number-check requirement.
  - md5: 0554f69be0c8ccec930d07a13d315ef9 -> c80b6111ee90e52ac6f3cd9be2a47a1b
- **`14_manifest.py`.** It adds the review rows to the manifest with
  `16_review.py` as their script, and lists `16_review.py`, raw/s1c and
  raw/s8 among the inputs. Answers the brief's number-check requirement.
  - md5: 97a3d014fd064e8cde419e5709eff24b -> db84e81dbbadddd9ec5261b00bf565b3
- **`run_all.sh`.** It runs `16_review.py` after step 11b and adds chart 4
  to the overflow check. Answers the brief's run_all requirement.
  - md5: abe15c405be256ed53386bfbc27c6105 -> 5eab55b06a53e558240daf5833538aec

**Article, `2026-11-14.md` (1,800 words before Sources):**

- **First screen and summary lead with the window result** (39 of 46
  five-year stretches; over two decades the Singapore dollar's own climb was
  larger). The title is kept. Answers article item 1.
- **"Who moved is not who benefits."** A Singaporean's dollar bought the full
  gain in yen, whichever currency moved. Answers article item 2.
- **The strength-or-steering either/or is replaced by a reaction-function
  paragraph, as theory context.** It quotes MAS's framework FAQ (raw/s5c) and
  cites Balassa (1964) and Samuelson (1964). Answers article item 3.
- **The verdict keeps the sealed sentence exactly.** It is followed by the
  inflation result: CPI in place of growth gives MAS's lead -0.04, and -0.01
  with inflation a quarter ahead (A5b). The weak parts are now a short list.
  Answers article item 4.
- **Renamed: "What failed, as I expected: the ringgit rose against
  everyone".** Answers article item 5.
- **Wording.** Answers article item 6:
  - log shares;
  - the summary's remainder;
  - "about 50% more yen";
  - "the yen's broad index fell 25 per cent";
  - single months give 54 per cent;
  - the specimen at S.278 and S/bin/bash.829, about 78,200 and 120,600 yen;
  - the ringgit's moves in per cent, with 254%/-171% moved to the
    researchers' page;
  - "Hong Kong's broad index";
  - the 11 currencies named;
  - "typical month" defined;
  - both 0.92 correlations on monthly changes;
  - the reason for the August 2005 start;
  - the finer coding's D 0.346;
  - what a rank correlation of 0.47 means.
- **New section "What it changes".** It answers QUESTION_RULES Rule 0 item 5
  (the decision test, added 5 October in the project's QUESTION_RULES; per
  Jacob's ruling (a) of round 5). Answers article item 7.
- **A1 in one sentence.** Answers article item 8.
- **To stay within 1,800 words, three passages were cut.** None of them is a
  number the article needs:
  - the January 2015 counter-example on chart 3;
  - "the strongest setting on the scale" clause;
  - the sentence on calibration.

**Researchers' page, `FOR_RESEARCHERS.md`:**

- **New section 10, "After outside review (not sealed)",** with A1-A5 in
  tables and the reasoning for each, and the ringgit's 254%/-171% explained.
  References are now section 11. Answers the brief's FOR_RESEARCHERS item.

**Checks.**

- The number check covers both files and every review output.
- All four real charts and all 32 fixture charts (eight fixtures, four charts
  each) pass `tools/check_figure_overflow.py`, bold included.
- Chart 4 was rendered at 390 px and 1280 px, light and dark, and looked at.
- The synthetic suite passes.

**Round 5 (10 October 2026): readers 3 and 4 and the checker's notes on round
4.** Added after outside review, not sealed. Round 4's fixes are kept and not
duplicated. Labels: Jacob's rulings (a)-(d), article items 1-13 and the
checker's notes 14-19 of the round-5 brief.

- **Rulings (a) and (b).** Done in the lines above: Rule 0 item 5, and the
  sentence on reviewer attribution.
- **Ruling (c).** RETRIEVED.txt gained a second appended block (the BoJ page,
  and a record that the Fed host was refused). It is additions only.
  - md5, RETRIEVED.txt: 11e68bd861c8fd882fda1213b8eb23b9 -> 04f77fc1cb1a8689a52281486f46caf1
- **Ruling (d).** "About 50% more yen" and "bought the full gain in yen" are
  kept. Item 18 below finishes the prices paragraph.
- **The specimen comes first, at S$1.28 and S$0.83.** "About 78,000" and
  "about 120,000" yen (1,000/0.83 x 100 = 120,482) replace round 4's 78,200
  and 120,600. Answers article item 1.
- **The opening gives "about 70%" and "about 30%, with a small remainder", in
  log terms.** Answers article item 2.
- **The ringgit paragraph is in plain words** ("That small gap is the whole
  5%"). 254%/-171% stay on the researchers' page only. Answers article item 3.
- **How the scoring works, in two sentences.** The tally scores each
  confidence, not the hit rate, and 2.68 is the five confidences added up.
  Answers article item 4.
- **"Monetary Authority of Singapore (MAS)" is spelled out at first use.**
  Answers article item 5.
- **The MAS path names the 2025 easings.** MAS reduced the slope in January
  and April 2025 (MPS_CODING rows 20250124 and 20250414, both "flatter").
  Answers article item 6.
- **Hong Kong.** The heading is now "steadier even than Hong Kong's dollar",
  with one clause on why: the peg is to the US dollar alone, while MAS manages
  against a basket. Answers article item 7.
- **Terms are defined before use.** "Both windows" is defined at bet 1, with
  the July 2005 reason. The 11 currencies and "typical month" were already
  defined in round 4 and are kept. Answers article item 8.
- **The long-window split states its remainder:** 57, 51 and -8. Answers
  article item 9.
- **One line of context on why the yen fell:** the gap between Japanese and
  US interest rates. Answers article item 10.
  - The Japan side cites the BoJ statement of 19 March 2024
    (`raw/s9_boj_mps_20240319.html`, new, md5
    60770f0b5154516bf37dbe987173197a).
  - The Federal Reserve host was refused by the session's network policy (403)
    and was not routed around, so the US side stays general and uncited.
- **USD/JPY from S2:** 105.9 to 154.1 (`review_a6_context.csv`). Answers
  article item 11.
- **The real effective yen, from S1b.** Its 2025 average, 72.5, was the
  second lowest of 32 full years since 1994; 2024 was lower, at 71.5, and the
  lowest months came in 2026. It is reported as "second lowest", not as the
  lowest. Answers article item 12.
- **"What to watch next" now says what would change the picture.** The
  replication page is not live on the site, so the next open question is not
  named; the line points to the open questions page. Answers article item 13.
- **The two-decade claim now says "against everyone".** Once, it adds that
  against the US dollar alone the order reverses (A1: 0.5737 against 0.4263).
  This applies in the summary, the second paragraph, the five-year section,
  "What it changes" and "Weaker than they read". Answers checker's note 14.
- **"Overlapping" five-year stretches.** One clause in the article (57 of 60
  months shared) and one sentence on the researchers' page, tied to A5(c).
  Answers checker's note 15.
- **The T7 range clause.** The 90% range "reaches below the pass line, so the
  lead is not clear of chance". This is description; the sealed outcome stands
  on the point estimate. Answers checker's note 16.
- **The single-month sentence is rewritten** ("Measured from single months at
  each end, the rise is 54 per cent; the tests average three months ..., which
  gives 49.5"). Answers checker's note 17.
- **The prices paragraph gives the traveller's figure.** Tokyo goods per
  Singapore dollar rose 32.1% (b - dln CPI_JP, new in `review_a3_real.csv`).
  It also says plainly that the real exchange rate rose more, 54.8%, because
  Singapore's prices rose faster. Answers checker's note 18.
- **Credit wording.** The institution is no longer named, here or on the
  researchers' page. Four outside readers are credited, with who confirmed
  the arithmetic. Answers checker's note 19.
- **`16_review.py`.** It adds the round-5 numbers: the specimen at two-decimal
  rates, the rounded shares, the long remainder, the traveller's figure, and
  the new `review_a6_context.csv` (USD/JPY and the real-yen rank). Answers
  article items 1, 2, 9, 11 and 12, and checker's note 18.
  - md5: 7bd3e63dd228006118d5d9725b7c2459 -> 3a64cd4205cb6df083d29ce14d7d792e
- **`14_manifest.py`.** raw/s9 joins the checksum inputs. Answers article item
  10 (every cited source is checksummed).
  - md5: db84e81dbbadddd9ec5261b00bf565b3 -> 9c17a563ed1d44010b649f425e3814ae
- **Length.** To stay within 1,800 words, "The extremes" was cut to one
  sentence first, as the brief allows. Other sentences were tightened, with
  the detail kept on the researchers' page (A6 and the A1 to A4 notes).

**Final touch (11 October 2026).** Added after outside review, not sealed;
wording only.

- **"The extremes" heading dropped.** Its one sentence is folded into the
  end of "The argument: strength, delivered through steering". Answers
  Jacob's ruling (c): a one-sentence section looked thin in the table of
  contents. Rulings (a), keep the uncited general line on US rates, and (b),
  keep /open/ until publication day, needed no change.
- **"What it changes", first sentence.** It names the half: "The evidence cut
  against reading the cheap yen as a sign of Singapore's strength". Answers
  Jacob's edit note: "the comfortable story's second half" made the reader
  work out which half.
- 1,794 words before Sources.

**Wording fix (11 October 2026).** Added after outside review, not sealed;
wording only.

- **"Yardstick" reworded (site Vale rule Site.Jargon).** Article line 94 now reads "depended on what it was measured against"; FOR_RESEARCHERS A1 heading reads "reference currency", and its notes read "reference" and "the choice of reference". No number changed. md5, 2026-11-14.md: f386b95af10efc3fd8100a95d75d42d9 -> 89fdd1eed106d42e3987fe4e6bb4b46f; FOR_RESEARCHERS.md: 06301df82da33d7c7a05dad19a442861 -> c13530cb0d61376ce4539fce9b40157d.

## 11. The results note, and the charts, keys and researchers' page brought into line with it (4 November 2026)

The article is now a short results note, published on 14 November 2026. It
passed a checker truth pass, a robustness table and a consequence check, a
wording review and two outside rounds; Jacob approved its title on 4
November. Everything below was added after outside review, is not sealed and
is not scored. No sealed file changed: THESIS.md (8acdcf79b52383b9cee21cdf2e973dc0),
SEAL_MANIFEST.md, 11_tests.py and `out/tests.csv` (8f311f1ec47b811824f84d36bdbf4801)
are as they were.

- **The article (commit 43ffe39, placed by the WEBSITE moderator).**
  `2026-11-14.md` is replaced by the approved results note r5, titled
  "2021-25: the yen fell further than the Singapore dollar rose". Not edited
  here.
  - md5: 89fdd1eed106d42e3987fe4e6bb4b46f -> 0ce617a8e34eca274fabaee98a34aace
- **`12_figures.py`, chart wording.** Presentation only; no SVG edited by
  hand. The cause-like "own" and the absolute "all" are gone from the chart
  wording. Chart 3 is unchanged.
  - Chart 1, title: "Yen: mostly the yen falling against its trading
    partners. Ringgit: mostly the Singapore dollar rising against its trading
    partners." (the SURVIVE and FAIL branches; the other branches unchanged).
  - Chart 1, caption: "the Singapore dollar against its trading partners (BIS
    broad index)" and "the other currency against its trading partners (BIS
    broad index)".
  - Chart 2, caption: "each bar is how much a currency's value against its
    trading partners (BIS broad index) typically moved in a month".
  - Chart 4, title: "In 39 of the 46 overlapping five-year stretches when the
    Singapore dollar gained on the yen, the yen's fall was the larger part".
  - Chart 4, legend: "Singapore dollar's rise", "Yen's fall".
  - Chart 4, caption: "The windows overlap: only four five-year stretches fit
    end to end without overlapping." (the count read from
    `A4_nonoverlap_windows`); "Blue: the Singapore dollar's rise against its
    trading partners ... Grey: the yen's fall against its trading partners".
  - md5: f785232aed80b6b1ee343ef41fce830e -> 0e6bfbcd1e103477553519836d574e0e
  - md5, figs/sgd_chart1_split.svg: 11a36cebf01e23ed484f29a14a8aee90 -> d8b45e0f37ade3fc670a64c3a77c2174
  - md5, figs/sgd_chart2_steady.svg: 77f2ea041862e4ddbbde9c9d154eb74c -> cd38477aa18b173ce9f0977db84dbee7
  - md5, figs/sgd_chart4_rolling.svg: 4911204aa8c3e4940980941e3389d1af -> 95106d29ae893bde595d615934ed149b
  - figs/sgd_chart3_path.svg unchanged: da66e8cbfa2a72a3e65d25013e614968
- **`16_review.py`.**
  - (a) The meaning of `A3_scored_JPY_tokyo_goods_pct` and `_pct0` is now
    "goods per Singapore dollar at Japan's national consumer prices (b - dln
    CPI_JP)". The key names stay; the values (32.1, 32) do not change.
  - (b) Four A4 keys: `A4_nonoverlap_windows` 4 (five-year windows that fit
    end to end, from August 2005: every 20th window), `A4_nonoverlap_rose` 2,
    `A4_nonoverlap_yen_larger` 2, `A4_yen_larger_runs` 3 (runs of consecutive
    windows in which the yen's fall was the larger part).
  - (c) `out/intervals.csv` is not rewritten. Recomputed from the committed
    file, rho_g is 0.1144, D 0.3509 and the finer-coding D 0.3443, against
    the sealed 0.1127, 0.3526 and 0.3460. Six decimals give the same 0.1144,
    0.3509 and 0.3443, so they change nothing. The cause: some interval means
    of growth that print alike differ in their last binary digit in the run
    (1.5999999999999999 against 1.6, for example), so the sealed run ranks
    them apart, while the printed file ties them. Only full precision (17
    significant digits) reproduces the sealed values, and because
    `16_review.py` reads this file for A5, it would move `A5_block4_lo` from
    0.09 to 0.10 and `A5_block8_lo` from 0.14 to 0.15. RESULTS values may not
    change, so the file stays as the sealed `11_tests.py` writes it, and the
    researchers' page says in one line why the third decimals come from
    unrounded values.
  - md5: 3a64cd4205cb6df083d29ce14d7d792e -> 9149d86e4aeb2374736a96abce3844cb
  - md5, out/review_a3_real.csv: fd3e6bc1f06654311818dcf7827af9ab -> 2aa52bd888d109004aea86cee92a28ec
  - md5, out/review_a4_rolling.csv: 98f3b4b97cc2b4c0319bba0b6d2d2f98 -> 5dd06ab6c87444548215ebfaa24b6e8e
  - out/intervals.csv unchanged: e174fe5c92264708b46bdbb0fe47bd3b
- **`RESULTS.md` and `number_manifest.csv`, regenerated.** RESULTS changes in
  the two A3 meanings and the four new A4 rows only; the manifest, which has
  no meaning column, in the four A4 rows only. No printed number changed.
  - md5, RESULTS.md: 6643d15edb50cc92eb0256152018604f -> 22807d6a6030d716c5b7d9fc17fbdb9a
  - md5, number_manifest.csv: 1e6ce6f42f0cc98310904c82ec1d237c -> 78639b4e53e997f7e0217a8170d3af54
- **`FOR_RESEARCHERS.md`.** The link text is the new title. Every sentence
  that ranked the two decades on one measure now says the long split ranks
  neither part (|R| 0.0782 is larger than the gap between S 0.5724 and P
  0.5058) and that the other yardsticks disagree with each other: without
  the other currency in each basket, S 0.5332, P 0.4924, R -0.0256, the
  Singapore dollar's part first; against the US dollar, 57 per cent against
  43, and on the sealed real indices, P 1.0349 against S 0.4740, the yen's
  part first (section 5, its sensitivity table, A1 and A4). The page prints
  the manifest's four-decimal values, not three-decimal forms, so that
  `14_manifest.py --check` verifies each one. "Own rise" and "own fall" now
  read "rise" and "fall against its trading partners" (and, in A1's
  US-dollar formula, "move" and "fall against the US dollar"). "Tokyo goods"
  now reads "goods at Japan's national consumer prices". A4 adds one
  sentence on the four non-overlapping windows and the three runs, and
  section 3 the one line on unrounded values. No number was removed.
  - md5: c13530cb0d61376ce4539fce9b40157d -> fbcba3b7b017378bb154d073b44c98ea
- **`CHECKSUMS.md5`**, regenerated last with `python3 sgd/14_manifest.py`.
  Before: 2eeb3399cd6bfa9ed9f6a3752aff5265. It records this file's md5, so
  its own after-md5, and this file's, are in the pull request, not here.
  THESIS_ADDENDUM.md before this item: 8d211a41ebc79d86ad95de8eaf8c0c6e.
- **Checks.** `bash sgd/run_all.sh`: the synthetic suite, steps 10 to 16, 56
  numbers and outcomes reproduced with 0 differing, the four real charts and
  the chart 1 to 3 fixtures of four outcome branches passing
  `tools/check_figure_overflow.py`, and `14_manifest.py --check` with every
  checksum and manifest number verified.

No sealed number, outcome, threshold or verdict-rule wording changed.
