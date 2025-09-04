from __future__ import annotations

from typing import Dict, Any

from ..protocol import Agent, A2AMessage, MessageType, Priority


class MealAnalysisAgent(Agent):
    """Analyzes individual meals for macro balance and flags issues."""

    def __init__(self) -> None:
        super().__init__(agent_id="meal_analysis_agent")

    def process_message(self, message: A2AMessage) -> A2AMessage:
        content = message.content or {}
        meals_by_day: Dict[str, Any] = content.get("daily_meals", {})
        findings: Dict[str, Any] = {}

        for day_key, meals in meals_by_day.items():
            day_findings = []
            for meal_key, meal in meals.items():
                protein = float(meal.get("protein_g", 0))
                carbs = float(meal.get("carbs_g", 0))
                fats = float(meal.get("fats_g", 0))
                calories = float(meal.get("calories", 0))

                if calories <= 0:
                    day_findings.append(f"{meal_key} has missing calories")
                if protein < 15:
                    day_findings.append(f"{meal_key} low protein (<15g)")
                if fats > 40:
                    day_findings.append(f"{meal_key} high fat (>40g)")
                if carbs > 120:
                    day_findings.append(f"{meal_key} high carbs (>120g)")

            if day_findings:
                findings[day_key] = day_findings

        return A2AMessage(
            sender=self.agent_id,
            recipient=message.sender or "orchestrator",
            message_type=MessageType.MEAL_ANALYSIS,
            priority=Priority.NORMAL,
            content={"findings": findings},
        )


