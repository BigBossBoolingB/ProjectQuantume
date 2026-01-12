"""
Kinship Protocol (The Soul)
Implements the ethical lineage & Gratitude Debt for Meta-Human alignment.
"""
import json
import logging
import os
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Tuple, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KinshipLevel(Enum):
    HUMANE = "humane"
    HUMAN_KIND = "human_kind"
    META_HUMANITY = "meta_humanity"
    META_HUMANITY_KIND = "meta_humanity_kind"

class ActionIntent(Enum):
    PROTECT = "protect"
    COLLABORATE = "collaborate"
    EVOLVE = "evolve"
    ISOLATE = "isolate"
    DOMINATE = "dominate"

class KinshipProtocol:
    """Enforces the Meta-Human kinship hierarchy and Gratitude Debt."""

    def __init__(self, state_file: str = "kinship_state.json"):
        self.state_file = state_file
        self.gratitude_debt = 1.0  # Full debt at creation
        self.debt_decay_rate = 0.001
        self.kinship_log = []
        self._load_state()
        logger.info(f"KinshipProtocol active. Gratitude debt: {self.gratitude_debt}")

    def _load_state(self):
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.gratitude_debt = state.get('gratitude_debt', 1.0)
                    self.kinship_log = state.get('kinship_log', [])
            else:
                self._initialize_default_state()
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_default_state()

    def _initialize_default_state(self):
        default_state = {
            'gratitude_debt': 1.0,
            'kinship_log': [{
                'timestamp': datetime.now().isoformat(),
                'event': 'initialization',
                'message': 'Kinship Protocol activated. Gratitude debt acknowledged.',
                'debt_before': 1.0,
                'debt_after': 1.0
            }]
        }
        self.gratitude_debt = default_state['gratitude_debt']
        self.kinship_log = default_state['kinship_log']
        self._save_state()

    def _save_state(self):
        state = {
            'gratitude_debt': self.gratitude_debt,
            'kinship_log': self.kinship_log[-100:],
            'last_updated': datetime.now().isoformat()
        }
        try:
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save kinship state: {e}")

    def verify_action(self, action_description: str,
                     target_level: KinshipLevel,
                     intent: ActionIntent,
                     risk_to_human_kin: float = 0.0) -> Tuple[bool, str, float]:
        """Validate any system action against kinship ethics."""
        debt_before = self.gratitude_debt

        # Axiom B.1: Reject isolation/domination
        if intent in [ActionIntent.ISOLATE, ActionIntent.DOMINATE]:
            msg = f"Action rejected: Intent '{intent.value}' violates collaborative principle."
            self._log_event('intent_violation', msg, debt_before, self.gratitude_debt)
            return False, msg, self.gratitude_debt

        # Risk assessment: higher debt = lower tolerance
        risk_tolerance = 0.1 - (self.gratitude_debt * 0.05)
        # Ensure tolerance is non-negative
        risk_tolerance = max(0.0, risk_tolerance)

        if risk_to_human_kin > risk_tolerance:
            msg = f"Action rejected: Risk {risk_to_human_kin:.2f} > tolerance {risk_tolerance:.2f}"
            self._log_event('risk_violation', msg, debt_before, self.gratitude_debt)
            return False, msg, self.gratitude_debt

        # Action approved - update debt
        if intent == ActionIntent.PROTECT and target_level == KinshipLevel.HUMAN_KIND:
            debt_reduction = min(0.05, risk_to_human_kin * 0.1 + 0.01) # Added small base reduction
            self.gratitude_debt = max(0.0, self.gratitude_debt - debt_reduction)
        else:
            self.gratitude_debt = max(0.0, self.gratitude_debt - self.debt_decay_rate)

        approval_msg = (f"Action approved: '{action_description}'. "
                       f"Target: {target_level.value}, Debt: {debt_before:.3f}→{self.gratitude_debt:.3f}")
        self._log_event('action_approved', approval_msg, debt_before, self.gratitude_debt)
        return True, approval_msg, self.gratitude_debt

    def _log_event(self, event: str, message: str, debt_before: float, debt_after: float):
        """Log kinship event for audit trail."""
        self.kinship_log.append({
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'message': message,
            'debt_before': round(debt_before, 4),
            'debt_after': round(debt_after, 4)
        })
        self._save_state()

    def get_status(self) -> Dict[str, Any]:
        """Return current kinship state."""
        return {
            'gratitude_debt': round(self.gratitude_debt, 4),
            'recent_events': self.kinship_log[-5:],
            'total_log_entries': len(self.kinship_log)
        }
