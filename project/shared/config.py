from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "Vehicle Service and Repair Dataset for Analysis.csv"
)

"""
    this file contains the configuration settings for the project,
    including the base directory and the path to the cleaned dataset. 
    The BASE_DIR variable is set to the parent directory of the current file,
    and the DATA_PATH variable is set to the path of the cleaned dataset within the data/processed directory.

"""