# ALTERNATIVES -- cdc piece: sealed alternative specifications

**UNSEALED DRAFT, 24 November 2026.** Sealed with THESIS.md and listed in
SEAL_MANIFEST.md. Written before any index value was opened.

Each alternative changes one thing in the main specification of THESIS.md
section 4 to answer one named referee objection. Each is scored by the same
rule as its test (the controls, Gate D, the 0.5 line or p; for T4 the largest
placebo excess). They are run by `12_alternatives.py` with the tests and
reported beside them as "k of n alternatives give the same result as the main
specification". They never make a second verdict, and none replaces a test.

## Where the objections came from

Two outside models read the THESIS draft (md5 031d0705a320607b8c1bedbb179efee7)
on 24 November 2026 as journal referees, each asked for its eight most
damaging objections (prompt P3): NVIDIA Nemotron 3 Ultra ("N1" to "N8") and
Baidu Ernie 5.5 Flash ("E1" to "E8"). Objections marked "own" are confounds
THESIS.md section 10 named before the models were asked.

## The alternatives

| Code | Objection answered | What changes | Counted as not keeping the result if |
|---|---|---|---|
| A1 | The window is too short: vouchers are spent over months (N2, E1) | Window from the month before the launch to three months after it (five launches: 2021 Nov to 2022 Mar, 2022 Apr to Aug, 2024 May to Sep, 2025 Apr to Aug, 2026 May to Sep; January launches: Dec to Apr) | the test gives a different result on the longer window |
| A2 | Restaurants and fast food are substitutes for hawker food and some restaurants take vouchers, so the gap can stay flat while hawker prices rise (N1, E2) | Comparison is row 1 (All Items) alone | the hawker row steps against All Items |
| A3a | The geometric mean of two rows hides a move in one of them (N5) | Comparison is row 1.11.1 (Restaurants, Cafes & Pubs) alone | the result differs against restaurants alone |
| A3b | The same (N5); fast-food chains are also the row least likely to take vouchers (N1) | Comparison is row 1.11.2 (Fast Food Restaurants) alone | the result differs against fast food alone |
| A4 | The placebo years hold a GST rise, the pandemic and the lower-income vouchers (N4, E4, own) | Every placebo window with a month in 2007, 2020 or 2021 is dropped | the result differs on the clean placebo years |
| A5 | A fixed 2005 to 2021 baseline ignores a trend or catch-up in the gap after 2021 (E5, N7, own) | From every window change, launch and placebo alike, the window's own earlier pace is taken away: the change of the gap over the 12 months to the window's first month, scaled to the window's length. Placebo years then start one year later | the result differs once each window is measured against its own trend |
| A6 | The June 2026 launch followed the energy shock of 28 February 2026 (own) | The June 2026 launch is left out (four launches) | the result rests on June 2026 |
| A7 | The June 2024 tranche opened on 25 June, after most of June's prices were collected (own) | That launch's month is July 2024 (window 2024 Jun to Aug) | the result differs when the late launch is dated a month later |

T1 and T2: A1 to A7 (eight specifications, counting A3a and A3b).
T3 and T4: A1, A2, A3a, A3b, A4 and A5 (six). A6 and A7 concern launches that
are not in T3 or T4.

For T4 the A1 window ends in 2027 Apr, so its A1 line is filled about two
months after the main result.

## Objections answered without a new specification

- **The treated row is diluted; score the Hawker Centres sub-row (N3, E3).**
  Row 1.11.3.1 starts in 2019 Jan: at most three placebo years, so no result on
  it can be told from chance. It is described beside the tests (THESIS section
  9), and the dilution is in the weak-evidence sentence. Row 1.11.1.1 starts in
  2024 and has no placebo year.
- **Gate D may be underpowered; report the minimum detectable effect (N6).**
  Done: the smallest step each test sees four times in five is reported beside
  every result (THESIS section 4, step 6).
- **Gate D measures noise in the placebo years, not in 2022 to 2026 (E7).**
  Accepted as a limit. The noise of the launch years cannot be measured without
  assuming which of their months are free of voucher effects. A4 and A5 show how
  much the gate moves with the placebo set.
- **Tranches overlap: households hold a stock of unspent vouchers, so launches
  are not separate shocks; test one level shift from December 2021 (E6).** A
  level shift after 2021 cannot be told apart from everything else that changed
  then (GST, the recovery from the pandemic, rents). A1 lengthens the window;
  the limit is in the weak-evidence sentence.
- **T1 and T2 use the same statistic (E8).** Stated in T2. Both are kept: T1 is
  the size that matters for the decision, T2 whether any step shows.
- **The 0.5 line is asserted (E8).** It was fixed at Checkpoint 0 as the
  smallest effect that matters, before this design. T2 does not depend on it.
- **The January 2027 tranche may be cancelled or priced in early (N8).** T4 is
  void if no tranche for all households is issued in January 2027. Its window
  starts from December 2026, so a rise before December is not counted; that is
  a limit of T4.
