#!/bin/sh
# PreToolUse write guard for this wiki.
#
# Two jobs, one hook, matched on Write|Edit|MultiEdit|NotebookEdit:
#
#   1. raw/ immutability. CLAUDE.md ("Who I am, and why this wiki exists") makes
#      raw/ read-only with exactly two documented exceptions: reorganisation on
#      the owner's explicit per-action permission, and filing a newly attached
#      file before an ingest. Both ADD; neither MODIFIES. So this hook denies
#      every edit of an existing raw file and every write over one, and lets a
#      write that creates a new raw file through.
#   2. Secret detection. Private keys and credential files never belong in this
#      repo, raw/ or not. The pattern set is deliberately small: the wiki holds
#      prose ABOUT API keys and regulatory text, so matching is on file path and
#      on value shape, never on the mere word "token".
#
# Contract (Claude Code PreToolUse, verified against code.claude.com/docs/en/hooks
# on 2026-08-04, CLI 2.1.179): JSON on stdin with tool_name / tool_input / cwd;
# a deny is exit 0 plus
#   {"hookSpecificOutput":{"hookEventName":"PreToolUse",
#    "permissionDecision":"deny","permissionDecisionReason":"..."}}
# on stdout. Exit 0 with no stdout means "no decision, normal permission flow".
#
# Dependency: jq. Missing jq FAILS CLOSED (denies) rather than waving writes
# through: a guard that cannot evaluate a write must not wave it through.

set -u

# --- output helpers -----------------------------------------------------------

deny() {
  # $1 = reason text
  jq -n --arg r "$1" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
  exit 0
}

allow_silently() { exit 0; }

if ! command -v jq >/dev/null 2>&1; then
  # Hand-rolled JSON so this path needs no jq itself.
  printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"guard-raw.sh cannot run: jq is not installed, so the raw/ write guard and secret scan cannot evaluate this call. Failing closed. Install jq (brew install jq / apt-get install jq) or disable the PreToolUse hook in .claude/settings.json."}}'
  exit 0
fi

# --- read the hook payload ----------------------------------------------------

INPUT=$(cat)
# Empty stdin is not a tool call. Anything else must be valid JSON: a payload the
# guard cannot parse is a payload it cannot clear, so that denies rather than
# waving the write through.
[ -n "$INPUT" ] || allow_silently
if ! printf '%s' "$INPUT" | jq -e . >/dev/null 2>&1; then
  deny "guard-raw.sh received a PreToolUse payload it could not parse as JSON, so it cannot tell whether this write targets raw/ or carries credentials. Failing closed."
fi

TOOL=$(printf '%s' "$INPUT" | jq -r '.tool_name // ""')
case "$TOOL" in
  Write|Edit|MultiEdit|NotebookEdit) ;;
  *) allow_silently ;;
esac

HOOK_CWD=$(printf '%s' "$INPUT" | jq -r '.cwd // ""')
[ -n "$HOOK_CWD" ] || HOOK_CWD=$PWD

# NotebookEdit carries notebook_path; the rest carry file_path.
TARGET=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // .tool_input.notebook_path // ""')
[ -n "$TARGET" ] || allow_silently

