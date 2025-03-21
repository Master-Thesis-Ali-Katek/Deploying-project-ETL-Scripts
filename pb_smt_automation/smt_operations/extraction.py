import pandas as pd
import os


def extract_smt_data(file_path):
    """
    Extract data from SMT input files.
    
    :param file_path: Path to the SMT input file.
    :return: Extracted DataFrame or None if there's an error.
    """
    # Validate the file existence
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Please verify the path and try again.")
        return None

    # Load the SMT CSV file
    try:
        # Assuming the delimiter and header information is consistent
        df = pd.read_csv(file_path, delimiter=';', header=1)
        print(f"Successfully extracted SMT data from {file_path}")
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}. Please check and try again.")
    except PermissionError:
        print(f"Permission denied: Unable to read {file_path}.")
    except pd.errors.ParserError as e:
        print(f"ParserError: Unable to parse {file_path}. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while extracting SMT data: {e}")

    return None
