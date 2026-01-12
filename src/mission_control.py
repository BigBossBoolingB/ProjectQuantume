import json
import os
from src.cypher import CyrillicCypher
from src.kinship import KinshipProtocol

class MissionControl:
    def __init__(self, state_file='system_state.json'):
        self.state_file = state_file
        self.cypher = CyrillicCypher()
        self.kinship = KinshipProtocol()
        self.state = {}
        self.load_state()

    def load_state(self):
        """Loads the state from the JSON file."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                content = f.read()
                try:
                    # Attempt to decrypt and load
                    if content:
                        decrypted_content = self.cypher.decrypt(content)
                        self.state = json.loads(decrypted_content)
                    else:
                        self.state = {}
                except (json.JSONDecodeError, Exception):
                    # Fallback or empty state on corruption/format change
                    self.state = {}
        else:
            self.state = {}

    def save_state(self):
        """Saves the current state to the JSON file."""
        json_str = json.dumps(self.state, indent=4)
        encrypted_content = self.cypher.encrypt(json_str)
        with open(self.state_file, 'w') as f:
            f.write(encrypted_content)

    def update_state(self, key, value):
        """Updates a key in the state and saves it if it passes Kinship Protocol."""
        if self.kinship.verify_update(key, value):
            self.state[key] = value
            self.save_state()
            return True
        else:
            return False

    def get_state(self, key):
        """Retrieves a value from the state."""
        return self.state.get(key)
