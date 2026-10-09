#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 build_site.py
if [ -f .private_terms ] && grep -rliF -f .private_terms --exclude=.private_terms --exclude-dir=.git . ; then echo "Forbidden string found; aborting"; exit 1; fi
git add -A
git commit -m "${1:-Update practice pages}" || echo "nothing to commit"
git push origin main
