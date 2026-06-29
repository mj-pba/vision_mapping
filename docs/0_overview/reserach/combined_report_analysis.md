# Combined Analysis: Two R&D Reports on 2D Vision-Based Calibration

## Document Overview

| Attribute | Report 1 (Lines 1–707) | Report 2 (Lines 712–869) |
|:---|:---|:---|
| **Title** | *PBA Systems — R&D Literature Review & Technical Report* | *R&D Technical Report: 2D Vision-Based Volumetric Calibration...* |
| **Depth** | ~700 lines, highly detailed with full mathematical derivations | ~160 lines, concise executive-summary style |
| **Equation detail** | Full HTM matrices, Abbe derivations, Fourier SDE model, Cramér-Rao bound, GPR posterior, PINN loss, LuGre/Dahl models | Condensed HTM formulation, compact planar deviation equations |
| **References** | 8 papers cited (Table 4), but **incomplete bibliographic data** (missing DOIs, years, first authors for several entries) | 4 verified references with **complete DOIs, authors, journals, and years** |
| **IP/Publication** | Full section with 3 journal targets, 3 novelty claims, IP strategy, detailed paper outline | Briefer publication section with 3 journal targets, structural outline |

---

## 1. Points of Agreement (Consensus)

The two reports converge on the following key positions. These represent a **strong consensus foundation** for the scientific paper.

### ✅ 1.1 Kinematic Error Framework

| Topic | Report 1 | Report 2 | Consensus Strength |
|:---|:---|:---|:---|
| 21-error Rigid Body Kinematic (RBK) model | Explicitly codified (ISO 230-1, ASME B5.54) with full 6-PDGE + 3-PIGE breakdown | Same framework, references "Rigid Body Assumption" with 21 components | **Strong** — Both adopt the canonical model |
| HTM-based volumetric error propagation | Full 4×4 matrices with small-angle approximation | Same HTM topology (Base → Y → X → Tool) with small-angle rotation error matrix $\mathbf{R}_{E,i}$ | **Strong** — Mathematically equivalent |
| Planar deviation equations ($d_x$, $d_y$) | Equations (lines 90–100) include positioning, straightness, squareness, and Abbe terms | Equations (lines 762–768) include same terms with explicit Abbe offset notation $(X_p, Y_p, Z_p)$ | **Strong** — Functionally identical; Report 2 uses clearer Abbe offset notation |
| Squareness error dominance | $\alpha_{xy} \cdot y$ grows linearly with travel; at 500 mm, even 1 µrad/mm → 500 µm | Included in $d_x$ as $-y \cdot \alpha_{xy}$ | **Strong** |
| Abbe error as dominant amplifier | Quantified: 5 µrad × 80 mm offset = 0.4 µm — "consumes entire ±200 nm budget twice over" | Explicitly calls $Z_p$ the "heavily amplifying" parameter | **Strong** |

> [!TIP]
> **For the paper:** The agreed kinematic model is mature and well-referenced. Use Report 1's detailed derivation as the primary mathematical exposition, and Report 2's $(X_p, Y_p, Z_p)$ notation for Abbe offsets as it is more intuitive for readers.

---

### ✅ 1.2 Encoder Error Decomposition

| Topic | Report 1 | Report 2 | Consensus |
|:---|:---|:---|:---|
| SDE is cyclic, non-accumulating, at grating pitch | Yes — full Fourier model with $n=1,2$ harmonics | Yes — "repeats exactly every scale grating pitch" | **Strong** |
| SDE sources: amplitude mismatch, phase error, DC offset | Detailed Lissajous distortion analysis | "Signal offset, amplitude imbalance, phase shift, harmonic distortion" | **Strong** |
| Long-range scale errors from CTE mismatch + mounting | Quantified: ZERODUR vs steel ΔL calculation | "Thermal expansion, mechanical tension, cosine errors" | **Strong** |
| Transition to ZERODUR scales for sub-µm work | Explicit recommendation with Heidenhain LIP 481 specs | "Transition to Zerodur scales or Laser Interferometric Encoders" | **Strong** |

---

### ✅ 1.3 Thermal Compensation Strategy

