# THESIS ADDENDUM: minimum wage or the Progressive Wage Model

THESIS.md was sealed on 28 September 2026 in commit e5f877b ("pwm: SEAL"),
md5 8d5beaf453f7310eb14aa0df9fd56a20, and is never edited. Every change made
after the seal is listed here, dated, with its reason. Nothing here is
applied to the scoring: the tests, thresholds, titles, windows, rungs and
confidences are those sealed.

## 1. 13_results.py: presentation of RESULTS.md (28 September 2026, before the data was opened)

- **What changed.** RESULTS.md now quotes each test's sealed wording
  verbatim (the Prediction, Survive if and Fail if lines, read from
  THESIS.md at run time), puts Jacob's confidence at seal beside each test,
  labels Part A and Part B of the verdict, prints the sealed T2 and T3 leans
  in THESIS's own words, states held against the expected count and the
  Brier score in one place, and marks every sensitivity row "not scored".
  It also says that THESIS fixes no interval for T3 and T5.
- **Why.** The Checkpoint 1 instructions ask for these in RESULTS.md; the
  sealed script printed the numbers but not the wording or the confidences
  beside them.
- **When.** Committed before `pwm/SEALED` was created, so before any real
  value was read (`10_load.py` and `15_reproduce.py` refuse `raw/` without
  it). Tested on the synthetic fixtures only.
- **md5.** `13_results.py`: sealed 3dce1abb26037126f53448a4f7b0f918, new
  5262d00cb9fa119795007810d9285e99.
- **No rule changed.** The files that compute, select or threshold are
  byte-identical to the seal: `pwmlib.py` e5f62fae032b53f0eafdca530360d923,
  `10_load.py` 069efc11c34920e7287188538edc7f85, `11_tests.py`
  813372c48e337720a6ca63b725313d8a, `15_reproduce.py`
  116fda301b8e49f9b0732266626e37a3, `14_manifest.py`
  a9a36c1ffde19085b6391a6bdcbf6b9e, `office/OCCUPATION_MAP.csv`
  10de6f3a90b4c8db26f0c18160aa9ba9. `13_results.py` reads `out/tests.csv`
  and prints it; every number still passes through `pwmlib.printed`, and
  `14_manifest.py --check` still requires each one to appear in RESULTS.md
  as printed.

## 2. 12_figures.py and run_all.sh: charts (28 September 2026, before the data was opened)

