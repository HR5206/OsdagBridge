# Published comment 41

https://github.com/Nidhikhare12/OsdagBridge/issues/41#issuecomment-6797283804

I found a second calculation path affected by custom deck density, in addition to the analysis-load path already described here.

In T05C at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`, the captured deck density is 25.5 kN/m³ and slab thickness is 300 mm. Both survive the design call, but the deck-design calculation text and report use **7.36 kN/m²** for slab dead load. Using the entered weight density gives **25.5 × 0.300 = 7.65 kN/m²**.

Evidence: `T05_save_evidence.zip`, under `t05c/`, includes the 300 mm input screenshot, complete recorder JSON and `T05C_report.pdf` (physical page 37, including cover). Geometry: span 25 m, carriageway 7.5 m, skew 0°, no median/footpath, Optimized; wearing course Concrete/75 mm; custom concrete `custom_concrete_45_3.5`. All exact parameters are in `input_before.json`.

[core/bridge_types/plate_girder/deckdesign.py:516](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/bridge_types/plate_girder/deckdesign.py#L516) contains:

```python
gamma_concrete_kN_m3 = IRC6_2017.cl_203_dead_load()["concrete_cement_reinforced"] * 9.81
w_DL_kN_m2 = gamma_concrete_kN_m3 * (deck_t_mm / 1000.0)
```

This path reads the code-table value instead of the custom material density. Fixing only `create_deck_load()` would leave this calculation inconsistent.

Please pass the validated concrete weight density into the deck-design function too, using a named argument such as `concrete_weight_density_kN_m3`, and calculate `w_DL_kN_m2 = concrete_weight_density_kN_m3 * deck_t_mm / 1000.0`. The UI already supplies weight density in kN/m³, so it should not receive another gravity conversion. Keep a clearly defined default path only for genuinely unspecified materials.

A focused regression should require 7.65 kN/m² for this configuration and confirm agreement between the global-analysis and deck-design load paths. No patched run has been performed.

[T05_save_evidence.zip](https://github.com/user-attachments/files/34689932/T05_save_evidence.zip)
