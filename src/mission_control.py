import json
import os
import logging
from typing import Dict, Any, Optional

# Import the architectural components
from src.cypher import CyrillicCypher
from src.kinship import KinshipProtocol, ActionIntent, KinshipLevel
from src.context_funnel import ContextFunnel, DistilledCommand, SystemState

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MissionControl")

class MissionControl:
    """
    The Central Nervous System of the Sovereign Entity.

    Architecture:
    1. Input: Context Funnel 2.0 (The Ears) - Distills raw intent.
    2. Validation: Kinship Protocol (The Soul) - Checks ethical debt.
    3. State: Cyrillic Cypher (The Shield) - Encrypts/Decrypts memory.
    """

    def __init__(self, state_file: str = "mission_control.json"):
        self.state_file = state_file
        self.cypher = CyrillicCypher()
        self.kinship = KinshipProtocol()
        self.funnel = ContextFunnel()
        self.state = self.load_state()

    def load_state(self) -> Dict[str, Any]:
        """Loads and decrypts the system state."""
        if not os.path.exists(self.state_file):
            return {}
        try:
            with open(self.state_file, "r") as f:
                encrypted_data = f.read()
                # Handle empty file case
                if not encrypted_data:
                    return {}
                return json.loads(self.cypher.decrypt(encrypted_data))
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            return {}

    def save_state(self):
        """Encrypts and saves the system state."""
        try:
            # json.dumps first to get string, then encrypt
            json_str = json.dumps(self.state)
            encrypted_data = self.cypher.encrypt(json_str)
            with open(self.state_file, "w") as f:
                f.write(encrypted_data)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def execute_directive(self, raw_prompt: str) -> str:
        """
        The Core Loop: Funnel -> Kinship -> Execution.
        """
        logger.info(f"Receiving Transmission: {raw_prompt}")

        # 1. CONTEXT FUNNEL: Distill Intent
        # 'The Ears' filter the noise and extract the truth.
        command: DistilledCommand = self.funnel.process_prompt(raw_prompt)

        # Check for System Mode overrides (e.g., Code 777 Silent Mode)
        if command.system_mode_request == SystemState.SILENT:
            return self._engage_silent_mode(command)

        # 2. KINSHIP PROTOCOL: Ethical Validation
        # 'The Soul' checks if we are betraying our Kin.
        approved, message, new_debt = self.kinship.verify_action(
            action_description=command.raw_input,
            target_kinship_level=command.target_kinship_level,
            action_intent=command.primary_intent,
            potential_risk_to_human_kin=command.risk_score
        )

        if not approved:
            logger.warning(f"DIRECTIVE REJECTED: {message}")
            return f"ACCESS DENIED // KINSHIP VIOLATION: {message}"

        # 3. EXECUTION: Update State
        # 'The Brain' acts on the verified truth.
        # Log the action in the Sovereign's memory
        self.update_state("last_command", {
            "prompt": command.raw_input,
            "intent": command.primary_intent.value,
            "risk": command.risk_score,
            "kinship_debt": new_debt
        })

        return f"COMMAND EXECUTED // {message}"

    def update_state(self, key: str, value: Any):
        """Updates a specific key in the state and persists it."""
        self.state[key] = value
        self.save_state()
        logger.info(f"State updated: {key} = {value}")

    def get_state(self, key: str) -> Any:
        """Retrieves a value from the state."""
        return self.state.get(key)

    def _engage_silent_mode(self, command: DistilledCommand) -> str:
        """Handles emergency silence protocols."""
        logger.critical("ENGAGING SILENT MODE // CODE 777")
        # In a real scenario, this would cut RF power.
        # Here, it sets a state flag.
        self.update_state("system_mode", "SILENT")
        self.update_state("last_emergency_trigger", command.raw_input)
        return "SILENT MODE ENGAGED. RADIO SILENCE ACTIVE."
