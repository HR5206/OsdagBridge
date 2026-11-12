# T02 — Custom steel and concrete: UI and saved-file retention

**Tester:** Harish Raghav S  
**Date:** 8 November 2026  
**Result:** The supplied before/after files and material dialogs retain the custom properties. The generated report contains failed structural checks and reporting inconsistencies. Use of every custom property inside the solver remains unverified.

## 1. What I tested

I kept the T01 bridge geometry and tested explicitly entered steel and concrete properties. The steel selection was `custom_steel_345_500` and the concrete selection was `custom_concrete_45_3.5`. I saved the inputs before and after the run, captured the material dialogs, and exported the report. I also rotated the CAD model successfully.

This case checks whether the custom values remain visible and saved after the run. That is a narrower claim than proving that every calculation used them. I have kept those two questions separate.

## 2. Evidence and run details

| Item | Observation |
| --- | --- |
| Project title in PDF | T02 – Custom Steel and Concrete Property Persistence Test |
| Location | Chennai (Minambakkam) (A), Tamil Nadu |
| Design mode | Optimized |
| Geometry | Span 25 m; carriageway 7.5 m; skew 0°; no median or footpath |
| Typical section | Four girders; spacing 2.1 m; overhang 1.05 m; overall width 8.4 m; deck thickness 250 mm |
| Barrier and wearing course | Barrier width 0.45 m; Concrete wearing course, 50 mm; saved wearing-course density 24.0 kN/m³ |
| Output evidence | A generated CAD image, material-information screenshots and a 58-page PDF |
| CAD rotation | Worked, as I confirmed after the run |
| Exact runtime and completion timestamp | Not captured; T01's 125.99-second duration does not apply to T02 |
| Main output dock | Not included: `03_result.png` shows the model only |
| Desktop version / commit / operating-system release | Not captured |
| Raw runtime input/output dictionaries | Not supplied |

The files are labelled before and after by the tester. Their contents can be compared, but the files themselves do not independently establish when each save occurred. No continuous recording was supplied for this case.

## 3. Exact material comparison

### Steel

The dialog is consistent with the intended girder material check. The saved files assign the same custom grade and properties to the girder, cross bracing and end diaphragm. Separate post-run cross-bracing/end-diaphragm dialogs were not supplied.

| Property | Before screenshot | Before OSI | After OSI | After screenshot |
| --- | --- | --- | --- | --- |
| Grade name | custom_steel_345_500 | custom_steel_345_500 | custom_steel_345_500 | custom_steel_345_500 |
| Weight density, kN/m³ | 77.0 | 77.0 | 77.0 | 77.0 |
| Yield strength Fy, MPa | 345.0 | 345.0 | 345.0 | 345.0 |
| Ultimate strength Fu, MPa | 500.0 | 500.0 | 500.0 | 500.0 |
| Elastic modulus E, GPa | 205.0 | 205.0 | 205.0 | 205.0 |
| Shear modulus G, GPa | 78.8 | 78.8 | 78.8 | 78.8 |
| Poisson ratio | 0.3 | 0.3 | 0.3 | 0.3 |
| Thermal coefficient, ×10⁻⁶/°C | **11.7** | **11.7** | **11.7** | **11.7** |

The planned steel thermal coefficient was 12.0, but the actual before screenshot already shows 11.7. I therefore recorded 11.7 as the tested value. There is no evidence here that the software changed 12.0 back to 11.7 during design. This case does not demonstrate a custom steel thermal coefficient different from T01.

As a consistency check, E / [2(1 + ν)] = 205 / 2.6 = 78.846… GPa, which rounds to the displayed G = 78.8 GPa. This confirms the displayed elastic constants are mutually consistent at the shown precision; it is not a bridge-analysis validation.

### Concrete deck

| Property | Before screenshot | Before OSI | After OSI | After screenshot |
| --- | --- | --- | --- | --- |
| Grade name | custom_concrete_45_3.5 | custom_concrete_45_3.5 | custom_concrete_45_3.5 | custom_concrete_45_3.5 |
| Weight density, kN/m³ | 25.5 | 25.5 | 25.5 | 25.5 |
| Compressive strength fck, MPa | 45.0 | 45 | 45 | 45.0 |
| Mean tensile strength fctm, MPa | 3.5 | 3.5 | 3.5 | 3.5 |
| Secant modulus Ecm, GPa | 35.0 | 35 | 35 | 35.0 |
| Thermal coefficient, ×10⁻⁶/°C | 10.5 | 10.5 | 10.5 | 10.5 |

