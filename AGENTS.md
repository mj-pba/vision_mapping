# PBA Vision Mapping — Agent Context

> **Read this file first.** It gives AI coding agents and new developers a rapid orientation to the entire project.

## 1. Project Identity

**PBA Vision Mapping** is a desktop application for high-precision 2D geometric error mapping of 3-axis motion systems. It uses an onboard camera to scan a certified master glass dot-grid, detects dot positions with sub-pixel accuracy, calculates positional errors across the XY plane, and generates compensation maps that can be fed back into the ACS motor controller.

**Domain:** Precision metrology / machine calibration for advanced manufacturing.
**Company:** PBA Vision Systems (Singapore).
**Repository:** `https://github.com/malithjkd/pba_vision_mapping`

## 2. Technology Stack

| Layer | Technology |
|:---|:---|
| Language | Python 3.13 |
| GUI | PySide6 (Qt for Python) |
| Vision — detection | MVTec HALCON (sub-pixel XLD contour detection) |
| Vision — processing | OpenCV, NumPy, SciPy, Pandas |
| Motor control | ACS SPiiPlus Python library (TCP/IP) |
| Cameras | Dahua A5501M (USB3, via MVSDK) and FLIR (via PySpin) |
| Reference | 500×500 mm certified master glass scale (5 mm pitch, solid + annulus dots) |

## 3. Project Structure

```
pba_vision_mapping/
├── AGENTS.md              ← You are here
├── README.md              ← Project intro, setup summary, structure diagram
├── requirements.txt       ← Python dependencies
├── src/
│   ├── main.py            ← Application entry point
│   ├── frontend/          ← PySide6 UI (.ui + generated .py)
│   └── backend/
│       ├── controllers/   ← UI logic controllers (axis_x/y/z, main controller)
│       ├── image_processing/
│       │   ├── scan_and_capture.py         ← Core scanning workflow
│       │   ├── calculate_position_error.py ← Error calculation
│       │   ├── calculation_using_halcon.py ← Halcon-based detection
│       │   └── dahua_cam_api/              ← Camera SDK bindings
│       ├── motor_control/
│       │   └── acs_python_modules.py       ← ACS SPiiPlus integration
│       └── services/
│           ├── generate_2D_glass_certificate_62207.py  ← Glass certificate generation
│           ├── generate_2D_encoder_error_matrix.py     ← Error matrix generation
│           ├── generate_2D_error_mapping_test.py       ← Error correction testing
│           └── generate_2D_error_mapping_test_plot.py  ← Error map visualization
├── tests/
│   ├── backend_tests/     ← Unit + integration tests
│   └── frontend_tests/    ← UI tests
├── docs/                  ← Comprehensive project documentation
│   ├── 10_standards/      ← Coding standards, git workflow, DoD (TS-001–TS-003)
│   └── 11_git_issues/     ← Local mirror of GitHub Issues for tracking
├── assets/                ← Images, logos, hardware drivers
├── logs/                  ← Runtime output (CSV logs)
└── hardware/              ← Hardware-related files
```

## 4. Current Phase & Status

| Attribute | Value |
|:---|:---|
| **Current Phase** | Phase 1: Static Mapping |
| **Phase Goal** | Achieve precise 2D geometric error mapping across the XY plane |
| **Hardware** | 500×500 mm certified master glass scale acquired and in use |
| **Key Challenge** | Accurate 1-pixel-to-mm distance calibration |
| **Environment** | Not yet thermally controlled; sub-micron accuracy expected under temp tolerances |
| **Developer** | Single full-time developer |

### Completed Features (Phase 1)
- ✅ `FEAT-001`: Dot grid scanning (`scan_method_5()`) with UI integration
- ✅ `FEAT-002`: Glass scale certificate generation (backend done)
- ✅ `FEAT-003`: Encoder error matrix generation (backend done)
- ✅ `FEAT-004`: Error correction system testing & controller file generation
- ✅ `FEAT-005`: Error map visualization (X and Y plots)
- ✅ `FEAT-006`: Y-directional data refactoring for plotting

### In-Progress Work
- 🔄 `FEAT-007` / `ITB-TASK-008`: Integrate all backend features into PySide6 UI
- 🔄 `ITB-TASK-009`: Implement progress/status feedback in UI
- 🔄 Hardware: 4X telecentric lens mounting and pixel-to-mm calibration in cleanroom

### Future Phases
- **Phase 2:** Dynamic thermal mapping — correlate temperature with positional drift ($E = f(x, y, T)$)
- **Phase 3:** Active compensation — real-time closed-loop error correction via ACS servo loop

## 5. Key Entry Points

