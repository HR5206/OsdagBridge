# T06 — Input validation, skew geometry and separate custom materials

**Packaged evidence:** [evidence/T06/](../evidence/T06/). File names below refer to this folder or its recorded session subfolder.


**Tested by:** Harish Raghav  
**Date:** 11 November 2026  
**Evidence folder:** `evidence/T06/`  
**Source commit:** `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`

## What I tested

I checked whether the app rejected a span and skew angle outside its supported ranges. I then ran a valid 30 m bridge with a 10° skew, a 9 m carriageway, a 300 mm deck and a 75 mm concrete wearing course. I used different custom steel materials for the girders, cross bracing and end diaphragms, together with a custom concrete deck material.

The invalid inputs produced validation messages and reset. The valid design call completed without an exception. I could rotate the CAD model and open the structural plots. However, completion did not mean that the bridge passed its design checks: the captured design result was **FAIL**, with a fatigue utilization ratio of **1.8924**. I also found that the end-diaphragm display did not agree with its own output dictionary.

## Evidence and environment

The recorder session is `session_20261111_175529_209781`, containing one design run, `run_01`. It records Windows 11 and Python 3.12.16 from conda-forge. The source metadata identifies the commit above; Git status lists untracked `FOSSEE_Testing/` and `screening/` folders.

The core design call started at **18:10:07 +05:30** and returned at **18:12:39 +05:30**. Its measured duration was **152.41 seconds**. `status.json` records `engine_returned`, `error: null` and an empty `capture_errors` list. This timing covers the wrapped core call, not the subsequent CAD interaction or PDF generation.

| Evidence | Purpose |
|---|---|
| `01_span_validation.png` | Span 19 m and the supported-range warning |
| `02_skew_validation.png` | Skew 16° and the supported-range warning; span now shows 20.0 m |
| `03_basic_inputs.png` | Valid geometry and location |
| `04_material_selections.png` | Different custom materials selected for all four material groups |
| `05_additional_input_a.png` | Deck thickness 300 mm |
| `05_additional_input_b.png` | Concrete wearing course, density 25.0 kN/m³, thickness 75 mm |
| `06_cad.png` | Generated bridge model |
| `07_plot_a.png`, `07_plot_b.png` | Girder 1, SW, major-component analysis results and plots |
| `08_cross_bracing.png` | G1–G2 cross-bracing results, Envelope |
| `09_end_diaphragm.png` | G1–G2 end-diaphragm results, Envelope |
| Recorder JSON files | Inputs before/after execution, output, runtime properties and run status |
| `T06_report.pdf` | Generated report, 55 physical PDF pages |

Page references below use physical PDF page numbers, including the cover. The report's printed page numbers are one lower.

## 1. Input validation

| Subtest | Value entered | Expected response | What happened | Result |
|---|---|---|---|---|
| T06-V1 | Span = 19 m | Reject a span below the supported minimum | The app displayed “Span must be between 20.0 m and 45.0 m (software limitation).” The subsequent skew screenshot shows the span reset to 20.0 m. | PASS |
| T06-V2 | Skew = 16° | Reject an angle above the supported maximum | The app displayed “Skew angle must be between -15.0° and 15.0°.” I confirmed that the field reset after the warning. | PASS |

I did not run a design with either invalid value. The exact replacement value after the skew warning is not recorded in a screenshot, so I have not assigned a value to it. These two checks cover an invalid lower span and an invalid upper skew; they do not establish that every boundary and input type has been tested.

## 2. Valid design inputs

| Parameter | Entered/selected value | Captured input / verification |
|---|---|---|
| Structure | Highway Bridge | Visible in basic-input screenshot |
| Location | Chennai (Minambakkam) (A), Tamil Nadu | Visible in basic-input screenshot |
| Span | 30 m | `geometry.span = 30`; runtime `L = 30.0` |
| Carriageway width | 9 m | `geometry.carriageway_width = 9`; runtime width 9.0 |
| Median | No | Visible in basic-input screenshot |
| Footpath | None | Visible in basic-input screenshot; runtime footpath count 0 |
| Skew | 10° | `geometry.skew_angle = 10`; runtime angle 10.0 |
| Design mode | Optimized | `geometry.design_mode = "Optimized"` |
| Deck thickness | 300 mm | Input before/after and output retain 300; design slab thickness 300.0 mm |
| Wearing course | Concrete, 75 mm, 25.0 kN/m³ | All three values retained in input and output |
| Overall bridge width | Derived: approximately 9.9 m | Dictionary stores `9.899999999999999`; report repeats this unrounded representation |
| Number of physical girders | Derived: 4 | Typical-section dictionary and report |
| Girder spacing / deck overhang | Derived: 2.475 m / 1.2375 m | Input, runtime geometry and report |

The runtime grillage has six longitudinal lines and 21 transverse lines. The six longitudinal lines include edge lines; I have not treated that number alone as evidence of six physical girders.

I used the direct-design workflow following the earlier Save Input finding. The archive contains no T06 `.osi` export. The captured `input_before.json` is the exact input snapshot for this run; I have not described it as an exported OSI file.

