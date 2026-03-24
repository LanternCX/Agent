# Telegram Notifier Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 交付一个定位为全局复用的完成提醒 skill，并在当前仓库内完成其目录、脚本、模板和说明，让 Agent 在自主判断当前结果值得主动提醒用户、且任务真正完成后，通过本地脚本向 Telegram 发送简洁提醒。

**Architecture:** 该功能拆成 6 个清晰单元：`SKILL.md` 负责触发规则与调用约束，`assets/message-template.md` 固定通知文案结构，`scripts/send_telegram.py` 负责读取显式传入的配置文件并发送消息，`config.example.env` 提供轻量配置模板，`README-zh.md` 作为主要面向用户的说明，`README.md` 提供同方向的英文简版说明。测试使用 Python 标准库 `unittest`，覆盖配置读取、消息发送请求构造与失败降级，不引入额外依赖。

**Tech Stack:** Markdown, Python 3, Telegram Bot API, unittest

---

### Task 1: 搭建 skill 目录与静态资源

**Files:**
- Create: `skill/telegram-notifier/SKILL.md`
- Create: `skill/telegram-notifier/assets/message-template.md`
- Create: `skill/telegram-notifier/config.example.env`
- Create: `skill/telegram-notifier/README.md`

- [ ] **Step 1: 创建 skill 目录骨架**

创建以下目录：

```text
skill/telegram-notifier/
skill/telegram-notifier/assets/
skill/telegram-notifier/scripts/
```

- [ ] **Step 2: 编写通知模板初稿**

在 `skill/telegram-notifier/assets/message-template.md` 写入单一模板，保留这些占位变量：

```text
[Agent][{{project_name}}] Session {{session_id}} 已完成：{{task_label}}。开始于 {{started_at}}。
```

要求：
- 模板固定为纯文本，不加入 Markdown 语法

- [ ] **Step 3: 创建 `SKILL.md` 占位文件**

先在 `skill/telegram-notifier/SKILL.md` 写入最小占位内容，确保目录骨架完整：

```markdown
---
name: telegram-notifier
description: placeholder
---
```

后续在 Task 4 再补齐正式内容。

- [ ] **Step 4: 编写配置模板**

在 `skill/telegram-notifier/config.example.env` 写入：

```env
TELEGRAM_BOT_TOKEN=123456:replace-me
TELEGRAM_CHAT_ID=replace-me
```

并补一行注释，说明这是示例模板，开发与测试时请在仓库内复制出自己的本地配置文件使用。

- [ ] **Step 5: 编写 README 骨架**

在 `skill/telegram-notifier/README.md` 先写出以下固定章节标题：

```markdown
# telegram-notifier
## What It Does
## First Use
## Configure
## How Agents Should Use It
## Troubleshooting
```

- [ ] **Step 6: 与用户确认首个提交说明（如需要提交）**

建议提交说明：`feat(skill): scaffold telegram notifier`

只有用户明确确认提交说明后，才执行：

```bash
git add skill/telegram-notifier/SKILL.md skill/telegram-notifier/assets/message-template.md skill/telegram-notifier/config.example.env skill/telegram-notifier/README.md
git commit -m "feat(skill): scaffold telegram notifier"
```

### Task 2: 先写发送脚本测试

**Files:**
- Create: `tests/skill/telegram_notifier/test_send_telegram.py`
- Test: `tests/skill/telegram_notifier/test_send_telegram.py`

- [ ] **Step 1: 写配置加载的失败用例**

在 `tests/skill/telegram_notifier/test_send_telegram.py` 写一个 `unittest.TestCase`，并先用 `importlib.util.spec_from_file_location` 从 `skill/telegram-notifier/scripts/send_telegram.py` 动态加载模块，避免因为目录名包含连字符而直接导入失败。随后覆盖“配置文件不存在时返回明确错误”的行为：

```python
def test_load_config_fails_when_file_missing(self):
    with self.assertRaisesRegex(FileNotFoundError, "telegram-notifier"):
        load_config(Path("/tmp/does-not-exist.env"))
```

- [ ] **Step 2: 写成功加载配置的用例**

