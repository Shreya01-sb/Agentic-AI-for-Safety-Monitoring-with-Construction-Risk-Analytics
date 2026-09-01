class RiskScoringEngine:
    """
    Calculates the overall risk score and risk level
    based on detected construction-site hazards.
    """

    SEVERITY_SCORES = {
        "low": 10,
        "medium": 25,
        "high": 40,
        "critical": 60
    }

    def calculate_score(self, hazards):
        """
        Calculate risk score from detected hazards.
        Maximum score is 100.
        """

        if not hazards:
            return 0

        score = 0

        for hazard in hazards:
            severity = hazard.get("severity", "low").lower()
            score += self.SEVERITY_SCORES.get(severity, 10)

        return min(score, 100)

    def get_risk_level(self, score):
        """
        Convert numerical score into a risk level.
        """

        if score == 0:
            return "Safe"
        elif score <= 25:
            return "Low"
        elif score <= 50:
            return "Medium"
        elif score <= 75:
            return "High"
        else:
            return "Critical"