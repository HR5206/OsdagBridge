# Published comment 43

https://github.com/Nidhikhare12/OsdagBridge/issues/43#issuecomment-6797318546

T06 adds a distinct-material configuration at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`:

| Component | Grade | Fy/Fu, MPa | E, GPa | Weight density, kN/m³ |
|---|---|---|---:|---:|
| Girder | custom_steel_345_500 | 345/500 | 205 | 77.0 |
| Cross bracing | custom_steel_275_430 | 275/430 | 200 | 77.2 |
| End diaphragm | custom_steel_355_510 | 355/510 | 210 | 78.0 |

All `material.*` keys match between the input-before, input-after and output dictionaries. Runtime `steel_prop` contains the girder values. This supports the retention-versus-use distinction, but I did not capture every internal CLI material object.

There is an additional concrete source path to include in the fix: [core/bridge_types/plate_girder/crossbracingforces.py:608](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/bridge_types/plate_girder/crossbracingforces.py#L608) copies `design_dict_tension_bolted` / `design_dict_struts_bolted` and sets load and length without replacing their component material fields. The cross-braced ED path in [core/bridge_types/plate_girder/plategirderbridge.py:2759](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py#L2759) follows the same pattern. These templates in [core/utils/connect.py:131](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/utils/connect.py#L131) contain fixed material entries, including `Material` and `Member.Material` values such as `E 250 (Fe 410 W)A`.

Therefore, creating separate global DTOs alone is insufficient: the actual member-design job payloads must receive the validated component material properties in the representation supported by the downstream solver. Passing only an unknown custom name is insufficient if that solver expects a database grade. Connector material selection should remain explicit and separate from member material selection.

`T06_evidence.zip` includes the exact inputs, material-selection screenshot, runtime properties and outputs. Geometry was 30 m span, 9 m carriageway, 10° skew, deck 300 mm and wearing course 75 mm.

Suggested regression: inspect each constructed CB/ED job payload using these distinct properties, then vary only one component's yield strength with section and loads fixed and check that only the appropriate member calculation changes. This is proposed validation, not a sensitivity test I have already run.

[T06_evidence.zip](https://github.com/user-attachments/files/34689986/T06_evidence.zip)

