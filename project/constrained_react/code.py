import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from shared.config import DATA_PATH
from shared.data_loader import DataLoader
from shared.tools import VehicleTools


# 1. Schema Definition (Required for Workstream 3)

@dataclass
class AgentStepSchema:
    thought: str
    action: Optional[str] = None
    action_input: Dict[str, Any] = field(default_factory=dict)
    is_final: bool = False
    final_answer: Optional[str] = None



# 2. Allow-List Definition (Required for Workstream 3)

ALLOWED_TOOLS = [
    "get_car_history",
    "get_car_state",
    "check_parts_inventory",
    "calculate_repair_cost"
]



# 3. Retry & Escalation Logic (Required for Workstream 3)

class EscalationException(Exception):
    """Exception raised when step budget or validation limits are exceeded."""


def parse_and_validate_step(raw_response_str: str | dict) -> AgentStepSchema:
    """Parses agent response and validates it against the step schema."""
    if isinstance(raw_response_str, dict):
        data = raw_response_str
    else:
        data = json.loads(raw_response_str)

    if not isinstance(data, dict):
        raise ValueError("Agent response must be a JSON object.")

    thought = data.get("thought")
    if not isinstance(thought, str) or not thought.strip():
        raise ValueError("Agent response must include a non-empty 'thought'.")

    action = data.get("action")
    if action is not None and not isinstance(action, str):
        raise ValueError("'action' must be a string when present.")

    action_input = data.get("action_input", {})
    if action_input is None:
        action_input = {}
    if not isinstance(action_input, dict):
        raise ValueError("'action_input' must be a dictionary.")

    is_final = data.get("is_final", False)
    if not isinstance(is_final, bool):
        raise ValueError("'is_final' must be a boolean.")

    final_answer = data.get("final_answer")
    if is_final and (final_answer is None or not isinstance(final_answer, str)):
        raise ValueError("Final steps must include a non-empty 'final_answer'.")

    return AgentStepSchema(
        thought=thought,
        action=action,
        action_input=action_input,
        is_final=is_final,
        final_answer=final_answer,
    )

def escalate_to_human(problem_description: str, history: list, reason: str) -> dict:
    """Handles auto-escalation when ReAct loop reaches MAX_STEPS or unrecoverable error."""
    return {
        "status": "ESCALATED_TO_HUMAN",
        "reason": reason,
        "problem": problem_description,
        "executed_steps_count": len(history)
    }




# 4. Constrained ReAct Agent Class (MAX_STEPS Enforced)

class ConstrainedReActAgent:
    def __init__(self, tools: VehicleTools | None = None, max_steps: int = 5):
        self.tools = tools or VehicleTools(DataLoader(DATA_PATH))
        self.MAX_STEPS = max_steps

    def execute_tool(self, tool_name: str, tool_args: dict):
        if tool_name not in ALLOWED_TOOLS:
            raise ValueError(
                f"Tool '{tool_name}' is not in the Allow-List: {ALLOWED_TOOLS}"
            )

        executor = getattr(self, f"_tool_{tool_name}", None)
        if not callable(executor):
            raise NotImplementedError(f"Tool '{tool_name}' is not implemented.")

        return executor(tool_args)

    def _tool_get_car_history(self, tool_args: dict):
        customer_id = tool_args.get("customer_id")
        if customer_id is None:
            raise ValueError("customer_id is required for get_car_history")
        return self.tools.get_history_by_customer(customer_id)

    def _tool_get_car_state(self, tool_args: dict):
        customer_id = tool_args.get("customer_id")
        if customer_id is None:
            raise ValueError("customer_id is required for get_car_state")

        dataset = self.tools.data_loader.get_dataset()
        matches = dataset[dataset["customer_id"] == customer_id]
        if matches.empty:
            return {"customer_id": customer_id, "state": None}

        return {
            "customer_id": customer_id,
            "state": matches.iloc[-1]["state"],
        }

    def _tool_check_parts_inventory(self, tool_args: dict):
        part_name = tool_args.get("part_name") or tool_args.get("part")
        if not part_name:
            raise ValueError("part_name is required for check_parts_inventory")

        part_name_norm = part_name.strip().lower()
        inventory = {
            "brake": 8,
            "engine": 3,
            "tire": 12,
            "battery": 5,
            "exhaust": 6,
        }

        quantity = 2
        for key, value in inventory.items():
            if key in part_name_norm:
                quantity = value
                break

        return {
            "part_name": part_name,
            "available": quantity > 0,
            "quantity": quantity,
        }

    def _tool_calculate_repair_cost(self, tool_args: dict):
        problem_text = tool_args.get("problem_text", "")
        text = problem_text.lower()

        if "engine" in text or "overheat" in text:
            cost = 12500
        elif "brake" in text:
            cost = 4200
        elif "tire" in text or "tyre" in text:
            cost = 2500
        elif "exhaust" in text or "smoke" in text:
            cost = 3200
        elif "battery" in text or "electrical" in text:
            cost = 1800
        else:
            cost = 2800

        return {
            "problem_text": problem_text,
            "estimated_cost": cost,
            "currency": "INR",
        }

    def _simulate_llm_response(self, problem: str, step: int) -> str:
        normalized = problem.lower()

        if step == 1:
            if "history" in normalized or "previous" in normalized:
                action = "get_car_history"
                action_input = {"customer_id": 1}
            elif "state" in normalized or "current" in normalized:
                action = "get_car_state"
                action_input = {"customer_id": 1}
            elif "part" in normalized or "inventory" in normalized:
                action = "check_parts_inventory"
                action_input = {"part_name": "brake pad"}
            else:
                action = "calculate_repair_cost"
                action_input = {"problem_text": problem}

            return json.dumps(
                {
                    "thought": "Determine the best tool to answer the repair request.",
                    "action": action,
                    "action_input": action_input,
                    "is_final": False,
                }
            )

        return json.dumps(
            {
                "thought": "Use the tool output to produce the final answer.",
                "is_final": True,
                "final_answer": (
                    "I have gathered the required information and prepared a final recommendation. "
                    "Please review the executed tool result above for full detail."
                ),
            }
        )

    def run(self, problem: str) -> dict:
        history = []

        for step in range(1, self.MAX_STEPS + 1):
            print(f"\n--- [Step {step} / {self.MAX_STEPS}] ---")
            raw_llm_output = self._simulate_llm_response(problem, step)

            try:
                step_obj = parse_and_validate_step(raw_llm_output)
                history.append(step_obj)

                if step_obj.is_final:
                    return {
                        "status": "SUCCESS",
                        "final_answer": step_obj.final_answer,
                        "steps": step,
                    }

                tool_result = self.execute_tool(step_obj.action, step_obj.action_input)
                print(f"Tool Output: {tool_result}")

            except Exception as error:
                print(f"Step {step} failed or invalid schema: {error}")
                return escalate_to_human(problem, history, str(error))

        return escalate_to_human(
            problem,
            history,
            f"Reached MAX_STEPS limit ({self.MAX_STEPS}) without a final answer.",
        )


def main() -> None:
    tools = VehicleTools(DataLoader(DATA_PATH))
    agent = ConstrainedReActAgent(tools=tools)
    result = agent.run(
        "The car engine is overheating and the brakes are noisy."
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
