#!/usr/bin/env bash
# lta-ab evidence note. One command, from the repository root or anywhere:
#
#   bash lta-ab/run_all.sh
#
# Builds every number (10), both charts (12), checks the charts for text
# overflow, then verifies checksums and every number in NOTE.md (14 --check).
# Exits non-zero if any step fails. CHECKSUMS.md5 and number_manifest.csv are
# never written here; regenerate them by hand, last, with
#   python3 lta-ab/14_manifest.py
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== lta-ab: python and packages"
python3 --version
python3 -c "import pandas, pypdf; print('pandas', pandas.__version__, '| pypdf', pypdf.__version__)"

echo; echo "== 10 facts, from lta-ab/raw/ (cut-off: October 2026, exercise 1)"
python3 lta-ab/10_facts.py

echo; echo "== 12 charts"
python3 lta-ab/12_figures.py

echo; echo "== figure overflow check (DejaVu Sans, needs playwright + chromium)"
python3 tools/check_figure_overflow.py lta-ab/figs/lta_ab_chart1_gap.svg lta-ab/figs/lta_ab_chart2_pqp.svg

echo; echo "== 14 checksums and number manifest, verified"
python3 lta-ab/14_manifest.py --check

echo; echo "lta-ab run_all.sh completed, all checksums verified"
