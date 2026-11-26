#!/usr/bin/env bash
# Static triage for one candidate repository.
# Clones only (no checkout hooks, LFS smudge skipped). Never executes repository content.
# Usage: triage.sh <id> <https://github.com/owner/repo>
set -u
export GIT_TERMINAL_PROMPT=0 GIT_LFS_SKIP_SMUDGE=1
ID="$1"
URL="$2"
CACHE=/home/user/ext/research-cache
mkdir -p "$CACHE"
NAME=$(printf '%s' "${URL#https://github.com/}" | sed -e 's#/#__#' -e 's#\.git$##')
D="$CACHE/$NAME"
if [ ! -d "$D/.git" ]; then
  rm -rf "$D"
  if ! timeout 900 git clone -q --depth 1 "$URL" "$D" 2>"$CACHE/$NAME.err"; then
    echo "$ID|$NAME|CLONE_FAIL|$(head -c 200 "$CACHE/$NAME.err" | tr '\n' ' ')"
    exit 0
  fi
fi
cd "$D" || exit 0
EX=(--exclude-dir=.git --exclude-dir=node_modules)
CODE=(--include='*.py' --include='*.js' --include='*.mjs' --include='*.cjs' --include='*.ts' --include='*.tsx' --include='*.jsx' --include='*.dart' --include='*.go' --include='*.rs' --include='*.java' --include='*.kt' --include='*.swift' --include='*.sh' --include='*.ps1' --include='*.rb' --include='*.php' --include='*.cs')
COMMIT=$(git rev-parse --short=12 HEAD)
FILES=$(git ls-files | wc -l)
SIZE_MB=$(du -sm --exclude=.git . | cut -f1)
SKILLS=$(find . -path ./.git -prune -o -name SKILL.md -print | wc -l)
LICF=$(ls -1 | grep -iE '^(LICEN[SC]E|COPYING|NOTICE)' | head -3 | tr '\n' ',')
LIC=NONE
F1=$(ls -1 | grep -iE '^(LICEN[SC]E|COPYING)' | head -1)
if [ -n "$F1" ]; then
  H=$(head -c 6000 "$F1")
  case "$H" in
    *"GNU AFFERO"*) LIC=AGPL-3.0 ;;
    *"GNU LESSER"*) LIC=LGPL ;;
    *"GNU GENERAL PUBLIC"*) LIC=GPL ;;
    *"Apache License"*) LIC=Apache-2.0 ;;
    *"Commons Clause"*) LIC=Commons-Clause ;;
    *"MIT License"*|*"Permission is hereby granted, free of charge"*) LIC=MIT ;;
    *"Redistribution and use in source and binary"*) LIC=BSD ;;
    *"Mozilla Public License"*) LIC=MPL-2.0 ;;
    *) LIC=OTHER ;;
  esac
