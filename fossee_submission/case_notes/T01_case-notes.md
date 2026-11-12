# T01 — Desktop baseline: execution completed, design checks failed

**Tester:** Harish Raghav S  
**Test date:** 8 November 2026  
**Evidence reviewed:** six screenshots, the saved input file and the generated design report  
**Overall finding:** The application completed the run and generated CAD, analysis plots and a PDF. The PDF contains failed design checks and several inconsistencies. I have therefore recorded execution, structural-design status and reporting consistency separately.

## 1. What I tested

I used this case to establish a desktop baseline for a straight, 25 m highway bridge in Chennai. I used a 7.5 m carriageway, four main girders, no median and no footpath. The selected design mode was Optimized. The visible steel grades were E 350A for the girder, cross bracing and end diaphragm, and the concrete deck grade was M40.

My aim was to check input retention, completion of the design workflow, generation of the bridge model and analysis plots, and consistency of the exported report. This was one desktop run, not a three-run state-persistence test. I have not treated the material selections as a demonstrated custom-material test.

## 2. Run record

| Item | Recorded evidence |
| --- | --- |
| Application | OsdagBridge, short-span plate-girder bridge module |
| Project | Analysis and Design of 25 m Composite Steel Girder Bridge |
| Location | Chennai (Minambakkam) (A), Tamil Nadu |
| Input file | `T01_inputs.osi`, containing 576 top-level saved fields |
| Design mode | Optimized |
| Completion timestamp | 2026-11-08 18:25:28, as displayed in the application log; timezone not displayed |
| Total solution time | 125.99 seconds, as reported by the application |
| Completion evidence | `ANALYSIS COMPLETE`; progress header `STAGE 14/14 COMPLETE : 3D CAD & DRAWING GENERATION [100%]` |
| Last logged stages | Stage 6 deck slab design completed, Stage 7 transverse member design completed, Stage 8 CAD and drawing generation completed |
| Desktop build / commit | Not recorded in the submitted evidence |
| Operating-system version | Not recorded in the submitted evidence |
| Starting state and exact start time | Not established by the screenshots; I have not inferred an exact start time from the duration |
| Application crash | No crash is shown; the completion log, model and report establish that this attempt reached its outputs |
| PDF | 58 physical pages, with internal report numbering through page 57; the cover also carries page 1 |

The progress header and detailed log use different stage counts (14/14 versus Stage 8). I have retained those labels as observed rather than rewriting them into a single numbering scheme. They may represent different progress groupings.

## 3. Inputs and cross-checks

The following comparison uses the visible UI, the saved `.osi` and the PDF. The `.osi` is a saved input snapshot, not a separately captured live backend input/output dictionary. Blank evidence is described explicitly rather than treated as a match.

PDF references below use the physical page number in a PDF viewer. The printed page number is generally one lower after the cover.

| Parameter | Screenshot | Saved input | PDF | Finding |
| --- | --- | --- | --- | --- |
| Structure | Highway Bridge | Highway Bridge field preserved in full input appendix | Highway Bridge, p.8 | Visible UI/report agree |
| Location | Chennai (Minambakkam) (A), Tamil Nadu | Same display text | Same, p.8 | Match |
| Span | 25 m | `geometry.span: '25'` | 25 m, p.8 | Match |
| Carriageway width | 7.5 m | `geometry.carriageway_width: '7.5'` | 7.5 m, p.8 | Match |
| Median | No | `geometry.include_median: 'No'` | No, p.8 | Match |
| Footpath | None | `geometry.footpath: None` (text selection) | None, p.8 | Match |
| Skew | 0 degrees | `geometry.skew_angle: '0'` | 0 degrees, p.8 | Match |
| Design mode | Optimized | Optimized | Optimized for G1–G4, p.10 | Match |
| Steel grades | E 350A for girder, cross bracing and end diaphragm | E 350A for all three | E 350A for all three, p.8 | Grade labels match |
| Deck grade | M40 | M40 | M40, p.8 | Match |
| Main girders | Four shown in typical-section illustration | 4 | 4, p.9 | Consistent with illustration and saved value |
| Girder spacing | Dimension text is clipped in supplied additional-input image | 2.1 m | 2.1 m, p.9 | File/report match; not independently readable in screenshot |
| Deck overhang | Dimension text is clipped | 1.05 m | 1.05 m, p.9 | File/report match |
| Overall width | Not legibly captured | 8.4 m | 8.4 m, p.9 | File/report match; runtime mesh width not verified |
| Deck thickness | 250 mm in illustration | 250.0 mm | 250.0 mm, p.9 | Match |
| Crash-barrier width | Not captured in its property panel | 0.45 m | Not explicitly listed in reviewed input tables | Saved value only |
| Wearing-course material | Concrete | Concrete | Concrete, p.9 | Match |
| Wearing-course thickness | 50.00 mm | 50.0 mm | 50.0 mm, p.9 | Match |
| Wearing-course density | **25.0 kN/m³** | **24.0 kN/m³** | No corresponding density in the wearing-course table | **Evidence mismatch; save timing and live state need checking** |

### Saved material properties

These values come from the `.osi`. The screenshots show the grade labels, not the full property dialogs, so property-level UI retention is not yet verified.

| Property | Girder | Cross bracing | End diaphragm |
| --- | --- | --- | --- |
| Grade | E 350A | E 350A | E 350A |
| Weight density, kN/m³ | 76.4 | 76.4 | 76.4 |
| Yield strength, MPa | 350.0 | 350.0 | 350.0 |
| Ultimate strength, MPa | 490.0 | 490.0 | 490.0 |
| Elastic modulus, GPa | 200.0 | 200.0 | 200.0 |
| Shear modulus, GPa | 76.9 | 76.9 | 76.9 |
| Poisson ratio | 0.30 | 0.30 | 0.30 |
| Thermal expansion, ×10⁻⁶/°C | 11.7 | 11.7 | 11.7 |

| Deck property | Saved value |
| --- | --- |
| Grade | M40 |
| Weight density | 24.5 kN/m³ |
| Characteristic compressive strength | 40.0 MPa |
| Mean tensile strength | 3.0 MPa |
| Secant modulus | 33.0 GPa |
| Thermal expansion | 11.7 ×10⁻⁶/°C |

PDF Table 3.1, physical p.14, repeats steel density 76.4 and deck density 24.5 kN/m³. This establishes agreement in the report labels, not that the load generator used those values. The 24.5 deck density, 24.0 saved wearing-course density and 25.0 displayed wearing-course density refer to different fields and must not be conflated.

### Member settings, loading and design options

The full input appendix preserves every saved field. The main settings affecting reproduction are:

- All four girders are welded and symmetric. Saved total depth is 1390 mm, top and bottom flange widths are 420 mm, and web depth is 1355 mm. Top/bottom flange and web thickness inputs are `All`, allowing the optimized selection to differ from the input.
- Each girder has intermediate stiffeners enabled: saved outstand 205 mm, spacing 2030 mm and thickness 10 mm. Longitudinal stiffeners are disabled. Bearing-stiffener inputs specify four at each end, outstand 205 mm, spacing 100 mm and thickness 10 mm. These are input settings, not verified final stiffener dimensions.
- Cross bracing is X-Bracing with top and bottom chords enabled. Saved section selections are IS 100 × 100 × 10, Double Angle (Long Leg), with 12.5 m spacing. Final report sections are 40 × 40 × 3; because this is an optimized run, a different selected section is not by itself a defect.
- Deck reinforcement grade is Fe 500; top, bottom and side clear covers are 50 mm.
- Shear-stud inputs: count 2, diameter 20 mm, height 100 mm, transverse spacing 100 mm, yield strength 385 MPa and ultimate strength 495 MPa.
- Enabled vehicle flags: Class A, 70R wheeled, 70R tracked, 70R bogie, AA wheeled, AA tracked, SV and fatigue. No custom vehicles are saved. Live-load eccentricity is 1.2 m and the self-weight factor is 1.00.
- Location data includes latitude 12.9855, longitude 80.1689, wind speed 50 m/s, seismic zone III and zone factor 0.16. These are application data, not independently checked environmental values.
- Seismic settings include 2% damping, period 0.5 s, importance factor 1.0, response reduction factor 1 and Type I rocky/hard soil. Wind terrain is Plain Terrain, topography is Flat, and average exposed height is 10 m.
- Construction-stage design is enabled; fatigue cycles are 2,000,000. All saved ULS and SLS check toggles are enabled. The full input appendix retains the partial factors and automatic/manual settings.

