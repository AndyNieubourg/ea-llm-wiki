#!/usr/bin/env python3
"""lint-aggregates.py counts the same pages in the tree and in the diff.

Each case builds a throwaway repository: a copy of lint-aggregates.py, a small
vault committed on `main`, `origin/main` pointed at it, and working-tree changes.

Run: python3 scripts/tests/test_lint_aggregates.py
"""

import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "lint-aggregates.py"


def question(status, ruminated):
    return (f"---\ntitle: q\ntype: question\ncreated: 2026-01-01\nupdated: 2026-01-01\n"
            f"status: {status}\nlast-ruminated: {ruminated}\n---\n\nBody.\n")


class Aggregates(unittest.TestCase):
    def setUp(self):
        self.dir = pathlib.Path(tempfile.mkdtemp(prefix="aggregates-test-"))
        (self.dir / "scripts").mkdir()
        shutil.copy(SCRIPT, self.dir / "scripts" / "lint-aggregates.py")
        for rel, text in {
            "wiki/questions/q1.md": question("open", "2026-01-01"),
            "wiki/questions/q2.md": question("open", "2026-01-01"),
            "notes/questions/q9.md": question("open", "2026-01-01"),
        }.items():
            self.write(rel, text)
        for args in (["init", "-q", "-b", "main"], ["config", "user.email", "t@example.invalid"],
                     ["config", "user.name", "t"], ["add", "-A"], ["commit", "-q", "-m", "main"],
                     ["update-ref", "refs/remotes/origin/main", "HEAD"]):
            subprocess.run(["git", *args], cwd=self.dir, check=True, capture_output=True)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def write(self, rel, text):
        path = self.dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_script(self, *flags):
        res = subprocess.run([sys.executable, "scripts/lint-aggregates.py", *flags],
                             cwd=self.dir, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        return res.stdout

    def test_a_status_move_outside_wiki_is_not_a_question_move(self):
        self.write("notes/questions/q9.md", question("answered", "2026-01-01"))
        self.write("wiki/questions/q1.md", question("converging", "2026-01-01"))
        out = self.run_script()
        self.assertIn("(frontmatter `status:` changed): 1", out)
        self.assertNotIn("notes/questions", out)

    def test_a_question_moved_out_of_questions_is_still_reported(self):
        subprocess.run(["git", "mv", "wiki/questions/q1.md", "wiki/analyses-q1.md"],
                       cwd=self.dir, check=True, capture_output=True)
        self.write("wiki/analyses-q1.md", question("answered", "2026-01-01"))
        out = self.run_script()
        self.assertIn("open → answered", out)

    def test_a_pyramid_sidecar_is_not_a_page_in_the_diff(self):
        self.write("wiki/analyses/essay.md", question("open", "2026-01-01"))
        self.write("wiki/analyses/essay.pyramid.md", "outline\n")
        self.write("wiki/.obsidian/scratch.md", "ui\n")
        out = self.run_script()
        self.assertIn("wiki pages: 1 added", out)

    def test_unchanged_questions_are_counted_not_listed(self):
        self.write("wiki/questions/q1.md", question("open", "2026-02-02"))
        out = self.run_script()
        self.assertIn("1 of 2", out)
        self.assertIn("(1 unchanged; --verbose lists them)", out)
        self.assertNotIn("unchanged  2026-01-01", out)
        self.assertIn("unchanged  2026-01-01  wiki/questions/q2.md", self.run_script("--verbose"))

    def test_frontmatter_closes_only_on_a_bare_dash_line(self):
        broken = question("converging", "2026-02-02").replace("\n---\n\nBody", "\n----\n\nBody")
        self.write("wiki/questions/q1.md", broken)
        out = self.run_script()
        self.assertIn("open → None", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
