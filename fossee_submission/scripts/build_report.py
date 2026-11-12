"""Rebuild the report with ReportLab and Pillow; uses Helvetica and Courier.
Run: python scripts/build_report.py
Reads the original evidence without changing it.
"""
from pathlib import Path
from html import escape, unescape
import re, json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, CondPageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import black, white, HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from PIL import Image as PILImage

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'report'; OUT.mkdir(exist_ok=True)
E=ROOT/'evidence'
W=425.197
styles={
 'body':ParagraphStyle('Body',fontName='Helvetica',fontSize=11.35,leading=14.45,alignment=TA_JUSTIFY,textColor=black,spaceAfter=11),
 'small':ParagraphStyle('Small',fontName='Helvetica',fontSize=10,leading=13,alignment=TA_JUSTIFY,textColor=black,spaceAfter=10),
 'chapter':ParagraphStyle('Chapter',fontName='Helvetica-Bold',fontSize=23.5,leading=29.9,spaceAfter=20,keepWithNext=True),
 'h1':ParagraphStyle('H1',fontName='Helvetica-Bold',fontSize=23.5,leading=29.9,spaceAfter=30,keepWithNext=True),
 'h2':ParagraphStyle('H2',fontName='Helvetica-Bold',fontSize=16.35,leading=20,spaceBefore=18,spaceAfter=13,keepWithNext=True),
 'h3':ParagraphStyle('H3',fontName='Helvetica-Bold',fontSize=11.35,leading=15,spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'cell':ParagraphStyle('Cell',fontName='Helvetica',fontSize=9.0,leading=11.6,textColor=black),
 'head':ParagraphStyle('Head',fontName='Helvetica-Bold',fontSize=9.0,leading=11.6,textColor=black),
 'caption':ParagraphStyle('Caption',fontName='Helvetica',fontSize=10.3,leading=13,alignment=TA_CENTER,spaceBefore=5,spaceAfter=13),
 'code':ParagraphStyle('Code',fontName='Courier',fontSize=8.6,leading=12,spaceBefore=5,spaceAfter=13),
 'title':ParagraphStyle('Title',fontName='Helvetica-Bold',fontSize=25,leading=33,alignment=TA_CENTER,spaceAfter=25),
 'centre':ParagraphStyle('Centre',fontName='Helvetica',fontSize=12,leading=18,alignment=TA_CENTER,spaceAfter=15),
}
styles['body'].allowOrphans=0
styles['body'].allowWidows=0
styles['left']=ParagraphStyle('Left',parent=styles['body'],alignment=TA_LEFT)
styles['small'].alignment=TA_LEFT
story=[];md=[];sections=[]
chapter_no=0;sub_no=0;figure_no=0;table_no=0
def plain(s):return unescape(re.sub('<[^>]+>','',str(s)))
def mdtext(s):
    s=re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>',r'[\2](\1)',str(s))
    return plain(s.replace('<br/>',' '))

REVISIONS = {
 'The strongest findings are a reproducible Save Input reset, end-diaphragm results replaced by cross-bracing values in the UI, inconsistent support-reaction displays, and a runtime crash-barrier width that differs from the input. All four have published reports with source-level explanations.': 'I found four problems that I reported as new issues: Save Input resets the thickness values, the end-diaphragm tab shows cross-bracing results, support-reaction values disagree within the same screen, and the runtime crash-barrier width differs from my input. I included the reproduction steps and relevant source code in each issue.',
 '<b>Reading the results:</b> successful execution is recorded separately from structural adequacy. The completed cases reviewed here contain failed engineering checks; I do not describe them as safe bridge designs.': 'Throughout this report, I have kept successful execution separate from the engineering result. A run can finish and display its outputs while still failing a design check. The completed cases reviewed here contain failed engineering checks, so I have not described them as safe bridge designs.',
 'Recorder sessions identify Windows 11 and Python 3.12.16 from conda-forge. Source metadata identifies commit d74f56d and only untracked evidence directories. T01 and T02 did not capture their installed revision or operating-system release; I have not retrospectively assigned the later revision to them.': 'My recorded sessions identify Windows 11 and Python 3.12.16 from conda-forge. The source metadata records commit d74f56d and only untracked evidence directories. I did not capture the installed revision or operating-system release during T01 and T02, so I have not assigned the later revision to those tests.',
 'The recorder wraps the original design method in memory and calls it once. Its core-call timings exclude later GUI rendering and report export and are not performance benchmarks. The scripts and source-level checks are included with this submission.': 'I used a recorder that wraps the original design method in memory and calls it once. The recorded time covers that call; it excludes later GUI rendering and report export. I have used these timings to describe the runs, not as performance benchmarks. I have included the scripts and source-level checks with the submission.',
 'I compared equal quantities and units, allowing displayed rounding. I did not equate a selected grade name with proof that all its properties reached every calculation. Videos were recorded, but this report is based on the supplied still images, files and logs; the recordings were not independently reviewed.': 'I compared values in the same units and allowed for rounding in the display. I also checked beyond the selected grade name, because a correct name does not prove that every calculation used the entered properties. I recorded videos separately. The comparisons in this report use my screenshots, saved files and logs; the video files were not independently reviewed for this report.',
 'T03 contributes three consecutive runs in one session. Across the register, seven completed designs are evidenced: T01, T02, T03-R1/R2/R3, T05C and T06-D. Five have recorder success records. T05 is not counted as a verified 300/75 design. No overall percentage is computed from mixed functional checks and engineering results.': 'I completed the three T03 runs in one session. The evidence supports seven completed designs: T01, T02, T03-R1/R2/R3, T05C and T06-D. Five have recorder success records. I have not counted T05 as a verified 300/75 design or combined the functional checks and engineering results into one pass percentage.',
 'Valid design cases use Highway Bridge, Chennai (Minambakkam) (A), Tamil Nadu, Optimized design, no median and no footpath. T05 has no basic-input screenshot and stores a null skew; I preserve that distinction instead of normalizing it to the intended zero.': 'For the valid design cases, I used Highway Bridge, Chennai (Minambakkam) (A), Tamil Nadu, Optimized design, no median and no footpath. T05 has no basic-input screenshot and stores a null skew. I have kept that value in the record rather than replacing it with the intended zero.',
 'The 25 m cases use four physical girders, 2.1 m spacing and 1.05 m overhang in the executed/saved baseline layout. T06 uses four physical girders, 2.475 m spacing and 1.2375 m overhang. Its width is approximately 9.9 m. Additional preview values in the inconclusive T05 attempt differ and are not substituted for the executed state.': 'In the executed or saved baseline layout, I found four physical girders with 2.1 m spacing and 1.05 m overhang for the 25 m cases. T06 uses four physical girders, 2.475 m spacing and 1.2375 m overhang, giving an overall width of approximately 9.9 m. The T05 preview shows different values. I have kept those preview values separate from the executed state.',
 'Wearing-course density is 24 kN/m3 in several saved baseline OSIs, but 25 kN/m3 in the UI and captured direct-design input states. This difference is documented rather than silently reconciled. T05C and T06 retain 25 kN/m3 through execution.': 'I noticed that several saved baseline OSIs contain a wearing-course density of 24 kN/m3, while the UI and captured direct-design inputs contain 25 kN/m3. I have recorded both values. T05C and T06 retain 25 kN/m3 through execution.',
 'T02 before/after OSIs are identical, and the property dialogs show the selected custom values. T03, T05C and T06 retain material keys through the design call. Yet the runtime girder density is 78,500 N/m3 instead of the entered 77,000 N/m3. A correct dictionary label is therefore not enough to mark downstream material use as passed.': 'I compared the T02 OSIs before and after the run and found them identical. The property dialogs also showed my custom values. T03, T05C and T06 retained the material keys through the design call, but the runtime girder density was 78,500 N/m3 instead of the entered 77,000 N/m3. This is why I checked how the values were used, as well as whether they remained in the dictionary.',
 'In T06, all material.* values match across input-before, input-after and output. The runtime girder E/Fy/Fu and concrete fck/fctm/Ecm match after conversion. Separate member-design material objects were not captured; source review identifies fixed CLI-template material fields needing component-specific propagation.': 'In T06, I found that all material.* values matched across input-before, input-after and output. The runtime girder E/Fy/Fu and concrete fck/fctm/Ecm also matched after unit conversion. I did not capture the separate member-design material objects. During source review, I found fixed CLI-template material fields that need to receive the properties of the relevant component.',
 'The T01 Girder 1/SW screen shows RB = 14.17 kN in its field but 19.3 kN on the sketch. The same class of inconsistency is reproduced with stronger recorder evidence in T06 and reported in ': 'In T01, I noticed that the Girder 1/SW screen showed RB = 14.17 kN in the field but 19.3 kN on the sketch. I found the same type of mismatch in T06, where I had recorder evidence, and reported it in ',
 'Both reports contain failed checks despite completed execution. T01 also shows total deflection up to 56.704 mm against a displayed limit of about 41.7 mm. T02 reduces the comparable maximum to 55.321 mm, still above that limit. The material change affects selected results, but multiple properties changed together, so this is not an isolated sensitivity study.': 'Both runs completed, but I found failed checks in both reports. T01 shows total deflection up to 56.704 mm against a displayed limit of about 41.7 mm. In T02, the comparable maximum falls to 55.321 mm, which is still above the limit. Several material properties changed together, so I cannot attribute this change to one property alone.',
 'T01/T02 have no captured live backend dictionaries. Their detailed notes distinguish UI, saved-file and report evidence and retain every saved input in an appendix. Later recorder evidence supplies the stronger runtime checks.': 'I did not capture live backend dictionaries for T01/T02. In their detailed notes, I have separated the UI, saved-file and report evidence and included every saved input in an appendix. I used the recorder in later tests to check runtime values.',
 'This passes the tested change-and-return sequence. It does not prove all consecutive-run scenarios are stable. The span edit also regenerates suggested sections: 84 before-input fields change between R1 and R2, so the raw dictionaries do not differ only in span.': 'This sequence passed: I could change the span and return to the original span without restarting. I have not treated one sequence as proof that every consecutive-run scenario is stable. Changing the span also regenerated suggested sections; 84 before-input fields changed between R1 and R2, not just the span field.',
 'All three designs report engineering FAIL. The screenshots are cropped and omit member/load selectors, so the visible deflection values are not labelled as a verified total-load case. Runtime lengths and plot axes provide direct evidence of the geometry update.': 'All three designs reported engineering FAIL. My plot screenshots are cropped and do not show the member/load selectors, so I have not labelled their deflection values as a verified total-load case. I used the runtime lengths and plot axes to confirm the geometry update.',
 'The source OSI is byte-identical to T03-R3 after-save. Exactly five of its 580 saved values change, all under material.deck. On the third recorded attempt, Design stops because material.deck.fck is missing. The first two attempts contain cancellation messages and are retained as cancelled attempts, not unexplained crashes.': 'I checked the source OSI against the T03-R3 after-save file and found them byte-identical. After reload, exactly five of the 580 saved values changed, all under material.deck. On the third recorded attempt, Design stopped because material.deck.fck was missing. The first two attempts contain cancellation messages, so I have recorded them as cancelled attempts.',
 'The app remains usable after the steel-info exception: I can open the deck dialog and attempt Design. The correct classification is a dialog callback exception followed by a handled design error.': 'After the steel-info exception, I could still open the deck dialog and attempt Design. I have therefore recorded a dialog callback exception followed by a handled design error, rather than a complete application crash.',
 'Loading does not rebuild InputDock._material_custom_fields. Later material priming can replace saved values with defaults. In material_properties.py:751, a custom-name branch also reaches defaults before assignment. Restore complete per-component properties on load; validate incomplete custom materials; initialize dialog locals safely. Fixing only the exception does not restore lost data.': 'In the source, I found that loading does not rebuild InputDock._material_custom_fields. Later material priming can replace the saved values with defaults. In material_properties.py:751, a custom-name branch also reaches defaults before assignment. I suggest restoring the complete properties for each component on load, checking incomplete custom materials and initializing the dialog variables safely. Fixing only the exception would not restore the lost data.',
 'The failure outputs are partial and must not be treated as completed design results.': 'I have kept these partial failure outputs separate from completed design results.',
 'Tester-observed retained values': 'Values I observed after dialog Save',
 'User values before main Save Input': 'Values I entered before Save Input',
 'T05 has no numbered recorder run. Its component screenshots are useful for the displayed 250 mm state, but I do not count it as a successful 300 mm design. T05B isolates the main Save Input action. T05C then bypasses that action and verifies 300/75 through the backend and report.': 'I do not have a numbered recorder run for T05. Its component screenshots show the 250 mm state, so I have not counted it as a successful 300 mm design. I used T05B to isolate the main Save Input action. In T05C, I went directly to Design after saving the dialog and verified 300/75 in the backend and report.',
 'T05C returned in 31.48 s without a captured exception. Its deck bottom/top/shear ratios 0.866/0.470/0.646 match the GUI 87%/47%/65% after rounding. The overall engineering status remains FAIL, with fatigue DCR 2.1776.': 'T05C returned in 31.48 s without a captured exception. I compared its deck bottom/top/shear ratios of 0.866/0.470/0.646 with the displayed 87%/47%/65% and found that they matched after rounding. The overall engineering status was still FAIL, with fatigue DCR 2.1776.',
 'The case uses distinct girder, cross-bracing and end-diaphragm grades. The before/after inputs each contain 588 keys; the output contains 1,070. Thirty-five input changes relate to section normalization and optimized thickness resolution; the targeted geometry/material fields remain intact.': 'For this case, I selected different grades for the girder, cross bracing and end diaphragm. The before/after inputs each contain 588 keys, and the output contains 1,070. I found 35 input changes related to section normalization and optimized thickness resolution. The geometry and material fields I was checking remained intact.',
 'The CAD screenshot demonstrates generation, not dimensional metrology. A 10-degree input and runtime angle do not by themselves establish that every solid in the rendered model has the correct skew.': 'I confirmed that the CAD model was generated and could be rotated. I did not measure every solid in the model, so the 10-degree input and runtime angle alone do not verify the skew of every rendered component.',
 'The file named 06_end_stiffner_results is an end-diaphragm view, not a bearing-stiffener check. I classified evidence by its visible content. The table above distinguishes component coverage from complete verification of every component equation.': 'I noticed that the file named 06_end_stiffner_results actually shows the end-diaphragm view. I used the visible content to classify it. The table records what I checked for each component; it does not claim that I verified every design equation.',
 'After saving Additional Inputs with a 300 mm deck and 75 mm wearing course, the main Save Input action serializes 250/50. The intended values can survive direct Design, as T05C establishes. This makes the reset a specific save-path defect rather than a blanket claim that custom thickness is unsupported.': 'I saved a 300 mm deck and 75 mm wearing course in Additional Inputs. When I then used the main Save Input button, the saved file contained 250/50. T05C showed that direct Design could retain 300/75. I therefore reported this as a problem in the save path, rather than saying that custom thicknesses never work.',
 'This guard illustrates non-destructive insertion for user-editable defaults. A complete correction must separate initialization, derived-layout recomputation and saving. Copying the dictionary before the existing destructive function would protect the live state but still save the wrong values. Applying a guard indiscriminately to derived values could also prevent necessary recomputation.': 'I suggest this guard for inserting defaults into user-editable fields without overwriting entered values. The complete fix still needs to separate initialization, derived-layout recomputation and saving. Copying the dictionary before calling the current function would protect the live state but still save the wrong values. Applying the guard to every derived value could also stop necessary recomputation.',
 'Keep 300/75 through save, reload and repeated save; fill genuinely absent optional defaults; recompute dependent geometry when its sources change. Also test cancelling Save, since the current mutation occurs before the file dialog. Cancellation is a source-derived risk, not a desktop scenario I executed.': 'For regression testing, I would check that 300/75 survives save, reload and repeated save; missing optional defaults are filled; and dependent geometry is recalculated when its inputs change. I would also check cancelling Save because the mutation occurs before the file dialog opens. I identified that cancellation risk from the source; I did not execute it as a desktop test.',
 'The core dictionaries contain different results, so this is not simply two components happening to receive equal checks. The source merge and the screenshot comparison establish the substitution. ': 'I found different results in the two core dictionaries, but the end-diaphragm screen repeated the cross-bracing values. Comparing the source merge with the screenshots confirmed the substitution. ',
 'Keep component results and governing forces separate at initial load and every refresh. Replacing setdefault with update merely reverses which tab is wrong. The included AST-based review script executes the actual merge statements against the captured output and reproduces all four substitutions; it does not launch Qt or run another analysis.': 'I suggest keeping each component\'s results and governing forces separate when the dialog loads and refreshes. Replacing setdefault with update would only make the other tab wrong. The included AST-based script executes the actual merge statements against the captured output and reproduces all four substitutions. It does not launch Qt or run another analysis.',
 'Retrieve reactions once and share the record between both displays. Handle unavailable data explicitly and review the extractor fallback against actual support nodes.': 'I suggest retrieving the reactions once and using that record for both displays. Missing data should be shown explicitly, and the extractor fallback should be checked against the actual support nodes.',
 'Use the validated KEY_CB_WIDTH value and a deliberate missing-value policy. Test propagation for multiple accepted widths and dependent layout updates. The mismatch is confirmed; its structural effect has not been quantified.': 'I suggest using the validated KEY_CB_WIDTH value and handling a missing value explicitly. I would check several accepted widths and the dependent layout updates after the change. I confirmed the mismatch, but I have not quantified its structural effect.',
 'The input and output retain 77, but _build_material_props() falls back to 78,500 when custom-grade lookup returns no database density. Read the validated custom key and convert kN/m3 to N/m3 once. A regression should expect 77,000 and check self-weight with section and geometry held fixed.': 'I found 77 in the input and output, but _build_material_props() falls back to 78,500 when the custom-grade lookup returns no database density. I suggest reading the validated custom key and converting kN/m3 to N/m3 once. A regression test should expect 77,000 and check self-weight while keeping the section and geometry fixed.',
 'T05C adds a separate deck-design path to the existing analysis-load issue. deckdesign.py:516 reads the code-table density and multiplies by 9.81 rather than using custom weight density. Pass the same validated density into both analysis and deck design; do not apply a second gravity conversion to a kN/m3 input.': 'In T05C, I found another path related to the existing analysis-load issue. The deck-design calculation in deckdesign.py:516 reads a code-table density and multiplies it by 9.81 instead of using my custom weight density. I suggest passing the same validated density into analysis and deck design, without applying another gravity conversion to an input already in kN/m3.',
 'The comments contain evidence and proposed regression checks. No isolated component-strength sensitivity test or patched material calculation was performed.': 'I included evidence and proposed regression checks in my comments. I did not run an isolated component-strength sensitivity test or validate a patched material calculation.',
 'Generate success/failure wording from evaluated checks, with an unavailable state for missing data. Use the selected material name and strength for quantity labels. Define units at the report-data boundary and distinguish pre-design UI inputs from optimized results; multiplying every value by 1000 would corrupt values already in millimetres.': 'I suggest generating the pass/fail wording from the evaluated checks and showing an unavailable state when data is missing. The quantity labels should use the selected material name and strength. Units also need to be defined where data enters the report, with pre-design inputs kept separate from optimized results. Multiplying every value by 1000 would give incorrect results for values already in millimetres.',
 'This is functional testing and consistency review. It is not an independent certification of the bridge design equations or compliance with every cited engineering standard. A failing engineering check alone is not classified as a software defect; contradictory displays, lost inputs and incorrect propagation are reported separately.': 'I have treated this work as functional testing and consistency checking. I have not independently certified the bridge-design equations or compliance with every cited engineering standard. I also have not counted a failed engineering check alone as a software defect. My bug reports concern contradictory displays, lost inputs and values that do not reach the intended calculation.',
 'The original issues were prepared after checking open/closed reports and related discussions. Existing issues are credited as existing work; the six comments above are my additions. The full URLs, post text and author metadata are preserved in issues/github_posts.json and issues/LIVE_ISSUES.md.': 'I checked open and closed issues and related discussions before preparing new reports. Where an existing issue covered the problem, I added my findings as a comment. The six comments listed above are my additions to those existing reports. I have kept the full URLs, post text and author metadata in issues/github_posts.json and issues/LIVE_ISSUES.md.',
 'All ten posts now include file-attachment links. The same original evidence is included in this submission, so review does not depend solely on GitHub attachment availability. No code fix is claimed as merged or validated.': 'All ten posts include file-attachment links. I have also included the same original evidence in this submission so it can be reviewed without relying only on the GitHub attachments. My code changes are suggestions; I have not claimed that they are merged or validated.',
 'I would address input preservation and component-result routing first, then material/runtime propagation and consistent status reporting. A useful regression suite should exercise serialization/reload, separate component result maps, custom material payloads and the full three-run change-and-return sequence.': 'I would first fix the lost inputs and the incorrect component results shown in the UI. Next, I would check custom-material propagation and report status wording. For regression testing, I would include save/reload, separate component result maps, custom-material payloads and the full three-run change-and-return sequence.',
 'Original filenames and file bytes are retained. Case-note statements such as “next test” or “not yet posted” reflect when those notes were written; the published issue register in this final report supersedes their reporting status. The original generated application reports remain unchanged even where this review identifies errors in them.': 'I have kept the original evidence filenames and file bytes unchanged. Some case notes say “next test” or “not yet posted” because I wrote them while testing. The issue register in this final report gives the updated reporting status. I have also kept the original application-generated reports unchanged, including the errors discussed here.',
 'My conclusion is that the tested workflow can complete repeated designs and generate inspectable outputs, but input persistence, material propagation and output consistency need correction. The retained successful checks and failures make those boundaries reproducible rather than hiding them behind a single pass/fail label.': 'From these tests, I found that the module can complete repeated designs and generate CAD models, plots and reports. I also found problems with saved inputs, custom-material use and consistency between outputs. I have kept both the successful checks and the failures, along with the files needed to repeat them. This gives a clearer record of what worked and what still needs correction.',
 'Rebuilds this report from the packaged evidence; requires reportlab, Pillow, PyMuPDF and DejaVu fonts.': 'Rebuilds this report from the packaged evidence; requires ReportLab and Pillow and uses standard Helvetica/Courier fonts.',
 'Live links and verification snapshot; issues are external, not locally invented IDs.': 'Links to my published issues/comments and the saved verification snapshot.',
 'Rotation confirmed by tester': 'I confirmed rotation',
 'reset confirmed by tester': 'I confirmed the reset',
 'No invented all-pass bridge case': 'No verified all-pass bridge case',
 'Tested source recorded from T03 onward:': 'Source revision recorded from T03 onward:',
 'What retention does and does not establish': 'What I checked after the run',
 'Observations not resolved into calculation-bug claims': 'Observations I could not fully resolve',
 'Regression expectations': 'Checks I would run after the fix',
 'Review priorities': 'What I would fix first',
}


def revise(s):
    for a,b in REVISIONS.items():s=s.replace(a,b)
    return s.replace('color="#126B70"','color="#000000"')
def para(s,style='body'):
    s=revise(s)
    if style=='body' and ('.py' in s or '_material_' in s):style='left'
    story.append(Paragraph(s,styles[style]));md.append(mdtext(s)+'\n')
def heading(s):
    s=revise(s);story.append(Paragraph(s,styles['h3']));md.append('### '+plain(s)+'\n')
def table(headers,rows,widths=None):
    global table_no
    table_no+=1
    widths=[W/len(headers)]*len(headers) if widths is None else [v*W/sum(widths) for v in widths]
    data=[[Paragraph(escape(str(x)),styles['head']) for x in headers]]+[[Paragraph(revise(str(x)),styles['cell']) for x in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
        ('LINEABOVE',(0,0),(-1,0),.7,black),('LINEBELOW',(0,0),(-1,0),.6,black),
        ('LINEBELOW',(0,1),(-1,-1),.25,HexColor('#B3B3B3')),('LINEBELOW',(0,-1),(-1,-1),.7,black)]))
    story.extend([KeepTogether([t]) if len(rows)<=7 else t,Spacer(1,13)])
    md.append('| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(mdtext(revise(str(v))).replace('\n',' ') for v in row)+' |' for row in rows)+'\n')
def pic(path,caption,maxh=230,width=W):
    global figure_no
    figure_no+=1
    path=Path(path);im=PILImage.open(path);w,h=im.size
    height=310
    if 'stiffener_results' in path.name:height=265
    if 'validation' in path.name:height=260
    factor=min(W/w,height/h)
    caption=f'Figure {chapter_no}.{figure_no}: '+revise(caption)
    story.append(KeepTogether([Spacer(1,6),Image(str(path),w*factor,h*factor,hAlign='CENTER'),Paragraph(caption,styles['caption'])]))
    md.append('!['+plain(caption)+'](../'+path.relative_to(ROOT).as_posix()+')\n')
def pairpics(paths,captions,maxh=210):
    for path,cap in zip(paths,captions):pic(path,cap,maxh)
def code(s):
    story.append(Paragraph(escape(s).replace('\n','<br/>').replace(' ','&nbsp;'),styles['code']))
    md.append('```python\n'+s+'\n```\n')
CHAPTERS={
 0:'Introduction and test setup',
 3:'Inputs and material properties',
 5:'Test observations',
 11:'Bugs and code review',
 16:'Coverage and published issues',
 18:'Reproduction and conclusion',
}
TITLES={0:'Overview',1:'Method and environment',2:'Complete test register',3:'Geometry and additional inputs',4:'Material properties',5:'T01 and T02: baseline and custom materials',6:'T03: three consecutive runs',7:'T04: saved custom materials after reload',8:'T05, T05B and T05C: additional inputs',9:'T06: validation and skew-bridge run',10:'Structural-component coverage',11:'Save Input resets thickness values',12:'End-diaphragm results in the wrong tab',13:'Support reactions and barrier width',14:'Further evidence on material issues',15:'Report errors and unresolved observations',16:'Requirement coverage and limits',17:'Published issue register',18:'Reproducing the tests and reviewing the evidence'}
def page(title,sub):
    global chapter_no,sub_no,figure_no
    idx=len(sections);sections.append(title)
    if idx in CHAPTERS:
        chapter_no+=1;sub_no=0;figure_no=0
        story.extend([PageBreak(),Spacer(1,92)])
        story.append(Paragraph(f'Chapter {chapter_no}',styles['chapter']))
        p=Paragraph(CHAPTERS[idx],styles['h1']);p._toc_level=0;p._toc_label=f'{chapter_no}  {CHAPTERS[idx]}';p._bookmark=f'chapter-{chapter_no}'
        story.append(p);md.append(f'\n# Chapter {chapter_no}: {CHAPTERS[idx]}\n')
    sub_no+=1
    label=f'{chapter_no}.{sub_no}  {TITLES[idx]}'
    p=Paragraph(label,styles['h2']);p._toc_level=1;p._toc_label=label;p._bookmark=f'section-{idx}'
    story.extend([CondPageBreak(155),p]);md.append('## '+label+'\n')
    if idx in (5,6,7,8,9,11,12,13,17):para(sub,'small')
def issue(n,label=None):return f'<a href="https://github.com/Nidhikhare12/OsdagBridge/issues/{n}" color="#000000">'+(label or f'Issue #{n}')+'</a>'
def source(path,line):return f'<a href="https://github.com/Nidhikhare12/OsdagBridge/blob/d74f56dd7f22925fb8148cabf5740ed8d1e39ff3/src/osdagbridge/{path}#L{line}" color="#000000">{path}:{line}</a>'
posts=json.loads((ROOT/'issues/github_posts.json').read_text())
def comment(n):
    x=next(x for x in posts if x['kind']=='comment' and x['issue_url'].endswith('/'+str(n)))
    return f'<a href="{x["url"]}" color="#000000">My supporting comment on #{n}</a>'
T05=E/'T05/session_20261110_202805_071320'
T05C=E/'T05C';T06=E/'T06'

story.append(Spacer(1,105))
story.append(Paragraph('OsdagBridge<br/>Functional Testing Report',styles['title']))
story.append(Paragraph('Short-span steel girder bridge module',styles['centre']))
story.append(Spacer(1,32))
story.append(Paragraph('FOSSEE Winter Internship Screening Task',styles['centre']))
story.append(Spacer(1,55))
story.append(Paragraph('<b>Harish Raghav S</b><br/>B.Tech Computer Science and Engineering<br/>SASTRA University',styles['centre']))
story.append(Spacer(1,32))
story.append(Paragraph('Tests carried out: 8-11 November 2026<br/>Report date: 11 November 2026',styles['centre']))
story.append(PageBreak())
story.append(Paragraph('Contents',styles['h1']))
toc=TableOfContents()
toc.levelStyles=[ParagraphStyle('TOCChapter',fontName='Helvetica-Bold',fontSize=11,leading=13,spaceBefore=6,spaceAfter=0),ParagraphStyle('TOCSection',fontName='Helvetica',fontSize=10,leading=11.5,leftIndent=18,firstLineIndent=0,spaceBefore=0,spaceAfter=0)]
story.append(toc)
md.append('# OsdagBridge Functional Testing Report\n\nHarish Raghav S | SASTRA University | 11 November 2026\n')

page('OsdagBridge\nFunctional Testing Report','FOSSEE winter internship screening | Short-span steel girder bridge module')
table(['Case groups','Recorded checks / attempts','New GitHub issues','Supporting comments'],[['8','14','4','6']])
para('I tested default and custom materials, repeated designs in one session, saved-input reloads, additional-input persistence and a skew bridge. The application produced useful results, CAD and plots, but several input and display paths did not preserve or represent the intended data correctly.')
para('The strongest findings are a reproducible Save Input reset, end-diaphragm results replaced by cross-bracing values in the UI, inconsistent support-reaction displays, and a runtime crash-barrier width that differs from the input. All four have published reports with source-level explanations.')
para('<b>Reading the results:</b> successful execution is recorded separately from structural adequacy. The completed cases reviewed here contain failed engineering checks; I do not describe them as safe bridge designs.')
para('<b>Repository:</b> <a href="https://github.com/HR5206/OsdagBridge" color="#126B70">github.com/HR5206/OsdagBridge</a><br/><b>Tested source recorded from T03 onward:</b> d74f56dd7f22925fb8148cabf5740ed8d1e39ff3','small')

page('01 / Scope and method','What the evidence establishes, and how I kept the comparisons reproducible')
para('I used the desktop application for the manual tests and retained original screenshots, saved OSI inputs and generated reports. From T03 onward, a recorder captured input/output dictionaries around the core design call, selected runtime properties, exceptions, timing and source metadata.')
table(['Evidence layer','What I used it to check'],[
 ['UI screenshots and interaction notes','Entered values, visible outputs, validation warnings, CAD rotation and opening plots.'],
 ['Saved .osi files','Serialization and reload fidelity; complete saved parameter combinations.'],
 ['Before/after JSON and runtime objects','Actual inputs supplied to Design, result changes and selected material/geometry propagation.'],
 ['Generated PDFs','Agreement with the displayed inputs, dictionary outputs and reported design status.'],
 ['Source inspection and isolated checks','Specific explanations for anomalies and proposed regression checks. These are distinct from desktop runs.']],[145,362])
heading('Environment and provenance')
para('Recorder sessions identify Windows 11 and Python 3.12.16 from conda-forge. Source metadata identifies commit d74f56d and only untracked evidence directories. T01 and T02 did not capture their installed revision or operating-system release; I have not retrospectively assigned the later revision to them.')
para('The recorder wraps the original design method in memory and calls it once. Its core-call timings exclude later GUI rendering and report export and are not performance benchmarks. The scripts and source-level checks are included with this submission.')
heading('Status conventions')
para('<b>PASS</b> means the stated functional check passed. <b>FAIL</b> identifies an observed defect or a software-reported engineering failure, with the category made explicit. <b>Cancelled</b> retains a cancellation outcome without calling it an unexpected crash. <b>Inconclusive</b> means the supplied evidence does not establish the intended scenario.')
para('I compared equal quantities and units, allowing displayed rounding. I did not equate a selected grade name with proof that all its properties reached every calculation. Videos were recorded, but this report is based on the supplied still images, files and logs; the recordings were not independently reviewed.')

page('02 / Complete test register','Every documented case, validation check and recorder attempt is retained')
table(['Case / date','Action or scenario','Observed outcome'],[
 ['T01 / 8 Nov','25 m default-grade baseline','Completed; CAD/plot/PDF generated. Reported engineering FAIL.'],
 ['T02 / 8 Nov','25 m; custom steel and concrete','Material UI/OSI retention passed; CAD rotation worked. Engineering FAIL.'],
 ['T03-R1 / 10 Nov','First run, span 25 m','Core returned; numerical baseline recorded.'],
 ['T03-R2 / 10 Nov','Unlock/change span to 20 m','Core returned; geometry, plots and numerical outputs changed.'],
 ['T03-R3 / 10 Nov','Unlock/return span to 25 m','Core returned; R1 numerical output reproduced, apart from report timestamp.'],
 ['T04-A1 / 10 Nov','Reloaded custom-material session; run 01','Cancelled: RuntimeError with cancellation message; 67.24 s.'],
 ['T04-A2 / 10 Nov','Same session; run 02','Cancelled: same cancellation message; 65.38 s.'],
 ['T04-A3 / 10 Nov','Same session; run 03','Design error: required material.deck.fck missing; 63.50 s.'],
 ['T05 / 10 Nov','Intended deck 300 / wearing course 75 mm','Inconclusive intended run: saved/results state is 250/50; no captured core call.'],
 ['T05B / 10 Nov','Isolate main Save Input action','FAIL: 300/75 becomes 250/50 in saved input. No design run.'],
 ['T05C / 11 Nov','300/75, direct Design after dialog Save','PASS for retention and deck output consistency; engineering FAIL.'],
 ['T06-V1 / 11 Nov','Enter span 19 m','PASS: range warning and reset; subsequent screenshot shows 20.0 m.'],
 ['T06-V2 / 11 Nov','Enter skew 16 degrees','PASS: range warning; reset confirmed by tester. Exact replacement not captured.'],
 ['T06-D / 11 Nov','30 m, 9 m width, skew 10; distinct materials','Core returned; CAD rotation/plots worked. UI/data defects and engineering FAIL.']],[90,171,246])
para('T03 contributes three consecutive runs in one session. Across the register, seven completed designs are evidenced: T01, T02, T03-R1/R2/R3, T05C and T06-D. Five have recorder success records. T05 is not counted as a verified 300/75 design. No overall percentage is computed from mixed functional checks and engineering results.','small')

page('03 / Geometry and input profiles','Exact combinations are preserved in the original OSI / input_before.json files')
table(['Case','Span / width / skew','Deck / wearing course','Materials'],[
 ['T01','25 m / 7.5 m / 0 deg','250 / 50 mm','Steel A; concrete A'],
 ['T02','25 / 7.5 / 0','250 / 50','Steel B for all steel; concrete B'],
 ['T03-R1, R3','25 / 7.5 / 0','250 / 50','B / B'],
 ['T03-R2','20 / 7.5 / 0','250 / 50','B / B'],
 ['T04 source','25 / 7.5 / 0','250 / 50','B / B before reload loss'],
 ['T05 saved','25 / 7.5 / null','250 / 50; UI intended 300/75','B / B'],
 ['T05B intended','25 / 7.5 / 0','300 / 75; save resets to 250/50','B / B'],
 ['T05C','25 / 7.5 / 0','300 / 75','B / B'],
 ['T06-D','30 / 9 / 10','300 / 75','Girder B; CB C; ED D; concrete B']],[84,149,166,108])
para('Valid design cases use Highway Bridge, Chennai (Minambakkam) (A), Tamil Nadu, Optimized design, no median and no footpath. T05 has no basic-input screenshot and stores a null skew; I preserve that distinction instead of normalizing it to the intended zero.')
heading('Additional inputs and loading')
para('The 25 m cases use four physical girders, 2.1 m spacing and 1.05 m overhang in the executed/saved baseline layout. T06 uses four physical girders, 2.475 m spacing and 1.2375 m overhang. Its width is approximately 9.9 m. Additional preview values in the inconclusive T05 attempt differ and are not substituted for the executed state.')
para('The saved baseline enables Class A, AA wheeled/tracked, 70R wheeled/tracked/bogie, SV and fatigue vehicle flags, with no custom vehicles. Self-weight factor is 1.0, eccentricity 1.2 m, reinforcement Fe 500, top/bottom/side cover 50 mm and fatigue cycles 2,000,000. The exact wind, seismic, member and partial-factor settings remain in each full input file; these were not all varied independently.')
para('Wearing-course density is 24 kN/m3 in several saved baseline OSIs, but 25 kN/m3 in the UI and captured direct-design input states. This difference is documented rather than silently reconciled. T05C and T06 retain 25 kN/m3 through execution.')

page('04 / Material properties','Profiles used in the preceding table; values are in the UI units')
table(['Steel property','A: E 350A','B: custom 345/500','C: custom 275/430','D: custom 355/510'],[
 ['Density, kN/m3','76.4','77.0','77.2','78.0'],['Fy, MPa','350','345','275','355'],['Fu, MPa','490','500','430','510'],['E, GPa','200','205','200','210'],['G, GPa','76.9','78.8','76.9','80.8'],['Poisson ratio','0.30','0.30','0.30','0.30'],['Thermal, x10^-6 / deg C','11.7','11.7','12.0','12.1']],[130,83,98,98,98])
para('Full custom names: B = custom_steel_345_500; C = custom_steel_275_430; D = custom_steel_355_510. Profile A values are from the T01 saved OSI. Profiles C and D were used in T06 to distinguish cross-bracing and end-diaphragm material paths.','small')
table(['Concrete property','A: M40','B: custom_concrete_45_3.5'],[
 ['Density, kN/m3','24.5','25.5'],['Cube strength fck, MPa','40','45'],['Mean tensile strength fctm, MPa','3.0','3.5'],['Secant modulus Ecm, GPa','33','35'],['Thermal, x10^-6 / deg C','11.7','10.5']],[215,90,202])
heading('What retention does and does not establish')
para('T02 before/after OSIs are identical, and the property dialogs show the selected custom values. T03, T05C and T06 retain material keys through the design call. Yet the runtime girder density is 78,500 N/m3 instead of the entered 77,000 N/m3. A correct dictionary label is therefore not enough to mark downstream material use as passed.')
para('In T06, all material.* values match across input-before, input-after and output. The runtime girder E/Fy/Fu and concrete fck/fctm/Ecm match after conversion. Separate member-design material objects were not captured; source review identifies fixed CLI-template material fields needing component-specific propagation.')

page('05 / Baseline and custom retention','T01 and T02 | 8 November 2026')
pairpics([E/'T01/04_result_cad.png',E/'T02/04_steel_after.png'],['T01: generated bridge CAD (original screenshot).','T02: retained custom steel properties after the run.'],210)
table(['Check','T01 baseline','T02 custom materials'],[
 ['Geometry / steel / deck','25 m / E 350A / M40','25 m / custom steel B / concrete B'],
 ['Evidence of completion','Log: analysis complete; 125.99 s','Generated model and PDF; exact duration not captured'],
 ['Input evidence','576-key saved OSI','580-key before/after OSIs; identical'],
 ['CAD interaction','Model visible; rotation not attributed to this case','Rotation confirmed by tester'],
 ['Engineering outcome','Report FAIL; max girder UR about 2.00','Report FAIL; fatigue about 2.00'],
 ['Selected output comparison','SW moment 97.318 kNm in report; UI 97.32','Moment resistance 6907.037 kNm vs baseline 6863.47']],[130,185,192])
para('The T01 Girder 1/SW screen shows RB = 14.17 kN in its field but 19.3 kN on the sketch. The same class of inconsistency is reproduced with stronger recorder evidence in T06 and reported in '+issue(73)+'.')
para('Both reports contain failed checks despite completed execution. T01 also shows total deflection up to 56.704 mm against a displayed limit of about 41.7 mm. T02 reduces the comparable maximum to 55.321 mm, still above that limit. The material change affects selected results, but multiple properties changed together, so this is not an isolated sensitivity study.')
para('T01/T02 have no captured live backend dictionaries. Their detailed notes distinguish UI, saved-file and report evidence and retain every saved input in an appendix. Later recorder evidence supplies the stronger runtime checks.','small')

page('06 / Three consecutive runs','T03 | One session, 25 m -> 20 m -> 25 m')
table(['Quantity','R1: 25 m','R2: 20 m','R3: 25 m'],[
 ['Core-call duration, s','131.52','68.41','136.86'],['Runtime span, m','25','20','25'],['Transverse mesh count','18','14','18'],['Girder depth / flange width, mm','1390 / 420','1120 / 340','1390 / 420'],['Visible plot Dy, mm','-3.70','-2.32','-3.70'],['Fatigue ratio','1.9985','2.2152','1.9985'],['Core exception','None','None','None']],[186,107,107,107])
pairpics([E/'T03/run_01/R1_deflection.png',E/'T03/run_02/R2_deflection.png'],['R1 plot: span 25 m; visible Dy -3.70 mm.','R2 plot: span 20 m; visible Dy -2.32 mm.'],170)
para('After each completed design, I unlocked the inputs, changed the span and ran again without restarting. The final 25 m run reproduced R1: parsed input-before dictionaries are equal; output dictionaries differ only in the generated timestamp inside design_results.report_text. R2 changes 163 top-level output entries.')
para('This passes the tested change-and-return sequence. It does not prove all consecutive-run scenarios are stable. The span edit also regenerates suggested sections: 84 before-input fields change between R1 and R2, so the raw dictionaries do not differ only in span.')
para('All three designs report engineering FAIL. The screenshots are cropped and omit member/load selectors, so the visible deflection values are not labelled as a verified total-load case. Runtime lengths and plot axes provide direct evidence of the geometry update.','small')

page('07 / Saved custom materials after reload','T04 | Fresh-session load exposes a dialog exception and loss of concrete properties')
table(['Concrete key','Source OSI','Re-saved state'],[['density','25.5','24.5'],['fck','45','null'],['fctm','3.5','null'],['ecm','35','null'],['thermal','10.5','11.7']],[235,136,136])
pairpics([E/'T04/02_info_button_error.txt.png',E/'T04/03_deck_info.png'],['Steel info callback: UnboundLocalError for defaults.','Concrete info: custom name remains, strength/modulus blank.'],180)
para('The source OSI is byte-identical to T03-R3 after-save. Exactly five of its 580 saved values change, all under material.deck. On the third recorded attempt, Design stops because material.deck.fck is missing. The first two attempts contain cancellation messages and are retained as cancelled attempts, not unexplained crashes.')
para('The app remains usable after the steel-info exception: I can open the deck dialog and attempt Design. The correct classification is a dialog callback exception followed by a handled design error.')
heading('Cause and proposed correction')
para('Loading does not rebuild InputDock._material_custom_fields. Later material priming can replace saved values with defaults. In material_properties.py:751, a custom-name branch also reaches defaults before assignment. Restore complete per-component properties on load; validate incomplete custom materials; initialize dialog locals safely. Fixing only the exception does not restore lost data.')
para(comment(19)+' includes the OSIs, screenshots and run_03 traceback. The failure outputs are partial and must not be treated as completed design results.','small')

page('08 / Additional inputs: failed save, successful run','T05, T05B and T05C | Keep the inconclusive attempt and the controlled follow-ups separate')
table(['Case / checkpoint','Deck thickness','Wearing course','Interpretation'],[
 ['T05 input screenshots','300 mm','75 mm','Intended values visible'],['T05 saved/result state','250 mm','50 mm','Does not establish the intended run'],['T05B after dialog Save','300 mm','75 mm','Tester-observed retained values'],['T05B after main Save Input','250 mm','50 mm','Reset reproduced in source function'],['T05C input -> output -> PDF','300 mm','75 mm','Direct Design retains intended values']],[168,90,90,159])
pic(T05C/'03_deck_thickness_result.png','T05C: the actual 300 mm deck result, with reinforcement and utilization displays.',240)
para('T05 has no numbered recorder run. Its component screenshots are useful for the displayed 250 mm state, but I do not count it as a successful 300 mm design. T05B isolates the main Save Input action. T05C then bypasses that action and verifies 300/75 through the backend and report.')
para('T05C returned in 31.48 s without a captured exception. Its deck bottom/top/shear ratios 0.866/0.470/0.646 match the GUI 87%/47%/65% after rounding. The overall engineering status remains FAIL, with fatigue DCR 2.1776.')

page('09 / Validation and skew-bridge run','T06 | Two rejected values, then one valid 30 m / 9 m / 10-degree design')
pairpics([T06/'01_span_validation.png',T06/'02_skew_validation.png'],['Span 19 m rejected: supported range 20-45 m.','Skew 16 degrees rejected: supported range -15 to 15.'],220)
para('Both warnings appeared and the fields reset. The second screenshot shows the span reset to 20.0 m. The skew replacement value is not captured; its reset is my interaction observation. Neither invalid input was submitted for design.')
table(['Valid-run check','Result'],[
 ['Runtime span / width / skew','30.0 m / 9.0 m / 10.0 degrees'],['Deck / wearing course','300 / 75 mm retained through inputs, outputs and PDF'],['Core call','152.41 s; engine_returned; no captured error'],['CAD and plots','Generated; rotation and opening plots confirmed'],['Girder 1 / SW plot','Mz 205.54 kNm; Vy 25.19 kN; Dy -5.28 mm'],['Engineering outcome','FAIL; fatigue DCR 1.8924 (189.24%)']],[188,319])
para('The case uses distinct girder, cross-bracing and end-diaphragm grades. The before/after inputs each contain 588 keys; the output contains 1,070. Thirty-five input changes relate to section normalization and optimized thickness resolution; the targeted geometry/material fields remain intact.')
para('The CAD screenshot demonstrates generation, not dimensional metrology. A 10-degree input and runtime angle do not by themselves establish that every solid in the rendered model has the correct skew.','small')

page('10 / Structural-component coverage','What I checked across the girder, deck, transverse members and stiffeners')
table(['Component','Evidence and comparison','Limit'],[
 ['Main girders','UI dimensions and SW plots; runtime materials; utilization and report tables','No independent full-code structural recalculation'],
 ['Concrete deck','Custom properties; 250/300 mm outputs; reinforcement and ratio comparisons','Density load path differs from custom input'],
 ['Cross bracing','Selected grade, section, demand/capacity/UR rows and output dictionary','Separate material propagation not verified by UI retention'],
 ['End diaphragms','Distinct output compared to UI in T06','UI substitutes cross-bracing ratios'],
 ['Intermediate / bearing stiffeners','Custom grade and dimensions visible in T05; report checks reviewed','Not a complete independent design audit'],
 ['Longitudinal stiffeners','Disabled / NA in tested configuration','Enabled configuration not tested'],
 ['Shear connectors / reinforcement','Saved dimensions and report checks retained','No separate connection-detail validation']],[110,237,160])
pic(T05/'07_stiffener_results.png','T05: intermediate and bearing stiffeners show custom grade, 10 mm thickness and 205 mm width; spacing 2030 and 100 mm respectively.',205)
para('The file named 06_end_stiffner_results is an end-diaphragm view, not a bearing-stiffener check. I classified evidence by its visible content. The table above distinguishes component coverage from complete verification of every component equation.')

page('11 / Defect: saving overwrites inputs','Published '+plain(issue(71))+' | Input persistence | Reproduced in GUI observations and an isolated source check')
para(issue(71,'Open issue #71: Save Input thickness reset'))
para('After saving Additional Inputs with a 300 mm deck and 75 mm wearing course, the main Save Input action serializes 250/50. The intended values can survive direct Design, as T05C establishes. This makes the reset a specific save-path defect rather than a blanket claim that custom thickness is unsupported.')
table(['Checkpoint','Deck, mm','Wearing course, mm'],[['User values before main Save Input','300','75'],['T05B saved OSI','250','50'],['Independent defaults-function reproduction','250','50']],[295,106,106])
heading('Source path')
para(source('desktop/ui/template_page.py',793)+' calls solve_extend_basic_input_dict(self.input_dict) before the file dialog. '+source('core/bridge_types/plate_girder/defaults.py',181)+' uses an unconditional dictionary update for defaults.')
code('def _update(key, value):\n    if input_dict.get(key) in (None, ""):\n        input_dict[key] = value')
para('This guard illustrates non-destructive insertion for user-editable defaults. A complete correction must separate initialization, derived-layout recomputation and saving. Copying the dictionary before the existing destructive function would protect the live state but still save the wrong values. Applying a guard indiscriminately to derived values could also prevent necessary recomputation.')
heading('Regression expectations')
para('Keep 300/75 through save, reload and repeated save; fill genuinely absent optional defaults; recompute dependent geometry when its sources change. Also test cancelling Save, since the current mutation occurs before the file dialog. Cancellation is a source-derived risk, not a desktop scenario I executed.')
para('scripts/reproduce_save_reset.py reads a copy of the OSI and calls the original function. Its assertion fails on the tested revision and should pass after a correct fix. No application patch has been applied or validated in this submission.','small')

page('12 / Defect: wrong end-diaphragm results','Published '+plain(issue(72))+' | UI/output dictionary consistency | G1-G2, Envelope')
table(['Check','CB output / UI','ED output','ED UI'],[['Diagonal tension','0.18','0.23','0.180'],['Diagonal compression','0.85','0.54','0.850'],['Chord tension','0.16','0.20','0.160'],['Chord compression','0.74','0.47','0.740']],[195,104,104,104])
pairpics([T06/'08_cross_bracing.png',T06/'09_end_diaphragm.png'],['Cross-bracing screen.','End-diaphragm screen repeats the CB ratios.'],180)
para('The core dictionaries contain different results, so this is not simply two components happening to receive equal checks. The source merge and the screenshot comparison establish the substitution. '+issue(72,'Open issue #72')+' contains full-size evidence.')
para(source('desktop/ui/dialogs/transverse_member_design.py',920)+' starts with a shallow copy of CB results, then attaches ED entries using setdefault. Existing diagonal/chord keys remain CB values. Both tab builders consume that merged map.')
code('self._cb_designs = deepcopy(cb_designs)\nself._ed_designs = deepcopy(ed_designs)\n# Render each tab with its own design AND force records.')
para('Keep component results and governing forces separate at initial load and every refresh. Replacing setdefault with update merely reverses which tab is wrong. The included AST-based review script executes the actual merge statements against the captured output and reproduces all four substitutions; it does not launch Qt or run another analysis.')

page('13 / Defects: reactions and runtime layout','Published issues #73 and #74 | Two independent consistency failures')
heading('Support reactions disagree within one screen')
pic(T06/'07_plot_a.png','T06 Girder 1 / SW: RB field 3.42 kN; sketch label about 16.7 kN.',255)
para(issue(73)+' traces the field to first/penultimate shear samples in steel_design.py:947, while the sketch calls engine.extract_reactions(). Retrieve reactions once and share the record between both displays. Handle unavailable data explicitly and review the extractor fallback against actual support nodes. I have not independently calculated which displayed reaction is correct.')
heading('Crash-barrier width is replaced in the runtime DTO')
table(['Location','Width'],[['Input before and after Design','0.45 m'],['Runtime deck_layout.crash_barrier_width','0.50 m']],[365,142])
para(issue(74)+' identifies _build_dtos() in plategirderbridge.py:1017, which assigns DEFAULT_CRASH_BARRIER_WIDTH. Use the validated KEY_CB_WIDTH value and a deliberate missing-value policy. Test propagation for multiple accepted widths and dependent layout updates. The mismatch is confirmed; its structural effect has not been quantified.')

page('14 / Existing material issues: added evidence','Supporting comments extend existing reports rather than create duplicates')
table(['Property / path','Entered or saved','Runtime / calculation','Status'],[
 ['Girder E','205 GPa','205e9 Pa','Match'],['Girder Fy / Fu','345 / 500 MPa','345e6 / 500e6 Pa','Match'],['Girder density','77 kN/m3','78,500 N/m3','Mismatch'],['Concrete fck / fctm','45 / 3.5 MPa','45 / 3.5 MPa','Match'],['Concrete Ecm','35 GPa','35 GPa / 35,000 MPa','Match'],['Deck self-weight, 300 mm','25.5 x 0.300 = 7.65 kN/m2','7.36 kN/m2 in deck design','Mismatch']],[145,123,151,88])
heading('Steel density - '+plain(comment(20)))
para('The input and output retain 77, but _build_material_props() falls back to 78,500 when custom-grade lookup returns no database density. Read the validated custom key and convert kN/m3 to N/m3 once. A regression should expect 77,000 and check self-weight with section and geometry held fixed.')
heading('Deck density - '+plain(comment(41)))
para('T05C adds a separate deck-design path to the existing analysis-load issue. deckdesign.py:516 reads the code-table density and multiplies by 9.81 rather than using custom weight density. Pass the same validated density into both analysis and deck design; do not apply a second gravity conversion to a kN/m3 input.')
heading('Component materials - '+plain(comment(43)))
para('T06 preserves distinct grades in the input/output dictionaries, but the global material object follows the girder. Source review also finds member-design jobs copied from fixed templates in core/utils/connect.py; load and length are updated without replacing the member material fields. Separate DTOs alone would not fix those payloads. Propagate validated component properties in the downstream solver\'s supported representation and keep connector materials separate.')
para('The comments contain evidence and proposed regression checks. No isolated component-strength sensitivity test or patched material calculation was performed.','small')

page('15 / Report verification and remaining questions','Consistency between the generated PDFs, dictionaries and displayed checks')
table(['Finding','Evidence','Reporting route'],[
 ['False girder PASS text','T06 PDF p.6: fatigue UR 1.89, then “Girder design pass”; output status FAIL','Supporting comment on #65'],
 ['False deck detailing assurance','T05C PDF p.41: 50 mm cover vs 75 mm required, FAIL; sentence says all detailing requirements satisfied','Additional source location in #65'],
 ['Hardcoded M40 label','T06 PDF p.50: M40 in quantities despite custom fck 45','Supporting comment on #48'],
 ['Metres labelled mm','T01/T05: 1.39 mm vs actual 1390 mm; web 0.008 mm vs 8 mm','Existing #66; no new duplicate'],
 ['Railing value changes','Saved 1.4715 kN/m vs design input/report 6.806 kN/m','Existing #64; retained in case notes'],
 ['Empty reaction/load rows','Report tables omit values despite completed designs','Existing #48/#68; not all graphics are missing']],[135,254,118])
heading('Proposed report corrections')
para('Generate success/failure wording from evaluated checks, with an unavailable state for missing data. Use the selected material name and strength for quantity labels. Define units at the report-data boundary and distinguish pre-design UI inputs from optimized results; multiplying every value by 1000 would corrupt values already in millimetres.')
heading('Observations not resolved into calculation-bug claims')
para('<b>Force/UR rows:</b> T06 reports 9.239/13.93 kN with UR 0.85, although the displayed ratio is about 0.663. Another summary uses 11.84 kN, consistent with 0.85. The governing force, capacity and utilization need a common source or clearer labelling; this does not establish a wrong capacity equation.')
para('<b>Deflection summaries:</b> T03-R1/R3 per-girder maximum total deflection is 55.321 mm, while the unsuffixed summary uses 22.190 mm. T05C similarly uses 60.608 versus 22.565 mm. Both are retained; member/load-combination mapping is unresolved. I do not choose the smaller value to claim a pass.')

page('16 / Requirement coverage and limits','The submission supports each tested claim without treating sampling as exhaustive validation')
table(['Screening requirement','Evidence supplied','Practical limit'],[
 ['Basic and additional inputs','20/25/30 m spans; 7.5/9 m widths; 0/10-degree skew; 250/300 mm deck; 50/75 mm wearing course','Not every supported geometry or load option was tested'],
 ['Custom steel and concrete','Full custom properties; distinct CB/ED selections; runtime comparisons','Some downstream use fails or remains unverified'],
 ['At least three consecutive designs','T03: one session, 25 -> 20 -> 25; before/after dictionaries and plots','One three-run sequence, not long-duration stress testing'],
 ['CAD and structural plots','Generated models; rotation confirmations; BMD/SFD/deflection views','No dimensional audit of every CAD solid'],
 ['Input/output dictionary comparisons','Recorder snapshots T03/T04/T05C/T06; complete saved OSIs elsewhere','T01/T02 lack live snapshots; T05 intended run inconclusive'],
 ['Steel components and deck','Girder, bracing, diaphragm, intermediate/bearing stiffener and deck evidence','Longitudinal stiffener enabled case not tested'],
 ['Successful and failed cases','Fourteen checks/attempts; cancellations and inconclusive case retained','No invented all-pass bridge case'],
 ['Code-level bug reports','Four original issues and six supporting comments, with source and proposed fixes','Proposed fixes not applied or regression-tested in GUI'],
 ['PDF, repository and supporting files','This report; README, scripts, notes, originals and integrity manifest','Publication and final submission checks are separate']],[128,226,153])
para('This is functional testing and consistency review. It is not an independent certification of the bridge design equations or compliance with every cited engineering standard. A failing engineering check alone is not classified as a software defect; contradictory displays, lost inputs and incorrect propagation are reported separately.')

page('17 / Published issue register','All links below were verified live under HR5206 on 11 November 2026')
table(['Type','Finding','Live reference'],[
 ['Original issue','Save Input resets additional thicknesses',issue(71)],
 ['Original issue','End Diaphragm tab shows CB results',issue(72)],
 ['Original issue','Reaction field and sketch disagree',issue(73)],
 ['Original issue','Runtime barrier width ignores input',issue(74)],
 ['Supporting comment','Reload loss, info-dialog exception',comment(19)],
 ['Supporting comment','Custom steel density runtime evidence',comment(20)],
 ['Supporting comment','Additional deck-density calculation path',comment(41)],
 ['Supporting comment','Distinct materials and fixed job templates',comment(43)],
 ['Supporting comment','Wrong concrete grade in take-off',comment(48)],
 ['Supporting comment','False PASS wording, including deck detailing',comment(65)]],[111,251,145])
para('The original issues were prepared after checking open/closed reports and related discussions. Existing issues are credited as existing work; the six comments above are my additions. The full URLs, post text and author metadata are preserved in issues/github_posts.json and issues/LIVE_ISSUES.md.')
para('All ten posts now include file-attachment links. The same original evidence is included in this submission, so review does not depend solely on GitHub attachment availability. No code fix is claimed as merged or validated.')

page('18 / Reproducing and reviewing the submission','A readable report backed by unchanged input files, dictionaries and screenshots')
table(['Folder / file','Contents'],[
 ['report/','This PDF and its Markdown text version.'],['case_notes/','Eight detailed case notes, including historical observations and exact saved-input appendices.'],['evidence/T01 ... T06/','Original screenshots, OSIs, generated app reports, recorder metadata and run JSON files.'],['scripts/capture_osdagbridge.py','Recorder used for the captured sessions; wraps the original core design call.'],['scripts/reproduce_save_reset.py','Isolated default-expansion reproduction; assertion fails on tested source.'],['scripts/reproduce_ed_merge.py','Actual source merge executed against captured results; no Qt/solver run.'],['scripts/build_report.py','Rebuilds this report from the packaged evidence; requires reportlab, Pillow, PyMuPDF and DejaVu fonts.'],['issues/','Live links and verification snapshot; issues are external, not locally invented IDs.'],['SHA256SUMS.txt','Checksums for the packaged evidence and documents.']],[194,313])
heading('How to replay a case')
para('Use the recorded source revision and the repository environment. For an OSI-backed case, open its original saved file in the desktop and follow the relevant case notes. For T05C/T06, no OSI export is claimed: use the full input_before.json as the exact parameter record and enter the documented configuration. Main Save Input is intentionally avoided in these follow-ups because of issue #71.')
para('For the isolated scripts, provide the T05B OSI or the T06 output JSON and the tested source file as described in each script header. These checks reproduce narrow failure mechanisms; they do not constitute additional desktop tests or validate the full solver.')
heading('Evidence handling')
para('Original filenames and file bytes are retained. Case-note statements such as “next test” or “not yet posted” reflect when those notes were written; the published issue register in this final report supersedes their reporting status. The original generated application reports remain unchanged even where this review identifies errors in them.')
heading('Review priorities')
para('I would address input preservation and component-result routing first, then material/runtime propagation and consistent status reporting. A useful regression suite should exercise serialization/reload, separate component result maps, custom material payloads and the full three-run change-and-return sequence.')

para('My conclusion is that the tested workflow can complete repeated designs and generate inspectable outputs, but input persistence, material propagation and output consistency need correction. The retained successful checks and failures make those boundaries reproducible rather than hiding them behind a single pass/fail label.')


class ReportDocument(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable, '_toc_level'):
            self.canv.bookmarkPage(flowable._bookmark)
            self.canv.addOutlineEntry(flowable._toc_label,flowable._bookmark,level=flowable._toc_level,closed=False)
            self.notify('TOCEntry',(flowable._toc_level,flowable._toc_label,self.page-2,flowable._bookmark))

def footer(c,doc):
    if doc.page==1:return
    c.saveState();c.setFont('Helvetica',11.35);c.setFillColor(black)
    label='i' if doc.page==2 else str(doc.page-2)
    c.drawCentredString(595.276/2,54,label);c.restoreState()

doc=ReportDocument(str(OUT/'OsdagBridge_Testing_Report_Harish_Raghav.pdf'),pagesize=(595.276,841.89),leftMargin=85.039,rightMargin=85.039,topMargin=50,bottomMargin=78,title='OsdagBridge Functional Testing Report - Harish Raghav S',author='Harish Raghav S')
doc.multiBuild(story,onFirstPage=footer,onLaterPages=footer)
(OUT/'OsdagBridge_Testing_Report.md').write_text('\n'.join(md),encoding='utf-8')
print('Created',OUT/'OsdagBridge_Testing_Report_Harish_Raghav.pdf','sections',len(sections))