补一个用例，确认脚本能读取 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID`。

- [ ] **Step 3: 写发送请求成功用例**

补一个用例，mock `urllib.request.urlopen`，校验请求发向：

```text
https://api.telegram.org/bot<token>/sendMessage
```

并断言请求体至少包含：

```python
{"chat_id": "123", "text": "done"}
```

- [ ] **Step 4: 写 Telegram 返回失败的用例**

补一个用例，mock API 返回 `{"ok": false, "description": "Bad Request"}`，断言脚本返回失败状态而不是抛出未处理异常。

- [ ] **Step 5: 写命令行入口用例**

补一个用例，覆盖 `main(argv)` 在未传入 `--config` 时返回 `1`，并输出提示需要显式提供配置文件路径的简短错误文本。

- [ ] **Step 6: 运行测试确认当前失败**

Run: `python3 -m unittest tests/skill/telegram_notifier/test_send_telegram.py -v`
Expected: FAIL，提示 `load_config` / `send_message` 尚未实现或模块不存在

### Task 3: 实现发送脚本

**Files:**
- Create: `skill/telegram-notifier/scripts/send_telegram.py`
- Modify: `tests/skill/telegram_notifier/test_send_telegram.py`
- Test: `tests/skill/telegram_notifier/test_send_telegram.py`

- [ ] **Step 1: 实现最小配置读取函数**

在 `skill/telegram-notifier/scripts/send_telegram.py` 写出最小实现：

```python
def load_config(config_path: Path) -> dict[str, str]:
    ...
```

要求：
- 仅支持 `KEY=value` 简单格式
- 缺少 `TELEGRAM_BOT_TOKEN` 或 `TELEGRAM_CHAT_ID` 时抛出 `ValueError`
- 文件不存在时抛出 `FileNotFoundError`

- [ ] **Step 2: 实现发送函数**

写出：

```python
def send_message(config: dict[str, str], message_text: str) -> tuple[bool, str]:
    ...
```

要求：
- 用 `urllib.request` 发 POST 请求
- 发送 JSON 体，只包含 `chat_id` 与 `text`
- Telegram 返回 `ok=true` 时返回 `(True, "sent")`
- Telegram 返回 `ok=false` 或网络异常时返回 `(False, <reason>)`

- [ ] **Step 3: 实现命令行入口**

写出：

```python
def main(argv: list[str]) -> int:
    ...
