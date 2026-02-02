import time
import sys
from pathlib import Path
from collections import deque
from hlsf_geometry.engine import hlsf_singleton
from core_4_minds.tribunal import FourMindTribunal
from vault_system.manager import VaultManager

# Ensure parent dir (where bayesian_engine.py lives) is importable without packaging.
PARENT = Path(__file__).resolve().parent.parent
if str(PARENT) not in sys.path:
    sys.path.append(str(PARENT))

from bayesian_engine import BayesianEngine


class CrossDomainPredicate:
    """Emergent thought-object synthesized across epistemic, spatial, and logic domains."""

    def __init__(self, epistemic, spatial, logic, synthesis_confidence):
        self.epistemic_traces = epistemic
        self.hlsf_node = spatial
        self.logic_validity = logic
        self.confidence = synthesis_confidence
        self.timestamp = time.time()

    def pulse(self):
        mode = self.logic_validity.get("active_mode") or (
            "INTUITION-JUMP" if self.logic_validity.get("intuitive_jump_triggered") else
            "HABIT" if self.logic_validity.get("custom_habit_active") else
            "GUARD"
        )
        return {
            "glow_intensity": self.confidence,
            "spatial_coordinate": self.hlsf_node,
            "epistemic_alignment": self._calculate_axiomatic_alignment(),
            "deterministic": self.confidence > 0.95,
            "predictive_intent": self.logic_validity.get("inductive_prediction", {}),
            "jump_vector": self.logic_validity.get("necessity_vector", []),
            "cognitive_mode": mode,
            "bayes_habit_prob": self.logic_validity.get("bayes_habit_prob"),
            "bayes_jump_prob": self.logic_validity.get("bayes_jump_prob"),
            "bayes_guard_prob": self.logic_validity.get("bayes_guard_prob"),
            "epistemic_bayes": self.logic_validity.get("epistemic_bayes"),
        }

    def _calculate_axiomatic_alignment(self):
        if not self.epistemic_traces:
            return 0.0
        confidences = [trace.get("confidence", 0.5) for trace in self.epistemic_traces.values()]
        return sum(confidences) / len(confidences)


class HabitTracker:
    """Humean constant conjunction tracker for cursor movements."""

    def __init__(self, vault_manager):
        self.vault = vault_manager
        if not hasattr(self.vault, "posteriori_cache"):
            self.vault.posteriori_cache = {}
        self.sequence_buffer = deque(maxlen=5)
        self.pattern_cache = {}

    def record_observation(self, stimulus):
        if stimulus.get("type") != "cursor_movement":
            return None
        coords = stimulus.get("coordinates", [0, 0])
        quadrant = self._coords_to_quadrant(coords)
        observation = {
            "quadrant": quadrant,
            "coords": coords,
            "velocity": stimulus.get("velocity", 0.0),
            "timestamp": time.time()
        }
        self.sequence_buffer.append(observation)
        if len(self.sequence_buffer) >= 3:
            pattern_key = self._serialize_pattern(list(self.sequence_buffer))
            self._update_conjunction_frequency(pattern_key)
        return observation

    def predict_next(self):
        if len(self.sequence_buffer) < 3:
            return None
        current_pattern = self._serialize_pattern(list(self.sequence_buffer)[-3:])
        cached = getattr(self.vault, "posteriori_cache", {}).get(f"habit_{current_pattern}")
        if cached:
            return {
                "prediction_type": "QUADRANT_TRANSITION",
                "target": cached.get("predicted_next"),
                "confidence": cached.get("frequency", 0.0),
                "hume_vivacity": min(cached.get("frequency", 0) * 1.2, 1.0)
            }
        return {"prediction_type": "UNSURE", "confidence": 0.3, "hume_vivacity": 0.4}

    def _coords_to_quadrant(self, coords):
        x, y = coords[0], coords[1]
        grid_x = 1920 / 2
        grid_y = 1080 / 2
        col = 0 if x < grid_x else 1
        row = 0 if y < grid_y else 1
        return ["NW", "NE", "SW", "SE"][row * 2 + col]

    def _serialize_pattern(self, sequence):
        return "_".join([s["quadrant"] for s in sequence])

    def _update_conjunction_frequency(self, pattern_key):
        if pattern_key not in self.pattern_cache:
            self.pattern_cache[pattern_key] = {"count": 0}
        self.pattern_cache[pattern_key]["count"] += 1
        self.vault.crystallize(f"habit_{pattern_key}", {
            "pattern": pattern_key,
            "frequency": min(self.pattern_cache[pattern_key]["count"] / 10.0, 1.0),
            "predicted_next": self._extrapolate_next_quadrant(pattern_key),
            "temporal_decay": 0.95
        })

    def _extrapolate_next_quadrant(self, pattern_key):
        parts = pattern_key.split("_")
        return parts[-1] if len(parts) >= 2 else "UNKNOWN"


