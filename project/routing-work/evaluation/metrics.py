import json
import os
import time
from datetime import datetime

RESULTS_FILE = "evaluation/results.json"


def time_and_record(
    agent_name: str,
    test_input: str,
    expected_category: str,
    run_fn,
) -> dict:
    start = time.perf_counter()
    error = None
    try:
        output = run_fn()
    except Exception as exc:
        output = {}
        error = str(exc)
    latency = round(time.perf_counter() - start, 3)
    predicted_category = output.get("category", "ERROR")
    correct = predicted_category == expected_category if error is None else False
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "agent": agent_name,
        "input": test_input,
        "expected_category": expected_category,
        "predicted_category": predicted_category,
        "correct": correct,
        "calls_made": output.get("calls_made", 1),
        "input_tokens": output.get("input_tokens", 0),
        "output_tokens": output.get("output_tokens", 0),
        "total_tokens": output.get("input_tokens", 0)
        + output.get("output_tokens", 0),
        "latency_sec": latency,
        "error": error,
    }


def save_results(
    records: list[dict],
    filepath: str = RESULTS_FILE,
) -> None:
    if not records:
        return
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    existing = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            existing = json.load(file)
    existing.extend(records)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(existing, file, indent=4, ensure_ascii=False)
    print(
        f"Saved {len(records)} record(s). Total records: {len(existing)}"
    )


def calculate_accuracy(records: list[dict]) -> float:
    if not records:
        return 0.0
    correct = sum(record["correct"] for record in records)
    return round((correct / len(records)) * 100, 2)


def print_summary(records: list[dict]) -> None:
    if not records:
        print("No evaluation records found.")
        return
    grouped = {}
    for record in records:
        grouped.setdefault(record["agent"], []).append(record)
    print("\n" + "=" * 80)
    print(
        f"{'Agent':<18}"
        f"{'Accuracy':<12}"
        f"{'Avg Latency':<15}"
        f"{'Avg Calls':<12}"
        f"{'Avg Tokens'}"
    )
    print("-" * 80)
    for agent, results in grouped.items():
        count = len(results)
        accuracy = calculate_accuracy(results)
        avg_latency = sum(
            r["latency_sec"] for r in results
        ) / count
        avg_calls = sum(
            r["calls_made"] for r in results
        ) / count
        avg_tokens = sum(
            r["total_tokens"] for r in results
        ) / count
        print(
            f"{agent:<18}"
            f"{accuracy:<11.1f}%"
            f"{avg_latency:<15.2f}"
            f"{avg_calls:<12.1f}"
            f"{avg_tokens:.1f}"
        )
    print("=" * 80)


if __name__ == "__main__":
    def sample_run():
        time.sleep(0.2)
        return {
            "category": "BRAKES",
            "calls_made": 1,
            "input_tokens": 120,
            "output_tokens": 8,
        }

    record = time_and_record(
        agent_name="routing",
        test_input="My brakes are making a grinding noise.",
        expected_category="BRAKES",
        run_fn=sample_run,
    )
    print(record)
    print_summary([record])
    save_results([record])