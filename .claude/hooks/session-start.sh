#!/bin/bash
set -uo pipefail

# Reports skills that are declared but not actually present.
#
# The failure this catches is silent: a skill has a row in the CLAUDE.md skills
# table, the session assumes it is available, and it is not — because setup.sh
# was never run on this clone (the ⬇ rows are installed, not committed), because
# a committed skill directory was renamed or dropped, or because a symlink lost
# its target. A session that believes it loaded a skill it never had produces
# work that silently skipped a mandatory step. So this hook reports the gap into
# the session context, where the session actually reads it, instead of to a
# stderr stream nothing reads.

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}" || exit 0
[ -f CLAUDE.md ] || exit 0

# Skill names declared in the CLAUDE.md skills table: rows shaped
# `| `name` |` or `| ⬇ `name` |` (⬇ marks installed-not-committed skills).
declared=$(grep -E '^\| (⬇ )?`[a-z][a-z-]*`' CLAUDE.md 2>/dev/null |
  sed -E 's/^\| (⬇ )?`([a-z-]+)`.*/\2/' | sort -u)

missing=""
for name in $declared; do
  [ -e ".claude/skills/$name" ] || missing="$missing, $name"
done
missing=${missing#, }

# Dangling symlinks under .claude/skills/ list in `ls` but resolve to nothing,
# so the existence check above can pass while the skill is absent.
dangling=$(find .claude/skills/ -maxdepth 1 -type l ! -exec test -e {} \; -print 2>/dev/null |
  sed 's|.*/||' | sort | paste -sd ',' - | sed 's/,/, /g')

[ -n "$missing$dangling" ] || exit 0

report="SKILLS DECLARED BUT MISSING."
if [ -n "$missing" ]; then
  report="$report These skills have a row in the CLAUDE.md skills table but no entry under .claude/skills/, so they are NOT available in this session: ${missing}. If a missing skill is a ⬇ (installed) row, run setup.sh (or setup.ps1) to install it; if it is a committed skill, the repo itself is missing it."
fi
if [ -n "$dangling" ]; then
  report="$report These entries under .claude/skills/ are symlinks whose target does not exist: ${dangling}."
fi
report="$report Do not claim to have loaded any skill named here. Say it is unavailable and why, then continue without it or ask."

jq -n --arg r "$report" '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:$r}}' 2>/dev/null || cat <<JSON
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "SKILLS DECLARED BUT MISSING (details unavailable: jq not installed). Compare the CLAUDE.md skills table against .claude/skills/ before claiming any skill loaded."
  }
}
JSON
