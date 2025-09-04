"""
Nutrition calculation utilities for the Multi-Agent AI Dietitian System
"""

from typing import Dict, Any, Tuple


def calculate_bmr_mifflin(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation"""
    if gender.lower() in ['male', 'm']:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    
    return bmr


def calculate_tdee(bmr: float, activity_level: str) -> float:
    """Calculate Total Daily Energy Expenditure"""
    activity_multipliers = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extremely active": 1.9
    }
    
    multiplier = activity_multipliers.get(activity_level.lower(), 1.2)
    return bmr * multiplier


def plan_energy_and_macros(weight_kg: float, height_cm: float, age: int, 
                          gender: str, activity_level: str, goal_type: str) -> Dict[str, Any]:
    """Plan energy and macronutrient targets"""
    
    # Calculate BMR and TDEE
    bmr = calculate_bmr_mifflin(weight_kg, height_cm, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    
    # Adjust calories based on goal
    if goal_type == "weight_loss":
        target_calories = tdee - 500  # 500 calorie deficit
    elif goal_type == "muscle_gain":
        target_calories = tdee + 300  # 300 calorie surplus
    else:
        target_calories = tdee  # maintenance
    
    # Calculate macronutrient targets
    protein_g = weight_kg * 2.0  # 2g per kg body weight
    fats_g = (target_calories * 0.25) / 9  # 25% of calories from fat
    carbs_g = (target_calories - (protein_g * 4) - (fats_g * 9)) / 4  # Remaining calories
    
    return {
        "bmr": bmr,
        "tdee": tdee,
        "target_calories": target_calories,
        "protein_g": protein_g,
        "fats_g": fats_g,
        "carbs_g": carbs_g,
        "fiber_g": 25.0,  # Recommended daily fiber
        "sodium_mg": 2300.0  # Recommended daily sodium
    }


def sum_nutrition(nutrition_list: list) -> Dict[str, float]:
    """Sum up nutrition values from a list of foods"""
    total = {
        "kcal": 0.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fats_g": 0.0,
        "fiber_g": 0.0,
        "sodium_mg": 0.0
    }
    
    for item in nutrition_list:
        for key in total:
            if key in item:
                total[key] += item[key]
    
    return total


def kcal_from_macros(protein_g: float, carbs_g: float, fats_g: float) -> float:
    """Calculate total calories from macronutrients"""
    return (protein_g * 4) + (carbs_g * 4) + (fats_g * 9)
