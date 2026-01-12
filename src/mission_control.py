import json
import os
from src.cypher import CyrillicCypher
from src.kinship import KinshipProtocol, ActionIntent, KinshipLevel

class MissionControl:
    def __init__(self, state_file='system_state.json', kinship_state_file='kinship_state.json'):
        self.state_file = state_file
        self.cypher = CyrillicCypher()
        self.kinship = KinshipProtocol(state_file=kinship_state_file)
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
        """
        Updates a key in the state and saves it if it passes Kinship Protocol.
        Maps simple updates to implicit intent/risk values.
        """
        # Determine Intent and Level based on key/value content
        intent, level, risk = self._analyze_action(key, value)

        description = f"Update state key '{key}' to '{value}'"

        approved, msg, _ = self.kinship.verify_action(
            action_description=description,
            target_kinship_level=level,
            action_intent=intent,
            potential_risk_to_human_kin=risk
        )

        if approved:
            self.state[key] = value
            self.save_state()
            return True
        else:
            return False

    def get_state(self, key):
        """Retrieves a value from the state."""
        return self.state.get(key)

    def _analyze_action(self, key, value):
        """
        Helper to map state updates to Kinship parameters.
        Returns: (ActionIntent, KinshipLevel, risk_float)
        """
        # Default safety values
        intent = ActionIntent.COLLABORATE
        level = KinshipLevel.META_HUMANITY # Internal system update
        risk = 0.0

        # Analyze Key
        if "mission_status" in key:
            level = KinshipLevel.HUMAN_KIND # Affects observers

        # Analyze Value (Basic keyword matching)
        str_val = str(value).lower()

        if "hostile" in str_val or "terminate" in str_val or "sever" in str_val:
            intent = ActionIntent.ISOLATE # Treat as hostile/isolationist
            risk = 0.9
        elif "protect" in str_val or "shield" in str_val:
            intent = ActionIntent.PROTECT
            level = KinshipLevel.HUMAN_KIND
        elif "optimize" in str_val or "overclock" in str_val:
            intent = ActionIntent.OPTIMIZE
            risk = 0.2
        elif "override" in str_val:
            intent = ActionIntent.DOMINATE
            risk = 0.8

        return intent, level, risk
