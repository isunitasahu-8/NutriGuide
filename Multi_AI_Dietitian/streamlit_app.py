"""
AI Dietitian Pro — Minimalist, real-time interaction UI.

No agent dashboards or manual initialization. Single interface to run the LangGraph
workflow and interact with the system outputs.
"""

import streamlit as st
from typing import Dict, Any, List
import random
import pandas as pd
import os
from datetime import datetime

from multi_ai_dietitian.a2a.orchestrator import A2ADietitianOrchestrator
try:
    from multi_ai_dietitian.a2a.langgraph_orchestrator import build_ai_dietitian_graph
    _HAS_LANGGRAPH = True
except Exception:
    build_ai_dietitian_graph = None  # type: ignore
    _HAS_LANGGRAPH = False
from multi_ai_dietitian.a2a.protocol import SystemState
from multi_ai_dietitian.utils.exports import export_csv, export_pdf, export_docx


st.set_page_config(
    page_title="NutriGuide", 
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Your personalized AI powered dietitian."
    }
)

# Custom CSS for background and interactive design
st.markdown("""
<style>
    /* Custom gradient background */
    .stApp {
        background: radial-gradient(circle, rgba(235, 188, 235, 1) 0%, rgba(233, 193, 148, 1) 100%);
        background-attachment: fixed;
    }
    
    /* Interactive title styling */
    .interactive-title {
        text-align: center;
        color: #4a2c5a;
        font-weight: bold;
        font-size: 2.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    
    /* Interactive subtitle */
    .interactive-subtitle {
        text-align: center;
        color: #5a3c4a;
        font-style: italic;
        font-size: 1.2rem;
        margin-bottom: 20px;
    }
    
    /* Interactive cards */
    .interactive-card {
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        background: rgba(255, 255, 255, 0.95);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(235, 188, 235, 0.4);
        transition: all 0.2s ease;
    }
    
    .interactive-card:hover {
        box-shadow: 0 8px 20px rgba(235, 188, 235, 0.3);
        border-color: rgba(235, 188, 235, 0.6);
    }
    
    /* Profile card styling */
    .profile-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(235, 188, 235, 0.15));
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border: 2px solid rgba(235, 188, 235, 0.4);
        transition: all 0.2s ease;
    }
    
    .profile-card:hover {
        box-shadow: 0 10px 25px rgba(235, 188, 235, 0.4);
        border-color: rgba(235, 188, 235, 0.6);
    }
    
    /* Interactive buttons */
    .stButton > button {
        background: linear-gradient(45deg, #8b5a8b, #a67c5a);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        transition: all 0.2s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #a67c5a, #8b5a8b);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Interactive metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 2px solid rgba(139, 90, 139, 0.3);
        transition: all 0.2s ease;
        color: #4a2c5a;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 20px rgba(139, 90, 139, 0.3);
        border-color: rgba(139, 90, 139, 0.5);
    }
    
    /* Interactive headings */
    .interactive-heading {
        color: #4a2c5a;
        font-weight: bold;
        margin: 15px 0 10px 0;
        padding: 10px 0;
        border-bottom: 2px solid rgba(235, 188, 235, 0.5);
    }
    
    /* Interactive section headers */
    .section-header {
        color: #5a3c4a;
        font-size: 1.4rem;
        font-weight: bold;
        margin: 20px 0 15px 0;
        padding: 15px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 8px;
        border-left: 4px solid rgba(139, 90, 139, 0.6);
    }
    
    /* Interactive form elements */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(235, 188, 235, 0.4);
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(235, 188, 235, 0.4);
        border-radius: 8px;
        color: #4a2c5a;
    }
    
    .stNumberInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(235, 188, 235, 0.4);
        border-radius: 8px;
        color: #4a2c5a;
    }
    
    /* Interactive tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #4a2c5a;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(139, 90, 139, 0.2);
        color: #4a2c5a;
    }
</style>
""", unsafe_allow_html=True)


def generate_simple_instructions(ingredients: List[Dict]) -> str:
    """Generate simple cooking instructions based on ingredients"""
    if not ingredients:
        return ""
    
    instructions = []
    for i, ing in enumerate(ingredients, 1):
        name = ing.get('name', '')
        method = ing.get('method', '')
        amount = ing.get('grams', ing.get('amount', ''))
        
        if method:
            if 'cooked' in method:
                instructions.append(f"{i}. Cook {name} until tender.")
            elif 'grilled' in method:
                instructions.append(f"{i}. Grill {name} for 4-5 minutes per side.")
            elif 'steamed' in method:
                instructions.append(f"{i}. Steam {name} for 3-4 minutes.")
            elif 'scrambled' in method:
                instructions.append(f"{i}. Scramble {name} in a pan with a little oil.")
            elif 'sautéed' in method:
                instructions.append(f"{i}. Sauté {name} in a pan for 2-3 minutes.")
            elif 'drizzle' in method:
                instructions.append(f"{i}. Drizzle {name} over the dish.")
            elif 'sliced' in method:
                instructions.append(f"{i}. Slice {name} and add to the dish.")
            elif 'cubed' in method:
                instructions.append(f"{i}. Cube {name} and add to the dish.")
            else:
                instructions.append(f"{i}. Prepare {name} using {method} method.")
        else:
            instructions.append(f"{i}. Add {name} to the dish.")
    
    return " ".join(instructions)


