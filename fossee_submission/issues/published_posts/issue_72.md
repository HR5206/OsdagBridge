# Published issue 72

https://github.com/Nidhikhare12/OsdagBridge/issues/72

## What happened

My design completed and both transverse-member tabs opened. With **G1–G2 / Envelope** selected, the End Diaphragm tab repeated the Crossbracing utilization values. The captured backend dictionaries contain different end-diaphragm results.

Windows 11, Python 3.12.16 (conda-forge), `dev` at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. The recorder source metadata reports no tracked source modifications. The recorder wraps the original design call; it does not replace the solver.

## Reproduction

Span 30 m; carriageway 9 m; skew 10°; Highway Bridge; Chennai (Minambakkam) (A), Tamil Nadu; no median; no footpath; Optimized; deck 300 mm; concrete wearing course 75 mm at 25 kN/m³. Girder `custom_steel_345_500`, cross bracing `custom_steel_275_430`, end diaphragm `custom_steel_355_510`, deck `custom_concrete_45_3.5`. The complete 588-key configuration is in the attached T06 `run_01/input_before.json`.

1. Enter the configuration and save Additional Inputs. Run Design directly, bypassing the separately reported Save Input reset.
2. Open Transverse Member Design, select G1–G2 and Envelope.
3. Compare Crossbracing and End Diaphragm, then compare the end-diaphragm rows with `end_diaphragm_design_results["G1-G2"]`.

| Check | Cross-bracing output/UI | End-diaphragm output | End-diaphragm UI |
|---|---:|---:|---:|
| Diagonal tension | 0.18 | 0.23 | 0.180 |
| Diagonal compression | 0.85 | 0.54 | 0.850 |
| Chord tension | 0.16 | 0.20 | 0.160 |
| Chord compression | 0.74 | 0.47 | 0.740 |

The leaf key is `Member.efficiency`, under `diagonal`/`chord` and `tension`/`compression`. Expected: the diaphragm tab displays its own result, with demand, capacity, load case and status belonging to that same component/check.

## Evidence

`T06_evidence.zip`: `08_cross_bracing.png`, `09_end_diaphragm.png`, complete input/output dictionaries, runtime/source metadata and report. The successful core call lasted 152.41 seconds; the design's separate structural status is FAIL. This issue is about UI data routing, not whether a failed design may generate CAD.

The included `reproduce_ed_merge.py` executes only the actual merge AST extracted from `_try_load_data()` against copies of the captured dictionaries. It reproduces all four substitutions above without Qt or another structural run. Its output is included in the archive.

## Root cause

[desktop/ui/dialogs/transverse_member_design.py:920](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/desktop/ui/dialogs/transverse_member_design.py#L920) starts with `designs_dict = dict(cb_designs)` and then merges ED entries using `entry.setdefault(k, v)`. Existing `diagonal` and `chord` keys win, leaving CB values in place. Both HTML builders receive the same merged dictionary. `_build_ed_design_check_html()` around line 1412 reads that dictionary; its cross-braced branch around line 1460 also reads the shared force mapping.

The outer `dict()` copy is shallow, so adding UI metadata to a nested entry can also modify the backend's CB dictionary. That consequence follows from the source; I did not separately capture the backend after opening the dialog.

## Suggested correction

Keep CB and ED results, force records and metadata separate throughout initial load and refresh:

```python
from copy import deepcopy
self._cb_designs = deepcopy(cb_designs)
self._ed_designs = deepcopy(ed_designs)
# Add ED metadata only to self._ed_designs.
# CB builder: CB force records + self._cb_designs.
# ED builder: ED force records + self._ed_designs.
```

Update every builder call, including pair/load-case changes. Replacing `setdefault` with `update` would merely make CB show ED values instead; it is not a correct fix. Do not repair only the UR field while leaving a force from another component beside it.

Regression test: distinct CB/ED fixtures must preserve the four ratios above in their own tabs after initialization, tab changes and pair/load-case changes. Opening the dialog must not mutate backend result dictionaries. Proposed fix only; no patched GUI run has been performed.

## Related consistency observation to investigate

The same evidence shows G1–G2 CB compression demand/capacity/UR as 9.239 kN / 13.93 kN / 0.85 for the diagonal, and 8.014 / 17.44 / 0.74 for the chord. Dividing the displayed numbers gives approximately 0.663 and 0.460. Report page 40 repeats this mismatch, while page 43 uses a different compression demand, 11.84 kN, consistent with 0.85.

The UI builder takes force values from one mapping and efficiency/capacity from another. The report does the same via `get_cb_governing_force()` versus `get_cb_capacity()` / `get_cb_efficiency()` in [core/reports/report_generator.py:540](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/reports/report_generator.py#L540). Preserve the governing check's force, capacity and utilization together, or label a utilization governed by another check explicitly. I have not established that the solver's capacity or efficiency calculation itself is wrong. This observation is related display evidence, not proof that the CB/ED merge is its sole cause.

## Duplicate check

Open and closed issues were checked on 11 November 2026. #43 addresses material-property propagation, not the substitution of CB output for distinct ED output. PRs #52 and #55 discuss transverse-module work; this reproduction applies to `dev` at the commit above. I found no existing issue for this exact tab/dictionary mismatch.

[T06_evidence.zip](https://github.com/user-attachments/files/34689511/T06_evidence.zip)

<img width="1097" height="718" alt="08_cross_bracing" src="https://github.com/user-attachments/assets/857855e5-62d8-47cd-8474-43d47101b05e" />
<img width="1091" height="719" alt="09_end_diaphragm" src="https://github.com/user-attachments/assets/40d9b1ed-4819-4309-a962-04b5496874c8" />