## 4. Results I recorded

### Execution and model

The completion screenshot records all visible design stages finishing and a total solution time of 125.99 seconds. The CAD screenshot shows the deck, both side barriers, longitudinal girder webs, repeated stiffeners and transverse end bracing. The model was generated and displayed.

A still image cannot establish rotation responsiveness, hidden-member correctness or exact CAD dimensions. I have not marked those checks as passed. The supplied CAD image is cropped to the model and does not include the main output dock.

### Girder 1 analysis screen

The selected member is **Girder 1**, load combination **SW**, component **Major (Mz, Vy, Dy)** and display mode **Maximum Values**.

| Result | Value shown |
| --- | --- |
| Left support reaction RA | 19.32 kN |
| Right support reaction RB, numeric field | 14.17 kN |
| Right support reaction, load sketch | 19.3 kN |
| Tx | 0.00 kNm |
| My | 0.00 kNm |
| Mz | 97.32 kNm |
| Mz location in callout | x = 11.76 m |
| Fx | 0.00 kN |
| Vy | -19.32 kN, callout at x = 0.00 m |
| Vz | 0.00 kN |
| Dx | 0.00 mm |
| Dy | -3.80 mm |
| Dz | 0.00 mm |

The bending-moment plot is visible over a 0–25 m span. The top of the shear plot is visible, but its lower part and the deflection plot are outside the screenshot. I have not recorded full shear/deflection plot verification from this image.

PDF Table 4.1, physical p.18, gives SW maximum moment 97.318 kNm for G1. Its magnitude rounds to the UI value 97.32. The report places it at 13.235 m, while the UI callout says 11.76 m. These positions are symmetric about midspan to displayed precision, so a tied-extremum selection is possible; the dataset is needed before calling this a calculation error. The signed plotted moment and positive maximum field also require a documented sign/magnitude convention.

### Design-check outcome

The PDF's project overview, physical p.3, reports **Fail (Fatigue Normal Stress, Int.Stiff: Leg H limit, Fatigue Shear Stress)** and maximum utilization **2.00 (Girder)**. The completed progress bar is therefore evidence of execution completion, not an all-pass design.

| Component/check | Reported result | Evidence / qualification |
| --- | --- | --- |
| Girder fatigue | FAIL for G1–G4; UR 1.967, 1.979, 1.998, 1.998 | Table 5.12, physical p.35 |
| Total girder deflection | FAIL: G1/G4 56.278 mm, G2/G3 56.704 mm against displayed 41.7 mm limit | Table 5.9, physical p.33 |
| Live-load girder deflection | PASS: 25.461–25.793 mm against displayed 31.2 mm limit | Same table |
| Girder final section | Depth 1390 mm; flanges 420 × 18 mm; web 8 mm | Table 5.1, physical pp.23–25 |
| Intermediate stiffener | Overview lists a leg-height-limit failure | Full UI design-check evidence and runtime result mapping still needed |
| End-panel stiffeners | Individual tabulated checks marked PASS | Table 5.8; this does not override the separate intermediate-stiffener failure |
| Deck flexure | Reported PASS: sagging demand/capacity 45.94/52.23 kNm/m; hogging 34.46/40.16 kNm/m | Table 5.17, physical p.38; not independently recalculated |
| Deck overhang | Reported PASS: 101.57/108.27 kNm/m | Table 5.18, physical p.38 |
| Cross bracing | Capacity rows marked PASS, but one reported UR does not equal its displayed demand/capacity ratio | Table 5.25, physical p.43; see findings |
| End diaphragm | Capacity rows marked PASS | Table 5.28, physical p.45; raw results not independently verified |
| Shear connectors | Report includes capacity and spacing checks | No separate UI or independent check captured |

I have not classified a failed structural check alone as a software bug. The reporting and display contradictions below are separate findings.

## 5. Findings and follow-up

### T01-F01 — The report says both FAIL and “Girder design pass”

**Observed inconsistency.** Physical p.3 and pp.34–35 contain failed girder checks. Physical p.6 nevertheless states “Girder design pass,” followed by pass statements for the other components.

The source review found literal pass text in `src/osdagbridge/core/reports/executive_summary.py`, lines 233–236. The proposed correction is to render each component's status from its actual check results, with an explicit not-evaluated state for missing results. Regression coverage should include passing, failing and unavailable component results.