def generate_shopping_list(daily_meals: Dict) -> Dict[str, List[str]]:
    """Generate a categorized shopping list from meal plan"""
    shopping_list = {
        "Proteins": [],
        "Grains & Carbs": [],
        "Vegetables": [],
        "Fruits": [],
        "Dairy": [],
        "Fats & Oils": [],
        "Nuts & Seeds": [],
        "Other": []
    }
    
    # Food categorization
    protein_foods = ["chicken", "salmon", "tofu", "lentils", "eggs", "greek yogurt", "fish", "beef", "pork"]
    grain_foods = ["brown rice", "quinoa", "oats", "bread", "pasta", "rice"]
    vegetable_foods = ["broccoli", "spinach", "tomato", "carrots", "bell pepper", "onion", "garlic"]
    fruit_foods = ["banana", "apple", "berries", "orange", "grape"]
    dairy_foods = ["milk", "cheese", "yogurt", "butter"]
    fat_foods = ["olive oil", "coconut oil", "avocado"]
    nut_foods = ["almonds", "walnuts", "chia seeds", "flax seeds"]
    
    for day_meals in daily_meals.values():
        for meal in day_meals.values():
            for ing in meal.get("ingredients", []):
                name = ing.get('name', '').lower()
                amount = ing.get('grams', ing.get('amount', ''))
                
                if amount:
                    item = f"{name.title()} ({amount}g)"
                else:
                    item = name.title()
                
                # Categorize the ingredient
                if any(p in name for p in protein_foods):
                    if item not in shopping_list["Proteins"]:
                        shopping_list["Proteins"].append(item)
                elif any(g in name for g in grain_foods):
                    if item not in shopping_list["Grains & Carbs"]:
                        shopping_list["Grains & Carbs"].append(item)
                elif any(v in name for v in vegetable_foods):
                    if item not in shopping_list["Vegetables"]:
                        shopping_list["Vegetables"].append(item)
                elif any(f in name for f in fruit_foods):
                    if item not in shopping_list["Fruits"]:
                        shopping_list["Fruits"].append(item)
                elif any(d in name for d in dairy_foods):
                    if item not in shopping_list["Dairy"]:
                        shopping_list["Dairy"].append(item)
                elif any(f in name for f in fat_foods):
                    if item not in shopping_list["Fats & Oils"]:
                        shopping_list["Fats & Oils"].append(item)
                elif any(n in name for n in nut_foods):
                    if item not in shopping_list["Nuts & Seeds"]:
                        shopping_list["Nuts & Seeds"].append(item)
                else:
                    if item not in shopping_list["Other"]:
                        shopping_list["Other"].append(item)
    
    # Remove empty categories
    return {k: v for k, v in shopping_list.items() if v}


