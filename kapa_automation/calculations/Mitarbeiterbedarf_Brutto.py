import logging
import pandas as pd
import numpy as np
import os
from datetime import datetime
from data_processing.extract_tables import extract_tables
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
try:
    data_frames = extract_tables()
    logging.info(f"Extracted tables: {list(data_frames.keys())}")
except Exception as e:
    logging.error(f"Failed to extract tables: {e}")
    data_frames = {}

def calculate_mitarbeiterbedarf(row, original_table):
    """Calculate the Mitarbeiterbedarf value for a given row."""
    try:
        current_pb_type = row['PB Type'].replace(" ", "")
        current_period = row['Period']
        today = datetime.now().date()  # Current date without time

        # Normalize PB Type and remove spaces for consistent comparison
        original_table['PB Type'] = original_table['PB Type'].astype(str).str.replace(r"\s+", "", regex=True).str.strip()
        current_pb_type = current_pb_type.replace(" ", "")

        # Ensure 'Date' is in datetime format
        original_table['Date'] = pd.to_datetime(original_table['Date'], errors='coerce')

        # Filter the original table for matching PB Type, Period, and today's date
        matching_rows = original_table[
            (original_table['PB Type'] == current_pb_type) &
            (original_table['Period'] == current_period) &
            (original_table['Date'].dt.date == today)
        ]

        if matching_rows.empty:
            logging.warning(f"No data found for PB Type: {current_pb_type}, Period: {current_period} on {today}. Check input data.")
            return np.nan

        # Calculate total production hours
        prod_hours_mask = (
            (matching_rows['Attribute'] == 'Production Hours') |
            ((current_pb_type == 'PB1') & (matching_rows['Attribute'] == 'Wartung'))
        )
        total_production_hours = matching_rows[prod_hours_mask]['Value'].sum()

        if total_production_hours <= 0:
            logging.warning(f"Invalid production hours ({total_production_hours}) for {current_pb_type}, Period {current_period}.")
            return np.nan

        # Calculate employee factor
        employee_factor = matching_rows[
            matching_rows['Attribute'] == 'Arbeitstage'
        ]['Value'].sum() * 7.25

        # Calculate effective availability
        availability_fields = ['Urlaubsquoten(Plan)', 'Krankheitsquoten(Plan)', 'Gleitzeit(Plan)', 'Verteilzeit(Plan)']
        availability_values = matching_rows[
            matching_rows['Attribute'].isin(availability_fields)
        ]['Value'].sum()
        effective_availability = 1 - (availability_values / 100)

        if 'SMT_OEE' in data_frames and not data_frames['SMT_OEE'].empty:
            extracted_oee = data_frames['SMT_OEE'].iloc[0, 0] / 100  # Convert percentage to decimal
        else:
            logging.warning("OEE data is missing! Using default OEE = 0.807 for PB1.")
            extracted_oee = 0.807  # Default fallback value

        # ✅ Use extracted OEE dynamically in calculations
        oee_adjusted = extracted_oee if current_pb_type == 'PB1' else 1
        # OEE Adjustment
        #oee_adjusted = 0.807 if current_pb_type == 'PB1' else 1

        denominator = employee_factor * effective_availability * oee_adjusted
        if denominator <= 0:
            logging.warning(f"Denominator {denominator} invalid for {current_pb_type}, Period {current_period}.")
            return np.nan

        mitarbeiterbedarf = total_production_hours / denominator
        logging.info(f"Calculated value for {current_pb_type} Period {current_period}: {mitarbeiterbedarf:.2f}")
        return mitarbeiterbedarf

    except Exception as e:
        logging.error(f"Calculation error: {str(e)}", exc_info=True)
        return np.nan


def process_file(input_path, output_dir):
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Read input data
        df = pd.read_excel(input_path, sheet_name='Sheet1')
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        today = datetime.now().date()

        logging.info(f"📌 Initial data rows: {df.shape[0]}")

        # Remove existing entries for today's Mitarbeiterbedarf_Brutto(Plan)
        df_clean = df[~(
            (df['Attribute'] == 'Mitarbeiterbedarf_Brutto(Plan)') &
            (df['Date'].dt.date == today)
        )]

        logging.info(f"📌 Data after removing today's existing values: {df_clean.shape[0]}")

        # Generate new calculations
        calculation_rows = df_clean[['Period', 'PB Type']].copy()
        calculation_rows['Attribute'] = 'Mitarbeiterbedarf_Brutto(Plan)'
        calculation_rows['Value'] = calculation_rows.apply(
            lambda r: calculate_mitarbeiterbedarf(r, df_clean), axis=1
        )
        calculation_rows['Date'] = pd.to_datetime(datetime.now().replace(minute=0, second=0, microsecond=0))

        logging.info(f"📌 New rows to append: {calculation_rows.shape[0]}")

        # ✅ Append new calculations to existing data
        final_df = pd.concat([df_clean, calculation_rows], ignore_index=True)

        # ✅ Drop PB Types ('PB 1', 'PB 2', etc.) before saving
        final_df = final_df[~final_df['PB Type'].isin(['PB 1', 'PB 2', 'PB 3', 'PB 4'])]

        logging.info(f"📌 Final data rows after appending and filtering: {final_df.shape[0]}")

        # Generate output path
        output_path = os.path.join(output_dir, os.path.basename(input_path))

        # ✅ Save to output location
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            final_df.to_excel(writer, sheet_name='Sheet1', index=False)

        logging.info(f"✔ Successfully processed and appended to: {output_path}")

    except Exception as e:
        logging.error(f"Failed to process {input_path}: {str(e)}", exc_info=True)


if __name__ == "__main__":
    # Path configuration
    input_files = {
        "monthly": "master_file_monthly.xlsx",
        "weekly": "master_file_weekly.xlsx"
    }
    output_directory = "processed_outputs"

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Process each file
    for file_type, file_path in input_files.items():
        if os.path.exists(file_path):
            process_file(file_path, output_directory)
        else:
            logging.error(f"Input file not found: {file_path}")