This source observation is from upstream commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`; my installed desktop commit is not yet recorded. It is a source-supported explanation, not a tested patch on my installation.

### T01-F02 — Girder dimensions are reported in inconsistent units

**Observed inconsistency.** Table 2.7 on physical p.10 labels depth **1.39 mm**, web thickness **0.008 mm**, flange width **0.42 mm** and flange thickness **0.018 mm**. Table 5.1 on physical p.23 gives **1390 mm**, **8 mm**, **420 mm** and **18 mm**, respectively. These differ by a factor of 1000 despite using the same unit label.

In the reviewed source, `_dim_row()` in `src/osdagbridge/core/reports/chap2.py` appends `mm` directly to values taken from the input dictionary. A proposed correction is to establish the units at the report-data boundary and convert values known to be in metres to millimetres once. Do not multiply every field indiscriminately: pre-design inputs already use millimetres. The report should distinguish requested inputs from optimized results.

### T01-F03 — Right-support reaction differs within the same analysis screen

**Observed inconsistency.** In `05_bmd.png`, RB is **14.17 kN** in the numeric field but **19.3 kN** beside support B in the sketch. This is not a rounding difference.

The reviewed `src/osdagbridge/desktop/ui/dialogs/steel_design.py` derives the numeric fields from shear-force samples (`sfd_values[0]` and `sfd_values[-2]`, lines 953–954), while the scheme uses `engine.extract_reactions()` around line 984. These different data paths are a plausible cause. A fix should make both representations use the same verified support-reaction extraction, mapping the correct support nodes and sign convention. Simply changing `[-2]` to `[-1]` without inspecting element-end ordering would not establish correctness. The underlying reaction values still need dataset verification.

### T01-F04 — Wearing-course density differs between UI and saved input

**Mismatch in submitted evidence; exact trigger not yet established.** `02_additional.png` shows Concrete, **25.0 kN/m³**, thickness **50.00 mm**. The saved key `typical_section.wearing_course.density` is **24.0**, with Concrete and 50.0 mm retained.

The evidence does not establish whether the OSI was saved before or after the displayed selection. Reopen the same wearing-course panel, capture its current value and immediately save a new OSI without changing it. If the mismatch persists, trace UI synchronization and serialization before attributing it to load computation.

### T01-F05 — Support-reaction table is empty

**Observed report omission.** Table 4.2 on physical p.21 has headings and blank rows, although reactions are shown elsewhere. The same page contains a rendered bending-moment envelope; the report also includes CAD images. This is a specific missing table, not a claim that all visualizations are absent.

Existing issue #48 concerns incomplete report sections. This observation should be checked against that issue before creating a new one.

### T01-F06 — Deflection summaries are not reconciled

**Observed difference requiring load-case/result mapping.** Tables 4.3 and 5.9 report maximum total deflection **56.704 mm** and FAIL. Table 5.29, physical p.45, instead shows a girder deflection demand **22.75 mm**, capacity **41.67 mm**, UR **0.55**, with the label `1.0 DL + 1.0 LL`.

The values may refer to different result selections, but the overall summary does not reconcile them. The source of each summary value and its load combination must be traced before proposing a numerical correction.

### T01-F07 — Cross-bracing utilization is not explained by its displayed row

**Observed arithmetic inconsistency under the report's demand/capacity definition.** Table 5.25, physical p.43, gives G1–G2 diagonal demand **6.151 kN**, capacity **18.160 kN**, UR **0.570**. Dividing the displayed demand by capacity gives approximately **0.339**, not 0.570. The end-diaphragm capacity table repeats these values.

The UR may have been taken from another governing case or check. The report needs either the matching demand/capacity pair or a clear explanation of the governing utilization. This observation alone does not establish which underlying design result is wrong.

### T01-F08 — Quantity-table values need unit and geometry reconciliation

**Report consistency follow-up.** Physical p.53 reports the crash-barrier total volume as **0.00** and total weight as **0.00**, despite the barrier geometry and load being nonzero. The saved barrier area is **302282.768**; its raw key carries no unit, so an independent area conversion is not assumed here.

The same quantity table uses girder area **0.02388 m²**, whereas Table 5.1 gives **259.52 cm²**, equivalent to **0.025952 m²**. The material take-off should identify the exact geometry used. No corrected bill of quantities is claimed from this review.

### Duplicate review and reporting status

The public GitHub issues list was checked on 8 November 2026 using all issue states. The response contained 13 issues, excluding pull requests, with no next page. Related existing reports are:

- [#44 — design completes and builds CAD when fatigue utilization exceeds 100%](https://github.com/Nidhikhare12/OsdagBridge/issues/44): relevant to the completed run with failing fatigue checks. Do not create a duplicate for that behavior.
- [#48 — generated report contains placeholder sections and missing visualizations](https://github.com/Nidhikhare12/OsdagBridge/issues/48): relevant to incomplete report sections, including the empty reaction table.

No exact issue describing F02 or F03 was found in that snapshot. F01's fixed pass text is a specific reporting problem but overlaps the reporting/status topics above; check scope before posting. This note does not claim any issue or comment has been published. Refresh the duplicate search and record the desktop commit before filing.

## 6. Evidence register

| File | What it establishes | Limitation |
| --- | --- | --- |
| `01_inputs_a.png` | Location and basic geometric inputs | Other inputs are outside the crop |
| `01_inputs_b.png` | Optimized mode and material grade selections | Detailed material properties are not displayed |
| `02_additional.png` | Typical-section illustration and wearing-course properties | Some geometry labels are clipped; most other tabs are not shown |
| `03_analysis.png` | Completion messages, visible stage progression and duration | Not a full console log or proof that all checks pass |
| `04_result_cad.png` | A rendered bridge model | Output dock, dimensional checks and interactive behavior are not captured |
| `05_bmd.png` | Girder 1 / SW numerical results and bending-moment plot | Shear plot cropped; deflection plot absent |
| `T01_inputs.osi` | Complete saved parameter combination | Capture timing and runtime dictionaries are not established |
| `T01_design_report.pdf` | Generated report, calculation summaries, CAD views and plots | Contains the documented inconsistencies |

## 7. Coverage and disposition

| Check | Disposition |
| --- | --- |
| Basic UI → saved file → report agreement | PASS for the specifically compared basic fields |
| Full workflow reaches completion | PASS for this desktop attempt |
| CAD generation | PASS for image generation/display only |
| Girder 1 / SW bending-moment plot generation | PASS for display; numerical correctness not independently validated |
| Structural design | FAIL as reported by the application; fatigue and total-deflection failures are documented |
| Internal consistency of report/display | FAIL for the explicit contradictions above |
| Full input/output dictionary verification | Not verified: live dictionaries were not supplied |
| Main output-dock status and design ratios | Not captured |
| CAD interaction and exact dimensional accuracy | Not verified |
| Custom steel and concrete retention | Not tested as a controlled custom-material case |
| Stiffener material mapping | Not independently verified; no separate stiffener material selection was captured |
| Three consecutive unlock/change/design runs | Not executed in this evidence set |
| Save/reload state preservation | Not tested |

Before changing this baseline, the useful remaining captures are the main output dock, the current wearing-course panel paired with a new saved input, and the installed source commit. These are follow-up evidence requests, not blanks for the tester to edit in this note.

## 8. My conclusion

The baseline completed and produced useful outputs, but I cannot call it a passing bridge design. The fatigue and total-deflection checks failed in the generated report. I also found contradictions in the report's status text and units, and a reaction mismatch within the analysis screen. The next case will use explicit custom steel and deck properties while keeping the geometry unchanged, so I can check whether those properties survive the design run. I will retain this baseline and its failures for comparison.

## Appendix A — Source review references

The code references below are from an assistant-assisted review of the public upstream source, separate from my desktop execution. No source change was applied to my application and no suggested fix was regression-tested. The installed desktop commit remains unverified.

- [Fixed pass statements, executive_summary.py](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/reports/executive_summary.py#L233)
- [Girder-dimension rendering, chap2.py](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/reports/chap2.py#L240)
- [Numeric reaction fields, steel_design.py](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/desktop/ui/dialogs/steel_design.py#L947)

## Appendix B — Exact saved input

The following is a verbatim text copy of the supplied `T01_inputs.osi`; YAML types and values have not been normalized. This preserves the complete parameter combination without requiring screenshots of every input tab. The original file's SHA-256 is `3fe41ea929d19937b1b995e6b71807db55016625c9a0265928ea61f1e1d8f15a`.

```yaml
bl_irc_class_sv: true
design_options.construction.stage: 'Yes'
design_options.deck.bottom_clear_cover: '50'
design_options.deck.reinforcement_bounds:
  lower: null
  upper: null
design_options.deck.reinforcement_material: Fe 500
design_options.deck.side_clear_cover: '50'
design_options.deck.top_clear_cover: '50'
design_options.shear_studs.count: '2'
design_options.shear_studs.diameter: '20'
design_options.shear_studs.height: '100'
design_options.shear_studs.transverse_spacing: '100'
design_options.shear_studs.ultimate_strength: '495'
design_options.shear_studs.yield_strength: '385'
design_options_cont.camber.mode: Default
design_options_cont.fatigue.load_cycles: '2000000'
design_options_cont.partial_factor.concrete_accidental.gamma_c_accidental: '1.20'
design_options_cont.partial_factor.concrete_basic.gamma_c_basic: '1.50'
design_options_cont.partial_factor.fatigue_load.gamma_flt: '1.00'
design_options_cont.partial_factor.fatigue_strength.gamma_mf: '1.35'
design_options_cont.partial_factor.reinforcing_steel.gamma_s: '1.15'
design_options_cont.partial_factor.shear_connectors.gamma_v: '1.25'
design_options_cont.partial_factor.ultimate_stress.gamma_m1: '1.25'
design_options_cont.partial_factor.yielding_and_buckling.gamma_m0: '1.10'
design_options_cont.sls.crack_width: true
design_options_cont.sls.deflection_control: true
design_options_cont.sls.longitudinal_shear: true
design_options_cont.sls.stress_limitation: true
design_options_cont.uls.bending_resistance: true
design_options_cont.uls.fatigue: true
design_options_cont.uls.lateral_torsional_buckling: true
design_options_cont.uls.longitudinal_shear: true
design_options_cont.uls.transverse_force: true
design_options_cont.uls.vertical_shear: true
geometry.carriageway_width: '7.5'
geometry.design_mode: Optimized
geometry.footpath: None
geometry.include_median: 'No'
geometry.skew_angle: '0'
geometry.span: '25'
loading.live_load.custom_vehicles: []
loading.live_load.eccentricity: '1.2'
loading.live_load.footpath_pressure.mode: As per IRC 6
loading.live_load.footpath_pressure.value: ''
loading.live_load.irc.70r_bogie: true
loading.live_load.irc.70r_tracked: true
loading.live_load.irc.70r_wheeled: true
loading.live_load.irc.aa_tracked: true
loading.live_load.irc.aa_wheeled: true
loading.live_load.irc.class_a: true
loading.live_load.irc.class_fatigue: true
loading.live_load.irc.class_sv: true
loading.load_combination.combinations: []
loading.permanent_load.dead_load.self_weight_factor: '1.00'
loading.seismic_load.computed.horizontal_coeff: '0.224'
loading.seismic_load.computed.spectral_coeff: '2.8'
loading.seismic_load.computed.vertical_coeff: '0.1493'
loading.seismic_load.computed.zone_factor: '0.16'
loading.seismic_load.damping: '2'
loading.seismic_load.dead_load.mode: Automatic
loading.seismic_load.dead_load.value: ''
loading.seismic_load.importance_factor: '1.0'
loading.seismic_load.live_load.mode: Automatic
loading.seismic_load.live_load.value: ''
loading.seismic_load.response_reduction_factor: '1'
loading.seismic_load.soil_type: "Type I \u2013 Rocky or Hard"
loading.seismic_load.time_period: '0.5'
loading.temperature_load.thermal_coeff_rcc: '11.7e-6'
loading.temperature_load.thermal_coeff_steel: '11.7e-6'
loading.wind_load.avg_exposed_height: '10'
loading.wind_load.drag_coeff.mode: As per IRC 6
loading.wind_load.drag_coeff.value: ''
loading.wind_load.drag_coeff_ll.mode: As per IRC 6
loading.wind_load.drag_coeff_ll.value: ''
loading.wind_load.exposed_frontal_area.mode: Automatic
loading.wind_load.exposed_frontal_area.value: ''
loading.wind_load.gust_factor.mode: As per IRC 6
loading.wind_load.gust_factor.value: ''
loading.wind_load.lift_coeff.mode: As per IRC 6
loading.wind_load.lift_coeff.value: ''
loading.wind_load.site_topography: Flat
loading.wind_load.super_area_elev.mode: Automatic
loading.wind_load.super_area_elev.value: ''
loading.wind_load.super_area_plain.mode: Automatic
loading.wind_load.super_area_plain.value: ''
loading.wind_load.terrain_type: Plain Terrain
loading.wind_load.wind_ecc_deck.mode: As per IRC 6
loading.wind_load.wind_ecc_deck.value: ''
loading.wind_load.wind_ll_ecc.mode: As per IRC 6
loading.wind_load.wind_ll_ecc.value: ''
material.cross_bracing: E 350A
material.cross_bracing.density: '76.4'
material.cross_bracing.e: '200.0'
material.cross_bracing.fu: '490.0'
material.cross_bracing.fy: '350.0'
material.cross_bracing.g: '76.9'
material.cross_bracing.poisson: '0.30'
material.cross_bracing.thermal: '11.7'
material.deck: M40
material.deck.density: '24.5'
material.deck.ecm: '33.0'
material.deck.fck: '40.0'
material.deck.fctm: '3.0'
material.deck.thermal: '11.7'
material.end_diaphragm: E 350A
material.end_diaphragm.density: '76.4'
material.end_diaphragm.e: '200.0'
material.end_diaphragm.fu: '490.0'
material.end_diaphragm.fy: '350.0'
material.end_diaphragm.g: '76.9'
material.end_diaphragm.poisson: '0.30'
material.end_diaphragm.thermal: '11.7'
material.girder: E 350A
material.girder.density: '76.4'
material.girder.e: '200.0'
material.girder.fu: '490.0'
material.girder.fy: '350.0'
material.girder.g: '76.9'
material.girder.poisson: '0.30'
material.girder.thermal: '11.7'
member_properties.cross_bracing_details.bottom_chord.G1G2.B1M1: 'Yes'
member_properties.cross_bracing_details.bottom_chord.G2G3.B2M1: 'Yes'
member_properties.cross_bracing_details.bottom_chord.G3G4.B3M1: 'Yes'
member_properties.cross_bracing_details.bottom_chord_section_designation.G1G2.B1M1: IS
  100 x 100 x 10
