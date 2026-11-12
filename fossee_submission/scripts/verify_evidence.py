"""Check every packaged file against SHA256SUMS.txt without changing files.

Run from any directory: python fossee_submission/scripts/verify_evidence.py
A mismatch reports the affected path and exits with a nonzero status.
"""
from pathlib import Path
import hashlib
import sys

root = Path(__file__).resolve().parents[1]
manifest = root / 'SHA256SUMS.txt'
checked = 0
problems = []

for line in manifest.read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    expected, relative = line.split('  ', 1)
    target = (root / relative).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        problems.append(f'MISSING OR INVALID: {relative}')
        continue
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    checked += 1
    if actual != expected:
        problems.append(f'MISMATCH: {relative}')

for problem in problems:
    print(problem)
print(f'Checked {checked} files; {len(problems)} problems.')
sys.exit(1 if problems else 0)
