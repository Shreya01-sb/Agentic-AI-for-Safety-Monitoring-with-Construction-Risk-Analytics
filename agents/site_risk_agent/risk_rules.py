# Risk levels and their scores

RISK_SCORES = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}


def calculate_risk_score(hazards):
    """
    Calculate the overall site risk score
    based on detected hazards.
    """

    if not hazards:
        return 0

    score = 0

    for hazard in hazards:
        severity = hazard.get("severity", "low").lower()
        score += RISK_SCORES.get(severity, 1)

    return score


def get_risk_level(score):
    """
    Convert numerical risk score into a risk level.
    """

    if score == 0:
        return "Safe"
    elif score <= 2:
        return "Low"
    elif score <= 4:
        return "Medium"
    elif score <= 6:
        return "High"
    else:
        return "Critical"