from services.risk_scoring_engine import RiskScoringEngine


class SiteRiskAgent:
    """
    Site Risk Agent responsible for detecting
    construction site hazards.
    """

    def __init__(self):
        self.agent_name = "Site Risk Agent"
        self.risk_engine = RiskScoringEngine()

    def detect_hazards(self, site_data):
        """
        Detect hazards from site monitoring data.
        """

        hazards = []

        # Environmental risks
        if site_data.get("weather") == "heavy_rain":
            hazards.append({
                "type": "Environmental",
                "hazard": "Heavy rain",
                "severity": "high",
                "recommendation": "Stop high-risk outdoor activities."
            })

        if site_data.get("visibility") == "low":
            hazards.append({
                "type": "Environmental",
                "hazard": "Low visibility",
                "severity": "medium",
                "recommendation": "Improve site lighting and visibility."
            })

        # Equipment risks
        if site_data.get("equipment_status") == "faulty":
            hazards.append({
                "type": "Equipment",
                "hazard": "Faulty equipment",
                "severity": "critical",
                "recommendation": "Stop using faulty equipment immediately."
            })

        # Site condition risks
        if site_data.get("floor_condition") == "wet":
            hazards.append({
                "type": "Site Condition",
                "hazard": "Wet floor",
                "severity": "medium",
                "recommendation": "Restrict access and remove water."
            })

        return hazards

    def analyze_site(self, site_data):
        """
        Analyze site data and generate risk assessment.
        """

        hazards = self.detect_hazards(site_data)

        risk_score = self.risk_engine.calculate_score(hazards)

        risk_level = self.risk_engine.get_risk_level(risk_score)

        recommendations = [
            hazard["recommendation"]
            for hazard in hazards
        ]

        return {
            "agent": self.agent_name,
            "timestamp": site_data.get("timestamp"),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "hazard_count": len(hazards),
            "hazards": hazards,
            "recommendations": recommendations
        }