The file labelled `02_deck_before.png` is a read-only Material Information dialog, rather than the editable creation dialog. It still provides evidence of the selected properties at the labelled before stage. Formatting such as `35` versus `35.0` is not a value mismatch.

### Complete saved-file comparison

Both OSI files contain **580 top-level fields**. They are byte-for-byte identical, and comparison of all parsed keys and values found **zero changes**. The full input is reproduced once in Appendix B; the second file need not be duplicated in the note.

SHA-256 for both `T02_before.osi` and `T02_after.osi`:

`58dc01982e6e495d475ffe88d9664e5df99a85b6f6924869d403abc0993abbab`

This establishes that the supplied saved snapshots agree. It does not turn an OSI into an output dictionary or prove that intermediate runtime state never changed.

## 4. Changes from T01

The baseline and T02 saved inputs have the same basic geometry, typical-section values, loading settings and design options. There are 27 differing material keys and four additional non-material keys, for 31 differing/added keys in total.

| Property | T01 | T02 |
| --- | --- | --- |
| Steel grade, all three selected steel components | E 350A | custom_steel_345_500 |
| Steel density | 76.4 kN/m³ | 77.0 kN/m³ |
| Steel Fy / Fu | 350 / 490 MPa | 345 / 500 MPa |
| Steel E / G | 200 / 76.9 GPa | 205 / 78.8 GPa |
| Steel Poisson ratio | 0.30 | 0.3; same numeric value |
| Steel thermal coefficient | 11.7 | 11.7; unchanged |
| Deck grade | M40 | custom_concrete_45_3.5 |
| Deck density | 24.5 kN/m³ | 25.5 kN/m³ |
| Deck fck / fctm | 40 / 3 MPa | 45 / 3.5 MPa |
| Deck Ecm | 33 GPa | 35 GPa |
| Deck thermal coefficient | 11.7 | 10.5 |

The additional keys are `member_properties.cross_bracing_details.no_of_cross_bracings.G1G2`, `.G2G3` and `.G3G4`, each with value 1, and `member_properties.girder_details.member_id` with value `G1M1`. They were absent from the T01 input. Their origin is not demonstrated by the screenshots, so I have not described this as an absolutely identical input dictionary except for materials.

The member/stiffener settings otherwise remain those of T01: welded symmetric girders; 1390 mm saved depth; 420 mm flange widths; optimized thickness inputs set to `All`; intermediate stiffeners enabled; longitudinal stiffeners disabled; bearing stiffeners enabled. No independent custom stiffener-material dialog was captured.

## 5. What changed in the report

Page numbers below are physical PDF viewer pages, not the printed footer numbers.

The material selection table on p.8 lists the custom names for all three steel selections and the deck. Underscores appear as spaces in the report text; that is a presentation difference rather than evidence of a different material.

Table 3.1 on p.14 shows steel density **77.0 kN/m³** and deck density **25.5 kN/m³**, matching the submitted input values. Because the report may display input values directly, this alone does not prove their use in load generation.

| Report item | T01 | T02 | Interpretation |
| --- | --- | --- | --- |
| Steel allowable stress, Table 5.10, p.34 | 315.00 MPa | 310.50 MPa | Consistent with 0.9 × Fy changing from 350 to 345 MPa |
| Maximum live-load deflection, Table 4.3, p.21 | 25.793 mm | 25.164 mm | Output changed; reported PASS in both |
| Maximum total deflection, same table | 56.704 mm | 55.321 mm | Output changed; reported FAIL in both against 41.7 mm |
| Overall girder moment capacity, Table 5.29, p.45 | 6863.47 kNm | 6907.04 kNm | Reported capacity changed |
| Shear-connector resistance, Table 5.13, p.35 | 95.36 kN | 99.53 kN | Reported capacity changed |
| Deck sagging capacity, Table 5.17, p.38 | 52.23 kNm/m | 51.09 kNm/m | Reported capacity changed; no independent recomputation |
| Deck hogging capacity, same table | 40.16 kNm/m | 47.29 kNm/m | Reported capacity changed |
| Deck overhang capacity, Table 5.18, p.38 | 108.27 kNm/m | 109.50 kNm/m | Reported capacity changed |
| Fatigue UR, G1–G4, Table 5.12, p.35 | 1.967, 1.979, 1.998, 1.998 | Same | Unchanged values alone do not establish stale state |

