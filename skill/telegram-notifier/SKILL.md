---
name: telegram-notifier
description: Send a Telegram completion reminder when you judge the current result is worth proactively notifying the user about. Use after the work is actually complete and the user may have stepped away.
---

# telegram-notifier

## What This Skill Does

This skill sends one concise plain-text Telegram reminder after work is truly done. It is a reminder, not a full report.

## When to Use

Use this skill when:
- the work is not an instant reply and the user may have stepped away while waiting
- the result is worth pulling the user back to the current session
- the work is actually complete and ready for the final reply

Do not use this skill when:
- the task is a quick answer or a small fast edit
- the work is still in progress, blocked, or waiting on review
- you are tempted to send a progress update or intermediate status

## Rules

- Send only after actual completion.
- Do not send progress notifications.
- Send only once per task when possible.
- If you retry part of the task or the final reply, avoid duplicate sends.
- Keep the message short, plain text, and non-sensitive.
- Do not include secrets, credentials, private data, or long technical dumps.
- Try sending the reminder first; do not proactively check local config before every send.
- If sending fails, then check whether `skill/telegram-notifier/config.local.env` is missing or incomplete.
- If config is missing or incomplete, read `references/setup-telegram.md` and run that setup flow.

## Workflow

1. Confirm the task is truly finished.
2. Read `assets/message-template.md` and use that exact plain-text structure.
3. Build a minimal reminder using:
    - current project name
    - current session id
    - a very short task label
    - the fixed completion wording already present in the template
    - task start time
4. Keep the final message to a single concise line whenever possible.
5. Run `python3 skill/telegram-notifier/scripts/send_telegram.py --config skill/telegram-notifier/config.local.env "<final message>"`.
6. If sending succeeds, stop.
7. If sending fails, note it briefly for yourself and check whether `skill/telegram-notifier/config.local.env` is missing or incomplete.
8. If config is missing or incomplete, read `references/setup-telegram.md` and complete that setup flow.
9. If setup succeeds, retry the same send once.
10. If setup is skipped, incomplete, or the retry still fails, continue with the normal final reply.
