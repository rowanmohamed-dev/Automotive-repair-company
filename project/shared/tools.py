from collections import Counter
import re


class VehicleTools:
    """
    Wraps the repair-history dataset as a small set of callable tools.
    All four agent architectures (reactive, routing, unconstrained ReAct,
    constrained ReAct) share this same class so the comparison stays fair.
    """

    def __init__(self, data_loader):
        self.data_loader = data_loader

    @staticmethod
    def _normalize_text(text):
        if text is None:
            return ""
        text = str(text).strip().lower()
        return " ".join(re.findall(r"\w+", text))

    def get_history_by_customer(self, customer_id):
        df = self.data_loader.get_dataset()
        if "customer_id" not in df.columns:
            raise ValueError("Column 'customer_id' not found in the dataset.")

        matches = df[df["customer_id"] == customer_id]
        if matches.empty:
            return []
        return matches["service_history"].tolist()

    def find_similar_problems(self, problem_text, limit=5):
        df = self.data_loader.get_dataset()
        if "common_problem" not in df.columns:
            raise ValueError("Column 'common_problem' not found in the dataset.")

        query = self._normalize_text(problem_text)
        if not query:
            return []

        query_terms = set(query.split())
        scored_rows = []

        for _, row in df.iterrows():
            problem = self._normalize_text(row.get("common_problem"))
            if not problem:
                continue

            problem_terms = set(problem.split())
            overlap = len(query_terms & problem_terms)
            score = overlap
            if score == 0 and query in problem:
                score = 1

            if score > 0:
                scored_rows.append((score, row))

        scored_rows.sort(key=lambda item: (-item[0], item[1].name))
        results = [row for _, row in scored_rows[:limit]]

        return [
            {
                "problem": row["common_problem"],
                "solution": row.get("solution_used"),
                "vehicle_company": row.get("vehicle_company"),
            }
            for row in results
        ]

    def get_solution_for_problem(self, problem_text):
        matches = self.find_similar_problems(problem_text, limit=50)
        if not matches:
            return None

        solutions = [m["solution"] for m in matches if m["solution"]]
        if not solutions:
            return None

        most_common, _ = Counter(solutions).most_common(1)[0]
        return most_common

    def get_problems_by_brand(self, vehicle_company, limit=10):
        df = self.data_loader.get_dataset()
        if "vehicle_company" not in df.columns:
            raise ValueError("Column 'vehicle_company' not found in the dataset.")

        company_name = self._normalize_text(vehicle_company)
        if not company_name:
            return []

        matches = df[df["vehicle_company"].apply(lambda value: company_name in self._normalize_text(value))]
        return matches["common_problem"].head(limit).tolist()

    def get_location_stats(self, city=None, state=None):
        df = self.data_loader.get_dataset()
        filtered = df

        if city is not None:
            if "city" not in df.columns:
                raise ValueError("City information is unavailable in the dataset.")
            city_normalized = self._normalize_text(city)
            filtered = filtered[filtered["city"].apply(lambda value: self._normalize_text(value) == city_normalized)]

        if state is not None:
            if "state" not in df.columns:
                raise ValueError("State information is unavailable in the dataset.")
            state_normalized = self._normalize_text(state)
            filtered = filtered[filtered["state"].apply(lambda value: self._normalize_text(value) == state_normalized)]

        return len(filtered)