class IntuitiveRecognizer:
    """Spinozan necessity recognizer for high-density fields."""

    def __init__(self, hlsf_engine):
        self.hlsf = hlsf_engine
        self.symmetry_threshold = 0.9
        self.density_threshold = 50

    def check_necessity(self, stimulus, current_node):
        field_density = len(self.hlsf.field_map)
        if field_density > self.density_threshold:
            symmetry_score = self._calculate_bilateral_symmetry()
            if symmetry_score > self.symmetry_threshold:
                necessity_vector = self._calculate_substance_vector(current_node)
                return {
                    "jump_triggered": True,
                    "necessity_vector": necessity_vector,
                    "substance_unity_score": symmetry_score,
                    "bypass_steps": field_density // 10,
                    "spinozan_certainty": 0.98,
                    "field_density": field_density
                }
        return {
            "jump_triggered": False,
            "field_density": field_density,
            "spinozan_certainty": 0.0,
            "substance_unity_score": self._calculate_bilateral_symmetry()
        }

    def _calculate_bilateral_symmetry(self):
        if not self.hlsf.field_map:
            return 0.0
        nodes = list(self.hlsf.field_map.values())
        if len(nodes) < 2:
            return 0.0
        mirror_count = 0
        coords_list = [n.coordinates for n in nodes]
        for i, c1 in enumerate(coords_list):
            for c2 in coords_list[i + 1:]:
                if len(c1) >= 2 and len(c2) >= 2:
                    if abs(c1[0] + c2[0]) < 0.2 and abs(c1[1] - c2[1]) < 0.2:
                        mirror_count += 1
        total_pairs = len(nodes) * (len(nodes) - 1) / 2
        return mirror_count / total_pairs if total_pairs > 0 else 0.0

    def _calculate_substance_vector(self, current_node):
        if not self.hlsf.field_map:
            return (0.0, 0.0)
        centroid = [0.0] * min(self.hlsf.dimension, 18)
        for node in self.hlsf.field_map.values():
            for i in range(len(centroid)):
                if i < len(node.coordinates):
                    centroid[i] += node.coordinates[i]
        count = len(self.hlsf.field_map)
        centroid = [c / count for c in centroid]
        return (centroid[0], centroid[1])


