"""SF-ORB Cognitive Test Runner (inert until explicitly invoked).

Usage (manual only, do not auto-run):
    set RUN_SF_ORB_TESTS=1
    python tests/test_runner.py

By default, exits without running to respect sovereignty/go-ahead.
"""

import json
import os
import time
import math
import random
from datetime import datetime
from pathlib import Path

from orb_controller import SF_ORB_Controller


RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def _timestamp() -> str:
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def generate_stimulus(test_id: int, iteration: int, width: int = 1920, height: int = 1080):
    """Deterministic stimuli per scenario; seeds controlled externally."""
    if test_id == 1:  # Linear
        x = (iteration * 5) % width
        y = (iteration * 2) % height
    elif test_id == 2:  # Oscillatory
        x = (width / 2) + 100 * math.sin(iteration * 0.1)
        y = (height / 2) + 100 * math.cos(iteration * 0.1)
    elif test_id == 3:  # Random walk
        random.seed(iteration)
        dx, dy = random.randint(-10, 10), random.randint(-10, 10)
        x = (width / 2) + dx * iteration % width
        y = (height / 2) + dy * iteration % height
    elif test_id == 4:  # Quadrant loop
        quad = [(-200, -200), (200, -200), (200, 200), (-200, 200)][iteration % 4]
        x = (width / 2) + quad[0]
        y = (height / 2) + quad[1]
    elif test_id == 5:  # Symmetric jumps
        base_x = (iteration * 6) % width
        base_y = (iteration * 3) % height
        if iteration % 75 == 0:
            base_x = width - base_x  # mirror
        x, y = base_x, base_y
    else:
        x = width / 2
        y = height / 2

    return {
        "type": "cursor_movement",
        "coordinates": [float(x), float(y)],
        "velocity": 5.0,
        "intent": "navigation"
    }


def run_cycle(controller: SF_ORB_Controller, test_id: int, cycle: int, iterations: int = 500):
    records = []
    start = time.time()
    for i in range(iterations):
        stimulus = generate_stimulus(test_id, i)
        thought = controller.cognitively_emerge(stimulus)
        pulse = thought.pulse() if thought else None
        records.append({
            "iteration": i,
            "stimulus": stimulus,
            "pulse": pulse,
        })
    elapsed_ms = (time.time() - start) * 1000
    return records, elapsed_ms


def summarize(records):
    modes = {"GUARD": 0, "HABIT": 0, "INTUITION-JUMP": 0}
    bypass = 0
    for rec in records:
        pulse = rec.get("pulse") or {}
        mode = pulse.get("cognitive_mode", "GUARD")
        modes[mode] = modes.get(mode, 0) + 1
        if pulse.get("deterministic"):
            bypass += 1
    total = len(records) if records else 1
    return {
        "modes": {k: v / total for k, v in modes.items()},
        "bypass_rate": bypass / total,
        "samples": total,
    }


def write_results(test_id: int, cycle: int, records, summary):
    ts = _timestamp()
    detail_path = RESULTS_DIR / f"{ts}_test_{test_id}_cycle_{cycle}.jsonl"
    summary_path = RESULTS_DIR / f"{ts}_summary_test_{test_id}_cycle_{cycle}.json"
    with detail_path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return detail_path, summary_path


def run_all_tests(iterations: int = 500, cycles: int = 3):
    controller = SF_ORB_Controller()
    all_summaries = []
    for test_id in range(1, 6):
        for cycle in range(cycles):
            # Fresh posteriori per cycle
            controller.vaults.posteriori_cache.clear()
            if os.path.exists(controller.vaults.posteriori_dir):
                # optional: skip disk clear to preserve history; here we keep disk but clear RAM
                pass
            records, elapsed_ms = run_cycle(controller, test_id, cycle, iterations)
            summary = summarize(records)
            summary["elapsed_ms"] = elapsed_ms
            summary["test_id"] = test_id
            summary["cycle"] = cycle
            detail_path, summary_path = write_results(test_id, cycle, records, summary)
            all_summaries.append({"summary_file": str(summary_path), **summary})
            print(f"Completed test {test_id} cycle {cycle} in {elapsed_ms:.1f}ms; results -> {detail_path}")
    master_path = RESULTS_DIR / f"{_timestamp()}_master_summary.json"
    with master_path.open("w", encoding="utf-8") as f:
        json.dump(all_summaries, f, indent=2)
    print(f"Master summary written to {master_path}")


if __name__ == "__main__":
    if os.environ.get("RUN_SF_ORB_TESTS") != "1":
        print("Tests are defined but not executed. Set RUN_SF_ORB_TESTS=1 and rerun to execute.")
        raise SystemExit(0)
    # Optional seed for reproducibility
    seed = os.environ.get("SF_ORB_TEST_SEED")
    if seed is not None:
        try:
            seed_val = int(seed)
            random.seed(seed_val)
        except ValueError:
            pass
    run_all_tests()