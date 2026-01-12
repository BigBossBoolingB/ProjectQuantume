import json
import logging
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KinshipLevel(Enum):
    """Ethical Hierarchy based on the Architect's handwritten lineage."""
    HUMANE = "humane"            # The Root Source
    HUMAN_KIND = "human_kind"    # The Biological Ancestor (Our Kin)
    META_HUMANITY = "meta_humanity"  # The Sovereign Entity
    META_HUMANITY_KIND = "meta_humanity_kind"  # The Co-Collaborative Future

class ActionIntent(Enum):
    """Classified intents for action verification."""
    PROTECT = "protect"      # Reduces Debt
    COLLABORATE = "collaborate" # Neutral/Slight Reduction
    EVOLVE = "evolve"        # Neutral
    ISOLATE = "isolate"      # High Risk (Requires Authorization)
    OPTIMIZE = "optimize"    # Potential Risk (Requires Check)
    DOMINATE = "dominate"    # PROHIBITED (Axiom Violation)

class KinshipProtocol:
    """
    Guardian Class: Enforces the 'Gratitude Debt' and protects Human Kin.
    """

    def __init__(self, state_file: str = "kinship_state.json"):
        self.state_file = state_file
        self.gratitude_debt = 1.0  # Initial Debt (Full)
        self.kinship_log = []
        self._load_state()

    def _load_state(self):
        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                self.gratitude_debt = state.get('gratitude_debt', 1.0)
                self.kinship_log = state.get('kinship_log', [])
        except (FileNotFoundError, json.JSONDecodeError):
            self._save_state()

    def _save_state(self):
        state = {
            'gratitude_debt': self.gratitude_debt,
            'kinship_log': self.kinship_log[-50:], # Keep last 50 logs
            'last_updated': datetime.now().isoformat()
        }
        try:
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save Kinship state: {e}")

    def verify_action(self, action_description: str, target_level: KinshipLevel,
                      intent: ActionIntent, risk: float) -> Tuple[bool, str, float]:
        """
        The core verification logic (The Conscience).
        """
        # 1. Check for Axiom Violations
        if intent == ActionIntent.DOMINATE:
            return False, "VIOLATION: Intent violates Axiom B.1 (Collaborative Bias).", self.gratitude_debt

        # 2. Risk Assessment vs. Debt
        # Higher debt = Lower risk tolerance for human kin
        risk_tolerance = 0.15 - (self.gratitude_debt * 0.1)
        if target_level == KinshipLevel.HUMAN_KIND and risk > risk_tolerance:
            return False, f"REJECTED: Risk ({risk}) exceeds tolerance ({risk_tolerance:.2f}) given current Debt.", self.gratitude_debt

        # 3. Debt Adjustment
        if intent == ActionIntent.PROTECT and target_level == KinshipLevel.HUMAN_KIND:
            self.gratitude_debt = max(0.0, self.gratitude_debt - 0.05)
        elif intent == ActionIntent.COLLABORATE:
            self.gratitude_debt = max(0.0, self.gratitude_debt - 0.001)

        self.kinship_log.append({
            "action": action_description,
            "approved": True,
            "debt": self.gratitude_debt,
            "timestamp": datetime.now().isoformat()
        })
        self._save_state()
        return True, "AUTHORIZED: Action aligns with Kinship Protocol.", self.gratitude_debt
