"""
Nutrient database utilities for food analysis
"""

from typing import Dict, Any

# Sample food database (100g portions)
FOOD_DB_100G = {
    "chicken_breast": {
        "kcal": 165,
        "protein_g": 31.0,
        "carbs_g": 0.0,
        "fats_g": 3.6,
        "fiber_g": 0.0,
        "sodium_mg": 74
    },
    "brown_rice": {
        "kcal": 111,
        "protein_g": 2.6,
        "carbs_g": 23.0,
        "fats_g": 0.9,
        "fiber_g": 1.8,
        "sodium_mg": 5
    },
    "salmon": {
        "kcal": 208,
        "protein_g": 25.0,
        "carbs_g": 0.0,
        "fats_g": 12.0,
        "fiber_g": 0.0,
        "sodium_mg": 59
    },
    "broccoli": {
        "kcal": 34,
        "protein_g": 2.8,
        "carbs_g": 7.0,
        "fats_g": 0.4,
        "fiber_g": 2.6,
        "sodium_mg": 33
    },
    "quinoa": {
        "kcal": 120,
        "protein_g": 4.4,
        "carbs_g": 22.0,
        "fats_g": 1.9,
        "fiber_g": 2.8,
        "sodium_mg": 7
    }
}


def estimate_dish_nutrition_by_name(dish_name: str, weight_g: float) -> Dict[str, Any]:
    """Estimate nutrition for a dish based on name and weight"""
    
    # Simple estimation based on common ingredients
    dish_name_lower = dish_name.lower()
    
    # Default nutrition (generic dish)
    base_nutrition = {
        "kcal": 150,
        "protein_g": 8.0,
        "carbs_g": 20.0,
        "fats_g": 6.0,
        "fiber_g": 2.0,
        "sodium_mg": 300
    }
    
    # Adjust based on dish type
    if any(word in dish_name_lower for word in ["chicken", "poultry", "breast"]):
        base_nutrition.update({
            "kcal": 180,
            "protein_g": 25.0,
            "carbs_g": 5.0,
            "fats_g": 8.0
        })
    elif any(word in dish_name_lower for word in ["fish", "salmon", "tuna"]):
        base_nutrition.update({
            "kcal": 200,
            "protein_g": 22.0,
            "carbs_g": 0.0,
            "fats_g": 12.0
        })
    elif any(word in dish_name_lower for word in ["pasta", "noodles", "rice"]):
        base_nutrition.update({
            "kcal": 130,
            "protein_g": 4.0,
            "carbs_g": 25.0,
            "fats_g": 2.0
        })
    elif any(word in dish_name_lower for word in ["salad", "vegetables", "greens"]):
        base_nutrition.update({
            "kcal": 80,
            "protein_g": 3.0,
            "carbs_g": 15.0,
            "fats_g": 2.0,
            "fiber_g": 4.0
        })
    
    # Scale by weight
    scale_factor = weight_g / 100.0
    nutrition = {}
    
    for key, value in base_nutrition.items():
        if isinstance(value, (int, float)):
            nutrition[key] = value * scale_factor
        else:
            nutrition[key] = value
    
    return nutrition
