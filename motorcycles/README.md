# motorcycles

Data and code behind **"Motorcycle COEs fell 17%. Car COEs rose 43%."**

Reads `../analysis.csv`, which `../02_clean.py` builds from `../raw.csv`. Nothing here
re-downloads or re-cleans anything, so the two source corrections exist in one place for the
whole repository. Script numbering continues from the parent.

## The data

**Source:** COE Bidding Results / Prices, Land Transport Authority, via data.gov.sg
**Dataset:** `d_69b3380ad7e51aff3a7dcc84eba52b8a`
**Page:** https://data.gov.sg/datasets/d_69b3380ad7e51aff3a7dcc84eba52b8a/view
**Retrieved:** 18 August 2026. Fixed snapshot; the dataset was updated on 19 August, so
a fresh download will not match the published checksums.
**Licence:** Singapore Open Data Licence version 1.0. Attribution wording in
`../DATA_LICENCE.md`, and it covers anything derived from the file, the figure included.

## Running it

```
python3 13_motorcycles.py    # every number in the piece
python3 14_figures.py        # figs/moto_vs_car.svg, needs 13 to have run
```

| Script | What it does | Reads | Writes |
|---|---|---|---|
| `13_motorcycles.py` | Each category against its own peak, a test of whether the motorcycle fall is noise, what quota and bids did in each category, and one mechanism that failed | `../analysis.csv` | stdout, `moto_vs_car.csv` |
| `14_figures.py` | The one figure in the piece | `moto_vs_car.csv` | `figs/moto_vs_car.svg` |

## Checking your reproduction

| File | MD5 |
|---|---|
| `../raw.csv` | `7b68a001709821c71ece5b8ed209d4d3` |
| `../analysis.csv` | `4480189cd99b4514885185843ac5f2cc` |
| `moto_vs_car.csv` | `ecd6316b5bc4b06e35142c42d83f4c3b` |
| `figs/moto_vs_car.svg` | `d18d1a5705f49d65a21923b1961518f3` |

Needs scipy for one t-test. Verified on Python 3.11.15 with pandas 3.0.2, numpy 2.4.4 and
scipy 1.17.1.

## The headline numbers

| | |
|---|---|
| Motorcycle premium, 2022 peak, 24 exercises | $10,945 |
| Motorcycle premium, 2025 and 2026, 39 exercises | $9,133 |
| Difference | $1,812, p below 0.0001 |
| Motorcycle premium against its own peak | -17% |
| Every car category against its own peak | within 2% |

Headline basis: 2022 against the 39 exercises since the start of 2025. That is the same
window as the significance test, and it avoids resting a ratio on the 15 exercises 2026 has
run so far.

| Category | Quota | Bids | Premium |
|---|---|---|---|
| A smaller cars | +125% | +149% | +43% |
| B larger cars | +59% | +67% | +20% |
| C goods vehicles | +221% | +139% | +29% |
| D motorcycles | +10% | -1% | -17% |
| E open | +39% | +58% | +19% |

**Sensitivity to the endpoint.** Against full-year 2025 alone, motorcycles are -18% and cars
+36%. Against the part year of 2026, -14% and +55%. The pooled basis sits between them, and
the part year understates the motorcycle fall while overstating the car rise, so the headline
is the conservative reading. `13_motorcycles.py` prints all three.

## What the analysis does not settle

**It is not a controlled comparison.** Categories differ in more than the number of bidders,
and nothing here holds those differences fixed. What the piece reports is what happened.

**Category C is a live counter-example.** Its quota grew faster than its bidding between 2022
and 2026 and the premium still rose 44%. Any mechanical reading of the table fails on that
row.

**One mechanism was tested and rejected.** Section 6 of `13_motorcycles.py` checks whether the
premium tracks bids per certificate. In levels every correlation is under 0.16. In first
differences it holds for categories A, B and D and cannot be distinguished from zero for C and
E. The tidy version of this story does not exist in the data, and the piece does not claim it.

**Why motorcycle bidding stopped growing is outside this file.** Licensing, delivery work and
the price of the bike itself are not in a COE bidding record.