### Custom steel properties

| Property | Girder | Cross bracing | End diaphragm |
|---|---:|---:|---:|
| Material name | `custom_steel_345_500` | `custom_steel_275_430` | `custom_steel_355_510` |
| Weight density, kN/m³ | 77.0 | 77.2 | 78.0 |
| Yield strength, MPa | 345 | 275 | 355 |
| Ultimate tensile strength, MPa | 500 | 430 | 510 |
| Elastic modulus, GPa | 205 | 200 | 210 |
| Rigidity modulus, GPa | 78.8 | 76.9 | 80.8 |
| Poisson's ratio | 0.3 | 0.3 | 0.3 |
| Thermal expansion, ×10⁻⁶/°C | 11.7 | 12.0 | 12.1 |

### Custom concrete properties

| Property | Value |
|---|---:|
| Material | `custom_concrete_45_3.5` |
| Weight density | 25.5 kN/m³ |
| Cube compressive strength | 45 MPa |
| Mean tensile strength | 3.5 MPa |
| Secant elastic modulus | 35 GPa |
| Thermal expansion | 10.5 ×10⁻⁶/°C |

All `material.*` fields match between `input_before.json`, `input_after.json` and `output_after.json`. This confirms retention in the dictionaries. It does not, by itself, prove that every calculation used every custom property.

The runtime girder properties correctly contain E = 205×10⁹ Pa, Fy = 345×10⁶ Pa, Fu = 500×10⁶ Pa and Poisson's ratio 0.3. The concrete runtime object contains fck = 45, fctm = 3.5 and Ecm = 35. The design result expresses concrete Ecm as 35,000 MPa, which is consistent with 35 GPa.

The runtime steel `rho` is **78,500**, while the entered weight density is **77 kN/m³**. This repeats the earlier density-propagation finding. The runtime crash-barrier width is **0.5 m**, while the input dictionary records **0.45 m**; that mismatch also remains present.

The recorder captures one general steel-property object. It does not separately capture the material objects inside every cross-bracing/end-diaphragm calculation. I therefore do not mark distinct material use in those calculations as verified merely because the selected names survived.

## 3. Dictionary and output checks

The input dictionaries each contain **588 top-level keys**. The initial output is empty; the final output has **1,070 top-level keys**. There are 35 changed input fields, all under the girder section-input fields. These include millimetre-to-metre conversions and resolution of `All` thickness selections. The geometry, custom materials, 300 mm deck and 75 mm wearing course remain unchanged through the core call.

The final girder design has a 1,670 mm overall depth, 510 mm flange widths, 22 mm flange thicknesses and a 10 mm web. The final calculated web depth is 1,626 mm. The pre-design web-depth field is 1,628 mm, reflecting the earlier sizing state; the normalized input field and final calculated design should therefore not be treated as interchangeable.

| Result | Captured value / comparison |
|---|---|
| Overall status | `FAIL` |
| Maximum DCR | 1.8924 |
| Recorded global checks | 13 PASS, 0 WARN, 1 FAIL |
| Failing check | Fatigue Normal Stress: 175.03 MPa demand / 92.49 MPa capacity |
| Fatigue dock percentage field | `util.fatigue = 189.24` |
| Flexure utilization | 22.54% |
| Shear utilization | 52.53% |
| Interaction utilization | 23.30% |
| Lateral torsional buckling utilization | 60.51% |
| Global live / total deflection | 9.098 mm / 24.765 mm; recorded limits 37.5 mm / 50 mm |
| Deck reinforcement | Bottom Ø12 @ 215 mm; top Ø12 @ 165 mm; longitudinal Ø12 @ 250 mm; overhang Ø12 @ 100 mm |

These are the software's reported checks, not an independent structural certification. The captured `per_girder` mapping contains G1 only. I have not claimed independent per-girder verification of G2–G4 from that mapping.

## 4. CAD and plots

The CAD model was generated, and I confirmed that rotation worked. The screenshot shows the deck, barriers, girders and transverse members. This is an interaction and visual-generation check; exact solid dimensions and skew accuracy were not measured from the image.

I opened the Girder 1 results under the **SW** load case and **Major** component selection. Bending moment, shear force and deflection plots were visible. The displayed values include:

- Mz = 205.54 kNm at x = 13.24 m.
- Vy = 25.19 kN at x = 25.24 m.
- Dy = −5.28 mm at x = 13.24 m.
- Tx = 20.72 kNm.

The plots extend to 30 m. Their left coordinate is approximately −1.763 m for this skew geometry; I have not classified that coordinate alone as an error.

The reaction fields show RA = 16.31 kN and RB = 3.42 kN, while the sketch labels the end arrows as approximately 16.3 and 16.7 kN. The RB display mismatch is visible in `07_plot_a.png`. This is a consistency finding; determining the correct support reaction requires tracing the support-reaction data rather than choosing one displayed number.

## 5. End-diaphragm display uses the wrong results

