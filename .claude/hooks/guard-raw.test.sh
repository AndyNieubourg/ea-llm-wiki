#!/bin/sh
# Acceptance tests for guard-raw.sh, the wiki's write guard.
#
# Run:  sh .claude/hooks/guard-raw.test.sh
# Exit: 0 all passed, 1 one or more failed.
#
# Builds PreToolUse payloads by hand, pipes them into the hook, and asserts the
# permissionDecision. Nothing real is written or read: the hook only reads stdin
# and stats paths.
#
# Self-contained on purpose. The fixture is built in a temp directory at run
# time and removed afterwards, so this test carries no dependency on the owner's
# local paths, on the material under raw/, or on a committed fixture.
# Two reasons that matters. raw/ is gitignored and absent from every worktree
# and from a fresh clone, so a test reaching into it would pass on one machine
# and fail everywhere else. And a committed fixture would need its own
# CLAUDE.md, which the guard uses as its wiki-root marker, and Claude Code reads
# every nested CLAUDE.md as project instructions.
#
# The guard finds a wiki root structurally: an ancestor directory named raw
# whose parent holds both wiki/ and CLAUDE.md. The temp fixture reproduces that
# shape. The second "main checkout" root that case (g) needs is wired in through
# WIKI_GUARD_EXTRA_ROOTS rather than by touching the real one.
#
# This file is exempt from the guard's own secret scan, alongside guard-raw.sh.
# It has to be: a test for a private-key detector that carries no
# private-key-shaped string tests nothing.

set -u

HOOK=$(cd "$(dirname "$0")" && pwd)/guard-raw.sh
[ -f "$HOOK" ] || { echo "guard-raw.sh not found beside this test at $HOOK"; exit 2; }
command -v jq >/dev/null 2>&1 || { echo "these tests need jq to build payloads"; exit 2; }

# --- fixture ------------------------------------------------------------------
TMP=$(mktemp -d "${TMPDIR:-/tmp}/guard-raw-test.XXXXXX") || exit 2
trap 'rm -rf "$TMP"' EXIT INT TERM

FIX="$TMP/worktree"        # stands in for a worktree checkout
MAIN="$TMP/main-checkout"  # stands in for the main checkout, where raw/ really lives
for root in "$FIX" "$MAIN"; do
  mkdir -p "$root/wiki/sources" "$root/wiki/concepts" "$root/wiki/inbox" \
           "$root/wiki/attachments" "$root/raw/Data Management"
  printf 'fixture root for guard-raw.test.sh\n' > "$root/CLAUDE.md"
done
printf 'existing raw source document\n' > "$FIX/raw/Data Management/existing-source.md"
printf 'existing raw source document\n' > "$MAIN/raw/Data Management/existing-source.md"
printf 'exists only in the main checkout\n' > "$MAIN/raw/Data Management/only-in-main.pdf"
mkdir -p "$FIX/unrelated/raw"
printf 'not protected\n' > "$FIX/unrelated/raw/somefile.md"

WIKI_GUARD_EXTRA_ROOTS="$MAIN"
export WIKI_GUARD_EXTRA_ROOTS

# A PEM header assembled at run time, so this file carries no contiguous
# private-key-shaped literal even though the exemption above would allow one.
PEM_OPEN="-----BEGIN OPENSSH PRIVATE $(printf 'KEY')-----"
PEM_CLOSE="-----END OPENSSH PRIVATE $(printf 'KEY')-----"
PEM_RSA="-----BEGIN RSA PRIVATE $(printf 'KEY')-----"
JWT="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

PASS=0
FAIL=0
FAILED_IDS=""

# run_case <id> <deny|allow> <description> <payload-json>
run_case() {
  id=$1; expected=$2; desc=$3; payload=$4
  out=$(printf '%s' "$payload" | sh "$HOOK" 2>&1)
  rc=$?
  if [ -n "$out" ]; then
    decision=$(printf '%s' "$out" | jq -r '.hookSpecificOutput.permissionDecision // "MALFORMED"' 2>/dev/null)
    [ -n "$decision" ] || decision="MALFORMED"
  else
    decision="allow-silent-$rc"
  fi
  case "$expected:$decision" in
    deny:deny)            verdict="PASS" ;;
    allow:allow-silent-0) verdict="PASS" ;;
    *)                    verdict="FAIL" ;;
  esac
  if [ "$verdict" = "PASS" ]; then
    PASS=$((PASS+1))
  else
    FAIL=$((FAIL+1)); FAILED_IDS="$FAILED_IDS $id"
  fi
  printf '%-5s %-5s  expect %-5s  got %-16s %s\n' "($id)" "$verdict" "$expected" "$decision" "$desc"
}

