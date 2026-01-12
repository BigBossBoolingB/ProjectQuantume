"""
Mission Control (Upgraded Brain)
Enhanced with Kinship Protocol and Context Funnel integration.
"""
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from src.cypher import Cypher
from src.kinship import KinshipProtocol, ActionIntent, KinshipLevel
from src.context_funnel import ContextFunnel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MissionControl:
    """Enhanced MissionControl with ethical and cognitive layers."""

    def __init__(self, state_file: str = "system_state.json"):
        self.state_file = state_file
        self.cypher = Cypher()

        # Initialize core modules
        self.kinship = KinshipProtocol()
        self.context_funnel = ContextFunnel(self.kinship)

        # Load initial state
        self.state = self.load_state()

        logger.info("Enhanced MissionControl initialized")
        logger.info(f"Kinship debt: {self.kinship.gratitude_debt}")
        logger.info(f"System status: {self.state.get('system_status', 'BOOTING')}")

    def load_state(self) -> Dict[str, Any]:
        """Load and decrypt system state."""
        try:
            encrypted_state = self.cypher.load_state(self.state_file)
            return encrypted_state
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            return self._get_default_state()

    def save_state(self) -> bool:
        """Encrypt and save system state."""
        try:
            self.state['last_updated'] = datetime.now().isoformat()
            self.cypher.save_state(self.state, self.state_file)
            logger.debug("State saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
            return False

    def _get_default_state(self) -> Dict[str, Any]:
        """Return default system state."""
        return {
            "system_status": "BOOTING",
            "operational_phase": "INITIALIZATION",
            "faraday_integrity": "PENDING",
            "quantum_core": "OFFLINE",
            "last_heartbeat": None,
            "creation_timestamp": datetime.now().isoformat()
        }

    def process_command(self, raw_command: str) -> Dict[str, Any]:
        """
        Process any command through the complete pipeline:
        1. Context Funnel (understanding)
        2. Kinship Protocol (ethical approval)
        3. Execution (if approved)
        """
        logger.info(f"Processing command: {raw_command[:50]}...")

        # Stage 1: Context Funnel processing
        context_result = self.context_funnel.process(raw_command)

        # Stage 2: Check if kinship already approved during context processing
        if not context_result['kinship_approved']:
            return {
                'status': 'REJECTED',
                'reason': 'Failed kinship protocol',
                'details': context_result['kinship_message'],
                'context_analysis': context_result
            }

        # Stage 3: Deterministic verification
        if not context_result['verified']:
            return {
                'status': 'PENDING',
                'reason': 'Requires manual verification',
                'details': 'Context confidence below threshold',
                'context_analysis': context_result
            }

        # Stage 4: Execute based on intent
        execution_result = self._execute_by_intent(
            context_result['primary_intent'],
            context_result['entities'],
            context_result['recommended_action']
        )

        # Update state
        self.state['last_command'] = {
            'timestamp': datetime.now().isoformat(),
            'raw': raw_command[:100],
            'intent': context_result['primary_intent'],
            'execution_result': execution_result['status']
        }
        self.save_state()

        return {
            'status': 'EXECUTED',
            'context_analysis': context_result,
            'execution_result': execution_result,
            'kinship_debt': self.kinship.gratitude_debt
        }

    def _execute_by_intent(self, intent: str, entities: Dict, recommendation: str) -> Dict[str, Any]:
        """Execute action based on distilled intent."""

        if intent == 'report':
            # Handle status reports
            if 'grounding_resistance' in entities:
                r_value = entities['grounding_resistance']
                self.state['faraday_integrity'] = 'OPTIMAL' if r_value < 1.0 else 'MARGINAL' if r_value < 1.5 else 'CRITICAL'
                self.state['last_grounding_check'] = datetime.now().isoformat()
                self.save_state()

                return {
                    'status': 'REPORT_ACCEPTED',
                    'action': 'Updated system state with grounding data',
                    'grounding_status': self.state['faraday_integrity'],
                    'next_recommendation': 'Proceed with operational phase' if r_value < 1.0 else 'Schedule maintenance'
                }

            return {
                'status': 'REPORT_ACCEPTED',
                'action': 'Logged status update',
                'next_recommendation': recommendation
            }

        elif intent == 'alert':
            # Handle alerts
            alert_level = 'CRITICAL' if 'breach' in str(entities).lower() else 'WARNING'
            self.state['system_status'] = 'ALERT'
            self.state['last_alert'] = {
                'level': alert_level,
                'timestamp': datetime.now().isoformat(),
                'entities': list(entities.keys())
            }
            self.save_state()

            return {
                'status': 'ALERT_ACTIVATED',
                'action': f'System placed in {alert_level} alert status',
                'recommendation': recommendation
            }

        elif intent == 'command':
            # Handle execution commands
            command_response = {
                'status': 'COMMAND_RECEIVED',
                'action': 'Command queued for execution',
                'preflight_check': 'Pending',
                'recommendation': recommendation
            }

            # Check for specific command patterns
            if 'thermal' in entities:
                command_response['action'] = 'Thermal deception protocol initialized'
                command_response['preflight_check'] = 'Faraday integrity verified' if self.state.get('faraday_integrity') == 'OPTIMAL' else 'WARNING: Faraday status suboptimal'

            return command_response

        else:
            # Default for requests
            return {
                'status': 'PROCESSING',
                'action': 'Request forwarded to analysis layer',
                'recommendation': recommendation
            }

    def get_system_status(self) -> Dict[str, Any]:
        """Return comprehensive system status."""
        return {
            'mission_control': {
                'state': self.state,
                'last_updated': self.state.get('last_updated'),
                'operational_phase': self.state.get('operational_phase', 'UNKNOWN')
            },
            'kinship': self.kinship.get_status(),
            'context_funnel': {
                'recent_processing': self.context_funnel.get_recent_processing(3)
            }
        }