This is the clearest new UI/output mismatch in T06. Both screenshots select **G1–G2 / Envelope**. The end-diaphragm screen repeats the cross-bracing utilization values, even though the end-diaphragm dictionary contains different results.

| G1–G2 check | Cross-bracing dictionary and UI | End-diaphragm dictionary | End-diaphragm UI |
|---|---:|---:|---:|
| Diagonal tension | 0.18 | 0.23 | 0.180 |
| Diagonal compression | 0.85 | 0.54 | 0.850 |
| Chord tension | 0.16 | 0.20 | 0.160 |
| Chord compression | 0.74 | 0.47 | 0.740 |

The dictionary paths are `crossbracing_design_results["G1-G2"]` and `end_diaphragm_design_results["G1-G2"]`, followed by `diagonal` or `chord`, `tension` or `compression`, and `Member.efficiency`.

Both result sets have the same displayed capacities for this case: 45.00 kN in tension, 13.93 kN for diagonal compression and 17.44 kN for chord compression. Matching capacities do not justify substituting the other component's utilization ratios.

### Code-level explanation and proposed correction

At this commit, `src/osdagbridge/desktop/ui/dialogs/transverse_member_design.py`, `_try_load_data()` around lines 920–937, begins with `designs_dict = dict(cb_designs)`. It then merges end-diaphragm results using `entry.setdefault(k, v)`. Since `diagonal` and `chord` already exist for the pair, the cross-bracing values remain. Both tab builders receive this shared dictionary. `_build_ed_design_check_html()` around line 1412 subsequently reads the shared pair entry, and its cross-braced branch also reads the cross-bracing-style force keys.

The fix should preserve separate component dictionaries and use the corresponding force data when rendering each tab. For example, the intended separation is:

```python
from copy import deepcopy

self._cb_designs = deepcopy(cb_designs)
self._ed_designs = deepcopy(ed_designs)
# Attach end-diaphragm type metadata only to self._ed_designs.
# Pass self._cb_designs to the cross-bracing builder.
# Pass self._ed_designs and end-diaphragm forces to the diaphragm builder.
```

This is a proposed change, not a patch applied during testing. All initial-load and refresh call sites must be updated together. The force mapping also needs correction; changing only the result dictionary would leave an inconsistent force/capacity/UR row. A regression check should use deliberately different CB and ED results and verify all four displayed URs, including after changing the selected pair and load case. Deep copies also avoid modifying the backend's nested dictionaries while adding UI metadata.

## 6. Report consistency

The PDF correctly includes the 300 mm deck and 75 mm wearing course on physical page 9. Its deck summary on page 43 agrees with selected dictionary values, including sagging utilization approximately 0.87 and hogging approximately 0.51.

Several inconsistencies remain:

1. **Contradictory girder summary:** physical page 6 shows fatigue utilization 1.89 and then states “Girder design pass.” The captured overall status is FAIL. This repeats an earlier report finding.
2. **Wrong concrete label:** physical page 50 labels the deck concrete as M40 despite the selected custom material and fck = 45 MPa.
3. **Force/UR mismatch:** physical page 40 lists the G1–G2 cross-bracing diagonal demand as 9.239 kN, capacity 13.930 kN and UR 0.850. The displayed demand divided by capacity is approximately 0.663. Its chord row shows 8.014/17.440 ≈ 0.460, but UR 0.740. These values do not describe a consistent demand/capacity pair. Page 43 uses a different governing compression demand, 11.84 kN, which is consistent with approximately 0.85. This supports a result-selection/mapping investigation, rather than assuming the underlying capacity calculation is wrong.

The original PDF is retained unchanged as evidence. After duplicate checking, I published issues [#72](https://github.com/Nidhikhare12/OsdagBridge/issues/72), [#73](https://github.com/Nidhikhare12/OsdagBridge/issues/73) and [#74](https://github.com/Nidhikhare12/OsdagBridge/issues/74), and added findings to existing issues. The [live register](../issues/LIVE_ISSUES.md) links to all posts.

## Outcome and limits

| Area | Outcome |
|---|---|
| Invalid span and skew rejection | PASS for the two tested values |
| Valid design execution | PASS: core call returned without an exception |
| CAD rotation and opening plots | PASS, confirmed during my interaction |
| Custom input retention | PASS in the before/after/output dictionaries |
| Full custom-material calculation propagation | Not fully verified; runtime density mismatch remains |
| 300/75 thickness persistence through direct Design | PASS |
| End-diaphragm UI vs its output dictionary | FAIL: cross-bracing URs appear in the diaphragm tab |
| Generated report consistency | FAIL for the documented summary, material label and force/UR comparisons |
| Structural design status | Software reports FAIL, governed by fatigue |

T06 adds invalid-input handling, a wider skew bridge and distinct component material selections to the previous cases. It is one design run, so the evidence for three consecutive designs remains in T03. The complete input JSON files retain the other loading and member options for reproduction. I have not marked untouched options, every load combination, every component calculation or every possible boundary as independently verified.

I completed this case and included its findings in the final report. The issue register records the published bug reports and supporting comments; the evidence folder contains the original captured files.
