import os
import json
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_fixed


# 1. Schema Definition (Required for Workstream 3)

class AgentStepSchema(BaseModel):
    thought: str = Field(description="Step-by-step reasoning of the agent.")
    action: Optional[str] = Field(default=None, description="Name of the tool to execute.")
    action_input: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Tool parameters.")
    is_final: bool = Field(default=False, description="Whether the final solution is reached.")
    final_answer: Optional[str] = Field(default=None, description="Final response to the user.")



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
    pass

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def parse_and_validate_step(raw_response_str: str) -> AgentStepSchema:
    """Parses LLM output and validates it strictly against the Pydantic schema."""
    data = json.loads(raw_response_str)
    return AgentStepSchema(**data)

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
    def __init__(self, df=None, max_steps: int = 5):
        self.df = df
        self.MAX_STEPS = max_steps  # Enforcing MAX_STEPS budget

    def execute_tool(self, tool_name: str, tool_args: dict):
        # Allow-List check
        if tool_name not in ALLOWED_TOOLS:
            raise ValueError(f"Tool '{tool_name}' is not in the Allow-List: {ALLOWED_TOOLS}")
        
        # Tool execution mock / logic
        return f"Executed {tool_name} with args {tool_args} successfully."

    def run(self, problem: str):
        history = []
        
        for step in range(1, self.MAX_STEPS + 1):
            print(f"\n--- [Step {step} / {self.MAX_STEPS}] ---")
            
            # Simulated model response strictly conforming to schema
            # In live run: call LLM with prompt forcing AgentStepSchema JSON
            try:
                # Step parsing with Retry logic
                raw_llm_output = '{"thought": "Checking history first", "action": "get_car_history", "action_input": {"vehicle_id": "123"}, "is_final": false}'
                step_obj = parse_and_validate_step(raw_llm_output)
                history.append(step_obj)
                
                if step_obj.is_final:
                    return {
                        "status": "SUCCESS",
                        "final_answer": step_obj.final_answer,
                        "steps": step
                    }
                
                # Execute tool via allow-list validation
                tool_result = self.execute_tool(step_obj.action, step_obj.action_input)
                print(f"Tool Output: {tool_result}")

            except Exception as e:
                print(f"Step {step} failed or invalid schema: {str(e)}")
                
        # If loop finishes without reaching final_answer -> Escalate!
        return escalate_to_human(problem, history, f"Reached MAX_STEPS limit ({self.MAX_STEPS})")
