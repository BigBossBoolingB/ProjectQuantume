"""
Context Funnel Module

Implements the input processing logic to filter and structure raw inputs
before they reach the Mission Control center. This module performs "Chunking"
and "Intent Extraction" as per the system blueprint.
"""

from typing import Dict, Any, List

class ContextFunnel:
    """
    Filters and structures raw input data.
    """
    def __init__(self):
        self.context_buffer = []

    def process_input(self, raw_input: str) -> Dict[str, Any]:
        """
        Processes raw text input through the funnel.

        Steps:
        1. Chunking (Simplistic splitting for now)
        2. Intent Extraction (Keyword based)
        3. Structure Output
        """
        chunks = self._chunk_input(raw_input)
        intent = self._extract_intent(raw_input)

        structured_data = {
            "original_input": raw_input,
            "chunks": chunks,
            "primary_intent": intent,
            "processed": True
        }

        self.context_buffer.append(structured_data)
        return structured_data

    def _chunk_input(self, text: str) -> List[str]:
        """Splits input into manageable chunks."""
        # Simple punctuation-based splitting
        return [chunk.strip() for chunk in text.replace('.', ',').split(',') if chunk.strip()]

    def _extract_intent(self, text: str) -> str:
        """Determines the primary intent of the input."""
        text_lower = text.lower()

        if "update" in text_lower or "change" in text_lower or "set" in text_lower:
            return "modify_state"
        elif "status" in text_lower or "check" in text_lower or "report" in text_lower:
            return "query_status"
        elif "encrypt" in text_lower or "secure" in text_lower:
            return "security_action"
        else:
            return "general_info"
