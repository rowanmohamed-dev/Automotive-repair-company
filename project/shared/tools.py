from collections import Counter


class VehicleTools:
    """
    Wraps the repair-history dataset as a small set of callable tools.
    All four agent architectures (reactive, routing, unconstrained ReAct,
    constrained ReAct) share this same class so the comparison stays fair.
    """

    def _init_(self, data_loader):
        self.data_loader = data_loader

    def get_history_by_customer(self, customer_id):
        """
        Look up the service history for a given customer.

        Args:
            customer_id: The customer ID to search for.

        Returns:
            list[str]: Service history entries for that customer.
        """
        df = self.data_loader.get_dataset()
        if "CUSTOMER ID" not in df.columns:
            raise ValueError("Column 'CUSTOMER ID' not found in the dataset.")

        matches = df[df["CUSTOMER ID"] == customer_id]
        if matches.empty:
            return []
        return matches["SERVICE HISTORY"].tolist()

    def find_similar_problems(self, problem_text, limit=5):
        """
        Find rows whose COMMON PROBLEM text overlaps with the given text.

        Args:
            problem_text (str): Free-text complaint from the customer.
            limit (int): Max number of matching rows to return.

        Returns:
            list[dict]: Matching rows as plain dicts (problem, solution,
            vehicle company).
        """
        df = self.data_loader.get_dataset()
        if "COMMON PROBLEM" not in df.columns:
            raise ValueError("Column 'COMMON PROBLEM' not found in the dataset.")

        query_words = set(problem_text.lower().split())

        def overlaps(problem):
            problem_words = set(str(problem).lower().split())
            return len(query_words & problem_words) > 0

        matches = df[df["COMMON PROBLEM"].apply(overlaps)]
        results = matches.head(limit)

        return [
            {
                "problem": row["COMMON PROBLEM"],
                "solution": row.get("SOLUTION USED"),
                "vehicle_company": row.get("VEHICAL COMPANY"),
            }
            for _, row in results.iterrows()
        ]

    def get_solution_for_problem(self, problem_text):
        """
        Return the most common repair solution used for problems similar
        to the given text.

        Args:
            problem_text (str): Free-text complaint from the customer.

        Returns:
            str | None: The most frequent matching solution, or None if
            no similar case was found.
        """
        matches = self.find_similar_problems(problem_text, limit=50)
        if not matches:
            return None

        solutions = [m["solution"] for m in matches if m["solution"]]
        if not solutions:
            return None

        most_common, _ = Counter(solutions).most_common(1)[0]
        return most_common

    def get_problems_by_brand(self, vehical_company, limit=10):
        """
        Return the common problems reported for a given vehicle brand.

        Args:
            vehical_company (str): Brand name, e.g. "Honda".
            limit (int): Max number of rows to return.

        Returns:
            list[str]: Common problem descriptions for that brand.
        """
        df = self.data_loader.get_dataset()
        if "VEHICAL COMPANY" not in df.columns:
            raise ValueError("Column 'VEHICAL COMPANY' not found in the dataset.")

        matches = df[
            df["VEHICAL COMPANY"].str.strip().str.lower()
            == vehical_company.strip().lower()
        ]
        return matches["COMMON PROBLEM"].head(limit).tolist()

    def get_location_stats(self, city=None, state=None):
        """
        Return how many records exist for a given city and/or state.

        Args:
            city (str, optional): City name to filter by.
            state (str, optional): State name to filter by.

        Returns:
            int: Number of matching records.
        """
        df = self.data_loader.get_dataset()
        filtered = df

        if city is not None:
            if "CITY" not in df.columns:
                raise ValueError("Column 'CITY' not found in the dataset.")
            filtered = filtered[filtered["CITY"] == city]

        if state is not None:
            if "STATE" not in df.columns:
                raise ValueError("Column 'STATE' not found in the dataset.")
            filtered = filtered[filtered["STATE"] == state]

        return len(filtered)