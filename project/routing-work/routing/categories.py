CATEGORIES = [
    "BRAKES",
    "ENGINE",
    "EXHAUST",
    "TIRES",
    "COSMETIC",
    "TRANSMISSION",
    "ELECTRICAL",
    "OTHER",
]

CATEGORY_KEYWORDS = {
    "BRAKES": [
        "brake", "brakes", "braking", "brake pad",
        "screech", "squeal", "grinding"
    ],
    "ENGINE": [
        "engine", "motor", "overheat",
        "misfire", "stall"
    ],
    "EXHAUST": [
        "exhaust", "tailpipe", "smoke", "emission"
    ],
    "TIRES": [
        "tire", "tyre", "flat",
        "alignment", "wear"
    ],
    "COSMETIC": [
        "headlight", "paint", "dent",
        "scratch", "cloudy", "dim",
        "yellowed", "faded", "body"
    ],
    "TRANSMISSION": [
        "transmission", "gearbox",
        "gear", "slipping"
    ],
    "ELECTRICAL": [
        "battery", "electrical",
        "wiring", "check engine light"
    ],
    "OTHER": []
}

CATEGORY_TO_WORKFLOW = {
    "BRAKES": "run_brake_workflow",
    "ENGINE": "run_engine_workflow",
    "EXHAUST": "run_exhaust_workflow",
    "TIRES": "run_tire_workflow",
    "COSMETIC": "run_cosmetic_workflow",
    "TRANSMISSION": "run_transmission_workflow",
    "ELECTRICAL": "run_electrical_workflow",
    "OTHER": "route_to_human",
}


def is_valid_category(category: str) -> bool:
    """Return True if the category is supported"""
    return category in CATEGORIES


def get_workflow(category: str) -> str:
    """Return the workflow name assigned to a category"""
    return CATEGORY_TO_WORKFLOW.get(category, "route_to_human")


def infer_category_from_text(problem_text: str) -> str:
    """
    Label a raw dataset complaint using the same keyword table the
    routing prompt describes, so evaluation test cases can be built
    straight from the CSV instead of being written by hand.

    Args:
        problem_text (str): Free-text complaint, e.g. a COMMON PROBLEM
        value from the dataset.

    Returns:
        str: The best-matching category, or "OTHER" if nothing matches.
    """
    text = problem_text.lower()

    for category in CATEGORIES:
        if category == "OTHER":
            continue
        keywords = CATEGORY_KEYWORDS.get(category, [])
        if any(keyword in text for keyword in keywords):
            return category

    return "OTHER"