member_properties.cross_bracing_details.bottom_chord_section_designation.G2G3.B2M1: IS
  100 x 100 x 10
member_properties.cross_bracing_details.bottom_chord_section_designation.G3G4.B3M1: IS
  100 x 100 x 10
member_properties.cross_bracing_details.bottom_chord_section_type.G1G2.B1M1: Double
  Angle (Long Leg)
member_properties.cross_bracing_details.bottom_chord_section_type.G2G3.B2M1: Double
  Angle (Long Leg)
member_properties.cross_bracing_details.bottom_chord_section_type.G3G4.B3M1: Double
  Angle (Long Leg)
member_properties.cross_bracing_details.bracing_section_designation.G1G2.B1M1: IS
  100 x 100 x 10
member_properties.cross_bracing_details.bracing_section_designation.G2G3.B2M1: IS
  100 x 100 x 10
member_properties.cross_bracing_details.bracing_section_designation.G3G4.B3M1: IS
  100 x 100 x 10
member_properties.cross_bracing_details.bracing_section_type.G1G2.B1M1: Double Angle
  (Long Leg)
member_properties.cross_bracing_details.bracing_section_type.G2G3.B2M1: Double Angle
  (Long Leg)
member_properties.cross_bracing_details.bracing_section_type.G3G4.B3M1: Double Angle
  (Long Leg)
member_properties.cross_bracing_details.member_id.G1G2.B1M1: B1M1 to B1M1
member_properties.cross_bracing_details.member_id.G2G3.B2M1: B2M1 to B2M1
member_properties.cross_bracing_details.member_id.G3G4.B3M1: B3M1 to B3M1
member_properties.cross_bracing_details.no_of_cross_bracings: 1
member_properties.cross_bracing_details.select_girders.G1G2.B1M1: G1 to G2
member_properties.cross_bracing_details.select_girders.G2G3.B2M1: G2 to G3
member_properties.cross_bracing_details.select_girders.G3G4.B3M1: G3 to G4
member_properties.cross_bracing_details.spacing.G1G2.B1M1: 12.5
member_properties.cross_bracing_details.spacing.G2G3.B2M1: 12.5
member_properties.cross_bracing_details.spacing.G3G4.B3M1: 12.5
member_properties.cross_bracing_details.top_chord.G1G2.B1M1: 'Yes'
member_properties.cross_bracing_details.top_chord.G2G3.B2M1: 'Yes'
member_properties.cross_bracing_details.top_chord.G3G4.B3M1: 'Yes'
member_properties.cross_bracing_details.top_chord_section_designation.G1G2.B1M1: IS
  100 x 100 x 10
member_properties.cross_bracing_details.top_chord_section_designation.G2G3.B2M1: IS
  100 x 100 x 10
member_properties.cross_bracing_details.top_chord_section_designation.G3G4.B3M1: IS
  100 x 100 x 10
member_properties.cross_bracing_details.top_chord_section_type.G1G2.B1M1: Double Angle
  (Long Leg)
member_properties.cross_bracing_details.top_chord_section_type.G2G3.B2M1: Double Angle
  (Long Leg)
member_properties.cross_bracing_details.top_chord_section_type.G3G4.B3M1: Double Angle
  (Long Leg)
member_properties.cross_bracing_details.type.G1G2.B1M1: X-Bracing
member_properties.cross_bracing_details.type.G2G3.B2M1: X-Bracing
member_properties.cross_bracing_details.type.G3G4.B3M1: X-Bracing
member_properties.end_diaphragm_details.bottom_chord.G1G2.E1M1: 'Yes'
member_properties.end_diaphragm_details.bottom_chord.G1G2.E1M2: 'Yes'
member_properties.end_diaphragm_details.bottom_chord.G2G3.E2M1: 'Yes'
member_properties.end_diaphragm_details.bottom_chord.G2G3.E2M2: 'Yes'
member_properties.end_diaphragm_details.bottom_chord.G3G4.E3M1: 'Yes'
member_properties.end_diaphragm_details.bottom_chord.G3G4.E3M2: 'Yes'
member_properties.end_diaphragm_details.bottom_chord_section_designation.G1G2.E1M1: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.bottom_chord_section_designation.G1G2.E1M2: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.bottom_chord_section_designation.G2G3.E2M1: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.bottom_chord_section_designation.G2G3.E2M2: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.bottom_chord_section_designation.G3G4.E3M1: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.bottom_chord_section_designation.G3G4.E3M2: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.bottom_chord_section_type.G1G2.E1M1: Double
  Angle (Long Leg)
member_properties.end_diaphragm_details.bottom_chord_section_type.G1G2.E1M2: Double
  Angle (Long Leg)
member_properties.end_diaphragm_details.bottom_chord_section_type.G2G3.E2M1: Double
  Angle (Long Leg)
member_properties.end_diaphragm_details.bottom_chord_section_type.G2G3.E2M2: Double
  Angle (Long Leg)
member_properties.end_diaphragm_details.bottom_chord_section_type.G3G4.E3M1: Double
  Angle (Long Leg)
member_properties.end_diaphragm_details.bottom_chord_section_type.G3G4.E3M2: Double
  Angle (Long Leg)
