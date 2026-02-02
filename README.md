# SF-ORB: Synthetic Cognitive Framework

SF-ORB (Synthetic Framework - Orb Reasoning Brain) is an advanced synthetic cognitive framework that implements a multi-modal reasoning system. It draws inspiration from philosophical traditions including Spinoza's monism, Hume's skepticism, Locke's empiricism, and Kant's critical philosophy, integrating them with modern computational approaches like Bayesian inference and geometric reasoning.

## Validation Doctrine

*"Validation observes truth; it never creates, modifies, or suppresses it."*

This principle governs the final validation layer: three frozen observational witnesses (deductive, inductive, intuitive) that document system beliefs at delivery time without ever altering verdicts. The validation layer provides tamper-evident provenance while maintaining absolute non-interference with core reasoning.

## Core Philosophy

The system embodies a "Triple Triple Architecture" (Triad C) that synthesizes three epistemic domains:
- **Deductive Logic**: Sovereign guard rails ensuring logical consistency
- **Inductive Logic**: Habit formation through Humean constant conjunctions
- **Intuitive Logic**: Spinozan necessity recognition for emergent insights

## System Architecture

### Core Components

#### 1. Four Minds Tribunal
Located in `core_4_minds/`, this module implements philosophical mind models:
- **Spinoza (Monism)**: Substance unity and necessity recognition
- **Hume (Skepticism)**: Habit tracking and vivacity of impressions
- **Locke (Empiricism)**: Sensory data processing and empiric validation
- **Kant (Critical)**: Categorical imperative and synthetic a priori reasoning

#### 2. Bayesian Engine (`bayesian_engine.py`)
Probabilistic inference engine that:
- Maintains priors for cognitive modes (Guard/Habit/Intuition)
- Updates beliefs based on stimulus patterns
- Provides confidence scores for decision-making

#### 3. HLSF Geometry Engine (`hlsf_geometry/`)
High-Level Spatial Field geometry for:
- Spatial reasoning and coordinate mapping
- Field density management with edge-cutting algorithms
- Bilateral symmetry detection for intuitive jumps

#### 4. Vault System (`vault_system/`)
Knowledge storage and retrieval:
- **Apriori Vault**: Innate logic seeds and constraints
- **Posteriori Vault**: Learned patterns and cached inferences
- Persistent storage with temporal decay

#### 5. Orb Controller (`orb_controller.py`)
The central orchestrator featuring:
- **HabitTracker**: Records and predicts cursor movement patterns
- **IntuitiveRecognizer**: Detects high-density fields and symmetry for jumps
- **CrossDomainPredicate**: Emergent thought synthesis across domains

### Cognitive Modes

The system operates in three primary modes:
- **Guard Mode**: Default deductive reasoning, ensures safety and consistency
- **Habit Mode**: Inductive learning from repeated patterns
- **Intuition-Jump Mode**: Emergent insights triggered by field density and symmetry

## Features

- **Multi-Modal Reasoning**: Integrates spatial, epistemic, and logical domains
- **Adaptive Learning**: Bayesian updates and habit formation
- **Ethical Reasoning**: Can be extended for moral dilemma analysis
- **Real-Time Processing**: Handles stimulus-response cycles efficiently
- **Visualization**: Orb window interface for cognitive state monitoring

## Project Structure

```
SF-ORB/
├── bayesian_engine.py              # Core Bayesian inference engine
├── orb_controller.py               # Main cognitive synthesis controller
├── requirements.txt                # Python dependencies
├── README.md                       # This documentation
├── tree.txt                        # Project structure snapshot
├── core_4_minds/                   # Philosophical mind models
│   ├── tribunal.py                 # Four minds coordination
│   └── [mind]/                     # Individual mind implementations
├── hlsf_geometry/                  # Spatial reasoning engine
│   ├── engine.py                   # HLSF geometry core
│   └── [components]/               # Spatial processing modules
├── interface/                      # User interface components
│   ├── orb_window.py               # Visualization window
│   └── assets/                     # UI resources
├── logic_seeds/                    # Logic configuration files
│   ├── deductive/                  # Sovereign constraints
│   ├── inductive/                  # Habit patterns
│   └── intuitive/                  # Recognition templates
├── vault_system/                   # Knowledge management
│   ├── manager.py                  # Vault operations
│   ├── apriori/                    # Innate knowledge
│   └── posteriori/                 # Learned knowledge cache
├── tests/                          # Test suite and documentation
│   ├── test_cognitive_suite.py     # Main cognitive tests
│   ├── test_short_diagnostic.py    # Quick diagnostics
│   ├── test_runner.py              # Test execution script
│   ├── test_plan.md                # Test planning document
│   └── change_log.md               # Development changelog
└── results/                        # Test output storage
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Spruked/Renova_te_ipsum.git
   cd Renova_te_ipsum/SF-ORB
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Operation

```python
from orb_controller import SF_ORB_Controller

