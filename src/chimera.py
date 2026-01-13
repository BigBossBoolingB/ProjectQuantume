import json
import os
from typing import Dict, Any, List

class ChimeraNode:
    def __init__(self, state_file: str = "chimera_state.json"):
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if not os.path.exists(self.state_file):
            raise FileNotFoundError(f"State file {self.state_file} not found.")

        with open(self.state_file, 'r') as f:
            return json.load(f)

    def get_identity(self) -> Dict[str, Any]:
        return self.state.get("system_identity", {})

    def get_health_status(self) -> str:
        vitals = self.state.get("infrastructure_health", {}).get("vitals", {})
        return vitals.get("status", "UNKNOWN")

    def get_active_directives(self) -> List[str]:
        return self.state.get("active_mission", {}).get("directives", [])

    def get_swarm_nodes(self) -> List[Dict[str, Any]]:
        return self.state.get("swarm_topology", {}).get("nodes", [])

    def get_hazard_alerts(self) -> List[Dict[str, Any]]:
        return self.state.get("environment_context", {}).get("hazards_detected", [])

    def update_intent(self, new_intent: str):
        if "cognitive_state" not in self.state:
            self.state["cognitive_state"] = {}
        self.state["cognitive_state"]["current_intent"] = new_intent
        self._save_state()

    def _save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
