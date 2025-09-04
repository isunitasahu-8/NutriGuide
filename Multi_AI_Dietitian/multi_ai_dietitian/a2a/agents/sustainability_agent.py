from __future__ import annotations

from typing import Dict, Any

from ..protocol import Agent, A2AMessage, MessageType, Priority


FOOTPRINT = {
    "beef": 27.0,
    "lamb": 39.0,
    "pork": 12.0,
    "chicken": 6.9,
    "fish": 5.4,
    "rice": 2.7,
    "beans": 0.8,
    "lentils": 0.9,
    "oats": 1.0,
    "vegetable": 0.5,
}


def estimate_co2e(name: str, amount: str) -> float:
    lower = name.lower()
    grams = 0.0
    try:
        if "g" in amount:
            grams = float(amount.replace("g", "").strip())
        elif "kg" in amount:
            grams = float(amount.replace("kg", "").strip()) * 1000
        else:
            grams = 100.0
    except Exception:
        grams = 100.0

    for k, kg_co2e in FOOTPRINT.items():
        if k in lower:
            return (grams / 1000.0) * kg_co2e
    return (grams / 1000.0) * 1.2


class SustainabilityAgent(Agent):
    """Estimates rough environmental footprint of the plan."""

    def __init__(self) -> None:
        super().__init__(agent_id="sustainability_analysis_agent")

    def process_message(self, message: A2AMessage) -> A2AMessage:
        content = message.content or {}
        daily_meals: Dict[str, Any] = content.get("daily_meals", {})
        co2e_per_day: Dict[str, float] = {}

        for day_key, meals in daily_meals.items():
            total = 0.0
            for _, meal in meals.items():
                for ing in meal.get("ingredients", []):
                    total += estimate_co2e(ing.get("name", ""), ing.get("amount", ""))
            co2e_per_day[day_key] = total

        avg = sum(co2e_per_day.values()) / max(len(co2e_per_day), 1)

        return A2AMessage(
            sender=self.agent_id,
            recipient=message.sender or "orchestrator",
            message_type=MessageType.SUSTAINABILITY_CHECK,
            priority=Priority.NORMAL,
            content={"daily_kg_co2e": co2e_per_day, "average_kg_co2e_per_day": avg},
        )