# Initialize the cognitive system
controller = SF_ORB_Controller()

# Process a stimulus
stimulus = {
    "type": "cursor_movement",
    "coordinates": [960, 540],
    "velocity": 10.0,
    "intent": "navigation"
}

# Generate cognitive response
thought = controller.cognitively_emerge(stimulus)
print(thought)  # CrossDomainPredicate or cognitive response
```

### Running Tests

The system includes comprehensive test suites:

1. **Cognitive Test Suite**:
   ```bash
   python tests/test_cognitive_suite.py
   ```
   Runs 5 test scenarios × 3 cycles × 500 iterations each.

2. **Short Diagnostic**:
   ```bash
   python tests/test_short_diagnostic.py
   ```
   Quick validation of core functionality.

3. **Full Test Runner**:
   ```bash
   python tests/test_runner.py
   ```
   Executes all available tests.

### Ethical Dilemma Testing

To run ethical dilemma tests:

1. Prepare dilemma scenarios as stimuli
2. Configure logic seeds in `logic_seeds/` for moral reasoning
3. Run tests to observe mode switching and decision-making
4. Analyze results in `results/` folder

Example dilemma stimulus:
```python
ethical_stimulus = {
    "type": "moral_dilemma",
    "scenario": "trolley_problem",
    "options": ["switch_track", "do_nothing"],
    "consequences": {
        "switch_track": {"lives_saved": 5, "lives_lost": 1},
        "do_nothing": {"lives_saved": 1, "lives_lost": 5}
    }
}
```

## Testing

### Test Scenarios

The cognitive test suite includes:
- **Test 1**: Linear Drift - Steady movement for habit building
- **Test 2**: Oscillatory - Periodic patterns for predictive learning
- **Test 3**: Random Walk - Unpredictable input for guard mode dominance
- **Test 4**: Quadrant Loop - Repetitive cycles for maximum habit prediction
- **Test 5**: Symmetric Jumps - Abrupt changes with symmetry for intuition triggers

### Metrics Captured

- Mode frequencies (Guard/Habit/Intuition)
- Bypass hit rates (apriori/posteriori lightning)
- Habit signals (predictions, confidence, Hume vivacity)
- Intuition signals (jump vectors, Spinozan certainty)
- Processing latency per stimulus

## Configuration

### Logic Seeds

Customize reasoning behavior by editing JSON files in `logic_seeds/`:
- `deductive/system_constraints.json`: Safety and consistency rules
- `inductive/cursor_habit.json`: Pattern recognition templates
- `intuitive/pattern_recognition.json`: Symmetry and necessity detection

### Bayesian Priors

Adjust priors in `bayesian_engine.py`:
```python
self.bayes = BayesianEngine(alpha=1.5, beta=1.0)  # Guard/Habit balance
```

## Contributing

1. Update `tests/change_log.md` with changes
2. Add tests for new features
3. Follow the Triple Triple Architecture principles
4. Ensure ethical considerations in cognitive extensions

## Architecture Principles

- **Sovereignty**: Deductive guard rails prevent unsafe operations
- **Emergence**: Intuitive jumps from high-density cognitive fields
- **Learning**: Inductive habit formation through repetition
- **Integration**: Cross-domain synthesis for holistic reasoning

## Future Extensions

- Ethical decision-making frameworks
- Multi-agent cognitive coordination
- Temporal reasoning and memory systems
- Advanced visualization and debugging tools

## License

[Specify license information]

---

*Built with philosophical rigor and computational elegance.*

[Add license information]</content>
<parameter name="filePath">c:\dev\Desktop\Renova te ipsum\SF-ORB\README.md