| Action | Command / File |
|:---|:---|
| Run the application | `python src/main.py` |
| Run tests | `pytest tests/` |
| Install dependencies | `pip install -r requirements.txt` |
| Setup guide | [CONTRIBUTING.md](docs/0_overview/CONTRIBUTING.md) |

## 6. Architecture Summary

The system follows a **4-layer architecture**:

1. **Presentation Layer** — PySide6 GUI (`src/frontend/`)
2. **Application Layer** — Controller classes that coordinate UI events with business logic (`src/backend/controllers/`)
3. **Domain Layer** — Core algorithms for scanning, image processing, error calculation, and motor control (`src/backend/image_processing/`, `src/backend/motor_control/`, `src/backend/services/`)
4. **Infrastructure Layer** — Camera SDK bindings, file I/O, hardware communication (`src/backend/image_processing/dahua_cam_api/`)

**Data flow:** GUI → Controller → Scan & Capture → Image Processing (Halcon/OpenCV) → Error Calculation → CSV output → ACS Controller upload.

Full architecture: [docs/2_architecture/architecture.md](docs/2_architecture/architecture.md)

## 7. Documentation Map

All documentation lives in `docs/` with a central navigation hub at [docs/links.md](docs/links.md).

| Section | Path | Contains |
|:---|:---|:---|
| Overview | `docs/0_overview/` | Project context, setup, stakeholders, contributing guide |
| Requirements | `docs/1_requirements/` | Features, user stories, NFRs, backlog |
| Architecture | `docs/2_architecture/` | System components, tech stack, architectural decisions |
| Design | `docs/3_design/` | UI components, flows, integration points |
| Technical Design | `docs/4_technical_design/` | Algorithms, data models, data flows, component designs |
| Implementation Plan | `docs/5_implementation_plan/` | Task backlog, dependency map, phased plan |
| Testing | `docs/6_testing/` | Test plan, test strategy, test cases |
| Context Cohesion | `docs/8_context_cohesion/` | As-built updates, changelog |
| AI Agent Blueprints | `docs/9_ai_agent_blueprints/` | Agent-driven development methodology |
| **Standards** | `docs/10_standards/` | Coding standards (TS-001), git workflow (TS-002), DoD (TS-003) |
| **Git Issues** | `docs/11_git_issues/` | Local mirror of GitHub Issues — work item tracking |

## 8. Conventions

- **Coding standards:** Follow [TS-001 Coding Standards](docs/10_standards/TS-001_Coding-Standards.md) — PEP 8, type hints, Google-style docstrings
- **Git workflow:** Follow [TS-002 Git Workflow](docs/10_standards/TS-002_Git-Workflow.md) — conventional commits, branch naming, PR process
- **Definition of Done:** Follow [TS-003 Definition of Done](docs/10_standards/TS-003_Definition-of-Done.md) — applies to code, hardware, and research tasks
- **Log output directory:** All CSV logs go to `logs/` (not the project root)
- **UI files:** Edit `src/frontend/main_window.ui` in Qt Designer, then compile:
  ```powershell
  pyside6-uic src/frontend/main_window.ui -o src/frontend/main_window_ui.py
  ```
- **Branch strategy:** `main` ← `develop` ← `feature/#NNN-description` (see TS-002)
- **Commit messages:** Conventional Commits format — `feat(scope): description` (see TS-002 §2)
- **Issue tracking:** All work items tracked as GitHub Issues with local mirror in `docs/11_git_issues/`
- **Documentation updates:** After completing a feature, update:
  1. `AGENTS.md` (status)
  2. `docs/11_git_issues/` (issue file status)
  3. `docs/8_context_cohesion/as_built_updates.md` (implementation details)
  4. `docs/8_context_cohesion/CHANGELOG.md` (changelog entry)

## 9. SOP & Issue Tracking

This project follows industry-standard operating procedures adapted from established software engineering practices. This ensures traceability, consistency, and smooth handover to a professional development team.

| What | Where | Purpose |
|:---|:---|:---|
| Coding standards | [TS-001](docs/10_standards/TS-001_Coding-Standards.md) | Python style, naming, error handling, testing |
| Git workflow | [TS-002](docs/10_standards/TS-002_Git-Workflow.md) | Branches, commits, PRs, issue templates |
| Definition of Done | [TS-003](docs/10_standards/TS-003_Definition-of-Done.md) | What "done" means for code, hardware, and research |
| Issue tracking | [Git Issues](docs/11_git_issues/README.md) | All work items with traceability to requirements |
| Issue types | `EPIC`, `FEAT`, `TASK`, `BUG`, `DOCS`, `RESEARCH`, `HW` | Categorised work items |

**For new team members:** Start with [docs/10_standards/README.md](docs/10_standards/README.md) for the reading order.
