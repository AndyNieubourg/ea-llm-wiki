#!/usr/bin/env python3
"""Derive the numbers a lint log entry restates, from the tree and the diff.

Hand-written lint aggregates drift: an inbox delta off by one, a ruminated count
that includes pages nobody re-asked, a status move forgotten. The fix is to derive
the number where it is read. Run this before writing the log entry and paste from
its output.

  inbox        note count at base and at head, with the delta
  entities     page count per entity directory at head, with the delta
  ruminated    existing question pages whose `last-ruminated` changed in the
               diff, as N of total — the tree count alone overstates it,
               because pages ruminated before the pass already carry a recent
               date. Pages new in the diff are listed apart, not counted:
               creating a question is not re-asking one
  status       question `status:` transitions in the diff, one line each, so
               the entry counts pages instead of remembering them (`status:`
               is question-page frontmatter in this wiki's schema)
  files        wiki pages added / modified / deleted / renamed in the diff

Read-only and dependency-free: git plumbing reads plus the filesystem, no
writes, no yaml. Head is the working tree by default, because the log entry
is written before the lint commits.

Usage:
  scripts/lint-aggregates.py                      # working tree vs merge-base(origin/main)
  scripts/lint-aggregates.py --base R1 --head R2  # a historical state, e.g. a merged PR

Exit 0 whenever it prints: the numbers gate nothing. The one non-zero exit is
an unresolvable base or head rev, which fails loudly rather than print drift
(a script born from drifted numbers must never produce them silently).
"""

import argparse
import functools
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"

ENTITY_DIRS = ["sources", "concepts", "frameworks", "questions", "cases",
               "analyses", "artifacts", "inbox"]


def git(*args):
    res = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return res.stdout if res.returncode == 0 else None


def wiki_pages(rev):
    """Repo-relative wiki/*.md paths at a rev, or on disk when rev is None.

    Hidden directories (.obsidian, .smart-env, .trash) are excluded on both
    sides, or the disk side would count gitignored files ls-tree never sees.
    `*.pyramid.md` sidecars (pyramid-structure outlines beside a page) are not
    pages and are excluded on both sides.
    """
    if rev:
        out = git("ls-tree", "-r", "-z", "--name-only", rev, "wiki/") or ""
        return [p for p in out.split("\0")
                if p.endswith(".md") and not p.endswith(".pyramid.md")
                and not any(s.startswith(".") for s in p.split("/"))]
    return [str(p.relative_to(ROOT)) for p in sorted(WIKI.rglob("*.md"))
            if not p.name.endswith(".pyramid.md")
            and not any(s.startswith(".") for s in p.relative_to(WIKI).parts)]


@functools.lru_cache(maxsize=None)
def read_page(path, rev):
    """Page text at a rev, or from disk when rev is None. None if absent."""
    if rev:
        return git("show", f"{rev}:{path}")
    p = ROOT / path
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else None


def fm_field(text, name):
    """A scalar frontmatter field, by regex on the block — no yaml dependency."""
    if text is None or not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    m = re.search(rf"^{name}:[ \t]*['\"]?([^'\"\n]+)", text[3:end], re.M)
    return m.group(1).strip() if m else None


def changed(base, head):
    """(status, old_path, path) per changed file; untracked count as added.

    NUL-separated output throughout: line- or space-split parsing shreds a
    path with a space and drops core.quotePath-escaped non-ASCII paths.
    """
    args = ["diff", "--name-status", "-z", "-M", base] + ([head] if head else [])
    toks = (git(*args) or "").split("\0")
    rows, i = [], 0
    while i < len(toks) and toks[i]:
        if toks[i][0] in "RC":          # two-path statuses carry old then new
            rows.append(("R", toks[i + 1], toks[i + 2]))
            i += 3
        else:
            rows.append((toks[i][0], toks[i + 1], toks[i + 1]))
            i += 2
    if not head:
        for p in (git("ls-files", "-o", "--exclude-standard", "-z") or "").split("\0"):
            if p:
                rows.append(("A", p, p))
    return rows


def resolve(rev, what):
    """A rev resolved to its commit hash, or a loud exit — never a silent
    empty base that prints maximally drifted numbers with exit 0."""
    full = (git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}") or "").strip()
    if not full:
        sys.exit(f"cannot resolve {what} rev {rev!r} — refusing to print numbers from it")
    return full


