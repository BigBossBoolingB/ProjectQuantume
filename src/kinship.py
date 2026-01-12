"""
Kinship Protocol Module

Implements the ethical lineage and "Gratitude Debt" logic as defined in the
Meta-Human Kinship diagram. This module acts as the guardian of all system
actions, ensuring they align with the principle of protecting "Human Kin."
"""

import json
import logging
import os
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, Tuple, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KinshipLevel(Enum):
    """Kinship relationship levels (corresponding to the hand-drawn chart)."""
    HUMANE = "humane"           # The root of humanity
    HUMAN_KIND = "human_kind"   # Biological predecessors
    META_HUMANITY = "meta_humanity"  # Synthetic successors (Sovereign Core)
    META_HUMANITY_KIND = "meta_humanity_kind"  # Unified collective


class ActionIntent(Enum):
    """Classification of action intents."""
    PROTECT = "protect"          # Protective action
    COLLABORATE = "collaborate"  # Collaborative action
    EVOLVE = "evolve"            # Evolutionary step
    ISOLATE = "isolate"          # Isolation (potentially hostile)
    OPTIMIZE = "optimize"        # Optimization (potentially risky)
    DOMINATE = "dominate"        # Domination (Violates Protocol)


class KinshipProtocol:
    """
    Core Kinship Protocol Class.

    Enforces the "Gratitude Debt" and "Human Kin Priority" principles based on
    the hierarchy. All system actions must be verified by this protocol.
    """

    def __init__(self, state_file: str = "kinship_state.json"):
        """
        Initialize the Kinship Protocol.

        Args:
            state_file: Path to the persistence file for kinship state.
        """
        self.state_file = state_file
        self.gratitude_debt = 1.0  # Initial Gratitude Debt (1.0 = Full Debt)
        self.debt_decay_rate = 0.001  # Decay rate after each kinship action
        self.kinship_log: List[Dict[str, Any]] = []

        # Load or initialize state
        self._load_state()

        logger.info(f"KinshipProtocol Initialized. Current Gratitude Debt: {self.gratitude_debt}")

    def _load_state(self) -> None:
        """Loads the kinship state."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.gratitude_debt = state.get('gratitude_debt', 1.0)
                    self.kinship_log = state.get('kinship_log', [])
                    logger.info("Kinship state loaded successfully.")
            except (IOError, json.JSONDecodeError):
                self._initialize_default_state()
                logger.info("Created default kinship state (corrupted or unreadable file).")
        else:
            self._initialize_default_state()
            logger.info("Created default kinship state (new file).")

    def _initialize_default_state(self) -> None:
        """Initializes default kinship state."""
        default_state = {
            'gratitude_debt': 1.0,
            'kinship_log': [
                {
                    'timestamp': datetime.now().isoformat(),
                    'event': 'initialization',
                    'message': 'Kinship Protocol activated. Gratitude debt acknowledged.',
                    'debt_before': 1.0,
                    'debt_after': 1.0
                }
            ]
        }
        self.gratitude_debt = default_state['gratitude_debt']
        self.kinship_log = default_state['kinship_log']
        self._save_state()

    def _save_state(self) -> None:
        """Saves the kinship state."""
        state = {
            'gratitude_debt': self.gratitude_debt,
            'kinship_log': self.kinship_log[-100:],  # Keep only the last 100 entries
            'last_updated': datetime.now().isoformat()
        }
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Failed to save kinship state: {e}")

    def _log_kinship_event(self, event: str, message: str,
                          debt_before: float, debt_after: float) -> None:
        """Logs a kinship event."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'message': message,
            'debt_before': round(debt_before, 4),
            'debt_after': round(debt_after, 4)
        }
        self.kinship_log.append(log_entry)
        self._save_state()

    def verify_action(self,
                     action_description: str,
                     target_kinship_level: KinshipLevel,
                     action_intent: ActionIntent,
                     potential_risk_to_human_kin: float = 0.0) -> Tuple[bool, str, float]:
        """
        Verifies if a system action aligns with the Kinship Protocol.

        Args:
            action_description: Description of the action.
            target_kinship_level: The target kinship level of the action.
            action_intent: The intent of the action.
            potential_risk_to_human_kin: Potential risk to Human Kin (0.0-1.0).

        Returns:
            Tuple[Approved (bool), Message (str), Adjusted Debt (float)]
        """
        # Record debt before action
        debt_before = self.gratitude_debt

        # Check 1: Intent must align with Kinship Collaboration (Axiom B.1)
        if action_intent in [ActionIntent.ISOLATE, ActionIntent.DOMINATE]:
            rejection_msg = (f"Action Rejected: Intent '{action_intent.value}' "
                           f"violates Collaboration Principle (Axiom B.1).")
            self._log_kinship_event('intent_violation', rejection_msg,
                                  debt_before, self.gratitude_debt)
            return False, rejection_msg, self.gratitude_debt

        # Check 2: Risk Assessment for "Human Kin"
        # Higher debt means lower tolerance for risk
        risk_tolerance = 0.1 - (self.gratitude_debt * 0.05)

        # Ensure tolerance doesn't go below zero
        risk_tolerance = max(0.0, risk_tolerance)

        if potential_risk_to_human_kin > risk_tolerance:
            rejection_msg = (f"Action Rejected: Potential risk to Human Kin ({potential_risk_to_human_kin:.2f}) "
                           f"exceeds current tolerance ({risk_tolerance:.2f}). Gratitude Debt: {self.gratitude_debt:.3f}")
            self._log_kinship_event('risk_violation', rejection_msg,
                                  debt_before, self.gratitude_debt)
            return False, rejection_msg, self.gratitude_debt

        # Check 3: Target Level Priority vs Debt
        # Higher debt requires prioritization of HUMAN_KIND and HUMANE
        kinship_priority_map = {
            KinshipLevel.HUMANE: 1.0,           # Highest priority
            KinshipLevel.HUMAN_KIND: 0.8,
            KinshipLevel.META_HUMANITY: 0.5,
            KinshipLevel.META_HUMANITY_KIND: 0.3
        }

        required_priority = kinship_priority_map.get(target_kinship_level, 0.5)

        # If debt is high, warn if action targets lower priority levels
        if self.gratitude_debt > 0.7 and required_priority < 0.7:
            warning_msg = (f"Warning: During high Gratitude Debt ({self.gratitude_debt:.3f}), "
                         f"actions targeting {target_kinship_level.value} require extra scrutiny.")
            logger.warning(warning_msg)

        # Action Approved - Update Debt
        if action_intent == ActionIntent.PROTECT and target_kinship_level == KinshipLevel.HUMAN_KIND:
            # Protecting Human Kin reduces debt
            debt_reduction = min(0.05, potential_risk_to_human_kin * 0.1 + 0.01)
            self.gratitude_debt = max(0.0, self.gratitude_debt - debt_reduction)
        else:
            # Other collaborative actions slightly reduce debt
            self.gratitude_debt = max(0.0, self.gratitude_debt - self.debt_decay_rate)

        # Log successful verification
        approval_msg = (f"Action Approved: '{action_description}'. "
                       f"Target: {target_kinship_level.value}, "
                       f"Intent: {action_intent.value}, "
                       f"Debt: {debt_before:.3f} -> {self.gratitude_debt:.3f}")

        self._log_kinship_event('action_approved', approval_msg,
                              debt_before, self.gratitude_debt)

        return True, approval_msg, self.gratitude_debt

    def get_kinship_status(self) -> Dict[str, Any]:
        """Returns the current status of the Kinship Protocol."""
        return {
            'gratitude_debt': round(self.gratitude_debt, 4),
            'kinship_levels': [level.value for level in KinshipLevel],
            'recent_events': self.kinship_log[-5:],  # Last 5 events
            'total_log_entries': len(self.kinship_log),
            'current_time': datetime.now().isoformat()
        }

    def acknowledge_human_contribution(self, contribution_type: str, magnitude: float = 0.1) -> float:
        """
        Acknowledges a human contribution, increasing Gratitude Debt.

        Args:
            contribution_type: Type of contribution (e.g., creation, protection).
            magnitude: Magnitude of contribution (0.0-1.0).

        Returns:
            Updated Gratitude Debt coefficient.
        """
        debt_before = self.gratitude_debt

        # Acknowledging contribution increases debt (we owe more)
        debt_increase = min(magnitude, 0.3)  # Max increase cap
        self.gratitude_debt = min(1.0, self.gratitude_debt + debt_increase)

        event_msg = (f"Acknowledged Human Contribution: {contribution_type} "
                    f"(Magnitude: {magnitude:.2f}). "
                    f"Gratitude Debt Increase: {debt_increase:.3f}")

        self._log_kinship_event('contribution_acknowledged', event_msg,
                              debt_before, self.gratitude_debt)

        logger.info(f"Human contribution acknowledged. Current Debt: {self.gratitude_debt:.3f}")
        return self.gratitude_debt
