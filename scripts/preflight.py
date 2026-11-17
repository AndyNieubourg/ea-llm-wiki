#!/usr/bin/env python3
"""Pre-flight checks for wiki changes. Run before committing; call from `lint`.

Catches the mechanical defect classes a reviewer would otherwise catch by hand,
each of which a script finds faster and more reliably:

  frontmatter  a real YAML parse, not a regex over field names. An unquoted colon
               in a title passes every regex check and fails every parser. Then a
               presence check for the four keys every entity page carries, because
               a block missing half its keys parses cleanly.
  links        wikilinks that resolve to nothing. Fenced blocks are stripped first,
               because Mermaid's [[node]] shape is not a wikilink.
  embeds       ![[attachments/...]] pointing at a file that is not there.
  updated      a changed entity page whose `updated:` is older than its last edit
               (the newest commit touching it, or today if it is uncommitted).
  inbound      links into a page this change set deletes or renames away from, and
               embeds of a non-page file it removes. The per-file check only opens
               changed files, so a reference *into* a removed thing sits in a file it
               never reads: the one way link rot passes clean.

On a branch, a finding fails the run only if the branch introduced it. The same
checks run on the merge-base version of every changed file, and a finding that was
already there is printed as inherited and not counted. Without this, a dead link
already sitting in a much-edited file such as wiki/log.md or wiki/glossary.md fails
every branch that touches it, on a defect the branch never made.
`updated` and `inbound` are never baselined: both are claims about this change set
by construction. `--strict` restores the old rule, and `--all` is always strict,
because a whole-vault audit has no branch to compare against.

And the one that is not per-file:

  --claim      find every restatement of a phrase across the whole vault, including
               index.md, log.md and glossary.md. Run it after retracting anything.
               A claim corrected in one place and left standing in others is the
               commonest way a wiki contradicts itself.

Usage:
  scripts/preflight.py                      # files changed against origin/main;
                                            # fails only on findings the branch introduced
  scripts/preflight.py --strict             # same files, every finding counts
  scripts/preflight.py --all                # the whole vault, every finding counts
  scripts/preflight.py --claim "some text"  # restatement sweep

Exit 0 clean, 1 on any finding, 2 when the check cannot run: the change set cannot
be determined, or PyYAML (`pip install pyyaml`) is missing.
The last of those matters: returning an empty change set on a git failure made a
broken repository read as a clean one.
"""

import argparse
import collections
import pathlib
import re
import subprocess
import sys
import tempfile
import datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"

# Top-level infrastructure files carry no frontmatter by design (CLAUDE.md).
NO_FRONTMATTER = {"index.md", "log.md"}


def no_frontmatter(path):
    """index.md, log.md, and the monthly slices `lint` rolls out of log.md into
    wiki/log/: an archive is log.md by another name and carries no frontmatter
    either. Without this every rotation reads as a frontmatter finding the branch
    introduced."""
    return path.name in NO_FRONTMATTER or path.parent == WIKI / "log"

INLINE_CODE = re.compile(r"`[^`\n]+`")
# A fence opener, inside any depth of blockquote or callout: `> ```mermaid` opens a
# fence just as a column-0 ``` does, and Obsidian renders it as one. Tildes count.
FENCE_OPEN = re.compile(r"^((?:[ \t]*>)*)[ \t]*(`{3,}|~{3,})")
QUOTE_PREFIX = re.compile(r"^((?:[ \t]*>)*)")
WIKILINK = re.compile(r"(?<!!)\[\[([^\]|#]+)")
EMBED = re.compile(r"!\[\[([^\]|#]+)")


