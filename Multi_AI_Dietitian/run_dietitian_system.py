"""
Multi-Agent AI Dietitian System - Single Runner

This file provides a unified interface to run all components of the system.
"""

import sys
import os
import argparse
from pathlib import Path

def run_streamlit():
    """Run the Streamlit interface"""
    try:
        import streamlit
        os.system("streamlit run streamlit_app.py")
    except ImportError:
        print("Streamlit not installed. Installing...")
        os.system("pip install streamlit")
        os.system("streamlit run streamlit_app.py")

def run_a2a_system():
    """Run the A2A system directly"""
    try:
        from multi_ai_dietitian.a2a.orchestrator import A2ADietitianOrchestrator
        from multi_ai_dietitian.schemas import UserProfile
        
        # Create sample user profile
        user_profile = UserProfile(
            name="Test User",
            age=30,
            gender="Male",
            height_cm=175,
            weight_kg=70,
            activity_level="Moderately Active",
            goal_type="weight_loss",
            dietary_preferences=["vegetarian"],
            allergies=[],
            intolerances=[],
            disliked_foods=[],
            avoid_ingredients=[],
            cuisine_preference="mediterranean",
            budget_level="medium",
            cooking_skill="intermediate",
            time_availability="medium",
            training_days=[1, 3, 5],
            medical_conditions=[],
            medications=[],
            country="United States"
        )
        
        # Initialize orchestrator
        orchestrator = A2ADietitianOrchestrator()
        
        # Generate plan
        print("Generating comprehensive meal plan...")
        result = orchestrator.create_comprehensive_plan(user_profile)
        
        print("Plan generated successfully!")
        print(f"Flow ID: {result['flow_id']}")
        print(f"Status: {result['status']}")
        
        if result['status'] == 'success':
            print("\nSummary:")
            summary = result['summary']
            for key, value in summary.items():
                print(f"  {key}: {type(value).__name__}")
        
        return result
        
    except Exception as e:
        print(f"Error running A2A system: {e}")
        return None

def run_dish_analysis():
    """Run dish analysis"""
    try:
        from multi_ai_dietitian.utils.nutrient_db import estimate_dish_nutrition_by_name
        
        dish_name = input("Enter dish name: ")
        weight = float(input("Enter weight in grams: "))
        
        nutrition = estimate_dish_nutrition_by_name(dish_name, weight)
        
        print(f"\nNutrition Analysis for {dish_name} ({weight}g):")
        print(f"Calories: {nutrition['kcal']:.0f} kcal")
        print(f"Protein: {nutrition['protein_g']:.1f} g")
        print(f"Carbs: {nutrition['carbs_g']:.1f} g")
        print(f"Fat: {nutrition['fats_g']:.1f} g")
        print(f"Fiber: {nutrition['fiber_g']:.1f} g")
        print(f"Sodium: {nutrition['sodium_mg']:.0f} mg")
        
    except Exception as e:
        print(f"Error analyzing dish: {e}")

def run_agent_insights():
    """Run agent insights"""
    try:
        from multi_ai_dietitian.a2a.orchestrator import A2ADietitianOrchestrator
        
        orchestrator = A2ADietitianOrchestrator()
        insights = orchestrator.get_agent_insights()
        
        print("Agent Insights:")
        for agent_name, agent_info in insights.items():
            print(f"  {agent_name}: {agent_info}")
            
    except Exception as e:
        print(f"Error getting agent insights: {e}")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    os.system("pip install -r requirements.txt")
    print("Dependencies installed successfully!")

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent AI Dietitian System")
    parser.add_argument("--mode", choices=["streamlit", "a2a", "dish", "insights", "install"], 
                       default="streamlit", help="Mode to run")
    
    args = parser.parse_args()
    
    if args.mode == "streamlit":
        print("Starting Streamlit interface...")
        run_streamlit()
    elif args.mode == "a2a":
        print("Running A2A system...")
        run_a2a_system()
    elif args.mode == "dish":
        print("Running dish analysis...")
        run_dish_analysis()
    elif args.mode == "insights":
        print("Getting agent insights...")
        run_agent_insights()
    elif args.mode == "install":
        install_dependencies()

if __name__ == "__main__":
    main()
