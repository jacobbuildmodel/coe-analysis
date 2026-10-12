# lta-ab -- evidence note for LTA's COE categorisation consultation

A short, descriptive evidence note for LTA's public consultation on merging COE Categories A
and B into one passenger car category with a feebate (8 October to 2 November 2026). It sets
out what the published bidding record showed on four points the consultation paper raised.
It takes no view on the proposal. Written by Jacob Ong in a personal capacity.

- **`NOTE.pdf`** is the submitted version.
- **`NOTE.md`** is its source; the PDF's text comes only from it. The three-line
  feedback-form version at its end stays out of the PDF.
- **Submitted on:** ____________ (date to be filled in by Jacob)
- **Cut-off:** the data run to the first October 2026 bidding exercise.

## Rerun

```
bash lta-ab/run_all.sh
```

It runs, in order:
- `10_facts.py`: every number, into `out/`;
- `12_figures.py`: Figure 1 (two panels, matplotlib, house fonts);
- `14_manifest.py --check`: checksums, plus every number in NOTE.md checked against the
  number manifest, ASCII, banned words, and the 800-word cap on the prose.

`python3 lta-ab/20_pdf.py` rebuilds NOTE.pdf (A4, 2 pages, fonts embedded). It needs
playwright and Chromium. The versions used are in `requirements.txt`.

## What is here

- **`raw/`:** LTA's release, annexes and consultation paper, and the bidding, SingStat
  and LTA M11 data. `raw/RETRIEVED.txt` records every download and refusal.
- **`office/`:**
  - `LTA_PROPOSAL.md`: the proposal, with paragraph references;
  - `DATA_INVENTORY.md` and `CANDIDATE_FACTS.md`;
  - `EXPOSURE.md`: every series and statistic looked at, for a later sealed A/B piece;
  - `LTA_CONSTANTS.csv`: LTA's amounts, as quoted from the paper.
- **`office/redesign/`:** the checker's reference design (fig.py, note.html, the target
  PDF), unpacked from `office/lta_redesign_upload.zip`.
- **`fonts/`:** Source Sans 3 and Source Serif 4, from the site repo's
  `research/paper-template/fonts` (SIL Open Font License; licences included).
- **`out/`, `figs/`, `number_manifest.csv`, `CHECKSUMS.md5`:** outputs and their checks.
