# Where commands run

This repo’s automation and repeatable work should **not** rely on ad-hoc “whatever `python` is on PATH” usage. Use **GitHub Actions** for production paths and **only** a **project virtualenv** when working locally.

## Rules

| Context | How to run |
|--------|------------|
| **Scheduled / production** (analytics, batch upload, weekly reports) | **[GitHub Actions](https://github.com/peterkrentel/living-ambient-engine/actions)** — workflows are the source of truth. Prefer `workflow_dispatch` to test a workflow after a change. |
| **Local development** | **Virtualenv only** — same as [README Quick Start](../README.md#quick-start): `python3 -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`), then `pip install -r requirements.txt`, then project commands. |
| **Avoid** | Running project scripts with **system/global Python** without the repo venv, or assuming others’ machines match your PATH. |

## For AI assistants and docs

- When suggesting shell commands for this repo, **assume venv is activated** or show activation in the same block.
- For integration checks that need secrets (YouTube, etc.), **do not** expect a successful local run without credentials; use **Actions** or document manual steps.

## Relationship to data

- **`data/*` commits** from [Analytics Agent (brand)](../.github/workflows/analytics-agent.yml) and [Analytics Agent (personal)](../.github/workflows/analytics-personal.yml) are produced **in CI**, not by ad-hoc local runs, unless you intentionally mirror that process inside a venv for debugging.

---

*Keeps environments reproducible and avoids “works on my machine” for automation.*
