"""
Adaptation Agent - The Coach

Tracks progress and adapts plans based on user feedback and results.
"""

from typing import Dict, List, Any
from datetime import datetime

from ..protocol import Agent, A2AMessage, MessageType


class AdaptationAgent(Agent):
    """The Coach - Tracks progress and adapts plans"""
    
    def __init__(self):
        super().__init__("adaptation_agent")
        self.progress_history: List[Dict[str, Any]] = []
        self.adaptation_log: List[Dict[str, Any]] = []
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.ADAPTATION_REQUEST:
            return self._adapt_plan(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "adaptation_agent"}
        )
    
    def _adapt_plan(self, message: A2AMessage) -> A2AMessage:
        """Adapt plan based on user feedback"""
        feedback = message.content.get("feedback", {})
        current_plan = message.content.get("current_plan", {})
        
        adaptations = []
        
        # Weight plateau adaptation
        if feedback.get("weight_plateau", False):
            adaptations.append({
                "type": "calorie_adjustment",
                "action": "reduce_calories_by_100",
                "reason": "Weight plateau detected"
            })
        
        # Boredom adaptation
        if feedback.get("boredom", False):
            adaptations.append({
                "type": "cuisine_rotation",
                "action": "introduce_new_cuisine",
                "reason": "User reported meal boredom"
            })
        
        # Record adaptation
        self.adaptation_log.append({
            "timestamp": datetime.now(),
            "feedback": feedback,
            "adaptations": adaptations
        })
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "adaptations": adaptations,
                "message": f"Plan adapted with {len(adaptations)} changes based on feedback"
            }
        )
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about adaptations"""
        return {
            "total_adaptations": len(self.adaptation_log),
            "progress_entries": len(self.progress_history),
            "latest_adaptation": self.adaptation_log[-1]["timestamp"] if self.adaptation_log else None,
            "adaptation_types": list(set([a["type"] for entry in self.adaptation_log for a in entry["adaptations"]]))
        }
