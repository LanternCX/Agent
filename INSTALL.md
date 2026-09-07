# 安装说明

为当前用户安装全局 Codex Harness：Matt Skills、个人规则及常用工具。

## 准备与授权

1. 只读检查 Codex、Git、Node.js、npm、现有 Skills、个人规则及下方工具的安装状态。Node.js 和 npm 用于安装 Matt Skills。
2. 阅读下方链接中的上游安装说明；命令有变化时以上游为准。复用可用的安装和包管理器，不主动升级或替换。
3. **写入前，向用户说明将安装的组件、安装位置、需修改或备份的文件，以及验证方式，取得该范围的批准。** 若用户已明确批准同一范围，不重复确认。
4. 批准后批量执行，不逐包询问。需要登录、系统权限、解决配置冲突，或扩大安装范围时，再请用户参与。

依赖安装在用户环境或隔离的工具环境中，不写入业务项目环境。替换已有个人配置前先备份并保留用户定制；无法合并的冲突交由用户决定。

## 默认工具

先检查，缺失时在批准的范围内安装。

| 工具 | 用途 | 安装方式 |
| --- | --- | --- |
| GitHub CLI（`gh`） | 操作 GitHub 仓库、Issue、PR 和 Actions | 按[官方说明](https://github.com/cli/cli#installation)，复用用户已有包管理器。 |
| uv | 运行 Python 脚本，管理 Python 版本和隔离工具 | 按[官方说明](https://docs.astral.sh/uv/getting-started/installation/)安装；复用兼容 Python，或由 uv 按需下载，不替换系统 Python。 |
| MarkItDown | 将常见文档的文字与结构提取为 Markdown | 通过 uv 安装下方常用格式支持。 |

### MarkItDown

缺失时安装：

```sh
uv tool install 'markitdown[pdf,docx,pptx,xlsx,xls]'
```

这些扩展覆盖常见 PDF 和 Office 文件。其他格式按[上游可选依赖说明](https://github.com/microsoft/markitdown#optional-dependencies)按需补充。已有安装缺少所需转换器时，保留版本及现有扩展，只补齐缺失部分。

图片、图表、扫描件或复杂版面提取不完整时，继续查看原件或使用适合的识别工具。

### 命令可用性与登录

确保命令能从 Agent 实际使用的 shell 调用。如果 uv 已安装工具但 PATH 中找不到命令，先按 [uv 工具路径说明](https://docs.astral.sh/uv/guides/tools/#installing-tool-executables)处理路径并刷新环境，不重复安装。

使用 `gh auth status` 检查 GitHub 登录状态。复用有效登录；需要时引导用户执行 `gh auth login`。等待用户登录时，可以继续其他已授权且不依赖登录的步骤。分别报告安装状态和登录状态。

## Matt Skills（必装）

按 [Matt Skills 上游说明](https://github.com/mattpocock/skills#installation-30-second-setup)，将整套 Skills 安装到 Codex 的用户级目录：

```sh
npx skills@latest add mattpocock/skills --global --agent codex --skill '*' --yes
```

保留完整目录结构和支持文件，不修改上游实现。此处只安装全局组件，不运行项目初始化。安装整套 Skills 不意味着每个任务都要执行完整工作流。

## Agent Browser（可选）

浏览器交互和前端调试优先使用当前 Agent 已具备且满足任务需要的浏览器能力。能力缺失、需要独立命令行自动化，或用户明确选择时，将 Agent Browser 纳入安装范围。

按[上游说明](https://github.com/vercel-labs/agent-browser#installation)安装，并检查兼容浏览器是否可用；缺失时，在已批准的范围内执行 `agent-browser install`。

未选择时跳过安装和验证，保留已有安装。

## Frontend Design（可选）

仅在用户明确选择时安装，否则保留已有安装。

从 [Anthropic 官方仓库](https://github.com/anthropics/skills/tree/main/skills/frontend-design)获取完整的 `skills/frontend-design` 目录，保留支持文件和许可证，安装到：

```text
~/.agents/skills/frontend-design/
```

复用完整的现有安装。其他 Agent 需要独立入口时，链接到这份共享副本，不维护重复内容。不将安装文件写入业务项目仓库。

## 个人规则

将 [LanternCX/Agent](https://github.com/LanternCX/Agent) 克隆到与用户确认的长期存放位置，或复用已有检出。

将仓库的 [rules/AGENTS.md](rules/AGENTS.md) 链接到 Codex 全局规则文件：默认是 `~/.codex/AGENTS.md`；设置了 `CODEX_HOME` 时，使用该目录下的 `AGENTS.md`。使用实际路径，不硬编码用户名。

- 目标已指向同一文件时，无须修改。
- 目标包含其他个人规则时，先备份并保留这些规则，在本地规则文件中引用本仓库规则。
- 不将用户额外规则写入本仓库；规则冲突交由用户决定。

## 验证

- 检查 Codex、Git、Node.js、npm、`gh`、`uv` 和 `markitdown` 能从 Agent 的 shell 调用。在项目环境外使用 `uv run --no-project python -c "print('ok')"` 验证 Python 执行。
- 使用含有已知文字的小型文档（如 DOCX）验证 MarkItDown，确认输出包含该文字，并检查 PDF 和 Office 转换器依赖。测试文件放在仓库外的临时目录，完成后清理。
- 选择 Agent Browser 时，用独立测试会话打开本地测试页面、读取快照并截图，最后只关闭该测试会话，不复用或关闭用户会话。
- 检查 Matt Skills 已完整安装，包括 `setup-matt-pocock-skills` 及其支持文件。
- 选择 Frontend Design 时，检查 `~/.agents/skills/frontend-design/SKILL.md` 可读且相关链接有效。
- 检查全局规则入口可读取本仓库规则。
- 提醒用户开启新会话，确认 Codex 能发现 Skills；未确认的加载状态如实报告。

最后简要报告安装或复用的组件、验证结果，以及仍需用户完成的登录或重启步骤。未验证的能力应明确标注。
