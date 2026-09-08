from agents.safety_agent.risk_rules import check_ppe, check_behavior
from services.safety_scoring_engine import SafetyScoringEngine
from services.safety_alert_service import SafetyAlertService


class SafetyAgent:

    def __init__(self):
        self.agent_name = "Safety Agent"
        self.scoring_engine = SafetyScoringEngine()
        self.alert_service = SafetyAlertService()

    def analyze_worker(self, worker_data):
        """Analyze one worker's safety condition."""

        # Detect PPE violations
        ppe_violations = check_ppe(worker_data)

        # Detect unsafe behavior
        behavior_violations = check_behavior(worker_data)

        # Combine all violations
        violations = ppe_violations + behavior_violations

        # Calculate safety score
        safety_score = self.scoring_engine.calculate_score(
            violations
        )

        # Determine safety level
        safety_level = self.scoring_engine.get_safety_level(
            safety_score
        )

        # Generate alert
        alert = self.alert_service.generate_alert(
            safety_score,
            violations
        )

        # Generate recommendations
        recommendations = [
            violation["recommendation"]
            for violation in violations
        ]

        return {
            "timestamp": worker_data.get("timestamp"),
            "worker_id": worker_data.get("worker_id"),
            "zone": worker_data.get("zone"),
            "safety_score": safety_score,
            "safety_level": safety_level,
            "ppe_compliance": (
                "Compliant"
                if not ppe_violations
                else "Violation"
            ),
            "violations": violations,
            "alert": alert,
            "recommendations": recommendations
        }