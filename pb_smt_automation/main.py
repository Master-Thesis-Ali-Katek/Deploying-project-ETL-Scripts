import os
import yaml
import pandas as pd
import sys
import re
import logging

# Add project root to Python path
#sys.path.append(os.path.abspath("C:/Users/PATANS/Downloads/pb_smt_data_automation"))
project_root = os.path.abspath(os.path.dirname(__file__))  # Gets the current script's directory
sys.path.append(project_root)  # Adds the project root dynamically
print(f"📂 Project Root Added to Path: {project_root}")
# Import modules
from pb_operations.data_extraction import extract_data
from pb_operations.clean_rename import clean_and_rename_columns
from pb_operations.data_unpivoting import unpivot_data
from pb_operations.append import append_to_master_file
from pb_operations.seperating_first_line import process_pb_files, save_combined_production_hours


from smt_operations.extraction import extract_smt_data
from smt_operations.clean_rename import clean_and_rename_smt_columns
from smt_operations.data_unpivoting import unpivot_smt_data
from smt_operations.append import append_to_master_smt_file

from smt_load_operations.extraction import extract_smt_load_data
from smt_load_operations.clean_rename import rename_columns_for_12_months, rename_columns_for_5_quarters
from smt_load_operations.data_unpivoting import unpivot_smt_load_table, add_belastungsart_column
from smt_load_operations.append import append_to_master_smt_load_file
#from utility_functions import process_file
from cleanup_old_data import delete_old_data_from_output_files
from helpers import add_date_and_extract_columns , map_week_to_month_and_quarter # Common helper


def load_config(config_path):
    """
    Load the YAML configuration file.  
    """
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        return None
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def main():
    # Define the output folder path
    output_folder = "/main/pb_smt_data_automation/processed_outputs"
    os.makedirs(output_folder, exist_ok=True)  # Ensure directory exists

    # Step 1: Perform data cleanup
    print("Deleting old data from processed output files...")
    delete_old_data_from_output_files(output_folder, months_to_keep=8, date_column="Date", date_format='%Y-%m-%d')

    # Step 2: Proceed with your existing workflow
    process_files(config, base_output_folder)

def process_pb_combined_hours(base_output_folder):
    """
    Process PB files for combined production hours.
    Extracts data, unpivots, and saves weekly and monthly combined files, including additional attributes.
    """
    # Define local lists to store production hours
    total_production_hours_weekly = []
    total_production_hours_monthly = []

    # Process PB files
    process_pb_files(total_production_hours_weekly, total_production_hours_monthly)

    # Save unpivoted weekly production hours
    weekly_output_file = os.path.join(base_output_folder, "combined_weekly_production_hours.xlsx")
    monthly_output_file = os.path.join(base_output_folder, "combined_monthly_production_hours.xlsx")
    
    # Save the base combined files (already includes unpivoted data)
    save_combined_production_hours(total_production_hours_weekly, weekly_output_file)
    save_combined_production_hours(total_production_hours_monthly, monthly_output_file)

    # Load the saved files for further processing
    weekly_df = pd.read_excel(weekly_output_file)
    monthly_df = pd.read_excel(monthly_output_file)

    # Add 'Month', 'Week', and 'Quarter' columns to the unpivoted files
    weekly_df = add_date_and_extract_columns(weekly_df, period_column='Period')
    monthly_df = add_date_and_extract_columns(monthly_df, period_column='Period')

    # Map 'Month' and 'Quarter' from monthly to weekly
    weekly_df = map_week_to_month_and_quarter(weekly_df, monthly_df)

    # Save the new files with additional attributes
    weekly_with_date_output = os.path.join(base_output_folder, "save_combined_production_weekly_date.xlsx")
    monthly_with_date_output = os.path.join(base_output_folder, "save_combined_production_monthly_date.xlsx")

    try:
        weekly_df.to_excel(weekly_with_date_output, index=False)
        logging.info(f"Weekly production hours with dates saved to {weekly_with_date_output}")
    except Exception as e:
        logging.error(f"Error saving weekly production hours with dates: {e}")

    try:
        monthly_df.to_excel(monthly_with_date_output, index=False)
        logging.info(f"Monthly production hours with dates saved to {monthly_with_date_output}")
    except Exception as e:
        logging.error(f"Error saving monthly production hours with dates: {e}")



