# telegram-notifier

This skill sends a short Telegram reminder to call you back to work when a task is truly finished and worth proactively surfacing.

## Quick Start

Install this skill into your global skills.

The Agent guides you through setup the first time you use it.

After setup, it is ready to use.

## Manual Setup

The local config file path is `skill/telegram-notifier/config.local.env`

Required values:
- `TELEGRAM_BOT_TOKEN`: create a bot with [@BotFather](https://t.me/BotFather), then copy the token it returns
- `TELEGRAM_CHAT_ID`: send a message to the bot, open `https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getUpdates`, then copy the numeric `chat.id` from that conversation

## Common Cases

- If `--config` is missing, the script fails immediately
- If `TELEGRAM_BOT_TOKEN` or `TELEGRAM_CHAT_ID` is missing, the script returns a clear error
- If Telegram is temporarily unreachable, treat the reminder as best-effort and continue the main task
