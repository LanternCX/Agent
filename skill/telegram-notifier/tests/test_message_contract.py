import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "assets" / "message-template.md"
SKILL_PATH = ROOT / "SKILL.md"


class MessageContractTests(unittest.TestCase):
    def test_template_is_project_prefix_only(self) -> None:
        template = TEMPLATE_PATH.read_text(encoding="utf-8").strip()

        self.assertEqual(template, "[{{project_name}}]")

    def test_skill_no_longer_mentions_task_label(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertNotIn("task_label", skill_text)

    def test_skill_no_longer_requires_exact_old_message_structure(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertNotIn("use that exact plain-text structure", skill_text)


if __name__ == "__main__":
    unittest.main()
