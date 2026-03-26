---
name: telegram-notifier
description: Use when non-instant work reaches a user-facing checkpoint and you need the user back for review, confirmation, reply, or completion.
---

# telegram-notifier

## What This Skill Does

This skill sends one concise plain-text Telegram reminder when work reaches a point where the user should come back. It is a reminder, not a full report.

## When to Use

Use this skill when:
- the work is not an instant reply and the user may have stepped away while waiting
- the result is worth pulling the user back to the current session
- the work is fully complete and ready for the final reply
- the work has reached a natural stopping point and now needs user review, confirmation, or a reply

Do not use this skill when:
- the task is a quick answer or a small fast edit
- the work is still actively in progress and does not need anything from the user yet
- you are tempted to send a progress update or intermediate status

## Rules

- Send only when the work is fully complete or paused at a user-facing checkpoint.
- Do not send progress notifications.
- Send only once per task when possible.
- If you retry part of the task, return to the same checkpoint, or send the final reply later, avoid duplicate sends.
- Keep the message short, plain text, and non-sensitive.
- Prefer a single concise line.
- Start from the project prefix in the template, then add a short suffix that tells the user why they should come back now.
- Add exactly one space between the project prefix and the suffix when assembling the final message.
- The suffix may include a small amount of key outcome detail if it helps the user judge urgency.
- The suffix must not be empty or reduced to a vague status word.
- Treat markers like review, confirmation, or reply as direction, not fixed sample sentences.
- Do not include secrets, credentials, private data, or long technical dumps.
- Try sending the reminder first; do not proactively check local config before every send.
- If sending fails, then check whether `skill/telegram-notifier/config.local.env` is missing or incomplete.
- If config is missing or incomplete, read `references/setup-telegram.md` and run that setup flow.

## Workflow

1. Confirm the work is either truly finished or paused at a checkpoint that needs the user back.
2. Read `assets/message-template.md` and use it as the project prefix only.
3. Add one space after that prefix.
4. Write a short plain-text suffix that explains why the user should come back now.
5. If useful, include a small amount of key outcome detail, but keep the message a reminder rather than a report.
6. Keep the final message to a single concise line whenever possible.
7. Run `python3 skill/telegram-notifier/scripts/send_telegram.py --config skill/telegram-notifier/config.local.env "<final message>"`.
8. If sending succeeds, stop.
9. If sending fails, note it briefly for yourself and check whether `skill/telegram-notifier/config.local.env` is missing or incomplete.
10. If config is missing or incomplete, read `references/setup-telegram.md` and complete that setup flow.
11. If setup succeeds, retry the same send once.
12. If setup is skipped, incomplete, or the retry still fails, continue with the normal final reply.