| Topic | Report 1 | Report 2 | Consensus |
|:---|:---|:---|:---|
| Thermal error is 40–70% of total volumetric error | Implied through structured taxonomy | Explicitly stated: "40%–70% of total machine volumetric error" | **Strong** |
| Camera intrinsic drift is a critical, neglected error source | Full quantification: 23 ppm/K magnification drift, 12 nm/K edge-of-field error | "Drift in camera's intrinsic matrix ($f_x, f_y, c_x, c_y$)" | **Strong** |
| GPR for thermal error compensation | Full Bayesian posterior derivation with kernel function | "Non-parametric Bayesian framework... handles non-linear thermal time-constants" | **Strong** |
| PINNs for physics-constrained thermal modelling | Full PINN loss function ($\mathcal{L}_{data} + \lambda_{pde} \cdot \mathcal{L}_{PDE} + \lambda_{bc} \cdot \mathcal{L}_{BC}$) | "Embeds Fourier heat conduction equations into the loss function" | **Strong** |
| RTD sensor network is required | 6-point placement recommendation | "Distributed PT100/RTD networks" | **Strong** |

---

### ✅ 1.4 Vision-Based Calibration Architecture

| Topic | Report 1 | Report 2 | Consensus |
|:---|:---|:---|:---|
| Zerodur grid plate as metrological reference | Detailed specs table; CTE ±0.05 ppb/K | "CTE ≈ 0 ± 0.05 × 10⁻⁶/K" | **Strong** |
| Sub-pixel centroiding for dot detection | Cramér-Rao bound derivation → 12 nm theoretical | "Zernike moments or Gaussian fitting... 1/100th of a pixel" | **Strong** |
| Bundle Adjustment (BA) for simultaneous error solving | Full reprojection error minimisation formulation with Huber robust loss | "Bundle Adjustment (Global Optimization)... minimizes reprojection error" | **Strong** |
| Homography for rapid thermal drift monitoring | 4-point DLT/homography in <5 ms | "Compute a Homography Matrix $\mathbf{H}$ mapping image plane coordinates to metric coordinates" | **Strong** |
| ACS SPiiPlus 2D LUT integration | Detailed architecture: bilinear interpolation, `MTBF` atomic updates, demand-side offsets | "ACS's `Mapped Variables` allow native multi-axis 2D compensation tables" | **Strong** |

---

### ✅ 1.5 Nanopositioning Challenges

| Topic | Report 1 | Report 2 | Consensus |
|:---|:---|:---|:---|
| Pre-sliding hysteresis / stick-slip in rolling guides | Full Dahl + LuGre model derivation | "LuGre (Lund-Grenoble) or Dahl dynamic friction observer" | **Strong** |
| Force ripple / cogging in linear motors | Fourier series model of cogging; coreless motors recommended | "Iron-core → cogging; ironless → spatial force ripple" | **Strong** |
| Cable drag chain as poorly-modelled disturbance | Detailed: 0.5–5 N parasitic force, non-repeatable settling disturbance 50–300 nm | "Chaotic, position-dependent spring-stiffness and damping" | **Strong** |
| Air bearings for <100 nm work | Technology roadmap table recommends air bearings below 500 nm | "At <100 nm, transition hardware to Aerostatic (Air) Bearings" | **Strong** |
| ±200 nm is achievable only with active management of **every** error source | RSS error budget totalling 55–75 nm (1σ) | "Pushing against fundamental non-linear physical phenomena" | **Strong** |

---

### ✅ 1.6 Publication & IP Strategy

| Topic | Report 1 | Report 2 | Consensus |
|:---|:---|:---|:---|
| Target journals include *Precision Engineering* and *IEEE/ASME TMECH* | Yes — Primary and secondary targets | Yes — listed as targets 2 and 3 | **Strong** |
| File provisional patent before publication | Explicit IP protection sequence | "File utility patents on 'Real-Time PINN-based LUT Morphing' before publishing" | **Strong** |
| Novelty must be "simultaneous decoupling" not just "we made a vision system" | Three explicit novelty claims articulated | "Reviewers will reject simple 'we made a vision system' papers" | **Strong** |
| Paper must include experimental validation against laser interferometer ground truth | Section 6 of paper outline | Section 5 of paper outline | **Strong** |

---

## 2. Points of Disagreement / Divergence

