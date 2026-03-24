# Setup Telegram

Use this file only when `skill/telegram-notifier/config.local.env` is missing or incomplete.

## Goal

Collect the two required values, write `config.local.env`, then return to the normal reminder flow.

## Questions

Ask for these values one at a time:

1. `TELEGRAM_BOT_TOKEN`
2. `TELEGRAM_CHAT_ID`

If the user does not know where to get them, give the shortest practical hint:

- for `TELEGRAM_BOT_TOKEN`: create a bot with BotFather and copy the returned token
- for `TELEGRAM_CHAT_ID`: send a message to the target chat first, open `https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getUpdates`, find the latest conversation under `chat.id`, and copy only the numeric chat id

If the user says `getUpdates` returns an empty result, guide them with the shortest next step:

- open the bot chat in Telegram
- press `Start` or send a short message like `hi`
- wait a second and refresh the same `getUpdates` URL
- then copy the numeric value from `"chat":{"id":...}`

## Rules

- Keep setup short and guided.
- Explain that the file is stored locally at `skill/telegram-notifier/config.local.env`.
- Do not ask the user to manually edit a config file.
- If the user does not want to configure it now, skip this notification and continue the main task.
- If the user is unsure where to look, give the shortest next step instead of abstract API jargon.
- Remind the user that project name, session id, completion status, and start time are filled automatically later and do not need to be provided during setup.

## Write Format

Write exactly this structure:

```env
TELEGRAM_BOT_TOKEN=<value>
TELEGRAM_CHAT_ID=<value>
```

## Return To Main Flow

After writing the file:

1. Confirm setup is complete in one short sentence.
2. If the user chose not to configure it now, skip the reminder and return to the main task.
3. Otherwise return to the reminder workflow.
4. Send the Telegram reminder for the current completed task.
