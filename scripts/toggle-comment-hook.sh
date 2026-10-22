#!/usr/bin/env bash
set -euo pipefail

# Enables/disables the detect-new-comments Pre/PostToolUse hook pair in
# ~/.claude/settings.json without hand-editing JSON.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
HOOK_SCRIPT="$REPO/hooks/detect-new-comments.py"
PRE_CMD="$HOOK_SCRIPT pre"
POST_CMD="$HOOK_SCRIPT post"
SETTINGS="$HOME/.claude/settings.json"
MATCHER="Write|Edit"

usage() {
  echo "usage: $0 [enable|disable|status]" >&2
  exit 1
}

[ $# -eq 1 ] || usage

case "$1" in
  enable)
    tmp="$(mktemp)"
    jq --arg pre "$PRE_CMD" --arg post "$POST_CMD" --arg matcher "$MATCHER" '
      .hooks.PreToolUse //= [] |
      .hooks.PreToolUse |= (map(select(.hooks[0].command != $pre)) + [{
        matcher: $matcher,
        hooks: [{type: "command", command: $pre}]
      }]) |
      .hooks.PostToolUse //= [] |
      .hooks.PostToolUse |= (map(select(.hooks[0].command != $post)) + [{
        matcher: $matcher,
        hooks: [{type: "command", command: $post}]
      }])
    ' "$SETTINGS" > "$tmp"
    mv "$tmp" "$SETTINGS"
    echo "enabled: $HOOK_SCRIPT (pre+post) on $MATCHER"
    ;;
  disable)
    tmp="$(mktemp)"
    jq --arg pre "$PRE_CMD" --arg post "$POST_CMD" '
      .hooks.PreToolUse |= (if . then map(select(.hooks[0].command != $pre)) else . end) |
      .hooks.PostToolUse |= (if . then map(select(.hooks[0].command != $post)) else . end)
    ' "$SETTINGS" > "$tmp"
    mv "$tmp" "$SETTINGS"
    echo "disabled: $HOOK_SCRIPT"
    ;;
  status)
    pre_on="$(jq -e --arg pre "$PRE_CMD" '.hooks.PreToolUse // [] | any(.hooks[0].command == $pre)' "$SETTINGS" >/dev/null && echo yes || echo no)"
    post_on="$(jq -e --arg post "$POST_CMD" '.hooks.PostToolUse // [] | any(.hooks[0].command == $post)' "$SETTINGS" >/dev/null && echo yes || echo no)"
    if [ "$pre_on" = yes ] && [ "$post_on" = yes ]; then
      echo "enabled"
    elif [ "$pre_on" = no ] && [ "$post_on" = no ]; then
      echo "disabled"
    else
      echo "partial (pre=$pre_on post=$post_on)"
    fi
    ;;
  *)
    usage
    ;;
esac
