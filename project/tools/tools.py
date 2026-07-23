def searchVehicle(df , vechicleId):
    """
    Search for a vehicle in the dataset based on its ID.

    Args:
        df (pd.DataFrame): The dataset as a pandas DataFrame.
        vechicleId: The ID of the vehicle to search for.

    Returns:
        pd.DataFrame: A DataFrame containing the rows that match the vehicle ID.
    """
    if 'VEHICAL ID' in df.columns:
        result_df = df[df['VEHICAL ID'] == vechicleId]
        return result_df
    else:
        raise ValueError("Column 'VEHICAL ID' not found in the dataset.")
    
    
def getCarHistory(df, vechicleId):
    """
    Get the history of a vehicle based on its ID.

    Args:
        df (pd.DataFrame): The dataset as a pandas DataFrame.
        vechicleId: The ID of the vehicle to retrieve history for.

    Returns:
        pd.DataFrame: A DataFrame containing the history of the specified vehicle.
    """
    if 'VEHICAL ID' in df.columns:
        history_df = df[df['VEHICAL ID'] == vechicleId]['SEVICE HISTORY'].values
        return history_df
    else:
        raise ValueError("Column 'VEHICAL ID' not found in the dataset.")
    
    
def getCarState(df ,vechicleId):
    """
    
    Get the current state of a vehicle based on its ID.

    Args:
        df (pd.DataFrame): The dataset as a pandas DataFrame.
        vechicleId: The ID of the vehicle to retrieve the state for.

    Returns:
        str: The current state of the specified vehicle.
    """
    if 'VEHICAL ID' in df.columns and 'STATE' in df.columns:
        state = df[df['VEHICAL ID'] == vechicleId]['STATE'].values
        return state
    else:
        raise ValueError("Required columns not found in the dataset.")