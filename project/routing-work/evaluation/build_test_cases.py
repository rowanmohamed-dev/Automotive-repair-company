import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(SCRIPT_DIR.parent / "routing"))

from categories import infer_category_from_text
from shared.data_loader import DataLoader

DEFAULT_CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "cleaned"
    / "cleaned_vehicle_service_repair_dataset.csv"
)


def get_test_cases(csv_path=DEFAULT_CSV_PATH, n_per_category=4, seed=42):
    """
    Build a labeled test set straight from the dataset's COMMON PROBLEM
    column, instead of hand-writing complaints. Labels are inferred with
    the same keyword table the routing prompt uses, so BRAKES/ENGINE/...
    rows are balanced, and rows that match no keyword (e.g. "Steering
    issues", "AC not cooling") come through as OTHER — these are the
    tricky/unseen cases the assignment asks each agent to be tested on.

    Args:
        csv_path (str): Path to the vehicle service dataset CSV.
        n_per_category (int): Max rows to sample per category.
        seed (int): Random seed, so the same test set is reproducible
        across all four agent architectures.

    Returns:
        list[tuple[str, str]]: (complaint, expected_category) pairs.
    """
    loader = DataLoader(csv_path)
    df = loader.get_dataset()

    df = df.copy()
    df["INFERRED_CATEGORY"] = df["common_problem"].apply(
        infer_category_from_text
    )

    test_cases = []
    for category, group in df.groupby("INFERRED_CATEGORY"):
        sample_size = min(n_per_category, len(group))
        sample = group.sample(n=sample_size, random_state=seed)
        for problem in sample["common_problem"]:
            test_cases.append((problem, category))

    return test_cases


if __name__ == "__main__":
    cases = get_test_cases()
    for complaint, expected in cases:
        print(f"{expected:<14} | {complaint}")
    print(f"\nTotal test cases: {len(cases)}")