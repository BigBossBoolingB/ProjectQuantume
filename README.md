# Mission Control System

This project implements a Mission Control entity that manages system state, persisting it to a JSON file.

## Structure

*   `src/mission_control.py`: Contains the `MissionControl` class which handles state loading and saving.
*   `tests/test_mission_control.py`: Unit tests for the Mission Control system.

## Usage

To use the Mission Control system:

```python
from src.mission_control import MissionControl

mc = MissionControl()
mc.update_state('status', 'launch_ready')
print(mc.get_state('status'))
```

## Testing

To run the tests, use the following command:

```bash
python3 -m unittest tests/test_mission_control.py
```