# Everything that will land in the file, across the four tools.
CONTENT=$(printf '%s' "$INPUT" | jq -r '
  [ (.tool_input.content // empty)
  , (.tool_input.new_string // empty)
  , (.tool_input.new_source // empty)
  , ((.tool_input.edits // []) | .[]? | (.new_string // empty))
  ] | join("\n")')

# --- path resolution ----------------------------------------------------------

# Absolute, with . and .. collapsed lexically. Lexical is the right call here:
# ".." must not be resolvable through a symlink into raw/ and then be waved
# through because the literal string did not say "raw".
case "$TARGET" in
  /*) ABS=$TARGET ;;
  *)  ABS="$HOOK_CWD/$TARGET" ;;
esac

ABS=$(printf '%s\n' "$ABS" | awk '
{
  n = split($0, seg, "/"); top = 0;
  for (i = 1; i <= n; i++) {
    s = seg[i];
    if (s == "" || s == ".") continue;
    if (s == "..") { if (top > 0) top--; continue; }
    stack[++top] = s;
  }
  out = "";
  for (i = 1; i <= top; i++) out = out "/" stack[i];
  if (out == "") out = "/";
  print out;
}')

BASENAME=${ABS##*/}

# --- 1. secret detection ------------------------------------------------------

# This script carries the patterns it looks for, so it would flag itself. Its
# test file has to carry them too: a test for a private-key detector that holds
# no private-key-shaped string tests nothing. Both are exempt, and nothing else
# is. Confirmed the hard way on 2026-08-04, when the guard blocked the very file
# written to prove it works.
case "$ABS" in
  */.claude/hooks/guard-raw.sh|*/.claude/hooks/guard-raw.test.sh) SKIP_SECRET_SCAN=1 ;;
  *) SKIP_SECRET_SCAN=0 ;;
esac

if [ "$SKIP_SECRET_SCAN" -eq 0 ]; then
  # Credential-file paths. .env.example / .env.sample / .env.template are
  # placeholders by convention and stay allowed.
  case "$BASENAME" in
    .env.example|.env.sample|.env.template) : ;;
    .env|.env.*)
      deny "Blocked by .claude/hooks/guard-raw.sh (secret guard): '$BASENAME' is an environment file, which holds credentials by convention. Nothing in this wiki needs one. Path: $ABS" ;;
    id_rsa|id_dsa|id_ecdsa|id_ed25519)
      deny "Blocked by .claude/hooks/guard-raw.sh (secret guard): '$BASENAME' is an SSH private key filename. Private keys never belong in this repo. Path: $ABS" ;;
    *.pem|*.p12|*.pfx|*.key)
      deny "Blocked by .claude/hooks/guard-raw.sh (secret guard): '$BASENAME' has a private-key / certificate-bundle extension. Private key material never belongs in this repo. Path: $ABS" ;;
  esac

  # Value-shaped content patterns. Field separator is '~' because the patterns
  # themselves use '|' for alternation.
  if [ -n "$CONTENT" ]; then
    FINDING=""
    while IFS='~' read -r LABEL PATTERN; do
      [ -n "${LABEL:-}" ] || continue
      case "$LABEL" in \#*) continue ;; esac
      if printf '%s' "$CONTENT" | LC_ALL=C grep -Eq -- "$PATTERN" 2>/dev/null; then
        FINDING=$LABEL
        break
      fi
    done <<'PATTERNS'