These differences show that the exported result set is not simply an unchanged T01 report with a new title. They do not establish that every custom property was used correctly, because several properties changed together and the runtime dictionaries were not captured.

## 6. Design status and graphical output

The project overview on p.3 reports **Fail (Fatigue Normal Stress, Int.Stiff: Leg H limit, Fatigue Shear Stress)** and maximum girder utilization **2.00**. Table 5.12 marks all four girders FAIL for fatigue. Table 5.9, p.33, reports total deflections of 54.905 mm for G1/G4 and 55.321 mm for G2/G3, also marked FAIL.

Deck flexural checks are marked PASS in the report. Cross-bracing and end-diaphragm capacity tables also show PASS, but the report inconsistencies described below limit what can be concluded from those labels.

The supplied CAD image shows the deck, side barriers, girder/stiffener details and end bracing. I confirmed that CAD rotation worked. This confirms that interaction, not exact component dimensions or structural adequacy. No separate T02 analysis-dialog screenshot was supplied. The PDF includes a bending-moment envelope on p.21; its presence is verified, its numerical correctness is not independently established.

## 7. Findings

### T02-F01 — Custom concrete is still labelled M40 in the quantity table

**Observed report inconsistency.** The input/material-selection table identifies `custom_concrete_45_3.5`, while Table 7.1 on p.53 describes the deck as **Concrete (M40)**. The same row gives volume 52.50 m³ and weight 131.25 MT.

