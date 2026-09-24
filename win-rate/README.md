# win-rate

Data and code behind **"Two in three COE bidders win. It is not a lottery."**

## Why this is a subdirectory rather than its own repository

Same source file, same two corrections, same cleaning step. Copying `raw.csv` into a second
repository would create two copies of a file that must stay identical, and the moment LTA
changes something upstream they would drift apart. One raw file, one cleaning script, many
analyses.

Script numbering continues from the parent rather than restarting at 01, so the run order
across the whole repository is unambiguous.

## The data

Inherited from the parent directory. Nothing here re-downloads or re-cleans anything.

**Source:** COE Bidding Results, Land Transport Authority, via data.gov.sg
**Dataset:** `d_69b3380ad7e51aff3a7dcc84eba52b8a`
**Page:** https://data.gov.sg/datasets/d_69b3380ad7e51aff3a7dcc84eba52b8a/view
**Retrieved:** 18 August 2026
**Licence:** Singapore Open Data Licence version 1.0. Attribution wording in
`../DATA_LICENCE.md`, and it applies to anything derived from the file, including the figure
here.

Two corrections are applied in `../02_clean.py` and documented in `../README.md`. Both were
verified against independently published results before being changed.

## Running it

From this directory, after the parent's `02_clean.py` has produced `../analysis.csv`:

```
python3 11_winrate.py     # all the numbers in the piece
python3 12_figures.py     # figs/winrate.svg, needs 11 to have run
python3 ../tools/check_figure_overflow.py figs/winrate.svg   # DejaVu Sans margin check
```

Or from the repository root:

```
bash run_all.sh                       # parent pipeline, builds analysis.csv
cd win-rate && python3 11_winrate.py && python3 12_figures.py
```

| Script | What it does | Reads | Writes |
|---|---|---|---|
| `11_winrate.py` | Win rates by category and year, how much price moves against how much the win rate moves, the correlation between the two, and the extreme exercises | `../analysis.csv` | stdout, `winrate_catA.csv` |
| `12_figures.py` | The one figure in the piece | `winrate_catA.csv` | `figs/winrate.svg` |

## Checking your reproduction

| File | MD5 |
|---|---|
| `../raw.csv` | `7b68a001709821c71ece5b8ed209d4d3` |
| `../analysis.csv` | `4480189cd99b4514885185843ac5f2cc` |
| `winrate_catA.csv` | `28c140661104ab9099f66bf73a0019df` |
| `figs/winrate.svg` | `f83012ca77825d4dac999f0ce3d79d31` |

`11_winrate.py` needs scipy, for one correlation test. Everything else is pandas and numpy.
Verified on Python 3.11.15 with pandas 3.0.2, numpy 2.4.4 and scipy 1.17.1.

`figs/winrate.svg`'s hash changed 24 September 2026: redrawn for legibility (Phase 3 shared
figure tokens, 480px canvas, 14px minimum text, DejaVu-Sans-safe margins) and to write LF
line endings on every platform. No data or reported value changed.

## The headline numbers

| | Category A |
|---|---|
| Share of bids that succeed, 2010 to 2026 | **67.1%** |
| Lowest year | 53.8% (2013) |
| Highest year | 75.0% (2017) |
| Win rate, highest year over lowest | 1.39x |
| Premium, highest year over lowest | 3.93x |
| Variation relative to mean: win rate | 8.4% |
| Variation relative to mean: premium | 42.5% |

By category, the share of bids that succeed: motorcycles 75.6%, larger cars 67.4%, smaller
cars 67.1%, goods vehicles 61.8%, open 59.5%.

## What the analysis does not settle

**These are bids, not bidders.** The file counts bids submitted, not people. Somebody who
fails and rebids appears more than once. The share of *people* who eventually obtain a
certificate is therefore higher than 67%, and nothing in this data says how much higher.

**The win rate is not perfectly flat.** It is weakly lower when premiums are high: the
correlation with log premium across all 393 Category A exercises is -0.15 with a p-value of
0.002. On annual means it is -0.33 with a p-value of 0.20. Section 3 of `11_winrate.py`
reports this for every category. Price does most of the rationing, not all of it.

**Most bids are placed by dealers.** A bid is not a clean count of one person wanting a car.
