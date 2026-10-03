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
