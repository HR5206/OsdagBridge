# T04 — Custom materials after reopening a saved design

**Test date:** 10 November 2026  
**Test type:** Fresh-session OSI reload, material information and design execution  
**Result:** FAIL — the custom steel information dialog raises an exception, custom concrete properties are lost, and Design stops because the required concrete strength is null.

## Purpose and starting point

I checked whether the custom materials used in my completed T03 design survived saving and reopening the input file in a fresh application session. This complements T03, where three consecutive designs completed within one session.

I used `T04_source.osi`, copied from T03's `run_03/R3_after.osi`. A byte-for-byte comparison confirms that the two files are identical. The source contains the complete custom steel and concrete properties; the missing concrete values were not missing from the original saved file.

The linked T03 session records source commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`, Windows 11 and Python 3.12.16. The subsequently supplied T04 recorder session independently confirms the same commit, Windows 11 and Python 3.12.16. It started at 20:05:43 (UTC+05:30), process ID 2120. Its Git status records only the untracked evidence directories `FOSSEE_Testing/` and `screening/`. The screenshot tracebacks agree with the relevant line locations in that source. I have not treated a failed design as a completed engineering result.

## Input configuration

| Input | Value in T04_source.osi |
|---|---|
| Span | 25 m |
| Carriageway width | 7.5 m |
| Skew | 0° |
| Median | No |
| Footpath | None |
| Design mode | Optimized |
| Deck thickness | 250 mm |
| Wearing course | Concrete, 50 mm |
| Saved wearing-course density | 24 kN/m³ |
| Girder, cross-bracing and end-diaphragm grade | custom_steel_345_500 |
| Concrete grade | custom_concrete_45_3.5 |

The exact combination of all 580 saved input keys is preserved in the source OSI. The wearing-course density above is the saved value; no wearing-course UI screenshot was supplied for T04, and this case does not resolve the separate T03 wearing-course discrepancy.

### Material values before reload

| Steel property | Value |
|---|---:|
| Weight density | 77.0 kN/m³ |
| Yield strength | 345 MPa |
| Ultimate tensile strength | 500 MPa |
| Elastic modulus | 205 GPa |
| Shear modulus | 78.8 GPa |
| Poisson's ratio | 0.3 |
| Thermal expansion coefficient | 11.7 × 10⁻⁶/°C |

These values are present separately under the girder, cross-bracing and end-diaphragm material prefixes. The source deck properties are density 25.5 kN/m³, fck 45 MPa, fctm 3.5 MPa, Ecm 35 GPa and thermal expansion coefficient 10.5 × 10⁻⁶/°C.

## Sequence and observations

1. I reopened the saved custom-material design for the T04 reload test. The material selectors still displayed custom grade names.
2. I clicked the girder material information button. Its dialog did not open. The terminal showed an `UnboundLocalError` in `material_properties.py`.
3. I opened the concrete material information dialog. It opened, but showed density 24.5 and thermal coefficient 11.7. The fck, fctm and Ecm fields were blank even though the custom material name remained visible.
4. I saved the current inputs as `T04_before.osi`. The recorder contains three design attempts in this session: the first two ended with the cancellation message, and the third reached the missing-fck error.
5. The third attempt displayed an error requiring `material.deck.fck`. The traceback reaches the girder design-check configuration through the recorder's wrapper around the original design method. The screenshots alone did not show the earlier attempts; they are included in the run log below.

The app remained usable enough after the information-button error to open the deck dialog and attempt Design. I recorded a dialog callback exception followed by a handled design error, rather than a confirmed whole-application crash. I have not claimed that every steel information button was separately tested.

## Source file versus re-saved file

Both OSIs contain 580 keys. Parsing and comparing their complete YAML mappings shows exactly five changed values, all under `material.deck`. The remaining 575 key/value pairs are equal.

| Key | T04_source.osi | T04_before.osi | Deck information screenshot |
|---|---:|---:|---|
| material.deck.density | "25.5" | "24.5" | 24.5 kN/m³ |
| material.deck.fck | "45" | null | Blank |
| material.deck.fctm | "3.5" | null | Blank |
| material.deck.ecm | "35" | null | Blank |
| material.deck.thermal | "10.5" | "11.7" | 11.7 × 10⁻⁶/°C |

The concrete grade name remains `custom_concrete_45_3.5` in both files. All saved steel names and steel property values remain equal. This shows why seeing the custom material name in the UI is insufficient to verify its properties.

The available evidence establishes loss between the original file and the re-saved pre-design state. It does not isolate the precise UI action that first overwrote each value. Source inspection shows that the shared action handler primes materials for Save, Additional Inputs and Design, so the loss should not be attributed solely to clicking the info button.

## Failure A — Steel information dialog does not open

**Evidence:** `01_material_info_not_opening.png` and `02_info_button_error.txt.png`.

The second filename ends in `.png`; it is a screenshot of terminal text, not a text log. Its visible traceback is:

```text
input_dock.py:806, _show_material_info
    MaterialPropertiesDialog(...)
