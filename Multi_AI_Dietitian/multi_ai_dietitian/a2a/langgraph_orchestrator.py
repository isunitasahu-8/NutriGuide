from __future__ import annotations

from typing import Dict, Any, Callable

from langgraph.graph import StateGraph, END

from .protocol import SystemState, MessageType
from .orchestrator import A2ADietitianOrchestrator


def build_ai_dietitian_graph(system: A2ADietitianOrchestrator) -> StateGraph:
    graph = StateGraph(SystemState)

    def preference_node(state: SystemState) -> SystemState:
        resp = system.send_message(system.agents["preference_agent"].send_message(
            recipient="preference_agent", message_type=MessageType.PREFERENCE_UPDATE, content={"profile": state.profile}
        ))
        state.events.append({"topic": "preference", "payload": resp.content})
        return state

    def goal_node(state: SystemState) -> SystemState:
        resp = system.send_message(system.agents["goal_agent"].send_message(
            recipient="goal_agent", message_type=MessageType.GOAL_ANALYSIS, content={"profile": state.profile}
        ))
        state.goals = resp.content
        state.events.append({"topic": "goal", "payload": resp.content})
        return state

    def food_node(state: SystemState) -> SystemState:
        resp = system.send_message(system.agents["food_knowledge_agent"].send_message(
            recipient="food_knowledge_agent", message_type=MessageType.FOOD_SUGGESTION, content={"preferences": state.profile, "targets": state.goals.get("targets", {})}
        ))
        state.plan = resp.content
        state.events.append({"topic": "food_knowledge", "payload": resp.content})
        return state

    def safety_node(state: SystemState) -> SystemState:
        foods = []
        for _, meals in state.plan.get("daily_meals", {}).items():
            for meal in meals.values():
                for ing in meal.get("ingredients", []):
                    foods.append(ing.get("name", ""))
        resp = system.send_message(system.agents["restriction_safety_agent"].send_message(
            recipient="restriction_safety_agent", message_type=MessageType.SAFETY_CHECK, content={"foods": foods, "user_profile": state.profile}
        ))
        state.safety_flags = resp.content.get("warnings", [])
        state.events.append({"topic": "safety", "payload": resp.content})
        return state

    def analysis_meal_node(state: SystemState) -> SystemState:
        resp = system.send_message(system.agents["meal_analysis_agent"].send_message(
            recipient="meal_analysis_agent", message_type=MessageType.MEAL_ANALYSIS, content=state.plan
        ))
        state.analysis_results.setdefault("meal", resp.content)
        return state

    def analysis_daily_node(state: SystemState) -> SystemState:
        resp = system.send_message(system.agents["daily_nutrition_analysis_agent"].send_message(
            recipient="daily_nutrition_analysis_agent", message_type=MessageType.DAILY_NUTRITION_ANALYSIS, content=state.plan
        ))
        state.analysis_results.setdefault("daily", resp.content)
        return state

    def analysis_progress_cost_sustainability_node(state: SystemState) -> SystemState:
        daily = state.analysis_results.get("daily", {})
        pa = system.send_message(system.agents["progress_analysis_agent"].send_message(
            recipient="progress_analysis_agent", message_type=MessageType.PROGRESS_ANALYSIS, content={"days": daily.get("days", {}), "total_calories": state.plan.get("total_calories", 0)}
        ))
        ca = system.send_message(system.agents["cost_analysis_agent"].send_message(
            recipient="cost_analysis_agent", message_type=MessageType.COST_ANALYSIS, content=state.plan
        ))
        sa = system.send_message(system.agents["sustainability_analysis_agent"].send_message(
            recipient="sustainability_analysis_agent", message_type=MessageType.SUSTAINABILITY_CHECK, content=state.plan
        ))
        state.analysis_results.update({"progress": pa.content, "cost": ca.content, "sustainability": sa.content})
        state.events.append({"topic": "analysis", "payload": state.analysis_results})
        return state

    def adaptation_node(state: SystemState) -> SystemState:
        resp = system.send_message(system.agents["adaptation_agent"].send_message(
            recipient="adaptation_agent", message_type=MessageType.ADAPTATION_REQUEST, content={"current_plan": state.plan, "analysis": state.analysis_results, "safety": state.safety_flags}
        ))
        state.events.append({"topic": "adaptation", "payload": resp.content})
        return state

    def emergency_node(state: SystemState) -> SystemState:
        resp = system.send_message(system.agents["emergency_risk_agent"].send_message(
            recipient="emergency_risk_agent", message_type=MessageType.EMERGENCY_ALERT, content={"user_profile": state.profile, "health_data": {}}
        ))
        state.events.append({"topic": "emergency", "payload": resp.content})
        return state

    graph.add_node("preference", preference_node)
    graph.add_node("goal", goal_node)
    graph.add_node("food", food_node)
    graph.add_node("safety", safety_node)
    graph.add_node("analysis_meal", analysis_meal_node)
    graph.add_node("analysis_daily", analysis_daily_node)
    graph.add_node("analysis_pcs", analysis_progress_cost_sustainability_node)
    graph.add_node("adaptation", adaptation_node)
    graph.add_node("emergency", emergency_node)

    graph.set_entry_point("preference")
    graph.add_edge("preference", "goal")
    graph.add_edge("goal", "food")
    graph.add_edge("food", "safety")
    graph.add_edge("safety", "analysis_meal")
    graph.add_edge("analysis_meal", "analysis_daily")
    graph.add_edge("analysis_daily", "analysis_pcs")
    graph.add_edge("analysis_pcs", "adaptation")
    graph.add_edge("adaptation", "emergency")
    graph.add_edge("emergency", END)

    return graph


