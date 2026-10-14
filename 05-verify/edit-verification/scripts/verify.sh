#!/usr/bin/env sh
# verify.sh BEFORE AFTER   -> runs rewrite-fidelity (mechanical meaning check) and prints its RESULT line, then the number comparison.
# Looks for fidelity.py in this repo's submodule, then in ~/.claude/skills. Exit code follows rewrite-fidelity (1 on FAIL), 3 if it is not found.
set -u
here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../../.." && pwd)
fid=""
for f in "$repo/external/rewrite-fidelity-skill/scripts/fidelity.py" "$HOME/.claude/skills/rewrite-fidelity-skill/scripts/fidelity.py" "$HOME/.claude/skills/rewrite-fidelity/scripts/fidelity.py"; do
  if [ -f "$f" ]; then fid="$f"; break; fi
done
if [ -z "$fid" ]; then echo "rewrite-fidelity not found. Run: git submodule update --init external/rewrite-fidelity-skill" >&2; exit 3; fi
python3 "$fid" "$1" "$2"; rc=$?
dm="$repo/03-structure/result-writeup-editor/scripts/doc_metrics.py"
if [ -f "$dm" ]; then echo; python3 "$dm" --compare "$1" "$2"; fi
exit $rc
