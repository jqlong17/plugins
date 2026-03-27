from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.init_workflow import TEMPLATES, build_existing_workflow_advice, initialize_workflow


PLUGIN_ROOT = Path(__file__).resolve().parent.parent


class InitWorkflowTests(unittest.TestCase):
    def test_initialize_creates_full_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir)

            summary = initialize_workflow(target)

            self.assertEqual(len(summary["created"]), len(TEMPLATES))
            self.assertFalse(summary["updated"])
            self.assertFalse(summary["skipped"])

            for relative_path in TEMPLATES:
                self.assertTrue((target / relative_path).exists(), relative_path)

    def test_existing_workflow_advice_mentions_no_changes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir)
            initialize_workflow(target)

            advice = build_existing_workflow_advice(target / "workflow")

            self.assertIn("No files were changed", advice)
            self.assertIn("Suggested review items", advice)

    def test_cli_refuses_to_modify_existing_workflow_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir)
            initialize_workflow(target)
            readme_path = target / "workflow/README.md"
            readme_path.write_text("user content", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, "scripts/init_workflow.py", str(target)],
                cwd=PLUGIN_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Detected an existing workflow directory", result.stdout)
            self.assertEqual(readme_path.read_text(encoding="utf-8"), "user content")

    def test_force_overwrites_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir)

            initialize_workflow(target)
            readme_path = target / "workflow/README.md"
            readme_path.write_text("changed", encoding="utf-8")

            summary = initialize_workflow(target, force=True)

            self.assertIn("workflow/README.md", summary["updated"])
            self.assertEqual(readme_path.read_text(encoding="utf-8"), TEMPLATES["workflow/README.md"])

    def test_readme_is_unnumbered_and_other_markdown_files_are_numbered(self) -> None:
        markdown_paths = [Path(path) for path in TEMPLATES if path.endswith(".md")]

        for path in markdown_paths:
            if path.name.lower() == "readme.md":
                continue
            self.assertRegex(path.name, r"^\d{2}-.+\.md$")

    def test_allow_existing_workflow_flag_permits_updates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir)
            initialize_workflow(target)
            readme_path = target / "workflow/README.md"
            readme_path.write_text("user content", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/init_workflow.py",
                    str(target),
                    "--force",
                    "--allow-existing-workflow",
                ],
                cwd=PLUGIN_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Initialized workflow under", result.stdout)
            self.assertEqual(readme_path.read_text(encoding="utf-8"), TEMPLATES["workflow/README.md"])


if __name__ == "__main__":
    unittest.main()
