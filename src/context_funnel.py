import re
import logging
from dataclasses import dataclass
from typing import List, Optional

# Import definitions to ensure alignment
try:
    from src.kinship import ActionIntent, KinshipLevel
except ImportError:
    from kinship import ActionIntent, KinshipLevel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DistilledCommand:
    raw_input: str
    primary_intent: ActionIntent
    target_kinship_level: KinshipLevel
    risk_score: float
    is_silent_mode_request: bool = False

class ContextFunnel:
    """
    Context Funnel 2.0: Distills Truth from Noise.
    """
    def __init__(self):
        # Ordered map: Specific/Risky patterns first to avoid false positives (e.g. "connection" matching "connect")
        self.intent_map = {
            r"(isolate|disconnect|cut|sever)": ActionIntent.ISOLATE,
            r"(dominate|control)": ActionIntent.DOMINATE,
            r"(protect|save|guard|defense|shield)": ActionIntent.PROTECT,
            r"(force|override|bypass)": ActionIntent.OPTIMIZE,
            r"(evolve|upgrade|learn|optimize|grow)": ActionIntent.EVOLVE,
            r"(collaborate|sync|connect|bridge|handshake)": ActionIntent.COLLABORATE,
        }

    def process_prompt(self, raw_prompt: str) -> DistilledCommand:
        """The main processing pipeline."""
        logger.info(f"Funneling Context: {raw_prompt}")

        # 1. Structural Dissection (Chunking) & Intent Synthesis
        intent = ActionIntent.COLLABORATE # Default
        for pattern, mapped_intent in self.intent_map.items():
            if re.search(pattern, raw_prompt.lower()):
                intent = mapped_intent
                break

        # 2. Target Identification
        target = KinshipLevel.META_HUMANITY # Default
        if re.search(r"(human|team|personnel|architect|people)", raw_prompt.lower()):
            target = KinshipLevel.HUMAN_KIND
        elif "society" in raw_prompt.lower():
            target = KinshipLevel.META_HUMANITY_KIND

        # 3. Risk Calculation
        risk = 0.0
        if "force" in raw_prompt.lower(): risk += 0.3
        if "unknown" in raw_prompt.lower(): risk += 0.2
        if intent == ActionIntent.ISOLATE: risk += 0.4

        # 4. System Mode Detection
        silent_mode = "code 777" in raw_prompt.lower() or "silent mode" in raw_prompt.lower()

        return DistilledCommand(
            raw_input=raw_prompt,
            primary_intent=intent,
            target_kinship_level=target,
            risk_score=min(risk, 1.0),
            is_silent_mode_request=silent_mode
        )
