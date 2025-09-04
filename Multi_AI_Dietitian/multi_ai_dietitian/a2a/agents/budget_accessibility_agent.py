"""
Budget & Accessibility Agent - The Practical Shopper

Considers budget constraints and food availability in meal planning.
"""

from typing import Dict, Any

from ..protocol import Agent, A2AMessage, MessageType


class BudgetAccessibilityAgent(Agent):
    """The Practical Shopper - Considers budget and availability"""
    
    def __init__(self):
        super().__init__("budget_accessibility_agent")
        self.price_database = {
            "expensive": ["quinoa", "salmon", "almonds", "avocado"],
            "affordable": ["brown rice", "chicken", "lentils", "banana"],
            "budget": ["oats", "eggs", "carrots", "apple"]
        }
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.BUDGET_CHECK:
            return self._check_budget(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "budget_accessibility_agent"}
        )
    
    def _check_budget(self, message: A2AMessage) -> A2AMessage:
        """Check budget compatibility and suggest substitutions"""
        budget_level = message.content.get("budget_level", "medium")
        foods = message.content.get("foods", [])
        
        substitutions = {}
        total_cost = 0
        
        for food in foods:
            food_lower = food.lower()
            
            if budget_level == "low":
                if any(expensive in food_lower for expensive in self.price_database["expensive"]):
                    if "quinoa" in food_lower:
                        substitutions[food] = "brown rice"
                    elif "salmon" in food_lower:
                        substitutions[food] = "chicken"
                    elif "almonds" in food_lower:
                        substitutions[food] = "peanuts"
            
            # Estimate cost (simplified)
            if food_lower in self.price_database["expensive"]:
                total_cost += 15
            elif food_lower in self.price_database["affordable"]:
                total_cost += 8
            else:
                total_cost += 3
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "budget_friendly": total_cost <= 20,
                "substitutions": substitutions,
                "estimated_cost": total_cost,
                "message": f"Budget check complete: ${total_cost} estimated cost"
            }
        )
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about budget considerations"""
        return {
            "price_categories": list(self.price_database.keys()),
            "expensive_items": len(self.price_database["expensive"]),
            "affordable_items": len(self.price_database["affordable"]),
            "budget_items": len(self.price_database["budget"])
        }
