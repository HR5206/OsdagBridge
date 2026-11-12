# T05C — Direct design with a 300 mm deck and 75 mm wearing course

**Packaged evidence:** [evidence/T05C/](../evidence/T05C/). File names below refer to this folder or its recorded session subfolder.


**Test date:** 11 November 2026  
**Functional result:** PASS for the tested input-retention path. The intended thicknesses reached the backend and agree with the output dictionary and report.  
**Engineering result:** FAIL overall, as reported by the application.  
**Relationship to T05B:** This is a successful direct-design comparison, not a fix or a successful retest of Save Input.

## Purpose and sequence

I tested whether Design could use my custom deck and wearing-course thicknesses when I skipped the main Save Input action that reset them in T05B. I retained the 25 m custom-material bridge, entered the additional thicknesses, saved them inside the Additional Inputs dialog and proceeded to Design following the direct-design workflow.

The screenshots show deck thickness 300 mm, wearing-course thickness 75 mm and the Additional Inputs “Inputs saved successfully” message. The recorder establishes the actual values at the backend boundary. Its completed run and the resulting deck screen provide stronger evidence than the input preview alone.

I did not export an OSI for this case because the main Save Input action was the defect under investigation. I used direct Design after saving the Additional Inputs dialog. The recorder's complete input dictionaries preserve the executed parameter combination instead. Earlier OSI evidence remains available in T01–T05B.

## Environment and execution record

| Item | Recorded value |
|---|---|
| Evidence archive | t05c.7z |
| Session directory | session_20261111_075351_337157 |
| Repository commit | d74f56dd7f22925fb8148cabf5740ed8d1e39ff3 |
| Platform | Windows-11-10.0.26300-SP0 |
| Python | 3.12.16, conda-forge |
| Process ID | 1872 |
| Session start | 07:53:51, UTC+05:30 |
| Design-call start | 07:58:41, UTC+05:30 |
| Design-call finish | 07:59:13, UTC+05:30 |
| Core-call duration | 31.4816 seconds |
| Recorder outcome | engine_returned |
| Captured exception | None |
| Capture errors | Empty list |
| Before/after input key counts | 588 / 588 |
| Completed output key count | 1,078 |
| Output before calculation | Empty dictionary |

Git status records untracked `FOSSEE_Testing/` and `screening/` directories and no tracked changes. The recorder wraps the original design call in memory; it does not change solver inputs or logic. The recorded duration excludes later GUI rendering and PDF export and should not be treated as a benchmark against earlier runs.

The PDF contains 58 physical pages. Its metadata records creation at 08:02:17 local time on 11 November 2026. Page references below refer to physical PDF pages, including the cover.

## Exact case configuration

The full 588-key combination is retained in `run_01/input_before.json`. Selected inputs are:

| Input | Value |
|---|---|
| Span | 25 m |
| Carriageway width | 7.5 m |
| Design mode | Optimized |
| Skew | 0° |
| Median / footpath | No / None |
| Physical girder count | 4 |
| Girder spacing | 2.1 m |
| Overall bridge width in input | 8.4 m |
| Deck overhang | 1.05 m |
| Deck thickness | 300 mm |
| Wearing course | Concrete, 75 mm |
| Wearing-course weight density | 25.0 kN/m³ |
| Crash-barrier width in input | 0.45 m |
| Girder / cross-bracing / end-diaphragm material | custom_steel_345_500 |
| Deck material | custom_concrete_45_3.5 |

### Custom properties

| Property | Steel, all three selected component groups | Concrete deck |
|---|---:|---:|
| Weight density, kN/m³ | 77 | 25.5 |
| Yield / ultimate strength, MPa | 345 / 500 | Not applicable |
| Elastic modulus, GPa | 205 | Ecm = 35 |
| Shear modulus, GPa | 78.8 | Not specified |
| Poisson's ratio | 0.3 | Not specified |
| fck / fctm, MPa | Not applicable | 45 / 3.5 |
| Thermal coefficient, ×10⁻⁶/°C | 11.7 | 10.5 |

All material keys remain equal between the before- and after-call input dictionaries. This establishes retention, not correct downstream use of every property.

## Input-to-output verification

| Quantity | UI evidence | Input before Design | Input after Design | Output dictionary | PDF / result screen |
|---|---|---:|---:|---|---|
| Deck thickness | 300 mm | 300 | 300 | `typical_section.deck_thickness = 300`; `design_results.slab_thickness_mm = 300.0`; `deck_design_results.deck_thickness = "300"` | Report pp. 3, 9, 37: 300 mm; Deck Design screen: 300 mm |
| Wearing-course thickness | 75 mm | 75 | 75 | `typical_section.wearing_course.thickness = 75` | Report p. 9: 75 mm |
| Wearing-course density | 25.0 kN/m³ | 25.0 | 25.0 | `typical_section.wearing_course.density = 25.0` | No separate numerical load check established from the screenshot |
| Deck overhang | 1.05 m in preview | 1.05 m | 1.05 m | `deck_design_results.deck_overhang = "1050"` mm | Deck screen: 1050 mm; report: 1.05 m |
| Concrete grade | Custom grade shown in results | custom_concrete_45_3.5 | Same | Same in runtime and deck results | Same grade in result screen and report |

