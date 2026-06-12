# Task Backlog: PBA Vision Mapping

| Task ID | Priority | Est. Effort | Description | Status | Parent Item(s) | Acceptance Criteria (Derived/Referenced) | Task Description |
|:--- |:--- |:--- |:--- |:--- |:--- |:--- |:--- |
| ITB-TASK-001 | Critical | M | Implement dot grid scanning logic and logging           | Done | FEAT-001, US-001, ImageAcquisitionModule | AC1-AC5 (FEAT-001), AC1-AC2 (US-001) | |
| ITB-TASK-002 | High     | S | Develop UI for scan parameter input and scan initiation | Done | FEAT-001, US-001, MainWindow, UIController | AC1-AC2 (FEAT-001), AC1 (US-001) | |
| ITB-TASK-003 | Critical | M | Implement glass certificate generation logic            | Done | FEAT-002, US-002, GlassCertificateGenerationModule | AC1-AC4 (FEAT-002), AC1-AC2 (US-002) | |
| ITB-TASK-004 | Critical | M | Implement encoder error matrix generation               | Done | FEAT-003, US-003, EncoderErrorMatrixModule | AC1-AC6 (FEAT-003), AC1-AC2 (US-003) | |
| ITB-TASK-005 | High     | M | Implement error correction test and controller file generation | Done | FEAT-004, US-004, ErrorMappingTestUtilsModule | AC1-AC7 (FEAT-004), AC1-AC3 (US-004) | |
| ITB-TASK-006 | Medium   | S | Implement error map visualization (X and Y)             | Done | FEAT-005, US-005, ErrorMapPlottingModule | AC1-AC3 (FEAT-005), AC1-AC2 (US-005) | |
| ITB-TASK-007 | Medium   | S | Refactor Y-directional data handling for plotting       | Done | FEAT-006, US-006, ErrorMapPlottingModule | AC1-AC3 (FEAT-006), AC1-AC2 (US-006) | |
| ITB-TASK-008 | Critical | L | Integrate all backend features into the main UI         | To Do | FEAT-007, US-007, MainWindow, UIController | AC1-AC6 (FEAT-007), AC1-AC6 (US-007) | |
| ITB-TASK-009 | High     | S | Implement progress/status feedback in UI                | To Do | FEAT-001, FEAT-003, FEAT-007, MainWindow | AC5 (FEAT-001), AC6 (FEAT-003), AC6 (FEAT-007) | |
| ITB-TASK-010 | High     | M | Document and test all implemented features              | To Do | All | All feature/user story ACs | |

*Est. Effort: S=Small, M=Medium, L=Large. See `dependency_map.md` for dependencies.*

---

*Related Links:*
*   [Implementation Plan README](./README.md)
*   [Implementation Plan Links](./links.md)
*   [Main Project README](../../README.md)

## Action Items (To Do)

