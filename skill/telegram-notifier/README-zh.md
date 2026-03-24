# telegram-notifier

## 这是做什么的

这个 skill 会在任务真正完成、而且值得主动提醒你回来看结果时，发送一条简短的 Telegram 提醒。它不是完整报告，只是告诉你可以回来继续看当前会话了。

## 会收到什么

提醒默认保持很短，只包含这些最小信息：
- 项目名
- session 标识
- 任务短标签
- 已完成状态
- 任务开始时间

这些内容都由 Agent 自动填写。详细结果仍然以当前会话里的回复为准。

## 第一次使用

第一次真的需要发送提醒时，Agent 会自动检查本地配置是否齐全。若还没准备好，它会按 `references/setup-telegram.md` 的流程做一次很短的引导，并在你提供两个必填值后写好本地配置。在这个仓库里，你不需要为 skill 额外安装别的组件，但在第一次发送提醒前，仍然要先准备好 bot token 和 chat id。如果你这次不想配置，也可以直接跳过当前提醒，主任务不会受影响。

## 本地配置

本地配置文件路径是 `skill/telegram-notifier/config.local.env`，只保存在当前机器，不应提交。

必填项只有两个：
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

## 如何拿到这两个值

最短路径是这样：

- `TELEGRAM_BOT_TOKEN`：先去 BotFather 创建机器人，再复制它返回的 token
- `TELEGRAM_CHAT_ID`：先给目标聊天发一条消息，再打开 `https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getUpdates`，从那条会话里的 `chat.id` 复制纯数字 chat ID

如果 `getUpdates` 返回空列表，先打开这个 bot 的聊天窗口，点一次 `Start` 或发一条 `hi`，等一秒后再刷新同一个地址。

## 手动测试

```bash
python3 skill/telegram-notifier/scripts/send_telegram.py --config skill/telegram-notifier/config.local.env "[Agent][agent-repo] Session abc123 已完成：Telegram notifier。开始于 14:02。"
```

这个仓库里的默认提醒文案有意保持中文；如果你以后把它复用到别处，可以改模板文案，但不需要改发送脚本的调用方式。

## 常见情况

- 没有传入 `--config` 时，脚本会直接报错
- 缺少 `TELEGRAM_BOT_TOKEN` 或 `TELEGRAM_CHAT_ID` 时，脚本会给出清晰提示
- 如果 Telegram 暂时不可达，这次提醒按尽力而为处理，不影响主任务完成
