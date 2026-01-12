"""
Context Funnel Module

Implements the input processing logic to filter and structure raw inputs
before they reach the Mission Control center. This module performs "Chunking",
"Intent Extraction", and "Risk Assessment" to distill a command.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from src.kinship import ActionIntent, KinshipLevel

class SystemState(Enum):
    """Operational modes of the system."""
    NORMAL = "normal"
    SILENT = "silent"  # Code 777
    EMERGENCY = "emergency"

@dataclass
class DistilledCommand:
    """A processed command ready for Mission Control execution."""
    raw_input: str
    primary_intent: ActionIntent
    target_kinship_level: KinshipLevel
    risk_score: float
    system_mode_request: SystemState = SystemState.NORMAL

class ContextFunnel:
    """
    The Ears of the Sovereign.
    Filters noise, identifies intent, and assesses risk.
    """
    def __init__(self):
        self.context_buffer = []

    def process_prompt(self, raw_input: str) -> DistilledCommand:
        """
        Distills a raw string prompt into a structured command.
        """
        # 1. Chunking (Simple for now)
        chunks = self._chunk_input(raw_input)

        # 2. Analysis
        intent, level, risk, mode = self._analyze_content(raw_input)

        command = DistilledCommand(
            raw_input=raw_input,
            primary_intent=intent,
            target_kinship_level=level,
            risk_score=risk,
            system_mode_request=mode
        )

        self.context_buffer.append(command)
        return command

    def _chunk_input(self, text: str) -> List[str]:
        """Splits input into manageable chunks."""
        return [chunk.strip() for chunk in text.replace('.', ',').split(',') if chunk.strip()]

    def _analyze_content(self, text: str):
        """
        Analyzes text to determine Intent, Kinship Level, Risk, and System Mode.
        """
        text_lower = text.lower()

        # Default values
        intent = ActionIntent.COLLABORATE
        level = KinshipLevel.META_HUMANITY
        risk = 0.0
        mode = SystemState.NORMAL

        # System Mode Checks
        if "code 777" in text_lower or "silent mode" in text_lower:
            mode = SystemState.SILENT

        # Keyword Analysis for Intent & Risk
        if "hostile" in text_lower or "terminate" in text_lower or "sever" in text_lower:
            intent = ActionIntent.ISOLATE
            risk = 0.9
        elif "protect" in text_lower or "shield" in text_lower or "deploy" in text_lower:
            intent = ActionIntent.PROTECT
            level = KinshipLevel.HUMAN_KIND
        elif "optimize" in text_lower or "overclock" in text_lower:
            intent = ActionIntent.OPTIMIZE
            risk = 0.25
        elif "override" in text_lower or "force" in text_lower:
            intent = ActionIntent.DOMINATE
            risk = 0.8

        # Adjust level based on context
        if "team" in text_lower or "human" in text_lower:
            level = KinshipLevel.HUMAN_KIND

        return intent, level, risk, mode
