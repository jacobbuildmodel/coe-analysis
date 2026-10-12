# lta-ab -- evidence note for LTA's COE categorisation consultation

A short, descriptive evidence note for LTA's public consultation on merging COE Categories A
and B into one passenger car category with a feebate (8 October to 2 November 2026). It sets
out what the published bidding record showed on four points the consultation paper raised.
It takes no view on the proposal. Written by Jacob in a personal capacity.

- **`NOTE.pdf`** is the submitted version.
- **`NOTE.md`** is its source; the PDF's text comes only from it.
- **Submitted on:** ____________ (date to be filled in by Jacob)
- **Cut-off:** the data run to the first October 2026 bidding exercise.

## Rerun

```
bash lta-ab/run_all.sh
```

It runs, in order:
- `10_facts.py`: every number, into `out/`;
- `12_figures.py`: the two charts;
- the figure overflow check;
- `14_manifest.py --check`: checksums, plus every number in NOTE.md checked against the
  number manifest, ASCII, banned words, and the 800-word cap.

`python3 lta-ab/20_pdf.py` rebuilds NOTE.pdf. It needs playwright and Chromium.

## What is here

- **`raw/`:** LTA's release, annexes and consultation paper, and the bidding, SingStat
  and LTA M11 data. `raw/RETRIEVED.txt` records every download and refusal.
- **`office/`:**
  - `LTA_PROPOSAL.md`: the proposal, with paragraph references;
  - `DATA_INVENTORY.md` and `CANDIDATE_FACTS.md`;
  - `EXPOSURE.md`: every series and statistic looked at, for a later sealed A/B piece;
  - `LTA_CONSTANTS.csv`: LTA's amounts, as quoted from the paper.
- **`out/`, `figs/`, `number_manifest.csv`, `CHECKSUMS.md5`:** outputs and their checks.