private key material (PEM block header)~-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----
AWS access key id~AKIA[0-9A-Z]{16}
AWS secret access key assignment~aws_secret_access_key[[:space:]]*[:=][[:space:]]*['"]?[A-Za-z0-9/+=]{40}
credential assignment with a high-entropy value~(api[_-]?key|apikey|secret[_-]?key|client[_-]?secret|access[_-]?token|auth[_-]?token|token|password)[[:space:]]*[:=][[:space:]]*['"]?[A-Za-z0-9/+=_-]{32,}
known provider credential~(sk-ant-[A-Za-z0-9_-]{24,}|ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}|xox[baprs]-[0-9A-Za-z-]{12,}|AIza[0-9A-Za-z_-]{35})
PATTERNS

    if [ -n "$FINDING" ]; then
      deny "Blocked by .claude/hooks/guard-raw.sh (secret guard): the content being written matches $FINDING. Path: $ABS. Remove the credential, or if this is prose about credentials rather than a real one, reword it so it does not look like an assignment with a high-entropy value."
    fi
  fi
fi

# --- 2. raw/ immutability -----------------------------------------------------

# Known wiki roots. The structural test below covers the normal cases; this
# list exists so the MAIN CHECKOUT stays protected even if its layout markers
# ever move, because raw/ is gitignored and empty inside every worktree while
# the real source documents live only in the main checkout.
# {{MAIN_CHECKOUT_PATH}} is filled during /init-wiki with the absolute path of
# the owner's main checkout (the parent of {{RAW_MAIN_PATH}}). Until then it is
# a harmless non-path and the structural test stands alone.
MAIN_CHECKOUT="{{MAIN_CHECKOUT_PATH}}"
KNOWN_ROOTS="$MAIN_CHECKOUT"
# Colon-separated extra roots, for tests and for a relocated checkout.
if [ -n "${WIKI_GUARD_EXTRA_ROOTS:-}" ]; then
  KNOWN_ROOTS="$KNOWN_ROOTS:$WIKI_GUARD_EXTRA_ROOTS"
fi

is_wiki_root() {
  # A directory is an llm-wiki root when it carries the wiki and the manual, or
  # when it is named as a known root.
  if [ -d "$1/wiki" ] && [ -f "$1/CLAUDE.md" ]; then
    return 0
  fi
  OLD_IFS=$IFS
  IFS=':'
  for R in $KNOWN_ROOTS; do
    if [ -n "$R" ] && [ "$R" = "$1" ]; then
      IFS=$OLD_IFS
      return 0
    fi
  done
  IFS=$OLD_IFS
  return 1
}

RAW_DIR=""
RAW_ROOT=""
DIR=${ABS%/*}
[ -n "$DIR" ] || DIR="/"
while [ "$DIR" != "/" ]; do
  if [ "${DIR##*/}" = "raw" ]; then
    PARENT=${DIR%/*}
    [ -n "$PARENT" ] || PARENT="/"
    if is_wiki_root "$PARENT"; then
      RAW_DIR=$DIR
      RAW_ROOT=$PARENT
      break
    fi
  fi
  DIR=${DIR%/*}
  [ -n "$DIR" ] || DIR="/"
done

[ -n "$RAW_DIR" ] || allow_silently   # not under a wiki raw/ — nothing more to check

RELPATH=${ABS#"$RAW_DIR"/}
RULE="CLAUDE.md, \"Who I am, and why this wiki exists\": raw/ is immutable. The only two exceptions are reorganising raw/ after the owner has given explicit permission for that specific action, and filing a newly attached file before an ingest. Both ADD a file; neither modifies one."

case "$TOOL" in
  Edit|MultiEdit|NotebookEdit)
    deny "Blocked by .claude/hooks/guard-raw.sh: $TOOL would modify a source document under raw/.
Path: $ABS
Rule: $RULE
If the raw file genuinely has to change, do it yourself outside Claude Code. If you meant to record what the source says, write to wiki/sources/ instead."
    ;;
  Write)
    if [ -e "$ABS" ]; then
      deny "Blocked by .claude/hooks/guard-raw.sh: Write would overwrite an existing source document under raw/.
Path: $ABS
Rule: $RULE
Adding a NEW file under raw/ is allowed; replacing this one is not."
    fi
    # Worktree case: raw/ is gitignored, so a worktree's raw/ is empty and a
    # write there looks new even when the real document exists in the main
    # checkout. Without this check the guard would let an agent create a
    # divergent shadow copy of a protected file.
    OLD_IFS=$IFS
    IFS=':'
    for R in $KNOWN_ROOTS; do
      [ -n "$R" ] || continue
      [ "$R" = "$RAW_ROOT" ] && continue
      if [ -e "$R/raw/$RELPATH" ]; then
        IFS=$OLD_IFS
        deny "Blocked by .claude/hooks/guard-raw.sh: Write targets raw/$RELPATH, which does not exist here but DOES exist in the main checkout at $R/raw/$RELPATH.
Path: $ABS
Rule: $RULE
raw/ is gitignored, so a worktree's raw/ is empty while the real source documents live only in the main checkout. Writing here would create a divergent shadow copy of a protected file."
      fi
    done
    IFS=$OLD_IFS
    ;;
esac

# New file under raw/ — the documented ingest-filing exception. Allowed.
exit 0
