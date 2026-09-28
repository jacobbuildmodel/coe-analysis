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
