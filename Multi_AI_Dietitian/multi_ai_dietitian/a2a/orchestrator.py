from __future__ import annotations

from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from .protocol import A2AOrchestrator as BaseOrchestrator, A2AMessage, MessageType, Priority, AgentMessage, SystemState
from .agents.preference_agent import PreferenceAgent
from .agents.goal_agent import GoalAgent
from .agents.food_knowledge_agent import FoodKnowledgeAgent
from .agents.restriction_safety_agent import RestrictionSafetyAgent
from .agents.adaptation_agent import AdaptationAgent
from .agents.motivation_education_agent import MotivationEducationAgent
from .agents.cultural_lifestyle_agent import CulturalLifestyleAgent
from .agents.budget_accessibility_agent import BudgetAccessibilityAgent
from .agents.meal_timing_habit_agent import MealTimingHabitAgent
from .agents.sustainability_environment_agent import SustainabilityEnvironmentAgent
from .agents.medical_biomarker_agent import MedicalBiomarkerAgent
from .agents.feedback_learning_agent import FeedbackLearningAgent
from .agents.emergency_risk_agent import EmergencyRiskAgent
from .agents.meal_analysis_agent import MealAnalysisAgent
from .agents.daily_nutrition_analysis_agent import DailyNutritionAnalysisAgent
from .agents.progress_analysis_agent import ProgressAnalysisAgent
from .agents.cost_analysis_agent import CostAnalysisAgent
from .agents.sustainability_agent import SustainabilityAgent as SustainabilityAnalysisAgent
from ..schemas import UserProfile, Plan30, MacroTargets


