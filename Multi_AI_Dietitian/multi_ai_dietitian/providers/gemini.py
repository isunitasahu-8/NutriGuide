"""
Gemini LLM provider for the Multi-Agent AI Dietitian System
"""

from typing import Dict, Any, Optional
import google.generativeai as genai


class GeminiLLM:
    """Gemini LLM provider implementation"""
    
    def __init__(self, api_key: str = ""):
        """Initialize Gemini LLM provider"""
        if api_key:
            genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Gemini"""
        try:
            response = self.model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            return f"Error generating text: {str(e)}"
    
    def generate_meal_plan(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate meal plan using Gemini"""
        prompt = f"""
        Generate a personalized meal plan for a user with the following profile:
        {user_profile}
        
        Please provide a structured meal plan with:
        1. Daily meals (breakfast, lunch, dinner, snacks)
        2. Nutritional targets
        3. Recipe suggestions
        4. Shopping list
        """
        
        try:
            response = self.model.generate_content(prompt)
            return {
                "meal_plan": response.text,
                "status": "success"
            }
        except Exception as e:
            return {
                "meal_plan": f"Error generating meal plan: {str(e)}",
                "status": "error"
            }
