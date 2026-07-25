import pandas as pd


class DataLoader:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = pd.read_csv(self.data_path)

    
    #Retruns the dataset as a pandas DataFrame
    def get_dataset(self):
        """
        Load the cleaned dataset from the specified path.

        Returns:
            pd.DataFrame: The cleaned dataset as a pandas DataFrame.
        """
        return self.df
    
    
    def get_columns(self):
        """
        Get the column names of the cleaned dataset.

        Returns:
            list: A list of column names in the cleaned dataset.
        """
        return self.df.columns.tolist()
    
    def show_dataset_info(self):
        """
        Display information about the cleaned dataset, including the number of rows, columns, and data types.
        """
        print("Dataset Information:")
        self.df.info()
        
        
    def get_column_info(self, column_name):
        """
        Get information about a specific column in the cleaned dataset.

        Args:
            column_name (str): The name of the column to get information about.

        Returns:
            dict: A dictionary containing information about the specified column, including data type and unique values.
        """
        if column_name in self.df.columns:
            column_info = {
                "data_type": self.df[column_name].dtype,
                "unique_values": self.df[column_name].unique().tolist(),
                "num_unique_values": self.df[column_name].nunique()
            }
            return column_info
        else:
            raise ValueError(f"Column '{column_name}' not found in the dataset.")
    
    def filter_dataset(self, column_name, value):
        """
        Filter the cleaned dataset based on a specific column and value.

        Args:
            column_name (str): The name of the column to filter by.
            value: The value to filter for in the specified column.

        Returns:
            pd.DataFrame: The filtered dataset as a pandas DataFrame.
        """
        if column_name in self.df.columns:
            filtered_df = self.df[self.df[column_name] == value]
            return filtered_df
        else:
            raise ValueError(f"Column '{column_name}' not found in the dataset.")
        
        
        
    def take_sample(self, n=5):
        """
        Take a random sample of the cleaned dataset.

        Args:
            n (int): The number of samples to take. Default is 5.

        Returns:
            pd.DataFrame: A random sample of the cleaned dataset as a pandas DataFrame.
        """
        
        if n > len(self.df):
            raise ValueError(f"Sample size n={n} is larger than the dataset size {len(self.df)}.")
        return self.df.sample(n=n)
    
    
    def get_number_of_rows(self):
        """
        Get the number of rows in the cleaned dataset.

        Returns:
            int: The number of rows in the cleaned dataset.
        """
        return len(self.df)

    def get_number_of_columns(self):
        """
        Get the number of columns in the cleaned dataset.

        Returns:
            int: The number of columns in the cleaned dataset.
        """
        return len(self.df.columns)
    
