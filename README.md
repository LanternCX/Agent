# 我的 Agent Harness

个人规则与常用 Skills。

## Quickstart

把下面这句话发给 Agent：

```text
请阅读 https://github.com/LanternCX/Agent/blob/main/INSTALL.md，并按照说明完成安装。
```

## 组件

| 组件 | 用途 | 来源 |
| --- | --- | --- |
| Matt Skills | 开发工作流 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| Ponytail | 简化实现，控制复杂度 | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |
| 个人规则 | 协作偏好与开发约束 | [rules/AGENTS.md](rules/AGENTS.md) |

独立 Skill 安装到 `~/.agents/skills/`；工作流套件遵循上游安装说明。具体步骤见 [安装说明](INSTALL.md)。

## 可选 Skills

以下 Skills 按需安装：

| Skill | 用途 | 来源 |
| --- | --- | --- |
| Frontend Design | 前端界面设计 | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) |
| telegram-notifier | 任务完成时发送 Telegram 提醒 | [自定义 Skill](skill/telegram-notifier/README-zh.md) |