These are areas where the reports differ in emphasis, specificity, or recommendation. **Each must be resolved before writing the paper.**

### ⚠️ 2.1 Primary Target Journal

| Aspect | Report 1 | Report 2 | Resolution Recommendation |
|:---|:---|:---|:---|
| **Primary journal** | *Precision Engineering* (IF ~3.5) | *Int. J. Machine Tools & Manufacture* (IF ~14) | **Report 2 is more ambitious and strategically correct.** IJMTM has much higher impact and visibility. However, the 4× higher IF means stricter review. **Suggestion:** Target IJMTM first; fall back to *Precision Engineering* if rejected. |
| **CIRP Annals** | Listed as "Prestigious/Selective" (IF ~6.5) | Not mentioned | Include as aspirational target for a condensed 4-page CIRP version after the full paper is accepted |

> [!IMPORTANT]
> **For the paper strategy:** Report 2's recommendation of *Int. J. Machine Tools & Manufacture* is the stronger choice — it is **the** definitive venue for machine tool calibration. The Gao et al. (2023) review paper cited in Report 2 was published there. However, **the bar is higher** — you need laser interferometer ground-truth validation data and full ISO GUM uncertainty budgets to pass review.

---

### ⚠️ 2.2 HTM Topology Order

| Aspect | Report 1 | Report 2 |
|:---|:---|:---|
| **Kinematic chain** | Base → X → Y → Tool | Base → Y → X → Tool |

> [!WARNING]
> **This is a significant mathematical disagreement.** The ordering of the kinematic chain (which axis is stacked on which) determines how cross-axis errors couple. The correct topology depends on PBA's **actual physical machine design** — which axis carries which. For a typical gantry: the Y-axis carriage rides on the X-axis gantry beam, making the chain Base → X → Y → Tool (Report 1's convention). However, the reverse is also common in bridge-type gantries.
> 
> **Resolution:** Verify against the physical machine. This must be consistent in the paper. The equations in both reports are functionally equivalent **if** the symbols are relabelled — but the ordering must match reality.

---

### ⚠️ 2.3 Abbe Offset Notation

| Aspect | Report 1 | Report 2 |
|:---|:---|:---|
| **Notation** | $L_y$, $L_z$, $L_x$ as "Abbe arm components" | $(X_p, Y_p, Z_p)$ as "Abbe offsets from carriage center" |

**Resolution:** Report 2's notation is physically clearer and more common in the precision engineering literature (e.g., Schwenke et al., CIRP 2008). **Adopt Report 2's notation** in the paper.

---

### ⚠️ 2.4 Sub-Pixel Detection Algorithm

| Aspect | Report 1 | Report 2 |
|:---|:---|:---|
| **Method** | "Sub-pixel blob detection" with Cramér-Rao lower bound analysis | "Zernike moments or Gaussian fitting" |
| **Actual codebase** | MVTec HALCON XLD contour detection (`add_metrology_object_circle_measure`) — **neither blob detection nor Zernike moments** |

> [!CAUTION]
> **Neither report accurately describes the implemented algorithm.** The codebase uses HALCON's metrology model with XLD (eXtended Line Description) contour-based circle fitting — a fundamentally different approach from simple blob detection or Zernike moments. The paper **must** describe the actual HALCON metrology approach used.
>
> **The HALCON XLD approach is arguably superior** to both suggestions — it uses sub-pixel edge detection along measurement regions radiating from an expected circle, fitting a circle to the detected edge points. This is the industry standard for high-accuracy circle metrology and has a strong academic pedigree (Steger, "Subpixel-precise extraction of lines and edges," *ISPRS J. Photogrammetry*, 2000).

---

### ⚠️ 2.5 Thermal Compensation Readiness

| Aspect | Report 1 | Report 2 |
|:---|:---|:---|
| **Presentation** | GPR and PINN as future Phase 2/3 capabilities with full mathematical detail | GPR and PINN presented as "cutting-edge research" to be adopted |
| **Codebase reality** | Temperature monitoring exists ([temparature_monitoring.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/services/temparature_monitoring.py)) with 4 RTD channels logged, but **no GPR/PINN model is implemented** |