fi
HOOKS=$(find . -path ./.git -prune -o -type f \( -name hooks.json -o -path '*/hooks/*' -o -path '*/.claude/settings*.json' \) -print | wc -l)
PLUG=$(find . -path ./.git -prune -o -type f \( -name plugin.json -o -name marketplace.json -o -name skill.json -o -name gemini-extension.json -o -path '*/.claude-plugin/*' -o -path '*/.cursor-plugin/*' -o -path '*/.codex-plugin/*' \) -print | sed 's#^\./##' | head -6 | tr '\n' ' ')
AGENT=$(ls -1 | grep -E '^(AGENTS|CLAUDE|GEMINI)\.md$|^\.cursorrules$' | tr '\n' ' ')
MCP=$(find . -path ./.git -prune -o -type f \( -name '.mcp.json' -o -name 'mcp.json' -o -name 'mcp_config*.json' \) -print | sed 's#^\./##' | head -6 | tr '\n' ' ')
INST=$(find . -path ./.git -prune -o -path '*/node_modules' -prune -o -type f \( -iname 'install*.sh' -o -iname 'install*.ps1' -o -iname 'install*.py' -o -iname 'install*.js' -o -iname 'install*.mjs' -o -iname 'install*.ts' -o -iname 'setup*.sh' -o -iname 'setup*.py' -o -iname 'bootstrap*.sh' \) -print | sed 's#^\./##' | head -6 | tr '\n' ' ')
LIFE=$(grep -rlE --include=package.json '"(pre|post)install"[[:space:]]*:' . 2>/dev/null | grep -v node_modules | wc -l)
ATL=$(grep -rIl --exclude-dir=.git --exclude-dir=node_modules '@latest' . 2>/dev/null | wc -l)
PIPESH=$(grep -rEIl --exclude-dir=.git -E 'curl[^|]*\|[[:space:]]*(sudo[[:space:]]+)?(ba|z)?sh|wget[^|]*\|[[:space:]]*(sudo[[:space:]]+)?(ba|z)?sh|iwr[^|]*\|[[:space:]]*iex' . 2>/dev/null | wc -l)
NET=$(grep -rEI "${CODE[@]}" "${EX[@]}" -E 'requests\.|urllib|httpx|aiohttp|\bfetch\(|axios|http\.request|https\.get|XMLHttpRequest|new WebSocket|net/http|reqwest|OkHttp|HttpClient' . 2>/dev/null | wc -l)
SUBP=$(grep -rEI "${CODE[@]}" "${EX[@]}" -E 'subprocess\.|os\.system|child_process|execSync|spawnSync|\bspawn\(|Runtime\.getRuntime|Process\.Start|exec\.Command' . 2>/dev/null | wc -l)
EVAL=$(grep -rEI "${CODE[@]}" "${EX[@]}" -E '\beval\(|new Function\(|pickle\.load|yaml\.load\(|exec\(compile' . 2>/dev/null | wc -l)
CRED=$(grep -rEIil --exclude-dir=.git --exclude-dir=node_modules -E 'API_KEY|apikey|ACCESS_TOKEN|AUTH_TOKEN|SECRET_KEY|client_secret|PASSWORD|sessionid|cookies' . 2>/dev/null | wc -l)
TELEM=$(grep -rEIil --exclude-dir=.git --exclude-dir=node_modules -E 'telemetry|analytics|sentry|posthog|mixpanel|amplitude|google-analytics|gtag\(|datadog|opentelemetry' . 2>/dev/null | wc -l)
MODELS=$(grep -rEIil --exclude-dir=.git --exclude-dir=node_modules -E 'huggingface|\.safetensors|\.gguf|snapshot_download|from_pretrained|ollama pull|model weights' . 2>/dev/null | wc -l)
BIG=$(find . -path ./.git -prune -o -type f -size +5M -print | wc -l)
LFS=$(grep -c 'filter=lfs' .gitattributes 2>/dev/null)
LOCKS=$(ls -1 | grep -E '^(package-lock.json|pnpm-lock.yaml|yarn.lock|bun.lockb?|poetry.lock|uv.lock|Pipfile.lock|Cargo.lock|go.sum|Gemfile.lock)$' | tr '\n' ' ')
RD=$(ls -1 | grep -iE '^README' | head -1)
RT=""
[ -n "$RD" ] && RT=$(head -c 300 "$RD" | tr '\n' ' ' | cut -c1-140)
echo "$ID|$NAME|commit=$COMMIT|LIC=$LIC|licfiles=${LICF:-none}|files=$FILES|sizeMB=$SIZE_MB|SKILL.md=$SKILLS|hooks_files=$HOOKS|plugin=${PLUG:-none}|agentfiles=${AGENT:-none}|mcp=${MCP:-none}|installers=${INST:-none}|lifecycle_pkgs=$LIFE|atlatest_files=$ATL|pipe_sh_files=$PIPESH|net_lines=$NET|subproc_lines=$SUBP|eval_lines=$EVAL|cred_files=$CRED|telem_files=$TELEM|model_files=$MODELS|big5MB=$BIG|lfs=${LFS:-0}|locks=${LOCKS:-none}|readme=${RT}"
