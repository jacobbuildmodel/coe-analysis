# lta-ab -- evidence note for LTA's COE categorisation consultation

A short, descriptive evidence note for LTA's public consultation on merging COE Categories A
and B into one passenger car category with a feebate (8 October to 2 November 2026). It sets
out what the published bidding record showed on four points the consultation paper raised.
It takes no view on the proposal. Written by Jacob Ong in a personal capacity.

- **`NOTE.pdf`** is the version linked from the submitted reply.
- **`NOTE.md`** is its source; the PDF's text comes only from it. The three-line
  feedback-form version at its end stays out of the PDF.
- **Submitted on:** 15 October 2026 (Jacob's reply as submitted: SUBMITTED_REPLY.md)
- **`ONEPAGER.md`** is the one-page public version of the consultation (under 800 words); its
  numbers, quotes from SUBMITTED_REPLY.md and model rows are checked by `14_manifest.py --check`.
- **`FORM_TEXT.md`** is an earlier descriptive draft of the feedback form's three boxes, from the same numbers; it was not used.
- **Cut-off:** the data run to the first October 2026 bidding exercise.
- **Windows** (checker's ruling of 12 Oct 2026), the same in every section, table and figure,
  in this order:
  1. since January 2010;
  2. since May 2022, exercise 1, the first exercise under Category A's raised power threshold
     for electric cars (LTA news release of 14 Apr 2022, para 3);
  3. the last 12 months;
  4. the latest exercise or month.

## Rerun

```
bash lta-ab/run_all.sh
```

It runs, in order:
- `10_facts.py`: every number, into `out/`;
- `12_figures.py`: Figure 1 (two panels, matplotlib, house fonts);
- `16_bands.py`: LTA's example bands per model (Tables 1-2) into `out/bands.csv`, and the
  numbers ONEPAGER.md uses into `out/bands_summary.csv`, with their checks;
- `14_manifest.py --check`: checksums, plus every number in NOTE.md checked against the
  number manifest, ASCII, banned words, and the 800-word cap on the prose.

Figure 1's PNG bytes depend on the machine's rasteriser, and on Windows matplotlib writes the SVG with CRLF line endings; on another machine expect a checksum mismatch for `figs/lta_ab_fig1.png` (and, on Windows, the SVG) only, while every file in `out/` reproduces exactly.

**Word cap (checker's ruling, 12 Oct 2026).** The 800-word cap applies to the prose only:
the paragraphs of sections 1-4 and Scope, without the Summary box, Tables 1 and 2, captions,
Notes lines and the figure block (the Sources lines under the tables count as prose). `14_manifest.py --check` prints the current count. The whole note,
everything before "Data and method", is reported but not capped. The check covers
`FORM_TEXT.md` too.

`python3 lta-ab/20_pdf.py` rebuilds NOTE.pdf (A4, fonts embedded; three pages since Table 2
was added, as no table is split from its notes). It needs playwright and Chromium, and
pymupdf and uharfbuzz for its glyph check (copied text must not break inside words). The versions used are in `requirements.txt`.

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
