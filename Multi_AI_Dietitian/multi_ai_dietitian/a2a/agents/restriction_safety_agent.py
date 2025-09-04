"""
Restriction & Safety Agent - The Guardian

Ensures safety by flagging foods to avoid and warning against nutritional risks.
"""

from typing import Dict, List, Any

from ..protocol import Agent, A2AMessage, MessageType
from ...schemas import SafetyIssue


class RestrictionSafetyAgent(Agent):
    """The Guardian - Ensures safety and flags restrictions"""
    
    def __init__(self):
        super().__init__("restriction_safety_agent")
        self.safety_flags: List[SafetyIssue] = []
        self.restriction_database = {
            "allergens": ["nuts", "dairy", "eggs", "shellfish", "wheat", "soy"],
            "medication_interactions": {
                "grapefruit": ["statins", "blood_pressure_meds"],
                "vitamin_k_foods": ["warfarin"],
                "tyramine_foods": ["maois"]
            }
        }
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.SAFETY_CHECK:
            return self._check_safety(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "restriction_safety_agent"}
        )
    
    def _check_safety(self, message: A2AMessage) -> A2AMessage:
        """Check food safety against user restrictions"""
        foods = message.content.get("foods", [])
        user_profile = message.content.get("user_profile", {})
        
        issues = []
        warnings = []
        
        # Check allergens
        allergies = user_profile.get("allergies", [])
        for food in foods:
            food_lower = food.lower()
            for allergen in allergies:
                if allergen.lower() in food_lower:
                    issues.append(f"ALLERGY ALERT: {food} contains {allergen}")
        
        # Check medication interactions
        medications = user_profile.get("medications", [])
        for food in foods:
            food_lower = food.lower()
            for food_type, meds in self.restriction_database["medication_interactions"].items():
                if food_type in food_lower:
                    for med in meds:
                        if med in [m.lower() for m in medications]:
                            warnings.append(f"INTERACTION: {food} may interact with {med}")
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "safe": len(issues) == 0,
                "issues": issues,
                "warnings": warnings,
                "message": f"Safety check complete: {len(issues)} critical issues, {len(warnings)} warnings"
            }
        )
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about safety checks"""
        return {
            "total_safety_flags": len(self.safety_flags),
            "known_allergens": len(self.restriction_database["allergens"]),
            "medication_interactions": len(self.restriction_database["medication_interactions"]),
            "safety_checks_performed": len(self.safety_flags)
        }