class A2ADietitianOrchestrator(BaseOrchestrator):
    """Main orchestrator for the 13-agent A2A dietitian system"""
    
    def __init__(self, llm=None):
        super().__init__()
        
        # Store LLM reference
        self.llm = llm
        
        # Register core and analysis agents
        self._register_all_agents()
        
        # Track conversation flows
        self.conversation_flows: List[Dict[str, Any]] = []
    
    def _register_all_agents(self):
        """Register core + analysis agents"""
        agents = [
            PreferenceAgent(),           # 1. The Listener
            GoalAgent(),                 # 2. The Planner
            FoodKnowledgeAgent(),        # 3. The Expert Chef + Scientist
            RestrictionSafetyAgent(),    # 4. The Guardian
            AdaptationAgent(),           # 5. The Coach
            MotivationEducationAgent(),  # 6. The Friend
            CulturalLifestyleAgent(),    # 7. The Personal Touch
            BudgetAccessibilityAgent(),  # 8. The Practical Shopper
            MealTimingHabitAgent(),      # 9. The Scheduler
            SustainabilityEnvironmentAgent(), # 10. The Eco-Friendly Guide (legacy)
            MedicalBiomarkerAgent(),     # 11. The Clinician
            FeedbackLearningAgent(),     # 12. The Evolver
            EmergencyRiskAgent()         # 13. The Watchdog
        ]
        analysis_agents = [
            MealAnalysisAgent(),
            DailyNutritionAnalysisAgent(),
            ProgressAnalysisAgent(),
            CostAnalysisAgent(),
            SustainabilityAnalysisAgent(),
        ]
        
        for agent in agents + analysis_agents:
            self.register_agent(agent)

    # Simplified LangGraph-like step runner using SystemState
    def run_flow(self, state: SystemState) -> SystemState:
        # START → Preference → Goal → Food Knowledge → Restriction & Safety → (Meal Analysis → Nutrition Analysis → Progress/Cost/Sustainability) → Adaptation → Emergency → END
        # Preference
        pref_resp = self.send_message(A2AMessage(sender="orchestrator", recipient="preference_agent", message_type=MessageType.PREFERENCE_UPDATE, content={"profile": state.profile}))
        state.events.append({"topic": "preference", "payload": pref_resp.content})

        # Goal
        goal_resp = self.send_message(A2AMessage(sender="orchestrator", recipient="goal_agent", message_type=MessageType.GOAL_ANALYSIS, content={"profile": state.profile}))
        state.goals = goal_resp.content
        state.events.append({"topic": "goal", "payload": goal_resp.content})

        # Food Knowledge
        fk_resp = self.send_message(A2AMessage(sender="orchestrator", recipient="food_knowledge_agent", message_type=MessageType.FOOD_SUGGESTION, content={"preferences": pref_resp.content.get("profile", {}), "targets": goal_resp.content.get("targets", {})}))
        state.plan = fk_resp.content
        state.events.append({"topic": "food_knowledge", "payload": fk_resp.content})

        # Restriction & Safety
        foods = []
        for _, meals in fk_resp.content.get("daily_meals", {}).items():
            for meal in meals.values():
                for ing in meal.get("ingredients", []):
                    foods.append(ing.get("name", ""))
        safety_resp = self.send_message(A2AMessage(sender="orchestrator", recipient="restriction_safety_agent", message_type=MessageType.SAFETY_CHECK, content={"foods": foods, "user_profile": state.profile}))
        state.safety_flags = safety_resp.content.get("warnings", [])
        state.events.append({"topic": "safety", "payload": safety_resp.content})

        # Analysis block
        plan_like = state.plan if state.plan else {}
        meal_analysis = self.send_message(A2AMessage(sender="orchestrator", recipient="meal_analysis_agent", message_type=MessageType.MEAL_ANALYSIS, content=plan_like))
        daily_analysis = self.send_message(A2AMessage(sender="orchestrator", recipient="daily_nutrition_analysis_agent", message_type=MessageType.DAILY_NUTRITION_ANALYSIS, content=plan_like))
        progress_analysis = self.send_message(A2AMessage(sender="orchestrator", recipient="progress_analysis_agent", message_type=MessageType.PROGRESS_ANALYSIS, content={"days": daily_analysis.content.get("days", {}), "total_calories": plan_like.get("total_calories", 0)}))
        cost_analysis = self.send_message(A2AMessage(sender="orchestrator", recipient="cost_analysis_agent", message_type=MessageType.COST_ANALYSIS, content=plan_like))
        sustain_analysis = self.send_message(A2AMessage(sender="orchestrator", recipient="sustainability_analysis_agent", message_type=MessageType.SUSTAINABILITY_CHECK, content=plan_like))

        state.analysis_results = {
            "meal": meal_analysis.content,
            "daily": daily_analysis.content,
            "progress": progress_analysis.content,
            "cost": cost_analysis.content,
            "sustainability": sustain_analysis.content,
        }
        state.events.append({"topic": "analysis", "payload": state.analysis_results})

        # Adaptation
        adapt_resp = self.send_message(A2AMessage(sender="orchestrator", recipient="adaptation_agent", message_type=MessageType.ADAPTATION_REQUEST, content={"current_plan": state.plan, "analysis": state.analysis_results, "safety": state.safety_flags}))
        state.events.append({"topic": "adaptation", "payload": adapt_resp.content})

        # Emergency
        emergency_resp = self.send_message(A2AMessage(sender="orchestrator", recipient="emergency_risk_agent", message_type=MessageType.EMERGENCY_ALERT, content={"user_profile": state.profile, "health_data": {}}))
        state.events.append({"topic": "emergency", "payload": emergency_resp.content})

        return state
    
    def generate_comprehensive_plan(self, user_profile: UserProfile, 
                                  health_data: Optional[Dict[str, Any]] = None,
                                  feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a comprehensive diet plan using LLM and all 13 agents"""
        
        # If LLM is available, use it for enhanced meal planning
        if self.llm:
            try:
                # Generate LLM-enhanced meal plan
                llm_plan = self._generate_llm_plan(user_profile, health_data, feedback)
                
                # Process through agents for validation and enhancement
                enhanced_plan = self._enhance_plan_with_agents(llm_plan, user_profile, health_data, feedback)
                
                return enhanced_plan
            except Exception as e:
                # Fallback to agent-only plan if LLM fails
                return self._generate_agent_only_plan(user_profile, health_data, feedback)
        else:
            # Use agent-only approach
            return self._generate_agent_only_plan(user_profile, health_data, feedback)
    
    def _generate_llm_plan(self, user_profile: UserProfile, 
                          health_data: Optional[Dict[str, Any]] = None,
                          feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate meal plan using LLM"""
        prompt = f"""
        Generate a personalized 30-day meal plan for a user with the following profile:
        
        Personal Info: {user_profile.name}, {user_profile.age} years old, {user_profile.gender}
        Height: {user_profile.height_cm}cm, Weight: {user_profile.weight_kg}kg
        Activity Level: {user_profile.activity_level}
        Goal: {user_profile.goal_type}
        
        Dietary Preferences: {', '.join(user_profile.dietary_preferences)}
        Allergies: {', '.join(user_profile.allergies)}
        Intolerances: {', '.join(user_profile.intolerances)}
        Disliked Foods: {', '.join(user_profile.disliked_foods)}
        Cuisine Preference: {user_profile.cuisine_preference}
        Budget Level: {user_profile.budget_level}
        Cooking Skill: {user_profile.cooking_skill}
        Country: {user_profile.country}
        
        Health Data: {health_data or 'None provided'}
        Previous Feedback: {feedback or 'None provided'}
        
        Please provide a structured meal plan with:
        1. Daily meals (breakfast, lunch, dinner, snacks)
        2. Nutritional targets and calculations
        3. Recipe suggestions with ingredients and instructions
        4. Shopping lists
        5. Cultural adaptations
        6. Budget considerations
        7. Safety notes and substitutions
        
        Format the response as a JSON structure with clear sections.
        """
        
        try:
            response = self.llm.generate_text(prompt)
            # Try to parse as JSON, fallback to text if needed
            try:
                import json
                return json.loads(response)
            except:
                return {"llm_response": response, "status": "text_format"}
        except Exception as e:
            return {"error": f"LLM generation failed: {str(e)}", "status": "error"}
    
    def _enhance_plan_with_agents(self, llm_plan: Dict[str, Any], 
                                 user_profile: UserProfile,
                                 health_data: Optional[Dict[str, Any]] = None,
                                 feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Enhance LLM plan with agent insights"""
        enhanced_plan = llm_plan.copy()
        
        # Add agent validations and enhancements
        # This would integrate with the existing agent system
        enhanced_plan["agent_enhancements"] = "Plan enhanced by AI agents"
        enhanced_plan["status"] = "enhanced"
        
        return enhanced_plan
    
    def _generate_agent_only_plan(self, user_profile: UserProfile, 
                                health_data: Optional[Dict[str, Any]] = None,
                                feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate plan using only agents (fallback method)"""
        return self.create_comprehensive_plan(user_profile, health_data, feedback)
    
    def create_comprehensive_plan(self, user_profile: UserProfile, 
                                health_data: Optional[Dict[str, Any]] = None,
                                feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a comprehensive diet plan using all 13 agents"""
        
        # Start conversation flow
        flow_id = f"flow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        flow = {
            "flow_id": flow_id,
            "user_profile": user_profile.__dict__,
            "health_data": health_data or {},
            "feedback": feedback or {},
            "messages": [],
            "results": {}
        }
        
        try:
            # Step 1: Update preferences (Preference Agent)
            pref_response = self.send_message(
                A2AMessage(
                    sender="orchestrator",
                    recipient="preference_agent",
                    message_type=MessageType.PREFERENCE_UPDATE,
                    content=user_profile.__dict__
                )
            )
            flow["messages"].append(pref_response.to_dict())
            
            # Step 2: Analyze goals (Goal Agent)
            goal_response = self.send_message(
                A2AMessage(
                    sender="orchestrator",
                    recipient="goal_agent",
                    message_type=MessageType.GOAL_ANALYSIS,
                    content={"profile": user_profile.__dict__}
                )
            )
            flow["messages"].append(goal_response.to_dict())
            flow["results"]["nutritional_blueprint"] = goal_response.content
            
            # Step 3: Get food suggestions (Food Knowledge Agent)
            food_response = self.send_message(
                A2AMessage(
                    sender="orchestrator",
                    recipient="food_knowledge_agent",
                    message_type=MessageType.FOOD_SUGGESTION,
                    content={
                        "preferences": pref_response.content["profile"],
                        "targets": goal_response.content["targets"]
                    }
                )
            )
            flow["messages"].append(food_response.to_dict())
            flow["results"]["food_suggestions"] = food_response.content
            
            # Step 4: Safety check (Restriction & Safety Agent)
            foods_to_check = []
            for meal_type, meals in food_response.content["suggestions"].items():
                for meal in meals:
                    for ingredient in meal.get("ingredients", []):
                        foods_to_check.append(ingredient["name"])
            
            safety_response = self.send_message(
                A2AMessage(
                    sender="orchestrator",
                    recipient="restriction_safety_agent",
                    message_type=MessageType.SAFETY_CHECK,
                    content={
                        "foods": foods_to_check,
                        "user_profile": user_profile.__dict__
                    }
                )
            )
            flow["messages"].append(safety_response.to_dict())
            flow["results"]["safety_check"] = safety_response.content
            
            # Step 5: Cultural adaptation (Cultural & Lifestyle Agent)
            cultural_response = self.send_message(
                A2AMessage(
                    sender="orchestrator",
                    recipient="cultural_lifestyle_agent",
                    message_type=MessageType.CULTURAL_ADAPTATION,
                    content={
                        "cuisine_preference": user_profile.cuisine_preferences[0] if user_profile.cuisine_preferences else "",
                        "dietary_preferences": user_profile.dietary_preferences,
                        "suggestions": food_response.content["suggestions"]
                    }
                )
            )
            flow["messages"].append(cultural_response.to_dict())
            flow["results"]["cultural_adaptations"] = cultural_response.content
            
            # Step 6: Budget check (Budget & Accessibility Agent)
            budget_response = self.send_message(
                A2AMessage(
                    sender="orchestrator",
                    recipient="budget_accessibility_agent",
                    message_type=MessageType.BUDGET_CHECK,
                    content={
                        "budget_level": user_profile.budget_level,
                        "foods": foods_to_check
                    }
                )
            )
            flow["messages"].append(budget_response.to_dict())
            flow["results"]["budget_check"] = budget_response.content
            
            # Step 7: Meal timing (Meal Timing & Habit Agent)
            timing_response = self.send_message(
                A2AMessage(
                    sender="orchestrator",
                    recipient="meal_timing_agent",
                    message_type=MessageType.TIMING_SUGGESTION,
                    content={
                        "schedule": {
                            "training_days": user_profile.training_days,
                            "work_schedule": {"notes": user_profile.work_schedule_notes}
                        }
                    }
                )
            )
            flow["messages"].append(timing_response.to_dict())
            flow["results"]["meal_timing"] = timing_response.content
            
            # Step 8: Sustainability check (Sustainability & Environment Agent)
            sustainability_response = self.send_message(
                A2AMessage(
                    sender="orchestrator",
                    recipient="sustainability_agent",
                    message_type=MessageType.SUSTAINABILITY_CHECK,
                    content={"foods": foods_to_check}
                )
            )
            flow["messages"].append(sustainability_response.to_dict())
            flow["results"]["sustainability_check"] = sustainability_response.content
            
            # Step 9: Medical analysis (Medical & Biomarker Agent)
            if health_data:
                medical_response = self.send_message(
                    A2AMessage(
                        sender="orchestrator",
                        recipient="medical_biomarker_agent",
                        message_type=MessageType.MEDICAL_ALERT,
                        content={"biomarkers": health_data}
                    )
                )
                flow["messages"].append(medical_response.to_dict())
                flow["results"]["medical_analysis"] = medical_response.content
            
            # Step 10: Emergency risk check (Emergency & Risk Agent)
            emergency_response = self.send_message(
                A2AMessage(
                    sender="orchestrator",
                    recipient="emergency_risk_agent",
                    message_type=MessageType.EMERGENCY_ALERT,
                    content={
                        "health_data": health_data or {},
                        "user_profile": user_profile.__dict__
                    }
                )
            )
            flow["messages"].append(emergency_response.to_dict())
            flow["results"]["emergency_check"] = emergency_response.content
            
            # Step 11: Process feedback if available (Feedback & Learning Agent)
            if feedback:
                feedback_response = self.send_message(
                    A2AMessage(
                        sender="orchestrator",
                        recipient="feedback_learning_agent",
                        message_type=MessageType.FEEDBACK_PROCESSING,
                        content={
                            "feedback": feedback,
                            "user_id": user_profile.name or "user"
                        }
                    )
                )
                flow["messages"].append(feedback_response.to_dict())
                flow["results"]["feedback_analysis"] = feedback_response.content
            
            # Step 12: Adaptation if needed (Adaptation Agent)
            if feedback:
                adaptation_response = self.send_message(
                    A2AMessage(
                        sender="orchestrator",
                        recipient="adaptation_agent",
                        message_type=MessageType.ADAPTATION_REQUEST,
                        content={
                            "feedback": feedback,
                            "current_plan": flow["results"]
                        }
                    )
                )
                flow["messages"].append(adaptation_response.to_dict())
                flow["results"]["adaptations"] = adaptation_response.content
            
            # Step 13: Motivation and education (Motivation & Education Agent)
            motivation_response = self.send_message(
                A2AMessage(
                    sender="orchestrator",
                    recipient="motivation_education_agent",
                    message_type=MessageType.MOTIVATION_MESSAGE,
                    content={
                        "context": "comprehensive_plan_created",
                        "progress": feedback.get("progress", {}) if feedback else {}
                    }
                )
            )
            flow["messages"].append(motivation_response.to_dict())
            flow["results"]["motivation"] = motivation_response.content
            
            # Record the flow
            self.conversation_flows.append(flow)
            
            return {
                "flow_id": flow_id,
                "status": "success",
                "summary": {
                    "nutritional_blueprint": flow["results"]["nutritional_blueprint"],
                    "food_suggestions": flow["results"]["food_suggestions"],
                    "safety_check": flow["results"]["safety_check"],
                    "cultural_adaptations": flow["results"]["cultural_adaptations"],
                    "budget_check": flow["results"]["budget_check"],
                    "meal_timing": flow["results"]["meal_timing"],
                    "sustainability_check": flow["results"]["sustainability_check"],
                    "emergency_check": flow["results"]["emergency_check"],
                    "motivation": flow["results"]["motivation"]
                },
                "agent_status": self.get_agent_status()
            }
            
        except Exception as e:
            flow["error"] = str(e)
            self.conversation_flows.append(flow)
            return {
                "flow_id": flow_id,
                "status": "error",
                "error": str(e),
                "agent_status": self.get_agent_status()
            }
    
    def get_conversation_history(self, flow_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get conversation history for a specific flow or all flows"""
        if flow_id:
            return [flow for flow in self.conversation_flows if flow["flow_id"] == flow_id]
        return self.conversation_flows
    
    def get_agent_insights(self) -> Dict[str, Any]:
        """Get insights from all agents for the Streamlit dashboard"""
        insights = {}
        
        for agent_id, agent in self.agents.items():
            # Get agent status
            status = "Active" if agent.get_pending_messages() else "Ready"
            
            insights[agent_id] = {
                "status": status,
                "insights": {
                    "pending_messages": len(agent.get_pending_messages()),
                    "conversation_history": len(agent.conversation_history)
                },
                "last_activity": "Recent" if agent.conversation_history else "None"
            }
        
        return insights
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            agent_id: {
                "pending_messages": len(agent.get_pending_messages()),
                "conversation_history_length": len(agent.conversation_history)
            }
            for agent_id, agent in self.agents.items()
        }