member_properties.end_diaphragm_details.bottom_flange_thickness.G1G2.E1M1: ''
member_properties.end_diaphragm_details.bottom_flange_thickness.G1G2.E1M2: ''
member_properties.end_diaphragm_details.bottom_flange_thickness.G2G3.E2M1: ''
member_properties.end_diaphragm_details.bottom_flange_thickness.G2G3.E2M2: ''
member_properties.end_diaphragm_details.bottom_flange_thickness.G3G4.E3M1: ''
member_properties.end_diaphragm_details.bottom_flange_thickness.G3G4.E3M2: ''
member_properties.end_diaphragm_details.bottom_flange_width.G1G2.E1M1: ''
member_properties.end_diaphragm_details.bottom_flange_width.G1G2.E1M2: ''
member_properties.end_diaphragm_details.bottom_flange_width.G2G3.E2M1: ''
member_properties.end_diaphragm_details.bottom_flange_width.G2G3.E2M2: ''
member_properties.end_diaphragm_details.bottom_flange_width.G3G4.E3M1: ''
member_properties.end_diaphragm_details.bottom_flange_width.G3G4.E3M2: ''
member_properties.end_diaphragm_details.bracing_connection.G1G2.E1M1: Bolted
member_properties.end_diaphragm_details.bracing_connection.G1G2.E1M2: Bolted
member_properties.end_diaphragm_details.bracing_connection.G2G3.E2M1: Bolted
member_properties.end_diaphragm_details.bracing_connection.G2G3.E2M2: Bolted
member_properties.end_diaphragm_details.bracing_connection.G3G4.E3M1: Bolted
member_properties.end_diaphragm_details.bracing_connection.G3G4.E3M2: Bolted
member_properties.end_diaphragm_details.bracing_section.G1G2.E1M1: Double Angle (Long
  Leg)
member_properties.end_diaphragm_details.bracing_section.G1G2.E1M2: Double Angle (Long
  Leg)
member_properties.end_diaphragm_details.bracing_section.G2G3.E2M1: Double Angle (Long
  Leg)
member_properties.end_diaphragm_details.bracing_section.G2G3.E2M2: Double Angle (Long
  Leg)
member_properties.end_diaphragm_details.bracing_section.G3G4.E3M1: Double Angle (Long
  Leg)
member_properties.end_diaphragm_details.bracing_section.G3G4.E3M2: Double Angle (Long
  Leg)
member_properties.end_diaphragm_details.bracing_section_designation.G1G2.E1M1: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.bracing_section_designation.G1G2.E1M2: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.bracing_section_designation.G2G3.E2M1: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.bracing_section_designation.G2G3.E2M2: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.bracing_section_designation.G3G4.E3M1: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.bracing_section_designation.G3G4.E3M2: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.bracing_type.G1G2.E1M1: X-Bracing
member_properties.end_diaphragm_details.bracing_type.G1G2.E1M2: X-Bracing
member_properties.end_diaphragm_details.bracing_type.G2G3.E2M1: X-Bracing
member_properties.end_diaphragm_details.bracing_type.G2G3.E2M2: X-Bracing
member_properties.end_diaphragm_details.bracing_type.G3G4.E3M1: X-Bracing
member_properties.end_diaphragm_details.bracing_type.G3G4.E3M2: X-Bracing
member_properties.end_diaphragm_details.is_section.G1G2.E1M1: ''
member_properties.end_diaphragm_details.is_section.G1G2.E1M2: ''
member_properties.end_diaphragm_details.is_section.G2G3.E2M1: ''
member_properties.end_diaphragm_details.is_section.G2G3.E2M2: ''
member_properties.end_diaphragm_details.is_section.G3G4.E3M1: ''
member_properties.end_diaphragm_details.is_section.G3G4.E3M2: ''
member_properties.end_diaphragm_details.material_properties.elastic_modulus_zy.G1G2.E1M1: 25.3
member_properties.end_diaphragm_details.material_properties.elastic_modulus_zy.G1G2.E1M2: 25.3
member_properties.end_diaphragm_details.material_properties.elastic_modulus_zy.G2G3.E2M1: 25.3
member_properties.end_diaphragm_details.material_properties.elastic_modulus_zy.G2G3.E2M2: 25.3
member_properties.end_diaphragm_details.material_properties.elastic_modulus_zy.G3G4.E3M1: 25.3
member_properties.end_diaphragm_details.material_properties.elastic_modulus_zy.G3G4.E3M2: 25.3
member_properties.end_diaphragm_details.material_properties.elastic_modulus_zz.G1G2.E1M1: 25.3
member_properties.end_diaphragm_details.material_properties.elastic_modulus_zz.G1G2.E1M2: 25.3
member_properties.end_diaphragm_details.material_properties.elastic_modulus_zz.G2G3.E2M1: 25.3
member_properties.end_diaphragm_details.material_properties.elastic_modulus_zz.G2G3.E2M2: 25.3
member_properties.end_diaphragm_details.material_properties.elastic_modulus_zz.G3G4.E3M1: 25.3
member_properties.end_diaphragm_details.material_properties.elastic_modulus_zz.G3G4.E3M2: 25.3
member_properties.end_diaphragm_details.material_properties.plastic_modulus_zuy.G1G2.E1M1: 45.5
member_properties.end_diaphragm_details.material_properties.plastic_modulus_zuy.G1G2.E1M2: 45.5
member_properties.end_diaphragm_details.material_properties.plastic_modulus_zuy.G2G3.E2M1: 45.5
member_properties.end_diaphragm_details.material_properties.plastic_modulus_zuy.G2G3.E2M2: 45.5
member_properties.end_diaphragm_details.material_properties.plastic_modulus_zuy.G3G4.E3M1: 45.5
member_properties.end_diaphragm_details.material_properties.plastic_modulus_zuy.G3G4.E3M2: 45.5
member_properties.end_diaphragm_details.material_properties.plastic_modulus_zuz.G1G2.E1M1: 45.4
member_properties.end_diaphragm_details.material_properties.plastic_modulus_zuz.G1G2.E1M2: 45.4
member_properties.end_diaphragm_details.material_properties.plastic_modulus_zuz.G2G3.E2M1: 45.4
member_properties.end_diaphragm_details.material_properties.plastic_modulus_zuz.G2G3.E2M2: 45.4
member_properties.end_diaphragm_details.material_properties.plastic_modulus_zuz.G3G4.E3M1: 45.4
member_properties.end_diaphragm_details.material_properties.plastic_modulus_zuz.G3G4.E3M2: 45.4
member_properties.end_diaphragm_details.member_id.G1G2.E1M1: E1M1 to E1M2
member_properties.end_diaphragm_details.member_id.G1G2.E1M2: E1M1 to E1M2
member_properties.end_diaphragm_details.member_id.G2G3.E2M1: E2M1 to E2M2
member_properties.end_diaphragm_details.member_id.G2G3.E2M2: E2M1 to E2M2
member_properties.end_diaphragm_details.member_id.G3G4.E3M1: E3M1 to E3M2
member_properties.end_diaphragm_details.member_id.G3G4.E3M2: E3M1 to E3M2
member_properties.end_diaphragm_details.section_properties.area.G1G2.E1M1: 19.1
member_properties.end_diaphragm_details.section_properties.area.G1G2.E1M2: 19.1
member_properties.end_diaphragm_details.section_properties.area.G2G3.E2M1: 19.1
member_properties.end_diaphragm_details.section_properties.area.G2G3.E2M2: 19.1
member_properties.end_diaphragm_details.section_properties.area.G3G4.E3M1: 19.1
member_properties.end_diaphragm_details.section_properties.area.G3G4.E3M2: 19.1
member_properties.end_diaphragm_details.section_properties.iy.G1G2.E1M1: 180.0
member_properties.end_diaphragm_details.section_properties.iy.G1G2.E1M2: 180.0
member_properties.end_diaphragm_details.section_properties.iy.G2G3.E2M1: 180.0
member_properties.end_diaphragm_details.section_properties.iy.G2G3.E2M2: 180.0
member_properties.end_diaphragm_details.section_properties.iy.G3G4.E3M1: 180.0
member_properties.end_diaphragm_details.section_properties.iy.G3G4.E3M2: 180.0
member_properties.end_diaphragm_details.section_properties.iz.G1G2.E1M1: 180.0
member_properties.end_diaphragm_details.section_properties.iz.G1G2.E1M2: 180.0
member_properties.end_diaphragm_details.section_properties.iz.G2G3.E2M1: 180.0
member_properties.end_diaphragm_details.section_properties.iz.G2G3.E2M2: 180.0
member_properties.end_diaphragm_details.section_properties.iz.G3G4.E3M1: 180.0
member_properties.end_diaphragm_details.section_properties.iz.G3G4.E3M2: 180.0
member_properties.end_diaphragm_details.section_properties.mass.G1G2.E1M1: 15.04
member_properties.end_diaphragm_details.section_properties.mass.G1G2.E1M2: 15.04
member_properties.end_diaphragm_details.section_properties.mass.G2G3.E2M1: 15.04
member_properties.end_diaphragm_details.section_properties.mass.G2G3.E2M2: 15.04
member_properties.end_diaphragm_details.section_properties.mass.G3G4.E3M1: 15.04
member_properties.end_diaphragm_details.section_properties.mass.G3G4.E3M2: 15.04
member_properties.end_diaphragm_details.section_properties.radius_gyration_y.G1G2.E1M1: 3.07
member_properties.end_diaphragm_details.section_properties.radius_gyration_y.G1G2.E1M2: 3.07
member_properties.end_diaphragm_details.section_properties.radius_gyration_y.G2G3.E2M1: 3.07
member_properties.end_diaphragm_details.section_properties.radius_gyration_y.G2G3.E2M2: 3.07
member_properties.end_diaphragm_details.section_properties.radius_gyration_y.G3G4.E3M1: 3.07
member_properties.end_diaphragm_details.section_properties.radius_gyration_y.G3G4.E3M2: 3.07
member_properties.end_diaphragm_details.section_properties.radius_gyration_z.G1G2.E1M1: 3.07
member_properties.end_diaphragm_details.section_properties.radius_gyration_z.G1G2.E1M2: 3.07
member_properties.end_diaphragm_details.section_properties.radius_gyration_z.G2G3.E2M1: 3.07
member_properties.end_diaphragm_details.section_properties.radius_gyration_z.G2G3.E2M2: 3.07
member_properties.end_diaphragm_details.section_properties.radius_gyration_z.G3G4.E3M1: 3.07
member_properties.end_diaphragm_details.section_properties.radius_gyration_z.G3G4.E3M2: 3.07
member_properties.end_diaphragm_details.select_girders.G1G2.E1M1: G1 to G2
member_properties.end_diaphragm_details.select_girders.G1G2.E1M2: G1 to G2
member_properties.end_diaphragm_details.select_girders.G2G3.E2M1: G2 to G3
member_properties.end_diaphragm_details.select_girders.G2G3.E2M2: G2 to G3
member_properties.end_diaphragm_details.select_girders.G3G4.E3M1: G3 to G4
member_properties.end_diaphragm_details.select_girders.G3G4.E3M2: G3 to G4
member_properties.end_diaphragm_details.symmetry.G1G2.E1M1: ''
member_properties.end_diaphragm_details.symmetry.G1G2.E1M2: ''
member_properties.end_diaphragm_details.symmetry.G2G3.E2M1: ''
member_properties.end_diaphragm_details.symmetry.G2G3.E2M2: ''
member_properties.end_diaphragm_details.symmetry.G3G4.E3M1: ''
member_properties.end_diaphragm_details.symmetry.G3G4.E3M2: ''
member_properties.end_diaphragm_details.top_chord.G1G2.E1M1: 'Yes'
member_properties.end_diaphragm_details.top_chord.G1G2.E1M2: 'Yes'
member_properties.end_diaphragm_details.top_chord.G2G3.E2M1: 'Yes'
member_properties.end_diaphragm_details.top_chord.G2G3.E2M2: 'Yes'
member_properties.end_diaphragm_details.top_chord.G3G4.E3M1: 'Yes'
member_properties.end_diaphragm_details.top_chord.G3G4.E3M2: 'Yes'
member_properties.end_diaphragm_details.top_chord_section_designation.G1G2.E1M1: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.top_chord_section_designation.G1G2.E1M2: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.top_chord_section_designation.G2G3.E2M1: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.top_chord_section_designation.G2G3.E2M2: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.top_chord_section_designation.G3G4.E3M1: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.top_chord_section_designation.G3G4.E3M2: IS
  100 x 100 x 10