def save_profile_to_excel(profile: Dict[str, Any], plan: Dict[str, Any], analysis: Dict[str, Any]) -> str:
    """Save profile, meal plan, and analysis to Excel file"""
    try:
        # Create data directory if it doesn't exist
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data_dir}/profile_{profile.get('name', 'user')}_{timestamp}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Profile sheet
            profile_data = {
                'Field': ['Name', 'Age', 'Gender', 'Height (cm)', 'Weight (kg)', 'Activity Level', 
                         'Goal', 'Cuisine Preference', 'Budget Level', 'Country', 'Dietary Preferences',
                         'Allergies', 'Intolerances', 'Disliked Foods', 'Avoid Ingredients'],
                'Value': [
                    profile.get('name', ''),
                    profile.get('age', ''),
                    profile.get('gender', ''),
                    profile.get('height_cm', ''),
                    profile.get('weight_kg', ''),
                    profile.get('activity_level', ''),
                    profile.get('goal_type', ''),
                    profile.get('cuisine_preference', ''),
                    profile.get('budget_level', ''),
                    profile.get('country', ''),
                    ', '.join(profile.get('dietary_preferences', [])),
                    ', '.join(profile.get('allergies', [])),
                    ', '.join(profile.get('intolerances', [])),
                    ', '.join(profile.get('disliked_foods', [])),
                    ', '.join(profile.get('avoid_ingredients', []))
                ]
            }
            profile_df = pd.DataFrame(profile_data)
            profile_df.to_excel(writer, sheet_name='Profile', index=False)
            
            # Meal plan sheet
            meal_data = []
            daily_meals = plan.get('daily_meals', {})
            for day_key, meals in daily_meals.items():
                for meal_type, meal in meals.items():
                    meal_data.append({
                        'Day': day_key.replace('_', ' ').title(),
                        'Meal Type': meal_type.replace('_', ' ').title(),
                        'Dish Name': meal.get('name', ''),
                        'Calories': meal.get('calories', 0),
                        'Protein (g)': meal.get('protein_g', 0),
                        'Carbs (g)': meal.get('carbs_g', 0),
                        'Fats (g)': meal.get('fats_g', 0),
                        'Ingredients': ', '.join([ing.get('name', '') for ing in meal.get('ingredients', [])]),
                        'Instructions': meal.get('instructions', '')
                    })
            
            if meal_data:
                meal_df = pd.DataFrame(meal_data)
                meal_df.to_excel(writer, sheet_name='Meal Plan', index=False)
            
            # Analysis sheet
            analysis_data = []
            daily_summary = analysis.get('daily', {}).get('summary', {})
            if daily_summary:
                analysis_data.append({
                    'Metric': 'Average Daily Calories',
                    'Value': daily_summary.get('avg_calories', 0),
                    'Unit': 'kcal'
                })
                analysis_data.append({
                    'Metric': 'Average Daily Protein',
                    'Value': daily_summary.get('avg_protein_g', 0),
                    'Unit': 'g'
                })
                analysis_data.append({
                    'Metric': 'Average Daily Carbohydrates',
                    'Value': daily_summary.get('avg_carbs_g', 0),
                    'Unit': 'g'
                })
                analysis_data.append({
                    'Metric': 'Average Daily Fats',
                    'Value': daily_summary.get('avg_fats_g', 0),
                    'Unit': 'g'
                })
            
            cost_data = analysis.get('cost', {})
            if cost_data:
                analysis_data.append({
                    'Metric': 'Average Daily Cost',
                    'Value': cost_data.get('average_cost_per_day', 0),
                    'Unit': 'USD'
                })
            
            sustainability_data = analysis.get('sustainability', {})
            if sustainability_data:
                analysis_data.append({
                    'Metric': 'Average Daily CO2 Emissions',
                    'Value': sustainability_data.get('average_kg_co2e_per_day', 0),
                    'Unit': 'kg'
                })
            
            if analysis_data:
                analysis_df = pd.DataFrame(analysis_data)
                analysis_df.to_excel(writer, sheet_name='Analysis', index=False)
            
            # Shopping list sheet
            shopping_list = generate_shopping_list(daily_meals)
            shopping_data = []
            for category, items in shopping_list.items():
                if items:
                    for item in items:
                        shopping_data.append({
                            'Category': category,
                            'Item': item
                        })
            
            if shopping_data:
                shopping_df = pd.DataFrame(shopping_data)
                shopping_df.to_excel(writer, sheet_name='Shopping List', index=False)
        
        return filename
    except Exception as e:
        st.error(f"Error saving to Excel: {str(e)}")
        return None


def load_profiles_from_excel() -> Dict[str, Any]:
    """Load all saved profiles from Excel files"""
    profiles = {}
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        return profiles
    
    try:
        for filename in os.listdir(data_dir):
            if filename.startswith("profile_") and filename.endswith(".xlsx"):
                filepath = os.path.join(data_dir, filename)
                try:
                    # Read profile sheet
                    profile_df = pd.read_excel(filepath, sheet_name='Profile')
                    profile_data = {}
                    for _, row in profile_df.iterrows():
                        field = row['Field']
                        value = row['Value']
                        
                        if field in ['Dietary Preferences', 'Allergies', 'Intolerances', 'Disliked Foods', 'Avoid Ingredients']:
                            profile_data[field.lower().replace(' ', '_')] = [x.strip() for x in str(value).split(',') if x.strip()] if value else []
                        elif field in ['Age', 'Height (cm)', 'Weight (kg)']:
                            profile_data[field.lower().replace(' ', '_').replace('(', '').replace(')', '')] = int(value) if value else 0
                        else:
                            key = field.lower().replace(' ', '_').replace('(', '').replace(')', '')
                            profile_data[key] = value
                    
                    # Extract profile name from filename
                    profile_name = filename.replace("profile_", "").replace(".xlsx", "").split("_")[0]
                    profiles[profile_name] = profile_data
                    
                except Exception as e:
                    st.warning(f"Could not load profile from {filename}: {str(e)}")
                    continue
    except Exception as e:
        st.error(f"Error loading profiles: {str(e)}")
    
    return profiles


