#!/usr/bin/env python3
"""preflight.py fails a branch only on findings the branch introduced.

Each case builds a throwaway repository: a copy of preflight.py, a small vault
committed on `main`, `origin/main` pointed at it, and a branch that changes
something. The first case is the one the baseline exists for: a file that already
carries a dead link is touched, and the run must pass while still printing the
inherited finding.

Run: python3 scripts/tests/test_preflight_baseline.py
"""

import datetime
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
PREFLIGHT = REPO / "scripts" / "preflight.py"
TODAY = datetime.date.today().isoformat()


def page(title, body, kind="concept"):
    return (f"---\ntitle: {title}\ntype: {kind}\ncreated: 2026-01-01\n"
            f"updated: {TODAY}\ntags: []\n---\n\n{body}\n")


class Vault:
    def __init__(self):
        self.dir = pathlib.Path(tempfile.mkdtemp(prefix="preflight-test-"))
        (self.dir / "scripts").mkdir()
        shutil.copy(PREFLIGHT, self.dir / "scripts" / "preflight.py")
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "test")

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.dir, check=True, capture_output=True)

    def write(self, rel, text):
        path = self.dir / "wiki" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def append(self, rel, text):
        with open(self.dir / "wiki" / rel, "a", encoding="utf-8") as handle:
            handle.write(text)

    def commit_main(self):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "main")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.git("checkout", "-q", "-b", "claude/test")

    def commit(self, date=None):
        self.git("add", "-A")
        env = None
        if date:
            stamp = f"{date}T12:00:00"
            env = dict(os.environ, GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp)
        subprocess.run(["git", "commit", "-q", "-m", "branch"], cwd=self.dir,
                       check=True, capture_output=True, env=env)

    def remove(self, rel):
        self.git("rm", "-q", f"wiki/{rel}")

    def run(self, *flags):
        res = subprocess.run([sys.executable, "scripts/preflight.py", *flags],
                             cwd=self.dir, capture_output=True, text=True)
        return res.returncode, res.stdout + res.stderr

    def close(self):
        shutil.rmtree(self.dir, ignore_errors=True)


