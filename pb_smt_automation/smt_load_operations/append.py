import os
import pandas as pd

def append_to_master_smt_load_file(df, master_file_path):
    """
    Append data to the SMT Load master file. If the file doesn't exist, create it.
    """
    print("Appending data to master file...")
    if os.path.exists(master_file_path):
        master_df = pd.read_excel(master_file_path)
        print(f"Existing master file loaded with {len(master_df)} rows.")
        updated_df = pd.concat([master_df, df], ignore_index=True)
    else:
        print("Master file does not exist. Creating a new one.")
        updated_df = df

    updated_df.to_excel(master_file_path, index=False)
    print(f"Data successfully saved to {master_file_path}")
