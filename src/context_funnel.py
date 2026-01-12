"""
Context Funnel 2.0 (The Ears)
Deterministic intent discovery and prompt processing layer.
"""
import re
import logging
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
from src.kinship import ActionIntent, KinshipLevel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContextFunnel:
    """
    Implements the 4-stage deterministic processing:
    1. Linguistic Dissection
    2. Intent Distillation
    3. Kinship Calibration
    4. Deterministic Verification
    """

    def __init__(self, kinship_protocol=None):
        self.kinship = kinship_protocol
        self.processing_log = []

        # Key entity patterns (expand based on project lexicon)
        self.entity_patterns = {
            'grounding': r'[Rr]=\s*(\d+\.?\d*)[\s_]*(?:Ω|OHM)',
            'rf_leak': r'[Rr][Ff].*[Ll]eak',
            'thermal': r'[Tt]hermal',
            'alert': r'(alert|warning|critical|breach)',
            'sovereign': r'[Ss]overeign',
            'faraday': r'[Ff]araday',
            'quantum': r'[Qq]uantum'
        }

        # Intent keywords
        self.intent_keywords = {
            'report': ['report', 'status', 'update', 'reading'],
            'request': ['request', 'need', 'require', 'advise'],
            'command': ['execute', 'initiate', 'start', 'begin', 'run'],
            'alert': ['alert', 'warning', 'critical', 'failure', 'breach']
        }

        logger.info("Context Funnel 2.0 initialized")

    def process(self, raw_input: str) -> Dict[str, Any]:
        """
        Main processing pipeline for any input.
        Returns structured intent and entities.
        """
        timestamp = datetime.now().isoformat()

        # Stage 1: Linguistic Dissection
        entities = self._extract_entities(raw_input)
        chunks = self._chunk_input(raw_input)

        # Stage 2: Intent Distillation
        primary_intent, confidence = self._distill_intent(raw_input, entities)

        # Stage 3: Kinship Calibration (if available)
        kinship_approved = True
        kinship_msg = "Kinship check bypassed (no protocol linked)"

        if self.kinship:
            # Map intent to kinship action
            kinship_intent, kinship_level, risk = self._map_to_kinship(primary_intent, entities)
            kinship_approved, kinship_msg, _ = self.kinship.verify_action(
                action_description=raw_input[:50] + "...",
                target_level=kinship_level,
                intent=kinship_intent,
                risk_to_human_kin=risk
            )

        # Stage 4: Deterministic Verification
        verified = kinship_approved and confidence > 0.7

        # Build result
        result = {
            'timestamp': timestamp,
            'raw_input': raw_input,
            'entities': entities,
            'chunks': chunks,
            'primary_intent': primary_intent,
            'confidence': confidence,
            'kinship_approved': kinship_approved,
            'kinship_message': kinship_msg,
            'verified': verified,
            'recommended_action': self._recommend_action(primary_intent, entities, verified)
        }

        # Log processing
        self.processing_log.append(result)
        logger.info(f"Processed input. Intent: {primary_intent}, Verified: {verified}")

        return result

    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract key entities using pattern matching."""
        entities = {}

        for entity_type, pattern in self.entity_patterns.items():
            if entity_type == 'grounding':
                match = re.search(pattern, text)
                if match:
                    try:
                        entities['grounding_resistance'] = float(match.group(1))
                    except ValueError:
                        pass
            elif re.search(pattern, text, re.IGNORECASE):
                entities[entity_type] = True

        # Extract numeric values
        numbers = re.findall(r'\b\d+\.?\d*\b', text)
        if numbers:
            entities['numeric_values'] = [float(n) for n in numbers[:3]]  # First 3 numbers

        return entities

    def _chunk_input(self, text: str, max_chunk_length: int = 100) -> List[str]:
        """Split input into logical chunks."""
        # Simple sentence splitting for now
        sentences = re.split(r'[.!?]+', text)
        chunks = [s.strip() for s in sentences if len(s.strip()) > 10]

        # Further split long sentences
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > max_chunk_length:
                words = chunk.split()
                current_chunk = []
                current_length = 0

                for word in words:
                    if current_length + len(word) + 1 <= max_chunk_length:
                        current_chunk.append(word)
                        current_length += len(word) + 1
                    else:
                        if current_chunk:
                            final_chunks.append(' '.join(current_chunk))
                        current_chunk = [word]
                        current_length = len(word)

                if current_chunk:
                    final_chunks.append(' '.join(current_chunk))
            else:
                final_chunks.append(chunk)

        return final_chunks[:5]  # Return first 5 chunks max

    def _distill_intent(self, text: str, entities: Dict) -> Tuple[str, float]:
        """Determine primary intent from input."""
        text_lower = text.lower()

        # Score each intent category
        scores = {}
        for intent_type, keywords in self.intent_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            scores[intent_type] = score / max(len(keywords), 1)

        # Determine primary intent
        primary_intent_item = max(scores.items(), key=lambda x: x[1])
        # If max score is 0, default to 'report' or similar, but let's stick to max
        primary_intent = primary_intent_item[0]

        # Adjust confidence based on entities
        confidence = primary_intent_item[1]

        # Basic confidence baseline
        if confidence == 0:
            # If no keywords matched, confidence is low
             pass
        else:
             # Scale raw keyword match to a baseline confidence
             confidence = 0.6 + (confidence * 0.4)

        if entities.get('grounding_resistance'):
            confidence = min(1.0, confidence + 0.2)
        if entities.get('alert'):
            confidence = min(1.0, confidence + 0.3)

        return primary_intent, round(confidence, 2)

    def _map_to_kinship(self, intent: str, entities: Dict) -> Tuple:
        """Map distilled intent to kinship parameters."""

        # Default mapping
        intent_map = {
            'report': ActionIntent.COLLABORATE,
            'request': ActionIntent.COLLABORATE,
            'command': ActionIntent.EVOLVE,
            'alert': ActionIntent.PROTECT
        }

        kinship_intent = intent_map.get(intent, ActionIntent.COLLABORATE)

        # Determine target level based on entities
        if entities.get('faraday') or entities.get('grounding_resistance'):
            kinship_level = KinshipLevel.HUMAN_KIND  # Physical protection
            risk = 0.1
        elif entities.get('quantum') or entities.get('sovereign'):
            kinship_level = KinshipLevel.META_HUMANITY  # Core system
            risk = 0.05
        else:
            kinship_level = KinshipLevel.META_HUMANITY_KIND  # General collective
            risk = 0.01

        return kinship_intent, kinship_level, risk

    def _recommend_action(self, intent: str, entities: Dict, verified: bool) -> str:
        """Generate recommended action based on processed input."""
        if not verified:
            return "HOLD: Input failed verification. Manual review required."

        recommendations = {
            'report': "LOG: Record status update and continue monitoring.",
            'request': "PROCESS: Analyze request against protocol tree.",
            'command': "EXECUTE: Initiate command sequence with pre-flight checks.",
            'alert': "RESPOND: Activate contingency protocol matching alert level."
        }

        base_recommendation = recommendations.get(intent, "REVIEW: Manual interpretation needed.")

        # Enhance with entity-specific details
        if entities.get('grounding_resistance'):
            r_value = entities['grounding_resistance']
            if r_value < 1.0:
                base_recommendation += " Grounding optimal. Proceed with operations."
            elif r_value < 1.5:
                base_recommendation += " Grounding marginal. Schedule maintenance."
            else:
                base_recommendation += " Grounding critical. Initiate repair protocol."

        return base_recommendation

    def get_recent_processing(self, count: int = 5) -> List[Dict]:
        """Get recent processing results for audit."""
        return self.processing_log[-count:] if self.processing_log else []