The thickness comparison passes for this actual call. Unlike T05, the result is now tied to a numbered recorder run with complete dictionaries.

There are 35 changed input entries during the design call, involving girder dimensions and resolved thickness selections. These correspond to the previously observed metre conversion and optimization path. The targeted deck/wearing-course fields and all custom material fields remain unchanged. Their retention is therefore not inferred merely from an identical screenshot.

## Deck result verification

The result screenshot shows the updated 300 mm slab. Its reinforcement values agree with the captured `deck_design_results` dictionary:

| Position | Bar diameter | Spacing | Clear cover | Displayed/provided area | Agreement |
|---|---:|---:|---:|---:|---|
| Top | 12 mm | 165 mm | 50 mm | 685 | GUI and dictionary match; report p. 41 confirms area 685 mm²/m |
| Bottom | 12 mm | 230 mm | 50 mm | 492 | GUI, dictionary and report pp. 40–41 match |
| Overhang | 12 mm | 105 mm | 50 mm | 1077 | GUI and dictionary match; captured deck-check text confirms 1077 mm²/m |

All three displayed reinforcement yield strengths are 500 MPa. The GUI labels area as mm², whereas the detailed calculation text and report use mm²/m. This label difference should remain explicit in the final report.

The three visible utilization bars also agree with dictionary values after rounding:

| Deck check | Output ratio | GUI | Report comparison |
|---|---:|---:|---|
| Bottom flexure / sagging | 0.866 | 87% | p. 38: 44.18 / 51.01 ≈ 0.866 |
| Top flexure / hogging | 0.470 | 47% | p. 38: 33.13 / 70.45 ≈ 0.470 |
| Interior one-way shear | 0.646 | 65% | p. 40: 86.23 / 133.45 ≈ 0.646 |

The output bottom crack width is 0.2221 mm against a 0.3 mm limit, matching the report on page 40. These are consistency checks between representations, not independent validation of the full structural calculation method.

## Engineering outcome and updated results

The core call completed, but `design_results.overall_status` is `FAIL`. The captured maximum ratio is 2.1776; the report executive summary rounds it to 2.18 and identifies fatigue as governing.

| Captured summary field | Value, % |
|---|---:|
| util.flexure | 25.24 |
| util.shear | 60.54 |
| util.interaction | 25.63 |
| util.ltb | 63.23 |
| util.long_trans_shear | 24.72 |
| util.fatigue | 217.76 |
| util.stress_limitation | 35.02 |
| util.deflection_crack | 54.16 |

The report's per-girder deflection summary on page 21 uses maximum live-load deflection 25.163 mm and maximum total-load deflection 60.608 mm. These agree with the `.G1`–`.G4` output fields. It marks total-load deflection as FAIL against approximately 41.7 mm.

The separate unsuffixed summary fields contain live deflection 10.305 mm and total deflection 22.565 mm. As in earlier cases, these do not represent the same numerical summary as the per-girder maxima. I have retained both values and do not assume that the lower summary proves the total-deflection check passes.

Compared with T03's 25 m / 250 mm / 50 mm run, selected values changed: girder moment capacity 6907.037 → 7314.011 kNm, maximum total deflection 55.321 → 60.608 mm and fatigue ratio 1.9985 → 2.1776. These changes show the captured results are not simply the earlier unchanged output. Two geometric parameters changed together, so this comparison does not isolate each parameter's individual effect.

## Remaining defects and cautions

### Steel density still differs at runtime

The input specifies 77 kN/m³, while the runtime steel object contains `rho = 78500` N/m³, equivalent to 78.5 kN/m³. This repeats the issue #20 finding. E, Fy, Fu and Poisson's ratio do match the selected values after unit conversion.

### Custom concrete density is retained but not used consistently

The input retains deck density 25.5 kN/m³. The captured deck-check text and report p. 37 use slab self-weight 7.36 kN/m². For the entered density and a 0.300 m slab, the direct weight-density calculation is 25.5 × 0.300 = 7.65 kN/m².

Source inspection of `src/osdagbridge/core/bridge_types/plate_girder/deckdesign.py` around lines 516–517 shows a separate deck-design load path obtaining concrete unit weight from `IRC6_2017.cl_203_dead_load()["concrete_cement_reinforced"] * 9.81`, rather than the custom deck-density input. This identifies another relevant location when extending the existing custom-deck-density issue #41, whose earlier description concerns the analysis load-creation path.

