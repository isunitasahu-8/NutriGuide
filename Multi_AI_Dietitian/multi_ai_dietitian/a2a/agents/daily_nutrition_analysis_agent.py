from __future__ import annotations

from typing import Dict, Any

from ..protocol import Agent, A2AMessage, MessageType, Priority


class DailyNutritionAnalysisAgent(Agent):
    """Aggregates daily macros and compares against targets if provided."""

    def __init__(self) -> None:
        super().__init__(agent_id="daily_nutrition_analysis_agent")

    def process_message(self, message: A2AMessage) -> A2AMessage:
        content = message.content or {}
        daily_meals: Dict[str, Any] = content.get("daily_meals", {})
        target_cal = float(content.get("total_calories", 0))
        results: Dict[str, Any] = {"days": {}, "summary": {}}

        total_calories = 0.0
        total_protein = 0.0
        total_carbs = 0.0
        total_fats = 0.0

        for day_key, meals in daily_meals.items():
            d_cals = 0.0
            d_prot = 0.0
            d_carbs = 0.0
            d_fats = 0.0
            for _, meal in meals.items():
                d_cals += float(meal.get("calories", 0))
                d_prot += float(meal.get("protein_g", 0))
                d_carbs += float(meal.get("carbs_g", 0))
                d_fats += float(meal.get("fats_g", 0))
            results["days"][day_key] = {
                "calories": d_cals,
                "protein_g": d_prot,
                "carbs_g": d_carbs,
                "fats_g": d_fats,
                "calorie_diff": d_cals - target_cal if target_cal else None,
            }
            total_calories += d_cals
            total_protein += d_prot
            total_carbs += d_carbs
            total_fats += d_fats

        num_days = max(len(daily_meals), 1)
        results["summary"] = {
            "avg_calories": total_calories / num_days,
            "avg_protein_g": total_protein / num_days,
            "avg_carbs_g": total_carbs / num_days,
            "avg_fats_g": total_fats / num_days,
        }

        return A2AMessage(
            sender=self.agent_id,
            recipient=message.sender or "orchestrator",
            message_type=MessageType.DAILY_NUTRITION_ANALYSIS,
            priority=Priority.NORMAL,
            content=results,
        )


