import logging
import pandas as pd
import os
import numpy as np
from data_processing.extract_tables import extract_tables
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_utilization(df, personal_factor_df):
    try:
        personal_factor_constant = (personal_factor_df['Personal\nFactor'] * personal_factor_df['Result']).sum()
        logging.info(f"Personal Factor Constant: {personal_factor_constant}")

        # Ensure Date is parsed correctly
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

        # Check for invalid dates
        if df['Date'].isna().sum() > 0:
            logging.warning("Some dates could not be parsed correctly. Check the format in Excel.")

        today = datetime.now().date()  # Use only the date (ignore time)

        # Clean up column types
        df['Attribute'] = df['Attribute'].astype(str).str.strip()
        df['PB Type'] = df['PB Type'].astype(str).str.strip()
        df['Period'] = df['Period'].astype(str).str.strip()

        def calculate_row(row):
            pb_type = str(row['PB Type']).strip()
            period = str(row['Period']).strip()

            # Filter today's data
            df_today = df[
                (df['PB Type'] == pb_type) & 
                (df['Period'] == period) & 
                (df['Date'].dt.date == today)
            ]

            if df_today.empty:
                logging.warning(f"No data found for PB Type: {pb_type}, Period: {period} on {today}")
                return np.nan

            df_today = df_today.drop_duplicates(subset=['PB Type', 'Period', 'Attribute'], keep='last')

            # PB1 uses "Production Hours" and "Kurzarbeitsplanung"
            if pb_type == 'PB1':
                production_hours = df_today[df_today['Attribute'] == 'Production Hours']['Value'].sum()
                arbeitstage = df_today[df_today['Attribute'] == 'Arbeitstage']['Value'].sum()

                if production_hours > 0 and arbeitstage > 0:
                    utilization_value = (production_hours * 100) / (personal_factor_constant * arbeitstage * 3 * 7.25)
                    logging.info(f"Utilization calculated for PB1 ({period}): {utilization_value:.2f}%")
                    return utilization_value
                else:
                    logging.warning(f"Invalid values for PB1: Production Hours={production_hours}, Arbeitstage={arbeitstage}")
                    return np.nan

            # Other PB Types use "MitarbeiterbedarfBrutto" and "Mitarbeiter"
            else:
                mitarbeiterbedarf_brutto = df_today[df_today['Attribute'] == 'Mitarbeiterbedarf_Brutto(Plan)']['Value'].sum()
                mitarbeiter = df_today[df_today['Attribute'] == 'Mitarbeiter(IST)']['Value'].sum()

                if mitarbeiter <= 0:
                    logging.warning(f"No Mitarbeiter data for PB{pb_type}, skipping calculation.")
                    return np.nan

                utilization_value = (mitarbeiterbedarf_brutto / mitarbeiter) * 100
                logging.info(f"Utilization calculated for PB{pb_type} ({period}): {utilization_value:.2f}%")
                return utilization_value

        utilization_table = df[['Period', 'PB Type']].drop_duplicates()
        utilization_table['Attribute'] = 'Utilization'
        utilization_table['Value'] = utilization_table.apply(calculate_row, axis=1)
        utilization_table['Date'] = pd.to_datetime(datetime.now().replace(minute=0,second=0, microsecond=0))

        return utilization_table.dropna(subset=['Value'])

    except Exception as e:
        logging.error(f"Error calculating utilization: {e}", exc_info=True)
        return pd.DataFrame()


def process_utilization(file_path, personal_factor_df, output_dir):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        logging.info(f"Processing file: {file_path}")
        df = pd.read_excel(file_path, sheet_name='Sheet1')

        # Ensure 'Value' column is numeric
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce').fillna(0)

        # Ensure 'Date' column is in datetime format
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

        # Check for invalid dates and drop rows with NaT
        if df['Date'].isna().sum() > 0:
            logging.warning(f"Invalid or missing dates detected in {file_path}. Dropping these rows.")
            df = df.dropna(subset=['Date'])

        today = datetime.now().date()

        # Remove existing utilization entries for today's date
        df = df[~((df['Attribute'] == 'Utilization') & (df['Date'].dt.date == today))]

        # Calculate utilization
        utilization_table = calculate_utilization(df, personal_factor_df)

        if utilization_table.empty:
            logging.warning(f"No utilization data calculated for {file_path}")
            return

        # ✅ Debugging: Print shapes before appending
        print(f"📌 Existing Data Before Appending: {df.shape}")
        print(f"📌 New Utilization Rows to Append: {utilization_table.shape}")

        # ✅ Append the calculated utilization rows to the existing DataFrame
        df_combined = pd.concat([df, utilization_table], ignore_index=True).drop_duplicates(
            subset=['Period', 'PB Type', 'Attribute', 'Date'], keep='last'
        )

        print(f"📌 Final Data After Appending: {df_combined.shape}")

        # Save updated data
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, os.path.basename(file_path))

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_combined.to_excel(writer, sheet_name='Sheet1', index=False, header=True)

        logging.info(f"✔ Utilization calculation completed and saved to: {output_path}")

    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}", exc_info=True)


if __name__ == "__main__":
    master_monthly_path = "master_file_monthly.xlsx"
    master_weekly_path = "master_file_weekly.xlsx"
    output_directory = "processed_outputs"

    # Extract Personal Factor Table
    try:
        data_frames = extract_tables()
        if 'Personal_Factor' in data_frames:
            personal_factor_df = data_frames['Personal_Factor']
        else:
            raise KeyError("Personal_Factor table missing.")
    except Exception as e:
        logging.error(f"Error extracting Personal_Factor table: {e}")
        personal_factor_df = None

    # Calculate Utilization if Personal Factor is available
    if personal_factor_df is not None:
        process_utilization(master_monthly_path, personal_factor_df, output_directory)
        process_utilization(master_weekly_path, personal_factor_df, output_directory)