material_properties.py:261, __init__
    self._load_material_info_for_view(self.selected_material)
material_properties.py:751, _load_material_info_for_view
    KEY_MATERIAL_GIRDER_E: "{:.1f}".format(defaults.get("E", 0.0)) if defaults else "",
UnboundLocalError: cannot access local variable 'defaults' where it is not associated with a value
```

The path prefix is `src/osdagbridge/desktop/ui/`, with the first file in `docks/` and the second in `dialogs/`.

### Root cause

`InputDock._show_material_info()` obtains custom properties from `_material_custom_fields`, an in-memory mapping. `populate_from_dict()` restores input values and material names from an OSI but does not rebuild that mapping.

When the material dialog receives no custom fields, `_load_material_info_for_view()` takes a fallback path. The name `custom_steel_345_500` matches its regular expression, so it extracts Fy and Fu. However, `defaults` is assigned only in the alternative branch for nonmatching names. The common dictionary construction then reads `defaults`, raising the exact exception shown in the terminal.

### Suggested correction

In `src/osdagbridge/desktop/ui/dialogs/material_properties.py`, initialize the local before either name-parsing branch:

```python
# Within the steel fallback branch of _load_material_info_for_view:
defaults = None
fy_value = ""
fu_value = ""

custom_match = re.match(
    r"^(?:Cus_|custom_steel_)([0-9]+(?:\.[0-9]+)?)_([0-9]+(?:\.[0-9]+)?)$",
    name,
    re.IGNORECASE,
)
```

This is a minimal exception fix, not a complete persistence fix. By itself, it can leave E, G and Poisson's ratio blank. The full correction must restore the saved custom fields before constructing the dialog and must not replace valid saved values with fallback blanks.

## Failure B — Concrete values revert or disappear after reload

**Evidence:** both OSIs and `03_deck_info.png`.

The deck information dialog opens with the correct grade name but incorrect or blank properties. The five changed OSI fields match the screenshot, so this is not merely a display-formatting problem.

### Root cause and files requiring changes

- `src/osdagbridge/desktop/ui/docks/input_dock.py`, `populate_from_dict()` around line 1048: restore the custom-property mapping as well as the selected material names.
- The same file, `_prime_material_inputs()` around line 324: preserve valid loaded custom values; do not overwrite them with fallback blanks or defaults.
- `src/osdagbridge/desktop/ui/dialogs/material_properties.py`, `_load_material_info_for_view()` around line 707 and `_deck_defaults()` around line 485: a custom concrete name without a restored property mapping currently reaches the standard-grade fallback. The fallback returns blank fck/fctm/Ecm, default concrete weight density and the steel thermal coefficient constant.
- `src/osdagbridge/desktop/ui/template_page.py`, `common_design_func()` around line 630: calls `_prime_material_inputs()` before shared action processing. This explains how an apparently successful OSI load can later lose values when another action is taken.

A concrete restoration approach for `populate_from_dict()` is to reconstruct the map from the loaded member-prefixed keys. The steel dialog stores base girder-prefixed keys even for cross-bracing and end-diaphragm materials, so those prefixes need translation. For example:

```python
def restored_custom_fields(data, member_key):
    grade = str(data.get(member_key, "")).strip()
    steel_members = {
        "material.girder", "material.cross_bracing", "material.end_diaphragm"
    }
    if member_key in steel_members and grade.startswith("custom_steel_"):
        suffixes = ("density", "fy", "fu", "e", "g", "poisson", "thermal")
        base = "material.girder"
    elif member_key == "material.deck" and grade.startswith("custom_concrete_"):
        suffixes = ("density", "fck", "fctm", "ecm", "thermal")
        base = "material.deck"
    else:
        return None

    fields = {}
    for suffix in suffixes:
        value = data.get(f"{member_key}.{suffix}")
        if value is None or value == "":
            raise ValueError(f"Missing saved custom property: {member_key}.{suffix}")
        fields[f"{base}.{suffix}"] = str(value)
    return grade, fields
