class VehicleTools:
    def __init__(self, data_loader):
        self.data_loader = data_loader

    def searchVehicle(self, vehicleId):
        """
        Search for a vehicle in the dataset based on its ID.

        Args:
            vehicleId: The ID of the vehicle to search for.

        Returns:
            pd.DataFrame: A DataFrame containing the rows that match the vehicle ID.
        """
        df = self.data_loader.get_dataset()
        if 'VEHICLE ID' in df.columns:
            result_df = df[df['VEHICLE ID'] == vehicleId]
            return result_df
        else:
            raise ValueError("Column 'VEHICLE ID' not found in the dataset.")
    
    def getCarHistory(self, vehicleId):
        """
        Get the history of a vehicle based on its ID.

        Args:
            vehicleId: The ID of the vehicle to retrieve history for.

        Returns:
            pd.DataFrame: A DataFrame containing the history of the specified vehicle.
        """
        df = self.data_loader.get_dataset()
        if 'VEHICLE ID' in df.columns:
            history_df = df[df['VEHICLE ID'] == vehicleId]['SERVICE HISTORY'].values
            return history_df
        else:
            raise ValueError("Column 'VEHICLE ID' not found in the dataset.")
    
    def getCarState(self, vehicleId):
        """
        Get the current state of a vehicle based on its ID.

        Args:
            vehicleId: The ID of the vehicle to retrieve the state for.

        Returns:
            str: The current state of the specified vehicle.
        """
        df = self.data_loader.get_dataset()
        if 'VEHICLE ID' in df.columns and 'STATE' in df.columns:
            state = df[df['VEHICLE ID'] == vehicleId]['STATE'].values
            return state
        else:
            raise ValueError("Required columns not found in the dataset.")