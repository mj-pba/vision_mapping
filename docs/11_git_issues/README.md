# Git Issues — Local Mirror

This folder is a **local mirror** of GitHub Issues for the PBA Vision Mapping project. It provides offline reference, allows coding agents and developers to understand current tasks, and maintains a traceable link between requirements and work items.

---

## Naming Convention

```
[TYPE]-NNN_#GH_Short-Title.md
```

| Part | Description | Example |
|------|-------------|---------|
| `TYPE` | Issue type prefix (see below) | `FEAT`, `TASK`, `HW`, `RESEARCH` |
| `NNN` | Sequential number per type (you assign) | `001`, `002`, `003` |
| `#GH` | GitHub issue number (auto-assigned by GitHub) | `#1`, `#5`, `#12` |
| `Short-Title` | Hyphenated short title (3–6 words) | `Glass-Certificate-1D`, `Telecentric-Lens-Mount` |

### Issue Type Prefixes

| Prefix | Type | GitHub Label | Description |
|--------|------|-------------|-------------|
| `EPIC` | Epic | `type: epic` | A large body of work grouping multiple issues |
| `FEAT` | Feature | `type: feature` | A new feature or capability |
| `BUG` | Bug Report | `type: bug` | Something is broken or incorrect |
| `TASK` | Technical Task | `type: tech-debt` | Infrastructure, setup, or development work |
| `DOCS` | Documentation | `type: docs` | Documentation creation or update |
| `RESEARCH` | Research | `type: research` | Investigation, calibration, or experimentation |
| `HW` | Hardware | `type: hardware` | Physical equipment setup, mounting, testing |

### Examples

```
EPIC-001_#NN_Phase-1-Static-Mapping.md
FEAT-001_#NN_Dot-Grid-Scanning.md
RESEARCH-001_#58_1D-Glass-Certificate-Verification.md
HW-001_#NN_4X-Telecentric-Lens-Mount.md
TASK-001_#NN_UI-Progress-Feedback.md
DOCS-001_#57_SOP-Adoption.md
```

---

## Issue Template

Every issue file must follow this structure:

```markdown
---
GitHub Issue: #[number]
Type: [Epic / Feature / Bug / Task / Docs / Research / Hardware]
Priority: [Critical / High / Medium / Low]
Status: [Open / In Progress / In Review / Closed]
Assignee: [Name or TBD]
Sprint: [Sprint N or Backlog]
Labels: [comma-separated GitHub labels]
Created: [YYYY-MM-DD]
Requirement Refs: [REQ-XX, FEAT-XX]
---

# [TYPE-NNN] Title

## Description
[Context and description]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Tasks
- [ ] Task 1
- [ ] Task 2

## Definition of Done
- [ ] Code reviewed and approved
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Hardware test documented (if applicable)

## Notes
[Any additional context, links, diagrams]
```

---

## Issue Index

### Epics

| File | Type | GH # | Title | Status |
|------|------|------|-------|--------|
| [EPIC-001](EPIC-001_%23NN_Phase-1-Static-Mapping.md) | Epic | #NN | Phase 1: Static 2D Error Mapping | 🔄 In Progress |

### Completed Features (Phase 1)

| File | Type | GH # | Title | Status | Req Refs |
|------|------|------|-------|--------|----------|
| [FEAT-001](FEAT-001_%23NN_Dot-Grid-Scanning.md) | Feature | #NN | Dot Grid Scanning | ✅ Closed | REQ-001 |
| [FEAT-002](FEAT-002_%23NN_Glass-Certificate-2D.md) | Feature | #NN | 2D Glass Certificate Generation | ✅ Closed | REQ-002 |
| [FEAT-003](FEAT-003_%23NN_Encoder-Error-Matrix.md) | Feature | #NN | Encoder Error Matrix Generation | ✅ Closed | REQ-003 |
| [FEAT-004](FEAT-004_%23NN_Error-Correction-Test.md) | Feature | #NN | Error Correction Test & Controller File Gen | ✅ Closed | REQ-004 |
| [FEAT-005](FEAT-005_%23NN_Error-Map-Visualization.md) | Feature | #NN | Error Map Visualization | ✅ Closed | REQ-005 |
| [FEAT-006](FEAT-006_%23NN_Y-Data-Refactoring.md) | Feature | #NN | Y-Data Refactoring for Plotting | ✅ Closed | REQ-006 |

### Completed Hardware

| File | Type | GH # | Title | Status | Req Refs |
|------|------|------|-------|--------|----------|
| [HW-003](HW-003_%23NN_0.35X-Telecentric-Lens-Setup.md) | Hardware | #NN | 0.35X Telecentric Lens Setup | ✅ Closed | RESEARCH-001 |

### Active Work Items