```

The load handler should build and validate a temporary mapping with this helper before committing changes to the current project. If two members have the same grade name but conflicting saved properties, it must report the conflict or use member-scoped identities rather than silently replacing one mapping with another. Numeric finiteness and material validation should use the application's validation rules. The restored mapping must be available before any priming or information-dialog construction.

These snippets are proposed changes based on source inspection. They have not been applied to the tested installation or validated in its GUI.

## Failure C — Design cannot proceed with the reloaded inputs

**Evidence:** `04_design_error.png` and the null `material.deck.fck` in `T04_before.osi`.

The error dialog states:

```text
ValueError: 'material.deck.fck' is required but was not found in 'input_dict'.
Populate 'material.deck.fck' before running the design check.
```

The visible call chain is:

```text
template_page.py:690 -> backend.design()
capture_osdagbridge.py:105 -> original(self, *args, **kwargs)
plategirderbridge.py:757 -> stage 5, _run_dcr_checks
plategirderbridge.py:2297 -> run_design_check(...)
designer.py:3235 -> BridgeConfig.from_plate_girder_bridge(...)
designer.py:332 -> required material.deck.fck lookup
designer.py:95 -> ValueError
```

The core files are under `src/osdagbridge/core/bridge_types/plate_girder/`. The error text says “not found,” but the supplied pre-design OSI contains the key with a null value. The source requirement helper rejects both `None` and an empty string. I therefore describe this as a missing required value, not proof that the key itself was deleted.

The backend check should continue rejecting an absent concrete strength. The fix belongs in material restoration and early validation; inserting an arbitrary fck or suppressing the exception would conceal the data loss. An early validation message should identify the incomplete custom material before a lengthy analysis begins.

No successful T04 output dictionary, final design report or newly generated CAD model has been verified. The supplied recorder folder contains `output_at_failure.json` for all three attempts, not successful `output_after.json` files. Each failure output has 580 keys and exactly equals that attempt's post-call input dictionary. These are partial state snapshots, not completed calculation results.

## Duplicate check and reporting decision

The upstream open and closed issue list was checked on 10 November 2026. Existing [issue #19](https://github.com/Nidhikhare12/OsdagBridge/issues/19) already describes the missing custom-material map after OSI load and subsequent priming from defaults. The concrete-property loss and downstream design failure belong as additional evidence on that issue.

The reviewed issue list did not contain a separate issue specifically naming the `defaults` UnboundLocalError. Because it is triggered by the same reload sequence, the first reporting step should be to add this traceback and its separate one-line initialization fix to #19. A separate narrowly scoped issue should only be opened after checking the issue discussion and confirming that maintainers want it tracked separately.

No issue or comment was posted during this review. An existing issue link is a reference, not a claim that I created that issue.

### Draft additional finding for issue #19

> I reproduced this through a fresh-session reload using a saved 25 m design with custom steel (345/500 MPa) and custom concrete (fck 45 MPa). My source OSI is byte-identical to the saved input from a completed design. Comparing the source with the re-saved pre-design OSI gives exactly five changed values: concrete density 25.5 → 24.5, fck 45 → null, fctm 3.5 → null, Ecm 35 → null and thermal coefficient 10.5 → 11.7. The custom concrete grade name remains unchanged.
>
> The steel information button also raises `UnboundLocalError` at `material_properties.py:751`: the custom-name branch references `defaults` without assigning it. The deck information dialog opens but displays the missing/defaulted values. Design subsequently stops in `designer.py` because `material.deck.fck` is required.
>
> Restoring `_material_custom_fields` from the loaded property keys would address the persistence path. Initializing `defaults` before the steel name-parsing branches would separately prevent the information-dialog exception; that initialization alone would not restore the saved properties. The backend should retain its missing-fck guard.
>
> Evidence: `T04_source.osi`, `T04_before.osi`, the terminal traceback screenshot, the deck information screenshot and the Design Error screenshot. The files and screenshots are attached to my test evidence; the T04 recorder metadata confirms commit `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. It also shows two preceding cancellation exits and a third attempt that fails on the missing fck value.

## Regression checks to verify a future fix

These are proposed checks, not tests already executed on a patched build.

