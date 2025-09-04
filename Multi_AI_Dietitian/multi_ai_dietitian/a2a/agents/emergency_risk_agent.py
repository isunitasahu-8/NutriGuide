"""
Emergency & Risk Agent - The Watchdog

Detects red flags and dangerous conditions requiring immediate attention.
"""

from typing import Dict, List, Any

from ..protocol import Agent, A2AMessage, MessageType


class EmergencyRiskAgent(Agent):
    """The Watchdog - Detects red flags and dangerous conditions"""
    
    def __init__(self):
        super().__init__("emergency_risk_agent")
        self.risk_thresholds = {
            "weight_loss_rate": {"dangerous": 2.0, "concerning": 1.0},  # kg/week
            "bmi": {"underweight": 18.5, "obese": 30.0},
            "blood_pressure": {"high": 140, "low": 90},
            "heart_rate": {"high": 100, "low": 60}
        }
        self.emergency_flags: List[Dict[str, Any]] = []
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.EMERGENCY_ALERT:
            return self._assess_risks(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "emergency_risk_agent"}
        )
    
    def _assess_risks(self, message: A2AMessage) -> A2AMessage:
        """Assess health risks and flag emergencies"""
        health_data = message.content.get("health_data", {})
        user_profile = message.content.get("user_profile", {})
        
        risks = []
        emergencies = []
        
        # Check weight loss rate
        if "weight_loss_rate" in health_data:
            wlr = health_data["weight_loss_rate"]
            try:
                wlr = float(wlr)
                if wlr > self.risk_thresholds["weight_loss_rate"]["dangerous"]:
                    emergencies.append("DANGEROUS WEIGHT LOSS - Consult healthcare provider immediately")
                elif wlr > self.risk_thresholds["weight_loss_rate"]["concerning"]:
                    risks.append("Rapid weight loss detected - consider slowing down")
            except (ValueError, TypeError):
                pass
        
        # Check BMI
        if "bmi" in health_data:
            bmi = health_data["bmi"]
            try:
                bmi = float(bmi)
                if bmi < self.risk_thresholds["bmi"]["underweight"]:
                    risks.append("Underweight BMI - consider increasing caloric intake")
                elif bmi > self.risk_thresholds["bmi"]["obese"]:
                    risks.append("High BMI - consider medical supervision for weight loss")
            except (ValueError, TypeError):
                pass
        
        # Check blood pressure
        if "blood_pressure" in health_data:
            bp = health_data["blood_pressure"]
            try:
                bp = float(bp)
                if bp > self.risk_thresholds["blood_pressure"]["high"]:
                    risks.append("High blood pressure - monitor closely")
                elif bp < self.risk_thresholds["blood_pressure"]["low"]:
                    risks.append("Low blood pressure - consider medical evaluation")
            except (ValueError, TypeError):
                pass
        
        # Check for extreme fatigue
        if "fatigue_level" in health_data:
            fatigue = health_data["fatigue_level"]
            if fatigue in ["extreme", "severe"]:
                emergencies.append("EXTREME FATIGUE - May indicate underlying health issue")
        
        # Check for supplement-drug interactions
        medications = user_profile.get("medications", [])
        supplements = health_data.get("supplements", [])
        
        for med in medications:
            for supp in supplements:
                if self._check_interaction(med, supp):
                    emergencies.append(f"SUPPLEMENT-DRUG INTERACTION: {supp} with {med}")
        
        # Record emergency flags
        if emergencies or risks:
            self.emergency_flags.append({
                "timestamp": message.timestamp,
                "emergencies": emergencies,
                "risks": risks,
                "user_id": user_profile.get("name", "unknown")
            })
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "emergencies": emergencies,
                "risks": risks,
                "requires_medical_attention": len(emergencies) > 0,
                "message": f"Risk assessment complete: {len(emergencies)} emergencies, {len(risks)} risks"
            }
        )
    
    def _check_interaction(self, medication: str, supplement: str) -> bool:
        """Check for known supplement-drug interactions"""
        known_interactions = {
            "warfarin": ["vitamin_k", "fish_oil", "garlic"],
            "statins": ["grapefruit", "red_yeast_rice"],
            "blood_pressure_meds": ["licorice", "garlic"],
            "diabetes_meds": ["chromium", "cinnamon"]
        }
        
        med_lower = medication.lower()
        supp_lower = supplement.lower()
        
        for med, supps in known_interactions.items():
            if med in med_lower:
                for supp in supps:
                    if supp in supp_lower:
                        return True
        
        return False
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about risk assessments"""
        return {
            "total_emergency_flags": len(self.emergency_flags),
            "risk_thresholds_configured": len(self.risk_thresholds),
            "latest_emergency": self.emergency_flags[-1]["timestamp"] if self.emergency_flags else None,
            "emergency_types": list(set([flag for flags in self.emergency_flags for flag in flags["emergencies"]]))
        }
