# HANDOVER -- coe-analysis (researcher role), as of 11 October 2026

For a new chat taking over the researcher role in this repo, with no history.
House rules live in the site repo, not here: jacobbuildmodel/jacobbuildmodel.github.io,
`office/` on main. Read those first (see "Rules" below).

## What this repo is

Code, data and drafts behind the Singapore policy site. One folder per piece; the
article itself is published from the site repo (`content/economics/YYYY-MM-DD.md`,
figures in `static/figs/`). Root: the COE pieces.

| Piece | Folder | Sealed | Data opened | On site main, dated (hidden until that date) |
|---|---|---|---|---|
| COE quota and prices | root (`01_`..`10_*.py`) | no (pre-seal era) | yes | 22 Aug 2026 |
| COE timing | root | no | yes | 29 Aug 2026 |
| COE win rate | `win-rate/` | no | yes | 5 Sep 2026 |
| Motorcycle COEs | `motorcycles/` | no | yes | 12 Sep 2026 |
| ERP or COE | `erp/` | 26 Sep 2026 (`erp/office/SEAL.txt`) | yes | 17 Oct 2026 |
| PWM / minimum wage | `pwm/` | 28 Sep 2026, e5f877b | yes | 31 Oct 2026 |
| Singapore dollar (sgd) | `sgd/` | 3 Oct 2026, **9e46034** | yes, key 59789e4 | 14 Nov 2026 |

The site has `buildFuture = false`, so 17 Oct, 31 Oct and 14 Nov stay hidden until their dates.
Other pieces (GST, HDB affordability, HDB loan) live in other repos (e.g. hdb-affordability).

## Open branches and PRs

- **PR #5, `sgd-review` -> main (draft), head d57f873.** Rounds 4-5 of outside review:
  `16_review.py` (A1-A6), chart 4, the article and FOR_RESEARCHERS rewrites, and
  THESIS_ADDENDUM item 10. The checker verified round 5. **Next step:** Jacob marks it ready and merges it with
    "Create a merge commit". Then the publication-day PR in the site repo (by 14 Nov)
    copies the merged files into the site:
    - `sgd/2026-11-14.md` -> `content/economics/2026-11-14.md`. The site still holds the
      Checkpoint-2 text.
    - `sgd/FOR_RESEARCHERS.md` -> `content/researchers/singapore-dollar.md`.
    - all four `sgd/figs/*.svg` -> `static/figs/`. `sgd_chart4_rolling.svg` is new.
    - The same PR switches "What to watch next" from /open/ to the replication's open
      question page, if that page is live. The checker confirms.
- **`handover-2026-10`:** this file.
- **All other branches** (`erp-wip`, `erp-merge`, `pwm-wip`, `pwm-merge`, `sgd-wip`,
  `phase3-shared-tokens`) are fully merged into main. Leave them; never delete `pwm-wip`.

## Rules and where they live

- **Site repo `office/`:** `CHECKPOINTS.md` (Checkpoints 0-3, checker independence);
  `STORY_CRAFT.md` (S1-S10, R1-R7, openings L1-L7); `QUESTION_RULES.md` (H1-H7, Rule 0;
  item 5, the decision test, added 5 Oct, site copy being synced); `EDITOR.md`;
  `REPLY_FORMAT.md` (every hand-back uses the 5-line block, 12 lines max).
- **Per piece:**
  - `THESIS.md` is sealed, never edited.
  - `THESIS_ADDENDUM.md` is the only place for changes after the seal: dated, numbered, one
    line per change, with md5s before and after.
  - `SEAL_MANIFEST.md` holds the md5 of every file at the seal.
  - `raw/RETRIEVED.txt` records every download (URL, date, bytes, md5). Append only.
- **Article style:** pure ASCII (no em dash, U+2212 or U+00D7); no "we"; banned words
  choose, should, recommend, better option, you should; findings in past tense; no
  advice; a not-advice line at the end; 1,200-1,800 words before Sources.
- **Post-hoc work** (after outside review) is labelled "added after outside review, not
  sealed" everywhere it appears, and never changes a sealed number, outcome, threshold or
  verdict-rule wording.

## Commands (run from the repo root)

