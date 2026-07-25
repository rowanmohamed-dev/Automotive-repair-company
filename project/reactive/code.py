class ReactiveAgent:
    """
    A rule-based reactive agent for the automotive repair company.

    The agent receives a predefined request type and directly calls
    the corresponding tool without using any model or reasoning process.
    """

    def __init__(self, tools):
        self.tools = tools

    def process_request(self, request_type, **kwargs):
        """
        Process a request using predefined rules.

        Args:
            request_type (str): The type of request to process.
            **kwargs: Additional arguments required by the selected tool.

        Returns:
            The result returned by the corresponding tool.
        """

        if request_type == "customer_history":
            return self.tools.get_history_by_customer(
                kwargs["customer_id"]
            )

        elif request_type == "similar_problems":
            return self.tools.find_similar_problems(
                kwargs["problem_text"]
            )

        elif request_type == "solution":
            return self.tools.get_solution_for_problem(
                kwargs["problem_text"]
            )

        elif request_type == "brand_problems":
            return self.tools.get_problems_by_brand(
                kwargs["vehicle_company"]
            )

        elif request_type == "location_stats":
            return self.tools.get_location_stats(
                city=kwargs.get("city"),
                state=kwargs.get("state")
            )

        else:
            return {
                "success": False,
                "message": (
                    f"Invalid request type: '{request_type}'. "
                    "Please specify a valid request type."
                )
            }