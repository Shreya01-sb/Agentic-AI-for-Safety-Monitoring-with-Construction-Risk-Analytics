class SafetyScoringEngine:

    def calculate_score(self, violations):
        """Calculate safety score out of 100."""

        penalties = {
            "Helmet violation": 25,
            "Safety vest violation": 20,
            "Safety shoes violation": 20,
            "Unsafe worker behavior": 35
        }

        score = 100

        for violation in violations:
            score -= penalties.get(violation["type"], 0)

        return max(0, score)

    def get_safety_level(self, score):
        """Convert safety score into safety level."""

        if score >= 90:
            return "Safe"
        elif score >= 70:
            return "Low"
        elif score >= 50:
            return "Medium"
        elif score >= 25:
            return "High"
        else:
            return "Critical"