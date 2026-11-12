# Published comment 20

https://github.com/Nidhikhare12/OsdagBridge/issues/20#issuecomment-6797253814

Additional runtime evidence from T06 at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3` (Windows 11/Python 3.12.16):

```text
input_before/material.girder.density = 77 kN/m³
input_after/material.girder.density  = 77 kN/m³
output_after/material.girder.density = 77 kN/m³
runtime material_props.steel_prop.rho = 78500
```

Other custom girder properties do propagate: E = 205e9 Pa, Fy = 345e6 Pa, Fu = 500e6 Pa and Poisson = 0.3. Thus a matching input/output dictionary alone does not establish that the density was used.

Span 30 m; carriageway 9 m; skew 10°; Highway Bridge; Chennai (Minambakkam) (A), Tamil Nadu; no median; no footpath; Optimized; deck 300 mm; concrete wearing course 75 mm at 25 kN/m³. Girder `custom_steel_345_500`, cross bracing `custom_steel_275_430`, end diaphragm `custom_steel_355_510`, deck `custom_concrete_45_3.5`. The complete 588-key configuration is in the attached T06 `run_01/input_before.json`.

The full evidence is in `T06_evidence.zip`, especially `input_before.json`, `output_after.json` and `runtime_properties.json`. The core call returned without an exception; that is separate from its failed fatigue check.

[core/bridge_types/plate_girder/plategirderbridge.py:1192](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/bridge_types/plate_girder/plategirderbridge.py#L1192) still substitutes `_DEFAULT_DENSITY` when the database lookup has no result. The proposed custom-key fallback should yield **77000 N/m³** for this 77 kN/m³ input. A regression should also check the resulting self-weight with section and geometry held fixed; comparing optimized runs can otherwise mix density and sizing effects. I have not patched the code or measured that isolated sensitivity here.

[T06_evidence.zip](https://github.com/user-attachments/files/34689880/T06_evidence.zip)