member_properties.end_diaphragm_details.top_chord_section_type.G1G2.E1M1: Double Angle
  (Long Leg)
member_properties.end_diaphragm_details.top_chord_section_type.G1G2.E1M2: Double Angle
  (Long Leg)
member_properties.end_diaphragm_details.top_chord_section_type.G2G3.E2M1: Double Angle
  (Long Leg)
member_properties.end_diaphragm_details.top_chord_section_type.G2G3.E2M2: Double Angle
  (Long Leg)
member_properties.end_diaphragm_details.top_chord_section_type.G3G4.E3M1: Double Angle
  (Long Leg)
member_properties.end_diaphragm_details.top_chord_section_type.G3G4.E3M2: Double Angle
  (Long Leg)
member_properties.end_diaphragm_details.top_flange_thickness.G1G2.E1M1: ''
member_properties.end_diaphragm_details.top_flange_thickness.G1G2.E1M2: ''
member_properties.end_diaphragm_details.top_flange_thickness.G2G3.E2M1: ''
member_properties.end_diaphragm_details.top_flange_thickness.G2G3.E2M2: ''
member_properties.end_diaphragm_details.top_flange_thickness.G3G4.E3M1: ''
member_properties.end_diaphragm_details.top_flange_thickness.G3G4.E3M2: ''
member_properties.end_diaphragm_details.top_flange_width.G1G2.E1M1: ''
member_properties.end_diaphragm_details.top_flange_width.G1G2.E1M2: ''
member_properties.end_diaphragm_details.top_flange_width.G2G3.E2M1: ''
member_properties.end_diaphragm_details.top_flange_width.G2G3.E2M2: ''
member_properties.end_diaphragm_details.top_flange_width.G3G4.E3M1: ''
member_properties.end_diaphragm_details.top_flange_width.G3G4.E3M2: ''
member_properties.end_diaphragm_details.total_depth.G1G2.E1M1: ''
member_properties.end_diaphragm_details.total_depth.G1G2.E1M2: ''
member_properties.end_diaphragm_details.total_depth.G2G3.E2M1: ''
member_properties.end_diaphragm_details.total_depth.G2G3.E2M2: ''
member_properties.end_diaphragm_details.total_depth.G3G4.E3M1: ''
member_properties.end_diaphragm_details.total_depth.G3G4.E3M2: ''
member_properties.end_diaphragm_details.type.G1G2.E1M1: Cross Bracing
member_properties.end_diaphragm_details.type.G1G2.E1M2: Cross Bracing
member_properties.end_diaphragm_details.type.G2G3.E2M1: Cross Bracing
member_properties.end_diaphragm_details.type.G2G3.E2M2: Cross Bracing
member_properties.end_diaphragm_details.type.G3G4.E3M1: Cross Bracing
member_properties.end_diaphragm_details.type.G3G4.E3M2: Cross Bracing
member_properties.end_diaphragm_details.web_thickness.G1G2.E1M1: ''
member_properties.end_diaphragm_details.web_thickness.G1G2.E1M2: ''
member_properties.end_diaphragm_details.web_thickness.G2G3.E2M1: ''
member_properties.end_diaphragm_details.web_thickness.G2G3.E2M2: ''
member_properties.end_diaphragm_details.web_thickness.G3G4.E3M1: ''
member_properties.end_diaphragm_details.web_thickness.G3G4.E3M2: ''
member_properties.girder_details.material_properties.modulus_of_elasticity_zy: 0.00102917
member_properties.girder_details.material_properties.modulus_of_elasticity_zy.G1.M1: 0.00102917
member_properties.girder_details.material_properties.modulus_of_elasticity_zy.G2.M1: 0.00102917
member_properties.girder_details.material_properties.modulus_of_elasticity_zy.G3.M1: 0.00102917
member_properties.girder_details.material_properties.modulus_of_elasticity_zy.G4.M1: 0.00102917
member_properties.girder_details.material_properties.modulus_of_elasticity_zz: 0.01198239
member_properties.girder_details.material_properties.modulus_of_elasticity_zz.G1.M1: 0.01198239
member_properties.girder_details.material_properties.modulus_of_elasticity_zz.G2.M1: 0.01198239
member_properties.girder_details.material_properties.modulus_of_elasticity_zz.G3.M1: 0.01198239
member_properties.girder_details.material_properties.modulus_of_elasticity_zz.G4.M1: 0.01198239
member_properties.girder_details.material_properties.plastic_modulus_zuy: 0.00155905
member_properties.girder_details.material_properties.plastic_modulus_zuy.G1.M1: 0.00155905
member_properties.girder_details.material_properties.plastic_modulus_zuy.G2.M1: 0.00155905
member_properties.girder_details.material_properties.plastic_modulus_zuy.G3.M1: 0.00155905
member_properties.girder_details.material_properties.plastic_modulus_zuy.G4.M1: 0.00155905
member_properties.girder_details.material_properties.plastic_modulus_zuz: 0.01319764
member_properties.girder_details.material_properties.plastic_modulus_zuz.G1.M1: 0.01319764
member_properties.girder_details.material_properties.plastic_modulus_zuz.G2.M1: 0.01319764
member_properties.girder_details.material_properties.plastic_modulus_zuz.G3.M1: 0.01319764
member_properties.girder_details.material_properties.plastic_modulus_zuz.G4.M1: 0.01319764
member_properties.girder_details.member_id.G1.M1: G1M1
member_properties.girder_details.member_id.G2.M1: G2M1
member_properties.girder_details.member_id.G3.M1: G3M1
member_properties.girder_details.member_id.G4.M1: G4M1
member_properties.girder_details.section_input.bottom_flange_thickness: All
member_properties.girder_details.section_input.bottom_flange_thickness.G1.M1: All
member_properties.girder_details.section_input.bottom_flange_thickness.G2.M1: All
member_properties.girder_details.section_input.bottom_flange_thickness.G3.M1: All
member_properties.girder_details.section_input.bottom_flange_thickness.G4.M1: All
member_properties.girder_details.section_input.bottom_flange_width: 420
member_properties.girder_details.section_input.bottom_flange_width.G1.M1: 420
member_properties.girder_details.section_input.bottom_flange_width.G2.M1: 420
member_properties.girder_details.section_input.bottom_flange_width.G3.M1: 420
member_properties.girder_details.section_input.bottom_flange_width.G4.M1: 420
member_properties.girder_details.section_input.depth: 1390
member_properties.girder_details.section_input.depth.G1.M1: 1390
member_properties.girder_details.section_input.depth.G2.M1: 1390
member_properties.girder_details.section_input.depth.G3.M1: 1390
member_properties.girder_details.section_input.depth.G4.M1: 1390
member_properties.girder_details.section_input.is_section.G1.M1: JB 150
member_properties.girder_details.section_input.is_section.G2.M1: JB 150
member_properties.girder_details.section_input.is_section.G3.M1: JB 150
member_properties.girder_details.section_input.is_section.G4.M1: JB 150
member_properties.girder_details.section_input.symmetry: Girder Symmetric
member_properties.girder_details.section_input.symmetry.G1.M1: Girder Symmetric
member_properties.girder_details.section_input.symmetry.G2.M1: Girder Symmetric
member_properties.girder_details.section_input.symmetry.G3.M1: Girder Symmetric
member_properties.girder_details.section_input.symmetry.G4.M1: Girder Symmetric
member_properties.girder_details.section_input.top_flange_thickness: All
member_properties.girder_details.section_input.top_flange_thickness.G1.M1: All
member_properties.girder_details.section_input.top_flange_thickness.G2.M1: All
member_properties.girder_details.section_input.top_flange_thickness.G3.M1: All
member_properties.girder_details.section_input.top_flange_thickness.G4.M1: All
member_properties.girder_details.section_input.top_flange_width: 420
member_properties.girder_details.section_input.top_flange_width.G1.M1: 420
member_properties.girder_details.section_input.top_flange_width.G2.M1: 420
member_properties.girder_details.section_input.top_flange_width.G3.M1: 420
member_properties.girder_details.section_input.top_flange_width.G4.M1: 420
member_properties.girder_details.section_input.torsional_restraint.G1.M1: Fully Restrained
member_properties.girder_details.section_input.torsional_restraint.G2.M1: Fully Restrained
member_properties.girder_details.section_input.torsional_restraint.G3.M1: Fully Restrained
member_properties.girder_details.section_input.torsional_restraint.G4.M1: Fully Restrained
member_properties.girder_details.section_input.type.G1.M1: Welded
member_properties.girder_details.section_input.type.G2.M1: Welded
member_properties.girder_details.section_input.type.G3.M1: Welded
member_properties.girder_details.section_input.type.G4.M1: Welded
member_properties.girder_details.section_input.warping_restraint.G1.M1: Both Flanges
  Restrained