```

要求：
- 通过 `--config <path>` 显式接收配置文件路径
- 接收一个必填参数：最终消息文本
- 成功时退出码为 `0`
- 配置错误、发送失败时退出码为 `1`

- [ ] **Step 4: 运行单测确认通过**

Run: `python3 -m unittest tests/skill/telegram_notifier/test_send_telegram.py -v`
Expected: PASS

- [ ] **Step 5: 做一次脚本冒烟检查**

Run: `python3 skill/telegram-notifier/scripts/send_telegram.py "smoke test"`
Expected: 因未传入 `--config` 而以清晰错误退出，不出现 Python traceback 噪音

- [ ] **Step 6: 与用户确认第二个提交说明（如需要提交）**

建议提交说明：`feat(skill): add Telegram sender script`

只有用户明确确认提交说明后，才执行：

```bash
git add skill/telegram-notifier/scripts/send_telegram.py tests/skill/telegram_notifier/test_send_telegram.py
git commit -m "feat(skill): add Telegram sender script"
```

### Task 4: 编写全局 skill 规则与说明文档

**Files:**
- Modify: `skill/telegram-notifier/SKILL.md`
- Modify: `skill/telegram-notifier/README.md`
- Modify: `skill/telegram-notifier/assets/message-template.md`

- [ ] **Step 1: 完成 `SKILL.md` 头部元信息**

写入：

```yaml
---
name: telegram-notifier
description: Send a Telegram completion reminder when you judge the current result is worth proactively notifying the user about. Use after the work is actually complete and the user may have stepped away.
---
```

- [ ] **Step 2: 写清“应该调用”和“不应调用”的边界**

在 `SKILL.md` 中明确写出：
- 不是即时完成型工作、用户可能离开时，应考虑调用
- 简单问答、快速小改动、尚未完成时，不调用
- 不允许在任务中途发送进度通知
- 每个任务只应发送一次，收尾重试时应尽量避免重复发送

- [ ] **Step 3: 写清固定调用流程**

在 `SKILL.md` 中用顺序步骤写出：
1. 确认任务真正完成
2. 如果 `skill/telegram-notifier/config.local.env` 缺失或不完整，则读取 `references/setup-telegram.md` 并完成首次初始化
3. 读取 `assets/message-template.md`
4. 生成只包含项目名、session 标识、任务短标签、完成状态和开始时间的最终纯文本消息
5. 运行 `python3 skill/telegram-notifier/scripts/send_telegram.py --config skill/telegram-notifier/config.local.env "<final message>"`
6. 若发送失败，只做简短记录，不影响主任务回复

- [ ] **Step 4: 完成 README 使用与配置说明**

在 `skill/telegram-notifier/README.md` 与 `skill/telegram-notifier/README-zh.md` 补齐：
- 本次只在当前仓库内开发，不做真实安装
- 首次使用时由 Agent 自动引导创建 `config.local.env`
- 如何获取 `TELEGRAM_CHAT_ID`
- 如何做一次手动发送测试
- 为什么通知只是一条提醒而不是完整报告

- [ ] **Step 5: 人工复核文档与模板的一致性**

逐项检查 `SKILL.md`、`README.md`、`README-zh.md`、`assets/message-template.md`：
- 发送方式都写成纯文本
- 都要求显式传入配置路径，不依赖真实全局安装
- 都没有重新引入固定分钟阈值

- [ ] **Step 6: 与用户确认第三个提交说明（如需要提交）**

建议提交说明：`feat(skill): document telegram notifier workflow`

只有用户明确确认提交说明后，才执行：

```bash
git add skill/telegram-notifier/SKILL.md skill/telegram-notifier/README.md skill/telegram-notifier/assets/message-template.md skill/telegram-notifier/config.example.env skill/telegram-notifier/references/setup-telegram.md skill/telegram-notifier/.gitignore
git commit -m "feat(skill): document telegram notifier workflow"
```

### Task 5: 端到端验证与收尾

**Files:**
- Check: `skill/telegram-notifier/SKILL.md`
- Check: `skill/telegram-notifier/scripts/send_telegram.py`
- Check: `skill/telegram-notifier/assets/message-template.md`
- Check: `skill/telegram-notifier/config.example.env`
- Check: `skill/telegram-notifier/README.md`
- Check: `skill/telegram-notifier/README-zh.md`
- Check: `skill/telegram-notifier/references/setup-telegram.md`
- Test: `tests/skill/telegram_notifier/test_send_telegram.py`

- [ ] **Step 1: 运行自动化测试**

Run: `python3 -m unittest tests/skill/telegram_notifier/test_send_telegram.py -v`
Expected: PASS

- [ ] **Step 2: 做一次模板到脚本的本地串联检查**

用一个示例消息运行：

Run: `python3 skill/telegram-notifier/scripts/send_telegram.py --config skill/telegram-notifier/config.local.env "[Agent][agent-repo] Session abc123 已完成：Telegram notifier。开始于 14:02。"`

Expected: 
- 若本地配置完整且 Telegram 可达，则发送成功
- 若 `config.local.env` 缺失或配置不完整，则给出清晰错误，不影响其他文件

- [ ] **Step 3: 对照 spec 做人工验收**

逐项核对 `docs/superpowers/specs/2026-03-24-telegram-notifier-design.md` 中的验收标准，确认：
- 是全局复用 skill 目录结构
- 由 Agent 判断这次完成是否值得提醒
- 脚本负责真实发送
- 配置轻量且无分钟阈值
- 失败不阻塞主任务

- [ ] **Step 4: 整理最终交付说明**

准备最终说明时，至少覆盖：
- 新增了哪些文件
- 如何在当前仓库内完成首次初始化
- 如何做手动验证

- [ ] **Step 5: 如用户要求提交，再先确认提交说明**

建议合并提交说明：`feat(skill): add telegram notifier`

只有用户明确确认提交说明后，才执行：

```bash
git add skill/telegram-notifier tests/skill/telegram_notifier docs/superpowers/specs/2026-03-24-telegram-notifier-design.md docs/superpowers/plans/2026-03-24-telegram-notifier.md
git commit -m "feat(skill): add telegram notifier"
```
