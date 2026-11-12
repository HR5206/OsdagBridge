# T05 — Additional geometry and component-output review

**Packaged evidence:** [evidence/T05/](../evidence/T05/). File names below refer to this folder or its recorded session subfolder.


**Test date:** 10 November 2026  
**Status:** Inconclusive for the intended 300 mm deck / 75 mm wearing-course design. Component displays and the exported report were reviewed, but the input screenshots do not match the saved and reported geometry. My archive contains no recorded design-call dictionaries.

## Purpose

I intended to keep the 25 m custom-material bridge configuration and change the deck thickness to 300 mm and the concrete wearing-course thickness to 75 mm. I also inspected the girder, deck, cross-bracing, end-diaphragm and stiffener result views.

The screenshots show the intended additional inputs, but the saved files and result views show a different configuration. I have preserved this attempt rather than marking the intended scenario as completed or assuming that the software ignored a correctly committed setting. I investigated the divergence in the separate T05B and T05C follow-ups.

## Evidence I retained

`t05.7z` contains `session_20261110_202805_071320` with two OSI files, eleven screenshots, a PDF report, its LaTeX source and session/source metadata. The session started at 20:28:05 local time (UTC+05:30), process ID 26392. It records Windows 11, Python 3.12.16 and repository commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. Git status lists only the untracked evidence directories.

There is no `run_01` directory, `input_before.json`, `output_after.json`, `runtime_properties.json` or `status.json` in this archive. The session metadata proves that the recorder launcher started; it does not prove that this launcher captured the calculation associated with the screenshots and PDF. I have not assigned an engine duration, exception-free outcome or runtime-dictionary pass to T05.

The report has 58 physical pages and the project title “T05 Highway Bridge Test.” Its PDF metadata records creation at 20:38:50 on 10 November 2026. Export time does not establish when its underlying calculation ran.

## Input comparison

| Parameter | Intended / visible input evidence | Saved OSI evidence | Result / report evidence |
|---|---|---|---|
| Span | Intended 25 m | 25 m | Report: 25 m |
| Carriageway width | Screenshot: 7.50 m | 7.5 m | Report: 7.5 m |
| Deck thickness | Screenshots: **300 mm** | **250 mm**, before and after | Deck result: **250 mm**; report physical pages 3 and 9: **250 mm** |
| Wearing-course thickness | Screenshot: **75 mm** | **50 mm**, before and after | Report physical page 9: **50 mm** |
| Wearing-course density | Screenshot: **25.00 kN/m³** | **24.0 kN/m³** | Runtime value unavailable |
| Girder spacing | Input-section image: **2.15 m** | See exact saved configuration | Report: **2.1 m** |
| Deck overhang | Input-section image: **1.07 m** | See exact saved configuration | Deck result: **1050 mm**; report: **1.05 m** |
| Skew | Intended 0°, no basic-input screenshot captured | **null** | Report field blank |
| Median / footpath | Intended No / None | No / None | Not independently demonstrated by a basic-input screenshot |
| Design mode | Intended Optimized | Optimized | Report: Optimized |

`T05_before.osi` and `T05_after.osi` each contain 588 keys and are equal as parsed mappings. Their equality establishes saved-file stability within this pair; it does not demonstrate that the intended changes were committed or used by a calculation.

The deck/spacing/overhang differences suggest that the input preview and reviewed results represent different geometry states. Possible causes include settings not being committed, a later input reset, a different application window or an evidence-folder mismatch. These files alone do not distinguish the possible causes. I later isolated the main Save Input reset in T05B and reported it as issue #71; I have kept the original T05 attempt inconclusive.

## Custom materials in the saved files

All three steel selections retain `custom_steel_345_500`. Saved values are weight density 77 kN/m³, Fy 345 MPa, Fu 500 MPa, E 205 GPa, G 78.8 GPa, Poisson ratio 0.3 and thermal coefficient 11.7 × 10⁻⁶/°C.

The deck retains `custom_concrete_45_3.5`, density 25.5 kN/m³, fck 45 MPa, fctm 3.5 MPa, Ecm 35 GPa and thermal coefficient 10.5 × 10⁻⁶/°C. The deck result screenshot also displays this grade name. This supports retention in the saved data and selected display labels; no T05 runtime object is available to verify use of every property.

## Component observations

### Girder and CAD

`03_overview_a.png` is the Girder 1 / SW **Details** view, rather than the main utilization summary. It shows the custom steel grade, welded slender section, 1390 mm depth, 8 mm web, and top/bottom flange widths of 420 mm with 18 mm thickness. It lists a mass near 187 kg/m and area near 0.0239 m².

