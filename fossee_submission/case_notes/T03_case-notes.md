# T03 — Three consecutive designs with custom materials

**Packaged evidence:** [evidence/T03/](../evidence/T03/). File names below refer to this folder or its recorded session subfolder.


**Test date:** 10 November 2026 (local timestamps, UTC+05:30)  
**Sequence:** 25 m → 20 m → 25 m in one recorded application session  
**Result:** The three engine calls completed without captured exceptions. The plots updated and the final 25 m run reproduced the first run's captured numerical results. Material-density and data-consistency findings remain open. All three generated designs report an overall engineering status of FAIL.

## What I wanted to check

I wanted to check whether changing the span between designs updated the calculations and graphics without restarting the application. Returning to the original span gave me a direct comparison with the first run. I kept the same custom steel and concrete material selections for this sequence.

I reported no errors during my recording. The video has not been reviewed for these notes; the findings below come from my screenshots, saved inputs, captured dictionaries, runtime properties and PDF reports. A completed analysis is recorded separately from a structurally passing design.

## Evidence and environment

My original session was `session_20261110_185755_761615`. Its extracted files are included under `evidence/T03/`, with one session record and three numbered run folders. Each run contains the before/after input and output dictionaries, runtime properties, status, two OSI files, a CAD screenshot, a deflection screenshot and a PDF report. I have kept these original files unchanged.

The session metadata records Windows 11, Python 3.12.16 (conda-forge), process ID 23780 and repository commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. The recorded Git status lists the untracked `FOSSEE_Testing/` and `screening/` directories and no tracked changes. The session started at 18:57:55.

The recorder wrapped `PlateGirderBridge.design()` in memory and called the original method once per run. It captured state immediately around that call. It did not alter design inputs or solver logic. Its timings cover the core call, not subsequent GUI rendering or PDF export; recording also adds some file-I/O overhead. These observations are not a performance benchmark.

## Inputs used

| Parameter | R1 | R2 | R3 |
|---|---:|---:|---:|
| Span, m | 25 | 20 | 25 |
| Carriageway width, m | 7.5 | 7.5 | 7.5 |
| Skew, degrees | 0 | 0 | 0 |
| Median | No | No | No |
| Footpath | None | None | None |
| Design mode | Optimized | Optimized | Optimized |
| Deck thickness, mm, as reported | 250 | 250 | 250 |
| Girder spacing, m, as reported | 2.1 | 2.1 | 2.1 |
| Physical girders in report | 4 | 4 | 4 |
| Wearing course material | Concrete | Concrete | Concrete |
| Wearing course thickness, mm | 50 | 50 | 50 |

The complete parameter combinations are preserved in each `input_before.json` and `R*_before.osi`. These files are both needed: they do not contain identical values for every field, as documented below. I did not assume that all unedited fields were defaults.

### Custom steel

The three input dictionaries select `custom_steel_345_500` for the girder, cross bracing and end diaphragm. The following material values remain unchanged before and after all three design calls.

| Property | Entered/captured value | Runtime girder property |
|---|---:|---|
| Weight density | 77.0 kN/m³ | **78,500 N/m³ = 78.5 kN/m³ — mismatch** |
| Yield strength | 345 MPa | 345,000,000 Pa — matches |
| Ultimate strength | 500 MPa | 500,000,000 Pa — matches |
| Elastic modulus | 205 GPa | 205,000,000,000 Pa — matches |
| Shear modulus | 78.8 GPa | Not separately exposed in the captured steel object |
| Poisson's ratio | 0.3 | 0.3 — matches |
| Thermal expansion coefficient | 11.7 × 10⁻⁶/°C | Not separately exposed in the captured steel object |

The design output also names this custom steel as `stiffener_grade`. This establishes the selected label; it does not independently verify every stiffener calculation. Using the same grade for all three steel selections does not test whether cross bracing and end diaphragms can use different material grades independently.

### Custom concrete

| Property | Captured input | Runtime/output evidence |
|---|---:|---|
| Material | custom_concrete_45_3.5 | Same grade in runtime and design results |
| Weight density | 25.5 kN/m³ | Not present in captured concrete DTO; correct use in deck loading is not established by this capture alone |
| Cube compressive strength | 45 MPa | Runtime fck = 45 |
| Mean tensile strength | 3.5 MPa | Runtime fctm = 3.5 |
| Secant elastic modulus | 35 GPa | Runtime Ecm = 35; design output Ecm_MPa = 35,000 |
| Thermal expansion coefficient | 10.5 × 10⁻⁶/°C | Retained in inputs; downstream use not established |

