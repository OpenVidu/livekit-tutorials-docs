#!/usr/bin/env bash
# PostToolUse hook: after editing a tutorial page or a shared snippet, check that
# this site and openvidu.io still say the same thing (~0.2 s).
#
# Drift goes back to Claude via exit 2 so it is fixed in the same turn. Degrades
# to a no-op when the file is out of scope, when python3 is missing, or when
# there is no openvidu.io checkout next door — a hook that fails for reasons the
# author cannot act on gets disabled.

file=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null) || exit 0
[ -n "$file" ] || exit 0

case "$file" in
  */docs/tutorials/*.md | */shared/*.md) ;;
  *) exit 0 ;;
esac

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
[ -d ../openvidu.io ] || exit 0
command -v python3 >/dev/null 2>&1 || exit 0

if ! output=$(python3 tools/sync-check.py 2>&1); then
  printf 'This site and openvidu.io now disagree:\n\n%s\n' "$output" >&2
  exit 2
fi
exit 0
