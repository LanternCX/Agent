# Installation

Follow these steps to install the user's global Codex harness.

## Preparation

1. Check that Codex, Git, Node.js, and npm are available. Install missing prerequisites using their official instructions and reuse existing package managers. Node.js must be accessible from a non-interactive shell so Ponytail hooks can run.
2. Check existing skills, the Ponytail plugin, and global rules. Reuse correctly installed components. Back up files before replacing them, preserve user customizations, and ask the user to resolve conflicts that cannot be merged automatically.
3. Read the upstream installation instructions linked below. Follow the current upstream documentation if commands differ, and install at user scope.

The user's request to follow this guide authorizes installing the default tools and components below. Proceed without asking for confirmation for each package, while respecting the host's permission requirements. Pause only for required user interaction, such as login, system permissions, or unresolved configuration conflicts. Reuse working installations without proactively upgrading or replacing them.

## Default tools

Check each tool before installing it. Install missing tools using the linked upstream instructions and the user's existing package manager. Keep tool dependencies outside project environments.

| Tool | Purpose | Installation |
| --- | --- | --- |
| GitHub CLI (`gh`) | GitHub repositories, issues, pull requests, and Actions | Follow the [official installation instructions](https://github.com/cli/cli#installation). |
| uv | Run Python scripts and manage Python versions and isolated tools | Follow the [official installation instructions](https://docs.astral.sh/uv/getting-started/installation/). Let uv reuse a compatible Python or download one when needed; do not replace system Python. |
| Agent Browser | Browser interaction and frontend debugging | Follow the [upstream installation instructions](https://github.com/vercel-labs/agent-browser#installation). Ensure a supported browser is available; run `agent-browser install` if the required browser is missing. |
| MarkItDown | Extract document content as Markdown | Use uv to install the common document converters described below. |

For a missing MarkItDown installation, run:

```sh
uv tool install 'markitdown[pdf,docx,pptx,xlsx,xls]'
```

These extras cover common PDF and Office documents. Follow [MarkItDown's optional dependency documentation](https://github.com/microsoft/markitdown#optional-dependencies) for additional formats when needed. If an existing installation lacks a required converter, add the missing extras while preserving its version and existing extras.

Ensure commands are accessible from the shell the agent actually uses. If a uv-installed tool is missing from PATH, follow the [uv tool executable instructions](https://docs.astral.sh/uv/guides/tools/#installing-tool-executables), refresh the current shell environment, and check again before reinstalling it.

Check GitHub authentication with `gh auth status`. Reuse valid authentication; otherwise, guide the user through `gh auth login`. Continue independent installation steps while user interaction is pending, and report authentication separately from installation status.

## Matt Skills

Follow the [Matt Skills installation instructions](https://github.com/mattpocock/skills#installation-30-second-setup). Use the recommended Skills installer to install all available skills globally for Codex:

```sh
npx skills@latest add mattpocock/skills --global --agent codex --skill '*' --yes
```

Preserve the upstream directory structure and supporting files. This procedure installs global components only; do not run project initialization.

## Ponytail

Follow the [Ponytail installation instructions for Codex](https://github.com/DietrichGebert/ponytail#codex) to install the complete plugin:

```sh
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

Reuse an existing marketplace or an already enabled plugin. Keep the bundled skills and hooks, and use the default `full` mode. Guide the user to review and trust the Ponytail hooks through `/hooks` in Codex, then start a new thread. Desktop app users should restart the app.

## Frontend Design (optional)

Install this skill only when the user requests it. Otherwise, skip this section and leave any existing installation untouched.

Get the complete `skills/frontend-design` directory from [Anthropic's official repository](https://github.com/anthropics/skills/tree/main/skills/frontend-design). Preserve its supporting files and license files, and install it at:

```text
~/.agents/skills/frontend-design/
```

Use this as the shared installation location for the standalone skill. Reuse an existing complete installation. If another agent needs an entry in its own skills directory, link to this copy instead of maintaining duplicates. Do not put installation files in the current project repository.

## Personal rules

Clone [LanternCX/Agent](https://github.com/LanternCX/Agent) into a permanent location chosen for the user, or reuse an existing local checkout.

Link the repository's [rules/AGENTS.md](rules/AGENTS.md) to Codex's global rules file: `~/.codex/AGENTS.md` by default, or `AGENTS.md` under `CODEX_HOME` when that variable is set. Use the actual checkout path without hardcoding a username.

If the destination already points to the same file, leave it as is. If it contains other personal rules, back them up and preserve them, referencing this repository's rules from the local rules file. Do not write the user's additional rules into the repository. Ask the user to resolve conflicting rules.

## Verification

- Check that Git, Node.js, npm, `gh`, `uv`, `agent-browser`, and `markitdown` run from the agent's shell. Verify Python execution with `uv run --no-project python -c "print('ok')"` outside project environments.
- Verify Agent Browser in a separate test session using a local test page: open it, read a snapshot, take a screenshot, and close only that test session. Do not reuse or close the user's browser sessions.
- Verify MarkItDown with a small generated document, such as a DOCX containing known text, and check that the Markdown output includes that text. Also check that the PDF and Office converter dependencies are installed. Use a temporary directory outside the repository for test files and remove them afterward.
- Check that Matt Skills are installed globally, including `setup-matt-pocock-skills`, with their supporting files intact.
- If Frontend Design was selected, check that `~/.agents/skills/frontend-design/SKILL.md` is readable and related symlinks resolve.
- Use `codex plugin list` to check that `ponytail@ponytail` is installed and enabled, and confirm that Node.js is available to its hooks.
- Check that the global rules file provides access to the repository's rules.
- Remind the user to start a new thread and confirm that Codex discovers the skills and displays Ponytail's activation message.

Finish with a brief report of the tools and components installed or reused, verification results, and any login, hook approval, or restart steps the user still needs to complete. Explicitly state any capability or activation status that has not been verified.