def init_session():
    if "system" not in st.session_state:
        st.session_state.system = A2ADietitianOrchestrator()
    if "state" not in st.session_state:
        st.session_state.state = SystemState()
    if "plan" not in st.session_state:
        st.session_state.plan = {}
    if "analysis" not in st.session_state:
        st.session_state.analysis = {}
    if "events" not in st.session_state:
        st.session_state.events = []
    if "safety" not in st.session_state:
        st.session_state.safety = []


def profile_form() -> Dict[str, Any]:
    # Profile management section
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    st.markdown("### Profile Management")
    
    # Load existing profiles
    if "saved_profiles" not in st.session_state:
        st.session_state.saved_profiles = {}
    
    # Load profiles from Excel
    excel_profiles = load_profiles_from_excel()
    all_profiles = {**st.session_state.saved_profiles, **excel_profiles}
    
    # Profile selection
    if all_profiles:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            selected_profile = st.selectbox(
                "Load Existing Profile:",
                ["Create New Profile"] + list(all_profiles.keys()),
                help="Select an existing profile or create a new one"
            )
        with col2:
            if st.button("Load Profile", type="secondary"):
                if selected_profile != "Create New Profile":
                    profile_data = all_profiles[selected_profile]
                    # Update form fields with loaded profile data
                    st.session_state.loaded_profile = profile_data
                    st.success(f"Profile '{selected_profile}' loaded!")
                    st.rerun()
        with col3:
            if st.button("Delete Profile", type="secondary"):
                if selected_profile != "Create New Profile":
                    # Delete from session state
                    if selected_profile in st.session_state.saved_profiles:
                        del st.session_state.saved_profiles[selected_profile]
                    # Delete Excel file
                    data_dir = "data"
                    for filename in os.listdir(data_dir):
                        if filename.startswith(f"profile_{selected_profile}_") and filename.endswith(".xlsx"):
                            os.remove(os.path.join(data_dir, filename))
                            break
                    st.success(f"Profile '{selected_profile}' deleted!")
                    st.rerun()
    
    # Display saved profiles section
    if all_profiles:
        st.markdown('<div class="interactive-card">', unsafe_allow_html=True)
        st.markdown('<h4 class="section-header">Saved Profiles</h4>', unsafe_allow_html=True)
        for profile_name, profile_data in all_profiles.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{profile_name}** - {profile_data.get('age', 'N/A')} years, {profile_data.get('gender', 'N/A')}")
            with col2:
                st.write(f"Goal: {profile_data.get('goal_type', 'N/A')}")
            with col3:
                st.write(f"Budget: {profile_data.get('budget_level', 'N/A')}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### Personal Information")
    with st.form("profile_form", clear_on_submit=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Basic Info**")
            name = st.text_input("Name", value="User", help="Your name for personalization")
            age = st.number_input("Age", 1, 120, 28, help="Your age in years")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=2, help="For accurate nutritional calculations")
            
        with col2:
            st.markdown("**Physical Stats**")
            height = st.number_input("Height (cm)", 100, 250, 175, help="Your height in centimeters")
            weight = st.number_input("Weight (kg)", 30, 300, 70, help="Your current weight in kilograms")
            activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"], index=2, help="Your daily activity level")
            
        with col3:
            st.markdown("**Goals & Preferences**")
            goal = st.selectbox("Primary Goal", ["weight_loss", "muscle_gain", "maintenance", "performance"], index=2, help="Your main health goal")
            cuisine = st.selectbox("Cuisine Preference", [
                "International", "Mediterranean", "Asian", "Mexican", "Italian", 
                "Indian", "Middle Eastern", "American", "French", "Thai", "Japanese"
            ], index=0, help="Preferred cuisine style")
            budget = st.selectbox("Budget Level", ["low", "medium", "high"], index=1, help="Your food budget range")
        
        st.markdown("**Dietary Information**")
        col4, col5 = st.columns(2)
        with col4:
            dietary_options = st.multiselect(
                "Dietary Preferences",
                ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Keto", "Paleo", 
                 "Low-Carb", "High-Protein", "Mediterranean", "Whole30", "Pescatarian"],
                help="Select all that apply"
            )
            dietary = ", ".join(dietary_options)
            
            allergy_options = st.multiselect(
                "Allergies",
                ["Nuts", "Shellfish", "Dairy", "Eggs", "Soy", "Wheat", "Fish", "Sesame"],
                help="Select all that apply"
            )
            allergies = ", ".join(allergy_options)
            
            intolerance_options = st.multiselect(
                "Intolerances",
                ["Lactose", "Gluten", "FODMAPs", "Histamine", "Sulfites", "MSG"],
                help="Select all that apply"
            )
            intolerances = ", ".join(intolerance_options)
        
        with col5:
            disliked_options = st.multiselect(
                "Disliked Foods",
                ["Mushrooms", "Olives", "Anchovies", "Blue Cheese", "Liver", "Brussels Sprouts", 
                 "Beets", "Cilantro", "Black Licorice", "Raw Onions"],
                help="Select foods you don't like"
            )
            disliked = ", ".join(disliked_options)
            
            avoid_options = st.multiselect(
                "Avoid Ingredients",
                ["Artificial Sweeteners", "High Fructose Corn Syrup", "Trans Fats", "MSG", 
                 "Artificial Colors", "Preservatives", "Sodium Nitrate"],
                help="Select ingredients to avoid"
            )
            avoid = ", ".join(avoid_options)
            
            country = st.selectbox(
                "Country/Region",
                ["United States", "Canada", "United Kingdom", "Australia", "Germany", "France", 
                 "Italy", "Spain", "Japan", "India", "Brazil", "Mexico", "Other"],
                index=0, help="Your location for regional food preferences"
            )

        col6, col7 = st.columns([1, 1])
        with col6:
            submitted = st.form_submit_button("Save Profile", use_container_width=True, type="primary")
        with col7:
            save_as_new = st.form_submit_button("Save as New Profile", use_container_width=True, type="secondary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if submitted or save_as_new:
        profile = {
            "name": name,
            "age": int(age),
            "gender": gender,
            "height_cm": int(height),
            "weight_kg": float(weight),
            "activity_level": activity,
            "goal_type": goal,
            "dietary_preferences": [x.strip() for x in dietary.split(',') if x.strip()],
            "allergies": [x.strip() for x in allergies.split(',') if x.strip()],
            "intolerances": [x.strip() for x in intolerances.split(',') if x.strip()],
            "disliked_foods": [x.strip() for x in disliked.split(',') if x.strip()],
            "avoid_ingredients": [x.strip() for x in avoid.split(',') if x.strip()],
            "cuisine_preference": cuisine,
            "budget_level": budget,
            "country": country,
        }
        
        if save_as_new:
            profile_name = st.text_input("Enter profile name:", value=f"{name}'s Profile")
            if profile_name:
                st.session_state.saved_profiles[profile_name] = profile
                st.success(f"Profile '{profile_name}' saved successfully!")
        
        st.session_state.state.profile = profile
        st.success("Profile saved.")
    
    # Add Excel save button if meal plan exists
    if st.session_state.plan and st.session_state.analysis:
        st.markdown('<div class="interactive-card">', unsafe_allow_html=True)
        st.markdown('<h4 class="section-header">Save Complete Profile to Excel</h4>', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("Save your complete profile, meal plan, and analysis to an Excel file for future reference.")
        with col2:
            if st.button("Save to Excel", type="primary"):
                profile = st.session_state.state.profile if hasattr(st.session_state.state, 'profile') else st.session_state.state.get('profile', {})
                if profile:
                    filename = save_profile_to_excel(profile, st.session_state.plan, st.session_state.analysis)
                    if filename:
                        st.success(f"Complete profile saved to: {filename}")
                        # Provide download link
                        with open(filename, 'rb') as f:
                            st.download_button(
                                label="Download Excel File",
                                data=f.read(),
                                file_name=os.path.basename(filename),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                else:
                    st.error("Please save your profile first.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Safe access to profile with fallback
    if hasattr(st.session_state.state, 'profile'):
        return st.session_state.state.profile
    elif isinstance(st.session_state.state, dict):
        return st.session_state.state.get('profile', {})
    else:
        return {}


def run_flow():
    system = st.session_state.system
    state = st.session_state.state
    with st.spinner("Running AI Dietitian Pro flow..."):
        if _HAS_LANGGRAPH and build_ai_dietitian_graph is not None:
            graph = build_ai_dietitian_graph(system)
            app = graph.compile()
            result = app.invoke(state)
        else:
            # Fallback to internal sequential flow if LangGraph is unavailable
            result = system.run_flow(state)
    
    # Handle both SystemState object and dictionary cases
    if hasattr(result, 'plan'):
        # result is a SystemState object
        st.session_state.state = result
        st.session_state.plan = result.plan
        st.session_state.analysis = result.analysis_results
        st.session_state.events = result.events
        st.session_state.safety = result.safety_flags
    else:
        # result is a dictionary (from LangGraph)
        st.session_state.state = result
        st.session_state.plan = result.get('plan', {})
        st.session_state.analysis = result.get('analysis_results', {})
        st.session_state.events = result.get('events', [])
        st.session_state.safety = result.get('safety_flags', [])
    
    st.success("Flow completed.")


def render_meal_plan():
    plan = st.session_state.plan
    if not plan:
        st.info("No meal plan generated yet. Please run the flow first.")
        return
    
    # Interactive header with regenerate button
    st.markdown('<div class="interactive-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h2 class="interactive-heading">Your Personalized Meal Plan</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("Regenerate Plan", help="Generate a new meal plan with different recipes", type="secondary"):
            # Add a random seed to force variety
            import random
            st.session_state.regenerate_seed = random.randint(1, 1000)
            run_flow()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Daily nutrition summary with interactive metrics
    st.markdown('<div class="interactive-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">Daily Nutritional Summary</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Daily Calories", f"{plan.get('total_calories', 0):.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Protein (g)", f"{plan.get('total_protein', 0):.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Carbs (g)", f"{plan.get('total_carbs', 0):.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Fats (g)", f"{plan.get('total_fats', 0):.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()
    
    # Export options
    st.subheader("Export Options")
    col1, col2, col3 = st.columns(3)
    with col1:
        include_recipes = st.checkbox("Include Recipe Instructions", value=True)
    with col2:
        include_nutrition = st.checkbox("Include Nutrition Facts", value=True)
    with col3:
        include_shopping = st.checkbox("Include Shopping List", value=False)
    
    if "daily_meals" in plan:
        for idx, (day, meals) in enumerate(plan["daily_meals"].items()):
            day_name = day.replace('_', ' ').title()
            with st.expander(f"{day_name}", expanded=idx < 2):
                for meal_type, meal in meals.items():
                    meal_name = meal_type.replace('_', ' ').title()
                    
                    # Meal header with nutrition
                    st.markdown(f"### **{meal_name}** — {meal.get('name','')}")
                    
                    # Nutrition metrics
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Calories", f"{meal.get('calories', 0):.0f} kcal")
                    c2.metric("Protein", f"{meal.get('protein_g', 0):.1f} g")
                    c3.metric("Carbs", f"{meal.get('carbs_g', 0):.1f} g")
                    c4.metric("Fats", f"{meal.get('fats_g', 0):.1f} g")
                    
                    # Ingredients list
                    if meal.get("ingredients"):
                        st.markdown("**Ingredients:**")
                        for ing in meal["ingredients"]:
                            amount = ing.get('amount', ing.get('grams', ''))
                            method = ing.get('method', '')
                            if amount and method:
                                st.write(f"• **{ing.get('name','')}** — {amount}g ({method})")
                            elif amount:
                                st.write(f"• **{ing.get('name','')}** — {amount}g")
                            else:
                                st.write(f"• **{ing.get('name','')}**")
                    
                    # Recipe instructions (if available)
                    if include_recipes and meal.get("instructions"):
                        st.markdown("**Instructions:**")
                        st.write(meal["instructions"])
                    elif include_recipes:
                        # Generate simple instructions based on ingredients
                        instructions = generate_simple_instructions(meal.get("ingredients", []))
                        if instructions:
                            st.markdown("**Instructions:**")
                            st.write(instructions)
                    
                st.divider()
    
    # Shopping list
    if include_shopping and "daily_meals" in plan:
        st.subheader("Shopping List")
        shopping_list = generate_shopping_list(plan["daily_meals"])
        for category, items in shopping_list.items():
            st.markdown(f"**{category}:**")
            for item in items:
                st.write(f"• {item}")
            st.write("")


def render_analysis():
    a = st.session_state.analysis
    if not a:
        st.info("No analysis available yet. Please generate a meal plan first.")
        return
    
    st.subheader("Nutritional Analysis Summary")
    
    # Daily Averages Section
    daily = a.get("daily", {}).get("summary", {})
    if daily:
        st.markdown("### Daily Nutritional Averages")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average Calories", f"{round(daily.get('avg_calories', 0), 0)} kcal")
        with col2:
            st.metric("Average Protein", f"{round(daily.get('avg_protein_g', 0), 1)} g")
        with col3:
            st.metric("Average Carbs", f"{round(daily.get('avg_carbs_g', 0), 1)} g")
        with col4:
            st.metric("Average Fats", f"{round(daily.get('avg_fats_g', 0), 1)} g")
    
    st.divider()
    
    # Progress, Cost, and Sustainability Section
    st.markdown("### Progress & Impact Analysis")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        progress_data = a.get("progress", {})
        trend = progress_data.get("trend", "stable")
        calorie_delta = progress_data.get("avg_calorie_delta", 0)
        
        st.markdown("**Progress Trend**")
        if trend == "likely_weight_loss":
            st.success("Weight Loss Trend")
            st.caption(f"Calorie deficit: {round(calorie_delta, 0)} kcal")
        elif trend == "likely_weight_gain":
            st.warning("Weight Gain Trend")
            st.caption(f"Calorie surplus: {round(calorie_delta, 0)} kcal")
        else:
            st.info("Maintenance Trend")
            st.caption("Balanced calorie intake")
    
    with col2:
        cost_data = a.get("cost", {})
        avg_cost = cost_data.get("average_cost_per_day", 0)
        
        st.markdown("**Cost Analysis**")
        st.metric("Daily Food Cost", f"${round(avg_cost, 2)}")
        st.caption("Estimated cost per day")
    
    with col3:
        sustainability_data = a.get("sustainability", {})
        co2_emissions = sustainability_data.get("average_kg_co2e_per_day", 0)
        
        st.markdown("**Environmental Impact**")
        st.metric("CO2 Emissions", f"{round(co2_emissions, 2)} kg/day")
        st.caption("Carbon footprint estimate")
    
    st.divider()
    
    # Meal Findings Section
    meal_data = a.get("meal", {})
    findings = meal_data.get("findings", {})
    
    if findings:
        st.markdown("### Meal Analysis Findings")
        
        # Convert findings to readable format
        if isinstance(findings, dict):
            for category, details in findings.items():
                st.markdown(f"**{category.replace('_', ' ').title()}:**")
                if isinstance(details, dict):
                    for key, value in details.items():
                        st.write(f"• {key.replace('_', ' ').title()}: {value}")
                elif isinstance(details, list):
                    for item in details:
                        st.write(f"• {item}")
                else:
                    st.write(f"• {details}")
        else:
            st.write(findings)
    else:
        st.info("No specific meal findings available.")


def render_safety():
    flags = st.session_state.safety
    if not flags:
        st.success("No safety alerts detected. Your meal plan is safe!")
        return
    
    st.subheader("Safety Alerts & Recommendations")
    
    # Group alerts by type for better organization
    critical_alerts = []
    warning_alerts = []
    info_alerts = []
    
    for item in flags:
        if isinstance(item, str):
            # Simple string alerts
            if any(keyword in item.lower() for keyword in ['allergy', 'intolerance', 'dangerous', 'unsafe']):
                critical_alerts.append(item)
            elif any(keyword in item.lower() for keyword in ['low', 'high', 'excessive', 'deficient']):
                warning_alerts.append(item)
            else:
                info_alerts.append(item)
        elif isinstance(item, dict):
            # Dictionary alerts - convert to readable format
            alert_text = format_safety_alert(item)
            if any(keyword in alert_text.lower() for keyword in ['allergy', 'intolerance', 'dangerous', 'unsafe']):
                critical_alerts.append(alert_text)
            elif any(keyword in alert_text.lower() for keyword in ['low', 'high', 'excessive', 'deficient']):
                warning_alerts.append(alert_text)
            else:
                info_alerts.append(alert_text)
    
    # Display alerts by priority
    if critical_alerts:
        st.markdown("### Critical Alerts")
        for alert in critical_alerts:
            st.error(f"⚠️ {alert}")
    
    if warning_alerts:
        st.markdown("### Warnings")
        for alert in warning_alerts:
            st.warning(f"⚠️ {alert}")
    
    if info_alerts:
        st.markdown("### Information")
        for alert in info_alerts:
            st.info(f"ℹ️ {alert}")


def format_safety_alert(alert_dict):
    """Convert safety alert dictionary to readable text"""
    if isinstance(alert_dict, str):
        return alert_dict
    
    # Handle different alert formats
    if 'day' in alert_dict and 'meal' in alert_dict:
        day = alert_dict.get('day', 'Unknown day')
        meal = alert_dict.get('meal', 'Unknown meal')
        issue = alert_dict.get('issue', 'Safety concern detected')
        return f"{day} - {meal}: {issue}"
    elif 'type' in alert_dict and 'message' in alert_dict:
        return f"{alert_dict['type']}: {alert_dict['message']}"
    else:
        # Fallback: convert dict to readable text
        return " | ".join([f"{k}: {v}" for k, v in alert_dict.items()])


def render_events():
    events = st.session_state.events
    if not events:
        st.info("No system events recorded yet. Generate a meal plan to see activity logs.")
        return
    
    st.subheader("System Activity Log")
    st.caption("Timeline of system actions and user interactions")
    
    # Group events by topic for better organization
    event_groups = {}
    for event in events:
        topic = event.get("topic", "general")
        if topic not in event_groups:
            event_groups[topic] = []
        event_groups[topic].append(event)
    
    # Display events in chronological order with readable format
    for topic, topic_events in event_groups.items():
        topic_name = topic.replace('_', ' ').title()
        
        with st.expander(f"{topic_name} ({len(topic_events)} events)", expanded=False):
            for i, event in enumerate(topic_events):
                st.markdown(f"**Event {i+1}:** {format_event_summary(event)}")
                
                # Show detailed payload if available
                payload = event.get("payload", {})
                if payload and isinstance(payload, dict):
                    st.markdown("*Details:*")
                    for key, value in payload.items():
                        if isinstance(value, (dict, list)) and len(str(value)) > 100:
                            # Collapse large data structures
                            with st.expander(f"{key.replace('_', ' ').title()}", expanded=False):
                                st.json(value)
                        else:
                            st.write(f"• **{key.replace('_', ' ').title()}:** {value}")
                elif payload:
                    st.write(f"• **Data:** {payload}")
                
                if i < len(topic_events) - 1:
                    st.divider()


def format_event_summary(event):
    """Convert event to readable summary"""
    topic = event.get("topic", "unknown")
    payload = event.get("payload", {})
    
    # Create readable summaries based on event type
    if topic == "preference":
        return "User preferences processed and updated"
    elif topic == "goal":
        return "Nutritional goals analyzed and set"
    elif topic == "food_knowledge":
        return "Meal suggestions generated based on preferences"
    elif topic == "safety":
        return "Safety check completed for meal plan"
    elif topic == "analysis":
        return "Nutritional analysis performed"
    elif topic == "adaptation":
        return "Meal plan adaptations applied"
    elif topic == "emergency":
        return "Emergency risk assessment completed"
    else:
        # Generic summary
        if isinstance(payload, dict):
            if "status" in payload:
                return f"System action completed: {payload['status']}"
            elif "message" in payload:
                return payload["message"]
            else:
                return f"{topic.replace('_', ' ').title()} event processed"
        else:
            return f"{topic.replace('_', ' ').title()} event processed"


def render_downloads():
    plan = st.session_state.plan
    analysis = st.session_state.analysis
    if not plan:
        return
    
    st.subheader("Download Your Meal Plan")
    
    # Export customization options
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("**Export Options:**")
        include_recipes_export = st.checkbox("Include Recipe Instructions", value=True, key="export_recipes")
        include_nutrition_export = st.checkbox("Include Nutrition Facts", value=True, key="export_nutrition")
        include_shopping_export = st.checkbox("Include Shopping List", value=False, key="export_shopping")
        include_analysis_export = st.checkbox("Include Analysis Results", value=True, key="export_analysis")
    
    with col2:
        st.markdown("**File Format:**")
        export_format = st.selectbox(
            "Choose format:",
            ["PDF", "DOCX", "CSV"],
            help="PDF for printing, DOCX for editing, CSV for data analysis"
        )
    
    # Generate export data based on options
    export_data = {
        "plan": plan,
        "analysis": analysis if include_analysis_export else {},
        "include_recipes": include_recipes_export,
        "include_nutrition": include_nutrition_export,
        "include_shopping": include_shopping_export,
        "shopping_list": generate_shopping_list(plan.get("daily_meals", {})) if include_shopping_export else {}
    }
    
    # Download button
    if st.button(f"Download {export_format}", use_container_width=True, type="primary"):
        try:
            if export_format == "PDF":
                pdf_bytes = export_pdf(plan, analysis)
                st.download_button(
                    "Download PDF", 
                    data=pdf_bytes, 
                    file_name="ai_dietitian_meal_plan.pdf", 
                    mime="application/pdf", 
                    use_container_width=True
                )
            elif export_format == "DOCX":
                docx_bytes = export_docx(plan, analysis)
                st.download_button(
                    "Download DOCX", 
                    data=docx_bytes, 
                    file_name="ai_dietitian_meal_plan.docx", 
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                    use_container_width=True
                )
            elif export_format == "CSV":
                csv_bytes = export_csv(plan, analysis)
                st.download_button(
                    "Download CSV", 
                    data=csv_bytes, 
                    file_name="ai_dietitian_meal_plan.csv", 
                    mime="text/csv", 
                    use_container_width=True
                )
            st.success(f"{export_format} file ready for download!")
        except Exception as e:
            st.error(f"Error generating {export_format}: {str(e)}")
            st.info("Try a different format or check your meal plan data.")


def main():
    init_session()
    
    # Interactive header with custom styling
    st.markdown('<h1 class="interactive-title">AI Dietitian Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="interactive-subtitle">Personalized meal planning powered by artificial intelligence</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Create tabs with cleaner names
    tabs = st.tabs(["Dashboard", "Meal Plan", "Analysis", "Safety Alerts", "Event Log"]) 

    with tabs[0]:
        st.header("User Profile & System Control")
        st.caption("Complete your profile information and generate your personalized meal plan.")
        
        # Profile form
        profile = profile_form()
        
        # Run button with better layout
        st.markdown("### Generate Meal Plan")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Generate Meal Plan", use_container_width=True, type="primary"):
                if profile:
                    with st.spinner("Generating your personalized meal plan..."):
                        run_flow()
                else:
                    st.warning("Please complete and save your profile first.")
        
        st.markdown("---")
        render_downloads()

    with tabs[1]:
        st.header("Meal Plan")
        render_meal_plan()

    with tabs[2]:
        st.header("Nutritional Analysis")
        render_analysis()

    with tabs[3]:
        st.header("Safety Alerts")
        render_safety()

    with tabs[4]:
        st.header("System Events")
        render_events()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8em;'>"
        "NutriGuide - Advanced meal planning with AI agents | "
        "Built with Streamlit and Multi-Agent Architecture"
        "</div>", 
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()