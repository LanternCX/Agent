# Telegram Notifier Failure-Driven Config Check Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the Telegram notifier skill so it only guides configuration checks after a send attempt fails, instead of checking configuration before every send.

**Architecture:** Keep the change limited to the skill instructions in `skill/telegram-notifier/SKILL.md`. Move the config-check trigger from the pre-send path to the failure-handling path, and define one recovery retry after setup succeeds so the reminder still has a chance to send.

**Tech Stack:** Markdown skill definition, existing Python sender script, repo docs under `docs/superpowers/`

---

## File Map

- Modify: `skill/telegram-notifier/SKILL.md` - change the rules and workflow so config inspection happens only after a failed send attempt
- Reference: `skill/telegram-notifier/references/setup-telegram.md` - keep setup handoff wording aligned with the new post-failure trigger
- Reference: `docs/superpowers/specs/2026-03-25-telegram-notifier-failure-driven-config-check-design.md` - approved design source for the behavior change

### Task 1: Update Skill Rules

**Files:**
- Modify: `skill/telegram-notifier/SKILL.md`
- Reference: `docs/superpowers/specs/2026-03-25-telegram-notifier-failure-driven-config-check-design.md`

- [ ] **Step 1: Read the current rule block and locate the pre-send config check wording**

Inspect `skill/telegram-notifier/SKILL.md:24` and identify the line that currently tells the agent to check `config.local.env` before sending.

- [ ] **Step 2: Replace the old rule with failure-driven wording**

Update the rules so they explicitly say:

```md
- Try sending the reminder first; do not proactively check local config before every send.
- If sending fails, then check whether `skill/telegram-notifier/config.local.env` is missing or incomplete.
- If config is missing or incomplete, read `references/setup-telegram.md` and run that setup flow.
```

- [ ] **Step 3: Verify the rule text matches the approved design**

Check that the rule no longer requires pre-send inspection and still preserves best-effort behavior.

### Task 2: Rewrite The Workflow Sequence

**Files:**
- Modify: `skill/telegram-notifier/SKILL.md`
- Reference: `skill/telegram-notifier/references/setup-telegram.md`

- [ ] **Step 1: Write the new ordered workflow as a failing expectation checklist**

Use this target flow while editing:

```md
1. Confirm the task is truly finished.
2. Read `assets/message-template.md` and use that exact plain-text structure.
3. Build a minimal reminder using the existing required fields.
4. Keep the final message to a single concise line whenever possible.
5. Run `python3 skill/telegram-notifier/scripts/send_telegram.py --config skill/telegram-notifier/config.local.env "<final message>"`.
6. If sending succeeds, stop.
7. If sending fails, note it briefly for yourself and check whether `skill/telegram-notifier/config.local.env` is missing or incomplete.
8. If config is missing or incomplete, read `references/setup-telegram.md` and complete that setup flow.
9. If setup succeeds, retry the same send once.
10. If setup is skipped, incomplete, or the retry still fails, continue with the normal final reply.
```

- [ ] **Step 2: Edit the workflow block in `skill/telegram-notifier/SKILL.md`**

Remove the current step that forces setup before any send attempt, then insert the new post-failure recovery path.

- [ ] **Step 3: Verify the setup and retry branches are explicit**

Confirm the workflow answers all three cases clearly:

```text
- send succeeds immediately
- send fails because config is missing/incomplete and setup succeeds
- send still cannot complete, so the main task continues without blocking
```

### Task 3: Review And Validate The Instruction Change

**Files:**
- Modify: `skill/telegram-notifier/SKILL.md`

- [ ] **Step 1: Read the full updated file once**

Run a file read on `skill/telegram-notifier/SKILL.md` and confirm the Rules and Workflow sections tell the same story.

- [ ] **Step 2: Run a targeted text check**

Run: `python3 - <<'PY'
from pathlib import Path
text = Path('skill/telegram-notifier/SKILL.md').read_text()
assert 'If `skill/telegram-notifier/config.local.env` is missing or incomplete, read `references/setup-telegram.md` and run the setup flow first.' not in text
assert 'If sending fails' in text
assert 'retry' in text.lower()
print('ok')
PY`

Expected: `ok`

- [ ] **Step 3: Sanity-check the referenced setup doc still fits**

Read `skill/telegram-notifier/references/setup-telegram.md` and confirm it still works when invoked after failure rather than before the first send attempt.

- [ ] **Step 4: Commit**

```bash
git add skill/telegram-notifier/SKILL.md
git commit -m "fix(skill): check telegram config after send failure"
```

Only do this step if the user explicitly asks for a commit.
