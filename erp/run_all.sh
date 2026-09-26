#!/usr/bin/env bash
# ERP piece: rebuilds erp/out, erp/figs and erp/RESULTS.md from erp/raw, then
# verifies every checksum. One command, from clean:
#
#   rm -rf erp/out erp/figs && bash erp/run_all.sh
#
# Exits non-zero if any step fails or any checksum does not match.
# CHECKSUMS.md5 is never written here; regenerate it by hand, last, with
#   python3 erp/14_manifest.py
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== ERP: python and packages"
python3 --version
python3 -c "import pandas, numpy, statsmodels, pypdf; print('pandas', pandas.__version__, '| numpy', numpy.__version__, '| statsmodels', statsmodels.__version__, '| pypdf', pypdf.__version__)"

mkdir -p erp/out erp/figs

echo; echo "== 10 load raw/ into the annual table, coverage asserted against RETRIEVED.txt"
python3 erp/10_load.py

echo; echo "== 11 T1-T4 as sealed, T5 leg (a) unscored, S1, scorecard, verdict"
python3 erp/11_tests.py

echo; echo "== 12 charts"
python3 erp/12_figures.py

echo; echo "== 13 RESULTS.md"
python3 erp/13_results.py

echo; echo "== 15 independent reproduction of every scored number"
python3 erp/15_reproduce.py

echo; echo "== figure overflow check (DejaVu Sans, needs playwright + chromium)"
python3 tools/check_figure_overflow.py erp/figs/chart1_speed_vs_band.svg erp/figs/chart2_door_fee.svg

echo; echo "== 14 checksums and number manifest, verified"
python3 erp/14_manifest.py --check

echo; echo "ERP run_all.sh completed, all checksums verified"
