import json
import os
from typing import Dict, Any

class MissionControl:
    def __init__(self, state_file: str = None):
        if state_file is None:
            # Default to system_state.json in the project root (assuming src is one level deep)
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.state_file = os.path.join(base_dir, "system_state.json")
        else:
            self.state_file = state_file

        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if not os.path.exists(self.state_file):
            raise FileNotFoundError(f"State file {self.state_file} not found.")

        with open(self.state_file, 'r') as f:
            return json.load(f)

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def get_meta(self) -> Dict[str, Any]:
        return self.state.get("system_state", {}).get("meta", {})

    def get_status(self) -> str:
        return self.get_meta().get("status", "UNKNOWN")

    def update_status(self, new_status: str):
        if "system_state" not in self.state:
            self.state["system_state"] = {}
        if "meta" not in self.state["system_state"]:
            self.state["system_state"]["meta"] = {}

        self.state["system_state"]["meta"]["status"] = new_status
        self.save_state()

    def get_infrastructure_status(self) -> Dict[str, Any]:
        return self.state.get("system_state", {}).get("physical_infrastructure", {})

    def get_security_protocols(self) -> Dict[str, Any]:
        return self.state.get("system_state", {}).get("security_protocols", {})

    def get_next_critical_event(self) -> Dict[str, Any]:
        return self.state.get("system_state", {}).get("next_critical_event", {})
