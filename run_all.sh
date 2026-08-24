#!/usr/bin/env bash
# Reproduce everything, in order, from raw.csv.
# 02 must run first. 03 through 10 are independent of one another.
set -euo pipefail

echo "== 01 data quality pass (diagnostic; found the two source errors)"
python3 01_explore.py

echo; echo "== 02 build analysis.csv, with both corrections asserted"
python3 02_clean.py

for s in 03_regress 04_decompose 05_chartdata 06_ev 07_av_benchmark \
         08_bidding_round 09_figures 10_deregistration; do
  echo; echo "== ${s}"
  python3 "${s}.py"
done

echo; echo "== checksum"
if command -v md5sum >/dev/null; then md5sum analysis.csv; else md5 analysis.csv; fi
echo "   expected: 4480189cd99b4514885185843ac5f2cc"
