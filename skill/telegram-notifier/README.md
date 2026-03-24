# telegram-notifier

## What It Does

This skill sends one short plain-text Telegram reminder after a task is truly complete and worth proactively surfacing. It is a reminder, not a full report.

## What The Reminder Includes

The message stays minimal and only includes:
- project name
- session id
- short task label
- completion status
- task start time

The Agent fills these values automatically. The full result still lives in the current session.

## First Use

On first real use, the Agent checks whether local config is ready. If not, it follows `references/setup-telegram.md`, guides the user through a short setup, and writes the local config after the user provides the two required values. In this repo, you do not need an extra install step for the skill itself, but you still need a bot token and chat id before the first reminder can be sent. If you do not want to configure it yet, the current reminder is skipped and the main task continues.

## Local Config

The local config file lives at `skill/telegram-notifier/config.local.env` and should not be committed.

Required keys:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

## How to get the two values

Use the shortest path that gets the value:

- `TELEGRAM_BOT_TOKEN`: create a bot with BotFather, then copy the token it returns
- `TELEGRAM_CHAT_ID`: send a message to the target chat first, open `https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getUpdates`, then copy the numeric `chat.id` from that conversation

If `getUpdates` returns an empty list, open the bot chat, press `Start` or send a short message like `hi`, wait a second, and refresh the same URL.

## Manual test

```bash
python3 skill/telegram-notifier/scripts/send_telegram.py --config skill/telegram-notifier/config.local.env "[Agent][agent-repo] Session abc123 已完成：Telegram notifier。开始于 14:02。"
```

The default reminder text is intentionally Chinese in this repo. If you later reuse the skill elsewhere, you can change the template wording without changing the sender script contract.

## Common cases

- If `--config` is missing, the script fails immediately.
- If `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` is missing, the script returns a clear error.
- If Telegram is unreachable, treat the reminder as best-effort and continue the main task.
