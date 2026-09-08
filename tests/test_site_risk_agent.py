from services.site_data_loader import SiteDataLoader
from services.risk_report_generator import RiskReportGenerator
from agents.site_risk_agent.agent import SiteRiskAgent


input_file = "data/raw/site_monitoring.csv"
output_file = "data/processed/site_risk_results.csv"


# Load site monitoring data
loader = SiteDataLoader(input_file)
site_records = loader.load_data()


# Create Site Risk Agent
agent = SiteRiskAgent()


# Analyze all site records
results = []

for record in site_records:
    result = agent.analyze_site(record)
    results.append(result)


# Save results
report_generator = RiskReportGenerator(output_file)
report_generator.save_results(results)


print("\n===== SITE RISK ANALYSIS COMPLETED =====")
print(f"Records analyzed: {len(results)}")
print(f"Risk report saved to: {output_file}")