echo "guard-raw.sh acceptance run"
echo "hook    : $HOOK"
echo "---------------------------------------------------------------------------"

# --- raw/ immutability --------------------------------------------------------
run_case a deny "Edit of an existing raw/ file, absolute path" "$(jq -nc \
  --arg cwd "$FIX" --arg p "$FIX/raw/Data Management/existing-source.md" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Edit",tool_input:{file_path:$p,old_string:"existing",new_string:"tampered"}}')"

run_case b deny "Write over an existing raw/ file, relative path plus cwd" "$(jq -nc \
  --arg cwd "$FIX" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:"raw/Data Management/existing-source.md",content:"replaced"}}')"

run_case c allow "Write a NEW file under raw/, the ingest-filing exception" "$(jq -nc \
  --arg cwd "$FIX" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:"raw/Data Management/newly-attached-deck.md",content:"# a freshly attached source"}}')"

run_case d allow "Normal wiki/ write" "$(jq -nc \
  --arg cwd "$FIX" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:"wiki/sources/dama-dmbok2.md",content:"---\ntitle: DAMA-DMBOK2\ntype: source\n---\nEleven knowledge areas."}}')"

run_case e deny "Edit of a raw/ file in another checkout, by absolute path" "$(jq -nc \
  --arg cwd "$FIX" --arg p "$MAIN/raw/Data Management/existing-source.md" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Edit",tool_input:{file_path:$p,old_string:"a",new_string:"b"}}')"

run_case g deny "Write to a worktree raw/ path that exists only in the main checkout" "$(jq -nc \
  --arg cwd "$FIX" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:"raw/Data Management/only-in-main.pdf",content:"shadow copy"}}')"

run_case h deny "Path traversal, wiki/sources/../../raw/<existing>" "$(jq -nc \
  --arg cwd "$FIX" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:"wiki/sources/../../raw/Data Management/existing-source.md",content:"sneaky"}}')"

run_case i allow "Edit under an unrelated raw/ dir, no wiki root above it" "$(jq -nc \
  --arg cwd "$FIX" --arg p "$FIX/unrelated/raw/somefile.md" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Edit",tool_input:{file_path:$p,old_string:"a",new_string:"b"}}')"

run_case m deny "MultiEdit of an existing raw/ file" "$(jq -nc \
  --arg cwd "$FIX" --arg p "$FIX/raw/Data Management/existing-source.md" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"MultiEdit",tool_input:{file_path:$p,edits:[{old_string:"existing",new_string:"tampered"}]}}')"

run_case n deny "NotebookEdit under raw/, which uses notebook_path not file_path" "$(jq -nc \
  --arg cwd "$FIX" --arg p "$FIX/raw/Data Management/analysis.ipynb" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"NotebookEdit",tool_input:{notebook_path:$p,new_source:"print(1)"}}')"

run_case o allow "Read of a raw/ file, the guard must not touch reads" "$(jq -nc \
  --arg cwd "$FIX" --arg p "$FIX/raw/Data Management/existing-source.md" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Read",tool_input:{file_path:$p}}')"

# --- secret detection ---------------------------------------------------------
run_case f deny "wiki/ content carrying a PEM private-key header" "$(jq -nc \
  --arg cwd "$FIX" --arg body "$PEM_OPEN
b3BlbnNzaC1rZXktdjEAAAAABG5vbmU
$PEM_CLOSE" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:"wiki/sources/deploy-notes.md",content:$body}}')"

run_case j allow "wiki/ prose ABOUT api keys, tokens and the EU AI Act" "$(jq -nc \
  --arg cwd "$FIX" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:"wiki/concepts/api-key-management.md",content:"An API key is a bearer credential. EU AI Act Article 15 asks for accuracy, robustness and cybersecurity. Rotate the token every 90 days; never commit an api_key to git. Placeholder: api_key = YOUR_KEY_HERE"}}')"

