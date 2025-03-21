import os
import pandas as pd
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Input paths for PB files
PB_INPUT_FILES = {
    "PB1": {
        "monthly": "/local_files/exp_wayconnect_0100 PB1_customer_labor_monthly.csv",
      "weekly": "/local_files/exp_wayconnect_0100 PB1_customer_labor_weekly.csv",
    },  
    "PB2": {
        "monthly": "/local_files/exp_wayconnect_0100 PB2_customer_labor_monthly.csv",
      "weekly": "/local_files/exp_wayconnect_0100 PB2_customer_labor_weekly.csv",
    },
    "PB3": {
        "monthly": "/local_files/exp_wayconnect_0100 PB3_customer_labor_monthly.csv",
      "weekly": "/local_files/exp_wayconnect_0100 PB3_customer_labor_weekly.csv",
    },
    "PB4": {
        "monthly": "/local_files/exp_wayconnect_0100 PB4_customer_labor_monthly.csv",
      "weekly": "/local_files/exp_wayconnect_0100 PB4_customer_labor_weekly.csv",
    },
}

def extract_data(file_path):
    """
    Extract data from a given file path and return a DataFrame.
    """
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return None
    try:
        # Assuming the file uses a semicolon delimiter and has a header
        df = pd.read_csv(file_path, delimiter=';', header=1)
        logging.info(f"Successfully loaded data from {file_path}")
        return df
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None

def clean_and_rename_columns(df):
    """
    Clean and rename columns in the DataFrame.
    - Renames 'Info1 (Mat.Dat.)' to 'Coustmer Type'.
    - Renames 'Arbeitsplatznummer' to 'SMT Type'.
    - Converts month-year and week-year columns to a unified 'Period' format.
    """
    if df is None:
        logging.warning("DataFrame is empty. Cannot clean and rename columns.")
        return None

    # Rename 'Info1 (Mat.Dat.)' to 'Coustmer Type'
    potential_columns = [col for col in df.columns if re.search(r'Info1.*Mat\.Dat\.', col)]
    if potential_columns:
        df.rename(columns={potential_columns[0]: 'Coustmer Type'}, inplace=True)

    # Rename Month-Year and Week-Year columns to a unified 'Period' format
    period_columns = {}
    for col in df.columns:
        # Match Month-Year columns (e.g., Ecktermin 🔑:MM.YYYY,...)
        if re.search(r'Ecktermin .*:\d{2}\.\d{4},.*', col):
            new_col_name = re.sub(r'Ecktermin .*:(\d{2}\.\d{4}),.*', r'\1', col)
            period_columns[col] = new_col_name

    # Rename weekly period columns
    week_year_columns = [col for col in df.columns if re.search(r'Ecktermin 🔑:W\d{2} \d{4},Rest-Belastung Gesamt Personal', col)]
    for col in week_year_columns:
        # Extract only the week number (WXX) and rename to KWXX
        new_col_name = re.sub(r'Ecktermin 🔑:W(\d{2}) \d{4},Rest-Belastung Gesamt Personal', r'KW\1', col)
        df.rename(columns={col: new_col_name}, inplace=True)

    # Apply renaming for all identified Period columns
    df.rename(columns=period_columns, inplace=True)

    # Drop unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Clean 'Coustmer Type' column
    if "Coustmer Type" in df.columns:
        df["Coustmer Type"] = df["Coustmer Type"].str.replace(r'[+"-]', '', regex=True).str.strip()

    logging.info(f"Cleaned and renamed columns: {df.columns.tolist()}")
    return df

def process_pb_file(pb_type, frequency):
    """
    Process a single PB file (weekly or monthly) for a given PB type.
    """
    file_path = PB_INPUT_FILES.get(pb_type, {}).get(frequency)
    if not file_path:
        logging.warning(f"No file path found for {pb_type} {frequency}.")
        return None

    df = extract_data(file_path)
    if df is not None:
        df = clean_and_rename_columns(df)
    return df
