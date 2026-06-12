# Definition of Done

---
**Document ID:** TS-003
**Title:** Definition of Done — PBA Vision Mapping
**Version:** 1.0
**Status:** Active
**Owner:** Project Lead
**Last Updated:** 2026-04-14
**Review Due:** 2026-07-14
**Approved By:** Project Lead
---

# TS-003 — Definition of Done

> A work item is **Done** only when ALL applicable criteria below are met. This applies to all features, tasks, research items, and hardware tasks.

---

## 1. Code Tasks (Features, Bug Fixes, Refactors)

A code-related work item is **Done** when:

### 1.1 Code Quality
- [ ] All code is committed and pushed (no uncommitted local changes)
- [ ] Code follows [TS-001 Coding Standards](TS-001_Coding-Standards.md)
- [ ] Linter passes (`ruff check .`)
- [ ] Formatter passes (`black .`)
- [ ] No hardcoded credentials, paths, or secrets
- [ ] No commented-out code blocks
- [ ] No `print()` debugging statements in production code

### 1.2 Testing
- [ ] Unit tests written and passing (`pytest tests/`)
- [ ] Test coverage maintained at ≥ 80% for modified files
- [ ] Edge cases tested (empty input, boundary values, error paths)
- [ ] Tests are independent — no test relies on state from another

### 1.3 Documentation
- [ ] Google-style docstrings on all new/modified public functions
- [ ] `AGENTS.md` updated if project structure or status changed
- [ ] `docs/8_context_cohesion/as_built_updates.md` updated with implementation details
- [ ] `docs/8_context_cohesion/CHANGELOG.md` updated

### 1.4 Review & Merge
- [ ] PR opened against `develop` with [PR template](TS-002_Git-Workflow.md#pr-template) filled in
- [ ] Code reviewed (peer review or self-review with checklist)
- [ ] All `issue` and `question` review comments resolved
- [ ] PR merged into `develop`
- [ ] Feature branch deleted after merge

### 1.5 Issue Tracking
- [ ] GitHub Issue updated with completion status
- [ ] Local issue mirror file updated (in `docs/11_git_issues/`)
- [ ] Acceptance criteria verified and checked off

---

## 2. Research Tasks (Experiments, Calibration Studies)

A research task is **Done** when:

### 2.1 Investigation
- [ ] Research question answered (or documented as inconclusive with reasons)
- [ ] Approach and methodology documented
- [ ] Results are reproducible

### 2.2 Documentation
- [ ] Findings documented in the issue file or a dedicated report
- [ ] Data files (CSV, images) saved to `logs/` or appropriate directory
- [ ] Key metrics and measurements recorded with units
- [ ] Environmental conditions noted (temperature, humidity, cleanroom status)

### 2.3 Decision
- [ ] Clear recommendation or next steps documented
- [ ] If the research leads to new features/tasks, GitHub Issues created
- [ ] `as_built_updates.md` updated if findings affect system understanding

---

## 3. Hardware Tasks (Equipment Setup, Physical Tests)

A hardware task is **Done** when:

### 3.1 Physical Work
- [ ] Hardware task completed per procedure
- [ ] Equipment functioning correctly after modification
- [ ] Safety precautions followed

### 3.2 Verification
- [ ] Acceptance criteria verified with measurements
- [ ] Test results documented using the Hardware Test Report format:

```markdown
## Hardware Test Report
- **Date:** YYYY-MM-DD
- **Equipment:** [gantry, camera model, lens, glass scale]
- **Environment:** [temperature ±X°C, cleanroom Y/N, humidity]
- **Procedure:** [step-by-step what was done]
- **Results:** [measurements, CSV file paths]
- **Pass/Fail:** [against acceptance criteria]
- **Photos:** [reference to captured images]
- **Notes:** [observations, anomalies, follow-up needed]
```

### 3.3 Documentation
- [ ] Test results saved to `logs/` or documented in issue
- [ ] Photos or screenshots captured (if applicable)
- [ ] `as_built_updates.md` updated with hardware changes
- [ ] `AGENTS.md` updated if hardware status changed

### 3.4 Issue Tracking
- [ ] GitHub Issue updated with results and status
- [ ] Local issue mirror file updated

---

## 4. Documentation Tasks

A documentation task is **Done** when:

- [ ] Document created or updated following project standards
- [ ] All internal links verified and working
- [ ] Mermaid diagrams render correctly on GitHub
- [ ] Table of contents updated (if document has one)
- [ ] Committed and pushed via PR
- [ ] GitHub Issue updated

---

## 5. DoD Quick Reference Card

```
FOR EVERY WORK ITEM:
  □ Acceptance criteria met
  □ GitHub Issue updated
  □ Local issue file updated
  □ as_built_updates.md entry added (if applicable)
  □ CHANGELOG.md updated

ADDITIONAL FOR CODE:
  □ Tests written and passing
  □ Linter + formatter pass
  □ Docstrings added
  □ PR merged

ADDITIONAL FOR HARDWARE:
  □ Test report documented
  □ Measurements with units recorded
  □ Environmental conditions noted

ADDITIONAL FOR RESEARCH:
  □ Findings documented
  □ Recommendation or next steps stated
  □ Data files archived
```

---

## Change Log

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-04-14 | Malith | Initial version — adapted from docs_SOP; added hardware and research DoD sections specific to PBA Vision Mapping |
