import logging
import pandas as pd
import numpy as np
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_abweichung(row, original_table):
    """
    Calculate Abweichung by comparing actual staff with MitarbeiterbedarfBrutto for a given PB Type and Period.
    """
    try:
        current_pb_type = row['PB Type']
        current_period = row['Period']
        today = datetime.now().date()  # Consistent datetime format

        # Ensure 'Date' is in consistent format
        original_table['Date'] = pd.to_datetime(original_table['Date'], format='%d.%m.%Y %H:%M', errors='coerce', dayfirst=True)

        # Filter rows for Mitarbeiterbedarf_Brutto(Plan)
        mitarbeiterbedarf_brutto_table = original_table[
            original_table['Attribute'].str.strip() == 'Mitarbeiterbedarf_Brutto(Plan)'
        ]

        mitarbeiterbedarf_brutto_table['Date'] = pd.to_datetime(
            mitarbeiterbedarf_brutto_table['Date'], format='%d.%m.%Y %H:%M', errors='coerce', dayfirst=True
        )

        # Filter Mitarbeiterbedarf_Brutto rows for matching PB Type, Period, and Date
        filtered_bedarf = mitarbeiterbedarf_brutto_table[
            (mitarbeiterbedarf_brutto_table['PB Type'] == current_pb_type) &
            (mitarbeiterbedarf_brutto_table['Period'] == current_period) &
            (mitarbeiterbedarf_brutto_table['Date'].dt.date == today)
        ]

        mitarbeiterbedarf_brutto_value = filtered_bedarf['Value'].iloc[-1] if not filtered_bedarf.empty else 0

        # Get actual staff for today's date
        filtered_staff = original_table[
            (original_table['Attribute'].str.strip() == 'Mitarbeiter(IST)') &
            (original_table['PB Type'] == current_pb_type) &
            (original_table['Period'] == current_period) &
            (original_table['Date'].dt.date == today)
        ]

        actual_staff = filtered_staff['Value'].iloc[-1] if not filtered_staff.empty else 0

        # Calculate Abweichung as the difference between actual staff and MitarbeiterbedarfBrutto
        abweichung = actual_staff - mitarbeiterbedarf_brutto_value

        logging.info(f"Abweichung -> PB Type: {current_pb_type}, Period: {current_period}, "
                     f"Staff: {actual_staff}, Bedarf: {mitarbeiterbedarf_brutto_value}, Result: {abweichung}")

        return abweichung

    except Exception as e:
        logging.error(f"Error calculating Abweichung: {e}")
        return np.nan

def calculate_and_append_abweichung(file_path, output_dir):
    """
    Load the master file, calculate 'Abweichung', and append the results to a new output file.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        logging.info(f"Processing file: {file_path}")
        df = pd.read_excel(file_path, sheet_name='Sheet1')

        # Ensure Value column is numeric and clean up date
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y %H:%M', errors='coerce', dayfirst=True)

        today = datetime.now().date()
        df_filtered = df[df['Date'].dt.date == today]

        if df_filtered.empty:
            logging.warning(f"No data found for today's date {today} in {file_path}. Skipping calculation.")
            return

        logging.info(f"Filtered data for today's date: {df_filtered.shape[0]} rows")

        # Prepare Abweichung calculation table
        abweichung_table = df_filtered[['Period', 'PB Type']].drop_duplicates()
        abweichung_table['Attribute'] = 'Abweichung'
        abweichung_table['Value'] = abweichung_table.apply(
            lambda row: calculate_abweichung(row, df), axis=1
        )
        abweichung_table['Date'] =pd.to_datetime(datetime.now().replace(minute=0, second=0, microsecond=0))  # Consistent datetime format

        logging.info(f"New Abweichung rows calculated: {abweichung_table.shape[0]}")

        if abweichung_table.empty:
            logging.warning(f"No new 'Abweichung' entries to append for {file_path}")
            return

        # ✅ Debugging: Print shapes before appending
        print(f"📌 Existing Data Before Appending: {df.shape}")
        print(f"📌 New Abweichung Rows to Append: {abweichung_table.shape}")

        # ✅ Append the calculated Abweichung rows to the existing DataFrame
        df_combined = pd.concat([df, abweichung_table], ignore_index=True)

        print(f"📌 Final Data After Appending: {df_combined.shape}")

        # Save to the output directory
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, os.path.basename(file_path))

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_combined.to_excel(writer, sheet_name='Sheet1', index=False)

        logging.info(f"✔ Abweichung calculation completed and saved to: {output_path}")

    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}", exc_info=True)


if __name__ == "__main__":
    master_monthly_path = "master_file_monthly.xlsx"
    master_weekly_path = "master_file_weekly.xlsx"
    output_directory = "processed_outputs"

    # Process each file and save results in the output directory
    calculate_and_append_abweichung(master_monthly_path, output_directory)
    calculate_and_append_abweichung(master_weekly_path, output_directory)
