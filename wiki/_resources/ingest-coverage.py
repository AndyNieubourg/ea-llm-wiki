#!/usr/bin/env python3
"""ingest-coverage.py — generate a raw/ → wiki ingest-coverage manifest.

Purpose
-------
Answers "which raw/ files are already ingested, and which changed since they
were?" without re-running a fragile full-corpus search every time. Cross-
references every raw/ source file against the `sources:` frontmatter of every
wiki page (the source-first record of truth), and records a content hash so a
later run can flag sources that were re-exported / updated.

Why a generated manifest (not a hand-maintained list)
-----------------------------------------------------
A hand-curated inventory is a second source of truth that drifts. This is
*derived* — rebuilt from raw/ + the `sources:` fields — so it can't silently
go stale. It is the materialised-view sibling of coverage.md.

Why it lives in wiki/_resources/ (not raw/)
-------------------------------------------
`.gitignore` excludes `raw/*`, so a manifest inside raw/ would be uncommitted
AND invisible inside `claude/*` worktrees (where raw/ is empty). Committing it
under _resources/ is the only way a worktree session can see raw/ coverage
without reaching the absolute main-checkout path.

Status semantics (honest, per "absence is a claim")
---------------------------------------------------
  ingested      basename appears in some page's `sources:` array  → trustworthy
  mentioned     basename appears in wiki text but NOT a `sources:` array
                → convention gap (fix the page's sources:) OR an index-only page
                  that deliberately lists titles in the body — check before
                  re-ingesting
  unreferenced  basename appears nowhere in wiki  → candidate to ingest (verify:
                may be a reworded title or a file bundled into a parent page)
  asset         non-source type (image/url/css/zip/…) — not assessed, size only

`unreferenced` is a CANDIDATE, never a verdict — reworded titles and multi-file
parent pages produce false positives. Always confirm before claiming a file is
un-ingested ("absence is a claim").

Change detection (the hash payoff)
----------------------------------
On re-run, if a prior manifest exists, files whose sha256 differs are flagged
`changed=yes` → the source was updated; consider re-ingesting and recording a
`supersedes` / `superseded-by` relationship.

Usage
-----
  # from the MAIN checkout (raw/ populated):
  python3 wiki/_resources/ingest-coverage.py

  # from a worktree (raw/ is empty here) — point --raw at the main checkout:
  python3 wiki/_resources/ingest-coverage.py \
      --raw "/abs/path/to/main-checkout/raw" --wiki wiki

  --no-hash   presence-only, fast (skips reading file bodies)
  --out PATH  manifest path (default wiki/_resources/ingest-coverage.tsv)
"""
from __future__ import annotations
import argparse, hashlib, os, re, sys
from pathlib import Path

SOURCE_EXTS = {".pdf", ".docx", ".pptx", ".epub", ".doc", ".txt", ".md", ".csv", ".xlsx", ".xlsm", ".xls"}
# extensions we treat as ingestable sources; everything else is an "asset"
EXT_RE = re.compile(r"[^,\[\]\"'\n]+?\.(?:pdf|docx|pptx|epub|doc|txt|md|csv|xlsx|xlsm|xls)", re.IGNORECASE)
ARXIV_RE = re.compile(r"\b\d{4}\.\d{4,5}\b")   # bare arXiv ids (extensionless source files)
SKIP_DIR_PARTS = ("_files",)            # web-scrape asset folders
SKIP_NAMES = {".DS_Store", ".gitkeep"}


def sources_basenames(wiki_dir: Path) -> dict[str, list[str]]:
    """Map raw basename -> [wiki pages listing it in `sources:`]."""
    out: dict[str, list[str]] = {}
    for md in wiki_dir.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        fm = text[: end if end != -1 else len(text)]
        m = re.search(r"^sources:(.*?)(?=^\w[\w-]*:|\Z)", fm, re.MULTILINE | re.DOTALL)
        if not m:
            continue
        for tok in EXT_RE.findall(m.group(1)) + ARXIV_RE.findall(m.group(1)):
            base = os.path.basename(tok.strip().strip("\"'").strip())
            out.setdefault(base, []).append(md.name)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    here = Path(__file__).resolve()
    repo = here.parents[2]                       # wiki/_resources/ -> repo root
    ap.add_argument("--raw", default=str(repo / "raw"))
    ap.add_argument("--wiki", default=str(repo / "wiki"))
    ap.add_argument("--out", default=str(here.parent / "ingest-coverage.tsv"))
    ap.add_argument("--no-hash", action="store_true")
    args = ap.parse_args()

    raw_dir, wiki_dir, out_path = Path(args.raw), Path(args.wiki), Path(args.out)
    if not any(raw_dir.iterdir()) if raw_dir.is_dir() else True:
        print(f"raw/ at {raw_dir} is empty or missing — pass --raw pointing at the "
              f"main checkout's populated raw/.", file=sys.stderr)
        return 2

    smap = sources_basenames(wiki_dir)
    wiki_blob = "\n".join(
        p.read_text(encoding="utf-8", errors="replace") for p in wiki_dir.rglob("*.md")
    )

    prior: dict[str, str] = {}
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines()[1:]:
            c = line.split("\t")
            if len(c) >= 6 and c[1]:
                prior[c[5]] = c[1]               # relpath -> sha

    rows = []
    for f in sorted(raw_dir.rglob("*")):
        if not f.is_file() or f.name in SKIP_NAMES or f.name.startswith("._"):
            continue
        if any(part for part in f.parts if part.endswith(SKIP_DIR_PARTS)):
            continue
        rel = f.relative_to(raw_dir).as_posix()
        is_arxiv = bool(ARXIV_RE.fullmatch(f.name))
        ext = "arxiv" if is_arxiv else f.suffix.lower()
        top = rel.split("/", 1)[0]
        try:
            size = f.stat().st_size
        except OSError:
            size = -1
        is_source = is_arxiv or ext in SOURCE_EXTS
        sha = ""
        if is_source and not args.no_hash:
            try:
                h = hashlib.sha256()
                with f.open("rb") as fh:
                    for chunk in iter(lambda: fh.read(1 << 20), b""):
                        h.update(chunk)
                sha = h.hexdigest()[:16]
            except OSError:
                sha = "READERR"
        if not is_source:
            status = "asset"
        else:
            base = f.name
            if base in smap:
                status = "ingested"
            elif base in wiki_blob:
                status = "mentioned"
            else:
                status = "unreferenced"
        changed = "new" if is_source else "-"
        if sha and rel in prior:
            changed = "yes" if prior[rel] != sha else "no"
        ref = ";".join(sorted(set(smap.get(f.name, []))))
        rows.append((status, sha, str(size), ext.lstrip("."), top, rel, changed, ref))

    order = {"unreferenced": 0, "mentioned": 1, "ingested": 2, "asset": 3}
    rows.sort(key=lambda r: (order.get(r[0], 9), r[4], r[5]))

    header = "status\tsha256_16\tbytes\text\ttop_folder\trelpath\tchanged\treferenced_in"
    out_path.write_text(header + "\n" + "\n".join("\t".join(r) for r in rows) + "\n", encoding="utf-8")

    from collections import Counter
    counts = Counter(r[0] for r in rows)
    chg = sum(1 for r in rows if r[6] == "yes")
    print(f"wrote {out_path} — {len(rows)} files")
    for k in ("ingested", "mentioned", "unreferenced", "asset"):
        print(f"  {k:<13} {counts.get(k, 0)}")
    if chg:
        print(f"  changed-since-last: {chg}  (candidate re-ingest)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