`03_overview_b.png` shows a rendered bridge CAD model. A static image establishes rendering, but not rotation responsiveness or precise model dimensions. I did not record a separate T05 confirmation of rotation or plot interaction in this archive.

The report's physical page 10, Table 2.7, labels the girder dimensions as 1.39 mm, 0.008 mm, 0.42 mm and 0.018 mm. These conflict with the displayed 1390/8/420/18 mm values by a factor of 1000. This repeats the report-unit finding already identified in the earlier cases. The earlier source diagnosis concerned appending mm to metre-valued post-design fields; the report formatting and data-unit contract need correction together.

### Deck

`04_deck_results_a.png` displays a 250 mm slab and 1050 mm overhang, so this result cannot demonstrate the intended 300 mm slab scenario.

| Reinforcement position | Yield strength | Bar diameter | Spacing | Clear cover | Displayed area |
|---|---:|---:|---:|---:|---:|
| Top | 500 MPa | 12 mm | 195 mm | 50 mm | 580 |
| Bottom | 500 MPa | 12 mm | 185 mm | 50 mm | 611 |
| Overhang | 500 MPa | 12 mm | 80 mm | 50 mm | 1414 |

The screenshot labels area in mm²; the report uses mm²/m for reinforcement area. I have preserved this distinction rather than silently assuming the two labels have the same dimensional meaning.

The visible deck utilization bars include sagging 90%, hogging 71%, overhang flexure 93%, one-way shear 76%, bottom crack width 69% and top crack width 55%. Selected report values agree at displayed precision:

| Quantity | GUI | Report evidence |
|---|---:|---|
| Bottom reinforcement | 12 @ 185, area 611 | Physical pages 40–41: 12 @ 185 mm, 611 mm²/m |
| Top reinforcement area | 580 | Physical page 41: 580 mm²/m |
| Sagging utilization | 90% | Physical page 46: 44.58 / 49.76 = approximately 0.90 |
| Hogging utilization | 71% | Physical page 46: 33.43 / 47.29 = approximately 0.71 |
| Overhang flexure utilization | 93% | Physical page 46: 101.57 / 109.50 = approximately 0.93 |
| One-way shear utilization | 76% | Physical page 40: 86.64 / 114.11 = approximately 0.76 |
| Bottom crack utilization | 69% | Physical page 40: 0.2065 / 0.30 = approximately 0.69 |

