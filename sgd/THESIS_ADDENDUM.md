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
