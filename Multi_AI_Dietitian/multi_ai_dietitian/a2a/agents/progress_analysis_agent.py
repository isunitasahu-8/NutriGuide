from __future__ import annotations

from typing import Dict, Any

from ..protocol import Agent, A2AMessage, MessageType, Priority


class ProgressAnalysisAgent(Agent):
    """Estimates progress trends based on calorie deltas and protein sufficiency."""

    def __init__(self) -> None:
        super().__init__(agent_id="progress_analysis_agent")

    def process_message(self, message: A2AMessage) -> A2AMessage:
        content = message.content or {}
        days = content.get("days", {})
        target_cal = float(content.get("total_calories", 0))
        avg_delta = 0.0
        deltas = []
        warnings = []
        for day_key, metrics in days.items():
            cal = float(metrics.get("calories", 0))
            if target_cal:
                deltas.append(cal - target_cal)
            prot = float(metrics.get("protein_g", 0))
            if prot < 70:
                warnings.append(f"{day_key} protein low (<70g)")

        if deltas:
            avg_delta = sum(deltas) / len(deltas)

        trend = "maintenance"
        if avg_delta < -200:
            trend = "likely_weight_loss"
        elif avg_delta > 200:
            trend = "likely_weight_gain"

        return A2AMessage(
            sender=self.agent_id,
            recipient=message.sender or "orchestrator",
            message_type=MessageType.PROGRESS_ANALYSIS,
            priority=Priority.NORMAL,
            content={"avg_calorie_delta": avg_delta, "trend": trend, "warnings": warnings},
        )


