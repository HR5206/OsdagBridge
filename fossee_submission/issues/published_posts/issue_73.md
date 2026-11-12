# Published issue 73

https://github.com/Nidhikhare12/OsdagBridge/issues/73

## Reproduction and evidence

Windows 11, Python 3.12.16 (conda-forge), `dev` at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. The recorder source metadata reports no tracked source modifications. The recorder wraps the original design call; it does not replace the solver.

Span 30 m; carriageway 9 m; skew 10°; Highway Bridge; Chennai (Minambakkam) (A), Tamil Nadu; no median; no footpath; Optimized; deck 300 mm; concrete wearing course 75 mm at 25 kN/m³. Girder `custom_steel_345_500`, cross bracing `custom_steel_275_430`, end diaphragm `custom_steel_355_510`, deck `custom_concrete_45_3.5`. The complete 588-key configuration is in the attached T06 `run_01/input_before.json`.

After Design, open Girder Analysis and Design Results Summary → Girder 1 → SW → Analysis Results → Major. In `T06_evidence.zip`, `07_plot_a.png` shows:

| Location | Left reaction, kN | Right reaction, kN |
|---|---:|---:|
| Support Reactions fields | 16.31 | 3.42 |
| Load sketch labels | 16.3 | 16.7 |

The right values differ far beyond rounding. Expected: both displays use the same support-reaction record for the selected member and load case. The design ran and the plot opened; this is a result-display inconsistency rather than a plotting crash.

## Root cause and suggested fix

[desktop/ui/dialogs/steel_design.py:947](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/desktop/ui/dialogs/steel_design.py#L947) fills `R_A` from `abs(sfd_values[0])` and `R_B` from `abs(sfd_values[-2])`, assuming the penultimate sample is the right-support shear. Later, around line 982, the sketch obtains reactions through `engine.extract_reactions(loadcase, member_key)` instead.

[core/bridge_types/plate_girder/graph_engine.py:1061](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/bridge_types/plate_girder/graph_engine.py#L1061) first attempts actual model support reactions, with an SFD-based fallback. This means the field and sketch use different retrieval paths. An SFD sample should not silently stand in for the model reaction.

Extract reactions once and share the result between the fields and sketch:

```python
reactions = engine.extract_reactions(loadcase, member_key)
self._current_max_dict["R_A"] = reactions.get("Ra")
self._current_max_dict["R_B"] = reactions.get("Rb")
# Pass this same reactions mapping to render_plots().
```

Handle absent values as unavailable, clearing the previous display. The extractor's fallback also deserves review: select a confirmed support node/component or expose unavailable data rather than assuming the penultimate sample is always a support. Maintain a consistent, documented sign convention.

Regression checks should cover straight/skew bridges, changed load cases, component switches and unavailable reaction data. Field and sketch values must agree after rounding. I have not independently calculated the correct reaction or assumed that the sketch is necessarily correct. No patch has been applied.

## Duplicate check

Open and closed issues checked on 11 November 2026. #61 concerns Fx/Tx plot titles and #48 concerns report omissions; neither describes these conflicting reaction values. No matching issue found.

[T06_evidence.zip](https://github.com/user-attachments/files/34689644/T06_evidence.zip)

<img width="1021" height="719" alt="07_plot_a" src="https://github.com/user-attachments/assets/07dfb7ac-122f-4c7e-9a1d-e123bb96dc0e" />
<img width="1022" height="719" alt="07_plot_b" src="https://github.com/user-attachments/assets/12027f83-f86e-49b7-9d05-da1f5c0ed90e" />
