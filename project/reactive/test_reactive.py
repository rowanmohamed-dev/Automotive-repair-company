import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from shared.config import DATA_PATH
from shared.data_loader import DataLoader
from shared.tools import VehicleTools
from reactive.reactive_agent import ReactiveAgent


def main():

    # 1. Load the dataset
    data_loader = DataLoader(DATA_PATH)

    # 2. Initialize the shared tools
    tools = VehicleTools(data_loader)

    # 3. Initialize the Reactive Agent
    agent = ReactiveAgent(tools)

    print("=" * 50)
    print("REACTIVE AGENT TEST")
    print("=" * 50)

    # -------------------------------------------------
    # Test 1: Customer History
    # -------------------------------------------------
    print("\n[TEST 1] Customer History")

    result = agent.process_request(
        "customer_history",
        customer_id=1
    )

    print("Result:")
    print(result)

    # -------------------------------------------------
    # Test 2: Similar Problems
    # -------------------------------------------------
    print("\n[TEST 2] Similar Problems")

    result = agent.process_request(
        "similar_problems",
        problem_text="brake problem"
    )

    print("Result:")
    for item in result:
        print(item)

    # -------------------------------------------------
    # Test 3: Solution
    # -------------------------------------------------
    print("\n[TEST 3] Solution")

    result = agent.process_request(
        "solution",
        problem_text="brake problem"
    )

    print("Result:")
    print(result)

    # -------------------------------------------------
    # Test 4: Problems by Brand
    # -------------------------------------------------
    print("\n[TEST 4] Problems by Brand")

    result = agent.process_request(
        "brand_problems",
        vehicle_company="Honda"
    )

    print("Result:")
    for problem in result:
        print(problem)

    # -------------------------------------------------
    # Test 5: Location Statistics
    # -------------------------------------------------
    print("\n[TEST 5] Location Statistics")

    result = agent.process_request(
        "location_stats",
        state="Andhra Pradesh"
    )

    print("Result:")
    print(result)

    # -------------------------------------------------
    # Test 6: Invalid Request
    # -------------------------------------------------
    print("\n[TEST 6] Invalid Request")

    result = agent.process_request(
        "invalid_request"
    )

    print("Result:")
    print(result)

    print("\n" + "=" * 50)
    print("TESTING COMPLETED")
    print("=" * 50)


if __name__ == "__main__":
    main()