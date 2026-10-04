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
