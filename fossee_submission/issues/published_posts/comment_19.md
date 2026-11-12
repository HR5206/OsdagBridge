# Published comment 19

https://github.com/Nidhikhare12/OsdagBridge/issues/19#issuecomment-6797191826

I reproduced this through the desktop reload path at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` on Windows 11/Python 3.12.16, and found two useful additional symptoms.

The original `T04_source.osi` contains complete custom properties. After loading it in a fresh session, the steel information button raised:

```text
material_properties.py, line 751, _load_material_info_for_view
UnboundLocalError: cannot access local variable 'defaults' where it is not associated with a value
```

The deck information dialog opened with the custom name still selected, but fck/fctm/Ecm were blank. Comparing the original OSI with `T04_before.osi` shows exactly five changes:

| Deck key | Source | Re-saved pre-design state |
|---|---:|---:|
| density | 25.5 | 24.5 |
| fck | 45 | null |
| fctm | 3.5 | null |
| ecm | 35 | null |
| thermal | 10.5 | 11.7 |

The selected name stays `custom_concrete_45_3.5`. All other 575 saved key/value pairs are equal. The design attempt in `run_03` then stops with `ValueError: 'material.deck.fck' is required but was not found in 'input_dict'`. Earlier attempts in the same session contain cancellation messages; I am not counting them as crashes.

Evidence is in `T04_evidence.zip`: both OSIs, screenshots, `run_03` dictionaries and the full traceback. Geometry w

[T04_evidence.zip](https://github.com/user-attachments/files/34689798/T04_evidence.zip)

as span 25 m, carriageway 7.5 m, skew 0°, no median/footpath, Optimized. Steel was `custom_steel_345_500`; the OSI preserves all exact parameters. This is a dialog callback exception plus a handled design failure, not a confirmed process crash.

In addition to rebuilding the custom-property map in `InputDock.populate_from_dict()`, please handle the missing-map branch in [desktop/ui/dialogs/material_properties.py:751](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/desktop/ui/dialogs/material_properties.py#L751). The name-parsing path can reach `defaults` without initializing it. Initializing that local variable prevents the exception, but does not restore the lost concrete data by itself.

A complete fix should reconstruct per-component property dictionaries from the OSI before info/Save/Additional Inputs/Design can re-prime them. Avoid relying only on a grade name as material identity when two components may share a name but have different values. Preserve complete saved values; reject an incomplete custom material clearly rather than silently filling arbitrary strengths. Tests should exercise a fresh process, all material information dialogs, re-save and a subsequent design. No patch has been applied in my testing.

