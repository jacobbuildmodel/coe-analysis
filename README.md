# COE analysis

Data and code behind two articles on Singapore's Certificate of Entitlement auction:

- **The COE quota went up 62%. Prices tripled anyway.**
- **Perfect COE timing is worth $1,840. Nobody has it.**

Running the scripts in the order below reproduces every figure in both articles, including
the four SVGs, from the raw file as downloaded. Nothing is hand-entered downstream of
`raw.csv`.

---

## The data

**Source:** COE Bidding Results / Prices, Land Transport Authority, published through data.gov.sg
**Dataset:** `d_69b3380ad7e51aff3a7dcc84eba52b8a`
**Page:** https://data.gov.sg/datasets/d_69b3380ad7e51aff3a7dcc84eba52b8a/view
**Retrieved:** 18 August 2026
**Coverage:** January 2010 to August 2026. 1,965 records, 393 bidding exercises per category.

`raw.csv` is that download, unmodified. Its MD5 is `7b68a001709821c71ece5b8ed209d4d3`.

**This is a fixed snapshot, not a live mirror.** The dataset was updated on 19 August 2026, the
day after this file was retrieved. Downloading it fresh today will not necessarily reproduce
the MD5 above, and that is the point: every figure in both articles was computed from this
exact file, so it is committed here rather than fetched at run time. To check the analysis
against newer data, download the current file separately and compare, rather than replacing
`raw.csv`.

Columns: `month`, `bidding_no` (1 or 2), `vehicle_class` (Category A to E), `quota`,
`bids_success`, `bids_received`, `premium`.

Categories: A is smaller cars, B is larger and more powerful cars, C is goods vehicles and
buses, D is motorcycles, E is "Open" and usable for any vehicle, which in practice means it
gets bid up for large cars and arbitrages against B.

Licence and attribution are in `DATA_LICENCE.md`. Reuse of the raw file is subject to those
terms.

### Two corrections applied to the source file

Both were found by internal consistency checks and then verified against an independently
published result for the same bidding day before being changed. Both are values copied from
the row above.

| Where | LTA publishes | Corrected to | Why |
|---|---|---|---|
| 2010-01 exercise 2, Category D premium | 20,090 | **852** | Identical to Category C's premium in the same exercise. Motorcycle premiums either side were 889 and 852. |
| 2010-02 exercise 1, Category B quota | 1,154 | **693** | Identical to Category A's quota in the same exercise, and about 1.7 times Category B's neighbours. Produces the file's only exercise with fewer bids than certificates, which cannot happen above a reserve price. |

`02_clean.py` asserts the original wrong values, so it fails loudly if LTA ever fixes the
source file. If that assertion fires, the corrections are no longer needed and the article
text about them needs updating.

Five untouched records were spot-checked against published figures and match exactly:
2023-10 exercise 2 Category E at 158,004; 2025-09 exercise 2 Category A at 119,003;
2025-11 exercise 1 Category A at 110,002; 2010-02 exercise 1 Category A at 19,989; and the
corrected 2010-01 Category D at 852.

### One loading trap

`bids_success` and `bids_received` contain thousands separators in later rows, which silently
loads those columns as strings. `02_clean.py` strips the commas before coercing. Anyone
rebuilding this from scratch will hit it.

---

## Running it

```
pip install -r requirements.txt
bash run_all.sh
```

Or one at a time, in this order. Every script reads and writes in the working directory.