def process_single_file(process_type, frequency, file_path, clean_rename_func, unpivot_func, master_file_path, extraction_func):
    """
    Process a single PB or SMT file and append results to the master file.
    """
    print(f"\n>> Processing {process_type} | Frequency: {frequency}")
    print(f"File Path: {file_path}")

    # Step 1: Extract Data
    df = extraction_func(file_path)
    if df is None or df.empty:
        print(f"Error: Data extraction failed for {process_type} - {frequency}.")
        return None

    # Step 2: Clean and Rename Columns
    df_cleaned = clean_rename_func(df)
    if df_cleaned is None or df_cleaned.empty:
        print(f"Error: Cleaning and renaming failed for {process_type} - {frequency}.")
        return None

    # Step 3: Unpivot Data
    if "PB" in process_type:
        # Pass PB type to ensure correct labeling
        df_unpivoted = unpivot_func(df_cleaned, pb_type=process_type)
    else:
        # For SMT, pass frequency
        df_unpivoted = unpivot_func(df_cleaned, frequency)

    if df_unpivoted is None or df_unpivoted.empty:
        print(f"Error: Unpivoting failed for {process_type} - {frequency}.")
        return None

    # Step 4: Add Date, Month, Week, and Quarter
    df_final = add_date_and_extract_columns(df_unpivoted, period_column='Period')

    # Step 5: Append to Master File
    append_to_master_file(df_final, master_file_path)

    print(f"Successfully processed and appended {process_type} - {frequency} to master file.")
    return df_final


def process_smt_load_file(file_path, master_file_path, rename_func, suffix):
    """
    Process SMT Load Table (12 months or 5 quarters).
    """
    print(f"\n>> Processing SMT Load Table | {suffix}")
    print(f"File Path: {file_path}")

    # Step 1: Extract Data
    df = extract_smt_load_data(file_path)
    if df is None or df.empty:
        print(f"Error: Data extraction failed for SMT Load - {suffix}.")
        return None

    # Step 2: Rename Columns
    df_renamed = rename_func(df)

    # Step 3: Separate SMT0 Rows
    smt0_rows = df_renamed[df_renamed.iloc[:, 0] == 'SMT0']
    df_renamed = df_renamed[df_renamed.iloc[:, 0] != 'SMT0']

    # Step 4: Unpivot Data
    df_unpivoted = unpivot_smt_load_table(df_renamed)
    smt0_unpivoted = unpivot_smt_load_table(smt0_rows)

    # Step 5: Add Belastungsart to SMT0 rows
    smt0_unpivoted = add_belastungsart_column(smt0_unpivoted)

    # Step 6: Append to Master File
    append_to_master_smt_load_file(df_unpivoted, master_file_path)
    print(f"Successfully processed and appended SMT Load {suffix} to master file.")


def process_files(config, base_output_folder):
    """
    Orchestrates processing for PB, SMT, and SMT Load files.
    """
    #Process PB Combined Hours
    process_pb_combined_hours(base_output_folder)
    # PB Processing
    pb_input_files = config['data_extraction']['pb_input_files']
    pb_master_file_path_monthly = os.path.join(base_output_folder, "pb_master_monthly.xlsx")
    pb_master_file_path_weekly = os.path.join(base_output_folder, "pb_master_weekly.xlsx")

    for pb_type, frequencies in pb_input_files.items():
        for frequency, file_path in frequencies.items():
            process_single_file(
                process_type=pb_type,
                frequency=frequency,
                file_path=file_path,
                clean_rename_func=clean_and_rename_columns,
                unpivot_func=unpivot_data,
                master_file_path=(pb_master_file_path_monthly if frequency == 'monthly' else pb_master_file_path_weekly),
                extraction_func=extract_data,
            )

    # SMT Processing
    smt_input_files = config['data_extraction']['smt_input_files']
    smt_master_file_path_monthly = os.path.join(base_output_folder, "smt_master_monthly.xlsx")
    smt_master_file_path_weekly = os.path.join(base_output_folder, "smt_master_weekly.xlsx")

    for frequency, file_path in smt_input_files.items():
        process_single_file(
            process_type="SMT",
            frequency=frequency,
            file_path=file_path,
            clean_rename_func=clean_and_rename_smt_columns,
            unpivot_func=unpivot_smt_data,
            master_file_path=(smt_master_file_path_monthly if frequency == 'monthly' else smt_master_file_path_weekly),
            extraction_func=extract_smt_data,
        )

    # SMT Load Processing
    smt_load_files = config['data_extraction'].get('smt_load_files', {})
    smt_load_master_12months = os.path.join(base_output_folder, "smt_load_master_12months.xlsx")
    smt_load_master_5quarters = os.path.join(base_output_folder, "smt_load_master_5quarters.xlsx")

    for suffix, file_path in smt_load_files.items():
        if suffix == '12months':
            process_smt_load_file(file_path, smt_load_master_12months, rename_columns_for_12_months, suffix)
        elif suffix == '5quarters':
            process_smt_load_file(file_path, smt_load_master_5quarters, rename_columns_for_5_quarters, suffix)


if __name__ == "__main__":
    # Load configuration
    config_path = "config/config.yaml"
    config = load_config(config_path)

    # Define base output folder
    base_output_folder = "/main/pb_smt_data_automation/processed_outputs"
    os.makedirs(base_output_folder, exist_ok=True)  # Ensure directory exists


    if config is not None:
        os.makedirs(base_output_folder, exist_ok=True)
        process_files(config, base_output_folder)
        print("PB, SMT, and SMT Load processing completed successfully!")
    else:
        print("Configuration could not be loaded.")