An assistant-assisted review of upstream commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` found the literal string `Concrete (M40) for Deck Slab` in `src/osdagbridge/core/reports/chap7.py`, line 22. That is a source-supported explanation for the grade label; my installed desktop commit is still unknown.

Proposed correction: construct the description from the selected deck grade in the report payload, escape the name safely for LaTeX, and avoid a fallback that silently labels unknown materials M40. Test a named grade and a custom grade. Any quantity or density correction is a separate change and requires tracing its calculation. No patch was applied or tested on my desktop.

### T02-F02 — UI/file retention does not settle density use

**Not yet verified inside the engine.** Steel and deck densities are retained in the dialogs and OSI and are printed in the PDF. The quantity table nevertheless retains deck weight 131.25 MT and girder weight 18.75 MT from T01, despite the changed densities and unchanged listed volumes.

This is a useful diagnostic observation, but the mass/weight convention and quantity-generation path must be checked before assigning corrected totals. The upstream source reviewed during the case contains a fixed steel fallback density in `_build_material_props()`; that source observation is not a runtime capture from this desktop run.

Existing reports already address custom steel density (#20), custom deck density (#41), and transverse-member custom grades (#43). If runtime capture reproduces those behaviors, add evidence to the relevant issue rather than opening duplicates.

### T02-F03 — Report defects from T01 recur

The following are repeated observations, not additional independent bugs:

- Physical p.6 says “Girder design pass,” although p.3 and pp.34–35 report failures.
- Table 2.7, p.10, labels values such as girder depth 1.39 and flange width 0.42 as millimetres, while Table 5.1 uses 1390 mm and 420 mm.
- Table 4.2, p.21, remains blank despite the availability of reactions elsewhere.
- Table 4.3 reports total deflection 55.321 mm and FAIL, while Table 5.29 shows 22.19 mm, capacity 41.67 mm and UR 0.53 for its labelled load combination. The selection of results is not reconciled.
- The G1–G2 diagonal capacity row gives demand 6.151 kN, capacity 18.160 kN and UR 0.570; the displayed demand/capacity quotient is about 0.339. The governing-result mapping remains unresolved.

T01's wearing-course UI/saved-file mismatch is still open. Both T02 saved files contain density 24.0, but no new wearing-course screenshot was supplied to close that check.

### Issue status

No issue or comment was published for this case. Relevant previously reviewed issues are [#20](https://github.com/Nidhikhare12/OsdagBridge/issues/20), [#41](https://github.com/Nidhikhare12/OsdagBridge/issues/41), [#43](https://github.com/Nidhikhare12/OsdagBridge/issues/43), [#44](https://github.com/Nidhikhare12/OsdagBridge/issues/44) and [#48](https://github.com/Nidhikhare12/OsdagBridge/issues/48). These references come from the earlier same-day issue review; refresh the search before publishing a new finding.

## 8. Evidence register and test disposition

| Evidence | What it supports |
| --- | --- |
| `01_steel_before.png` | Custom steel creation values; thermal coefficient is 11.7 |
| `02_deck_before.png` | Selected custom concrete properties in a read-only information dialog |
| `03_result.png` | CAD model displayed; no main output-dock values or completion time in this image |
| `04_steel_after.png` | Same steel property values in the after information dialog |
| `05_deck_after.png` | Same deck property values in the after information dialog |
| `T02_before.osi` / `T02_after.osi` | 580 identical saved fields, including all three steel selections and deck properties |
| `T02_design_report.pdf` | Custom material labels, changed numerical results, design failures and report inconsistencies |
| Tester statement | “CAD rotation worked” |

| Check | Disposition |
| --- | --- |
| Selected steel properties retained in supplied UI and saved snapshots | PASS |
| Selected concrete properties retained in supplied UI and saved snapshots | PASS |
| Custom cross-bracing/end-diaphragm fields retained in saved snapshots | PASS for serialization; separate UI and solver use not verified |
| All 580 saved fields stable between supplied before/after files | PASS |
| CAD generation and rotation | PASS for display and the interaction confirmed by the tester |
| Report produced with changed material labels and some changed results | PASS for output generation only |
| All structural checks pass | FAIL according to the generated report |
| Report consistency | FAIL for the explicit discrepancies above |
| Every custom property used in analysis/design | NOT VERIFIED |
| Independent stiffener material customization | NOT VERIFIED |
| Main output-dock versus output dictionary versus PDF | NOT VERIFIED |
| Three consecutive runs in one documented session | NOT VERIFIED by this evidence set |
| Custom-material cold reload | NOT TESTED as a controlled case |

The remaining checks will be collected separately. They are not fields for me to fill by guessing or retrospectively claiming a pass.

## 9. My conclusion

The custom values I actually entered remained visible and were preserved in both saved files. I could rotate the generated CAD model. Some reported calculations changed from T01, including allowable steel stress, deflection and connector resistance, but the report still contains failed design checks and inconsistent labels. The next step is a recorded three-run sequence with runtime dictionary capture, so I can compare the visible inputs, the engine state and the final outputs for each run.

## Appendix A — Source reference and capture-method limits

The quantity-table label was inspected at [chap7.py, line 22](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/reports/chap7.py#L22). This was a read-only source review. No calculation was re-executed for this note, and no runtime output dictionary was reconstructed from the PDF.

## Appendix B — Complete saved input

The following text is copied from `T02_before.osi`. `T02_after.osi` has the same bytes and hash. Values are kept as saved rather than converted into an assumed unit system.

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
material.cross_bracing: custom_steel_345_500
material.cross_bracing.density: '77.0'
material.cross_bracing.e: '205.0'
material.cross_bracing.fu: '500.0'
material.cross_bracing.fy: '345.0'
material.cross_bracing.g: '78.8'
material.cross_bracing.poisson: '0.3'
material.cross_bracing.thermal: '11.7'
material.deck: custom_concrete_45_3.5
material.deck.density: '25.5'
material.deck.ecm: '35'
material.deck.fck: '45'
material.deck.fctm: '3.5'
material.deck.thermal: '10.5'
material.end_diaphragm: custom_steel_345_500
material.end_diaphragm.density: '77.0'
material.end_diaphragm.e: '205.0'
material.end_diaphragm.fu: '500.0'
material.end_diaphragm.fy: '345.0'
material.end_diaphragm.g: '78.8'
material.end_diaphragm.poisson: '0.3'
material.end_diaphragm.thermal: '11.7'
material.girder: custom_steel_345_500
material.girder.density: '77.0'
material.girder.e: '205.0'
material.girder.fu: '500.0'
material.girder.fy: '345.0'
material.girder.g: '78.8'
material.girder.poisson: '0.3'
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
member_properties.cross_bracing_details.no_of_cross_bracings.G1G2: 1
member_properties.cross_bracing_details.no_of_cross_bracings.G2G3: 1
member_properties.cross_bracing_details.no_of_cross_bracings.G3G4: 1
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
member_properties.girder_details.member_id: G1M1
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
