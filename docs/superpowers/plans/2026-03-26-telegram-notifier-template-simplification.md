# Telegram Notifier Template Simplification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce the Telegram message template to a project-only prefix while updating the skill guidance so agents write short, situational suffixes that explain why the user should come back.

**Architecture:** Keep the message skeleton in `assets/message-template.md`, but narrow it to the project prefix only. Move the behavioral detail into `SKILL.md`. Use lightweight regression tests only for objective contract rules, then use focused document review for the softer writing guardrails so the plan protects behavior without freezing exact prose.

**Tech Stack:** Markdown skill docs, plain-text template asset, Python `unittest`

---

## File Map

- Modify: `skill/telegram-notifier/assets/message-template.md` — shrink the template to the project-only prefix.
- Modify: `skill/telegram-notifier/SKILL.md` — replace the old fixed-template instructions with the new prefix-plus-agent-written-suffix contract.
- Create: `skill/telegram-notifier/tests/test_message_contract.py` — regression tests for the template and documented message rules.

### Task 1: Lock the objective message contract with tests

**Files:**
- Create: `skill/telegram-notifier/tests/test_message_contract.py`
- Test: `skill/telegram-notifier/tests/test_message_contract.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "assets" / "message-template.md"
SKILL_PATH = ROOT / "SKILL.md"


class MessageContractTests(unittest.TestCase):
    def test_template_is_project_prefix_only(self) -> None:
        template = TEMPLATE_PATH.read_text(encoding="utf-8").strip()

        self.assertEqual(template, "[{{project_name}}]")

    def test_skill_drops_old_fixed_fields_and_keeps_prefix_assembly_rules(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertNotIn("task_label", skill_text)
        self.assertNotIn("use that exact plain-text structure", skill_text)
        self.assertIn("one space", skill_text)
        self.assertIn("project", skill_text)
        self.assertIn("prefix", skill_text)

    def test_skill_rejects_empty_suffixes(self) -> None:
        skill_text = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn("empty", skill_text)
        self.assertIn("suffix", skill_text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest skill/telegram-notifier/tests/test_message_contract.py -v`
Expected: FAIL because the template still contains `task_label` / `Completed` and `SKILL.md` still documents the old exact-structure behavior instead of the new prefix-plus-suffix contract.

- [ ] **Step 3: Write minimal implementation**

Update the template file to exactly:

```text
[{{project_name}}]
```

Update `SKILL.md` so the workflow says the agent reads the prefix, adds one space during message assembly, and writes a short suffix that explains why the user should return now. Remove references to `task_label` and fixed completion wording, and explicitly reject empty suffixes.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest skill/telegram-notifier/tests/test_message_contract.py -v`
Expected: PASS

### Task 2: Update the skill wording for style guardrails and review it directly

**Files:**
- Modify: `skill/telegram-notifier/SKILL.md`
- Test: `skill/telegram-notifier/tests/test_message_contract.py`

- [ ] **Step 1: Review the approved style guardrails before editing**

Re-read the spec and confirm these soft constraints must all be present in the final wording:

- The suffix explains why the user should come back now.
- The message stays short, single-line-first, plain-text, and non-sensitive.
- The suffix may include a small amount of key outcome detail.
- The message remains a reminder, not a report.
- Scenario markers like review / confirmation / reply are guidance only, not fixed sample sentences.

- [ ] **Step 2: Update `SKILL.md` with the approved middle ground**

Add concise wording in `SKILL.md` that preserves those five constraints without introducing new hard-coded example sentences.

- [ ] **Step 3: Run the objective contract tests again**

Run: `python3 -m unittest skill/telegram-notifier/tests/test_message_contract.py -v`
Expected: PASS

- [ ] **Step 4: Do a direct wording review against the spec**

Read the updated `skill/telegram-notifier/SKILL.md` and verify all five style guardrails are clearly present in meaning, even if the exact wording differs from the spec.

### Task 3: Run focused verification

**Files:**
- Test: `skill/telegram-notifier/tests/test_message_contract.py`
- Test: `skill/telegram-notifier/tests/test_send_telegram.py`

- [ ] **Step 1: Run the notifier contract tests**

Run: `python3 -m unittest skill/telegram-notifier/tests/test_message_contract.py -v`
Expected: PASS

- [ ] **Step 2: Run the existing notifier script tests**

Run: `python3 -m unittest skill/telegram-notifier/tests/test_send_telegram.py -v`
Expected: PASS

- [ ] **Step 3: Run the full notifier test directory**

Run: `python3 -m unittest discover -s skill/telegram-notifier/tests -p 'test_*.py' -v`
Expected: PASS for both the existing SSL-context test and the new message-contract regression coverage
