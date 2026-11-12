"""Function-level check; no GUI, structural solver, or file write is performed.

Run in the osdagbridge environment:
python reproduce_save_reset.py path/to/T05B_before.osi
The assertion fails on the tested commit and should pass after a correct fix.
"""
import sys
from copy import deepcopy
from pathlib import Path
import yaml
from osdagbridge.core.bridge_types.plate_girder.defaults import solve_extend_basic_input_dict

saved = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
working = deepcopy(saved)
keys = ("typical_section.deck_thickness", "typical_section.wearing_course.thickness")
working[keys[0]], working[keys[1]] = 300.0, 75.0
before = {key: working[key] for key in keys}
solve_extend_basic_input_dict(working)
after = {key: working[key] for key in keys}
print("Before:", before)
print("After: ", after)
assert after == before, "Save-path default expansion overwrote custom thicknesses"
