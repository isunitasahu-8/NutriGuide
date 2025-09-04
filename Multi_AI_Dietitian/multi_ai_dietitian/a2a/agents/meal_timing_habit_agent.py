"""
Meal Timing & Habit Agent - The Scheduler

Designs optimal meal timings around lifestyle, workouts, and daily schedule.
"""

from typing import Dict, Any
from datetime import datetime

from ..protocol import Agent, A2AMessage, MessageType


class MealTimingHabitAgent(Agent):
    """The Scheduler - Designs meal timings around lifestyle"""
    
    def __init__(self):
        super().__init__("meal_timing_agent")
        self.timing_rules = {
            "workout_days": {
                "pre_workout": "2-3 hours before",
                "post_workout": "within 30 minutes",
                "protein_timing": "distribute throughout day"
            },
            "rest_days": {
                "breakfast": "within 1 hour of waking",
                "lunch": "4-5 hours after breakfast",
                "dinner": "2-3 hours before bed"
            }
        }
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.TIMING_SUGGESTION:
            return self._suggest_timing(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "meal_timing_agent"}
        )
    
    def _suggest_timing(self, message: A2AMessage) -> A2AMessage:
        """Suggest optimal meal timing based on schedule"""
        schedule = message.content.get("schedule", {})
        training_days = schedule.get("training_days", [])
        work_schedule = schedule.get("work_schedule", {})
        
        today = datetime.now().weekday()
        is_training_day = today in training_days
        
        if is_training_day:
            timing = {
                "breakfast": "7:00 AM - Protein + carbs",
                "pre_workout_snack": "5:00 PM - Light carbs",
                "post_workout": "7:30 PM - Protein + carbs",
                "dinner": "8:00 PM - Balanced meal"
            }
        else:
            timing = {
                "breakfast": "8:00 AM - Balanced meal",
                "lunch": "12:30 PM - Protein + vegetables",
                "snack": "3:30 PM - Fruit + nuts",
                "dinner": "7:00 PM - Light meal"
            }
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "meal_timing": timing,
                "is_training_day": is_training_day,
                "message": f"Meal timing optimized for {'training' if is_training_day else 'rest'} day"
            }
        )
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about meal timing"""
        return {
            "timing_scenarios": list(self.timing_rules.keys()),
            "workout_day_rules": len(self.timing_rules["workout_days"]),
            "rest_day_rules": len(self.timing_rules["rest_days"]),
            "total_timing_rules": sum(len(rules) for rules in self.timing_rules.values())
        }
