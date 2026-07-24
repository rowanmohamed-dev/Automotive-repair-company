import os
import sys
import time

sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "routing")
)
sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "data")
)
sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "tools")
)

from build_test_cases import get_test_cases
from classifier import classify
from data_loader import DataLoader
from metrics import (
    RESULTS_FILE,
    print_summary,
    save_results,
    time_and_record,
)
from vehicle_tools import VehicleTools
from workflows import run_workflow

# Gemini free tier allows 5 requests/minute for this model.
# 13 seconds between calls keeps us safely under that limit.
SECONDS_BETWEEN_CALLS = 13

CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "Vehicle_Service_and_Repair_Dataset_for_Analysis.csv",
)


def classify_and_route(complaint, tools):
    """
    Run the full deterministic-routing pipeline for one complaint:
    one classification call, then the fixed workflow that category
    maps to. Returns the same keys classify() returns so metrics.py
    needs no changes, plus the workflow output for inspection.
    """
    result = classify(complaint)
    workflow_result = run_workflow(result["category"], complaint, tools)
    result["workflow_result"] = workflow_result
    return result


def main() -> None:
    tools = VehicleTools(DataLoader(CSV_PATH))
    test_cases = get_test_cases(CSV_PATH)

    records = []
    for index, (complaint, expected_category) in enumerate(test_cases):
        record = time_and_record(
            agent_name="routing",
            test_input=complaint,
            expected_category=expected_category,
            run_fn=lambda text=complaint: classify_and_route(text, tools),
        )
        records.append(record)
        status = "PASS" if record["correct"] else "FAIL"
        print(
            f"{status:<5} | "
            f"{record['predicted_category']:<15} | "
            f"{complaint}"
        )

        is_last_case = index == len(test_cases) - 1
        if not is_last_case:
            time.sleep(SECONDS_BETWEEN_CALLS)
    save_results(records, RESULTS_FILE)
    print_summary(records)


if __name__ == "__main__":
    main()