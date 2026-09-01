from services.site_data_loader import SiteDataLoader
from agents.site_risk_agent.agent import SiteRiskAgent


file_path = "data/raw/site_monitoring.csv"

loader = SiteDataLoader(file_path)

site_records = loader.load_data()

agent = SiteRiskAgent()


print("\n===== SITE RISK MONITORING =====")

for record in site_records:

    result = agent.analyze_site(record)

    print("\nTimestamp:", record["timestamp"])
    print("Risk Score:", result["risk_score"])
    print("Risk Level:", result["risk_level"])

    if result["hazards"]:
        print("Hazards:")

        for hazard in result["hazards"]:
            print("-", hazard["hazard"])
            print("  Severity:", hazard["severity"])
            print("  Recommendation:", hazard["recommendation"])

    else:
        print("Hazards: None")