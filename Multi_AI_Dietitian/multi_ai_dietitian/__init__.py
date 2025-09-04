"""
Multi-Agent AI Dietitian System

A professional multi-agent system for personalized nutrition planning.
"""

__version__ = "1.0.0"
__author__ = "AI Dietitian Team"

from .a2a.orchestrator import A2ADietitianOrchestrator
from .schemas import UserProfile, Plan30, MacroTargets

__all__ = [
    "A2ADietitianOrchestrator",
    "UserProfile", 
    "Plan30",
    "MacroTargets"
]