| S.No | Priority | Target | Action Item | Status | Remarks | Task Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | High | Wk38 | Request quotations and create part numbers for the 480 x 480 glass scale and the 1X/4X cameras. | Started | Need support from CC Lim | |
| 2 | High | Wk38 | Follow up on assembling NPD00566. | Yet to start | | Asanga and Pei Soon |
| 3 | High | Wk38 | Halcon software purchase for next year. | Started | | |
| 4 |Medium| Wk38 | Follow up on the design and PRQ mountings for the NPD00566-based vision capability test. | Done | | given all the requiments to Gilbert |
| 5 | Low  | Wk38 | Study circle radius calculation using sub pixels calculation. | Started | | |                                   
| 6 | Low  | Wk39 | Prepare software for 4X telecentric camera-based test. 2D error mapping, vision capability. | Yet to start | | |
| 6 | Low  | Wk39 | Get space from Andrew. | Yet to start | | |
| 7 | High | Wk40 | **Phase 1: Initial Hardware Setup & Testing** | Yet to start | | This task bundles the initial hardware and software preparations before moving to the cleanroom. |
| 8 | High | Wk40 | Mount 4X telecentric lens and perform basic functionality checks. | Yet to start | | **Depends on:** Hardware delivery (ITB-TASK-008). **Acceptance Criteria:** 1. Lens is securely mounted. 2. Camera acquires and saves images through the new lens via the software. |
| 9 | High | Wk40 | **Phase 2: High-Precision Calibration & Capability Analysis (In Cleanroom)** | Yet to start | | This phase covers the critical measurements to be performed in the temperature-stable environment. **Prerequisite:** Gantry moved to cleanroom. See [Test Plan](../6_testing/test_plan.md) |
| 10 | High | Wk40 | **Task A: Accurate Pixel-to-mm Calibration ([TST-003](../6_testing/test_plan.md#tst-003))** | Yet to start | | **Method:** Use image stitching and a laser interferometer to establish a precise, repeatable pixel-to-mm ratio. **Acceptance Criteria:** 1. A stable pixel-to-mm value is determined with a variation of less than 0.1% across multiple tests. 2. The methodology is documented. |
| 11 | High | Wk41 | **Task B: Vision Measurement & Jitter Analysis ([TST-001](../6_testing/test_plan.md#tst-001), [TST-002](../6_testing/test_plan.md#tst-002))** | Yet to start | | **Method:** Perform "In-position" and "multi-position" tests to quantify measurement repeatability. **Acceptance Criteria:** 1. The 3-sigma deviation of dot radius and center position is calculated and documented from at least 100 samples at a single location. 2. The analysis is repeated for at least 5 different grid locations to ensure consistency. |
| 12 | High | Wk41 | **Task C: Verify Glass Certificate Generation ([TST-004](../6_testing/test_plan.md#tst-004))** | Yet to start | | **Method:** Generate the glass certificate multiple times using the new stable setup. **Acceptance Criteria:** 1. At least 3 glass certificates are generated. 2. The variation between the generated certificates is analyzed and documented. The results should be consistent, proving the process is reliable. |
| 13 | Low | Wk41 | Conduct a thermal stability and expansion test for limited dots inside the clean room. | Yet to start | | This is now part of the prerequisite environmental validation for Phase 2. |
| 14 | Low | Wk41 | Generate the glass certificate using a laser-based reference measurement inside the clean room. | Yet to start | | This is covered by Task C. |
| 15 | Low | Wk41 | Create a 3D plot of multiple glass certificates and study the reasons for variations. | Yet to start | | This is an analysis step within Task C. |

## Completed Action Items

| S.No | Priority | Target | Action Item | Status | Remarks | Task Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | High | Wk31 | Generate glass scale certification. | Done | Use log file from scan; run certificate script. | |
| 2 | High | Wk31 | Verify distance using laser measurement. | Done | Ensure calibration accuracy. | |
| 3 | High | Wk31 | Create 2D error mapping values. | Done | Generate X and Y error maps. | |
| 4 | High | Wk31 | Send error values to ACS and re-run test with error mapping enabled. | Done | Validate correction effectiveness. | |
| 5 | High | Wk32 | Present the 2D error mapping report to CC Lim & Asanga and get the next steps. | Done | | |
| 6 | High | Wk32-33 | Measure Cleanroom temperature fluctuations. | Done | 90% done | |
| 7 | High | Wk32 | Follow-up and get the quotation for glass scale. | Done | Received three quotations. | |
| 8 | High | Wk34 | L1 R&D room temperature measurement. | Done | | |
| 9 | High | Wk34 | Follow up on purchase of large glass scale with certificate. | Done | | |
| 10 | High | Wk34 | Vision capability analysis. | Done | | |
| 11 | High | Wk35 | Prepare and send L1 R&D room temperature variation report. | Done | | |
| 12 | High | Wk35 | Follow up Glass scale purchase & provide info. | Done | | |
| 13 | High | Wk35 | New 4x telecentric lens image quality test. | Done | | |
| 14 | Medium | Wk36 | Generate plots for error mapping (X and Y axes). | Done | Visualize and compare before/after correction. | |
| 15 | High | Wk36 | Generate vision-based plots for 2D repeatability and accuracy measurement. | Done | | |
| 16 | High | Wk36 | Glass scale purchase following up. | Done | | |
| 17 | High | Wk37 | Glass scale purchase progress proposal. | Done | | |
| 18 | High | Wk37 | Identify errors in 2D error calculation - 3D plot. | Done | | |
| 19 | High | Wk37 | Prepare setup for remote operation gantry / lights / programming. | Done | | |
| 21 | Low | Wk38 | Study ML experiment tracking. | Done | | |
| 22 | Low | Wk38 | Finalize the 480 x 480 glass scale and 1X/4X camera specifications. | Done | | |
| 23 | High | Wk39 | Complete Dot Grid Scanning logic (FEAT-001) and integrate into `main_window_ui.py`. | Done | See `REQ-001` | |