class Baseline(unittest.TestCase):
    def setUp(self):
        self.v = Vault()
        self.v.write("concepts/alpha.md", page("alpha", "See [[ghost]]. And [[beta]]."))
        self.v.write("concepts/beta.md", page("beta", "Back to [[alpha]]."))
        self.v.commit_main()

    def tearDown(self):
        self.v.close()

    def test_touching_a_file_with_an_inherited_finding_passes(self):
        self.v.append("concepts/alpha.md", "\n")
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 0, out)
        self.assertIn("inherited from merge base", out)
        self.assertIn("[[ghost]] resolves to nothing", out)
        self.assertIn("0 introduced finding(s); 1 inherited", out)
        self.assertTrue(out.rstrip().endswith("clean"), out)

    def test_a_line_inserted_above_keeps_the_finding_inherited(self):
        text = (self.v.dir / "wiki/concepts/alpha.md").read_text()
        self.v.write("concepts/alpha.md", text.replace("\n\nSee", "\n\nA new opening line.\n\nSee"))
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 0, out)

    def test_a_new_dead_link_fails_and_only_it_counts(self):
        self.v.append("concepts/alpha.md", "\nAlso [[phantom]].\n")
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 1, out)
        self.assertIn("1 introduced finding(s); 1 inherited", out)
        introduced = out.split("introduced by this branch")[1]
        self.assertIn("[[phantom]]", introduced)
        self.assertNotIn("[[ghost]]", introduced)

    def test_uncommitted_changes_are_compared_too(self):
        self.v.append("concepts/alpha.md", "\nAlso [[phantom]].\n")
        code, out = self.v.run()
        self.assertEqual(code, 1, out)
        self.assertIn("1 introduced finding(s)", out)

    def test_strict_counts_the_inherited_finding(self):
        self.v.append("concepts/alpha.md", "\n")
        self.v.commit()
        code, out = self.v.run("--strict")
        self.assertEqual(code, 1, out)
        self.assertIn("[[ghost]] resolves to nothing", out)
        self.assertNotIn("inherited", out)

    def test_all_is_strict(self):
        code, out = self.v.run("--all")
        self.assertEqual(code, 1, out)
        self.assertNotIn("inherited", out)

    def test_a_rename_keeps_the_finding_inherited(self):
        self.v.git("mv", "wiki/concepts/alpha.md", "wiki/concepts/alpha-renamed.md")
        self.v.write("concepts/beta.md", page("beta", "Back to [[alpha-renamed]]."))
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 0, out)
        self.assertIn("1 inherited", out)

    def test_a_new_page_counts_everything(self):
        self.v.write("concepts/gamma.md", page("gamma", "See [[ghost]]."))
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 1, out)
        self.assertIn("gamma.md: [[ghost]]", out.split("introduced by this branch")[1])

    def test_a_stale_updated_field_is_never_inherited(self):
        text = (self.v.dir / "wiki/concepts/alpha.md").read_text()
        self.v.write("concepts/alpha.md", text.replace(f"updated: {TODAY}", "updated: 2026-01-02")
                     + "\nMore.\n")
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 1, out)
        self.assertIn(f"`updated: 2026-01-02` but last edited {TODAY}", out)

    def test_an_unreadable_baseline_fails_closed(self):
        # The merge base resolves but its tree cannot be read. A shim that fails
        # `git ls-tree` and passes everything else through stands in for that.
        fake = self.v.dir / "bin"
        fake.mkdir()
        real = shutil.which("git")
        (fake / "git").write_text(
            "#!/bin/sh\n"
            f'if [ "$1" = "ls-tree" ]; then echo "ls-tree broken" >&2; exit 128; fi\n'
            f'exec "{real}" "$@"\n')
        (fake / "git").chmod(0o755)
        self.v.append("concepts/alpha.md", "\n")
        self.v.commit()
        res = subprocess.run([sys.executable, "scripts/preflight.py"],
                             cwd=self.v.dir, capture_output=True, text=True,
                             env=dict(os.environ, PATH=f"{fake}:{os.environ['PATH']}"))
        out = res.stdout + res.stderr
        self.assertEqual(res.returncode, 1, out)
        self.assertIn("baseline unavailable", out)
        self.assertIn("[[ghost]] resolves to nothing", out)


DAYS_AGO = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()


def dated_page(title, body, updated):
    return (f"---\ntitle: {title}\ntype: concept\ncreated: 2026-01-01\n"
            f"updated: {updated}\ntags: []\n---\n\n{body}\n")


