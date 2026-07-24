def run_brake_workflow(complaint, tools):
    """Handle a BRAKES complaint using historical repair cases."""
    matches = tools.find_similar_problems(complaint)
    solution = tools.get_solution_for_problem(complaint)
    return {
        "workflow": "run_brake_workflow",
        "matched_cases": matches,
        "suggested_solution": solution,
    }


def run_engine_workflow(complaint, tools):
    """Handle an ENGINE complaint using historical repair cases."""
    matches = tools.find_similar_problems(complaint)
    solution = tools.get_solution_for_problem(complaint)
    return {
        "workflow": "run_engine_workflow",
        "matched_cases": matches,
        "suggested_solution": solution,
    }


def run_exhaust_workflow(complaint, tools):
    """Handle an EXHAUST complaint using historical repair cases."""
    matches = tools.find_similar_problems(complaint)
    solution = tools.get_solution_for_problem(complaint)
    return {
        "workflow": "run_exhaust_workflow",
        "matched_cases": matches,
        "suggested_solution": solution,
    }


def run_tire_workflow(complaint, tools):
    """Handle a TIRES complaint using historical repair cases."""
    matches = tools.find_similar_problems(complaint)
    solution = tools.get_solution_for_problem(complaint)
    return {
        "workflow": "run_tire_workflow",
        "matched_cases": matches,
        "suggested_solution": solution,
    }


def run_cosmetic_workflow(complaint, tools):
    """Handle a COSMETIC complaint using historical repair cases."""
    matches = tools.find_similar_problems(complaint)
    solution = tools.get_solution_for_problem(complaint)
    return {
        "workflow": "run_cosmetic_workflow",
        "matched_cases": matches,
        "suggested_solution": solution,
    }


def run_transmission_workflow(complaint, tools):
    """Handle a TRANSMISSION complaint using historical repair cases."""
    matches = tools.find_similar_problems(complaint)
    solution = tools.get_solution_for_problem(complaint)
    return {
        "workflow": "run_transmission_workflow",
        "matched_cases": matches,
        "suggested_solution": solution,
    }


def run_electrical_workflow(complaint, tools):
    """Handle an ELECTRICAL complaint using historical repair cases."""
    matches = tools.find_similar_problems(complaint)
    solution = tools.get_solution_for_problem(complaint)
    return {
        "workflow": "run_electrical_workflow",
        "matched_cases": matches,
        "suggested_solution": solution,
    }


def route_to_human(complaint, tools):
    """
    Fallback for OTHER / unrecognized complaints. No dataset lookup —
    this is the deterministic-routing equivalent of an escalation.
    """
    return {
        "workflow": "route_to_human",
        "matched_cases": [],
        "suggested_solution": None,
    }


WORKFLOW_DISPATCH = {
    "BRAKES": run_brake_workflow,
    "ENGINE": run_engine_workflow,
    "EXHAUST": run_exhaust_workflow,
    "TIRES": run_tire_workflow,
    "COSMETIC": run_cosmetic_workflow,
    "TRANSMISSION": run_transmission_workflow,
    "ELECTRICAL": run_electrical_workflow,
    "OTHER": route_to_human,
}


def run_workflow(category, complaint, tools):
    """
    Dispatch to the workflow function for a given category. This is the
    "ordinary, testable code" step that runs after the single routing
    classification call.

    Args:
        category (str): Category returned by classify().
        complaint (str): Original customer complaint text.
        tools (VehicleTools): Shared dataset tools instance.

    Returns:
        dict: Workflow result (matched cases + suggested solution).
    """
    workflow_fn = WORKFLOW_DISPATCH.get(category, route_to_human)
    return workflow_fn(complaint, tools)