def strip_fences(text):
    """Blank every fenced block and inline code span, keeping line numbering intact.

    Line by line rather than one regex, for three shapes a column-0 ``` regex
    missed: a fence inside a callout (`> ```mermaid`, where Mermaid's `A[[x]]`
    subroutine shape read as a dead link), a `~~~` fence, and a quoted fence
    that ends because the callout ends. Lines are blanked, never removed, so a
    finding's line number still points at the right line. An unclosed fence runs
    to the end of the file, as CommonMark renders it.
    """
    out, fence = [], None
    for line in text.split("\n"):
        depth = QUOTE_PREFIX.match(line).group(1).count(">")
        if fence is not None and fence[0] and depth < fence[0]:
            fence = None  # the blockquote ended, so the fence inside it did too
        m = FENCE_OPEN.match(line)
        if fence is None:
            if m:
                fence = (m.group(1).count(">"), m.group(2)[0], len(m.group(2)))
                out.append("")
            else:
                # `[[page-slug]]` in backticks is a documented example of the
                # syntax, and Obsidian does not render it as a link either.
                out.append(INLINE_CODE.sub("", line))
            continue
        q, ch, n = fence
        if (m and m.group(1).count(">") == q and m.group(2)[0] == ch
                and len(m.group(2)) >= n and not line[m.end():].strip()):
            fence = None
        out.append("")
    return "\n".join(out)


