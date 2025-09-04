"""
Food Knowledge Agent - The Expert Chef + Scientist

Database of foods, recipes, and nutrition science with evidence-based suggestions.
"""

from typing import Dict, List, Any

from ..protocol import Agent, A2AMessage, MessageType
from ...utils.nutrient_db import estimate_dish_nutrition_by_name


class FoodKnowledgeAgent(Agent):
    """The Expert Chef + Scientist - Database of foods and nutrition science"""
    
    def __init__(self):
        super().__init__("food_knowledge_agent")
        self.food_database = {
            "proteins": ["chicken", "salmon", "tofu", "lentils", "eggs", "greek yogurt"],
            "carbs": ["brown rice", "quinoa", "oats", "sweet potato", "banana"],
            "fats": ["olive oil", "almonds", "avocado"],
            "vegetables": ["broccoli", "spinach", "tomato", "carrots"],
            "cooking_methods": ["grilled", "baked", "steamed", "raw", "stir-fried"]
        }
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.FOOD_SUGGESTION:
            return self._suggest_foods(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "food_knowledge_agent"}
        )
    
    def _suggest_foods(self, message: A2AMessage) -> A2AMessage:
        """Suggest foods based on preferences and targets"""
        preferences = message.content.get("preferences", {})
        targets = message.content.get("targets", {})
        
        # Add variety by using different meal options for each day
        import random
        
        # Generate 7-day meal plan with variety
        daily_meals = {}
        for day in range(1, 8):
            day_key = f"day_{day}"
            
            # Use different meal variations for each day
            breakfast_options = self._suggest_breakfast(preferences, targets)
            lunch_options = self._suggest_lunch(preferences, targets)
            dinner_options = self._suggest_dinner(preferences, targets)
            snack_options = self._suggest_snacks(preferences, targets)
            
            # Select different options for variety (cycle through options)
            breakfast = breakfast_options[day % len(breakfast_options)]
            lunch = lunch_options[day % len(lunch_options)]
            dinner = dinner_options[day % len(dinner_options)]
            snack = snack_options[day % len(snack_options)]
            
            daily_meals[day_key] = {
                "breakfast": {
                    "name": breakfast["name"],
                    "calories": breakfast["nutrition"]["kcal"],
                    "protein_g": breakfast["nutrition"]["protein_g"],
                    "carbs_g": breakfast["nutrition"]["carbs_g"],
                    "fats_g": breakfast["nutrition"]["fats_g"],
                    "ingredients": breakfast["ingredients"],
                    "instructions": breakfast.get("instructions", "")
                },
                "lunch": {
                    "name": lunch["name"],
                    "calories": lunch["nutrition"]["kcal"],
                    "protein_g": lunch["nutrition"]["protein_g"],
                    "carbs_g": lunch["nutrition"]["carbs_g"],
                    "fats_g": lunch["nutrition"]["fats_g"],
                    "ingredients": lunch["ingredients"],
                    "instructions": lunch.get("instructions", "")
                },
                "dinner": {
                    "name": dinner["name"],
                    "calories": dinner["nutrition"]["kcal"],
                    "protein_g": dinner["nutrition"]["protein_g"],
                    "carbs_g": dinner["nutrition"]["carbs_g"],
                    "fats_g": dinner["nutrition"]["fats_g"],
                    "ingredients": dinner["ingredients"],
                    "instructions": dinner.get("instructions", "")
                },
                "snack_1": {
                    "name": snack["name"],
                    "calories": snack["nutrition"]["kcal"],
                    "protein_g": snack["nutrition"]["protein_g"],
                    "carbs_g": snack["nutrition"]["carbs_g"],
                    "fats_g": snack["nutrition"]["fats_g"],
                    "ingredients": snack["ingredients"],
                    "instructions": snack.get("instructions", "")
                },
                "snack_2": {
                    "name": snack["name"],
                    "calories": snack["nutrition"]["kcal"],
                    "protein_g": snack["nutrition"]["protein_g"],
                    "carbs_g": snack["nutrition"]["carbs_g"],
                    "fats_g": snack["nutrition"]["fats_g"],
                    "ingredients": snack["ingredients"],
                    "instructions": snack.get("instructions", "")
                }
            }
        
        # Calculate totals
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fats = 0
        
        for day_meals in daily_meals.values():
            for meal in day_meals.values():
                total_calories += meal.get("calories", 0)
                total_protein += meal.get("protein_g", 0)
                total_carbs += meal.get("carbs_g", 0)
                total_fats += meal.get("fats_g", 0)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "daily_meals": daily_meals,
                "total_calories": total_calories,
                "total_protein": total_protein,
                "total_carbs": total_carbs,
                "total_fats": total_fats,
                "message": "Evidence-based 7-day meal plan tailored to your preferences"
            }
        )
    
    def _suggest_breakfast(self, preferences: Dict, targets: Dict) -> List[Dict]:
        """Suggest breakfast options with variety"""
        vegetarian = "vegetarian" in preferences.get("dietary_preferences", [])
        protein_sources = ["tofu", "greek yogurt"] if vegetarian else ["eggs", "greek yogurt"]
        
        return [
            {
                "name": "Protein Power Bowl",
                "ingredients": [
                    {"name": protein_sources[0], "grams": 150, "method": "scrambled" if "eggs" in protein_sources[0] else "cubed"},
                    {"name": "oats", "grams": 50, "method": "cooked"},
                    {"name": "banana", "grams": 120, "method": "sliced"},
                    {"name": "almonds", "grams": 20, "method": "chopped"}
                ],
                "nutrition": self._calculate_nutrition([protein_sources[0], "oats", "banana", "almonds"], [150, 50, 120, 20]),
                "instructions": "Cook oats with water. Scramble eggs or cube tofu. Slice banana and chop almonds. Layer in bowl and enjoy!"
            },
            {
                "name": "Green Smoothie Bowl",
                "ingredients": [
                    {"name": "spinach", "grams": 50, "method": "blended"},
                    {"name": "banana", "grams": 100, "method": "frozen"},
                    {"name": "greek yogurt", "grams": 100, "method": "plain"},
                    {"name": "chia seeds", "grams": 15, "method": "sprinkled"}
                ],
                "nutrition": self._calculate_nutrition(["spinach", "banana", "greek yogurt", "chia seeds"], [50, 100, 100, 15]),
                "instructions": "Blend spinach, frozen banana, and yogurt until smooth. Pour into bowl and top with chia seeds."
            },
            {
                "name": "Avocado Toast Deluxe",
                "ingredients": [
                    {"name": "whole grain bread", "grams": 60, "method": "toasted"},
                    {"name": "avocado", "grams": 80, "method": "mashed"},
                    {"name": "eggs" if not vegetarian else "tofu", "grams": 100, "method": "poached" if not vegetarian else "scrambled"},
                    {"name": "tomato", "grams": 50, "method": "sliced"}
                ],
                "nutrition": self._calculate_nutrition(["whole grain bread", "avocado", "eggs" if not vegetarian else "tofu", "tomato"], [60, 80, 100, 50]),
                "instructions": "Toast bread. Mash avocado with salt and pepper. Poach egg or scramble tofu. Layer avocado, egg/tofu, and tomato slices on toast."
            }
        ]
    
    def _suggest_lunch(self, preferences: Dict, targets: Dict) -> List[Dict]:
        """Suggest lunch options with variety"""
        vegetarian = "vegetarian" in preferences.get("dietary_preferences", [])
        protein = "tofu" if vegetarian else "chicken"
        
        return [
            {
                "name": "Mediterranean Bowl",
                "ingredients": [
                    {"name": protein, "grams": 180, "method": "grilled"},
                    {"name": "quinoa", "grams": 150, "method": "cooked"},
                    {"name": "cucumber", "grams": 100, "method": "diced"},
                    {"name": "tomato", "grams": 80, "method": "chopped"},
                    {"name": "olive oil", "grams": 10, "method": "drizzle"}
                ],
                "nutrition": self._calculate_nutrition([protein, "quinoa", "cucumber", "tomato", "olive oil"], [180, 150, 100, 80, 10]),
                "instructions": "Grill protein and cook quinoa. Dice cucumber and chop tomato. Combine in bowl and drizzle with olive oil."
            },
            {
                "name": "Asian Stir-Fry",
                "ingredients": [
                    {"name": protein, "grams": 160, "method": "stir-fried"},
                    {"name": "brown rice", "grams": 180, "method": "cooked"},
                    {"name": "bell pepper", "grams": 100, "method": "sliced"},
                    {"name": "broccoli", "grams": 120, "method": "steamed"},
                    {"name": "soy sauce", "grams": 15, "method": "drizzle"}
                ],
                "nutrition": self._calculate_nutrition([protein, "brown rice", "bell pepper", "broccoli", "soy sauce"], [160, 180, 100, 120, 15]),
                "instructions": "Cook brown rice. Stir-fry protein with bell peppers. Steam broccoli separately. Combine and drizzle with soy sauce."
            },
            {
                "name": "Power Salad",
                "ingredients": [
                    {"name": protein, "grams": 150, "method": "grilled"},
                    {"name": "mixed greens", "grams": 100, "method": "fresh"},
                    {"name": "avocado", "grams": 60, "method": "sliced"},
                    {"name": "sweet potato", "grams": 120, "method": "roasted"},
                    {"name": "olive oil", "grams": 8, "method": "drizzle"}
                ],
                "nutrition": self._calculate_nutrition([protein, "mixed greens", "avocado", "sweet potato", "olive oil"], [150, 100, 60, 120, 8]),
                "instructions": "Grill protein and roast sweet potato. Arrange mixed greens in bowl. Top with sliced avocado, protein, and sweet potato. Drizzle with olive oil."
            }
        ]
    
    def _suggest_dinner(self, preferences: Dict, targets: Dict) -> List[Dict]:
        """Suggest dinner options with variety"""
        vegetarian = "vegetarian" in preferences.get("dietary_preferences", [])
        protein = "lentils" if vegetarian else "salmon"
        
        return [
            {
                "name": "Herb-Crusted Protein",
                "ingredients": [
                    {"name": protein, "grams": 160, "method": "baked"},
                    {"name": "sweet potato", "grams": 200, "method": "roasted"},
                    {"name": "asparagus", "grams": 100, "method": "grilled"},
                    {"name": "olive oil", "grams": 8, "method": "drizzle"}
                ],
                "nutrition": self._calculate_nutrition([protein, "sweet potato", "asparagus", "olive oil"], [160, 200, 100, 8]),
                "instructions": "Season protein with herbs and bake. Roast sweet potato and grill asparagus. Drizzle with olive oil and serve."
            },
            {
                "name": "One-Pan Wonder",
                "ingredients": [
                    {"name": protein, "grams": 150, "method": "pan-seared"},
                    {"name": "zucchini", "grams": 120, "method": "sautéed"},
                    {"name": "bell pepper", "grams": 100, "method": "sautéed"},
                    {"name": "brown rice", "grams": 150, "method": "cooked"},
                    {"name": "olive oil", "grams": 10, "method": "drizzle"}
                ],
                "nutrition": self._calculate_nutrition([protein, "zucchini", "bell pepper", "brown rice", "olive oil"], [150, 120, 100, 150, 10]),
                "instructions": "Cook brown rice. Pan-sear protein and sauté vegetables in the same pan. Serve over rice with olive oil drizzle."
            },
            {
                "name": "Comfort Bowl",
                "ingredients": [
                    {"name": protein, "grams": 140, "method": "braised"},
                    {"name": "quinoa", "grams": 180, "method": "cooked"},
                    {"name": "carrots", "grams": 100, "method": "roasted"},
                    {"name": "spinach", "grams": 80, "method": "wilted"},
                    {"name": "olive oil", "grams": 8, "method": "drizzle"}
                ],
                "nutrition": self._calculate_nutrition([protein, "quinoa", "carrots", "spinach", "olive oil"], [140, 180, 100, 80, 8]),
                "instructions": "Braise protein with herbs. Cook quinoa and roast carrots. Wilt spinach. Layer in bowl and drizzle with olive oil."
            }
        ]
    
    def _suggest_snacks(self, preferences: Dict, targets: Dict) -> List[Dict]:
        """Suggest snack options with variety"""
        return [
            {
                "name": "Energy Bites",
                "ingredients": [
                    {"name": "almonds", "grams": 25, "method": "chopped"},
                    {"name": "dates", "grams": 40, "method": "pitted"},
                    {"name": "coconut", "grams": 10, "method": "shredded"}
                ],
                "nutrition": self._calculate_nutrition(["almonds", "dates", "coconut"], [25, 40, 10]),
                "instructions": "Chop almonds and pit dates. Blend with coconut until sticky. Roll into small balls and refrigerate."
            },
            {
                "name": "Greek Yogurt Parfait",
                "ingredients": [
                    {"name": "greek yogurt", "grams": 120, "method": "plain"},
                    {"name": "berries", "grams": 80, "method": "fresh"},
                    {"name": "granola", "grams": 20, "method": "homemade"}
                ],
                "nutrition": self._calculate_nutrition(["greek yogurt", "berries", "granola"], [120, 80, 20]),
                "instructions": "Layer yogurt, berries, and granola in a glass. Repeat layers and enjoy immediately."
            },
            {
                "name": "Veggie Hummus",
                "ingredients": [
                    {"name": "hummus", "grams": 60, "method": "store-bought"},
                    {"name": "carrot sticks", "grams": 100, "method": "fresh"},
                    {"name": "cucumber", "grams": 80, "method": "sliced"}
                ],
                "nutrition": self._calculate_nutrition(["hummus", "carrot", "cucumber"], [60, 100, 80]),
                "instructions": "Cut carrots into sticks and slice cucumber. Serve with hummus for dipping."
            },
            {
                "name": "Protein Smoothie",
                "ingredients": [
                    {"name": "protein powder", "grams": 25, "method": "vanilla"},
                    {"name": "banana", "grams": 100, "method": "frozen"},
                    {"name": "almond milk", "grams": 200, "method": "unsweetened"},
                    {"name": "spinach", "grams": 30, "method": "fresh"}
                ],
                "nutrition": self._calculate_nutrition(["protein powder", "banana", "almond milk", "spinach"], [25, 100, 200, 30]),
                "instructions": "Blend protein powder, frozen banana, almond milk, and spinach until smooth. Serve immediately."
            }
        ]
    
    def _calculate_nutrition(self, foods: List[str], grams: List[float]) -> Dict[str, float]:
        """Calculate total nutrition for a combination of foods"""
        totals = {"kcal": 0, "protein_g": 0, "carbs_g": 0, "fats_g": 0, "fiber_g": 0, "sodium_mg": 0}
        for food, gram in zip(foods, grams):
            nutrition = estimate_dish_nutrition_by_name(food, gram)
            for key, value in nutrition.items():
                totals[key] = totals.get(key, 0) + value
        return totals
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about food knowledge"""
        return {
            "total_food_categories": len(self.food_database),
            "protein_sources": len(self.food_database["proteins"]),
            "carb_sources": len(self.food_database["carbs"]),
            "cooking_methods": len(self.food_database["cooking_methods"])
        }
