#!/usr/bin/env bash
# lta-ab evidence note. One command, from the repository root or anywhere:
#
#   bash lta-ab/run_all.sh
#
# Builds every number (10) and Figure 1 (12), then verifies checksums and
# every number in NOTE.md (14 --check). NOTE.pdf is built separately by
# 20_pdf.py (needs playwright + Chromium).
# Exits non-zero if any step fails. CHECKSUMS.md5 and number_manifest.csv are
# never written here; regenerate them by hand, last, with
#   python3 lta-ab/14_manifest.py
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== lta-ab: python and packages"
python3 --version
python3 -c "import pandas, pypdf, matplotlib; print('pandas', pandas.__version__, '| pypdf', pypdf.__version__, '| matplotlib', matplotlib.__version__)"

echo; echo "== 10 facts, from lta-ab/raw/ (cut-off: October 2026, exercise 1)"
python3 lta-ab/10_facts.py

echo; echo "== 12 Figure 1 (matplotlib, Source Sans 3 from lta-ab/fonts/)"
python3 lta-ab/12_figures.py

echo; echo "== 14 checksums and number manifest, verified"
python3 lta-ab/14_manifest.py --check

echo; echo "lta-ab run_all.sh completed, all checksums verified"