member_properties.girder_details.section_input.warping_restraint.G2.M1: Both Flanges
  Restrained
member_properties.girder_details.section_input.warping_restraint.G3.M1: Both Flanges
  Restrained
member_properties.girder_details.section_input.warping_restraint.G4.M1: Both Flanges
  Restrained
member_properties.girder_details.section_input.web_depth: 1355
member_properties.girder_details.section_input.web_depth.G1.M1: 1355
member_properties.girder_details.section_input.web_depth.G2.M1: 1355
member_properties.girder_details.section_input.web_depth.G3.M1: 1355
member_properties.girder_details.section_input.web_depth.G4.M1: 1355
member_properties.girder_details.section_input.web_thickness: All
member_properties.girder_details.section_input.web_thickness.G1.M1: All
member_properties.girder_details.section_input.web_thickness.G2.M1: All
member_properties.girder_details.section_input.web_thickness.G3.M1: All
member_properties.girder_details.section_input.web_thickness.G4.M1: All
member_properties.girder_details.section_input.web_type.G1.M1: Thin Web with ITS
member_properties.girder_details.section_input.web_type.G2.M1: Thin Web with ITS
member_properties.girder_details.section_input.web_type.G3.M1: Thin Web with ITS
member_properties.girder_details.section_input.web_type.G4.M1: Thin Web with ITS
member_properties.girder_details.section_inputs.support_type.G1.M1: Major Laterally
  Supported
member_properties.girder_details.section_inputs.support_type.G2.M1: Major Laterally
  Supported
member_properties.girder_details.section_inputs.support_type.G3.M1: Major Laterally
  Supported
member_properties.girder_details.section_inputs.support_type.G4.M1: Major Laterally
  Supported
member_properties.girder_details.section_inputs.support_width.G1.M1: 400.0
member_properties.girder_details.section_inputs.support_width.G2.M1: 400.0
member_properties.girder_details.section_inputs.support_width.G3.M1: 400.0
member_properties.girder_details.section_inputs.support_width.G4.M1: 400.0
member_properties.girder_details.section_properties.area: 0.02388012
member_properties.girder_details.section_properties.area.G1.M1: 0.02388012
member_properties.girder_details.section_properties.area.G2.M1: 0.02388012
member_properties.girder_details.section_properties.area.G3.M1: 0.02388012
member_properties.girder_details.section_properties.area.G4.M1: 0.02388012
member_properties.girder_details.section_properties.iy: 0.0002161251
member_properties.girder_details.section_properties.iy.G1.M1: 0.0002161251
member_properties.girder_details.section_properties.iy.G2.M1: 0.0002161251
member_properties.girder_details.section_properties.iy.G3.M1: 0.0002161251
member_properties.girder_details.section_properties.iy.G4.M1: 0.0002161251
member_properties.girder_details.section_properties.iz: 0.0083277576
member_properties.girder_details.section_properties.iz.G1.M1: 0.0083277576
member_properties.girder_details.section_properties.iz.G2.M1: 0.0083277576
member_properties.girder_details.section_properties.iz.G3.M1: 0.0083277576
member_properties.girder_details.section_properties.iz.G4.M1: 0.0083277576
member_properties.girder_details.section_properties.mass: 187.459
member_properties.girder_details.section_properties.mass.G1.M1: 187.459
member_properties.girder_details.section_properties.mass.G2.M1: 187.459
member_properties.girder_details.section_properties.mass.G3.M1: 187.459
member_properties.girder_details.section_properties.mass.G4.M1: 187.459
member_properties.girder_details.section_properties.radius_gyration_y: 0.095134
member_properties.girder_details.section_properties.radius_gyration_y.G1.M1: 0.095134
member_properties.girder_details.section_properties.radius_gyration_y.G2.M1: 0.095134
member_properties.girder_details.section_properties.radius_gyration_y.G3.M1: 0.095134
member_properties.girder_details.section_properties.radius_gyration_y.G4.M1: 0.095134
member_properties.girder_details.section_properties.radius_gyration_z: 0.590535
member_properties.girder_details.section_properties.radius_gyration_z.G1.M1: 0.590535
member_properties.girder_details.section_properties.radius_gyration_z.G2.M1: 0.590535
member_properties.girder_details.section_properties.radius_gyration_z.G3.M1: 0.590535
member_properties.girder_details.section_properties.radius_gyration_z.G4.M1: 0.590535
member_properties.girder_details.section_properties.torsion_constant_it: 1.641083e-06
member_properties.girder_details.section_properties.torsion_constant_it.G1.M1: 1.641083e-06
member_properties.girder_details.section_properties.torsion_constant_it.G2.M1: 1.641083e-06
member_properties.girder_details.section_properties.torsion_constant_it.G3.M1: 1.641083e-06
member_properties.girder_details.section_properties.torsion_constant_it.G4.M1: 1.641083e-06
member_properties.girder_details.section_properties.warping_constant_iw: 0.00010176522202
member_properties.girder_details.section_properties.warping_constant_iw.G1.M1: 0.00010176522202
member_properties.girder_details.section_properties.warping_constant_iw.G2.M1: 0.00010176522202
member_properties.girder_details.section_properties.warping_constant_iw.G3.M1: 0.00010176522202
member_properties.girder_details.section_properties.warping_constant_iw.G4.M1: 0.00010176522202
member_properties.girder_details.segment_table.G1:
- end: 25.0
  id: G1M1
  start: 0.0
