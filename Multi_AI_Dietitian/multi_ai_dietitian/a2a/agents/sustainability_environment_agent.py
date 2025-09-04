"""
Sustainability & Environment Agent - The Eco-Friendly Guide

Suggests sustainable food options and considers environmental impact.
"""

from typing import Dict, List, Any
from datetime import datetime

from ..protocol import Agent, A2AMessage, MessageType


class SustainabilityEnvironmentAgent(Agent):
    """The Eco-Friendly Guide - Suggests sustainable options"""
    
    def __init__(self):
        super().__init__("sustainability_agent")
        self.sustainability_database = {
            "high_carbon": ["beef", "lamb", "cheese"],
            "medium_carbon": ["chicken", "pork", "eggs"],
            "low_carbon": ["tofu", "lentils", "vegetables", "fruits"],
            "seasonal_months": {
                "berries": [6, 7, 8],  # Summer
                "pumpkin": [9, 10, 11],  # Fall
                "citrus": [12, 1, 2]  # Winter
            }
        }
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.SUSTAINABILITY_CHECK:
            return self._check_sustainability(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "sustainability_agent"}
        )
    
    def _check_sustainability(self, message: A2AMessage) -> A2AMessage:
        """Check sustainability of food choices"""
        foods = message.content.get("foods", [])
        current_month = datetime.now().month
        
        sustainability_score = 0
        suggestions = []
        
        for food in foods:
            food_lower = food.lower()
            
            if any(high_carbon in food_lower for high_carbon in self.sustainability_database["high_carbon"]):
                sustainability_score -= 3
                suggestions.append(f"Consider replacing {food} with plant-based alternative")
            elif any(medium_carbon in food_lower for medium_carbon in self.sustainability_database["medium_carbon"]):
                sustainability_score -= 1
            elif any(low_carbon in food_lower for low_carbon in self.sustainability_database["low_carbon"]):
                sustainability_score += 2
            
            # Check seasonality
            for seasonal_food, months in self.sustainability_database["seasonal_months"].items():
                if seasonal_food in food_lower and current_month not in months:
                    suggestions.append(f"{food} is not in season - consider local alternatives")
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "sustainability_score": sustainability_score,
                "suggestions": suggestions,
                "message": f"Sustainability score: {sustainability_score}/10"
            }
        )
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about sustainability"""
        return {
            "carbon_categories": list(self.sustainability_database.keys())[:3],
            "high_carbon_foods": len(self.sustainability_database["high_carbon"]),
            "low_carbon_foods": len(self.sustainability_database["low_carbon"]),
            "seasonal_foods": len(self.sustainability_database["seasonal_months"])
        }