## Run log

| Run | Engine start | Engine finish | Captured core duration | Outcome |
|---|---|---|---:|---|
| R1, 25 m | 19:01:26 | 19:03:38 | 131.52 s | Returned; no exception or capture error |
| R2, 20 m | 19:10:01 | 19:11:10 | 68.41 s | Returned; no exception or capture error |
| R3, 25 m | 19:16:36 | 19:18:54 | 136.86 s | Returned; no exception or capture error |

Each captured input dictionary has 580 keys and each completed output dictionary has 1,070 keys. All three `output_before.json` files are empty dictionaries. This supports output reset before each captured design call, although it does not prove that every internal cache was reset.

## Multi-run state and graphics

The three CAD screenshots show rendered bridge models. Their camera angles differ, so I did not use their apparent length on screen as a dimensional measurement. I had already checked that CAD rotation worked. The numerical span in runtime state and the horizontal plot axes provide the stronger evidence of the geometry change.

| Evidence | R1 | R2 | R3 |
|---|---:|---:|---:|
| Runtime grillage length, m | 25 | 20 | 25 |
| Runtime transverse mesh count, n_t | 18 | 14 | 18 |
| Visible deflection plot span, m | 0–25 | 0–20 | 0–25 |
| Visible plotted Dy, mm | −3.70 | −2.32 | −3.70 |
| Visible location of plotted value, m | 11.76 | 9.23 | 11.76 |
| Designed girder depth, mm | 1390 | 1120 | 1390 |
| Designed top flange width, mm | 420 | 340 | 420 |
| Designed top flange thickness, mm | 18 | 16 | 18 |

The deflection screenshots are cropped and do not include the member/load selectors. I have therefore recorded their visible values without asserting that they establish the full load-case context. They are not comparable directly with the total-load deflections in the report.

R1 and R3 have exactly equal parsed before-input dictionaries. Their parsed after-output dictionaries differ in only `design_results.report_text`; the only changed line is its generated timestamp (19:02:56 versus 19:18:08). All other captured values match, including nested numerical results. R2 differs from R1 in 163 top-level output entries. This is a pass for the tested change-and-return sequence, not a claim that every possible consecutive-run scenario is stable.

The input dictionaries already contain span-dependent suggested sections before Design. Changing the span changed 84 captured input fields, including generated section properties and bracing spacing. It would be inaccurate to describe the raw input dictionaries as differing only in the span field.

## Output dictionary versus reports

The captured `util.*` values are percentages; the report also uses dimensionless demand/capacity ratios. For example, 199.85% corresponds to 1.9985, which displays as approximately 2.00 in a report table.

| Check / output | R1 | R2 | R3 |
|---|---:|---:|---:|
| util.flexure, % | 23.73 | 25.29 | 23.73 |
| util.shear, % | 53.48 | 36.63 | 53.48 |
| util.interaction, % | 24.05 | 25.66 | 24.05 |
| util.ltb, % | 19.30 | 21.04 | 19.30 |
| util.long_trans_shear, % | 24.72 | 23.32 | 24.72 |
| util.fatigue, % | 199.85 | 221.52 | 199.85 |
| util.stress_limitation, % | 31.95 | 34.85 | 31.95 |
| util.deflection_crack, % | 53.26 | 62.97 | 53.26 |
| design_results.overall_status | FAIL | FAIL | FAIL |
| design_results.max_dcr | 1.9985 | 2.2152 | 1.9985 |
| Report maximum ratio, rounded | 2.00 | 2.22 | 2.00 |

All three PDF reports contain 58 physical pages. Their executive summaries on physical page 3 report an overall failed design and fatigue as the governing check. The larger fatigue ratio at 20 m is not, by itself, a stale-state bug: the optimized design selected a different, smaller girder section.

The per-girder output fields match the report's deflection tables:

| Report quantity / matching output fields | R1 and R3 | R2 |
|---|---:|---:|
| G1/G4 live deflection, mm | 24.840 | 30.146 |
| G2/G3 live deflection, mm | 25.164 | 30.969 |
| G1/G4 total deflection, mm | 54.905 | 57.886 |
| G2/G3 total deflection, mm | 55.321 | 58.934 |
| Live-load limit, mm | 31.25 | 25.00 |
| Total-load limit, mm | 41.67 | 33.33 |

