#!/bin/sh
# Every test under scripts/tests. Exit non-zero if any fails.
set -e
cd "$(dirname "$0")/../.."
for t in scripts/tests/test_*.py; do
  python3 "$t"
done
