#!/usr/bin/env bash
# PWM piece. One command, from the repository root or anywhere:
#
#   bash pwm/run_all.sh
#
# 1. Always: the synthetic test suite (pwm/tests/, invented data only). It
#    runs steps 10-15 end to end on a copy of pwm/tests/fixtures/ and forces
#    every outcome branch.
# 2. Only once the thesis is sealed (pwm/SEALED exists): steps 10-15 on the
#    real data in pwm/raw/, then every checksum verified. Before the seal the
#    real steps are skipped, and 10_load.py would refuse pwm/raw/ anyway.
#
# Exits non-zero if any test or step fails or any checksum does not match.
# CHECKSUMS.md5 is never written here; regenerate it by hand, last, with
#   python3 pwm/14_manifest.py
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== PWM: python and packages"
python3 --version
python3 -c "import pandas, numpy, statsmodels, openpyxl, xlrd, xlwt; print('pandas', pandas.__version__, '| numpy', numpy.__version__, '| statsmodels', statsmodels.__version__, '| openpyxl', openpyxl.__version__, '| xlrd', xlrd.__version__, '| xlwt', xlwt.__VERSION__)"

echo; echo "== PWM synthetic test suite (fixtures only; no real value is read)"
python3 -m unittest discover -s pwm/tests -p "test_*.py" -v

if [ ! -f pwm/SEALED ]; then
  echo; echo "== pwm/SEALED absent: THESIS.md is not sealed, so pwm/raw/ is not read."
  echo "PWM run_all.sh completed: synthetic tests only"
  exit 0
fi

mkdir -p pwm/out pwm/figs

echo; echo "== 10 load raw/ into tidy tables"
python3 pwm/10_load.py

echo; echo "== 11 T1-T5 as sealed, sensitivities, verdict, scorecard"
python3 pwm/11_tests.py

echo; echo "== 11b post-results checks (added after the results, not scored)"
python3 pwm/11b_postresults.py

echo; echo "== 12 charts"
python3 pwm/12_figures.py

echo; echo "== 13 RESULTS.md"
python3 pwm/13_results.py

echo; echo "== 15 independent reproduction of every scored number"
python3 pwm/15_reproduce.py

echo; echo "== figure overflow check (DejaVu Sans, needs playwright + chromium)"
python3 tools/check_figure_overflow.py pwm/figs/chart1_gap.svg pwm/figs/chart2_pace.svg pwm/figs/chart3_rung.svg

echo; echo "== 14 checksums and number manifest, verified"
python3 pwm/14_manifest.py --check

echo; echo "PWM run_all.sh completed, all checksums verified"
