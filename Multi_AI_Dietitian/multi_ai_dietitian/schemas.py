"""
Data schemas for the Multi-Agent AI Dietitian System
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime


@dataclass
class MacroTargets:
    """Macro and micro nutrient targets"""
    calories: float
    protein_g: float
    carbs_g: float
    fats_g: float
    fiber_g: float
    sodium_mg: float
    calcium_mg: float
    iron_mg: float
    vitamin_d_iu: float


@dataclass
class UserProfile:
    """User profile with all preferences and constraints"""
    name: str
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    activity_level: str
    goal_type: str
    dietary_preferences: List[str]
    allergies: List[str]
    intolerances: List[str]
    disliked_foods: List[str]
    avoid_ingredients: List[str]
    cuisine_preference: str
    budget_level: str
    cooking_skill: str
    time_availability: str
    training_days: List[int]
    medical_conditions: List[str]
    medications: List[str]
    country: str


@dataclass
class Plan30:
    """30-day nutrition plan"""
    user_profile: UserProfile
    targets_plan: MacroTargets
    weeks: List[Dict[str, Any]]
    safety_issues: List[str]
    disclaimers: List[str]
    adherence_playbook: Dict[str, Any]


@dataclass
class Meal:
    """Individual meal information"""
    name: str
    calories: float
    protein_g: float
    carbs_g: float
    fats_g: float
    ingredients: List[Dict[str, Any]]
    instructions: List[str]


@dataclass
class Recipe:
    """Recipe with detailed information"""
    name: str
    ingredients: List[Dict[str, Any]]
    instructions: List[str]
    nutrition: MacroTargets
    prep_time: int
    cook_time: int
    servings: int


@dataclass
class SafetyIssue:
    """Safety concern or contraindication"""
    severity: Literal["low", "medium", "high", "critical"]
    description: str
    recommendation: str
    requires_medical_attention: bool
