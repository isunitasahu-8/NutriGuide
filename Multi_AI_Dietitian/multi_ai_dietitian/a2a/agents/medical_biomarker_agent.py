"""
Medical & Biomarker Agent - The Clinician

Integrates health data, medical history, and biomarker information.
"""

from typing import Dict, List, Any

from ..protocol import Agent, A2AMessage, MessageType


class MedicalBiomarkerAgent(Agent):
    """The Clinician - Integrates health data and medical history"""
    
    def __init__(self):
        super().__init__("medical_biomarker_agent")
        self.biomarker_ranges = {
            "blood_sugar": {"normal": (70, 100), "prediabetic": (100, 125), "diabetic": (126, 200)},
            "cholesterol": {"normal": (0, 200), "high": (200, 240), "very_high": (240, 300)},
            "vitamin_d": {"deficient": (0, 20), "insufficient": (20, 30), "sufficient": (30, 100)}
        }
    
    def process_message(self, message: A2AMessage) -> A2AMessage:
        """Process incoming messages based on message type"""
        if message.message_type == MessageType.MEDICAL_ALERT:
            return self._process_medical_data(message)
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {"status": "processed", "agent": "medical_biomarker_agent"}
        )
    
    def _process_medical_data(self, message: A2AMessage) -> A2AMessage:
        """Process medical data and provide recommendations"""
        biomarkers = message.content.get("biomarkers", {})
        recommendations = []
        alerts = []
        
        # Process blood sugar
        if "blood_sugar" in biomarkers:
            bs_value = biomarkers["blood_sugar"]
            try:
                bs_value = float(bs_value)
                if bs_value > 125:
                    alerts.append("HIGH BLOOD SUGAR - Consult healthcare provider")
                    recommendations.append("Focus on low-GI foods and regular exercise")
            except (ValueError, TypeError):
                pass  # Skip if not a valid number
        
        # Process cholesterol
        if "cholesterol" in biomarkers:
            chol_value = biomarkers["cholesterol"]
            try:
                chol_value = float(chol_value)
                if chol_value > 200:
                    alerts.append("HIGH CHOLESTEROL - Consider dietary changes")
                    recommendations.append("Increase fiber, reduce saturated fats")
            except (ValueError, TypeError):
                pass  # Skip if not a valid number
        
        # Process vitamin D
        if "vitamin_d" in biomarkers:
            vit_d_value = biomarkers["vitamin_d"]
            try:
                vit_d_value = float(vit_d_value)
                if vit_d_value < 30:
                    alerts.append("LOW VITAMIN D - Consider supplementation")
                    recommendations.append("Add fortified foods and safe sun exposure")
            except (ValueError, TypeError):
                pass  # Skip if not a valid number
        
        return self.send_message(
            message.sender,
            MessageType.RESPONSE,
            {
                "alerts": alerts,
                "recommendations": recommendations,
                "message": f"Medical analysis complete: {len(alerts)} alerts, {len(recommendations)} recommendations"
            }
        )
    
    def get_insights(self) -> Dict[str, Any]:
        """Get insights about medical data"""
        return {
            "biomarker_types": list(self.biomarker_ranges.keys()),
            "total_biomarkers": len(self.biomarker_ranges),
            "blood_sugar_ranges": len(self.biomarker_ranges["blood_sugar"]),
            "cholesterol_ranges": len(self.biomarker_ranges["cholesterol"])
        }
