#!/usr/bin/env bash
# Lane F1 verification: the independent audit's own runners, run against committed heads.
# usage: bash verify.sh <beat-the-machine commit> <second-pass commit> <scratch dir>
# Writes outputs into ../outputs beside this script. Needs Node 18+, Python 3.9+ and pytest.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
GAME_REPO="$(cd "$HERE/../../.." && pwd)"
TRAINER_REPO="$(cd "$GAME_REPO/../second-pass" && pwd)"
A1="$GAME_REPO/audit/independent-2026-09-13"
OUT="$HERE/../outputs"
G="$3/game"; T="$3/trainer"
rm -rf "$G" "$T"; mkdir -p "$G" "$T" "$OUT"
git -C "$GAME_REPO" archive "$1" | tar -x -C "$G"
git -C "$TRAINER_REPO" archive "$2" | tar -x -C "$T"

echo "== browser suite at $1"
node "$G/tests/run-checker-tests.cjs" > "$OUT/browser-suite.log" || true
tail -1 "$OUT/browser-suite.log"
echo "== python suite at $2, with the browser beside it"
(cd "$T" && BEAT_THE_MACHINE="$G" python -m pytest tests/ -q -p no:cacheprovider > "$OUT/python-suite.log" 2>&1) || true
tail -1 "$OUT/python-suite.log"

for set in new-40-probes prior-24-probes six-drafts-as-fixtures a1-probes a1-sizing-probes; do
  name="${set%-probes}"; name="${name%-as-fixtures}"; name="${name/new-40/new-40}"
  node "$A1/runners/run-browser.cjs" "$G" "$A1/inputs/$set.json" "$OUT/$name-browser.json"
  python "$A1/runners/run-python.py" "$T" "$A1/inputs/$set.json" "$OUT/$name-python.json"
  python "$A1/runners/compare.py" "$OUT/$name-browser.json" "$OUT/$name-python.json" "$OUT/$name-parity.json"
done
node "$A1/runners/grade-probes.cjs" "$A1/inputs/a1-probes.json" "$OUT/a1-browser.json" "$OUT/a1-python.json" "$OUT/a1-parity.json" "$OUT/a1-graded.json"
node "$A1/runners/grade-probes.cjs" "$A1/inputs/a1-sizing-probes.json" "$OUT/a1-sizing-browser.json" "$OUT/a1-sizing-python.json" "$OUT/a1-sizing-parity.json" "$OUT/a1-sizing-graded.json"
echo "== author fold against the checker on every plain fixture"
# run on the working tree: git archive writes CRLF on this machine and the script searches LF text
node "$GAME_REPO/audit/author-repair-2026-09-13/parity-node.cjs" "$GAME_REPO" > "$OUT/author-parity-node.log" || true
tail -1 "$OUT/author-parity-node.log"
echo "== before and after, per class and per input set"
node "$HERE/summarize.cjs" "$A1" "$OUT"
