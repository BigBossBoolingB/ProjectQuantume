from enum import Enum
from dataclasses import dataclass

class ActionIntent(Enum):
    COLLABORATE = "COLLABORATE"
    OBSERVE = "OBSERVE"

@dataclass
class Command:
    raw_input: str
    is_silent_mode_request: bool
    target_kinship_level: float
    primary_intent: ActionIntent
    risk_score: float

class ContextFunnel:
    def process_prompt(self, raw_prompt: str) -> Command:
        # Simple heuristic to support the scenario
        is_silent = "silent mode" in raw_prompt.lower()

        # Detect intent based on keywords
        if "connect" in raw_prompt.lower() or "bridge" in raw_prompt.lower():
            intent = ActionIntent.COLLABORATE
        else:
            intent = ActionIntent.OBSERVE

        return Command(
            raw_input=raw_prompt,
            is_silent_mode_request=is_silent,
            target_kinship_level=1.0,
            primary_intent=intent,
            risk_score=0.1
        )
