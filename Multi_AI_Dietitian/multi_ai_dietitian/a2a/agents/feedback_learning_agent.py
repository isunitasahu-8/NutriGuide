"""
Feedback & Learning Agent - The Evolver

Learns from user feedback and adapts plans based on patterns and preferences.
"""

from typing import Dict, List, Any
from datetime import datetime

from ..protocol import Agent, A2AMessage, MessageType


class FeedbackLearningAgent(Agent):
    """The Evolver - Learns from feedback and adapts"""
    
    def __init__(self):
        super().__init__("feedback_learning_agent")
        self.feedback_history: List[Dict[str, Any]] = []
        self.learning_patterns: Dict[str, Any] = {}
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.FEEDBACK_PROCESSING:
            return self._process_feedback(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "feedback_learning_agent"}
        )
    
    def _process_feedback(self, message: A2AMessage) -> A2AMessage:
        """Process user feedback and identify patterns"""
        feedback = message.content.get("feedback", {})
        user_id = message.content.get("user_id", "unknown")
        
        # Record feedback
        self.feedback_history.append({
            "timestamp": datetime.now(),
            "user_id": user_id,
            "feedback": feedback
        })
        
        # Analyze patterns
        patterns = self._analyze_patterns(user_id)
        
        # Generate adaptations
        adaptations = []
        
        if patterns.get("skips_lunch", 0) > 3:
            adaptations.append("Shift calories to breakfast/dinner")
        
        if patterns.get("complains_hunger", 0) > 2:
            adaptations.append("Increase protein and fiber content")
        
        if patterns.get("bored_with_meals", 0) > 2:
            adaptations.append("Introduce more variety and new cuisines")
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "patterns": patterns,
                "adaptations": adaptations,
                "message": f"Feedback processed: {len(adaptations)} adaptations suggested"
            }
        )
    
    def _analyze_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze feedback patterns for a specific user"""
        user_feedback = [f for f in self.feedback_history if f["user_id"] == user_id]
        
        patterns = {
            "skips_lunch": 0,
            "complains_hunger": 0,
            "bored_with_meals": 0,
            "loves_spicy": 0,
            "prefers_quick_meals": 0
        }
        
        for feedback in user_feedback:
            feedback_text = str(feedback["feedback"]).lower()
            
            if "skip lunch" in feedback_text or "no lunch" in feedback_text:
                patterns["skips_lunch"] += 1
            if "hungry" in feedback_text or "hunger" in feedback_text:
                patterns["complains_hunger"] += 1
            if "boring" in feedback_text or "same" in feedback_text:
                patterns["bored_with_meals"] += 1
            if "spicy" in feedback_text or "hot" in feedback_text:
                patterns["loves_spicy"] += 1
            if "quick" in feedback_text or "fast" in feedback_text:
                patterns["prefers_quick_meals"] += 1
        
        return patterns
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about feedback and learning"""
        return {
            "total_feedback_entries": len(self.feedback_history),
            "unique_users": len(set(f["user_id"] for f in self.feedback_history)),
            "learning_patterns": len(self.learning_patterns),
            "latest_feedback": self.feedback_history[-1]["timestamp"] if self.feedback_history else None
        }
