class ReactiveAgent:
    """
    A rule-based reactive agent for the automotive repair company.

    The agent receives a predefined request type and directly calls
    the corresponding tool without using any model or reasoning process.
    """

    REQUEST_MAP = {
        "customer_history": "customer_history",
        "history": "customer_history",
        "similar_problems": "similar_problems",
        "similar": "similar_problems",
        "solution": "solution",
        "problem_solution": "solution",
        "brand_problems": "brand_problems",
        "brand": "brand_problems",
        "location_stats": "location_stats",
        "location": "location_stats",
    }

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
        if not isinstance(request_type, str):
            return {
                "success": False,
                "message": "Request type must be a string."
            }

        normalized_request = request_type.strip().lower()
        request_key = self.REQUEST_MAP.get(normalized_request)

        if request_key == "customer_history":
            customer_id = kwargs.get("customer_id")
            if customer_id is None:
                return {
                    "success": False,
                    "message": "Missing required parameter: customer_id."
                }
            return self.tools.get_history_by_customer(customer_id)

        if request_key == "similar_problems":
            problem_text = kwargs.get("problem_text")
            if not problem_text:
                return {
                    "success": False,
                    "message": "Missing required parameter: problem_text."
                }
            return self.tools.find_similar_problems(problem_text)

        if request_key == "solution":
            problem_text = kwargs.get("problem_text")
            if not problem_text:
                return {
                    "success": False,
                    "message": "Missing required parameter: problem_text."
                }
            return self.tools.get_solution_for_problem(problem_text)

        if request_key == "brand_problems":
            vehicle_company = kwargs.get("vehicle_company")
            if not vehicle_company:
                return {
                    "success": False,
                    "message": "Missing required parameter: vehicle_company."
                }
            return self.tools.get_problems_by_brand(vehicle_company)

        if request_key == "location_stats":
            return self.tools.get_location_stats(
                city=kwargs.get("city"),
                state=kwargs.get("state"),
            )

        return {
            "success": False,
            "message": (
                f"Invalid request type: '{request_type}'. "
                "Please specify a valid request type."
            )
        }

