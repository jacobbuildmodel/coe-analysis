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

echo; echo "== figure overflow check (DejaVu Sans, needs playwright + chromium)"
python3 tools/check_figure_overflow.py figs/mechanism.svg figs/indexed.svg \
  figs/decomposition.svg figs/gap_distribution.svg

echo; echo "== checksum: analysis.csv must be the file the README publishes"
expected=4480189cd99b4514885185843ac5f2cc
if command -v md5sum >/dev/null; then got=$(md5sum < analysis.csv | cut -c1-32); else got=$(md5 -q analysis.csv); fi
echo "   analysis.csv $got"
echo "   expected     $expected"
if [ "$got" != "$expected" ]; then
  echo "MISMATCH analysis.csv: this run did not reproduce the published file" >&2
  exit 1
fi

echo; echo "== ERP piece (erp/), its own steps and checksums"
bash erp/run_all.sh

echo; echo "== PWM piece (pwm/): synthetic tests always; real steps only once sealed"
bash pwm/run_all.sh
