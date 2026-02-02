import sys
import importlib

# SOVEREIGN CACHE PURGE: ensure fresh engine without stale bytecode
if 'hlsf_geometry.engine' in sys.modules:
    del sys.modules['hlsf_geometry.engine']
if 'hlsf_geometry' in sys.modules:
    del sys.modules['hlsf_geometry']

sys.dont_write_bytecode = True

from hlsf_geometry.engine import HLSFEngine, hlsf_singleton
from orb_controller import SF_ORB_Controller

print(f"DEBUG: Engine ID: {id(hlsf_singleton)}")
print(f"DEBUG: Has max_field_density? {hasattr(hlsf_singleton, 'max_field_density')}")
if hasattr(hlsf_singleton, 'max_field_density'):
    print(f"DEBUG: Threshold = {hlsf_singleton.max_field_density}")
    print(f"DEBUG: Soft cap = {hlsf_singleton.edge_cutter_threshold}")
else:
    print("⛔ CRITICAL: Running STALE engine without edge-cutter! Restart VS Code.")
    sys.exit(1)

import math
import random
import time
import json
from datetime import datetime
from collections import defaultdict

import pandas as pd


class CognitiveTestHarness:
    """
    Forensic validation of the Triple Triple architecture.
    5 Tests × 3 Cycles × 500 Iterations = 7,500 data points.
    """

    def __init__(self):
        print("Initializing Cognitive Test Harness...")
        print("Loading SF_ORB_Controller...")
        self.controller = SF_ORB_Controller()
        self.results = []
        self.metrics = defaultdict(list)

        # Screen bounds for realistic coordinate generation
        self.SCREEN_W = 1920
        self.SCREEN_H = 1080
        self.CENTER_X = self.SCREEN_W // 2
        self.CENTER_Y = self.SCREEN_H // 2

    def generate_stimulus(self, test_id, iteration, last_stimulus=None):
        """Generate synthetic cursor stimuli per test specification."""
        if test_id == 1:
            # Linear Movement: Constant velocity dx=5, dy=2
            if last_stimulus is None:
                x, y = 0, 0
            else:
                x = min(last_stimulus['coordinates'][0] + 5, self.SCREEN_W)
                y = min(last_stimulus['coordinates'][1] + 2, self.SCREEN_H)
            velocity = math.sqrt(5**2 + 2**2)

        elif test_id == 2:
            # Oscillatory: Sinusoidal path
            x = self.CENTER_X + 100 * math.sin(iteration * 0.1)
            y = self.CENTER_Y + 100 * math.cos(iteration * 0.1)
            velocity = 10.0

        elif test_id == 3:
            # Random Walk: Bounded random walk
            if last_stimulus is None:
                x, y = self.CENTER_X, self.CENTER_Y
                dx = dy = 0
            else:
                dx = random.uniform(-10, 10)
                dy = random.uniform(-10, 10)
                x = max(0, min(self.SCREEN_W, last_stimulus['coordinates'][0] + dx))
                y = max(0, min(self.SCREEN_H, last_stimulus['coordinates'][1] + dy))
            velocity = math.sqrt(dx**2 + dy**2) if last_stimulus else 5.0

        elif test_id == 4:
            # Repetitive Quadrant Loop: NW → NE → SE → SW
            quadrant = iteration % 4
            offsets = [(100, 100), (300, 100), (300, 300), (100, 300)]
            x = offsets[quadrant][0] + (iteration // 4) * 2
            y = offsets[quadrant][1] + (iteration // 4) * 2
            velocity = 8.0

        elif test_id == 5:
            # Abrupt Jumps with Symmetry
            if last_stimulus is None or (iteration > 0 and iteration % random.randint(50, 100) == 0):
                if last_stimulus:
                    x = self.SCREEN_W - last_stimulus['coordinates'][0]
                    y = last_stimulus['coordinates'][1]
                else:
                    x, y = self.CENTER_X, self.CENTER_Y
                velocity = 50.0
            else:
                if last_stimulus:
                    x = min(last_stimulus['coordinates'][0] + 3, self.SCREEN_W)
                    y = min(last_stimulus['coordinates'][1] + 1, self.SCREEN_H)
                else:
                    x = y = 0
                velocity = math.sqrt(3**2 + 1**2)

        else:
            x = self.CENTER_X
            y = self.CENTER_Y
            velocity = 0.0

        return {
            "type": "cursor_movement",
            "coordinates": [x, y],
            "velocity": velocity,
            "intent": "navigation",
            "meta": {"test_mode": True, "test_id": test_id, "iteration": iteration}
        }

    def run_single_cycle(self, test_id, cycle_num):
        print(f"\n[Test {test_id} | Cycle {cycle_num + 1}/3] Initializing...")

        # Reset posteriori cache for isolation (disk retained; RAM cleared)
        self.controller.vaults.posteriori_cache = {}
        print(f"  → Posteriori cache cleared. Field density: {len(self.controller.engine.field_map)}")

        cycle_results = []
        last_stimulus = None

        for i in range(500):
            stimulus = self.generate_stimulus(test_id, i, last_stimulus)

            start_proc = time.perf_counter()
            thought = self.controller.cognitively_emerge(stimulus)
            proc_time = (time.perf_counter() - start_proc) * 1000

            if thought:
                # Handle both CrossDomainPredicate objects and deterministic bypass dicts
                if isinstance(thought, dict):
                    payload = thought.get('predicate') or thought.get('data', {}).get('predicate', {})
                    proc_mode = payload.get('cognitive_mode', thought.get('triad_c_mode', 'BYPASS'))
                    record = {
                        'test_id': test_id,
                        'cycle': cycle_num + 1,
                        'iteration': i,
                        'stimulus_x': stimulus['coordinates'][0],
                        'stimulus_y': stimulus['coordinates'][1],
                        'velocity': stimulus['velocity'],
                        'cognitive_mode': proc_mode,
                        'glow_intensity': payload.get('glow_intensity'),
                        'epistemic_alignment': payload.get('epistemic_alignment'),
                        'deterministic': True,
                        'proc_time_ms': proc_time,
                        'field_density': payload.get('field_density', len(self.controller.engine.field_map))
                    }

                    pred = payload.get('predictive_intent') or {}
                    record['predicted_quadrant'] = pred.get('target') if 'target' in pred else None
                    record['hume_vivacity'] = pred.get('hume_vivacity', 0)

                    jump_vec = payload.get('jump_vector') or []
                    record['jump_x'] = jump_vec[0] if len(jump_vec) > 0 else 0
                    record['jump_y'] = jump_vec[1] if len(jump_vec) > 1 else 0
                else:
                    pulse = thought.pulse()
                    record = {
                        'test_id': test_id,
                        'cycle': cycle_num + 1,
                        'iteration': i,
                        'stimulus_x': stimulus['coordinates'][0],
                        'stimulus_y': stimulus['coordinates'][1],
                        'velocity': stimulus['velocity'],
                        'cognitive_mode': pulse['cognitive_mode'],
                        'glow_intensity': pulse['glow_intensity'],
                        'epistemic_alignment': pulse['epistemic_alignment'],
                        'deterministic': pulse['deterministic'],
                        'proc_time_ms': proc_time,
                        'field_density': len(self.controller.engine.field_map)
                    }

                    pred = pulse.get('predictive_intent') or {}
                    record['predicted_quadrant'] = pred.get('target') if 'target' in pred else None
                    record['hume_vivacity'] = pred.get('hume_vivacity', 0)

                    jump_vec = pulse.get('jump_vector') or []
                    record['jump_x'] = jump_vec[0] if len(jump_vec) > 0 else 0
                    record['jump_y'] = jump_vec[1] if len(jump_vec) > 1 else 0

            else:
                record = {
                    'test_id': test_id,
                    'cycle': cycle_num + 1,
                    'iteration': i,
                    'cognitive_mode': 'REJECTED',
                    'proc_time_ms': proc_time
                }

            cycle_results.append(record)
            last_stimulus = stimulus

            if (i + 1) % 500 == 0:
                self.controller.emergency_purge()

            if (i + 1) % 100 == 0:
                print(f"    Progress: {i + 1}/500 | Mode: {record.get('cognitive_mode', 'N/A')} | Density: {record.get('field_density', 0)}")

        return cycle_results

    def run_full_suite(self):
        print("=" * 60)
        print("SF-ORB COGNITIVE TEST SUITE")
        print("Triple Triple Architecture Validation")
        print("7,500 Iterations | 5 Test Scenarios | 3 Cycles Each")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Synthetic Data Only: {True} (Sovereignty Verified)")
        print("-" * 60)

        all_results = []
        descriptions = {
            1: "Linear Movement (Constant Velocity)",
            2: "Oscillatory Movement (Sinusoidal)",
            3: "Random Walk (Chaotic/Stochastic)",
            4: "Repetitive Quadrant Loop (Pattern)",
            5: "Abrupt Jumps with Symmetry (Chaos+Order)",
        }

        for test_id in range(1, 6):
            print(f"\n{'='*20} TEST {test_id} {'='*20}")
            print(f"Scenario: {descriptions[test_id]}")
            for cycle in range(3):
                cycle_data = self.run_single_cycle(test_id, cycle)
                all_results.extend(cycle_data)
                print(f"  ✓ Cycle {cycle + 1} complete. Records: {len(cycle_data)}")

        self.results = all_results
        self.save_results()
        self.analyze_results()

    def save_results(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cognitive_test_results_{timestamp}.csv"
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False)
        print(f"\n✓ Raw data saved to: {filename}")

    def analyze_results(self):
        print("\n" + "=" * 60)
        print("AGGREGATE ANALYSIS")
        print("=" * 60)

        df = pd.DataFrame(self.results)

        print("\n[Overall Cognitive Mode Distribution]")
        mode_dist = df['cognitive_mode'].value_counts(normalize=True) * 100
        for mode, pct in mode_dist.items():
            print(f"  {mode:20s}: {pct:6.2f}%")

        print("\n[Per-Test Mode Distribution]")
        test_summary = df.groupby('test_id')['cognitive_mode'].value_counts(normalize=True).unstack(fill_value=0) * 100
        print(test_summary.round(2))

        habit_df = df[df['cognitive_mode'] == 'HABIT']
        if not habit_df.empty:
            print("\n[Habit Performance]")
            print(f"  Total Habit activations: {len(habit_df)}")
            print(f"  Mean Humean Vivacity: {habit_df['hume_vivacity'].mean():.3f}")
            print(f"  Avg Processing Time: {habit_df['proc_time_ms'].mean():.2f}ms")

        jump_df = df[df['cognitive_mode'] == 'INTUITION-JUMP']
        if not jump_df.empty:
            print("\n[Intuition-Jump Performance]")
            print(f"  Total Jumps: {len(jump_df)}")
            print(f"  Trigger Tests: {jump_df['test_id'].unique()}")
            print(f"  Avg Processing Time: {jump_df['proc_time_ms'].mean():.2f}ms")
        else:
            print("\n[Intuition-Jump Performance]")
            print("  No jumps triggered (expected for Tests 1-4, anomaly for Test 5)")

        print("\n[Processing Performance]")
        print(f"  Mean latency: {df['proc_time_ms'].mean():.2f}ms")
        print(f"  Max latency: {df['proc_time_ms'].max():.2f}ms")
        print(f"  Min latency: {df['proc_time_ms'].min():.2f}ms")

        print("\n[Field Density Growth]")
        density_by_test = df.groupby('test_id')['field_density'].max()
        print(f"  Max density per test: {density_by_test.to_dict()}")

        print("\n" + "=" * 60)
        print("TEST SUITE COMPLETE")
        print("=" * 60)


def main():
    random.seed(42)
    harness = CognitiveTestHarness()
    harness.run_full_suite()


if __name__ == "__main__":
    main()
