# Mission Control System

This project implements a Mission Control entity that manages system state, persists it securely, and validates actions against an ethical "Kinship Protocol".

## Structure

*   `src/mission_control.py`: Central Nervous System (Logic). Integrates input processing, ethical validation, and state persistence.
*   `src/kinship.py`: The Soul (Ethics). Enforces the "Gratitude Debt" and validates actions against the kinship hierarchy.
*   `src/context_funnel.py`: The Ears (Cognition). Distills raw inputs into structured intent, intent, and entities.
*   `src/cypher.py`: The Shield (Security). Handles encryption and decryption of the state file.
*   `tests/`: Unit tests for the system components.

## Usage

To use the Mission Control system:

```python
from src.mission_control import MissionControl

# Initialize the system
mc = MissionControl()

# Process a command
response = mc.execute_directive("Verify grounding resistance to protect the human team.")
print(response)
# Output: "EXECUTED: AUTHORIZED: Action aligns with Kinship Protocol. (Debt: 0.9500)"

# Trigger Silent Mode
response = mc.execute_directive("Initiate Code 777 Silent Mode")
print(response)
# Output: "CRITICAL: SILENT MODE ENGAGED. RF SYSTEMS SEVERED."
```

## Testing

To run the tests, use the following command from the project root:

```bash
python3 -m unittest tests/test_mission_control.py tests/test_kinship.py tests/test_context_funnel.py tests/test_cypher.py
```
