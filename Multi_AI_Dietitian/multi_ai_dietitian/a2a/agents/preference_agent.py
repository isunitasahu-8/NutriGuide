"""
Preference Agent - The Listener

Understands user preferences and builds comprehensive food profile.
"""

from typing import Dict, List, Any
from datetime import datetime

from ..protocol import Agent, A2AMessage, MessageType


class PreferenceAgent(Agent):
    """The Listener - Understands user preferences and builds food profile"""
    
    def __init__(self):
        super().__init__("preference_agent")
        self.user_profile: Dict[str, Any] = {}
        self.preference_history: List[Dict[str, Any]] = []
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.PREFERENCE_UPDATE:
            return self._update_preferences(message)
        elif message.message_type == MessageType.REQUEST:
            return self._get_preferences(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "preference_agent"}
        )
    
    def _update_preferences(self, message: A2AMessage) -> A2AMessage:
        """Update user preferences and store in history"""
        content = message.content
        self.user_profile.update(content)
        self.preference_history.append({
            "timestamp": datetime.now(),
            "preferences": content.copy()
        })
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "status": "preferences_updated",
                "profile": self.user_profile,
                "message": "Preferences logged and will be respected in all meal suggestions"
            }
        )
    
    def _get_preferences(self, message: A2AMessage) -> A2AMessage:
        """Retrieve current user preferences"""
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"preferences": self.user_profile}
        )
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about user preferences"""
        return {
            "total_preferences": len(self.user_profile),
            "preference_history_count": len(self.preference_history),
            "last_updated": self.preference_history[-1]["timestamp"] if self.preference_history else None,
            "preference_categories": list(self.user_profile.keys()) if self.user_profile else []
        }
