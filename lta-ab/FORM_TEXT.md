# Feedback form text

Text for the three boxes of LTA's feedback form (go.gov.sg/coe-pcd-feedback). Every number
is from `out/facts.csv` and is checked by `14_manifest.py --check`, as in NOTE.md. Windows:
since January 2010, and since May 2022, when Category A's power threshold for electric cars
changed. Data to October 2026, exercise 1.

## Box 1. Merging Categories A and B with a feebate (consultation question 1)

The published bidding record agrees with the paper's account of 2026, and shows a gap between Categories A and B that was narrower in the latest data than over longer periods. Category A cleared above Category B in 3 of the 10 exercises from February to June 2026, consistent with paragraph 1.8, and in 21 of 397 exercises since January 2010. The median premium gap (B minus A) was $9,010 since January 2010 and $17,999 since May 2022, beside the paper's example band steps of $7,500 and $15,000 (median gap as a share of Category A's premium: 16 and 18 per cent); in the latest exercise in this submission (October 2026, exercise 1) it was $99. Compared with the same exercise 12 months earlier, the gap moved, up or down, by a median of $6,603 since January 2010 and $9,512 since May 2022. On renewal prices, paragraph 2.19's "broadly similar PQPs" is consistent with the last 12 months (median gap $4,930, 4 per cent of Category A's PQP) and October 2026 ($2,901, 2.3 per cent); over longer windows the gap was larger (median $8,668 since January 2010 and $19,254 since May 2022). Full note, data and code: https://github.com/jacobbuildmodel/coe-analysis (folder lta-ab).

## Box 2. Category E (consultation question 2)

Category E's premium cleared at or above both Category A's and Category B's in most bidding exercises. Category E received 15 per cent of the combined Category A, B and E quota since January 2010 and 11 per cent since May 2022. Since May 2022 it cleared at or above both Categories A and B in 74 of 107 exercises and below Category B in 33; the median of its premium minus Category B's was $888. The data do not show which vehicles were registered with Category E certificates (paragraph 2.22).

## Box 3. Other comments

This submission is descriptive and takes no view on the proposals. Every figure is produced by a public script from LTA, data.gov.sg and SingStat data, and can be rerun from the repository above (lta-ab/run_all.sh). It is made in a personal capacity by Jacob Ong, an independent researcher (ORCID 0009-0005-4438-9657).
