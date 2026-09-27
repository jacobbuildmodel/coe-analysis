# THESIS ADDENDUM -- ERP piece

THESIS.md is sealed at commit `6d2a345` (md5 `2f99e6513de2f5ebe7f578e6a5650f50`)
and is not edited. This file holds what was learned or decided after the seal.
**Nothing here changes a score in RESULTS.md.** Each item says whether it was
written before or after results were seen.

## 26 September 2026 -- written AFTER results were seen

### 1. T3: the bias named at the seal ran the other way

THESIS T3 named private-hire cars as a bias that would push toward FAIL if they
grew in the low-premium years, and Jacob's reason for his 20% confidence rested
on that ("they grew in the cheaper-COE years"). E3 shows the opposite: hire and
rental cars grew by 54,736 over the seven high-premium years and by 5,591 over
the seven low-premium years (RESULTS.md, T3). The bias pushed toward PASS, and
T3 failed anyway. The call was right; the stated mechanism was not.

What does line up with the split is time. All seven high-premium years fall in
2011-2017, and km per car fell in every year from 2007 to 2016. The
researcher's proposal named a slow secular fall as the main risk; the split
cannot separate the premium from that drift. Reported, not re-scored.

A second observation, not checkable from here: E2's cars row is recorded to the
kilometre for 2005-2009 (for example 20,603) and in round hundreds from 2010
(for example 19,100). That looks like a change in how the survey figure was
published, and it falls one year before the high-premium half begins. The E2
page notes could not be read (data.gov.sg refuses this sandbox). If a method
break is confirmed, T3's comparison crosses it. Reported, not re-scored.

### 2. T1: rounding in E1 after 2019, and the edge convention

E1 is recorded to one decimal for 2004-2019 and in whole km/h for 2020-2025.
The sealed text says "within 20-30 km/h" without saying whether 30 itself is
inside. `11_tests.py` reads the band as closed (30.0 is inside), a convention
fixed after the seal and stated in RESULTS.md. Under it, arterial 2017 (30.0),
2022 (30) and 2024 (30) are inside. Read as open, or if the rounded 2022 and
2024 values were above 30 before rounding, up to three more arterial years
would count as above the band. T1 is FAIL under every reading: 2016 (30.4) and
2023 (31) are above 30 whatever the convention or rounding.

### 3. The PENDING items of THESIS section 10, item 9

- **The band's history.** The MOT page (E6) and the ITF paper of 2020 (E5) state
  45-65 km/h on expressways and 20-30 km/h on arterial roads; no LTA release in
  `raw/` (June 2018 onward) states a different band. T1 was scored against those
  bands in every year, as sealed. No change found; none applied.
- **The speed measure LTA compares with the band.** Still not documented in any
  file in `raw/`. The ITF paper says LTA "has generally not published technical
  information on how ERP charges are determined". Open.
- **E1 method notes.** Not read; the data.gov.sg page is unreachable from this
  sandbox. The change to whole numbers in 2020 (item 2) is the only visible
  sign of a change. Open.

### 4. E8 and E8b disagree in one cell

For 2008 arterial lane-km, E8 (the data.gov.sg CSV) has 2932 and E8b (LTA's PDF)
has 2923. The other 19 cells of the ten overlapping years agree. E8 was used, as
sealed. The T2 sensitivity with E8b's value moves the arterial elasticity from
0.254 to 0.252 (RESULTS.md, T2 sensitivities).

### 5. Conventions fixed in code after the seal

- The 90 per cent intervals use statsmodels' default with HC1 errors, which is
  the normal critical value. With t critical values the T4 arterial interval
  still excludes zero, so T4 is MIXED either way.
- The annual premium is the mean over months of the mean over that month's
  exercises (section 4's "months with no bidding left out"). E4b and E4
  (`../raw.csv`) agree to the dollar for every year 2010-2025, so this choice
  does not move the T3 split or T4.
- "Cars" is E3's category "Cars and Station-wagons" in full: private, company,
  tuition, off-peak, private-hire and rental cars. Taxis and tax-exempted
  vehicles are separate categories in E3 and are not included.

### 6. Reasons against outcomes, for the scorecard

- T1 (35%, FAIL): Jacob's reason ("one fast year on the main roads breaks it,
  even if the control is working") describes what happened: the failure is on
  the fast side, on arterial roads.
- T2 (65%, PASS): held on both road classes, though the arterial slope is
  positive and gives way to the time trend when one is added.
- T3 (20%, FAIL): outcome as expected, mechanism not (item 1).
- T4 (70%, MIXED): the reason ("little left to explain") held for expressways
  and not for arterial roads, where the premium's interval excludes zero.

### 7. E1's averaging period, and one figure LTA printed differently

From the method-note lookup recorded in `raw/RETRIEVED.txt` (commit `e6d1a25`),
still written AFTER results were seen:

- LTA's *Statistics in Brief 2008* says traffic speed is "averaged over the
  period of financial year (April-March)"; the 2015 edition says "averaged over
  the period of January-December". The E1 series therefore switched from
  financial-year to calendar-year averages at some point between those editions,
  and LTA does not publish when. Neither the data.gov.sg page nor any LTA
  document found mentions it, or any rounding change in E1 or E2. The switch
  moves the window each annual figure covers by three months; it does not
  change what any test compares, and no score changes.
- *Statistics in Brief 2015* prints the 2013 expressway peak speed as 61.6 km/h;
  the data.gov.sg file (E1) has 61.4. Both are inside the 45-65 km/h band, and
  2013 is a scored expressway year for T1, so T1's expressway result is the same
  under either figure. E1 was used, as sealed. No score changes.
