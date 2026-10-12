# EXPOSURE -- every series and statistic looked at for this note

A later sealed Category A/B piece will not test anything described in this note, and will
disclose this log. Entries are dated (SGT) and say exactly what was seen: whole series, a
few rows, or labels only.

## Before this note (earlier pieces in this repo; prior exposure, already published or merged)

- **22-29 Aug 2026, root COE pieces** (`notes/FINDINGS*.md`, articles dated 22 and 29 Aug).
  - Seen: Category A and B premiums and quotas 2010-2026 from `raw.csv`.
  - Computed:
    - A vs B demand elasticity with an A/B interaction;
    - the elasticity by era for A and B;
    - the A-B and E arbitrage noted as a caveat;
    - the quota and premium paths.
- **5 Sep 2026, win rate** (`win-rate/`). Category A bids received against successful bids,
  by exercise.
- **12 Sep 2026, motorcycles** (`motorcycles/`). Category D against car categories,
  including A and B premium levels.
- **26 Sep - 10 Oct 2026, ERP piece** (`erp/`). e4b opened after its seal. The annual mean of
  the A and B quota premiums was used (THESIS section 4), cross-checked against `raw.csv`.

## Checkpoint 0, 11 Oct 2026 (this note)

| Time (SGT) | What | Exactly what was seen |
|---|---|---|
| 11 Oct, about 16:00 | `raw.csv` | Header; first 4 rows (2010-01 exercise 1, Cat A-D: quota, bids, premium); last 3 rows (2026-08 exercise 1, Cat C, D, E); md5 |
| 11 Oct, about 16:00 | `clean.csv` | Header and first 2 rows (2010-01 exercises 1-2, Cat A) |
| 11 Oct, about 16:00 | `README.md` | Coverage statement (2010-01 to 2026-08, 1,965 records) and the two documented corrections |
| 11 Oct, about 16:00 | `erp/raw/e4b_quota_premium_monthly.csv` | Header (months) and all 50 series labels. **Full rows printed by accident:** "Total Quota, 1st Bidding", "Total Successful Bids, 1st Bidding" (2002-02 to 2026-08), "Open Category, Bids Received, 2nd Bidding" and **"Open Category, Quota Premium, 2nd Bidding"** (2002-02 to 2026-08). The last bears on F4 (Q5). No A, B or PQP row was printed |
| 11 Oct, about 16:00 | `erp/raw/RETRIEVED.txt`, `erp/office/SOURCES_REPORT.md`, `erp/THESIS.md` | e4b provenance and definitions only |
| 11 Oct, about 16:00 | `notes/FINDINGS.md` (lines on A/B) | Era table of A and B elasticities; caveat on E arbitrage (already known, see above) |
| 11 Oct, 16:11 | LTA release, para 3 | LTA's statistic: Category A above Category B "on three occasions", February to June 2026 |
| 11 Oct, 16:11 | Annex C | Illustrative OMVs only ($31,000-$38,000, median $34,000, "for illustrative purposes only") |
| 11 Oct, about 16:15 | Web search snippets (press, secondary) | Band examples attributed to the unretrieved paper: a $15,000 rebate or surcharge, a 0-35th / 35th-50th / above-50th percentile three-band example, bands based on 2025 registrations. UNVERIFIED, not used |
| 11 Oct, about 16:20 | data.gov.sg metadata (2 datasets) | Last-updated dates and coverage only; no values |

No statistic was computed at Checkpoint 0.

## Checkpoint 1, 11 Oct 2026 (the note itself)

Everything in `out/` was computed and looked at for this note. A later sealed A/B piece
treats all of it as exposed:
- the B-A premium gap per exercise, 2010-01 to 2026-10 exercise 1, and its summaries;
- every exercise with A above B;
- the monthly PQP for A and B, and their gap, 2010-01 to 2026-10;
- the A, B and E quota shares;
- the E-B premium gap;
- the cross-checks.

| Time (SGT) | What | Exactly what was seen |
|---|---|---|
| 11 Oct, about 18:00 | `raw/coe-public-consult.pdf` | Full text. Its only data: the three occasions (1.8); 2025 OMV percentile bands and typical models (Tables 1-2); the 2025 bid clustering (3.12); multiple-car households (3.19) |
| 11 Oct, about 18:15 | Web search snippets (secondary, not used) | October 2026 exercise 1 premiums for A and B; the PQP for A and B in September and October 2026; a press summary of the 9 and 23 September results |
| 11 Oct, 18:21 | `raw/d3_lta_m11_coe_results_2025_2026.pdf` | **Printed by accident while checking the layout:** January 2026 exercise 1-2 values for all categories (quota, bids, premiums), and every "PQP for <month>" row, February 2025 to October 2026, for A, B, C and D |
| 11 Oct, 18:2x-19:xx | `out/*.csv`, `figs/*.svg` | All of the above, computed by `10_facts.py`, read in full while drafting NOTE.md |

## Checker's rulings of 12 Oct 2026 (outside reader's review)

All computed by `10_facts.py` and seen while revising NOTE.md and FORM_TEXT.md:
- every statistic for the four fixed windows: since January 2010, since May 2022 exercise 1,
  the last 12 months and the latest exercise or month;
- the median of (B-A)/A per exercise, overall and by calendar year;
- the median absolute 6- and 12-month change in the B-A gap.
The window-2 start comes from LTA's news release of 14 Apr 2022 (raw/c2b_...).
