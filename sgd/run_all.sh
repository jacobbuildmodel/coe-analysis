#!/usr/bin/env bash
# sgd piece. One command, from the repository root or anywhere:
#
#   bash sgd/run_all.sh
#
# 1. Always: the synthetic test suite (sgd/tests/, invented data only). It
#    builds invented raw files, runs steps 10-15 end to end on them and forces
#    every outcome branch.
# 2. Only once the thesis is sealed (sgd/SEALED exists): steps 10-15 on the
#    real data in sgd/raw/, then every checksum verified. Before the seal the
#    real steps are skipped, and 10_load.py would refuse sgd/raw/ anyway.
#
# Exits non-zero if any test or step fails or any checksum does not match.
# CHECKSUMS.md5 is never written here; regenerate it by hand, last, with
#   python3 sgd/14_manifest.py
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== SGD: python and packages"
python3 --version
python3 -c "import pandas, numpy, scipy, openpyxl; print('pandas', pandas.__version__, '| numpy', numpy.__version__, '| scipy', scipy.__version__, '| openpyxl', openpyxl.__version__)"

echo; echo "== SGD synthetic test suite (invented data only; no real value is read)"
python3 -m unittest discover -s sgd/tests -p "test_*.py" -v

if [ ! -f sgd/SEALED ]; then
  echo; echo "== sgd/SEALED absent: THESIS.md is not sealed, so sgd/raw/ is not read."
  echo "SGD run_all.sh completed: synthetic tests only"
  exit 0
fi

mkdir -p sgd/out sgd/figs

echo; echo "== 10 load raw/ into tidy tables"
python3 sgd/10_load.py

echo; echo "== 11 T1-T4, T7 and gate C as sealed, sensitivities, verdict, scorecard"
python3 sgd/11_tests.py

echo; echo "== 12 charts"
python3 sgd/12_figures.py

echo; echo "== 13 RESULTS.md"
python3 sgd/13_results.py

echo; echo "== 15 independent reproduction of every scored number"
python3 sgd/15_reproduce.py

echo; echo "== figure overflow check (DejaVu Sans, needs playwright + chromium)"
python3 tools/check_figure_overflow.py sgd/figs/sgd_chart1_split.svg sgd/figs/sgd_chart2_steady.svg sgd/figs/sgd_chart3_path.svg

echo; echo "== 14 checksums and number manifest, verified"
python3 sgd/14_manifest.py --check

echo; echo "SGD run_all.sh completed, all checksums verified"
