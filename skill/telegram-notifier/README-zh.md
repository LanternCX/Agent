# telegram-notifier

这个 skill 会在任务真正完成、而且值得主动提醒你回来看结果时，发送一条简短的 Telegram 提醒叫你回来干活。

## 快速开始

安装这个 Skill 到你的全局 Skill。

第一次使用的时候 Agent 会引导你配置。

配置完之后就能用了。

## 手动配置

本地配置文件路径是 `skill/telegram-notifier/config.local.env`

必填项：
- `TELEGRAM_BOT_TOKEN`：先去 (@BotFather)[https://t.me/BotFather] 创建机器人，再复制它返回的 token
- `TELEGRAM_CHAT_ID`：给机器人发一条消息，打开 `https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getUpdates`，从那条会话里的 `chat.id` 复制纯数字 chat ID

## 常见情况

- 没有传入 `--config` 时，脚本会直接报错
- 缺少 `TELEGRAM_BOT_TOKEN` 或 `TELEGRAM_CHAT_ID` 时，脚本会给出清晰提示
- 如果 Telegram 暂时不可达，这次提醒按尽力而为处理，不影响主任务完成