class Hardening(unittest.TestCase):
    """Paths git would quote, fences inside callouts, bounded frontmatter, dotted
    page names, and an `updated:` check that reads the commit date, not today."""

    def setUp(self):
        self.v = Vault()
        self.v.write("concepts/alpha.md", page("alpha", "See [[beta]]."))
        self.v.write("concepts/beta.md", page("beta", "Back to [[alpha]]."))
        self.v.commit_main()

    def tearDown(self):
        self.v.close()

    def test_a_path_with_a_space_is_checked(self):
        self.v.write("concepts/with space.md", page("with space", "See [[phantom]]."))
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 1, out)
        self.assertIn("with space.md: [[phantom]] resolves to nothing", out)

    def test_a_non_ascii_path_is_checked(self):
        self.v.write("concepts/caf\u00e9.md", page("caf\u00e9", "See [[phantom]]."))
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 1, out)
        self.assertIn("caf\u00e9.md: [[phantom]] resolves to nothing", out)

    def test_deleting_a_page_with_a_space_finds_its_inbound_links(self):
        self.v.write("concepts/beta two.md", page("beta two", "Text."))
        self.v.write("concepts/alpha.md", page("alpha", "See [[beta]] and [[beta two]]."))
        self.v.git("add", "-A")
        self.v.git("commit", "-q", "-m", "more")
        self.v.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.v.remove("concepts/beta two.md")
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 1, out)
        self.assertIn("links [[beta two]], which this change removes", out)

    def test_updated_matching_an_older_commit_passes(self):
        self.v.write("concepts/gamma.md", dated_page("gamma", "Text.", DAYS_AGO))
        self.v.commit(date=DAYS_AGO)
        code, out = self.v.run()
        self.assertEqual(code, 0, out)

    def test_updated_older_than_the_commit_is_flagged(self):
        self.v.write("concepts/gamma.md", dated_page("gamma", "Text.", "2026-01-02"))
        self.v.commit(date=DAYS_AGO)
        code, out = self.v.run()
        self.assertEqual(code, 1, out)
        self.assertIn(f"`updated: 2026-01-02` but last edited {DAYS_AGO}", out)

    def test_a_mermaid_block_inside_a_callout_is_not_read_as_links(self):
        body = "> [!note] Figure\n> ```mermaid\n> graph LR\n>   A[[subroutine]] --> B\n> ```"
        self.v.write("concepts/gamma.md", page("gamma", body))
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 0, out)

    def test_a_tilde_fence_is_not_read_as_links(self):
        self.v.write("concepts/gamma.md", page("gamma", "~~~\n[[not-a-link]]\n~~~"))
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 0, out)

    def test_a_link_after_a_closed_callout_fence_is_still_checked(self):
        body = "> ```\n> [[inside]]\n> ```\n\nSee [[phantom]]."
        self.v.write("concepts/gamma.md", page("gamma", body))
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 1, out)
        self.assertIn("[[phantom]]", out)
        self.assertNotIn("[[inside]]", out)

    def test_frontmatter_closes_only_on_a_bare_dash_line(self):
        text = (f"---\ntitle: gamma\ntype: concept\ncreated: 2026-01-01\n"
                f"updated: {TODAY}\ntags: []\n----\n\nBody.\n")
        self.v.write("concepts/gamma.md", text)
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 1, out)
        self.assertIn("frontmatter block is not closed", out)

    def test_a_one_line_triple_backtick_span_does_not_open_a_fence(self):
        self.v.write("concepts/gamma.md", page("gamma", "```code``` is inline.\n\nSee [[phantom]]."))
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 1, out)
        self.assertIn("[[phantom]]", out)

    def test_a_rewritten_committer_date_does_not_age_the_edit(self):
        self.v.write("concepts/gamma.md", dated_page("gamma", "Text.", DAYS_AGO))
        self.v.git("add", "-A")
        env = dict(os.environ, GIT_AUTHOR_DATE=f"{DAYS_AGO}T12:00:00",
                   GIT_COMMITTER_DATE=f"{TODAY}T12:00:00")
        subprocess.run(["git", "commit", "-q", "-m", "rebased"], cwd=self.v.dir,
                       check=True, capture_output=True, env=env)
        code, out = self.v.run()
        self.assertEqual(code, 0, out)

    def test_a_dotted_page_name_resolves(self):
        self.v.write("concepts/v1.2-notes.md", page("v1.2-notes", "Text."))
        self.v.write("concepts/gamma.md", page("gamma", "See [[v1.2-notes]] and [[alpha.md]]."))
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 0, out)

    def test_deleting_a_dotted_page_finds_its_inbound_links(self):
        self.v.write("concepts/v1.2-notes.md", page("v1.2-notes", "Text."))
        self.v.write("concepts/alpha.md", page("alpha", "See [[beta]] and [[v1.2-notes]]."))
        self.v.git("add", "-A")
        self.v.git("commit", "-q", "-m", "more")
        self.v.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.v.remove("concepts/v1.2-notes.md")
        self.v.commit()
        code, out = self.v.run()
        self.assertEqual(code, 1, out)
        self.assertIn("links [[v1.2-notes]], which this change removes", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
