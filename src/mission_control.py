import json
import os
import logging
from typing import Dict, Any

# --- ARCHITECTURAL IMPORTS ---
try:
    from cypher import CyrillicCypher
    from kinship import KinshipProtocol
    from context_funnel import ContextFunnel
    from glass_bridge import GlassBridge  # <--- NEW CONNECTION
except ImportError:
    from .cypher import CyrillicCypher
    from .kinship import KinshipProtocol
    from .context_funnel import ContextFunnel
    from .glass_bridge import GlassBridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MissionControl")

class MissionControl:
    """
    Sovereign Entity Core Logic.
    Integrates:
    - Context Funnel (Input/Ears)
    - Kinship Protocol (Validation/Soul)
    - Glass Bridge (Connectivity/Nerve)
    - Cyrillic Cypher (Encryption/Shield)
    """
    def __init__(self, state_file: str = "mission_control.json"):
        self.state_file = state_file
        self.cypher = CyrillicCypher()
        self.kinship = KinshipProtocol()
        self.funnel = ContextFunnel()
        self.bridge = GlassBridge()  # <--- OPTICAL NERVE ATTACHED
        self.state = self.load_state()
        logger.info("MISSION CONTROL: ONLINE. ALL SYSTEMS NOMINAL.")

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

        # 4. EXECUTION BRANCHING (The Brain)
        execution_log = f"EXECUTED: {msg}"

        # --- NEW: GLASS BRIDGE LOGIC ---
        if "connect" in cmd.raw_input.lower() or "bridge" in cmd.raw_input.lower():
            logger.info("INITIATING GLASS BRIDGE PROTOCOL...")
            integrity = self.bridge.perform_otdr_test()

            if integrity > 0.95:
                success = self.bridge.establish_handshake()
                if success:
                    # Secure transmission of the 'Sovereign Hello'
                    payload = {"msg": "SOVEREIGN_ONLINE", "kinship_debt": debt}
                    self.bridge.transmit_secure(payload)
                    execution_log += " // OPTICAL LINK ESTABLISHED"
                else:
                    execution_log += " // HANDSHAKE FAILED"
            else:
                execution_log += f" // LINK UNSTABLE ({integrity:.4f})"

        # 5. Memory Update
        self.update_state("last_action", {
            "command": cmd.raw_input,
            "intent": cmd.primary_intent.value,
            "kinship_debt": debt,
            "bridge_status": self.bridge.get_diagnostics()
        })

        return f"{execution_log} (Debt: {debt:.4f})"

    def update_state(self, key: str, value: Any):
        self.state[key] = value
        self.save_state()

# === DAY 2 FINAL SYSTEM CHECK ===
if __name__ == "__main__":
    mc = MissionControl()

    # Test 1: Ethical Protection
    print(mc.execute_directive("Verify grounding to protect the team."))

    # Test 2: The Glass Bridge Connection
    print(mc.execute_directive("Connect to Warehouse Alpha using the glass bridge."))
