"""Execute the actual merge AST from the tested source against captured results.

Usage: python reproduce_ed_merge.py path/to/transverse_member_design.py path/to/output_after.json
This isolates dictionary routing; it does not run Qt or a structural calculation.
"""
import ast
import json
import sys
from copy import deepcopy
from pathlib import Path

source_path, output_path = map(Path, sys.argv[1:3])
tree = ast.parse(source_path.read_text(encoding="utf-8"))
method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "_try_load_data")
block = next(n for n in method.body if isinstance(n, ast.Try)).body
start = next(i for i, n in enumerate(block) if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.target.id == "designs_dict")
merge = ast.Module(body=block[start:start + 2], type_ignores=[])
assert isinstance(merge.body[1], ast.For), "Source layout changed; review before running"
out = json.loads(output_path.read_text(encoding="utf-8"))
scope = {"cb_designs": deepcopy(out["crossbracing_design_results"]),
         "ed_designs": deepcopy(out["end_diaphragm_design_results"]), "od": out}
exec(compile(merge, str(source_path), "exec"), scope)
for member in ("diagonal", "chord"):
    for kind in ("tension", "compression"):
        expected = out["end_diaphragm_design_results"]["G1-G2"][member][kind]["Member.efficiency"]
        actual = scope["designs_dict"]["G1-G2"][member][kind]["Member.efficiency"]
        print(f"{member} {kind}: end-diaphragm={expected}, merged-for-display={actual}")
        assert actual == out["crossbracing_design_results"]["G1-G2"][member][kind]["Member.efficiency"]
        assert actual != expected
print("Confirmed: this source merge retains CB values instead of the distinct ED values.")