The fields are `steeldesign.deflection.live_mm.G1` through `.G4` and `steeldesign.deflection.total_mm.G1` through `.G4`. Physical page 21, Table 4.3, reports the maximum per-girder live and total values. The detailed Table 5.9 also reports failed total-deflection checks for all three runs, and failed live-deflection checks for the 20 m run.

However, the unsuffixed summary fields use smaller values: R1/R3 live = 11.103 mm and total = 22.190 mm; R2 live = 12.133 mm and total = 20.991 mm. These feed summary results that pass the deflection limit while the per-girder report values fail. The discrepancy needs load-combination and member-selection tracing before I can identify which calculation or mapping is wrong. I have kept both sets of values in the evidence rather than choosing one as correct.

### Additional screenshot: 06_output_dock.png

Despite the filename, this image is the **Girder Analysis and Design Results Summary**, on the Design Check tab with **Girder 1 / SW** selected. It shows shear demand 19.31 kN, resistance 443.02 kN, utilization 0.04 and PASS; the interaction card shows Mu = 97.32 kNm, Mdv = 6907.04 kNm, utilization 0.01 and PASS. The resistance values agree to displayed precision with the 25 m output capacities (443.023 kN and 6907.037 kNm).

These are checks for the selected member and SW case. They do not override the failed fatigue or total-deflection checks elsewhere. The image alone does not identify which 25 m run produced it, so I have not assigned it to a specific run.

## Input and saved-file consistency

The before/after OSI files are identical within each run. All selected custom material names and numeric material values also survive the design call in the input dictionaries. This is a pass for same-session input retention, but the density finding shows why retention alone is insufficient.

After normalizing numeric strings for comparison, each saved before-OSI differs from the captured before-input dictionary in 17 fields. Twelve differences are precision changes in generic girder section-property fields. Crash-barrier area changes from 302282.768 to 0.3023, consistent with mm²-to-m² conversion and rounding; barrier load changes from 7.557 to 7.56. The remaining differences require follow-up:

| Field | Saved OSI | Input at Design |
|---|---:|---:|
| typical_section.wearing_course.density | 24.0 | 25.0 |
| typical_section.railing.width | 0.0 | 0.275 |
| typical_section.railing.load_value | 1.4715 | 6.806 |

These discrepancies occur in all three runs. No footpath is selected, so the changed railing values do not by themselves establish an applied-load error. The wearing-course density difference is directly relevant to loading, but the exact save/reload or UI update event responsible has not yet been isolated. I followed this with T04, which captures a fresh-session reload without re-entering materials.

Each design call changes 35 input dictionary entries concerning girder dimensions and optimized thicknesses. For example, R1 depth changes from 1390 to 1.39, flange width from 420 to 0.42, and thickness selections from `All` to resolved metre values. These are consistent with unit conversion and optimization, not automatic proof of corruption. Any UI/report consuming the post-design dictionary must nevertheless convert units correctly.

## Confirmed findings and issue handling

### 1. Custom girder density is ignored at runtime

I entered 77.0 kN/m³, and all three captured input dictionaries retain that value. Every runtime steel object instead contains `rho = 78500.0` N/m³. The tested source confirms the path: `src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py`, `_build_material_props()`, lines 1192–1194, falls back to `_DEFAULT_DENSITY` when a custom grade has no database density.

The proposed change is to read `material.girder.density` for custom grades and convert kN/m³ to N/m³ before constructing `SteelProperties`, with validation for missing, nonfinite or nonpositive values. A focused regression check should assert that an input of 77 produces 77000, while a standard database grade keeps its database density. The application's `rho` field is used here as weight density; it must not be confused with kg/m³.