| Script | What it does | Reads | Writes |
|---|---|---|---|
| `01_explore.py` | Data quality pass. This is what found the two errors. Diagnostic only; `clean.csv` is a dead end that nothing downstream uses. | `raw.csv` | `clean.csv` |
| `02_clean.py` | Applies both corrections with assertions, strips thousands separators, builds logs and first differences | `raw.csv` | `analysis.csv` |
| `03_regress.py` | Four specifications from naive to defensible, the Category A against B test, era stability | `analysis.csv` | stdout |
| `04_decompose.py` | Splits the 2010 to 2026 price rise into the part quota explains and the residual. Policy arithmetic. | `analysis.csv` | stdout |
| `05_chartdata.py` | Chart data prep for an earlier exploratory viewer. Not used by the published figures. | `analysis.csv` | `chartdata.json` |
| `06_ev.py` | Event study on the May 2022 EV reclassification, plus placebo tests at fake break dates | `analysis.csv` | stdout |
| `07_av_benchmark.py` | Converts the estimated slope into the demand shift an autonomous-vehicle scenario would need | `analysis.csv` | stdout |
| `08_bidding_round.py` | First against second bidding exercise within a month. Fifteen sections including a drift test, a simulation placebo and an out-of-sample rule test. | `analysis.csv` | stdout |
| `09_figures.py` | Builds all four published SVGs | `analysis.csv` | `figs/*.svg` |
| `10_deregistration.py` | Whether the quota is exogenous. Variance decomposition, lagged-price tests, quarter fixed effects, and a bound on how large the bias would have to be. | `analysis.csv` | stdout |

`02` must run before anything numbered higher. `03` through `10` are independent of each
other and can run in any order.

### Checking your reproduction

| File | MD5 |
|---|---|
| `raw.csv` | `7b68a001709821c71ece5b8ed209d4d3` |
| `analysis.csv` | `4480189cd99b4514885185843ac5f2cc` |

If `analysis.csv` matches, everything downstream will. The four SVGs in `figs/` are also
committed, so a rebuild can be diffed against them directly.

### Environment

Verified on Python 3.11.15 with pandas 3.0.2, numpy 2.4.4, statsmodels 0.14.6 and scipy
1.17.1. Nothing here uses a recent API, so older versions of pandas and statsmodels should
work. Only `08_bidding_round.py` needs scipy, for one binomial test.

---

## The headline results

Preferred specification is `ln(premium) ~ ln(quota) + C(year)` with Newey-West standard
errors at 8 lags, which is about four months at two exercises a month. Beta is the percentage
change in premium per 1% change in quota.

| Category | beta | 95% CI |
|---|---|---|
| A smaller cars | **-0.304** | [-0.440, -0.169] |
| B larger cars | **-0.432** | [-0.676, -0.189] |
| C goods vehicles | -0.132 | [-0.179, -0.084] |
| D motorcycles | -0.703 | [-0.935, -0.472] |
| E open | -0.384 | [-0.573, -0.195] |

Report beta rather than the implied elasticity. The reciprocal is unstable when beta is
small: one first-difference run produced a confidence interval from -162 to -2.7, which is
not a measurement of anything.

The decomposition, Category A, 2010 to 2026: quota up 62%, premium up 287%, and the quota
change alone predicts a fall of 13.6%. Cutting premiums 10% would take about 41% more
certificates, or closer to 99% under the quarter fixed-effects specification in `10`.

Fuller write-ups of what was tested, including the tests that found nothing, are in `notes/`.

---

## What is deliberately not here

**Working drafts and outlines.** Superseded by the published articles. A draft with known
errors sitting beside the corrected version only creates ambiguity about which is
authoritative.

**`figures.html`.** An early interactive viewer that consumes `chartdata.json`. It is not
produced by any script here, so including it would break the claim that running these in
order reproduces everything. `05_chartdata.py` is kept because it is part of the numbered
sequence, but nothing published depends on it.

**Generated intermediates.** `clean.csv` and `chartdata.json` are gitignored. They are
outputs, not inputs.

**Project planning notes.** Not part of the analysis.

---

## What this analysis does not do

It does not measure demand. It measures what supply explains and calls the remainder demand.
A residual has a size and it has contents, and measuring the first is not measuring the
second. Incomes, population, credit conditions, foreign buyers, changing preferences and
omissions all sit inside it together, and this data cannot separate them.

The relationship is not stable across time. Estimated within each era, beta is -0.59 in
2010 to 2013, -0.23 in 2014 to 2019, -0.43 in 2020 to 2022, and +0.14 in 2023 to 2026. The
last of those cannot be distinguished from zero, at p = 0.25.

Category E can be used for any vehicle, which links it to A and B through arbitrage.
Treating the five categories as five independent markets overstates the precision of these
estimates.

`notes/FINDINGS_EXOGENEITY.md` covers the strongest objection, which is that the quota is
built from deregistrations and deregistration responds to price.
