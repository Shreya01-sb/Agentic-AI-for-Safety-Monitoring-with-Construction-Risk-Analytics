class SafetyAlertService:

    def generate_alert(self, safety_score, violations):
        """Generate an alert based on safety score and violations."""

        if not violations:
            return "No Alert"

        if safety_score < 50:
            return "Critical Alert"

        elif safety_score < 70:
            return "High Alert"

        else:
            return "Safety Warning"

    def get_alert_message(self, alert, worker_id, zone):
        """Create a readable safety alert message."""

        if alert == "No Alert":
            return "No safety issues detected."

        return (
            f"{alert}: Worker {worker_id} in {zone} "
            f"requires safety attention."
        )