member_properties.girder_details.segment_table.G2:
- end: 25.0
  id: G2M1
  start: 0.0
member_properties.girder_details.segment_table.G3:
- end: 25.0
  id: G3M1
  start: 0.0
member_properties.girder_details.segment_table.G4:
- end: 25.0
  id: G4M1
  start: 0.0
member_properties.girder_details.select_girder.G1: G1
member_properties.girder_details.select_girder.G2: G2
member_properties.girder_details.select_girder.G3: G3
member_properties.girder_details.select_girder.G4: G4
member_properties.stiffener_details.bearing_stiffener_outstand: '205'
member_properties.stiffener_details.bearing_stiffener_outstand.G1.M1: '205'
member_properties.stiffener_details.bearing_stiffener_outstand.G2.M1: '205'
member_properties.stiffener_details.bearing_stiffener_outstand.G3.M1: '205'
member_properties.stiffener_details.bearing_stiffener_outstand.G4.M1: '205'
member_properties.stiffener_details.bearing_stiffener_plate_thickness: '10'
member_properties.stiffener_details.bearing_stiffener_plate_thickness.G1.M1: '10'
member_properties.stiffener_details.bearing_stiffener_plate_thickness.G2.M1: '10'
member_properties.stiffener_details.bearing_stiffener_plate_thickness.G3.M1: '10'
member_properties.stiffener_details.bearing_stiffener_plate_thickness.G4.M1: '10'
member_properties.stiffener_details.bearing_stiffener_spacing: '100'
member_properties.stiffener_details.bearing_stiffener_spacing.G1.M1: '100'
member_properties.stiffener_details.bearing_stiffener_spacing.G2.M1: '100'
member_properties.stiffener_details.bearing_stiffener_spacing.G3.M1: '100'
member_properties.stiffener_details.bearing_stiffener_spacing.G4.M1: '100'
member_properties.stiffener_details.design_method: Simple Post Critical
member_properties.stiffener_details.design_method.G1.M1: Simple Post Critical
member_properties.stiffener_details.design_method.G2.M1: Simple Post Critical
member_properties.stiffener_details.design_method.G3.M1: Simple Post Critical
member_properties.stiffener_details.design_method.G4.M1: Simple Post Critical
member_properties.stiffener_details.intermediate_stiffener: 'Yes'
member_properties.stiffener_details.intermediate_stiffener.G1.M1: 'Yes'
member_properties.stiffener_details.intermediate_stiffener.G2.M1: 'Yes'
member_properties.stiffener_details.intermediate_stiffener.G3.M1: 'Yes'
member_properties.stiffener_details.intermediate_stiffener.G4.M1: 'Yes'
member_properties.stiffener_details.intermediate_stiffener_outstand: '205'
member_properties.stiffener_details.intermediate_stiffener_outstand.G1.M1: '205'
member_properties.stiffener_details.intermediate_stiffener_outstand.G2.M1: '205'
member_properties.stiffener_details.intermediate_stiffener_outstand.G3.M1: '205'
member_properties.stiffener_details.intermediate_stiffener_outstand.G4.M1: '205'
member_properties.stiffener_details.intermediate_stiffener_spacing: '2030'
member_properties.stiffener_details.intermediate_stiffener_spacing.G1.M1: '2030'
member_properties.stiffener_details.intermediate_stiffener_spacing.G2.M1: '2030'
member_properties.stiffener_details.intermediate_stiffener_spacing.G3.M1: '2030'
member_properties.stiffener_details.intermediate_stiffener_spacing.G4.M1: '2030'
member_properties.stiffener_details.intermediate_stiffener_thickness: '10'
member_properties.stiffener_details.intermediate_stiffener_thickness.G1.M1: '10'
member_properties.stiffener_details.intermediate_stiffener_thickness.G2.M1: '10'
member_properties.stiffener_details.intermediate_stiffener_thickness.G3.M1: '10'
member_properties.stiffener_details.intermediate_stiffener_thickness.G4.M1: '10'
member_properties.stiffener_details.longitudinal_stiffener: 'No'
member_properties.stiffener_details.longitudinal_stiffener.G1.M1: 'No'
member_properties.stiffener_details.longitudinal_stiffener.G2.M1: 'No'
member_properties.stiffener_details.longitudinal_stiffener.G3.M1: 'No'
member_properties.stiffener_details.longitudinal_stiffener.G4.M1: 'No'
member_properties.stiffener_details.longitudinal_stiffener_thickness: '8'
member_properties.stiffener_details.longitudinal_stiffener_thickness.G1.M1: '8'
member_properties.stiffener_details.longitudinal_stiffener_thickness.G2.M1: '8'
member_properties.stiffener_details.longitudinal_stiffener_thickness.G3.M1: '8'
member_properties.stiffener_details.longitudinal_stiffener_thickness.G4.M1: '8'
member_properties.stiffener_details.no_bearing_stiffeners_each_end: '4'
member_properties.stiffener_details.no_bearing_stiffeners_each_end.G1.M1: '4'
member_properties.stiffener_details.no_bearing_stiffeners_each_end.G2.M1: '4'
member_properties.stiffener_details.no_bearing_stiffeners_each_end.G3.M1: '4'
member_properties.stiffener_details.no_bearing_stiffeners_each_end.G4.M1: '4'
member_properties.stiffener_details.select_member_id.G1.M1: G1M1
member_properties.stiffener_details.select_member_id.G2.M1: G2M1
member_properties.stiffener_details.select_member_id.G3.M1: G3M1
member_properties.stiffener_details.select_member_id.G4.M1: G4M1
project.location:
  data:
    district: Chennai (Minambakkam) (A)
    state: Tamil Nadu
  display_text: Chennai (Minambakkam) (A), Tamil Nadu
  method: location_name
  show_display: true
  weather_data:
    latitude: 12.9855
    longitude: 80.1689
    max_temp: 49.1
    min_temp: 15.7
    wind_speed: 50
    z_value: 0.16
    zone: III
structure.type: Highway Bridge
support_conditions.bearing_length: '400.00'
support_conditions.left_support: Pinned
support_conditions.right_support: Roller
typical_section.crash_barrier.area: 302282.768
typical_section.crash_barrier.density: 25
typical_section.crash_barrier.height: 1.1
typical_section.crash_barrier.load: 7.557
typical_section.crash_barrier.post_spacing: 2
typical_section.crash_barrier.type: IRC 5 - RCC Crash Barrier
typical_section.crash_barrier.width: 0.45
typical_section.deck_overhang: 1.05
typical_section.deck_thickness: 250.0
typical_section.footpath_thickness: 100.0
typical_section.footpath_width: 0.0
typical_section.girder_spacing: 2.1
typical_section.median.area: null
typical_section.median.density: null
typical_section.median.height: null
typical_section.median.load: null
typical_section.median.post_spacing: null
typical_section.median.type: null
typical_section.median.width: 0.0
typical_section.no_of_footpaths: 0
typical_section.no_of_girders: 4
typical_section.overall_bridge_width: 8.4
typical_section.railing.height: 1.1
typical_section.railing.load_mode: As per IRC 6
typical_section.railing.load_value: 1.4715
typical_section.railing.type: IRC 5 - RCC Railing
typical_section.railing.width: 0.0
typical_section.wearing_course.density: 24.0
typical_section.wearing_course.material: Concrete
typical_section.wearing_course.thickness: 50.0
```
