#!/usr/bin/env bash
# cdc piece. One command, from the repository root or anywhere:
#
#   bash cdc/run_all.sh
#
# 1. Always: the synthetic test suite (cdc/tests/, invented data only): steps
#    10 to 12 end to end with no planted effect, with a planted step, with too
#    much noise and with failed controls.
# 2. Only once the thesis is sealed (cdc/SEALED exists): steps 10 to 12 on the
#    real data in cdc/raw/, then the manifest check. Before the seal the real
#    steps are skipped; 01_download.py and 10_load.py refuse anyway.
set -euo pipefail

cd "$(dirname "$0")/.."
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python

echo "== CDC: python and packages"
$PY --version
$PY -c "import numpy; print('numpy', numpy.__version__)"

echo; echo "== CDC synthetic test suite (invented data only; no real value is read)"
$PY -m unittest discover -s cdc/tests -p "test_*.py" -v

if [ ! -f cdc/SEALED ]; then
  echo; echo "== cdc/SEALED absent: THESIS.md is not sealed, so cdc/raw/ is not read."
  echo "CDC run_all.sh completed: synthetic tests only"
  exit 0
fi

echo; echo "== CDC on the real data"
$PY cdc/10_load.py
$PY cdc/11_tests.py
$PY cdc/12_alternatives.py
$PY cdc/14_manifest.py --check
echo "CDC run_all.sh completed"
