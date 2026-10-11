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