- **What changed.** The three charts are reordered and drawn to the
  Checkpoint 1 brief. Chart 1 (`figs/chart1_gap.svg`): the covered-minus-
  comparison gap by June for each covered group, with the pre-period,
  transition, excluded (2020-21) and post-period years shaded and labelled,
  and dashed before and after averages. Chart 2 (`figs/chart2_pace.svg`,
  was `chart3_pace.svg`): comparison jobs' bottom pay against the median,
  2009-2019, start and end windows shaded (T3). Chart 3
  (`figs/chart3_rung.svg`, was `chart2_rung.svg`): each group's bottom
  quarter against its entry rung by June, lines at 0.97 and 1.0 (T5). Every
  chart has a caption saying how to read it. Each title states the finding,
  chosen by a rule written into the script now, from the sealed outcome
  labels in `out/tests.csv` (for example, T2 SURVIVE gives "After the
  ladders, bottom pay in covered jobs pulled about N log points ahead").
  `run_all.sh` names the renamed files in its overflow check.
- **Why.** The Checkpoint 1 instructions set the chart order, the shading
  and labels, captions that explain how to read each chart, and titles that
  state the finding.
- **When.** Committed before `pwm/SEALED` was created, so before any real
  value was read. Tested on the synthetic fixtures only; rendered at 390 px
  and 1280 px, light and dark; `tools/check_figure_overflow.py` passes.
- **md5.** `12_figures.py`: sealed d5112e9748ef097b9f33e56958dd86b4, new
  e50f87db87f180b333a0736a27946863. `run_all.sh`: sealed
  e475040e845a57d190994f4becacb1c0, new 3c83f4fdad55532093f83424a870dd6b.
- **No rule changed.** The computation files are unchanged, with the same
  md5s as in item 1. `12_figures.py` reads `out/` only; `run_all.sh` changes
  only the two file names in the overflow-check line.

## 3. 12_figures.py: chart titles and chart 3 panels (28 September 2026, after the data was opened)

- **What changed.** Two presentation fixes, made after the real run:
  - The title rules of chart 1 and chart 3 said "covered jobs" and "the
    bottom quarter" without naming the groups. With T1 failing for cleaning
    and security, T2 and T5 were scored on landscape alone, so those titles
    overstated the finding. The rules now name the scored groups when T1
    drops some, and name the groups it dropped (chart 1: "Landscape: bottom
    pay pulled about 22 log points ahead. Cleaning and security failed the
    design test"; chart 3: "Landscape: in every scored June, the bottom
    quarter earned at least the entry rung").
  - Chart 3 drew empty panels for the groups T1 dropped. It now draws a
    panel only for each scored group and names the others in one line.
- **Why.** A title must not claim more than the scored tests show.
- **When.** After `pwm/SEALED`, so written with the results in view; it is
  listed here for that reason. It changes no number: the charts read the
  same `out/` files, and the figures in the titles (22 log points) are the
  sealed T2 estimate rounded.
- **md5.** `12_figures.py`: e50f87db87f180b333a0736a27946863 (item 2), new
  57b3c57f37ff4494ee593003892453f4.
- **No rule changed.** `pwmlib.py`, `10_load.py`, `11_tests.py`,
  `15_reproduce.py`, `14_manifest.py` and `office/OCCUPATION_MAP.csv` keep
  the md5s of the seal (item 1). No test, threshold, title list, window,
  rung or confidence changed.

## 4. tests/test_pipeline.py: the pre-seal guard test (28 September 2026, after the data was opened)

- **What changed.** `test_loader_refuses_real_raw_before_seal` asserted that
  `pwm/SEALED` did not exist, then checked that the loaders refuse the real
  `raw/`. Creating `pwm/SEALED` (commit dafb176) made that assertion false by
  design. The test is now skipped once `pwm/SEALED` exists, with the reason
  printed. `test_guard_logic` still checks the rule itself (refuse without
  the seal file, allow with it) on temporary paths.
- **Why.** The test described the state before the seal; after it, the
  loaders are meant to read `raw/`.
- **md5.** `tests/test_pipeline.py`: sealed 509ec2027efdd93ade688cc2479ae3c5,
  new e4954330163edccd95d28151f106008f.
- **No rule changed.** Only a test's precondition; no analysis script
  changed. The suite: 35 tests pass, 1 skipped.

## 5. Observation from the real run, reported, not applied (28 September 2026)

- **A drop inside a sensitivity that RESULTS.md does not list.** In June 2010
  the comparison cashier line (5230, "Cashiers and ticket clerk") has no
  basic-wage 25th percentile; its gross value is present. Under the sealed
  missing-year rule the "basic instead of gross" sensitivity therefore
  drops that one-June line (the cashier lineage keeps 42111 in 2009 and 52302
  from 2011). `11_tests.py` records the missing-year drops of the main
  series and of the all-successors sensitivity, not those made inside the
  other sensitivities, so RESULTS.md's "Titles dropped by the missing-year
  rule: None" describes the main series. The main series, every scored
  test and the verdict are unaffected. No script is changed for this.

## 6. 11b_postresults.py: post-results checks, NOT SCORED (28 September 2026, after the results)

A new script, run after `11_tests.py`; no sealed script computes differently.
It writes `out/postresults.csv`, which `14_manifest.py` adds to the number
manifest and `13_results.py` prints in its own section. md5
9b344428c0df19de0d1aaea351df01de.

- **A1. Landscape's pay gain net of its steepest sensitivity drift.** Of the
  sealed T1 sensitivities, the steepest landscape drift was 0.0118 a year
  (the Junes after the last pre-period classification break). Carried over
  the 7.5 years from the pre-period midpoint (mean of the Junes 2009-2014,
  2011.5) to the post-period midpoint (mean of 2017, 2018, 2019 and 2022,
  2019.0), it accounts for 0.0888. Landscape's T2 of 0.2201 net of that is
  0.1312, still above the 0.10 survive line. Not scored: T2 stays as sealed.
- **A2. T3 against the LFS median including employer CPF.** The sealed T3
  uses the median excluding employer CPF, because OWS gross wage excludes
  employer CPF too, so the two sides are like for like (THESIS T3, "the
  middle"). Against the median including employer CPF, the middle grew
  0.3089 and the shortfall is 0.0623, over the 0.05 line: T3 would fail on
  that measure. Not scored: T3 stays SURVIVE as sealed.
- **Per-cent equivalents**, 100 x (exp(x) - 1), of every log-point figure the
  article uses, the S$ levels behind the T5 ratios, Jacob's confidences in
  per cent, and the running record over the ERP and PWM pieces (4 of 8 held
  against 3.66 expected, Brier 0.205, from `erp/out/tests.csv` and
  `out/tests.csv`).

## 7. 12_figures.py: charts for readers (28 September 2026, after the results)

- **What changed.** Visible text only: values shown in per cent
  (100 x (exp(x) - 1) of the same log-point values in `out/`), no "log
  points", no test labels (T1, T2, T5), "transition" and "2020-21 excluded"
  for the bands (in two label rows so they do not collide), "failed the
  design test" for the dropped jobs, and titles that state the finding in
  plain words. Captions rewritten to match.
- **No number changed.** The charts read the same `out/` files; the
  overflow check passes, bold included; LF line endings.
- **md5.** `12_figures.py`: 57b3c57f37ff4494ee593003892453f4 (item 3), new
  6c340815bdeeafc2f9e2d2545077424a.

## 8. 13_results.py, 14_manifest.py, run_all.sh: the post-results checks and the article (28 September 2026)

- `run_all.sh` runs `11b_postresults.py` after `11_tests.py`. md5
  3c83f4fdad55532093f83424a870dd6b (item 2), new
  d167719adb1f98bc3ac1ad9c3b47c21e.
- `13_results.py` prints the post-results rows in a section marked not
  scored. md5 5262d00cb9fa119795007810d9285e99 (item 1), new
  a2086450c6d15b0e7a57b1e32131e1a2.
- `14_manifest.py` adds the post-results rows to the number manifest (script
  `11b_postresults.py`), lists `11b_postresults.py`, `THESIS_ADDENDUM.md` and
  the article among the checksummed inputs, and checks the article: every
  number it prints must be in the manifest, or be a year, a count up to 10,
  or a sealed constant (the entry rungs and LQS amounts, 97, 90, 25, and 0.25
  and 50 for the always-50-per-cent forecaster); the front matter must match
  the scorecard and the seal date. md5 a9a36c1ffde19085b6391a6bdcbf6b9e
  (sealed), new 6eae8b3350a866e6c67461d49d38c536.
- **No rule changed.** `pwmlib.py`, `10_load.py`, `11_tests.py`,
  `15_reproduce.py` and `office/OCCUPATION_MAP.csv` keep the md5s of the seal.
