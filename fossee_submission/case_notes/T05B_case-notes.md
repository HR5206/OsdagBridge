# T05B — Save Input resets additional geometry

**Packaged evidence:** [evidence/T05B/](../evidence/T05B/). File names below refer to this folder or its recorded session subfolder.


**Date:** 10 November 2026  
**Result:** FAIL — Save Input does not preserve the committed additional inputs.  
**Scope:** Input persistence; no design calculation was executed or captured in this attempt.

## What I checked

I followed up the discrepancy in T05 by separating the Additional Inputs Save action from the main Save Input button. After saving Additional Inputs, the deck thickness remained 300 mm and the wearing-course thickness remained 75 mm. When I used the main Save Input button and saved the OSI, they reverted to 250 mm and 50 mm.

This action sequence is my reported observation. The attached button screenshot identifies the main Save Input control but does not show a before/after thickness comparison. The saved OSI and source-level reproduction provide additional evidence for the reset.

The new evidence resolves a concrete cause of the T05 mismatch. I cannot retrospectively prove the precise order of every action in the earlier T05 session, but its 250/50 saved results are consistent with this reset path.

## Configuration and evidence

The files extracted from my original `t05b.7z` archive are included under `evidence/T05B/`:

- `t05b/T05B_before.osi`
- `t05b/session_20261110_210307_226248/session.json`
- `t05b/session_20261110_210307_226248/source.json`

The session started at 21:03:07 local time (UTC+05:30), process ID 18880, on Windows 11 with Python 3.12.16. The source record identifies commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. Git status records only the untracked evidence directories. There is no numbered design-run folder in this archive, which is consistent with stopping to investigate saving before calculating.

The saved configuration has 588 keys: Highway Bridge, Chennai (Minambakkam), span 25 m, carriageway 7.5 m, no median, no footpath, explicit skew 0 and Optimized design. The complete parameter combination is preserved in the OSI.

All three steel selections use `custom_steel_345_500`: density 77 kN/m³, Fy 345 MPa, Fu 500 MPa, E 205 GPa, G 78.8 GPa, Poisson ratio 0.3 and thermal coefficient 11.7 × 10⁻⁶/°C. The deck uses `custom_concrete_45_3.5`: density 25.5 kN/m³, fck 45 MPa, fctm 3.5 MPa, Ecm 35 GPa and thermal coefficient 10.5 × 10⁻⁶/°C.

## Expected versus observed

Saving should write the current validated design inputs without replacing valid user-entered properties with defaults.

| Field | After saving Additional Inputs, my observation | My OSI after Save Input | Source-function reproduction |
|---|---:|---:|---|
| typical_section.deck_thickness | 300 mm | 250 mm | 300 → 250 |
| typical_section.wearing_course.thickness | 75 mm | 50 mm | 75 → 50 |

The OSI also contains wearing-course density 24.0 kN/m³. T05's earlier screenshot showed 25.00. The inspected routine assigns 24.0 unconditionally; T05B does not include a separate before-save density screenshot, so I do not claim another independently observed density transition for this attempt.

This is different from T04's custom-material reload failure. T05B concerns an in-session Save Input action overwriting additional geometry. The custom concrete strength fields are complete in this OSI.

## Root cause

At the tested commit:

1. `src/osdagbridge/desktop/ui/template_page.py`, `saveOSI_inputs()` at lines 793–799, unconditionally calls `solve_extend_basic_input_dict(self.input_dict)` before opening the file-save dialog.
2. `src/osdagbridge/core/bridge_types/plate_girder/defaults.py`, `solve_extend_basic_input_dict()` beginning at line 870, calls `_update_typical_section_defaults()` before solving the layout.
3. `_update_typical_section_defaults()` defines `_update()` at lines 181–182 using unconditional `input_dict.update({key: value})`.
4. That helper writes deck thickness 250.0 at line 185, wearing-course density 24.0 at line 257 and wearing-course thickness 50.0 at line 258, even if valid custom values already exist.

The defaults helper's docstring says it fills keys that are None, but its implementation overwrites nonempty keys too. The save handler subsequently serializes the modified dictionary, so the reset is present in the saved file as well as the in-memory state.

Because the reset occurs before the save dialog, source inspection also suggests that cancelling that dialog may still leave inputs changed. That cancellation behavior has not been tested in the desktop and is a proposed follow-up regression check, not an observed T05B result.

## Source-level reproduction

A separate review-environment check imported the unmodified defaults module from the recorded commit, loaded a copy of my OSI, assigned the two intended values in memory and called the same function used by Save Input. It produced:

```text
before: deck_thickness=300.0, wearing_course.thickness=75.0
after:  deck_thickness=250.0, wearing_course.thickness=50.0
```

