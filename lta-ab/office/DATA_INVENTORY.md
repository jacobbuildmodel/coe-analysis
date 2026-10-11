# DATA_INVENTORY -- what public data can and cannot show (Checkpoint 0, 11 Oct 2026)

Nothing has been computed for this note. Coverage and fields below come from file headers,
the repo README and RETRIEVED records, and data.gov.sg metadata. The exposures are in
`EXPOSURE.md`.

## 1. Already in coe-analysis

| File | Source | Fields | Coverage | md5 |
|---|---|---|---|---|
| `raw.csv` (root) | data.gov.sg `d_69b3380ad7e51aff3a7dcc84eba52b8a`, "COE Bidding Results / Prices" (LTA), retrieved 18 Aug 2026 | month, bidding_no (1/2), vehicle_class (Cat A-E), quota, bids_success, bids_received, premium | 2010-01 to 2026-08 exercise 1; 1,965 rows (README) | 7b68a001709821c71ece5b8ed209d4d3 |
| `clean.csv` (root) | `02_clean.py` from raw.csv: two documented corrections (2010-01 ex 2 Cat D premium; 2010-02 ex 1 Cat B quota), commas stripped | adds date, cat, oversub, fill | as raw.csv | (generated) |
| `erp/raw/e4b_quota_premium_monthly.csv` | data.gov.sg `d_22094bf608253d36c0c63b52d852dd6e`, SingStat M651121, retrieved 26 Sep 2026 SGT | 50 series, wide: quota, successful bids, bids received and quota premium for each category and bidding; **Prevailing Quota Premium (2nd bidding)** for Cat A, B, C, D (none for E) | 2002-02 to 2026-08, monthly; "-" in months with no bidding (2020) | 8b9f1f55f0c73ad145b78cdbe7006864 |

Notes:
- **The labels describe today's criteria.** e4b's series are labelled "Cars Up To 1600cc
  And 97kW" and "Cars Above 1600cc Or 97kW". LTA says the power criterion dates from 2014
  (release para 3). Before that the split was by engine capacity only, so A and B are not
  the same groups across the break. The EV power threshold also needs checking against
  LTA's own text at Checkpoint 1 (it is not in the files held).
- **No bidding in 2020.** The bidding suspension in 2020 shows as "-" in e4b and as missing
  exercises in raw.csv.
- **Copies for the note.** A new folder copies its raw files into `lta-ab/raw/`, with
  md5s, and does not read across folders at run time.

## 2. To extend to the latest exercise (October 2026)

| Need | Source | Status |
|---|---|---|
| Bidding results to Oct 2026 | Same data.gov.sg dataset `d_69b3380ad7e51aff3a7dcc84eba52b8a`; metadata says last updated 2026-10-07 17:13 SGT, coverage to 2026-10 | Reachable. A fresh download is a NEW file (`lta-ab/raw/`), not a replacement for root `raw.csv`. Cross-check overlapping exercises against raw.csv |
| Oct 2026 exercise 2 | Same dataset, once updated (results in the second half of October) | Comes before the 2 Nov deadline; the cut-off exercise is Jacob's call |
| PQP for Sep-Oct 2026 | e4b dataset (metadata: coverage to 2026-08, updated 2026-08-25); LTA's own PQP page | e4b lags. LTA's PQP page not yet located. Deriving PQP from premiums needs LTA's exact definition (moving-average window and rounding) from LTA's text, not memory |
| The consultation paper | go.gov.sg/coe-public-consult | **Refused (403, policy).** Needs Jacob: a direct lta.gov.sg URL or the PDF |

## 3. What public data can and cannot show

**Can show:**
- per exercise, by category: each category's clearing premium, quota, bids received and
  successful bids;
- how often A cleared above B;
- the A/B quota split;
- the monthly PQP for A and B;
- Category E's premium beside A and B.

**Cannot show (as far as found):**
- **OMV by car model, or the OMV distribution of registrations.** Annex C bands models by
  "the percentile of vehicles registered in the previous year". No public dataset of OMV
  by model or registration was found: a search of data.gov.sg titles found car population
  and new registrations by make, fuel type and cc, none with OMV. So Q2 and Q3 (median OMV,
  band cut-offs, which models land where) cannot be examined with public data.
- **Which cars were bought with which COE,** or how many buyers moved from B to A as
  specifications changed. Registrations by make and cc exist, but not by COE category
  against specification.
- **Renewal volumes by category.** The PQP is published; how many owners renewed at it is
  not in the files held.
- **Bids below the clearing price** (the bid distribution). Only counts are published.
- **The feebate's amounts or cut-offs.** These are in the unretrieved paper, if anywhere.
