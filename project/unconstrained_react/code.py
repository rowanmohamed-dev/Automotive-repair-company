"""
Unconstrained ReAct Agent

Member 3 - ReAct & Reliability

This agent demonstrates a ReAct-style loop without strict
schema validation, allow-list enforcement, retry limits,
or escalation rules.
"""

import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(_file_).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from shared.config import DATA_PATH
from shared.data_loader import DataLoader
from shared.tools import VehicleTools


class UnconstrainedReActAgent:
    """
    A simple ReAct-style agent that can execute tool calls.

    This version is intentionally unconstrained:
    - No strict schema validation
    - No tool allow-list
    - No MAX_STEPS limit
    - No retry limit
    - No escalation mechanism
    """

    def _init_(self, tools):
        self.tools = tools

    def execute_tool(self, tool_name, arguments):
        """
        Execute a tool by its name.

        In the unconstrained version, there are no strict
        reliability restrictions.
        """

        tool = getattr(self.tools, tool_name)

        return tool(**arguments)

    def run(self, tool_name, arguments):
        """
        Run a tool call and return the result.
        """

        try:
            result = self.execute_tool(tool_name, arguments)

            return {
                "status": "success",
                "tool": tool_name,
                "result": result,
            }

        except Exception as error:

            return {
                "status": "error",
                "tool": tool_name,
                "error": str(error),
            }


def main():

    # Load the dataset using the shared DataLoader
    data_loader = DataLoader(DATA_PATH)

    # Create the shared tools
    tools = VehicleTools(data_loader)

    # Create the unconstrained ReAct agent
    agent = UnconstrainedReActAgent(tools)

    # Example tool call
    result = agent.run(
        tool_name="get_solution_for_problem",
        arguments={
            "problem_text": "engine overheating"
        }
    )

    print(result)


if _name_ == "_main_":
    main()