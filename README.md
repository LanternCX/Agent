# 我的 Agent 相关文件备份

不完全复制粘贴，只做别人没做过的事情

## Prompt

提示词模版

| 名称 | 用途 | 本地文件 |
| --- | --- | --- |
| init-project-prompt | 通过可配置的初始化约束新建一个新项目 | `prompt/init-project.md` |
| paper-prompt | 期末周帮我写论文用的 | `prompt/peper.md` |

## Skill

自己写的一些 Skill

尽量贴近渐进式披露的思想，Skill 都尽力防止了上下文腐化

| 名称 | 用途 | 本地文件 |
| --- | --- | --- |
| using-memory | 使用 memory 系统 | `skill/using-memory/SKILL.md` |
| record-memory | 构建与维护 memory 系统 | `skill/record-memory/SKILL.md` |
| using-opencode | 教 opencode 怎么使用自己 | `skill/using-opencode/SKILL.md` |
| telegram-notifier | 在需要我回来确认、查看或收尾时发 Telegram 提醒 | `skill/telegram-notifier/SKILL.md` |

## Commands

自己写的一些命令

虽然说其实更具备兼容性的方式是用 Skill 实现，因为实际上 Command 和 Skill 没有本质区别

但是 Command 作为一个手动触发的更短的 Skill 在有些场景挺好用的

| 名称 | 用途 | 本地文件 |
| --- | --- | --- |
| `/remind` | 主动告诉 Agent 我要离开，让他通过 TG 叫我 | `commands/remind.md` |

## Rules

项目以及全局的一般规则

| 名称 | 用途 | 本地文件 |
| --- | --- | --- |
| AGENT.md | 搜集 + 自己迭代来的好用规则 | `rules/AGENT.md` |

## 文章

设计与最佳实践有关文章

转换为了 Markdown 格式方便 Agent 阅读，有些做了翻译，剩下什么都没改。

| 名称 | 简介 | 原文链接 | 本地文件 |
| --- | --- | --- | --- |
| 提示词最佳实践 | Claude 提示词编写与代理式系统实践整理 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | `artical/anthropic-prompt-best-practice-zh.md` |
| 你不知道的 Claude Code：架构、治理与工程实践 | Claude Code 的使用经验与工程实践整理 | https://x.com/HiTw93/status/2032091246588518683 | `artical/you-dont-know-claude-zh.md` |
| 5 Agent Skill design patterns every ADK developer should know | Google Cloud Tech 分享的 5 种 Skill 设计模式 | https://x.com/GoogleCloudTech/status/2033953579824758855 | `artical/5-skill-design-patterns.md` |
| 构建 Claude Code 的经验：我们如何使用 Skills【译】 | 关于 Claude Code 中 Skills 用法的译文整理 | https://x.com/dotey/status/2034002188994060691 | `artical/how-anthorpic-use-skill.md` |
| 你不知道的 Agent：原理、架构与工程实践 | Agent 原理、架构和实践经验整理 | https://x.com/HiTw93/status/2034627967926825175 | `artical/you-dont-know-agent.md` |