class SF_ORB_Controller:
    """Canonical Triple Triple Controller (Triad C)."""

    def __init__(self):
        print("Initializing SF-ORB Sovereign Logic...")
        self.engine = hlsf_singleton
        self.tribunal = FourMindTribunal(skg_path="core_4_minds")
        self.vaults = VaultManager()
        self.habit_tracker = HabitTracker(self.vaults)
        self.intuitive_recognizer = IntuitiveRecognizer(self.engine)
        self.bayes = BayesianEngine(alpha=1.5, beta=1.0)
        self._initialize_bayesian_priors()
        print("✓ Triple Triple Architecture Online")
        print("✓ Logic Triad C: Deductive | Inductive | Intuitive")

    def emergency_purge(self):
        """Manual density reset to restore SLA."""
        before = len(self.engine.field_map)
        if before > 1000:
            self.engine._edge_cutter_purge()
            after = len(self.engine.field_map)
            print(f"🧹 EMERGENCY PURGE: {before} → {after} nodes")
            return True
        return False

    def cognitively_emerge(self, stimulus):
        start_time = time.time()

        if not self._check_sovereignty(stimulus):
            return None

        self.habit_tracker.record_observation(stimulus)

        node = self.engine.map_adjacency(stimulus)

        intuition = self.intuitive_recognizer.check_necessity(stimulus, node)
        inductive = None if intuition.get("jump_triggered") else self.habit_tracker.predict_next()

        bypass = self.vaults.lightning_query(stimulus)
        if bypass:
            elapsed = (time.time() - start_time) * 1000
            print(f"⚡ LIGHTNING BYPASS ({elapsed:.2f}ms)")
            return bypass

        shadows = self.tribunal.generate_epistemic_shadow(stimulus)
        bayes_shadows = self._update_bayesian_shadows(shadows)

        logic_state = self._synthesize_logic_triad(inductive, intuition, bayes_shadows)

        neighbors = self.engine.get_recursive_neighbors(node, radius=3)
        thought_vec = self.engine.calculate_thought_vector(neighbors + [node]) if neighbors else (0.0,) * self.engine.dimension

        confidence = self._calculate_convergence(shadows, logic_state, thought_vec)

        spatial_coord = {
            "node_id": f"NODE_{node.n}_{node.k}",
            "recursion_depth": node.k,
            "coordinates": node.coordinates,
            "adjacency_value": node.adjacency_value
        }

        thought = CrossDomainPredicate(
            epistemic=shadows,
            spatial=spatial_coord,
            logic=logic_state,
            synthesis_confidence=confidence
        )

        self._update_bayesian_outcome(logic_state)

        self.vaults.crystallize(stimulus, {
            "predicate": thought.pulse(),
            "confidence": confidence,
            "triad_c_mode": logic_state.get("active_mode"),
            "field_density": logic_state.get("field_density", 0)
        })

        elapsed = (time.time() - start_time) * 1000
        mode = logic_state.get("active_mode", "GUARD")
        print(f"🧠 [{mode}] {elapsed:.1f}ms | Density: {logic_state.get('field_density', 0)}")
        return thought

    def _check_sovereignty(self, stimulus):
        if stimulus.get("meta", {}).get("test_mode") is True:
            return True
        if stimulus.get("type") == "surveillance_probe":
            print("⛔ SOVEREIGNTY VIOLATION: Surveillance detected")
            return False
        return True

    def _synthesize_logic_triad(self, inductive, intuitive, bayes_shadows):
        live_density = len(self.engine.field_map)
        breach_density = getattr(self.engine, "last_density_breach", 0)
        effective_density = max(live_density, breach_density)
        state = {
            "field_density": effective_density,
            "active_mode": "GUARD"
        }
        if intuitive.get("jump_triggered"):
            state.update({
                "intuitive_jump_triggered": True,
                "necessity_vector": intuitive.get("necessity_vector"),
                "spinozan_certainty": intuitive.get("spinozan_certainty"),
                "active_mode": "INTUITION-JUMP",
                "substance_unity_score": intuitive.get("substance_unity_score")
            })
            return state
        if inductive:
            confidence = inductive.get("confidence", 0)
            state.update({
                "inductive_prediction": inductive,
                "hume_vivacity": inductive.get("hume_vivacity", 0),
                "custom_habit_active": confidence > 0.35,
                "active_mode": "HABIT" if confidence > 0.35 else "GUARD-HABIT"
            })
        habit_post = self.bayes.calculate_posterior("habit_continues") or 0.0
        jump_post = self.bayes.calculate_posterior("jump_necessary") or 0.0
        guard_post = self.bayes.calculate_posterior("guard_sufficient") or 0.0
        state.update({
            "bayes_habit_prob": habit_post,
            "bayes_jump_prob": jump_post,
            "bayes_guard_prob": guard_post,
            "epistemic_bayes": bayes_shadows,
        })
        # Apply space-field pressure: high density should bias away from inert GUARD.
        density = state.get("field_density", 0)
        if state.get("active_mode") in ("GUARD", "GUARD-HABIT") and density >= self.engine.purge_trigger_threshold:
            state["active_mode"] = "GUARD-HABIT"
            state["density_penalty"] = 1.0
            print(f"🚫 GUARD INVALIDATED: Density {density} → Forced GUARD-HABIT")
        if density >= self.engine.max_field_density * 0.95 and state.get("active_mode") != "INTUITION-JUMP":
            state["active_mode"] = "INTUITION-JUMP"
            state["density_penalty"] = 1.5
            print(f"🚨 EMERGENCY JUMP: Critical density {density}")
        if state.get("active_mode") in ("GUARD", "GUARD-HABIT") and habit_post > 0.55:
            state["active_mode"] = "HABIT"
        if state.get("active_mode") != "INTUITION-JUMP" and jump_post > 0.45:
            state["active_mode"] = "INTUITION-JUMP"
        if density >= self.engine.purge_trigger_threshold and state.get("active_mode") == "GUARD":
            print(f"CRITICAL: GUARD survived density breach ({density}) — enforcement failed!")
        return state

    def _calculate_convergence(self, shadows, logic, thought_vec):
        base = 0.85
        if logic.get("intuitive_jump_triggered"):
            base += 0.14
        elif logic.get("custom_habit_active"):
            base += 0.08
        if len(shadows) >= 3:
            base += 0.02
        vec_magnitude = sum(abs(v) for v in thought_vec) if thought_vec else 0.0
        base += min(vec_magnitude * 0.001, 0.02)
        return min(base, 0.99)

    def _initialize_bayesian_priors(self):
        seed_priors = {
            "habit_continues": (0.6, 1.2),
            "jump_necessary": (0.3, 0.8),
            "guard_sufficient": (0.7, 1.5),
        }
        for hyp, (prob, strength) in seed_priors.items():
            self.bayes.set_prior(hyp, prob, evidence_strength=strength)
            self.bayes.add_evidence(
                hypothesis=hyp,
                evidence_id=f"seed_{hyp}",
                likelihood=prob,
                source="init",
                reliability=0.01,
            )

    def _update_bayesian_shadows(self, shadows):
        bayes_view = {}
        timestamp_id = f"stim_{int(time.time()*1000)}"
        for mind_name, shadow in shadows.items():
            hyp = f"{mind_name}_pattern_persistence"
            likelihood = shadow.get("confidence", 0.5)
            reliability = shadow.get("reliability", 1.0)
            if hyp not in self.bayes.priors:
                self.bayes.set_prior(hyp, 0.5, evidence_strength=1.0)
            self.bayes.add_evidence(
                hypothesis=hyp,
                evidence_id=f"{timestamp_id}_{mind_name}",
                likelihood=likelihood,
                source=mind_name,
                reliability=reliability,
            )
            bayes_view[mind_name] = self.bayes.calculate_posterior(hyp) or likelihood
        return bayes_view

    def _update_bayesian_outcome(self, logic_state):
        mode = logic_state.get("active_mode", "GUARD")
        pred = logic_state.get("inductive_prediction", {}) or {}
        success = mode in ("HABIT", "GUARD-HABIT") and pred.get("confidence", 0) > 0.4
        self.bayes.update_with_outcome("habit_continues", success=success, weight=0.7)
        jump_success = mode == "INTUITION-JUMP" and logic_state.get("intuitive_jump_triggered")
        self.bayes.update_with_outcome("jump_necessary", success=bool(jump_success), weight=0.6)
        guard_success = mode == "GUARD" and not success and not jump_success
        self.bayes.update_with_outcome("guard_sufficient", success=guard_success, weight=0.5)


if __name__ == "__main__":
    orb = SF_ORB_Controller()
    sample = {
        "type": "cursor_movement",
        "coordinates": [100, 200],
        "velocity": 5.0,
        "intent": "navigation",
        "meta": {"test_mode": True}
    }
    orb.cognitively_emerge(sample)
