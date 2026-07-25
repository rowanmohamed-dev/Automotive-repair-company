import pandas as pd


class DataLoader:
    COLUMN_RENAME_MAP = {
        "customer id": "customer_id",
        "city": "city",
        "state": "state",
        "service history": "service_history",
        "vehical company": "vehicle_company",
        "vehicle company": "vehicle_company",
        "common problem": "common_problem",
        "solution used": "solution_used",
    }

    def __init__(self, data_path: str):
        """Initialize DataLoader and read CSV from data_path.

        Raises:
            FileNotFoundError: If the file at data_path does not exist.
            RuntimeError: If the file cannot be parsed as CSV.
        """
        self.data_path = data_path
        try:
            self.df = pd.read_csv(self.data_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to read CSV at {self.data_path}: {e}") from e

        self._normalize_columns()
        self._clean_string_columns()
        self._normalize_customer_id()

    def _normalize_columns(self) -> None:
        normalized_columns = [col.strip().lower() for col in self.df.columns]
        self.df.columns = [self.COLUMN_RENAME_MAP.get(col, col.replace(" ", "_")) for col in normalized_columns]

    def _clean_string_columns(self) -> None:
        for column in self.df.select_dtypes(include=[object]).columns:
            self.df[column] = self.df[column].apply(
                lambda value: value.strip() if isinstance(value, str) else value
            )

    def _normalize_customer_id(self) -> None:
        if "customer_id" in self.df.columns:
            try:
                converted = pd.to_numeric(self.df["customer_id"], errors="coerce")
                if converted.notna().all():
                    self.df["customer_id"] = converted.astype(int)
            except Exception:
                pass

    def get_dataset(self) -> pd.DataFrame:
        """Return the cleaned dataset as a pandas DataFrame."""
        return self.df

    def get_columns(self) -> list:
        """Get the column names of the cleaned dataset."""
        return self.df.columns.tolist()

    def show_dataset_info(self) -> None:
        """Display information about the cleaned dataset."""
        print("Dataset Information:")
        self.df.info()

    def get_column_info(self, column_name: str) -> dict:
        """Get information about a specific column in the cleaned dataset."""
        if column_name in self.df.columns:
            return {
                "data_type": self.df[column_name].dtype,
                "unique_values": self.df[column_name].unique().tolist(),
                "num_unique_values": self.df[column_name].nunique(),
            }
        raise ValueError(f"Column '{column_name}' not found in the dataset.")

    def filter_dataset(self, column_name: str, value) -> pd.DataFrame:
        """Filter the cleaned dataset based on a specific column and value."""
        if column_name not in self.df.columns:
            raise ValueError(f"Column '{column_name}' not found in the dataset.")
        return self.df[self.df[column_name] == value]

    def take_sample(self, n: int = 5) -> pd.DataFrame:
        """Take a random sample of the cleaned dataset."""
        if n <= 0:
            raise ValueError("Sample size n must be a positive integer")
        if n > len(self.df):
            raise ValueError(f"Sample size n={n} is larger than the dataset size {len(self.df)}.")
        return self.df.sample(n=n)

    def get_number_of_rows(self) -> int:
        """Get the number of rows in the cleaned dataset."""
        return len(self.df)

    def get_number_of_columns(self) -> int:
        """Get the number of columns in the cleaned dataset."""
        return len(self.df.columns)    