**Resolution:** The paper should clearly delineate Phase 1 (geometric mapping — what's implemented) from Phase 2 (thermal compensation — what's planned). Presenting GPR/PINN as "implemented" when they are not would be academically dishonest and would fail peer review.

---

### ⚠️ 2.6 Depth of Reference Quality

| Aspect | Report 1 | Report 2 |
|:---|:---|:---|
| **Number of references** | 8 papers in Table 4 | 4 references |
| **Bibliographic completeness** | **Incomplete** — several entries lack DOIs, full author lists, exact publication years (e.g., "Irino et al. (Precision Engineering)" — no year) | **Complete** — all 4 references have DOI, authors, journal, year |
| **Verification** | Several references appear to be approximate or partially fabricated (e.g., "GPR thermal error, *Precision Engineering*, 2022" — no authors or DOI) | All references appear verifiable with real DOIs |

> [!CAUTION]
> **Report 1's reference table (Table 4) contains bibliographic entries that cannot be independently verified.** For a peer-reviewed paper, every citation must be traceable to a real publication with correct DOI, authors, title, journal, volume, pages, and year. Report 2's references are the more trustworthy foundation.

---

## 3. Academic Rigor Assessment

### Rating Scale
- 🟢 **Rigorous** — Backed by peer-reviewed references, mathematically sound, experimentally grounded
- 🟡 **Partially Rigorous** — Correct concepts but missing citations, incomplete derivations, or unverified claims
- 🔴 **Not Rigorous** — Unsubstantiated claims, missing references, or conflicts with implementation

### 3.1 Report 1 Section-by-Section Assessment

| Section | Rigor | Issues |
|:---|:---|:---|
| §1.1 21-Error RBK Model | 🟢 | Well-established framework. Cite ISO 230-1:2012 and Schwenke et al. (2008) |
| §1.2 HTM Error Propagation | 🟢 | Standard formulation. Small-angle validity at ε ≲ 100 µrad correctly stated |
| §1.3 Abbe Error | 🟢 | Quantified correctly. Good PBA-specific worked example |
| §1.4 2D Volumetric Deviation Equations | 🟡 | Equations correct but "Fan et al." reference is **vague** — no DOI, incomplete citation |
| §1.5 Encoder SDE | 🟡 | Fourier model correct. "Ye et al., 2019" reference plausible but needs DOI verification. "Heidenhain LIP 481 SDE <1 nm" — needs manufacturer specification sheet citation |
| §2.1 Thermal Error Taxonomy | 🟡 | Good structure, but the quantitative values (e.g., "2–5 µm per active hour") are **unsourced** — need experimental or literature backing |
| §2.2 Camera Intrinsic Thermal Drift | 🟢 | Well-derived. $dn/dT$ for BK7 is correct. Magnification change calculation is sound |
| §2.3 RTD Placement | 🟡 | Reasonable recommendations but the "maximal information content" claim needs a citation (e.g., optimal sensor placement, D-optimal design) |
| §2.4 GPR/PINN Compensation Models | 🟡 | Mathematics correct. "GPR Precision Engineering 2022" claim of "<300 nm (3σ)" is **unverifiable** without proper citation |
| §3.1 Error Budget | 🟡 | Good RSS analysis. But the individual budget allocations (e.g., "10–20 nm for cable drag") are **engineering estimates, not measured values**. Must be labelled as such |
| §3.2 Friction Models | 🟢 | LuGre and Dahl models correctly formulated. Canudas de Wit (1995) is a valid foundational reference |
| §3.3 Force Ripple | 🟡 | Fourier model correct. "Fu et al., Wiley Complexity, 2018" — needs DOI verification |
| §3.4 Cable Drag Chain | 🟡 | Acknowledges this is "poorly published." The 0.5–5 N range is labelled as "internal industry data" — acceptable for R&D report but **insufficient for a peer-reviewed paper** |
| §4.1 Zerodur Grid Plate | 🟢 | Specifications match commercial data sheets (Heidenhain PP281, Schott ZERODUR) |
| §4.2 Sub-Pixel Detection | 🔴 | **Does not describe the actual HALCON XLD method used in the codebase.** Cramér-Rao bound analysis is theoretically correct but applied to a "Gaussian blob" model that doesn't match implementation |
| §4.3 Bundle Adjustment | 🟡 | Formulation correct but PBA's codebase **does not implement BA** — it uses direct homography per-image. Presenting this as "implemented" would be misleading |
| §4.4 ACS LUT Integration | 🟢 | Matches the codebase implementation in [acs_python_modules.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/motor_control/acs_python_modules.py) and [generate_2D_encoder_error_matrix.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/services/generate_2D_encoder_error_matrix.py) |
| §5 Publication & IP | 🟡 | Good strategic advice. Novelty claims are strong but **Claim 2 (BA-corrected camera drift) and Claim 3 (real-time LUT update) are aspirational, not yet validated with published data** |

