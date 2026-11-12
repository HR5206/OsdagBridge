# OsdagBridge functional testing

**Harish Raghav S · FOSSEE winter internship screening · 8–11 November 2026**

I tested the short-span steel girder bridge module using default and custom materials, three consecutive designs in one session, saved-input reloads, additional-input changes and a skew bridge. I compared the visible inputs and results with saved OSI files, captured dictionaries, runtime properties and generated reports.

Start with my [testing report](report/OsdagBridge_Testing_Report_Harish_Raghav.pdf). The [Markdown version](report/OsdagBridge_Testing_Report.md) provides searchable text and links to the original screenshots.

The application completed several designs and generated CAD models and structural plots. I also found reproducible input-persistence, material-propagation and result-display problems. A completed run does not mean the bridge passed its engineering checks: the completed designs reviewed here contain reported failures.

## Test record

| Case | What I checked | Main result |
| --- | --- | --- |
| T01 | 25 m baseline, E 350A steel, M40 deck | Analysis, CAD, plot and report generated; engineering checks include failures. |
| T02 | Custom steel and concrete | Material dialogs and saved values retained the custom inputs; CAD rotation worked. |
| T03 | 25 → 20 → 25 m in one session | All three runs completed; geometry and results changed, then returned to the first run's numerical output. |
| T04 | Reload saved custom materials | Steel information dialog raised an exception; concrete properties were lost; design failed on missing deck strength. Two earlier cancelled attempts are retained. |
| T05 | Intended 300 mm deck / 75 mm wearing course | Inconclusive: saved and displayed results remained 250/50; no captured design call. |
| T05B | Save Input after committing 300/75 | Save Input reset both thicknesses to 250/50. |
| T05C | Direct Design with 300/75 | Inputs reached execution and the deck results matched selected dictionary values. |
| T06 | Validation and 30 m / 9 m / 10° skew run | Invalid span/skew warnings worked; valid run completed; distinct component materials exposed further result-routing issues. |

There are eight case groups and 14 documented checks or attempts. Seven completed designs are evidenced; five have recorder success records. I have not converted those mixed checks into an overall pass percentage.

## Findings on GitHub

I published four original issues after reviewing existing reports:

- [#71 — Save Input resets additional thickness inputs](https://github.com/Nidhikhare12/OsdagBridge/issues/71)
- [#72 — End Diaphragm shows cross-bracing results](https://github.com/Nidhikhare12/OsdagBridge/issues/72)
- [#73 — Support-reaction fields and plot labels disagree](https://github.com/Nidhikhare12/OsdagBridge/issues/73)
- [#74 — Runtime crash-barrier width differs from the input](https://github.com/Nidhikhare12/OsdagBridge/issues/74)

I added supporting evidence to existing issues #19, #20, #41, #43, #48 and #65. The [complete live register](issues/LIVE_ISSUES.md) links directly to each comment. These ten posts were checked on 11 November 2026 and each had an evidence-attachment link. The local Markdown copies preserve their published text at that check; GitHub may change afterward.

## Evidence and provenance

| Folder | Contents |
| --- | --- |
| `report/` | Final report in PDF and Markdown. |
| `case_notes/` | Eight detailed case notes, including saved-input appendices where recorded. |
| `evidence/` | Original screenshots, OSI files, application-generated reports and recorder sessions. |
| `issues/` | Live links, published post copies and the verification snapshot. |
| `scripts/` | Recorder, two isolated reproductions and the report builder. |
| `scripts/review_results/` | Outputs of the isolated source-level reproductions. |
| `SHA256SUMS.txt` | SHA-256 checksums for the packaged files, excluding the manifest itself. |

The recorded source revision from T03 onward is `d74f56dd7f22925fb8148cabf5740ed8d1e39ff3`. T01/T02 did not record their installed revision. Later recorder metadata identifies Windows 11 and Python 3.12.16 from conda-forge.

Within a captured session, `input_before.json` records what was sent to the core design call, `input_after.json` records its state afterward, and `output_after.json` records the resulting dictionary. Status and runtime files provide exception, timing and selected propagation evidence. Full inputs are retained so reviewers can inspect parameters not repeated in the main report.

I have kept the original evidence files unchanged. I updated the case-note wording and issue links without changing the recorded observations. The original application-generated PDFs are preserved, including the incorrect wording and labels discussed in my report.

## Optional reproduction

Use the tested source revision and its project environment. Read each script's header before running it. The recorder wraps the original design method; it is not a replacement structural solver.

From this submission folder, with the tested `osdagbridge` package available:

```text
python scripts/reproduce_save_reset.py evidence/T05B/T05B_before.osi
```

On the tested revision, this prints 300/75 before default expansion and 250/50 afterward, then intentionally raises an assertion. It isolates the save-path mechanism and does not run the GUI or write an OSI file.

With this folder at the repository root and the source on the tested revision, the result-routing reproduction uses the source file and T06 output below:

```text
python scripts/reproduce_ed_merge.py ../src/osdagbridge/desktop/ui/dialogs/transverse_member_design.py evidence/T06/session_20261111_175529_209781/run_01/output_after.json
```

It executes the source's dictionary-merge block against captured output and confirms that cross-bracing values replace the distinct end-diaphragm values. These isolated reproductions are separate from the manual desktop tests.

To rebuild the report, install ReportLab and Pillow. The script uses standard Helvetica and Courier fonts, so no separate font installation is required. Run `python scripts/build_report.py` from any directory. Rebuilding changes the report files, so regenerate checksums if distributing the changed package.

## File integrity

I included `.gitattributes` to prevent Git from changing line endings in the original evidence. The following read-only check compares the packaged files with the manifest:

```text
python scripts/verify_evidence.py
```

The manifest describes the original evidence bytes, not normalized text. The hash check should report zero problems after extracting this archive or checking out the corrected files.

## Limits

This is functional testing and output-consistency review, not an independent bridge-design certification. I did not independently recompute every structural check, test every optional component configuration, or verify every member/load combination. T05's intended run is explicitly inconclusive. T01/T02 have no captured live backend dictionaries. The report distinguishes those gaps from confirmed findings.

Repository: [HR5206/OsdagBridge](https://github.com/HR5206/OsdagBridge).

The resume and hosted video are separate submission items; they are not included in this evidence package.
