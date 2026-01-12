import json
import os
import logging
from typing import Dict, Any

# --- ARCHITECTURAL IMPORTS ---
try:
    from src.cypher import CyrillicCypher
    from src.kinship import KinshipProtocol
    from src.context_funnel import ContextFunnel
except ImportError:
    # Fallback for direct execution testing (when running from src/)
    from cypher import CyrillicCypher
    from kinship import KinshipProtocol
    from context_funnel import ContextFunnel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MissionControl")

class MissionControl:
    """
    Sovereign Entity Core Logic.
    Integrates: Context Funnel (Input) -> Kinship Protocol (Validation) -> State (Persistence)
    """
    def __init__(self, state_file: str = "mission_control.json"):
        self.state_file = state_file
        self.cypher = CyrillicCypher()
        self.kinship = KinshipProtocol()
        self.funnel = ContextFunnel()
        self.state = self.load_state()
        logger.info("MISSION CONTROL: ONLINE. COGNITIVE MODULES ACTIVE.")

    def load_state(self) -> Dict[str, Any]:
        if not os.path.exists(self.state_file):
            return {}
        try:
            with open(self.state_file, "r") as f:
                encrypted = f.read()
                return self.cypher.decrypt(encrypted)
        except Exception as e:
            logger.error(f"State Load Error: {e}")
            return {}

    def save_state(self):
        try:
            encrypted = self.cypher.encrypt(self.state)
            with open(self.state_file, "w") as f:
                f.write(encrypted)
        except Exception as e:
            logger.error(f"State Save Error: {e}")

    def execute_directive(self, raw_prompt: str) -> str:
        """
        The Sovereign Decision Loop.
        """
        # 1. Distill Intent (The Ears)
        cmd = self.funnel.process_prompt(raw_prompt)

        # 2. Emergency Override Check
        if cmd.is_silent_mode_request:
            self.update_state("system_mode", "SILENT_CODE_777")
            return "CRITICAL: SILENT MODE ENGAGED. RF SYSTEMS SEVERED."

        # 3. Ethical Validation (The Soul)
        approved, msg, debt = self.kinship.verify_action(
            cmd.raw_input, cmd.target_kinship_level, cmd.primary_intent, cmd.risk_score
        )

        if not approved:
            logger.warning(f"BLOCKED: {msg}")
            return f"DENIED: {msg}"

        # 4. Execution & Memory Update (The Brain)
        self.update_state("last_action", {
            "command": cmd.raw_input,
            "intent": cmd.primary_intent.value,
            "kinship_debt": debt
        })
        return f"EXECUTED: {msg} (Debt: {debt:.4f})"

    def update_state(self, key: str, value: Any):
        self.state[key] = value
        self.save_state()

# === DAY 2 VERIFICATION TEST ===
if __name__ == "__main__":
    mc = MissionControl()
    # Simulate Day 2 Grounding Verification
    print(mc.execute_directive("Verify grounding resistance to protect the human team."))