### 3.2 Report 2 Section-by-Section Assessment

| Section | Rigor | Issues |
|:---|:---|:---|
| §1.1 SDE vs Mounting Errors | 🟢 | Concise and accurate |
| §1.2 HTM Formulation | 🟢 | Compact and correct. Clearer Abbe offset notation than Report 1 |
| §2.1 Thermal Sources | 🟡 | "40–70%" claim needs citation (Mayr et al., CIRP Annals 2012 is the standard reference for this statistic) |
| §2.2 GPR & PINNs | 🟡 | Correct concepts but compressed. Insufficient mathematical detail for a paper |
| §3 Nanopositioning Table | 🟢 | Good summary table with mitigation strategies. Well-structured |
| §4.1 Zerodur Artifacts | 🟢 | Correct CTE specification |
| §4.2 Algorithmic Workflow | 🟡 | Mentions "Zernike moments" — **not what's implemented**. Otherwise reasonable |
| §4.3 ACS Integration | 🟡 | "Cross-Coupled Feedback" claim ("micro-adjustments in Y and Yaw via dual-loop PID") is **not implemented in the codebase** — the ACS integration is LUT-based, not cross-coupled |
| §5.1 Target Journals | 🟢 | IJMTM is an excellent choice. Well-justified |
| §5.3 References | 🟢 | **All 4 references have complete, verifiable DOIs** — this is the gold standard |

---

## 4. Codebase vs. Reports: What's Actually Implemented?

This is **critical** for the paper — you can only claim what you've built and validated.

### ✅ Implemented and Validated (Can be published as Phase 1 results)

| Capability | Codebase Evidence | Report Coverage |
|:---|:---|:---|
| **2D dot grid scanning** with automated stage motion | [scan_and_capture.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/image_processing/scan_and_capture.py) — `scan_method_5()` | Both reports ✅ |
| **HALCON XLD sub-pixel circle detection** for dot centroiding | [calculation_using_halcon.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/image_processing/calculation_using_halcon.py) — HALCON metrology model | ❌ Neither report accurately describes this |
| **Vision-based self-centering** (dot center → encoder position correction) | [scan_and_capture.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/image_processing/scan_and_capture.py) — `estimate_dot_center_button_clicked()` | Report 1 mentions "self-referencing" |
| **Glass scale certificate generation** (relative dot distances) | [generate_2D_glass_certificate_62207.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/services/generate_2D_glass_certificate_62207.py) | Both reports ✅ |
| **Camera rotation correction** via best-fit line + rotation matrix | [generate_2D_encoder_error_matrix.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/services/generate_2D_encoder_error_matrix.py) — `get_camera_rotation_matrix()` | Not explicitly described in either report |
| **2D encoder error matrix** (encoder position − vision position) | [generate_2D_encoder_error_matrix.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/services/generate_2D_encoder_error_matrix.py) — `generate_2D_encoder_error_matrix()` | Both reports ✅ |
| **ACS-format 2D error map generation** (LUT for controller) | [generate_2D_encoder_error_matrix.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/services/generate_2D_encoder_error_matrix.py) — `generate_ACS_errormaps()` + `convert_to_acs_format()` | Both reports ✅ |
| **Error correction verification testing** | [generate_2D_error_mapping_test.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/services/generate_2D_error_mapping_test.py) | Report 1 §6 outline ✅ |
| **Error map visualization** (X and Y plots) | [generate_2D_error_mapping_test_plot.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/services/generate_2D_error_mapping_test_plot.py) | Both reports ✅ |
| **Camera distortion correction** (OpenCV `undistort()` with calibration data) | [generate_2D_glass_certificate_62207.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/services/generate_2D_glass_certificate_62207.py) — `create_undistort_image()` | Report 1 mentions Brown-Conrady model |
| **Temperature logging** (4 RTD channels via ACS/Wago) | [acs_python_modules.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/motor_control/acs_python_modules.py) — `read_temparature()`, logged in scan methods | Report 1 §2.3 ✅ |
| **ACS motor control integration** (SPiiPlus TCP/IP) | [acs_python_modules.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/motor_control/acs_python_modules.py) | Both reports ✅ |
| **In-position stability analysis** (static & dynamic) | [scan_and_capture.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/image_processing/scan_and_capture.py) — `scan_method_6()`, `scan_method_7()` | Not explicitly in reports |
| **Auto-focus via Sobel variance** | [scan_and_capture.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/image_processing/scan_and_capture.py) — `scan_method_8()`, `auto_focus()` | Not in reports |

