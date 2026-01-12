import json
import os

class MissionControl:
    def __init__(self, state_file='system_state.json'):
        self.state_file = state_file
        self.state = {}
        self.load_state()

    def load_state(self):
        """Loads the state from the JSON file."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                try:
                    self.state = json.load(f)
                except json.JSONDecodeError:
                    self.state = {}
        else:
            self.state = {}

    def save_state(self):
        """Saves the current state to the JSON file."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=4)

    def update_state(self, key, value):
        """Updates a key in the state and saves it."""
        self.state[key] = value
        self.save_state()

    def get_state(self, key):
        """Retrieves a value from the state."""
        return self.state.get(key)