| File | Type | GH # | Title | Status | Req Refs |
|------|------|------|-------|--------|----------|
| [FEAT-007](FEAT-007_%23NN_UI-Integration.md) | Feature | #NN | UI Integration for All Backend Features | 🔵 Open | REQ-007 |
| [FEAT-010](FEAT-010_%2356_Certificate-500mm-150mm-Glass-Scale.md) | Feature | #56 | Certificate Generation for 500mm & 150mm Glass Scale | 🔵 Open | REQ-002 |
| [TASK-001](TASK-001_%23NN_UI-Progress-Feedback.md) | Task | #NN | UI Progress/Status Feedback | 🔵 Open | REQ-007.6 |
| [TASK-004](TASK-004_%2349_Demo-Room-Gantry-Deployment.md) | Task | #49 | Deployment Test: Demo Room Gantry | 🔵 Open | — |
| [RESEARCH-001](RESEARCH-001_%2358_1D-Glass-Certificate-Verification.md) | Research | #58 | 1D Glass Certificate Verification | 🔄 In Progress | REQ-002 |
| [RESEARCH-002](RESEARCH-002_%23NN_Pixel-to-mm-Calibration.md) | Research | #NN | Pixel-to-mm Calibration (Both Lenses) | 🔵 Open | NFR-ACCU-001 |
| [RESEARCH-003](RESEARCH-003_%23NN_Temperature-Dependent-Calibration.md) | Research | #NN | Temperature-Dependent Calibration | 🔵 Open | NFR-ACCU-001 |
| [RESEARCH-004](RESEARCH-004_%2354_Vision-Motion-Distance-Capability.md) | Research | #54 | Vision-Based Motion Distance Capability | 🔵 Open | NFR-ACCU-001 |
| [HW-001](HW-001_%23NN_4X-Telecentric-Lens-Mount.md) | Hardware | #NN | 4X Telecentric Lens Mount | 🔵 Open | — |
| [HW-002](HW-002_%23NN_Vision-Jitter-Analysis.md) | Hardware | #NN | Vision Jitter Analysis (Both Lenses) | 🔵 Open | — |
| [TASK-002](TASK-002_%23NN_Glass-Certificate-Repeatability.md) | Task | #NN | Glass Certificate Repeatability Verification | 🔵 Open | REQ-002.4 |
| [DOCS-001](DOCS-001_%2357_SOP-Adoption.md) | Docs | #57 | SOP Adoption & Git Issue Tracking | 🔄 In Progress | REQ-008 |
| [TASK-003](TASK-003_%23NN_Document-Test-Features.md) | Task | #NN | Document & Test All Implemented Features | 🔵 Open | All |
| [TASK-005](TASK-005_%2359_Externalize-Recipe-Data.md) | Task | #59 | Externalize Recipe Data — Move `src/recipes/` Outside Source Tree | 🔵 Open | — |
| [FEAT-011](FEAT-011_%2360_First-Run-Recipe-Initialization.md) | Feature | #60 | First-Run Recipe Data Initialization | 🔵 Open | TASK-005 |

### Future Enhancements (Backlog)

| File | Type | GH # | Title | Status | Req Refs |
|------|------|------|-------|--------|----------|
| [FEAT-008](FEAT-008_%2346_AI-Noise-Filter.md) | Feature | #46 | AI Noise Filter | 🔵 Open | — |
| [FEAT-009](FEAT-009_%2352_CUDA-Glass-Certificate-Optimization.md) | Feature | #52 | CUDA-Based Glass Certificate Optimization | 🔵 Open | FEAT-002 |

---

## How to Use

1. **Creating a new issue:** Create the issue on GitHub first → get the auto-assigned `#number` → update the local `.md` file with the correct `#number` → update the index table above
2. **Updating status:** When the GitHub issue status changes, update the `Status` field in the file header and in the index table above
3. **Linking to requirements:** Always add `Requirement Refs` in the header to trace back to `docs/1_requirements/backlog.md`
4. **For coding agents:** Read this folder to understand what tasks are active. Check the `Status` field to know what's in progress

---

## Hardware & Camera Notes

| Component | Status | Notes |
|-----------|--------|-------|
| **FLIR BFS-U3** | ✅ Active | Primary camera. API: `bfs_camara_api` (PySpin) |
| **0.35X Telecentric Lens** | ✅ Mounted | Glass certificate lens. FOV: ~10H × 7V dots |
| **4X Telecentric Lens** | ⏳ Pending | High-res error mapping lens. Pending HW-001 |
| **Dahua A5501M** | ⚠️ Legacy | Code in `dahua_cam_api/` retained but not in active use |

---

## Status Legend

| Icon | Status |
|------|--------|
| 🔵 | Open — not yet started |
| 🔄 | In Progress — actively being worked on |
| 🟡 | In Review — PR open or awaiting review |
| ✅ | Closed — completed and verified |
| ❌ | Blocked — cannot proceed |

---

## Change Log

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-04-14 | Malith | Initial version — created issue index with 16 issues covering Phase 1 features and active work |
| 1.1 | 2026-04-16 | Malith | Updated camera refs (Dahua → FLIR BFS-U3). Added RESEARCH-003, RESEARCH-004, HW-003, FEAT-008, FEAT-009, FEAT-010, TASK-004. Synced GitHub issue numbers (#46, #49, #52, #54, #56, #57, #58). Added hardware/camera notes table. Expanded RESEARCH-002 for dual-lens scope. |
