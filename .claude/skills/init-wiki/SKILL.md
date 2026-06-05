---
name: init-wiki
description: One-time setup of the EA LLM-wiki foundation. Interviews the wiki owner and tailors CLAUDE.md, README.md, wiki/domains.md, and the voice guide in place, replacing the foundation placeholders. Use on a fresh clone of the foundation, or when asked to "initialise/set up this wiki", "personalise the foundation", or "run init".
allowed-tools: Read, Grep, Glob, Write, Edit, AskUserQuestion, Bash, Skill
user-invocable: true
---

# Initialise the EA LLM-wiki foundation

This skill turns the generic foundation scaffold into a personalised wiki for its owner. It is a thin wrapper around the canonical protocol in [`INIT.md`](../../../INIT.md) at the repo root.

## What to do

1. **Read `INIT.md` at the repo root in full.** It is the authoritative, step-by-step protocol — orient, interview (identity, purpose/jobs, domain taxonomy, locale, raw path, confidentiality, shipping autonomy), apply the edits, hand off to `voice-interview`, then verify and commit. Follow it exactly.
2. **Run it once, at the repo root** on the main/default branch (not a `claude/*` worktree) so the personalisation lands as the wiki's first real commit.
3. **Hand off the voice work** to the `voice-interview` skill (full pass) as INIT.md's Step 3 instructs, unless the owner defers it.
4. **Run the self-check** at the end of INIT.md before declaring done: no `{{placeholders}}` left, banner removed, domain set consistent across the four files, README personalised, log updated.

## Notes

- If `INIT.md` is missing (already deleted after a prior run), this wiki has likely been initialised already — confirm with the owner before re-running, since re-init would overwrite their personalised `CLAUDE.md`.
- This skill and `INIT.md` are setup-only. Once the wiki is initialised, both can be deleted; everyday work uses the four wiki workflows in `CLAUDE.md`.
