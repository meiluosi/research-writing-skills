#!/usr/bin/env sh
# install.sh [--copy] [--with-references] [DEST]
# Links (or copies) the skills into DEST (default ~/.claude/skills): every skill of this repository plus the three bundled external skills
# (human-in-the-loop-writing, rewrite-fidelity-skill, zh-disambiguate-skill). --with-references also installs the three reference forks
# (humanizer, stop-slop, avoid-ai-writing); skip them if you already have the upstream versions.
set -eu
mode=link; refs=0
while [ $# -gt 0 ]; do case "$1" in --copy) mode=copy; shift;; --with-references) refs=1; shift;; *) break;; esac; done
dest=${1:-$HOME/.claude/skills}
repo=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$dest"
put() { d=$1; n=$(basename "$d"); if [ -e "$dest/$n" ]; then echo "skip $n (exists in $dest)"; return; fi
        if [ "$mode" = copy ]; then cp -R "$d" "$dest/$n"; else ln -s "$d" "$dest/$n"; fi; echo "$mode $n"; }
for d in "$repo"/0*-*/*/; do [ -f "$d/SKILL.md" ] && put "${d%/}"; done
put "$repo/external/human-in-the-loop-writing/skills/human-in-the-loop-writing"
put "$repo/external/rewrite-fidelity-skill"
put "$repo/external/zh-disambiguate-skill"
if [ "$refs" = 1 ]; then put "$repo/external/humanizer"; put "$repo/external/stop-slop"; put "$repo/external/avoid-ai-writing/skills/avoid-ai-writing"; fi
