# Published comment 65

https://github.com/Nidhikhare12/OsdagBridge/issues/65#issuecomment-6797377599

I reproduced the contradictory summary with custom materials in T06 at `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. Physical page 6 of `T06_report.pdf` shows fatigue utilization **1.89** and then prints **“Girder design pass.”** The captured `design_results.overall_status` is `FAIL`, with `max_dcr = 1.8924` and a failed Fatigue Normal Stress check.

Evidence: `T06_evidence.zip`, including the report, input/output dictionaries and a rendered extract `report_page_06.png`. The rendering is a page from the original report, not a new GUI screenshot.

I also found the same fixed-success-text pattern in the deck detailing section. In T05C, physical page 41 marks clear cover **FAIL** (75 mm required; 50 mm provided) and then says all reinforcement provisions satisfy strength and detailing requirements. `T05_save_evidence.zip` contains that report and a rendered page extract.

The second text is hardcoded in [core/reports/chap5.py:1398](https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/core/reports/chap5.py#L1398). Alongside the executive-summary correction, derive the deck sentence from the actual detailing checks, or use neutral wording that does not assert a pass. Missing/unavailable checks should not be converted to PASS. Test with a failing cover check and otherwise passing reinforcement checks. I have not independently validated the exposure classification or prescribed cover; the confirmed defect is the report contradicting its own failed check.

[T05_save_evidence.zip](https://github.com/user-attachments/files/34690085/T05_save_evidence.zip)
[T06_evidence.zip](https://github.com/user-attachments/files/34690086/T06_evidence.zip)
