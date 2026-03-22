# README 资料索引 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将根目录 `README.md` 补全为一个可直接浏览的资料索引页, 按文章、Prompt、Skill、规范四类展示现有内容。

**Architecture:** 只修改 `README.md`, 保持仓库现有文件结构不变。先确认四类资料的实际条目与文章原文链接, 再按统一表格格式写入 README, 最后人工检查标题层级、说明语句和表格完整性。

**Tech Stack:** Markdown

---

### Task 1: 整理文章类条目与原文链接

**Files:**
- Modify: `README.md`
- Check: `artical/anthropic-prompt-best-practice-zh.md`
- Check: `artical/you-dont-know-claude-zh.md`
- Check: `artical/5-skill-design-patterns.md`
- Check: `artical/persuasion-principles.md`
- Check: `artical/anthropic-skill-best-practices.md`
- Check: `artical/how-anthorpic-use-skill.md`
- Check: `artical/you-dont-know-agent.md`

- [ ] **Step 1: 逐篇确认文章名称与简介**

从每篇文章开头提取标题, 为 README 准备一句简短说明。

- [ ] **Step 2: 逐篇确认原文链接**

优先使用文章正文已有的 `URL Source` 或显式原文链接；若未直接声明, 再结合正文线索补齐可用来源。只有全部文章都确认到原文链接后, 这一任务才算完成。

- [ ] **Step 3: 形成文章表格草稿**

在 README 中使用 `名称 | 简介 | 原文链接 | 本地文件` 四列。

### Task 2: 整理 Prompt、Skill 与规范条目

**Files:**
- Modify: `README.md`
- Check: `prompt/init-project.md`
- Check: `prompt/peper.md`
- Check: `skill/using-memory/SKILL.md`
- Check: `skill/record-memory/SKILL.md`
- Check: `skill/record-memory/bootstrap.md`
- Check: `skill/record-memory/template/type/base/ENTRY.md`
- Check: `skill/record-memory/template/type/base/INDEX.md`
- Check: `skill/record-memory/template/type/base/MEMORY.md`
- Check: `skill/record-memory/template/type/debug/ENTRY.md`
- Check: `skill/record-memory/template/type/debug/INDEX.md`
- Check: `skill/record-memory/template/type/debug/MEMORY.md`
- Check: `skill/record-memory/template/type/milestone/ENTRY.md`
- Check: `skill/record-memory/template/type/milestone/INDEX.md`
- Check: `skill/record-memory/template/type/milestone/MEMORY.md`
- Check: `skill/record-memory/template/type/refactor/ENTRY.md`
- Check: `skill/record-memory/template/type/refactor/INDEX.md`
- Check: `skill/record-memory/template/type/refactor/MEMORY.md`
- Check: `AGENT.md`

- [ ] **Step 1: 确认 Prompt 类条目与用途**

为 `prompt/` 下文件提炼一句用途说明。

- [ ] **Step 2: 确认 Skill 类条目与用途**

Skill 类收录范围以 `skill/` 目录下当前存在的全部资料文件为准。执行时需要基于这些实际文件整理出合适条目与一句用途说明, 避免遗漏现有内容。

- [ ] **Step 3: 确认规范类条目与用途**

将 `AGENT.md` 纳入规范分类, 提炼一句简要说明。

- [ ] **Step 4: 形成三类表格草稿**

在 README 中统一使用 `名称 | 用途 | 本地文件` 三列表格。

### Task 3: 写入 README 并检查格式

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 写入 README 顶部说明**

补上仓库用途简介, 作为索引页开场。

- [ ] **Step 2: 写入四个二级标题**

按 `文章 / Prompt / Skill / 规范` 顺序组织内容, 每类保留一句简要说明。

- [ ] **Step 3: 写入四个表格**

确保每个分类都按“二级标题 -> 1 句简要说明 -> 对应表格”的固定顺序写入, 且列名与内容保持一致。

- [ ] **Step 4: 自检格式要求**

确认共有 4 个二级标题, 每类都有一句说明和一个表格, 文章类每条都带原文链接。

- [ ] **Step 5: 读取 README 复核可读性**

检查整体是否清楚、简洁、便于后续追加内容。