Physical page 41 flags clear cover as FAIL (50 mm provided versus the report's stated 75 mm minimum), but immediately below says all reinforcement provisions satisfy strength and detailing requirements. This is a confirmed contradiction within the report wording. It does not by itself validate the cited cover requirement; that would require an independent code/exposure-condition check. The summary sentence should be derived from the actual checks rather than unconditional text.

### Cross bracing

The screenshots show X-bracing, bolted double angles, designation 40 × 40 × 3, and 12.500 m spacing. The visible member is B1M1 between G1 and G2. Its check table reports:

| Check | Force, kN | Capacity, kN | Displayed utilization | Status |
|---|---:|---:|---:|---|
| Diagonal tension | 3.783 | 45.00 | 0.080 | PASS |
| Diagonal compression | 6.151 | 18.16 | 0.570 | PASS |
| Chord tension | 3.297 | 45.00 | 0.070 | PASS |
| Chord compression | 5.360 | 22.14 | 0.490 | PASS |

Report Table 5.25 on physical page 43 repeats the G1–G2 compression demand, capacity and utilization values. Thus the GUI and report agree on what is displayed, but the compression arithmetic is inconsistent: 6.151/18.16 ≈ 0.339, not 0.570; 5.360/22.14 ≈ 0.242, not 0.490. The report's overall table on physical page 46 uses a different compression demand of 10.35 kN, which does produce approximately 0.57 with 18.16 kN capacity. This suggests mixed force/check selection, but the precise mapping needs source and output-dictionary tracing before naming the incorrect value.

### End diaphragm

The files named `06_end_stiffner_results_a.png` and `_b.png` show the **End Diaphragm** tab, not bearing stiffeners. I retain their original filenames and identify their actual content here.

The visible configuration uses two end diaphragms, cross-bracing type, bolted X-bracing and double angles 40 × 40 × 3. The E1M1 table repeats the four forces, capacities, utilizations and PASS labels listed above. Rows for E1M2 are partly visible. Table 5.28 on physical page 45 repeats the same G1–G2 compression values. I have not inferred that identical bracing and diaphragm values are inherently wrong; the relevant loading and mapping must be checked.

### Stiffeners

`07_stiffener_results.png` shows G1M1 details:

| Type | Grade | Thickness | Width | Spacing |
|---|---|---:|---:|---:|
| Intermediate | custom_steel_345_500 | 10 mm | 205 mm | 2030 mm |
| Bearing | custom_steel_345_500 | 10 mm | 205 mm | 100 mm |
| Longitudinal | NA | NA | NA | NA |

This confirms displayed section data and the preview. It is not evidence that every stiffener strength check passes. The report executive summary explicitly includes a failed intermediate-stiffener leg-limit check. Longitudinal entries are recorded as not applicable in this view, not as a crash or missing-result defect.

## Overall report status

The generated report states an overall failed design, a maximum girder utilization of approximately 2.00 and fatigue as the governing check. It reports live-load deflection 25.164 mm against approximately 31.2 mm, and total-load deflection 55.321 mm against approximately 41.7 mm, with the latter marked FAIL. These values agree with the earlier 25 m baseline results but do not establish a new 300/75 run.

The successful observations in this attempt are the availability of component result views, CAD rendering, retention of custom property values in the saved OSIs and several GUI/report numerical agreements. The unresolved items are input-to-result consistency, runtime dictionary capture and full component calculation validation.

## Follow-up completed in T05B and T05C

I retained this attempt unchanged. In T05B, I checked the committed 300 mm deck and 75 mm wearing-course values, then isolated the main Save Input action. The saved file reverted to 250/50. T05B contains the detailed comparison and source-function reproduction.

In T05C, I used direct Design after saving Additional Inputs and captured a new run folder, deck-result screenshot and report. That follow-up verified 300/75 through execution. The eleven T05 component screenshots remain evidence of their original displayed state.

I reported the isolated save-path defect in [issue #71](https://github.com/Nidhikhare12/OsdagBridge/issues/71). Related report findings are linked in the final [issue register](../issues/LIVE_ISSUES.md). This later reporting does not turn the inconclusive T05 run into a successful 300/75 test.

## Original evidence manifest

Paths are relative to my T05 session folder. These hashes identify the unmodified attachments.

| File | SHA-256 |
|---|---|
| `01_deck_input.png` | `148b3a4f6e5a7fe16d245d9cafedf72a4a66a5be85b9001250cf46afab46d922` |
| `02_wearing_course_input.png` | `ca9158c51f1defa466d03fd0d9ed9a689721a70b9ed3532cc558cf012093114e` |
| `03_overview_a.png` | `3e730aada373e591e7b3d298441e2e584b980bbf207783d97f17cc47e75b7a3d` |
| `03_overview_b.png` | `6a4c6f996e52d0c8aaf4d60a28049af79f642260dbcff60d3bc511813b5e4c56` |
| `04_deck_results_a.png` | `5e7283bf9d5b101cd9b40c990151071055c901ff7f762c090022957c74ef3c73` |
| `04_deck_results_b.png` | `7f6ab2b0b7bd4ba2ba323fe6ed306cda0499f46735d3174326161ba6db4ea69a` |
| `05_cross_bracing_results_a.png` | `1dcb868b720eb386cd5fcd58e88c2d1a1e023e82db3542c3954e94f1948d0d02` |
| `05_cross_bracing_results_b.png` | `abdfdbeb8f7f2009551c6c688fc49787834b941647eb18da366b00e6dfb361af` |
| `06_end_stiffner_results_a.png` | `c4770fa681ba5d2aaf4857ac56573fba4ac536ac69e0d1ed058c6056830d61c7` |
| `06_end_stiffner_results_b.png` | `f7f94b075ae3b161bf1ef219fd868874cf80dddc327baa14648ab41bdcdeb137` |
| `07_stiffener_results.png` | `62413e93e0ea6b390592c263ad36a57db2c289e557c5c2fef9f4882709608924` |
| `T05_after.osi` | `ae3038533a1d54aa997d900530d4bb00facb8994635c7d919c9c118de44d9a7b` |
| `T05_before.osi` | `ae3038533a1d54aa997d900530d4bb00facb8994635c7d919c9c118de44d9a7b` |
| `T05_design_report.pdf` | `4aaff7a0a19c182dd9ecc683bd59f95b06c20f1733dc86aad3c79b649209c096` |
| `T05_design_report.tex` | `c350cf528663ef2ff3cd0011c9200076cefd2ebbfd255bf63318068cc8eecbb8` |
| `session.json` | `f83dc841da43aaedba88ddc4eb40d443d01871f1e921ebdf1019b0d649ea5a28` |
| `source.json` | `64d5a2013c6f335d672f78fa324c835621cec0726fb9c152c112292216cb504d` |