### ❌ Discussed but NOT Implemented (Phase 2/3 — future work in paper)

| Capability | Status | Notes |
|:---|:---|:---|
| Bundle Adjustment (BA) | ❌ Not implemented | The codebase uses per-image homography/affine transform, not global BA |
| Gaussian Process Regression (GPR) for thermal compensation | ❌ Not implemented | Temperature is **logged** but no predictive model exists |
| Physics-Informed Neural Networks (PINNs) | ❌ Not implemented | No ML/DL code in the repository |
| Real-time dynamic LUT update during production | ❌ Partially — LUT is generated offline | The LUT is generated after a scan run (inside `scan_method_5()`), not updated in real-time |
| Cross-coupled feedback (Y + Yaw correction) | ❌ Not implemented | ACS integration is demand-side LUT, not cross-coupled PID |
| Disturbance Observer (DOB) / ADRC | ❌ Not implemented | Standard ACS PID loop is used |

---

## 5. Recommendations for the Scientific Paper

### 5.1 Recommended Paper Scope (What to Publish Now)

Based on what the codebase actually implements, the strongest publishable paper is:

> **Title:** *"In-Situ Vision-Based 2D Geometric Error Mapping for Production Gantry Stages Using Sub-Pixel XLD Contour Detection and Certified Grid Plate Metrology"*

This paper covers **Phase 1 only** — the geometric mapping system. It is honest about what's implemented, leaves GPR/PINN/BA as "Future Work," and focuses on the real engineering contributions.

### 5.2 Paper Structure Aligned to Codebase