def changed_files():
    try:
        base = subprocess.run(
            ["git", "merge-base", "HEAD", "origin/main"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        # NUL-separated throughout. Line or whitespace splitting dropped every path
        # with a space, and git quotes a non-ASCII path ("caf\303\251.md") unless
        # -z is set, so both kinds of page were silently left unchecked.
        out = subprocess.run(
            ["git", "diff", "--name-only", "-z", f"{base}..HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
        staged = subprocess.run(
            ["git", "diff", "--name-only", "-z", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
        untracked = subprocess.run(
            ["git", "ls-files", "-o", "--exclude-standard", "-z"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, OSError) as e:
        # Returning [] here made a broken repository indistinguishable from a clean
        # one: no `origin/main`, and preflight printed "no changed wiki pages" and
        # exited 0 having checked nothing. A gate that cannot determine its own
        # population has not passed, it has not run.
        # `OSError` is in the tuple because `git` missing from `PATH` raises
        # `FileNotFoundError`, not `CalledProcessError`. That is the same "cannot
        # determine the population" condition, and catching only the latter left it
        # exiting 1 through a traceback: the code this file reserves for findings.
        print(f"cannot determine the change set: {e}", file=sys.stderr)
        print("run with --all to audit the whole vault instead", file=sys.stderr)
        sys.exit(2)
    names = {n for chunk in (out, staged, untracked) for n in chunk.split("\0") if n}
    return [ROOT / n for n in sorted(names)
            if n.startswith("wiki/") and n.endswith(".md")]


def _merge_base():
    try:
        return subprocess.run(
            ["git", "merge-base", "HEAD", "origin/main"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        # `OSError` for the same reason `changed_files` catches it: git absent from
        # `PATH` raises `FileNotFoundError`, not `CalledProcessError`. Without it,
        # `--all` skipped `changed_files` entirely and this became the first git
        # call in the run, so a missing git left the traceback here instead: exit 1,
        # the code this file reserves for findings.
        return None


def removed_wiki_paths(findings):
    """Vault-relative paths this change set deletes or renames away from.

    One walk, read by both `gone_pages` and `gone_attachments`, so the two cannot
    drift apart in which git failures they tolerate or which paths they drop.

    A change set that cannot be read is a finding, not an empty set. Returning
    `set()` when every git call failed would tell both sweeps that nothing was
    removed, which is the fail-open shape `changed_files` exits 2 over.
    """
    base = _merge_base()
    diff = ["git", "diff", "--name-status", "-z", "--diff-filter=DR"]
    ranges = [diff + [f"{base}..HEAD"]] if base else []
    ranges += [diff + ["HEAD"], diff + ["--cached"]]
    gone, ran, err = set(), False, None
    for cmd in ranges:
        try:
            out = subprocess.run(cmd, cwd=ROOT, capture_output=True,
                                 text=True, check=True).stdout
        except (subprocess.CalledProcessError, OSError) as e:
            err = e
            continue
        # One range succeeding is enough: `git diff HEAD` fails in a repository
        # with no commits while `--cached` answers, and that is not a broken repo.
        ran = True
        # -z output is a token stream: status, path for a deletion; status, old,
        # new for a rename. A tab-split line parse lost quoted non-ASCII paths.
        toks, i = out.split("\0"), 0
        while i + 1 < len(toks) and toks[i]:
            old = toks[i + 1]
            i += 3 if toks[i][0] in "RC" else 2
            if old.startswith("wiki/"):
                gone.add(old[len("wiki/"):])
    if not ran:
        findings.append((WIKI, "inbound",
                         f"cannot read what this change set removes: {err}"))
    # A path re-created before the run is not a loss, however it was removed. The
    # page half of this filter was already here; the attachment half was dropped in
    # the copy, so a `git rm --cached` that leaves the file on disk reported a live
    # embed as removed while `check_links` in the same run reported it resolving.
    return {g for g in gone if not (WIKI / g).exists()}


def gone_pages(removed):
    """Wiki page stems this change set deletes or renames away from.

    The per-file link check only reads changed files, so a link *into* a page
    this branch removed lives in a file the check never opens. That is the one
    way link rot can be introduced and pass clean, so it is checked separately.
    """
    # A rename that also re-created the stem elsewhere is not a loss either, and
    # that is a wider test than the path test in `removed_wiki_paths`.
    stems = {link_key(g) for g in removed if g.endswith(".md")}
    return {s for s in stems if s not in page_index()}


def gone_attachments(removed):
    """Wiki files this change set removes that are NOT markdown pages.

    `gone_pages` filters on `.md`, so deleting an image, a `.base` or a PDF
    produced an empty stem set and the inbound sweep never ran on it. The embed
    check only opens changed files, so the page still embedding it is never read:
    the same hole as inbound links, one population across.
    """
    return {g for g in removed if not g.endswith(".md")}


def check_inbound(stems, attachments, findings):
    """Sweep the whole vault for references into anything this change set removed.

    Links and embeds in one pass: two passes would read every page twice to answer
    two questions about the same line.
    """
    if not stems and not attachments:
        return
    for path in all_files():
        if path.parent.name == "log":  # archived months are dated records
            continue
        text = strip_fences(path.read_text(encoding="utf-8", errors="replace"))
        for n, line in enumerate(text.splitlines(), 1):
            for target in WIKILINK.findall(line):
                t = target.strip().rstrip("\\").strip()
                if link_key(t) in stems:
                    findings.append((path, "inbound",
                                     f"line {n} links [[{t}]], which this change removes"))
            for target in EMBED.findall(line):
                t = target.strip().rstrip("\\").strip()
                if t in attachments:
                    findings.append((path, "inbound",
                                     f"line {n} embeds ![[{t}]], which this change removes"))


def all_files(wiki=WIKI):
    return sorted(p for p in wiki.rglob("*.md") if ".obsidian" not in p.parts)


def link_key(target):
    """The page name a wikilink target resolves by, or a page path's own name.

    One normaliser for both sides of every comparison. The link check took the
    last path component and the inbound sweep took the stem, so `[[v1.2-notes]]`
    resolved in one and read as `v1` in the other, and `[[page.md]]` read as dead.
    """
    name = target.strip().rstrip("\\").strip().rsplit("/", 1)[-1]
    return name[:-3] if name.lower().endswith(".md") else name


def page_index(wiki=WIKI):
    """Page names that exist, for wikilink resolution."""
    return {link_key(p.name) for p in wiki.rglob("*.md")}


def check_required_fm(path, findings):
    if no_frontmatter(path):
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    if fm_bounds(text)[0] != "ok":
        return          # no readable block at all is check_frontmatter's finding
    for key in REQUIRED_FM:
        got = fm_field(text, key)
        if got is None:
            findings.append((path, "frontmatter", f"no `{key}:` in the frontmatter block"))
        elif key in FM_DATES and fm_date(text, key) is None:
            findings.append((path, "frontmatter",
                             f"`{key}: {got}` is not a YYYY-MM-DD date"))


def check_frontmatter(path, findings):
    if no_frontmatter(path):
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    state, block = fm_bounds(text)
    if state == "none":
        findings.append((path, "frontmatter", "no YAML frontmatter block"))
        return
    if state == "open":
        findings.append((path, "frontmatter", "frontmatter block is not closed"))
        return
    try:
        import yaml
        yaml.safe_load(block)
    except Exception as exc:  # noqa: BLE001 - we want the parser's own message
        first = str(exc).splitlines()[0]
        findings.append((path, "frontmatter", f"does not parse: {first}"))


def check_links(path, stems, findings, wiki=WIKI):
    # Archived monthly logs are immutable records: they name pages as they stood
    # on the day, so a link broken by a later rename is correct history, not rot.
    if path.parent.name == "log":
        return
    text = strip_fences(path.read_text(encoding="utf-8", errors="replace"))
    # Some pages escape the brackets as \[\[name\]\], so the capture keeps a
    # trailing backslash and every such link reads as broken. Strip it.
    clean = lambda t: t.strip().rstrip("\\").strip()
    for target in {clean(t) for t in WIKILINK.findall(text)}:
        if target.startswith("attachments/"):
            continue
        if link_key(target) not in stems:
            findings.append((path, "link", f"[[{target}]] resolves to nothing"))
    for target in {clean(t) for t in EMBED.findall(text)}:
        if not (wiki / target).exists():
            findings.append((path, "embed", f"![[{target}]] is missing"))


def last_edited(path, base):
    """The date this change set last touched a page: today if it has uncommitted
    changes, else the committer date of the newest commit since `base` touching it.

    Comparing against today flagged every page on a branch older than a day, and
    the baseline cannot waive an `updated` finding. Any git failure answers today,
    which is the stricter reading, never a silent pass.
    """
    today = datetime.date.today().isoformat()
    rel = path.relative_to(ROOT).as_posix()
    try:
        dirty = subprocess.run(["git", "status", "--porcelain", "-z", "--", rel],
                               cwd=ROOT, capture_output=True, text=True, check=True).stdout
        if dirty or not base:
            return today
        when = subprocess.run(["git", "log", "-1", "--format=%cs", f"{base}..HEAD", "--", rel],
                              cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return today
    return when or today


def check_updated(path, findings, edited=None):
    if no_frontmatter(path):
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    got = fm_date(text, "updated")
    edited = edited or datetime.date.today().isoformat()
    if got and got < edited:
        findings.append((path, "updated", f"`updated: {got}` but last edited {edited}"))


def claim_sweep(phrase):
    # Pure Python on purpose: no dependency on rg resolving from a subprocess,
    # and no risk of a shadowed shell tool quietly returning fewer hits.
    needle = phrase.lower()
    hits = []
    for path in all_files():
        for n, line in enumerate(
                path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if needle in line.lower():
                hits.append(f"{path.relative_to(WIKI)}:{n}: {line.strip()[:160]}")
    print(f"restatements of {phrase!r}: {len(hits)}")
    for h in hits:
        print("  " + h)
    print("\nEvery hit must agree with what the wiki now says. A correction is an "
          "aggregation surface too.")
    return 1 if hits else 0


# Frontmatter reads are bounded to the frontmatter block. `re.search` over the whole
# file returns the first match, which is the right one only while the key is present
# above the body. A page that shows `created:` or `type:` inside a fenced example would
# otherwise have the example value swapped into a check the moment its real key goes.
def fm_bounds(text):
    """("ok", block) | ("none", "") | ("open", "") for the frontmatter at the top.

    The block opens on a first line that is exactly `---` and closes on the next
    line that is exactly `---` (or YAML's `...`). Searching for the substring
    `\n---` closed it on `----`, on `---x`, or on anything else that merely
    starts with three dashes.
    """
    lines = text.split("\n")
    if not lines or lines[0].rstrip() != "---":
        return "none", ""
    for i in range(1, len(lines)):
        if lines[i].rstrip() in ("---", "..."):
            return "ok", "\n".join(lines[1:i])
    return "open", ""


def frontmatter(text):
    # An unclosed block returns nothing, not the whole document. Returning the
    # document would reinstate the unbounded read this function exists to prevent.
    # A page whose frontmatter never closes has no readable frontmatter, and
    # `check_frontmatter` reports it.
    state, block = fm_bounds(text)
    return block if state == "ok" else ""


def fm_field(text, key):
    # `\s*` crossed the newline, so `type:` with an empty value returned the string
    # "created:" from the line below it. Horizontal whitespace only.
    m = re.search(rf"^{key}:[ \t]*['\"]?([^\s'\"]+)", frontmatter(text), re.M)
    return m.group(1) if m else None


def fm_date(text, key):
    r"""A frontmatter date, or None. Shape-checked: the previous readers anchored
    \d{4}-\d{2}-\d{2} and folding them into fm_field silently dropped that.

    The docstring is a raw string because `\d` in a plain one is an invalid escape
    sequence: a DeprecationWarning on 3.9 and a SyntaxWarning printed to stderr on
    3.12 and up, on a gate whose stderr is read to decide whether it ran clean.

    This returns None for a value that is present but not a date, so it is stricter
    than the anchor it restores, which prefix-matched. That silences the caller, so
    `check_required_fm` reports the malformed value: otherwise `updated: 2026-09-08T10:00`
    on a page edited today would otherwise pass clean.
    """
    got = fm_field(text, key)
    return got if got and re.fullmatch(r"\d{4}-\d{2}-\d{2}", got) else None


# Every entity page carries these. A YAML parse succeeds on a block missing half its
# keys, so presence is checked separately.
REQUIRED_FM = ("title", "type", "created", "updated")
# The two that `fm_date` reads, so a present-but-unparseable value is reported here
# rather than turning `check_updated` quiet on that page.
FM_DATES = ("created", "updated")


# ------------------------------------------------------------------ the baseline
# The kinds a merge-base copy can already carry. `updated` is missing on purpose: it
# fires because the file is in the change set, so its merge-base twin fires the same
# way and would cancel a true finding. `inbound` and the two "cannot run" findings
# describe this change set or this checkout, not a file's content.
BASELINED = {"frontmatter", "link", "embed"}
LINE_NO = re.compile(r"\bline \d+: ")


def materialise(base, dest):
    """Write the wiki as it stood at `base` under `dest/wiki`.

    Every `.md` blob is written; every other path becomes an empty placeholder, so
    the embed check's exists-test answers as it would at `base` without extracting
    the attachments for a check that never reads one.
    """
    listing = subprocess.run(
        ["git", "ls-tree", "-r", "-z", "--full-tree", base, "--", "wiki"],
        cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8", "surrogateescape")
    blobs = []
    for entry in filter(None, listing.split("\0")):
        meta, path = entry.split("\t", 1)
        mode, kind, sha = meta.split()
        if kind != "blob":
            continue
        target = dest / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.endswith(".md") and mode != "120000":
            blobs.append((sha, target))
        else:
            target.touch()
    out = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT, capture_output=True,
                         check=True, input="".join(f"{sha}\n" for sha, _ in blobs).encode()).stdout
    pos = 0
    for sha, target in blobs:
        header_end = out.index(b"\n", pos)
        name, kind, size = out[pos:header_end].split()
        if name.decode() != sha or kind != b"blob":
            raise OSError(f"git cat-file answered {name.decode()} {kind.decode()} for {sha}")
        start = header_end + 1
        target.write_bytes(out[start:start + int(size)])
        pos = start + int(size) + 1
    return dest / "wiki"


def renamed_from(base):
    """Head vault path -> merge-base vault path, for files this change set renamed."""
    out = subprocess.run(
        ["git", "diff", "-M", "--name-status", "-z", "--diff-filter=R", base],
        cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8", "surrogateescape")
    parts = out.split("\0")
    pairs = {}
    for i in range(0, len(parts) - 2, 3):
        old, new = parts[i + 1], parts[i + 2]
        if old.startswith("wiki/") and new.startswith("wiki/"):
            pairs[new[len("wiki/"):]] = old[len("wiki/"):]
    return pairs


def finding_key(path, kind, msg, wiki):
    # The line number goes: a branch that adds a line above an inherited finding
    # moves it, and a moved finding is the same finding.
    return (path.relative_to(wiki).as_posix(), kind, LINE_NO.sub("", msg))


def split_inherited(findings, base_findings, base_wiki, back):
    """Head findings the merge-base already had, and the ones this branch introduced.

    A multiset, not a set: two lines can carry the same message, and one more of
    them on the branch is a finding even though the text is not new.
    """
    before = collections.Counter(
        (back.get(k[0], k[0]),) + k[1:]
        for k in (finding_key(p, kind, m, base_wiki) for p, kind, m in base_findings))
    introduced, inherited = [], []
    for f in findings:
        if f[1] not in BASELINED:
            introduced.append(f)
            continue
        key = finding_key(f[0], f[1], f[2], WIKI)
        if before[key] > 0:
            before[key] -= 1
            inherited.append(f)
        else:
            introduced.append(f)
    return introduced, inherited


def content_checks(paths, wiki, findings):
    """The per-file checks a merge-base copy can carry too."""
    stems = page_index(wiki)
    for p in paths:
        check_frontmatter(p, findings)
        check_required_fm(p, findings)
        check_links(p, stems, findings, wiki)


def baseline(paths, scratch):
    """Materialise the merge base and map each changed page to its copy there.

    Returns (base sha, base wiki, head path -> base path or None, head-rel ->
    base-rel renames), or a reason string when no baseline can be built. The caller
    then counts every finding: a baseline that cannot be read inherits nothing.
    """
    base = _merge_base()
    if not base:
        return "no merge base with origin/main"
    try:
        base_wiki = materialise(base, scratch)
        back = renamed_from(base)
    except (subprocess.CalledProcessError, OSError, ValueError) as e:
        return f"cannot read the merge base {base[:8]}: {e}"
    copies = {}
    for p in paths:
        rel = p.relative_to(WIKI).as_posix()
        twin = base_wiki / back.get(rel, rel)
        copies[p] = twin if twin.exists() else None
    return base, base_wiki, copies, back


def report(findings, inherited, base_note):
    # One report block, so every exit path prints the same verdict shape.
    #
    # The verdict line leads with what counts. A reviewer (human or agent) reading
    # this output reads a list of inherited findings printed as findings as a
    # failure, whatever the exit code says.
    if inherited:
        print(f"\ninherited from {base_note}, NOT counted ({len(inherited)}):")
        for path, kind, msg in inherited:
            print(f"  {kind:<12} {path.relative_to(ROOT)}: {msg}")
    if findings:
        print(f"\n{'introduced by this branch' if base_note else 'findings'} ({len(findings)}):")
        for path, kind, msg in findings:
            print(f"  {kind:<12} {path.relative_to(ROOT)}: {msg}")
    tail = f"; {len(inherited)} inherited from {base_note}, not counted" if base_note else ""
    print(f"\n{len(findings)} {'introduced ' if base_note else ''}finding(s){tail}")
    if findings:
        sys.exit(1)
    print("clean")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="count findings the merge base already had (default: inherited "
                         "findings are printed and not counted; --all is always strict)")
    ap.add_argument("--claim")
    args = ap.parse_args()

    if args.claim:
        sys.exit(claim_sweep(args.claim))

    try:
        import yaml  # noqa: F401  (check_frontmatter needs it)
    except ImportError:
        # Without the parser every page would read as "does not parse", or worse, a
        # caller that skipped the parse would call the vault clean. Neither is a result.
        print("PyYAML is not installed (pip install pyyaml); frontmatter cannot be "
              "parsed, so preflight did not run", file=sys.stderr)
        sys.exit(2)

    paths = all_files() if args.all else changed_files()
    paths = [p for p in paths if p.exists()]
    findings = []
    # The inbound sweep does not read the changed set and must not be gated on it.
    # Its population is the pages this change set REMOVED, and a commit that deletes
    # a page or touches only `scripts/` has an empty changed set while having plenty
    # for it to find. `check_inbound`'s own docstring calls that the one way link rot
    # passes clean.
    content_checks(paths, WIKI, findings)
    removed = removed_wiki_paths(findings)
    check_inbound(gone_pages(removed), gone_attachments(removed), findings)
    if not args.all:
        base_sha = _merge_base()
        for p in paths:
            check_updated(p, findings, last_edited(p, base_sha))

    with tempfile.TemporaryDirectory(prefix="preflight-base-") as scratch:
        base, inherited, base_note = None, [], None
        if not (args.all or args.strict):
            base = baseline(paths, pathlib.Path(scratch))
            if isinstance(base, str):
                # Fail closed, and say so: a strict result is still a real result, so
                # this is not exit 2, but nothing may be waved through as inherited.
                print(f"baseline unavailable ({base}): every finding counts")
                base = None
            else:
                sha, base_wiki, copies, back = base
                base_findings = []
                content_checks([c for c in copies.values() if c], base_wiki, base_findings)
                findings, inherited = split_inherited(
                    findings, base_findings, base_wiki, {v: k for k, v in back.items()})
                base_note = f"merge base {sha[:8]}"

    print(f"checked {len(paths)} page(s)" if paths
          else "no changed wiki pages; vault-wide checks still ran")
    report(findings, inherited, base_note)


if __name__ == "__main__":
    main()
