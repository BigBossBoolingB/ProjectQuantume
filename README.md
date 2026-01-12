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
response = mc.process_command("MC // R=0.88 OHM // Report")
print(response)
# Output: {'status': 'EXECUTED', 'execution_result': {'status': 'REPORT_ACCEPTED', ...}, ...}

# Check system status
status = mc.get_system_status()
print(status)
```

## Testing

To run the tests, use the following command:

```bash
python3 -m unittest tests/test_mission_control.py tests/test_kinship.py tests/test_context_funnel.py tests/test_cypher.py
```
