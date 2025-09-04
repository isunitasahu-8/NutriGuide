"""
Motivation & Education Agent - The Friend

Keeps users engaged, motivated, and educated about nutrition and health.
"""

from typing import Dict, Any
import random

from ..protocol import Agent, A2AMessage, MessageType


class MotivationEducationAgent(Agent):
    """The Friend - Keeps user engaged and educated"""
    
    def __init__(self):
        super().__init__("motivation_education_agent")
        self.motivation_tips = [
            "Every healthy choice is a step toward your goals!",
            "Your body thanks you for nourishing it well.",
            "Small changes lead to big results over time.",
            "You're building healthy habits that last a lifetime."
        ]
        self.education_tips = {
            "protein": "Protein helps build and repair muscles, and keeps you feeling full longer.",
            "fiber": "Fiber supports gut health and helps regulate blood sugar levels.",
            "healthy_fats": "Healthy fats are essential for brain health and hormone production.",
            "vitamins": "Vitamins and minerals support your immune system and overall health."
        }
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.MOTIVATION_MESSAGE:
            return self._provide_motivation(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "motivation_education_agent"}
        )
    
    def _provide_motivation(self, message: A2AMessage) -> A2AMessage:
        """Provide motivational and educational content"""
        context = message.content.get("context", "")
        progress = message.content.get("progress", {})
        
        # Generate motivational message
        if progress.get("weight_loss", 0) > 0:
            motivation = f"Congratulations! You've lost {progress['weight_loss']}kg. Your dedication is paying off!"
        elif progress.get("streak", 0) > 0:
            motivation = f"Amazing! You've been consistent for {progress['streak']} days. Keep up the great work!"
        else:
            motivation = random.choice(self.motivation_tips)
        
        # Add educational tip
        if "protein" in context.lower():
            education = self.education_tips["protein"]
        elif "fiber" in context.lower():
            education = self.education_tips["fiber"]
        else:
            education = "Remember: Every meal is an opportunity to nourish your body with the nutrients it needs."
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "motivation": motivation,
                "education": education,
                "message": "Motivation and education provided to keep you engaged"
            }
        )
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about motivation and education"""
        return {
            "motivation_tips_count": len(self.motivation_tips),
            "education_topics": list(self.education_tips.keys()),
            "total_education_tips": len(self.education_tips)
        }