This was a function-level reproduction, not another Windows GUI test or a structural analysis. The original evidence file and source checkout were not modified. The following script reproduces that check when run with this source installed/importable and the OSI in the working directory:

```python
from copy import deepcopy
from pathlib import Path
import yaml

from osdagbridge.core.bridge_types.plate_girder.defaults import (
    solve_extend_basic_input_dict,
)

saved = yaml.safe_load(Path("T05B_before.osi").read_text())
working = deepcopy(saved)
keys = (
    "typical_section.deck_thickness",
    "typical_section.wearing_course.thickness",
)
working[keys[0]] = 300.0
working[keys[1]] = 75.0
before = {key: working[key] for key in keys}
solve_extend_basic_input_dict(working)
after = {key: working[key] for key in keys}
print("before:", before)
print("after:", after)
assert after == before, "Default expansion overwrote entered thicknesses"
```

The final assertion is expected to fail on the tested version. After a correct fix it should pass. This script only modifies a copied dictionary in memory.

## Suggested changes

**1. Make default insertion non-destructive for user-editable values.** In the typical-section default helper, use missing-value checks rather than unconditional replacement:

```python
def _update(key, value):
    if input_dict.get(key) in (None, ""):
        input_dict[key] = value
```

This preserves valid 300/75 entries while filling absent, null or empty values. Unlike a truthiness check, it does not silently replace an explicit zero or False. Explicit invalid values should be handled by validation rather than silently defaulted.

**2. Separate initialization, derived calculations and saving.** `saveOSI_inputs()` should serialize the current validated state, normally through a snapshot, rather than invoke an initialization routine that overwrites it. If omitted optional defaults must be included in the file, fill only genuinely missing user-editable keys in the snapshot. Derived geometry and dependent loads must be recomputed deliberately through their appropriate calculation paths.

Simply applying the guard everywhere is not sufficient review of derived data: barrier area/load, overall width and other dependent quantities may need recomputation when their source inputs change. Likewise, making a copy before running the existing destructive solver would protect the live UI but still save wrong values. Both saved-value fidelity and derived-data consistency need checking.

**3. Audit other callers.** `common_design_func()` conditionally calls the same solver when basic inputs are marked changed, and OSI loading also calls it. The fix should preserve custom inputs across these paths. A successful direct Design after editing is not guaranteed merely by bypassing Save Input; it must be verified through the captured design input dictionary.

These are proposed changes. No patch has been applied to the tested installation and no patched GUI run has been performed.

## Regression checks

The first check below was reproduced against the existing defaults function. The remaining checks describe validation required for a future fix.

| Check | Required result |
|---|---|
| Existing custom 300/75 values passed to default expansion | Remain 300/75; currently fails |
| Missing or null thickness values | Receive the documented defaults |
| Save valid inputs | File and live input dictionary retain the selected values |
| Cancel file-save dialog | Live input dictionary remains unchanged |
| Repeated save | No drift across consecutive saves |
| Change a basic geometric input | Derived layout updates without wiping unrelated custom thicknesses |
| Reopen saved file | Selected thicknesses remain intact after load and subsequent actions |
| Design with custom thicknesses | Recorder input and applicable result/report fields agree |

## Reporting and scope

This is a confirmed persistence defect supported by my observation, the saved OSI and a source-function reproduction. No successful 300/75 design is claimed from this archive. I did not run Design in T05B, so this case has no final calculation outputs, CAD or plot results.

I published this finding as [issue #71: Save Input overwrites committed deck and wearing-course thicknesses with defaults](https://github.com/Nidhikhare12/OsdagBridge/issues/71). It is separate from the custom-material-map reload problem in issue #19.

The earlier T05 evidence remains unchanged. Its component screenshots are still useful, but they describe the displayed 250 mm result state, not a verified 300 mm slab design.

## Duplicate-check record

The open and closed upstream issue list retrieved on 10 November 2026 contained no issue specifically covering this Save Input thickness reset. Issue #19 describes a different custom-material reload path. I completed the later duplicate review before publishing issue #71 on 11 November 2026.

## Evidence checksums

| File | SHA-256 |
|---|---|
| `T05B_before.osi` | `eeee6fdc3de74b576b61543fc6a4bba661a235d63a6ad2c33c8ec3c1f57808ff` |
| `session_20261110_210307_226248/session.json` | `8695ec8e8032f29ed5da8a5fcf69fa2c5bb10bf28296481156eaec2d4edbe572` |
| `session_20261110_210307_226248/source.json` | `64d5a2013c6f335d672f78fa324c835621cec0726fb9c152c112292216cb504d` |
