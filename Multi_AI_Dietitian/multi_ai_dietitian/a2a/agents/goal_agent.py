"""
Goal Agent - The Planner

Aligns nutrition with user goals and creates nutritional blueprints.
"""

from typing import Dict, Any
from datetime import datetime

from ..protocol import Agent, A2AMessage, MessageType
from ...schemas import UserProfile, MacroTargets
from ...utils.calculations import plan_energy_and_macros


class GoalAgent(Agent):
    """The Planner - Aligns nutrition with goals"""
    
    def __init__(self):
        super().__init__("goal_agent")
        self.nutritional_blueprints: Dict[str, MacroTargets] = {}
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.GOAL_ANALYSIS:
            return self._analyze_goals(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "goal_agent"}
        )
    
    def _analyze_goals(self, message: A2AMessage) -> A2AMessage:
        """Analyze user goals and create nutritional blueprint"""
        profile_data = message.content.get("profile", {})
        
        # Add default values for missing required fields
        defaults = {
            "cooking_skill": "beginner",
            "time_availability": "medium", 
            "training_days": [],
            "medical_conditions": [],
            "medications": []
        }
        
        # Merge defaults with provided data
        complete_profile = {**defaults, **profile_data}
        user_profile = UserProfile(**complete_profile)
        
        # Calculate nutritional blueprint
        targets_plan = plan_energy_and_macros(
            weight_kg=user_profile.weight_kg,
            height_cm=user_profile.height_cm,
            age=user_profile.age,
            gender=user_profile.gender,
            activity_level=user_profile.activity_level,
            goal_type=user_profile.goal_type
        )
        
        # Store blueprint
        blueprint_id = f"blueprint_{user_profile.name}_{datetime.now().strftime('%Y%m%d')}"
        self.nutritional_blueprints[blueprint_id] = targets_plan
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "blueprint_id": blueprint_id,
                "targets": targets_plan,
                "tdee": targets_plan.get("tdee", 0),
                "message": f"Nutritional blueprint created for {user_profile.goal_type} goal"
            }
        )
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about nutritional blueprints"""
        return {
            "total_blueprints": len(self.nutritional_blueprints),
            "blueprint_ids": list(self.nutritional_blueprints.keys()),
            "latest_blueprint": list(self.nutritional_blueprints.keys())[-1] if self.nutritional_blueprints else None
        }
