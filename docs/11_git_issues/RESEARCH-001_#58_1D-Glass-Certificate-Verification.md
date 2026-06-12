---
GitHub Issue: #58
Type: Research
Priority: High
Status: In Progress
Assignee: Malith
Sprint: Current
Labels: type: research, priority: high
Created: 2026-04-14
Requirement Refs: REQ-002, NFR-ACCU-001
---

# [RESEARCH-001] Generate 1D Glass Certificate for Column & Verify with Original Certificate

## Research Question

Can the onboard camera system (FLIR BFS-U3 + 0.35X telecentric lens + Halcon sub-pixel detection) replicate the certified glass scale measurements to the same decimal precision as the original certificate from the measurement company? What is the achievable measurement resolution in nanometers?

## Context and Motivation

The project relies on a certified master glass scale (500×500 mm, 5 mm pitch, 100×100 grid) as the reference standard. The original certificate from the measurement company provides certified dot positions for specific columns and rows. Before using the vision system for full 2D error mapping, we need to verify that our camera system can reproduce these certified values with sufficient accuracy.

This research also aims to:
- Calculate the **pixel distance in mm** (pixel-to-mm calibration)
- Study the **effect of temperature variation** on measurement accuracy
- Understand the limitations of the onboard camera system
- Determine the highest usable decimal precision

## 0.35X Telecentric Lens — Field of View Characteristics

| Parameter | Value |
|-----------|-------|
| **Lens magnification** | 0.35X telecentric |
| **Visible dots (horizontal)** | ~10 marks |
| **Visible dots (vertical)** | ~7 marks |
| **Dot pitch** | 5 mm |
| **Measurement pitch** | 25 mm (every 5th dot) |
| **Measured dots per image** | ~4 dots visible in single image |

> **Key advantage:** The 0.35X lens can see 4 measured dots in a single image, which is sufficient for creating the glass certificate. The 4X telecentric lens cannot capture enough fiducial marks for this purpose.

## Measured Lines on Original Certificate

| Line | Description | Points |
|------|-------------|--------|
| **Column C50** | Center column | R0-C50 → R100-C50 (21 measured dots) |
| **Row R50** | Center row | R50-C0 → R50-C100 (21 measured dots) |
| **Row R55** | Near-center row | R55-C0 → R55-C100 (21 measured dots) |

## Approach

### Equipment
- FLIR BFS-U3 camera (USB3, via PySpin / `bfs_camara_api`)
- 0.35X telecentric lens (currently mounted and operational)
- Gantry with ACS motor controller
- Certified 500×500 mm glass scale
- Temperature monitoring equipment

### Method
1. **Scan the 3 measured lines** using 1D expantion X axis and Y axis `scan_method_4()`.
2. **Generate 1D glass certificate** for each line using adapted `generate_glass_certificate_62207.py`
3. **Load original certificate data** (create input folder for certified values)
4. **Compare vision-measured positions** with original certified positions
5. **Calculate deltas** between vision and certified values at each dot
6. **Compute statistics**: mean error, max error, std deviation, 3σ
7. **Study pixel-to-mm calibration** stability across the measured lines
8. **Monitor temperature** during scans and correlate with measurement drift

### Data Storage
- Create folder for original certificate data: `data/reference_certificates/` or similar
- Store as CSV format (or matrix format — TBD)
- Consider hardcoding reference values in software for runtime comparison

### Baseline
- **Target precision:** 1nm resolution (even if not achievable, this is the aspiration)
- **Acceptable result:** Match original certificate within the certified uncertainty band
- **Good result:** Match within 100nm
- **Excellent result:** Match within 50nm or better

## Success Criteria

- [ ] 1D certificate generated for Column C50
- [ ] 1D certificate generated for Row R50
- [ ] 1D certificate generated for Row R55
- [ ] Vision vs. certified comparison completed for all 3 lines
- [ ] Pixel-to-mm distance calculated and documented
- [ ] Temperature variation effect studied and documented
- [ ] Statistical analysis (mean, max, std, 3σ) completed
- [ ] Results documented with clear recommendation for achievable precision
- [ ] Decision on data storage format for original certificate
- [ ] Input data folder created and structured

## Output Artifacts

| Artifact | Format | Location |
|----------|--------|----------|
| 1D Certificate — Column C50 | CSV | `<image_data_folder>/` |
| 1D Certificate — Row R50 | CSV | `<image_data_folder>/` |
| 1D Certificate — Row R55 | CSV | `<image_data_folder>/` |
| Comparison Report | CSV / Markdown | `docs/` |
| Original Certificate Data | CSV | `data/calibration_certificate_JL2621363131.csv/` |
| Temperature Log | CSV | `<image_data_folder>/` |
| Pixel-to-mm Calibration Values | CSV | `<image_data_folder>/` |

## Time Box

**Maximum time:** 3 weeks
**Check-in date:** Weekly progress review

## Notes

- The original certificate has certified values from the measurement company — these are the ground truth
- Temperature affects measurements — document ambient temperature for every scan
- Multiple repeat scans at same locations will help quantify vision system jitter
- This research directly informs whether the system can achieve NFR-ACCU-001 (100nm accuracy)
- Consider creating a dedicated script (e.g., `generate_1D_glass_certificate.py`) or adapting the existing 2D script
- For temperature-dependent calibration research, see [RESEARCH-003](RESEARCH-003_%23NN_Temperature-Dependent-Calibration.md)
