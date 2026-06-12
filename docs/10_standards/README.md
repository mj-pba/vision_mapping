# Technical Standards — PBA Vision Mapping

> **Start here** if you are new to the project's coding and workflow conventions.

This folder contains all team-wide coding, workflow, and process standards for the PBA Vision Mapping project. These standards are adapted from industry-standard SOPs to ensure traceability, consistency, and smooth knowledge handover.

---

## Standards Index

| ID | Title | Covers | Status |
|----|-------|--------|--------|
| **TS-001** | [Coding Standards](TS-001_Coding-Standards.md) | Python naming, functions, error handling, PySide6 rules, testing, docstrings | Active |
| **TS-002** | [Git Workflow](TS-002_Git-Workflow.md) | Branches, commits, PRs, GitHub Issues, sprint board, release process | Active |
| **TS-003** | [Definition of Done](TS-003_Definition-of-Done.md) | DoD checklist for code tasks, hardware tasks, and documentation | Active |

---

## Reading Order — New Team Members

| # | Document | What You'll Learn | Time |
|---|----------|-------------------|------|
| 1 | [AGENTS.md](../../AGENTS.md) | Project overview, architecture, structure, and current status | 15 min |
| 2 | [TS-001 Coding Standards](TS-001_Coding-Standards.md) | How to write code that meets project standards | 20 min |
| 3 | [TS-002 Git Workflow](TS-002_Git-Workflow.md) | Branch naming, commit messages, PR process | 15 min |
| 4 | [TS-003 Definition of Done](TS-003_Definition-of-Done.md) | What "done" means for code and hardware tasks | 10 min |
| 5 | [Git Issues](../11_git_issues/README.md) | How work is tracked via GitHub Issues | 10 min |

---

## Quick Reference — Which Document Answers Which Question?

| Question | Go To |
|----------|-------|
| "What are we building?" | [AGENTS.md](../../AGENTS.md) |
| "How do I name my branch?" | [TS-002 Git Workflow](TS-002_Git-Workflow.md) §1 |
| "How do I format my commit message?" | [TS-002 Git Workflow](TS-002_Git-Workflow.md) §2 |
| "How do I write a Python docstring?" | [TS-001 Coding Standards](TS-001_Coding-Standards.md) §3.3 |
| "How do I open a PR?" | [TS-002 Git Workflow](TS-002_Git-Workflow.md) §4 |
| "How do I create a GitHub Issue?" | [TS-002 Git Workflow](TS-002_Git-Workflow.md) §5 |
| "What is the Definition of Done?" | [TS-003 Definition of Done](TS-003_Definition-of-Done.md) |
| "How do I track my work?" | [Git Issues README](../11_git_issues/README.md) |

---

## Documentation Principles

- **Keep it current** — update docs in the same PR that changes the code
- **Use Mermaid** for diagrams — it renders on GitHub and is version-controlled
- **Link, don't duplicate** — reference other documents instead of copying content
- **Date everything** — include `Last Updated` in metadata headers

---

## Change Log

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-04-14 | Malith | Initial version — adapted from docs_SOP reference standards |
