# Published issue 74

https://github.com/Nidhikhare12/OsdagBridge/issues/74

## What I found

The design input contains a crash-barrier width of 0.45 m, but the runtime `DeckLayoutProperties` object contains 0.5 m. The mismatch appears in multiple captured designs, including T06. I am reporting input propagation; I have not quantified its effect on final forces or design adequacy.

Windows 11, Python 3.12.16 (conda-forge), `dev` at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. The recorder source metadata reports no tracked source modifications. The recorder wraps the original design call; it does not replace the solver.

## Reproduction

Span 30 m; carriageway 9 m; skew 10°; Highway Bridge; Chennai (Minambakkam) (A), Tamil Nadu; no median; no footpath; Optimized; deck 300 mm; concrete wearing course 75 mm at 25 kN/m³. Girder `custom_steel_345_500`, cross bracing `custom_steel_275_430`, end diaphragm `custom_steel_355_510`, deck `custom_concrete_45_3.5`. The complete 588-key configuration is in the attached T06 `run_01/input_before.json`.

Run Design and compare the captured `run_01/input_before.json` with `run_01/runtime_properties.json` in `T06_evidence.zip`:

```text
input_before["typical_section.crash_barrier.width"] = 0.45
input_after["typical_section.crash_barrier.width"]  = 0.45
runtime["deck_layout"]["crash_barrier_width"]      = 0.5
```

Expected: the runtime layout uses the validated width from the input dictionary, unless a documented and explicit transformation applies. Actual: it silently substitutes the fixed default.

## Root cause and proposed change

[core/bridge_types/plate_girder/plategirderbridge.py:1017](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py#L1017), `_build_dtos()`, constructs the layout with `crash_barrier_width=float(DEFAULT_CRASH_BARRIER_WIDTH)`. The declared input key `KEY_CB_WIDTH` is `typical_section.crash_barrier.width`.

Read and validate that key instead of substituting the constant. For example, after shared input validation:

```python
raw_width = inp.get(KEY_CB_WIDTH)
if raw_width in (None, ""):
    raise ValueError("Crash-barrier width is required before building the deck layout")
barrier_width = float(raw_width)
# Use barrier_width in DeckLayoutProperties(...).
```

Default initialization, if supported for this field, should happen once before validation and be reflected in the input state. Validation should reject nonfinite/invalid widths and preserve an explicitly supported zero-width/no-barrier case rather than using a truthiness fallback.

Regression check: input 0.45 produces runtime 0.45; a second accepted custom width propagates too; missing/invalid inputs follow the documented validation/default path. Check dependent width/load calculations after the change. This is a proposed fix, not a tested patch.

## Duplicate check

Open and closed issues checked on 11 November 2026. #64 concerns railing line load, while #41 concerns deck material density. Neither covers crash-barrier width in the runtime layout. No matching issue found.

[T06_evidence.zip](https://github.com/user-attachments/files/34690296/T06_evidence.zip)