The suggested correction is to pass the validated custom weight density explicitly into this deck-design calculation, using consistent kN/m³ units. A focused regression check should require 7.65 kN/m² for a 300 mm slab with density 25.5 kN/m³. The analysis and deck-design paths should use the same authoritative property. No fix has been implemented or tested here.

### Runtime barrier width still differs

The input width is 0.45 m; the runtime deck-layout object contains 0.5 m. This repeats the previously identified default-width substitution. T05C does not quantify its structural consequences.

### Report wording contradicts its own cover check

The deck result dictionary recommends 75 mm cover and identifies the exposure as “Extreme,” while my entered top/bottom cover is 50 mm. The report p. 41 marks the cover row FAIL but then states that all reinforcement provisions satisfy strength and detailing requirements. The contradiction in the report wording remains. I have not independently validated how the exposure category or required cover was selected.

## What this case proves

T05C demonstrates one successful path from the saved Additional Inputs dialog to Design: the 300/75 configuration reaches the backend, survives execution and appears in the output/report. The core call returned without a captured exception.

T05B's separate Save Input defect remains open. Bypassing that action in one successful run does not fix saved-file persistence, prove that all Design paths preserve custom inputs, or establish that the complete bridge design is adequate.

The output includes girder design, deck design, cross-bracing and end-diaphragm result dictionaries. This case focuses its detailed GUI comparison on the deck; I retained the broader component screenshots in T05. I did not capture new CAD/plot screenshots or record an interaction confirmation for T05C, so I have not marked those interactions as passed in this case. Earlier evidence covers those interactions for other cases.

## Evidence inventory

| Evidence | Purpose |
|---|---|
| 01_deck_thickness_change.png | Deck input and section preview showing 300 mm |
| 02_wearing_course_thickness_change.png | Concrete wearing course, density 25, thickness 75 mm |
| 03_inputs_saved_status.png | Save confirmation inside Additional Inputs; not an OSI-export confirmation |
| 03_deck_thickness_result.png | Deck result at 300 mm with reinforcement and utilization values |
| session.json / source.json | Runtime environment, launcher identity and tested source revision |
| run_01/input_before.json / input_after.json | Exact executed input state and post-call retention |
| run_01/output_before.json / output_after.json | Empty pre-run output and completed result dictionary |
| run_01/runtime_properties.json | Selected runtime material and geometry objects |
| run_01/status.json | Successful core return, timing and absence of captured errors |
| T05C_report.pdf | Exported report for comparison with captured output |

**Conclusion:** The targeted direct-design input-retention check passes. The overall structural design fails, and previously identified material-density, barrier-width and reporting concerns remain documented. This completes the intended 300/75 follow-up without erasing the failed Save Input case.

## Evidence checksums

Paths are relative to the extracted t05c folder.

| File | SHA-256 |
|---|---|
| `01_deck_thickness_change.png` | `4797ae8fc98aac8ed840039b5b9e41a54454c7d2a9bddf7e08ad6163419e5c11` |
| `02_wearing_course_thickness_change.png` | `a8eff21df17ac587eb261874258427fd065b2a2ee0f1a5b1c5ba4edf7fcfa122` |
| `03_deck_thickness_result.png` | `b1261b72df9e55b6febeb1c3c14a2f263c4bd7bfb46ddd5b59f47b348fd1eab8` |
| `03_inputs_saved_status.png` | `a185d39e088b956e61d36fbb96320a10cefcd7e236fa410f808bd2cfe157d55b` |
| `T05C_report.pdf` | `a4dd491e34f4b207c6ce371c44430a25e2463193aba72fcaf7624ef6bec5a402` |
| `session_20261111_075351_337157/run_01/input_after.json` | `f20e6bdc7af119e527c36da965d82775cb55cfa586f2c915252eab043bbd88fa` |
| `session_20261111_075351_337157/run_01/input_before.json` | `54584deb3e37981c4c809e10cade7d5178c3bf42bf454398370e46f43af3843a` |
| `session_20261111_075351_337157/run_01/output_after.json` | `d957b2e63ba5622d64663228b4c7330bc11e74a519664b2eecb18db11d69f6f7` |
| `session_20261111_075351_337157/run_01/output_before.json` | `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a` |
| `session_20261111_075351_337157/run_01/runtime_properties.json` | `c1dde83a0d5850246e914fc2e12ea425e305a60d905221f73f17ff623a3e249c` |
| `session_20261111_075351_337157/run_01/status.json` | `94abe075d5de296530b12e632dac790bb4b468a512f2be4c57378ba7bbbfe17c` |
| `session_20261111_075351_337157/session.json` | `f49fc8d6f8e0407d18e5fc058a5c2c0b908936070d6d0055e2a30ecba7c415d7` |
| `session_20261111_075351_337157/source.json` | `64d5a2013c6f335d672f78fa324c835621cec0726fb9c152c112292216cb504d` |