1. Save these custom materials, close the process, reopen and load the OSI. All material values must match the saved file.
2. Open the girder, cross-bracing, end-diaphragm and deck information dialogs. Each must open with complete, member-correct properties.
3. Use Save, Additional Inputs and Design after loading. None should overwrite saved custom properties with blanks or unrelated defaults.
4. Compare the material keys in the source OSI, re-saved OSI and recorder input dictionary. Require numeric equality for all properties.
5. Confirm Design passes the missing-material validation stage. Later engineering failures must be reported separately from persistence failures.
6. Load an intentionally incomplete custom-material file. Reject it clearly before calculation without silently substituting a design strength.

## Evidence inventory and limits

| File | Role |
|---|---|
| T04_source.osi | Original complete input, identical to T03 R3_after.osi |
| T04_before.osi | Re-saved input with five changed concrete values |
| 01_material_info_not_opening.png | Custom selections remain visible; button behavior is supported by the observation and traceback |
| 02_info_button_error.txt.png | Terminal screenshot confirming UnboundLocalError |
| 03_deck_info.png | Concrete dialog showing blank/defaulted properties |
| 04_design_error.png | Handled missing-fck design failure and traceback |

I did not need another video to establish these failures. The supplied files and screenshots give a reproducible starting point, a precise data comparison and two visible exceptions. The subsequently supplied recorder folder completes the runtime evidence for this session. It confirms the null concrete inputs and the missing-fck failure, and records two preceding cancellation exits.

**Conclusion:** T04 fails custom-material persistence and subsequent design execution. T03's successful same-session runs and this failed fresh-session reload identify a useful trigger condition: the saved property values exist on disk, but the UI's custom-material state is not restored consistently.

## Original evidence checksums

| File | SHA-256 |
|---|---|
| `T04_source.osi` | `26c79477e53f969b434e5ce6ced22954c3249ce9b103652e8fe13cb920502fef` |
| `T04_before.osi` | `d5458d64984fba2ac4c3187905cb4effb5d17941f47b705d5ba12b3074330118` |
| `01_material_info_not_opening.png` | `27edde4b0bc0eddc8b143a208f09271931ff75c27957b649f4e414600602267e` |
| `02_info_button_error.txt.png` | `0786a8edfd258bbfa10e63ea39463a718b12f274458f35628a77cb376078f00b` |
| `03_deck_info.png` | `26501a97b5eb699f9ba1925edf98446afb0c0e4514888ddd31b5ba41a300d46a` |
| `04_design_error.png` | `ab58169cec20e5c72907c621615a0312b5cbc81ef9db320eb44b6d765db2770c` |


## Recorder review added after receiving t04.7z

The archive contains `session_20261110_200543_966609` with three attempts. All times below are local UTC+05:30; durations cover the core design calls.

| Attempt | Start | Finish | Core duration | Recorded outcome |
|---|---|---|---:|---|
| run_01 | 20:07:31 | 20:08:38 | 67.24 s | RuntimeError: Analysis cancelled by user |
| run_02 | 20:14:34 | 20:15:40 | 65.38 s | RuntimeError: Analysis cancelled by user |
| run_03 | 20:16:36 | 20:17:39 | 63.50 s | ValueError: required material.deck.fck has no value |

All three status records contain an empty `capture_errors` list. The first two traces exit through `bridge_logger.check_cancel()` at stage 4G. I classify those as cancellation exits, not two additional occurrences of the missing-fck exception. The logs do not independently establish whether each cancellation was intentionally requested or whether cancellation state was retained.

All three captured before-input dictionaries already contain null fck, fctm and Ecm; deck density is 24.5 and thermal coefficient is 11.7. This establishes that the damaged values reached the backend, not just the saved OSI.

The runtime concrete object nonetheless contains fck = 25.0 MPa, fctm = 2.2 MPa and Ecm = 30.0 GPa under the custom grade name. `_build_material_props()` substitutes fallback values for missing custom properties. The later design configuration rejects the null original fck. Consequently, material validation is inconsistent across the analysis and design stages: a fallback material object is built before the missing value is rejected. This further supports validating restored custom materials before analysis.

The runtime steel object retains E = 205 GPa, Fy = 345 MPa and Fu = 500 MPa, but weight density remains 78.5 kN/m³ instead of the entered 77, consistent with T03's separate issue #20 evidence.

`output_before.json` is empty for attempt 1. Attempts 2 and 3 contain 580 entries of prior partial state. This differs from the empty pre-run outputs captured for T03's successful sequence. It does not establish that stale values were displayed to the user; failure-state outputs must be kept distinct from valid results.

The additional supplied runtime files are retained under their original session and run paths. No further repetition of T04 is needed to establish these observations.
