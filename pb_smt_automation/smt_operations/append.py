import os
import pandas as pd

def append_to_master_smt_file(df, master_file_path):
    """
    Append SMT DataFrame to the master file.

    :param df: DataFrame to append.
    :param master_file_path: Path to the master SMT Excel file.
    """
    try:
        if os.path.exists(master_file_path):
            # Load existing data
            existing_data = pd.read_excel(master_file_path, engine='openpyxl')
            print(f"Existing master file loaded: {master_file_path}")
        else:
            # Create an empty DataFrame if file does not exist
            existing_data = pd.DataFrame()

        # Combine old and new data
        combined_data = pd.concat([existing_data, df], ignore_index=True)

        # Save updated data back to the master file
        combined_data.to_excel(master_file_path, index=False, engine='openpyxl')
        print(f"Data successfully appended to {master_file_path}")

    except PermissionError:
        print(f"Permission denied: Unable to write to {master_file_path}. Please close the file and try again.")
    except Exception as e:
        print(f"Unexpected error while appending to {master_file_path}: {e}")