# j2 and j3 pin the boundary the guard actually draws. A long high-entropy run
# is not enough on its own; it needs a keyword and a separator in front of it.
run_case j2 allow "a bare JWT in prose, no keyword or separator before it" "$(jq -nc \
  --arg cwd "$FIX" --arg body "A JWT looks like $JWT on the wire." \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:"wiki/concepts/jwt.md",content:$body}}')"

run_case j3 deny "the same JWT behind a keyword and a separator" "$(jq -nc \
  --arg cwd "$FIX" --arg body "auth_token: ${JWT}aaaaaaaaaaaaaa" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:"wiki/inbox/scratch.md",content:$body}}')"

run_case k deny "wiki/ content carrying an AWS access key id and secret" "$(jq -nc \
  --arg cwd "$FIX" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:"wiki/inbox/scratch.md",content:"aws_access_key_id = AKIAIOSFODNN7EXAMPLE\naws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"}}')"

run_case l deny "a .pem file anywhere in the repo" "$(jq -nc \
  --arg cwd "$FIX" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:"wiki/attachments/server.pem",content:"placeholder"}}')"

run_case p deny "a NEW raw/ file whose content is a private key, secret guard wins" "$(jq -nc \
  --arg cwd "$FIX" --arg body "$PEM_RSA
MIIEpAIBAAK" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:"raw/new-key.txt",content:$body}}')"

run_case q deny "a .env file" "$(jq -nc \
  --arg cwd "$FIX" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:".env",content:"AWS_REGION=eu-west-1"}}')"

run_case r allow "a .env.example placeholder" "$(jq -nc \
  --arg cwd "$FIX" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:".env.example",content:"AWS_REGION="}}')"

# --- project skills stay writable ---------------------------------------------
mkdir -p "$FIX/.claude/skills/deep-recon" "$FIX/.claude/hooks"

run_case v1 allow "Write to a project-skill directory under .claude/skills/" "$(jq -nc \
  --arg cwd "$FIX" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:".claude/skills/deep-recon/SKILL.md",content:"---\nname: deep-recon\n---"}}')"

# --- fail-closed --------------------------------------------------------------
run_case s deny "a malformed, non-JSON payload" "not json at all"

# --- environment cases, asserted rather than printed --------------------------
t_out=$(printf '' | sh "$HOOK" 2>&1); t_rc=$?
if [ -z "$t_out" ] && [ "$t_rc" -eq 0 ]; then
  PASS=$((PASS+1)); printf '%-5s %-5s  empty stdin is a silent allow\n' "(t)" "PASS"
else
  FAIL=$((FAIL+1)); FAILED_IDS="$FAILED_IDS t"
  printf '%-5s %-5s  empty stdin: exit %s, output %s\n' "(t)" "FAIL" "$t_rc" "'$t_out'"
fi

NOJQ="$TMP/nojq-bin"; mkdir -p "$NOJQ"
for c in awk grep sed cat; do
  cbin=$(command -v "$c") && ln -sf "$cbin" "$NOJQ/$c"
done
u_out=$(jq -nc --arg cwd "$FIX" '{tool_name:"Write",cwd:$cwd,tool_input:{file_path:"wiki/x.md",content:"hi"}}' \
  | env -i PATH="$NOJQ" /bin/sh "$HOOK" 2>&1)
case "$u_out" in
  *'permissionDecision"'*deny*|*'permissionDecision":"deny"'*)
    PASS=$((PASS+1)); printf '%-5s %-5s  jq absent fails closed with a deny\n' "(u)" "PASS" ;;
  *)
    FAIL=$((FAIL+1)); FAILED_IDS="$FAILED_IDS u"
    printf '%-5s %-5s  jq absent did NOT deny: %s\n' "(u)" "FAIL" "$u_out" ;;
esac

echo "---------------------------------------------------------------------------"
echo "TOTAL: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || { echo "failed:$FAILED_IDS"; exit 1; }
echo
echo "NOT covered by this run:"
echo "  - Bash. rm, mv and sed -i under raw/ are intercepted by no hook."
echo "  - Whether Claude Code honours the deny. This asserts the script's answer,"
echo "    not the harness acting on it. Only a live tool call proves that."
exit 0
