# CANDIDATE_FACTS -- proposed for Jacob's choice (Checkpoint 0, 11 Oct 2026)

Nothing is computed yet. Each fact is descriptive: what the published record shows, with a
one-line "shows / does not show". The note has room for two charts. The proposal is
**F1 and F3 as charts, and F2, F4 and F5 as one-line facts.**

**The common window** starts at the first exercise under the 2014 criteria and ends at the
cut-off exercise Jacob sets (October 2026, exercise 1 or 2). Exercises from 2010 to the
2014 change are reported separately, labelled as cc-only criteria.

**The common trap.** A COE premium is the price that cleared a quota on a given day. It is
not a measure of a car's value, nor of what a buyer would pay for a particular car.

## F1 -- the A-B premium gap, and how often A cleared above B (Q1; Q3 amounts)

- **Source.** data.gov.sg `d_69b3380ad7e51aff3a7dcc84eba52b8a` (fresh copy to the cut-off),
  cross-checked against root `raw.csv` on overlapping exercises.
- **Definition.**
  - Per exercise, gap = premium(B) - premium(A), in dollars.
  - Also the count and dates of exercises with premium(A) > premium(B), and with A = B.
  - Summarised by calendar year, with the median and range, as nominal dollars, not
    deflated.
- **Why it matters.**
  - Annex C says the fee and rebate amounts "take reference from historical price gaps
    between Categories A and B".
  - The release's only statistic was three exercises, February to June 2026, in which A
    exceeded B (para 3). This reproduces it and puts it in the full record.
- **Trap.** The size of a "historical gap" depends on the window chosen. Each category's
  quota is set separately, so the gap moves with quota decisions as well as demand.
- **Shows / does not show.** It shows how far apart the two clearing prices were and when
  they crossed. It does not show why, nor what gap buyers of particular cars faced.

## F2 -- quota shares of A, B and E (Q1, Q5)

- **Source.** As F1 (the quota field).
- **Definition.**
  - Per exercise, A's share = quota(A) / (quota(A) + quota(B)).
  - Also each of A, B and E as a share of A + B + E.
  - Shown yearly.
- **Why it matters.** A merger pools the A and B quotas into one. How that pool was split
  before, and how large E was beside it, is the starting point for Q1 and Q5.
- **Trap.** Quota is an administrative allocation, from deregistrations by category and
  LTA's rules. It is not a measure of demand.
- **Shows / does not show.** It shows how certificates were divided. It does not show how
  many buyers wanted each.

## F3 -- the Prevailing Quota Premium (PQP) for A and B (Q4)

- **Source.** e4b (SingStat M651121 via data.gov.sg `d_22094bf608253d36c0c63b52d852dd6e`),
  copied to `lta-ab/raw/`. It is extended past August 2026 only from a published LTA or
  SingStat PQP, not from a re-derivation unless LTA's definition is retrieved.
- **Definition.**
  - Monthly PQP(B) - PQP(A).
  - Also the months with PQP(A) >= PQP(B).
  - Same window as F1.
- **Why it matters.** Renewals pay their category's PQP. Q4 asks whether the feebate
  applies to renewals. The PQP gap is the renewal-side counterpart of F1.
- **Trap.**
  - The PQP is a moving average, so it lags and smooths the premiums.
  - Renewal terms, such as a shorter renewal at part of the PQP, need LTA's text, not
    memory.
  - Renewal volumes are not public in the files held.
- **Shows / does not show.** It shows what renewing in A or B cost, by month. It does not
  show how many renewed, nor who.

## F4 -- Category E's premium beside A and B (Q5)

- **Source.** As F1.
- **Definition.**
  - Per exercise, premium(E) - premium(B) and premium(E) - premium(A).
  - Also the count of exercises with E below B.
- **Why it matters.** E certificates can be used for cars of either category, so E's price
  is tied to A and B. Q5 asks how E changes if they merge.
- **Trap.** E is also usable for goods vehicles, and its buyers are not identified. A small
  E-B gap shows substitution in price, not who bought E or why.
- **Shows / does not show.** It shows how E's clearing price tracked A and B. It does not
  show E's buyers.

## F5 -- bids per certificate in A and B (Q1)

- **Source.** As F1 (bids_received, quota).
- **Definition.** Per exercise, bids_received / quota for A and for B, shown yearly.
- **Why it matters.** The release says "more car buyers are competing for Category A COEs"
  (para 3). This is the published count closest to that claim.
- **Trap.**
  - Bids are lodged mostly by dealers, and their number responds to expected prices.
  - A ratio near 1 at a high premium and a ratio of 2 at a low one can both clear.
  - It is not a count of buyers.
- **Shows / does not show.** It shows how heavily each quota was bid. It does not show
  buyers' numbers or intentions.

## Not offered

- **Q2 and Q3 band design (median OMV, cut-offs).** The OMV-by-model or registration
  distribution is not public in what was found. The note can say only that.
- Any estimate of how prices would move after a merger. That is a forecast, outside the
  brief.

## Rule 0, item 5 (decision test)

LTA's COE review team, deciding Q1, Q3 and Q4, would set the feebate amounts and the
renewal treatment knowing:
- how large the A-B gap and the PQP gap were;
- how much they moved;
- how much the "historical gap" depends on the window chosen.

## Checker's rulings (11 Oct 2026)

- **F1 and F3 kept as the two charts.** F1 has two windows: from 2010 and the last five
  years. It checks LTA's "three occasions" (P 1.8).
- **F2 and F4 kept,** as one sentence each with no chart.
- **F5 dropped.** Dealer bids were too easy to misread.
- **The cut-off** is the first October 2026 exercise, with the data frozen.
- The definitions as built are in `10_facts.py`'s docstring.