This is already covered by [upstream issue #20](https://github.com/Nidhikhare12/OsdagBridge/issues/20). I added supporting evidence in [my comment on #20](https://github.com/Nidhikhare12/OsdagBridge/issues/20#issuecomment-6797253814).

### 2. Crash-barrier width changes in the runtime layout

The captured input uses `typical_section.crash_barrier.width = 0.45` m in all three runs. Each runtime deck layout instead contains `crash_barrier_width = 0.5` m. `_build_dtos()` in the same source file, line 1019, assigns `float(DEFAULT_CRASH_BARRIER_WIDTH)` rather than reading the selected width.

The proposed change is to resolve the width from the validated input dictionary when constructing the deck-layout DTO, using the default only when the field is absent. A regression check should set a nondefault width and compare the UI/input, DTO and downstream layout dimensions. This capture establishes the input-to-runtime mismatch; it does not quantify the resulting engineering error.

I checked the issue list on 10 November 2026 and found no report specifically covering this width mismatch in the returned list. After the later T06 comparison and duplicate review, I published [issue #74](https://github.com/Nidhikhare12/OsdagBridge/issues/74).

### Related existing issues

- [#19](https://github.com/Nidhikhare12/OsdagBridge/issues/19): OSI reload does not restore custom-material field maps. I tested this separately in T04; T03 alone does not prove the reload bug.
- [#41](https://github.com/Nidhikhare12/OsdagBridge/issues/41): custom concrete density is not passed into deck loading. T03 preserves the requested density in inputs but does not directly capture the deck-load call argument.
- [#43](https://github.com/Nidhikhare12/OsdagBridge/issues/43): independent cross-bracing/end-diaphragm materials are not used. T03 uses the same grade, so it cannot isolate this defect.
- [#44](https://github.com/Nidhikhare12/OsdagBridge/issues/44): design/CAD generation completes with fatigue utilization above 100%. T03 reproduces that observation. Generating a failed design for inspection is not inherently an error; the important question is whether failure is clearly reported and the promised optimization behavior is met.
- [#48](https://github.com/Nidhikhare12/OsdagBridge/issues/48): incomplete report content. The reactions table on physical page 21 remains empty in the reviewed reports.

## Coverage and limits

| Area | What this case establishes | What remains |
|---|---|---|
| Consecutive design calls | Three completed in one captured session | Other input combinations and longer sequences |
| Geometry / plots | Runtime spans and plot axes change and return | Exact CAD dimension measurement |
| Custom materials | Input retention; selected runtime strengths and E agree | Correct use of all material properties |
| Girder checks | Captured results compared with selected report tables | Independent engineering recalculation |
| Stiffeners | Custom grade label present; failed intermediate-stiffener check reported | Complete dock/report checks for bearing and intermediate stiffeners |
| Deck | Custom fck/fctm/Ecm reach runtime; deck result dictionary exists | Full reinforcement, load and dock/report comparison |
| Cross bracing / end diaphragm | Result dictionaries exist for all runs | Independent grades and complete component verification |
| Saved-file persistence | Before/after OSIs identical in each run | Fresh-process reload test |
| Video | Recording reported complete | Video not inspected for these notes |

I recorded T03 as **passed for the tested consecutive-run behavior, with data-consistency defects recorded**. I would not label the overall bridge designs as passing. This case covers the consecutive-run sequence. The later cases and final report record the additional component checks and remaining coverage limits.

## Evidence manifest

Paths below are relative to the extracted session folder. SHA-256 hashes identify the original submitted files.

| Evidence file | SHA-256 |
|---|---|
| `run_01/R1_after.osi` | `26c79477e53f969b434e5ce6ced22954c3249ce9b103652e8fe13cb920502fef` |
| `run_01/R1_before.osi` | `26c79477e53f969b434e5ce6ced22954c3249ce9b103652e8fe13cb920502fef` |
| `run_01/R1_deflection.png` | `ff0d01246f94bcf72cee38f2f4908dd4b80c2db9adbc4b9c27eee6ea73317feb` |
| `run_01/R1_report.pdf` | `5d5cd9d25a2e50b55e600e46f3928df46065e3b74b3ed5a39058a729b0db7bb6` |
| `run_01/R1_result.png` | `689c4e3a8f92d5d318ea9303902287499e79f221de771d80204cc907ba40c298` |
| `run_01/input_after.json` | `8b8e93d31134b8871669efbf73666fd5fdf29a1c2bea0bca230d5bde2e3f7db6` |
| `run_01/input_before.json` | `92e05c3034da738a76c2190aea1eba2df1e6f06151b9fa6a8249a7f48bbb2af6` |
| `run_01/output_after.json` | `639a398d0eb55602cb0a6881141e368c0e6a30343caee4cd8613fccb89a565f0` |
| `run_01/output_before.json` | `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a` |
| `run_01/runtime_properties.json` | `c1dde83a0d5850246e914fc2e12ea425e305a60d905221f73f17ff623a3e249c` |
| `run_01/status.json` | `feb750345f54e2c43fe496259c70a4db24f68ef56cdca0758382fe257fd4a7de` |
| `run_02/R2_after.osi` | `58e976dd42e2495ea3dd1fb6b1c83d07c50662d16ebaa3688a0dbdd8a407d067` |
| `run_02/R2_before.osi` | `58e976dd42e2495ea3dd1fb6b1c83d07c50662d16ebaa3688a0dbdd8a407d067` |
| `run_02/R2_deflection.png` | `55410fe64f9a15af84001f2927f2e8cad6873db1f08a1093d75c7d4f5d49fab8` |
| `run_02/R2_report.pdf` | `d940a246e0699a0deec86e1b7138f4720329a973c27e86a02012639317596dc7` |
| `run_02/R2_result.png` | `ddb5a99163b8daf534f1f0df544380929c3aa06269541a903fde7f4af24e602d` |
| `run_02/input_after.json` | `b2e35b1ad78f4966c1dc89d7c051793d8442bcd41e0e838d94b15f5d4ea791e2` |
| `run_02/input_before.json` | `c45385effeed6ddc8e719a18989d0eaa78db2eb06f31d9e03d385ec07af6aa01` |
| `run_02/output_after.json` | `85fd5efa93ba6a4553db2aabe4315da7182d05fbcb76aa0aa98b0e6837d74298` |
| `run_02/output_before.json` | `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a` |
| `run_02/runtime_properties.json` | `25b76324070c30ff5d2aec7a5e2ab60dc196f65f82a82f5679ae32c4803eda0f` |
| `run_02/status.json` | `f6a7d3d582d76884c6bff0ce0f084f2e79c24e2ac45244fbbf6e3063dd903824` |
| `run_03/R3_after.osi` | `26c79477e53f969b434e5ce6ced22954c3249ce9b103652e8fe13cb920502fef` |
| `run_03/R3_before.osi` | `26c79477e53f969b434e5ce6ced22954c3249ce9b103652e8fe13cb920502fef` |
| `run_03/R3_deflection.png` | `07eeb49a5e92f6dc0dfd4b338b8ada2a3f9661a63bd5d6e07fb0c502dbcce614` |
| `run_03/R3_report.pdf` | `4843110e713a883a36ac7800bc345674db918438129685f28afbcde97112df02` |
| `run_03/R3_result.png` | `789bf874c24a6d53c6ea79b10ca41ec5420a36de1ef2a4b8f04f3d12204ab0c1` |
| `run_03/input_after.json` | `8b8e93d31134b8871669efbf73666fd5fdf29a1c2bea0bca230d5bde2e3f7db6` |
| `run_03/input_before.json` | `92e05c3034da738a76c2190aea1eba2df1e6f06151b9fa6a8249a7f48bbb2af6` |
| `run_03/output_after.json` | `8a2e90b6c34d931e1f9df97cfb5090b07ed1159a8f30346b86f4d83546886e0b` |
| `run_03/output_before.json` | `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a` |
| `run_03/runtime_properties.json` | `c1dde83a0d5850246e914fc2e12ea425e305a60d905221f73f17ff623a3e249c` |
| `run_03/status.json` | `ee2f3f91cbe6b778b716b366ad4b4c03c40b29ce6e47b56e86709fd4f93c840b` |
| `session.json` | `f51777a21be2330359195a4dc9f379fd0024a3b1e8d9aba80c38ebbcb6626dce` |
| `source.json` | `64d5a2013c6f335d672f78fa324c835621cec0726fb9c152c112292216cb504d` |

## Appendix — Exact saved-input differences

Numeric strings were normalized only for this comparison; original files were preserved.

### R1

| Key | Saved OSI | Captured input before Design |
|---|---|---|
| `member_properties.girder_details.material_properties.modulus_of_elasticity_zy` | `0.00102917` | `0.00103` |
| `member_properties.girder_details.material_properties.modulus_of_elasticity_zz` | `0.01198239` | `0.012` |
| `member_properties.girder_details.material_properties.plastic_modulus_zuy` | `0.00155905` | `0.00156` |
| `member_properties.girder_details.material_properties.plastic_modulus_zuz` | `0.01319764` | `0.0132` |
| `member_properties.girder_details.section_properties.area` | `0.02388012` | `0.0239` |
| `member_properties.girder_details.section_properties.iy` | `0.0002161251` | `0.000216` |
| `member_properties.girder_details.section_properties.iz` | `0.0083277576` | `0.00833` |
| `member_properties.girder_details.section_properties.mass` | `187.459` | `187.0` |
| `member_properties.girder_details.section_properties.radius_gyration_y` | `0.095134` | `0.0951` |
| `member_properties.girder_details.section_properties.radius_gyration_z` | `0.590535` | `0.591` |
| `member_properties.girder_details.section_properties.torsion_constant_it` | `1.641083e-06` | `1.64e-06` |
| `member_properties.girder_details.section_properties.warping_constant_iw` | `0.00010176522202` | `0.000102` |
| `typical_section.crash_barrier.area` | `302282.768` | `0.3023` |
| `typical_section.crash_barrier.load` | `7.557` | `7.56` |
| `typical_section.railing.load_value` | `1.4715` | `6.806` |
| `typical_section.railing.width` | `0.0` | `0.275` |
| `typical_section.wearing_course.density` | `24.0` | `25.0` |

### R2

| Key | Saved OSI | Captured input before Design |
|---|---|---|
| `member_properties.girder_details.material_properties.modulus_of_elasticity_zy` | `0.00054598` | `0.000546` |
| `member_properties.girder_details.material_properties.modulus_of_elasticity_zz` | `0.00631607` | `0.00632` |
| `member_properties.girder_details.material_properties.plastic_modulus_zuy` | `0.00082696` | `0.000827` |
| `member_properties.girder_details.material_properties.plastic_modulus_zuz` | `0.00695265` | `0.00695` |
| `member_properties.girder_details.section_properties.area` | `0.01559201` | `0.0156` |
| `member_properties.girder_details.section_properties.iy` | `9.28159e-05` | `9.28e-05` |
| `member_properties.girder_details.section_properties.iz` | `0.0035369979` | `0.00354` |
| `member_properties.girder_details.section_properties.mass` | `122.3973` | `122.0` |
| `member_properties.girder_details.section_properties.radius_gyration_y` | `0.077154` | `0.0772` |
| `member_properties.girder_details.section_properties.radius_gyration_z` | `0.476284` | `0.476` |
| `member_properties.girder_details.section_properties.torsion_constant_it` | `7.03629e-07` | `7.04e-07` |
| `member_properties.girder_details.section_properties.warping_constant_iw` | `2.837086246e-05` | `2.84e-05` |
| `typical_section.crash_barrier.area` | `302282.768` | `0.3023` |
| `typical_section.crash_barrier.load` | `7.557` | `7.56` |
| `typical_section.railing.load_value` | `1.4715` | `6.806` |
| `typical_section.railing.width` | `0.0` | `0.275` |
| `typical_section.wearing_course.density` | `24.0` | `25.0` |

### R3

| Key | Saved OSI | Captured input before Design |
|---|---|---|
| `member_properties.girder_details.material_properties.modulus_of_elasticity_zy` | `0.00102917` | `0.00103` |
| `member_properties.girder_details.material_properties.modulus_of_elasticity_zz` | `0.01198239` | `0.012` |
| `member_properties.girder_details.material_properties.plastic_modulus_zuy` | `0.00155905` | `0.00156` |
| `member_properties.girder_details.material_properties.plastic_modulus_zuz` | `0.01319764` | `0.0132` |
| `member_properties.girder_details.section_properties.area` | `0.02388012` | `0.0239` |
| `member_properties.girder_details.section_properties.iy` | `0.0002161251` | `0.000216` |
| `member_properties.girder_details.section_properties.iz` | `0.0083277576` | `0.00833` |
| `member_properties.girder_details.section_properties.mass` | `187.459` | `187.0` |
| `member_properties.girder_details.section_properties.radius_gyration_y` | `0.095134` | `0.0951` |
| `member_properties.girder_details.section_properties.radius_gyration_z` | `0.590535` | `0.591` |
| `member_properties.girder_details.section_properties.torsion_constant_it` | `1.641083e-06` | `1.64e-06` |
| `member_properties.girder_details.section_properties.warping_constant_iw` | `0.00010176522202` | `0.000102` |
| `typical_section.crash_barrier.area` | `302282.768` | `0.3023` |
| `typical_section.crash_barrier.load` | `7.557` | `7.56` |
| `typical_section.railing.load_value` | `1.4715` | `6.806` |
| `typical_section.railing.width` | `0.0` | `0.275` |
| `typical_section.wearing_course.density` | `24.0` | `25.0` |

