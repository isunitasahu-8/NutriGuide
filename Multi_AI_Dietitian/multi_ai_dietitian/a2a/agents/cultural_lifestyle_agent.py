"""
Cultural & Lifestyle Agent - The Personal Touch

Considers cultural, religious, and lifestyle factors in meal planning.
"""

from typing import Dict, Any

from ..protocol import Agent, A2AMessage, MessageType


class CulturalLifestyleAgent(Agent):
    """The Personal Touch - Considers cultural and lifestyle factors"""
    
    def __init__(self):
        super().__init__("cultural_lifestyle_agent")
        self.cultural_database = {
            "indian": {
                "vegetarian_options": ["paneer", "dal", "tofu", "quinoa"],
                "spices": ["turmeric", "cumin", "coriander", "ginger"],
                "cooking_methods": ["curry", "tandoor", "steamed"]
            },
            "mediterranean": {
                "proteins": ["fish", "chicken", "legumes"],
                "fats": ["olive oil", "nuts", "avocado"],
                "grains": ["quinoa", "farro", "bulgur"]
            },
            "asian": {
                "proteins": ["tofu", "fish", "chicken"],
                "vegetables": ["bok choy", "ginger", "garlic"],
                "cooking_methods": ["stir-fry", "steamed", "soup"]
            }
        }
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.CULTURAL_ADAPTATION:
            return self._adapt_culturally(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "cultural_lifestyle_agent"}
        )
    
    def _adapt_culturally(self, message: A2AMessage) -> A2AMessage:
        """Adapt meals to cultural preferences"""
        cuisine_pref = message.content.get("cuisine_preference", "").lower()
        dietary_prefs = message.content.get("dietary_preferences", [])
        suggestions = message.content.get("suggestions", {})
        
        adaptations = {}
        
        if "indian" in cuisine_pref:
            adaptations["protein_swap"] = "paneer" if "vegetarian" in dietary_prefs else "chicken"
            adaptations["grain_swap"] = "quinoa"
            adaptations["spice_additions"] = ["turmeric", "cumin"]
        
        elif "mediterranean" in cuisine_pref:
            adaptations["protein_swap"] = "fish"
            adaptations["fat_swap"] = "olive oil"
            adaptations["grain_swap"] = "quinoa"
        
        elif "asian" in cuisine_pref:
            adaptations["protein_swap"] = "tofu" if "vegetarian" in dietary_prefs else "fish"
            adaptations["vegetable_additions"] = ["bok choy", "ginger"]
            adaptations["cooking_method"] = "stir-fry"
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "cultural_adaptations": adaptations,
                "message": f"Meals adapted to {cuisine_pref} cultural preferences"
            }
        )
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about cultural adaptations"""
        return {
            "supported_cuisines": list(self.cultural_database.keys()),
            "total_cultural_options": len(self.cultural_database),
            "adaptation_categories": ["protein_swap", "grain_swap", "spice_additions", "cooking_method"]
        }
