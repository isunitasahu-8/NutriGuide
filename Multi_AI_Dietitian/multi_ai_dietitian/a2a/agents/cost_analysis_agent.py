from __future__ import annotations

from typing import Dict, Any

from ..protocol import Agent, A2AMessage, MessageType, Priority


PRICE_TABLE = {
    "chicken": 0.012,  # per gram USD
    "salmon": 0.02,
    "beef": 0.018,
    "oats": 0.002,
    "apple": 0.003,
    "banana": 0.0025,
    "broccoli": 0.004,
    "rice": 0.0015,
    "yogurt": 0.005,
    "almonds": 0.01,
}


def estimate_item_cost(name: str, amount: str) -> float:
    lower = name.lower()
    grams = 0.0
    try:
        if "g" in amount:
            grams = float(amount.replace("g", "").strip())
        elif "kg" in amount:
            grams = float(amount.replace("kg", "").strip()) * 1000
        elif "cup" in amount:
            grams = 100.0
        else:
            grams = 50.0
    except Exception:
        grams = 50.0

    for key, price_per_g in PRICE_TABLE.items():
        if key in lower:
            return grams * price_per_g
    return grams * 0.003


class CostAnalysisAgent(Agent):
    """Rudimentary cost estimation for meals and averages."""

    def __init__(self) -> None:
        super().__init__(agent_id="cost_analysis_agent")

    def process_message(self, message: A2AMessage) -> A2AMessage:
        content = message.content or {}
        daily_meals: Dict[str, Any] = content.get("daily_meals", {})
        days_cost: Dict[str, float] = {}

        for day_key, meals in daily_meals.items():
            total_cost = 0.0
            for _, meal in meals.items():
                for ing in meal.get("ingredients", []):
                    total_cost += estimate_item_cost(ing.get("name", ""), ing.get("amount", ""))
            days_cost[day_key] = total_cost

        avg_cost = sum(days_cost.values()) / max(len(days_cost), 1)

        return A2AMessage(
            sender=self.agent_id,
            recipient=message.sender or "orchestrator",
            message_type=MessageType.COST_ANALYSIS,
            priority=Priority.NORMAL,
            content={"daily_costs": days_cost, "average_cost_per_day": avg_cost},
        )


