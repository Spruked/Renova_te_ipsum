import math
import random
import time
from datetime import datetime
from orb_controller import SF_ORB_Controller
from vault_system.manager import VaultManager

import importlib
import hlsf_geometry.engine
importlib.reload(hlsf_geometry.engine)
print("FORCE RELOAD: hlsf_geometry.engine module reloaded")


class ShortDiagnosticTest:
    def __init__(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting SHORT diagnostic - Test 4 Cycle 1 only")
        self.controller = SF_ORB_Controller()
        self.SCREEN_W = 1920
        self.SCREEN_H = 1080
        self.CENTER_X = self.SCREEN_W // 2
        self.CENTER_Y = self.SCREEN_H // 2

    def generate_quadrant_stimulus(self, iteration):
        quadrant = iteration % 4
        offsets = [(100, 100), (300, 100), (300, 300), (100, 300)]
        drift = (iteration // 4) * 2
        x = offsets[quadrant][0] + drift
        y = offsets[quadrant][1] + drift
        x = min(max(x, 0), self.SCREEN_W)
        y = min(max(y, 0), self.SCREEN_H)
        return {
            "type": "cursor_movement",
            "coordinates": [x, y],
            "velocity": 8.0,
            "intent": "navigation",
            "meta": {"test_mode": True, "test_id": 4, "iteration": iteration}
        }

    def run_test_4_cycle_1(self, max_iters=1200):
        print(f"→ Posteriori cache cleared. Initial density: {len(self.controller.engine.field_map)}")

        last_stimulus = None
        for i in range(max_iters):
            stimulus = self.generate_quadrant_stimulus(i)

            start = time.perf_counter()
            thought = self.controller.cognitively_emerge(stimulus)
            proc_ms = (time.perf_counter() - start) * 1000

            if thought:
                if isinstance(thought, dict):
                    payload = thought.get('predicate') or thought.get('data', {}).get('predicate', {})
                    mode = payload.get('cognitive_mode', thought.get('triad_c_mode', 'BYPASS'))
                    density = payload.get('field_density', len(self.controller.engine.field_map))
                else:
                    pulse = thought.pulse()
                    mode = pulse.get('cognitive_mode', 'UNKNOWN')
                    density = pulse.get('field_density', 0)
                print(f"Iter {i+1:4d} | {mode:12} | {proc_ms:6.1f}ms | Density: {density}")

                if (i + 1) % 500 == 0 and i > 0:
                    self.controller.emergency_purge()

            last_stimulus = stimulus

            if i % 100 == 0 and i > 0:
                print(f"Progress: {i}/{max_iters} | Current density: {len(self.controller.engine.field_map)}")

        print("Short Test 4 Cycle 1 complete.")


if __name__ == "__main__":
    random.seed(42)
    tester = ShortDiagnosticTest()
    tester.run_test_4_cycle_1(max_iters=1200)