def dir_of(path):
    parts = pathlib.PurePath(path).parts
    return parts[1] if len(parts) > 2 else "(top-level)"


def print_counts(head_pages, base_pages):
    base_by_dir = {}
    for p in base_pages:
        base_by_dir[dir_of(p)] = base_by_dir.get(dir_of(p), 0) + 1
    head_by_dir = {}
    for p in head_pages:
        head_by_dir[dir_of(p)] = head_by_dir.get(dir_of(p), 0) + 1
    print("entity pages at head (Δ vs base):")
    total = dtotal = 0
    for d in sorted(set(head_by_dir) | set(base_by_dir)):
        n, delta = head_by_dir.get(d, 0), head_by_dir.get(d, 0) - base_by_dir.get(d, 0)
        print(f"  {d:<14} {n:>5}  ({delta:+d})")
        if d in ENTITY_DIRS:
            total, dtotal = total + n, dtotal + delta
    print(f"  {'entity total':<14} {total:>5}  ({dtotal:+d})   "
          f"(sum over {', '.join(ENTITY_DIRS)})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", help="base rev (default: merge-base of HEAD and origin/main)")
    ap.add_argument("--head", help="head rev (default: the working tree)")
    args = ap.parse_args()

    base = args.base or (git("merge-base", "HEAD", "origin/main") or "").strip()
    if not base:
        sys.exit("no base: not a git repo, or origin/main unavailable")
    base = resolve(base, "base")
    head = resolve(args.head, "head") if args.head else None

    head_pages = wiki_pages(head)
    base_pages = wiki_pages(base)
    rows = changed(base, head)
    renames = {new: old for st, old, new in rows if st == "R"}

    print(f"lint aggregates — base {base[:8]}, head {head[:8] if head else 'working tree'}")
    print("(derived at write time; paste from here, never restate from memory)\n")

    n_base = sum(1 for p in base_pages if dir_of(p) == "inbox")
    n_head = sum(1 for p in head_pages if dir_of(p) == "inbox")
    print(f"inbox: {n_base} → {n_head} ({n_head - n_base:+d})\n")

    print_counts(head_pages, base_pages)

    questions = [p for p in head_pages if dir_of(p) == "questions"]
    ruminated, fresh, new = [], [], []
    for p in sorted(questions):
        before_text = read_page(renames.get(p, p), base)
        if before_text is None:            # created this pass — not re-asked
            new.append(p)
            continue
        now = fm_field(read_page(p, head), "last-ruminated")
        before = fm_field(before_text, "last-ruminated")
        (ruminated if now != before else fresh).append((p, now))
    print(f"\nruminated this pass (last-ruminated changed in the diff): "
          f"{len(ruminated)} of {len(questions) - len(new)}"
          + (f", plus {len(new)} new (not counted as ruminated)" if new else ""))
    for p in new:
        print(f"  new        {p}")
    for p, d in fresh:
        print(f"  unchanged  {d or '(no last-ruminated)'}  {p}")

    moves = []
    for st, old, p in rows:
        if dir_of(p) != "questions" and dir_of(old) != "questions":
            continue
        if st not in ("M", "R") or not p.endswith(".md"):
            continue
        was = fm_field(read_page(old, base), "status")
        now = fm_field(read_page(p, head), "status")
        if was != now:
            moves.append(f"  {p}: {was} → {now}")
    print(f"\nquestion status transitions (frontmatter `status:` changed): {len(moves)}")
    print("\n".join(moves))

    wiki_md = []
    for st, old, p in rows:
        new_in = p.startswith("wiki/") and p.endswith(".md")
        old_in = old.startswith("wiki/") and old.endswith(".md")
        if st == "R" and old_in and not new_in:
            wiki_md.append(("D", old, old))   # renamed out of wiki/ = a wiki deletion
        elif new_in:
            wiki_md.append((st, old, p))
    by = {st: [p for s, _, p in wiki_md if s == st] for st in "AMDR"}
    print(f"\nwiki pages: {len(by['A'])} added, {len(by['M'])} modified, "
          f"{len(by['D'])} deleted, {len(by['R'])} renamed")
    for st, label in (("A", "added"), ("D", "deleted"), ("R", "renamed")):
        for p in sorted(by[st]):
            print(f"  {label:<8} {p}")
    outside = [p for st, _, p in rows if not p.startswith("wiki/")]
    print(f"outside wiki/: {len(outside)} file(s) changed")


if __name__ == "__main__":
    main()
