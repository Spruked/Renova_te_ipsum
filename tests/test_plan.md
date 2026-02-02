# SF-ORB Cognitive Test Plan

Scope: Five stimulus scenarios, each 3 cycles × 500 iterations (7,500 total events).
Outputs: Per-stimulus pulse logs + per-cycle summaries; written to results/ as JSONL files. Tests are defined but not executed until explicitly run.

Test Scenarios
- Test 1 — Linear Drift: steady dx, dy to build habit lead.
- Test 2 — Oscillatory: sine/cosine path to probe periodic habit learning.
- Test 3 — Random Walk: bounded jitter to keep Guard dominant, low habit.
- Test 4 — Quadrant Loop: deterministic quadrant cycle to maximize habit prediction.
- Test 5 — Symmetric Jumps: mostly linear with mirrored jumps to trigger intuition.

Cycle Structure (per test)
- 3 cycles; each cycle clears posteriori cache to observe fresh vs learned behavior.
- 500 iterations per cycle; stimuli generated deterministically per scenario with seed control.

Metrics Captured
- Mode counts: Guard/Habit/Intuition-Jump frequencies.
- Bypass hits: apriori/posteriori lightning occurrences.
- Habit signals: predictive_intent targets, confidence, hume_vivacity.
- Intuition signals: jump_vector presence, spinozan_certainty.
- Timing: synthesis latency per stimulus (ms).

Execution Notes
- Tests are inert by default. Run manually via tests/test_runner.py (see instructions in that file).
- Results write to results/<timestamp>_test_<id>_cycle_<cycle>.jsonl plus a summary JSON.
- Do not run until explicit go-ahead.