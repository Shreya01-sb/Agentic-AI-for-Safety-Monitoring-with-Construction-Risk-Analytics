# Safety risk rules for PPE and worker behavior


def check_ppe(worker_data):
    """
    Detect PPE violations for a worker.
    """

    violations = []

    if str(worker_data.get("helmet", "")).lower() != "yes":
        violations.append({
            "type": "Helmet violation",
            "severity": "high",
            "recommendation": "Worker must wear a safety helmet."
        })

    if str(worker_data.get("safety_vest", "")).lower() != "yes":
        violations.append({
            "type": "Safety vest violation",
            "severity": "medium",
            "recommendation": "Worker must wear a safety vest."
        })

    if str(worker_data.get("safety_shoes", "")).lower() != "yes":
        violations.append({
            "type": "Safety shoes violation",
            "severity": "medium",
            "recommendation": "Worker must wear approved safety shoes."
        })

    return violations


def check_behavior(worker_data):
    """
    Detect unsafe worker behavior.
    """

    behavior = str(
        worker_data.get("behavior", "")
    ).lower()

    if behavior == "unsafe":
        return [{
            "type": "Unsafe worker behavior",
            "severity": "high",
            "recommendation": "Stop unsafe activity and provide safety guidance."
        }]

    return []