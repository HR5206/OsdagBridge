"""Launch OsdagBridge and capture evidence around each actual design call.

Run with the same conda environment and working directory as the normal app.
Files go beside this script, under t03/session_TIMESTAMP/run_01, run_02, ...
No repository files or design inputs are edited. This wraps the design method
in memory; capture adds file-I/O overhead. It does not validate calculations.
JSON is a readable projection: dataclasses/arrays are expanded, other objects
are explicitly tagged. A successful engine return is not a passing design or
proof that the later GUI/CAD update completed.
"""
from __future__ import annotations

import dataclasses
import functools
import hashlib
import inspect
import json
import math
import os
import platform
import subprocess
import sys
import threading
import time
import traceback
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path


def timestamp():
    return datetime.now().astimezone().isoformat()


def json_value(value, active=None):
    """Project Python state without modifying the source objects."""
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else {"non_finite_float": str(value)}
    if active is None:
        active = set()
    token = id(value)
    if token in active:
        return {"circular_reference_type": type(value).__name__}
    active.add(token)
    try:
        if isinstance(value, Mapping):
            return {str(k): json_value(v, active) for k, v in value.items()}
        if dataclasses.is_dataclass(value) and not isinstance(value, type):
            return {f.name: json_value(getattr(value, f.name), active)
                    for f in dataclasses.fields(value)}
        if isinstance(value, (list, tuple)):
            return [json_value(v, active) for v in value]
        if hasattr(value, "tolist"):
            return json_value(value.tolist(), active)
        if isinstance(value, Path):
            return str(value)
        return {"python_type": type(value).__name__, "repr": repr(value)}
    finally:
        active.remove(token)


def save_json(path, data):
    path.write_text(json.dumps(json_value(data), indent=2, ensure_ascii=False,
                               allow_nan=False), encoding="utf-8")


def install_recorder(bridge_class, session):
    original = bridge_class.design
    lock = threading.Lock()
    count = 0

    @functools.wraps(original)
    def recorded_design(self, *args, **kwargs):
        nonlocal count
        with lock:
            count += 1
            number = count
        folder = session / f"run_{number:02d}"
        errors = []
        try:
            folder.mkdir()
        except Exception as exc:
            # Evidence must not change whether the real engine can execute.
            print(f"EVIDENCE CAPTURE FAILED: {exc}", file=sys.stderr)
            return original(self, *args, **kwargs)

        def capture(name, value):
            try:
                save_json(folder / name, value)
            except Exception as exc:
                errors.append({"file": name, "error": str(exc)})

        started = timestamp()
        capture("input_before.json", getattr(self, "input_dict", {}))
        # Previous output is intentionally labelled; useful for stale-state checks.
        capture("output_before.json", getattr(self, "output_dict", {}))
        capture("status.json", {"state": "engine_running", "started": started,
                                "run_number": number})
        success = False
        failure = None
        timer = time.perf_counter()
        try:
            result = original(self, *args, **kwargs)
            success = True
            return result
        except BaseException as exc:
            failure = {"type": type(exc).__name__, "message": str(exc)}
            try:
                (folder / "traceback.txt").write_text(traceback.format_exc(), encoding="utf-8")
            except Exception as capture_exc:
                errors.append({"file": "traceback.txt", "error": str(capture_exc)})
            raise
        finally:
            elapsed = time.perf_counter() - timer
            capture("input_after.json", getattr(self, "input_dict", {}))
            output_name = "output_after.json" if success else "output_at_failure.json"
            capture(output_name, getattr(self, "output_dict", {}))
            state = {}
            for name in ("material_props", "deck_layout", "grillage_geometry"):
                if hasattr(self, name):
                    state[name] = getattr(self, name)
            capture("runtime_properties.json", state)
            capture("status.json", {
                "state": "engine_returned" if success else "engine_failed",
                "run_number": number, "started": started, "finished": timestamp(),
                "engine_elapsed_seconds": elapsed, "error": failure,
                "capture_errors": list(errors),
                "scope": "Core design call only. UI/CAD updates occur afterwards. "
                         "Failure-state output may contain partial or previous results. "
                         "Engine completion is not structural adequacy.",
            })
            if errors:
                print(f"EVIDENCE CAPTURE WARNINGS: {errors}", file=sys.stderr)
            print(f"Evidence for run {number:02d}: {folder}")

    bridge_class.design = recorded_design
    return original


def git_info(source_file):
    result = {"source_file": str(source_file)}
    for path in source_file.parents:
        if (path / ".git").exists():
            result["repository"] = str(path)
            for key, args in (("commit", ["rev-parse", "HEAD"]),
                              ("working_tree", ["status", "--short"])):
                try:
                    process = subprocess.run(["git", "-C", str(path), *args],
                                             text=True, capture_output=True, timeout=10)
                    result[key] = process.stdout.strip() if process.returncode == 0 else process.stderr.strip()
                except Exception as exc:
                    result[key] = f"Unavailable: {exc}"
            break
    return result


def main():
    # Match python -m's access to the user's normal source working directory.
    sys.path.insert(0, str(Path.cwd()))
    base = Path(__file__).resolve().parent / "t03"
    base.mkdir(exist_ok=True)
    session = base / datetime.now().strftime("session_%Y%m%d_%H%M%S_%f")
    session.mkdir()
    # Verify the evidence location before starting a long interactive session.
    save_json(session / "session.json", {
        "started": timestamp(), "python": sys.version, "platform": platform.platform(),
        "process_id": os.getpid(), "working_directory": str(Path.cwd()),
        "recorder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "method": "In-memory wrapper around PlateGirderBridge.design; original is called once. "
                  "No design inputs, environment settings, solver logic or source files are changed.",
        "verification_limit": "Recorder logic checked with fake success/failure backends. "
                              "A full Windows OsdagBridge GUI run was not performed by the author.",
    })
    try:
        # Import the normal entry point first so its native-library setup runs.
        from osdagbridge.desktop import __main__ as desktop
        bridge_class = desktop.PlateGirderBridge
        install_recorder(bridge_class, session)
        source = Path(inspect.getfile(bridge_class)).resolve()
        save_json(session / "source.json", git_info(source))
        print(f"Evidence capture active. Session folder: {session}")
        desktop.main()
    except Exception:
        (session / "startup_error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()
