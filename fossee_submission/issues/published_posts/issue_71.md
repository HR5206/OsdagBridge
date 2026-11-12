# Published issue 71

https://github.com/Nidhikhare12/OsdagBridge/issues/71

## What happened

I saved a 300 mm deck and a 75 mm wearing course in Additional Inputs. Those values remained set until I clicked the main **Save Input** button and saved an OSI. The saved values became 250 mm and 50 mm. In a separate direct-Design run, the intended 300/75 values reached the backend and appeared in the output/report, which helps isolate the save path.

## Environment and reproduction

Windows 11, Python 3.12.16 (conda-forge), `dev` at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. The recorder source metadata reports no tracked source modifications. The recorder wraps the original design call; it does not replace the solver.

1. Use span 25 m, carriageway 7.5 m, skew 0°, no median/footpath, Optimized. The attached `T05B_before.osi` contains the complete configuration and custom materials.
2. Open Additional Inputs, set deck thickness to 300 mm and concrete wearing-course thickness to 75 mm, then save that dialog.
3. Click the main Save Input button and save an OSI.
4. Inspect the two thickness keys in the saved file.

| Key | Intended after Additional Inputs Save | Saved OSI |
|---|---:|---:|
| `typical_section.deck_thickness` | 300 | 250 |
| `typical_section.wearing_course.thickness` | 75 | 50 |

Expected: saving preserves validated user inputs. Actual: default expansion overwrites them before serialization.

## Evidence

`T05_save_evidence.zip` contains the original T05B OSI and metadata, plus T05C's successful direct-design inputs, outputs, report and screenshots. T05B contains no design run; I am not presenting it as a completed calculation. The before-save values and action order are my observation, supported by the independent function-level reproduction below; there is no T05B before/after GUI screenshot pair.

The included `reproduce_save_reset.py` loads a copy of the OSI, assigns 300/75 and invokes the same unmodified default-expansion function. Running it against the tested commit produced:

```text
Before: deck_thickness=300.0, wearing_course.thickness=75.0
After:  deck_thickness=250.0, wearing_course.thickness=50.0
AssertionError: Save-path default expansion overwrote custom thicknesses
```

This is a function-level reproduction, not another desktop run. The assertion intentionally fails on the defective version.

## Root cause and suggested fix

[desktop/ui/template_page.py:793](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/desktop/ui/template_page.py#L793): `saveOSI_inputs()` invokes `solve_extend_basic_input_dict(self.input_dict)` before opening the save dialog. [core/bridge_types/plate_girder/defaults.py:181](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/bridge_types/plate_girder/defaults.py#L181) uses unconditional `input_dict.update()` for typical-section defaults, including deck thickness 250 and wearing-course thickness 50.

Preserve existing user-editable values when inserting defaults:

```python
def _update(key, value):
    if input_dict.get(key) in (None, ""):
        input_dict[key] = value
```

Separate initial default insertion from derived-layout recomputation and serialization. Saving should serialize the validated state; running the existing destructive helper on a copy alone would still save wrong values. Derived loads and layout must continue to update when their source inputs change. Audit the helper's load and Design callers too.

Regression checks: 300/75 survives save, reload and repeated save; omitted optional values still receive defaults; dependent geometry still updates. Because the call precedes the file dialog, also test cancellation without state mutation. Cancellation is a source-derived risk, not a GUI result I tested. No fix has been applied.

## Duplicate check

I checked open and closed issues on 11 November 2026. #19 concerns custom-material restoration after reload; this issue concerns overwriting additional geometry during Save Input. I found no issue for this exact save/default-expansion defect.

[T05_save_evidence.zip](https://github.com/user-attachments/files/34689430/T05_save_evidence.zip)
