import csv


class SafetyReportGenerator:

    def __init__(self, output_path):
        self.output_path = output_path

    def generate_report(self, results):
        """Save worker safety analysis results to CSV."""

        rows = []

        for result in results:

            violation_types = [
                violation["type"]
                for violation in result["violations"]
            ]

            rows.append({
                "timestamp": result["timestamp"],
                "worker_id": result["worker_id"],
                "zone": result["zone"],
                "safety_score": result["safety_score"],
                "safety_level": result["safety_level"],
                "ppe_compliance": result["ppe_compliance"],
                "violations": "; ".join(violation_types),
                "alert": result["alert"],
                "recommendations": "; ".join(
                    result["recommendations"]
                )
            })

        fieldnames = [
            "timestamp",
            "worker_id",
            "zone",
            "safety_score",
            "safety_level",
            "ppe_compliance",
            "violations",
            "alert",
            "recommendations"
        ]

        with open(
            self.output_path,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(rows)

        return self.output_path