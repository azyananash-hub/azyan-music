#!/usr/bin/env bash
# Deeper static read of one cached candidate. Reads files only; never executes repository content.
# Usage: deep.sh <owner__repo>   (cache folder name under /home/user/ext/research-cache)
set -u
D="/home/user/ext/research-cache/$1"
cd "$D" || { echo "missing $D"; exit 0; }
echo "### $1"
echo "## LICENSE (first lines)"
for f in $(ls -1 | grep -iE '^(LICEN[SC]E|COPYING|license)' | head -2); do
  echo "-- $f:"; head -n 3 "$f" | cut -c1-110
done
echo "## README essentials (non-HTML lines)"
RD=$(ls -1 | grep -iE '^README' | head -1)
[ -n "$RD" ] && grep -vE '^[[:space:]]*(<|$|!\[|\[!\[|\|)' "$RD" | head -n 10 | cut -c1-160
echo "## external hosts referenced by code (top 10)"
grep -rhoIE 'https?://[A-Za-z0-9.-]+' --include='*.py' --include='*.js' --include='*.mjs' --include='*.cjs' --include='*.ts' --include='*.tsx' --include='*.jsx' --include='*.dart' --include='*.go' --include='*.rs' --include='*.java' --include='*.kt' --include='*.swift' --include='*.sh' --include='*.ps1' --exclude-dir=.git --exclude-dir=node_modules . 2>/dev/null | sort | uniq -c | sort -rn | head -10
echo "## pipe-to-shell lines (6)"
grep -rnIE --exclude-dir=.git -E 'curl[^|]*\|[[:space:]]*(sudo[[:space:]]+)?(ba|z)?sh' . 2>/dev/null | cut -c1-150 | head -6
echo "## root lifecycle scripts"
[ -f package.json ] && python3 -I -c "import json;d=json.load(open('package.json'));print({k:v for k,v in (d.get('scripts') or {}).items() if k in ('preinstall','postinstall','prepare','install')})" 2>/dev/null
echo "## hooks / MCP configs (first 14 lines, max 3 files)"
for f in $(find . -path ./.git -prune -o -type f \( -name hooks.json -o -name '.mcp.json' -o -name 'mcp.json' \) -print | sed 's#^\./##' | head -3); do
  echo "-- $f"; head -n 14 "$f" | cut -c1-140
done