```
bash run_all.sh                          # root COE pieces + erp/ + pwm/ (NOT sgd/)
bash sgd/run_all.sh                      # sgd: tests, 10-16, charts, RESULTS, 15, overflow, 14 --check
python3 -m unittest discover -s sgd/tests -p "test_*.py"   # synthetic suite only
python3 sgd/14_manifest.py               # REWRITE checksums + number manifest (by hand, LAST)
python3 sgd/14_manifest.py --check       # verify md5s, manifest, every number in article + FOR_RESEARCHERS
python3 tools/check_figure_overflow.py sgd/figs/*.svg      # needs playwright + chromium; checks bold
python3 sgd/tests/make_fixtures.py DIR   # an invented-data fixture root (then run 10..16, 12 with --root DIR)
```

Before any hand-back, clone the branch fresh and run `bash sgd/run_all.sh`; it must exit 0
and leave `git status --short` empty.

**Site repo checks** (see `.github/workflows/lint.yml`):

```
python scripts/aitell.py <files> --strict --published-only
vale --no-wrap <files>
python scripts/check_open_pages.py
```

Run them through the real Hugo build at 390 px and 1280 px, in light and dark.

**Numbers in prose.** Every digit in the article or FOR_RESEARCHERS must be a printed
value in `sgd/number_manifest.csv`, a sealed constant (`ALLOW` in `14_manifest.py`), an
integer of 10 or less, or a year.

New numbers go through a script: `11b_postresults.py` before review, `16_review.py` after.
Never type a number by hand.

## Gotchas and fixes

- **The proxy CA.** Headless Chromium rejects the session proxy's CA. Save pages with
  `curl` instead. Never disable TLS checks.
- **Policy denials.** A host refused with 403 by network policy is not routed around.
  Record it in RETRIEVED.txt and keep the claim general. Hosts refused so far:
  www.federalreserve.gov (403, 10 Oct); fred.stlouisfed.org did not connect.
- **SingStat TableBuilder** stops at 5,000 observations. Check that the series you need is
  complete.
- **BIS PDFs moved** to `/publications/...` paths; the old `/publ/` paths serve a landing
  page.
- **`14_manifest.py --check` fails** after any edit until `python3 sgd/14_manifest.py`
  rewrites the checksums. Run the writer last, then the full `run_all`.
- **`14_manifest.py --seal` overwrites SEAL_MANIFEST.md.** Never run it after a seal. It
  happened once on 3 Oct; the file was restored with `git checkout` before any commit.
- **The banned-word grep must cover both** the article and FOR_RESEARCHERS: "as it should"
  slipped into FOR_RESEARCHERS once.
  `grep -n -i -w -E "we|choose|should|recommend" FILES` and
  `grep -i "better option\|you should" FILES`.
- **Word count method.** Count the body after the front matter, minus the verdict shortcode
  and image alt text, up to `## Sources`.
- **Fixture charts** need their `out/postresults.csv` and `out/review_*.csv` rebuilt
  (`11b`, then `16 --root DIR`) before the overflow check, or charts 2 and 4 are skipped.
- **Shares explode when b is tiny** (rolling windows). Chart 4 clips at -50/150 and its
  caption says so.
- **Claims from memory are often wrong.** Check each against `out/` before writing it (the
  HK basket was not mostly US dollar; the yen's index did not "cancel out" over two decades).
- **GitHub MCP tools drop out intermittently.** `gh api <REST path>` works for reads.
- **The root `run_all.sh` does not run `sgd/`.** Run both.

## Credentials (names only)

This repo needs none: every data file is committed in `raw/`. Workflows in other repos use
`CLAUDE_CODE_OAUTH_TOKEN` and `GITHUB_TOKEN`. The OneMap API token used elsewhere (hdb
pieces) **expired 8 Oct 2026**: ask Jacob for a new one, and never commit it.

## Do NOT

- Edit any sealed file. For sgd, the sealed files are `THESIS.md` (md5 8acdcf79...),
  `SEAL_MANIFEST.md`, `office/MPS_CODING.csv`, `office/MPS_CANDIDATES.txt`, and the bytes
  of `raw/*`. RETRIEVED.txt takes appended blocks only, logged in the addendum.
- Read real data before a seal. `10_load.py`, `15_reproduce.py` and `16_review.py` refuse
  `raw/` until `SEALED` exists.
- Set, suggest or move a confidence. Jacob sets every confidence alone; the researcher's
  proposal goes in THESIS "for the record" only.
- Merge, squash or rebase. Jacob merges with "Create a merge commit" only, so the seal and
  key hashes survive. Never rewrite history, never force-push a shared branch, never delete
  `pwm-wip`.
- Touch the website repo, except read-only, unless a brief says so.
- Name outside reviewers or their institutions without Jacob's permission.
- Present a post-hoc analysis as a finding. Label it, and leave the sealed verdict sentence
  verbatim.
