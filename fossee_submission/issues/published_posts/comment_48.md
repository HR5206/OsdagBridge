# Published comment 48

https://github.com/Nidhikhare12/OsdagBridge/issues/48#issuecomment-6797351975

Additional report data-fidelity finding at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`: T06's material take-off labels the deck **“Concrete (M40)”** even though its selected material is `custom_concrete_45_3.5`, and the input/runtime/design result contain fck = 45 MPa.

This appears on physical page 50 of `T06_report.pdf`. `T06_evidence.zip` includes the original PDF, a rendered page extract `report_page_50.png`, and complete input/output dictionaries. The design configuration is span 30 m, carriageway 9 m, skew 10°, deck 300 mm, wearing course 75 mm, Optimized.

The label is literal text in [core/reports/chap7.py:22](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/reports/chap7.py#L22):

```text
3 & Concrete (M40) for Deck Slab & ...
```

Please generate it from `KEY_DECK_CONCRETE_GRADE_BASIC` (and optionally the numeric fck), using the report's LaTeX escaping helper. For a custom grade, preserve its name or explicitly show fck = 45 MPa; do not silently relabel it as a standard grade. A regression should use a non-M40 grade and assert that the quantity table agrees with the material section. I am reporting the label mismatch, not claiming that all quantity calculations were independently verified.

[T06_evidence.zip](https://github.com/user-attachments/files/34690042/T06_evidence.zip)