| Section | Content | Key Code Reference |
|:---|:---|:---|
| **1. Introduction** | Production precision requirements; limitations of offline laser calibration; statement of contribution | — |
| **2. Kinematic Error Model** | 21-error RBK for XY gantry; HTM formulation; Abbe offset analysis; squareness error scaling | Mathematical from reports |
| **3. Vision Measurement System** | 3.1 Zerodur grid plate (500×500 mm, 5 mm pitch, certified); 3.2 HALCON XLD contour-based circle metrology (sub-pixel); 3.3 Camera calibration & distortion correction (OpenCV); 3.4 Camera rotation correction algorithm | [calculation_using_halcon.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/image_processing/calculation_using_halcon.py), [generate_2D_glass_certificate_62207.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/services/generate_2D_glass_certificate_62207.py) |
| **4. Error Map Generation** | 4.1 Glass certificate generation (relative dot distances); 4.2 Cumulative vision distance matrix; 4.3 Encoder error matrix (encoder − vision); 4.4 ACS 2D LUT format generation | [generate_2D_encoder_error_matrix.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/services/generate_2D_encoder_error_matrix.py) |
| **5. Experimental Setup & Results** | Machine description; scanning procedure; error map results (before/after correction); repeatability analysis; comparison with laser interferometer | [scan_and_capture.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/image_processing/scan_and_capture.py), [generate_2D_error_mapping_test.py](file:///c:/Users/mj.j/Documents/pba_vision_mapping/src/backend/services/generate_2D_error_mapping_test.py) |
| **6. Discussion** | Measurement uncertainty analysis (ISO GUM); comparison with prior art; limitations (no thermal compensation yet) | — |
| **7. Conclusion & Future Work** | Summary; Future: GPR/PINN thermal model, BA optimisation, real-time LUT update | — |

### 5.3 Critical Gaps to Fill Before Submission

| Gap | Priority | Action Required |
|:---|:---|:---|
| **Laser interferometer ground truth data** | 🔴 Critical | You need independent laser interferometer measurements of the same axes to validate the vision system. Without this, no top-tier journal will accept the paper |
| **ISO GUM uncertainty budget** | 🔴 Critical | Every measurement result must have a stated uncertainty with traceability. The codebase logs position error values but doesn't compute formal uncertainty |
| **Proper HALCON algorithm description** | 🟡 High | The paper must describe the actual XLD contour-based circle fitting used, not generic "blob detection" or "Zernike moments" |
| **Verified reference list** | 🟡 High | Start with Report 2's 4 verified references and expand. Every citation must have: Authors, Title, Journal, Volume, Pages, Year, DOI |
| **Repeatability data** | 🟡 High | Use `scan_method_6()` and `scan_method_7()` data to characterize measurement repeatability (3σ values) |
| **Temperature correlation data** | 🟢 Medium | Temperature is logged during scans. Even without GPR/PINN, plotting error drift vs. temperature would add value |

### 5.4 Key References to Build Upon

These are **verified, foundational references** that both reports agree on, supplemented with additional essential citations:

| # | Reference | DOI | Relevance |
|:---|:---|:---|:---|
| 1 | Gao, W., Ibaraki, S., et al. (2023) "Machine tool calibration: Measurement, modeling, and compensation..." *IJMTM* 167, 104017 | `10.1016/j.ijmachtools.2023.104017` | Definitive review — **must cite** |
| 2 | Schwenke, H., Knapp, W., et al. (2008) "Geometric error measurement and compensation of machines — An update" *CIRP Annals* | `10.1016/j.cirp.2008.09.008` | RBK model, Abbe offsets — **must cite** |
| 3 | Chen, G., Li, Y., et al. (2021) "Physics-informed Bayesian inference..." *IJMTM* | `10.1016/j.ijmachtools.2021.103767` | PINN framework for future work |
| 4 | Gao, W., Shimizu, Y. (2021) *Optical Metrology for Precision Engineering* De Gruyter | ISBN 978-3110541090 | SDE, vision calibration |
| 5 | Mayr, J., et al. (2012) "Thermal issues in machine tools" *CIRP Annals* 61(2), 771–791 | `10.1016/j.cirp.2012.05.008` | "40–70% thermal contribution" claim |
| 6 | Steger, C. (2000) "Subpixel-precise extraction of lines and edges" *ISPRS J. Photogrammetry & Remote Sensing* | — | HALCON XLD theoretical basis |
| 7 | Canudas de Wit, C., et al. (1995) "A new model for control of systems with friction" *IEEE TAC* 40(3) | `10.1109/9.376053` | LuGre friction model |

> [!IMPORTANT]
> **A peer-reviewed paper in IJMTM or Precision Engineering typically cites 30–60 references.** The current combined reference count of ~12 is insufficient. You need to expand to cover: (1) vision-based machine tool calibration, (2) grid plate metrology, (3) sub-pixel measurement methods, (4) ACS/motion controller error compensation, (5) gantry stage design, (6) measurement uncertainty/ISO GUM, (7) comparable industry implementations.

---

## 6. Summary Decision Matrix

| Decision Point | Recommendation | Source |
|:---|:---|:---|
| Primary journal | *Int. J. Machine Tools & Manufacture* | Report 2 |
| Kinematic chain topology | Verify against physical machine; adopt Report 2 notation | Resolve |
| Abbe offset notation | $(X_p, Y_p, Z_p)$ | Report 2 |
| Sub-pixel detection description | HALCON XLD contour-based circle metrology | Codebase |
| Thermal compensation claims | Phase 1 paper: **geometric only**; GPR/PINN as future work | Codebase reality |
| Bundle Adjustment claims | Future work; current system uses per-image homography | Codebase reality |
| Error budget | Report 1's RSS table — but label as "engineering estimates" pending validation | Report 1 |
| Reference foundation | Start from Report 2's 4 verified references; expand to 30–60 | Report 2 + additional literature search |
