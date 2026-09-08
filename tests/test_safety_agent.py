from agents.safety_agent.agent import SafetyAgent
from services.safety_data_loader import SafetyDataLoader
from services.safety_report_generator import SafetyReportGenerator


def main():

    # 1. Load worker safety data
    loader = SafetyDataLoader(
        "data/raw/worker_safety.csv"
    )

    worker_data = loader.load_data()

    # 2. Create Safety Agent
    safety_agent = SafetyAgent()

    # 3. Analyze all workers
    results = []

    for worker in worker_data:

        result = safety_agent.analyze_worker(worker)

        results.append(result)

    # 4. Generate processed report
    report_generator = SafetyReportGenerator(
        "data/processed/worker_safety_results.csv"
    )

    output_file = report_generator.generate_report(results)

    # 5. Print summary
    print("\n" + "=" * 60)
    print("MILESTONE 2 - SAFETY ANALYSIS COMPLETED")
    print("=" * 60)

    print("Total Workers:", len(results))
    print("Report Generated:", output_file)

    print("\nWorker Safety Summary:")
    print("-" * 60)

    for result in results:

        print(
            f"{result['worker_id']} | "
            f"{result['zone']} | "
            f"Score: {result['safety_score']} | "
            f"Level: {result['safety_level']} | "
            f"Alert: {result['alert']}"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()