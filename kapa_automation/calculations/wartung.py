import logging
import os
import pandas as pd
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_wartung(value, personal_factor_avg):
    """Calculate wartung value safely."""
    try:
        if pd.isna(value) or pd.isna(personal_factor_avg) or personal_factor_avg == 0:
            logging.warning("Skipping wartung calculation due to invalid input values.")
            return None
        return (value * 8) / (200 * personal_factor_avg)
    except Exception as e:
        logging.error(f"Error calculating wartung: {e}")
        return None


def filter_today_data(df):
    """Filter today's data while preserving original timestamps."""
    if 'Date' not in df.columns:
        logging.warning("No 'Date' column found. Returning empty DataFrame.")
        return pd.DataFrame(columns=df.columns)
    
    try:
        # Ensure 'Date' column is in datetime format
        df = df.copy()  # Prevents SettingWithCopyWarning
        df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y %H:%M', errors='coerce')

        today = datetime.now().strftime('%d.%m.%Y')
        today_df = df[df['Date'].dt.strftime('%d.%m.%Y') == today].reset_index(drop=True)
        return today_df
    except Exception as e:
        logging.error(f"Date filtering error: {e}")
        return pd.DataFrame(columns=df.columns)


def process_wartung(file_name, personal_factor_avg, output_dir):
    """Process wartung calculation and append to file only for specific conditions."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, file_name)
        required_columns = ['Attribute', 'PB Type', 'Value', 'Period', 'Date']

        # Load or create the master file
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path, engine='openpyxl')

            # Ensure all required columns are present
            if not all(col in existing_df.columns for col in required_columns):
                raise ValueError(f"Missing required columns in {file_name}")

            # Convert the 'Date' column to datetime
            existing_df = existing_df.copy()
            existing_df['Date'] = pd.to_datetime(
                existing_df['Date'], format='%d.%m.%Y %H', errors='coerce'
            )
        else:
            logging.info(f"File not found. Creating new file: {file_path}")
            existing_df = pd.DataFrame(columns=required_columns)

        # Get today's date
        today = datetime.now().strftime('%d.%m.%Y')

        # Check if wartung for today already exists
        if not existing_df.empty and any(
            (existing_df['Attribute'] == 'Wartung') &
            (existing_df['Date'].dt.strftime('%d.%m.%Y') == today)
        ):
            logging.info(f"Wartung for {today} already exists in {file_name}. Skipping.")
            return

        # Filter today's data excluding rows already processed as 'Wartung'
        today_df = filter_today_data(existing_df)
        if today_df.empty:
            logging.info(f"No data for today's date ({today}). Skipping.")
            return

        # Filter rows that match specific conditions
        unprocessed_df = today_df[
            (today_df['Attribute'] == 'Production Hours') &  # Filter by 'Attribute'
            (today_df['PB Type'] == 'PB1')                   # Filter by 'PB Type'
        ].copy()  # Explicit copy to avoid modifying original df

        if unprocessed_df.empty:
            logging.info(f"No new data matching conditions in {file_name}. Skipping wartung calculation.")
            return

        # Create wartung entries for unprocessed rows
        wartung_df = unprocessed_df.copy()
        wartung_df['Attribute'] = 'Wartung'
        wartung_df['Value'] = wartung_df['Value'].apply(
            lambda x: calculate_wartung(x, personal_factor_avg)
        )

        # Append wartung entries to the master file without altering other rows
        updated_df = pd.concat([existing_df, wartung_df], ignore_index=True)

        # Save the updated file
        updated_df.to_excel(file_path, index=False, engine='openpyxl')
        logging.info(f"Appended {len(wartung_df)} wartung entries to {file_name}.")

    except Exception as e:
        logging.error(f"Error processing {file_name}: {e}", exc_info=True)
        raise
