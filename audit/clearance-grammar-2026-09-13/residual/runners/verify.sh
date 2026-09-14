#!/usr/bin/env bash
# Lane F3 verification: the residual classes, run with the independent audit's own runners
# against committed heads, and the same runners against the heads before the lane as the "before".
# usage: bash verify.sh <game commit> <trainer commit> <game commit before> <trainer commit before> <scratch dir>
# Writes graded, parity, suite and summary files into ../outputs beside this script, and the full
# per-input exports into <scratch dir>/exports. Needs Node 18+, Python 3.9+ and pytest.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
GAME_REPO="$(cd "$HERE/../../../.." && pwd)"
TRAINER_REPO="$(cd "$GAME_REPO/../second-pass" && pwd)"
A1="$GAME_REPO/audit/independent-2026-09-13"
IN="$HERE/../inputs"
OUT="$HERE/../outputs"
X="$5/exports"
G="$5/game"; T="$5/trainer"; BG="$5/game-before"; BT="$5/trainer-before"
rm -rf "$G" "$T" "$BG" "$BT" "$X"; mkdir -p "$G" "$T" "$BG" "$BT" "$X" "$OUT"
git -C "$GAME_REPO" archive "$1" | tar -x -C "$G"
git -C "$TRAINER_REPO" archive "$2" | tar -x -C "$T"
git -C "$GAME_REPO" archive "$3" | tar -x -C "$BG"
git -C "$TRAINER_REPO" archive "$4" | tar -x -C "$BT"

echo "== browser suite at $1"
node "$G/tests/run-checker-tests.cjs" > "$OUT/browser-suite.log" || true
tail -1 "$OUT/browser-suite.log"
echo "== python suite at $2, with the browser beside it, and without it"
(cd "$T" && BEAT_THE_MACHINE="$G" python -m pytest tests/ -q -p no:cacheprovider > "$OUT/python-suite.log" 2>&1) || true
tail -1 "$OUT/python-suite.log"
(cd "$T" && BEAT_THE_MACHINE="$5/nowhere" python -m pytest tests/ -q -p no:cacheprovider > "$OUT/python-suite-standalone.log" 2>&1) || true
tail -1 "$OUT/python-suite-standalone.log"
echo "== parity test alone"
(cd "$T" && BEAT_THE_MACHINE="$G" python -m pytest tests/test_parity_shared_inputs.py -q -p no:cacheprovider > "$OUT/parity-suite.log" 2>&1) || true
tail -1 "$OUT/parity-suite.log"

run_set() { # <tree game> <tree trainer> <input file> <name> <suffix>
  node "$A1/runners/run-browser.cjs" "$1" "$3" "$X/$4-browser$5.json" > /dev/null
  python "$A1/runners/run-python.py" "$2" "$3" "$X/$4-python$5.json" > /dev/null
  python "$A1/runners/compare.py" "$X/$4-browser$5.json" "$X/$4-python$5.json" "$X/$4-parity$5.json" | tail -1
}
for set in new-40-probes prior-24-probes six-drafts-as-fixtures a1-probes a1-sizing-probes; do
  name="${set%-probes}"; name="${name%-as-fixtures}"
  echo "== $name, after then before"
  run_set "$G" "$T" "$A1/inputs/$set.json" "$name" ""
  run_set "$BG" "$BT" "$A1/inputs/$set.json" "$name" "-before"
done
for set in neighbour-probes samples; do
  echo "== $set, after then before"
  run_set "$G" "$T" "$IN/$set.json" "$set" ""
  run_set "$BG" "$BT" "$IN/$set.json" "$set" "-before"
done
for sfx in "" "-before"; do
  node "$A1/runners/grade-probes.cjs" "$A1/inputs/a1-probes.json" "$X/a1-browser$sfx.json" "$X/a1-python$sfx.json" "$X/a1-parity$sfx.json" "$X/a1-graded$sfx.json" | head -1
  node "$A1/runners/grade-probes.cjs" "$A1/inputs/a1-sizing-probes.json" "$X/a1-sizing-browser$sfx.json" "$X/a1-sizing-python$sfx.json" "$X/a1-sizing-parity$sfx.json" "$X/a1-sizing-graded$sfx.json" | head -1
done
for f in a1-graded a1-sizing-graded a1-parity a1-sizing-parity new-40-parity prior-24-parity six-drafts-parity neighbour-probes-parity samples-parity; do
  cp "$X/$f.json" "$OUT/$f.json"
done
echo "== the sentence splitter against a person's reading and against Python"
node "$HERE/split-parity.cjs" "$G" "$T" "$IN/split-readings.json" "$OUT/split-parity.json"
echo "== author fold against the checker on every plain fixture"
# run on the working tree: git archive writes CRLF on this machine and the script searches LF text
node "$GAME_REPO/audit/author-repair-2026-09-13/parity-node.cjs" "$GAME_REPO" > "$OUT/author-parity-node.log" || true
tail -1 "$OUT/author-parity-node.log"
echo "== before and after"
node "$HERE/summarize.cjs" "$A1" "$X" "$OUT" "$G"
