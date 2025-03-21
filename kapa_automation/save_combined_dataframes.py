import pandas as pd
import os
import logging
from datetime import datetime

def save_combined_dataframes(monthly, weekly, output_dir):
    # Validate inputs
    if not isinstance(monthly, pd.DataFrame) or not isinstance(weekly, pd.DataFrame):
        raise ValueError("Both 'monthly' and 'weekly' must be pandas DataFrames.")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Define file paths
    monthly_path = os.path.join(output_dir, "master_file_monthly.xlsx")
    weekly_path = os.path.join(output_dir, "master_file_weekly.xlsx")

    def _safe_save(new_data, path):
        if new_data.empty:
            logging.warning(f"No data to save for {path}. Skipping.")
            return
        
        # Add "Date" column if missing
        if "Date" not in new_data.columns:
            new_data["Date"] = datetime.now().strftime("%d.%m.%Y %H:%M")
        
        try:
            # Append to existing data
            existing = pd.read_excel(path) if os.path.exists(path) else pd.DataFrame()
            combined = pd.concat([existing, new_data], ignore_index=True)
            combined = combined.drop_duplicates()  # Remove duplicates
            combined.to_excel(path, index=False, engine="openpyxl")
            logging.info(f"Saved {len(new_data)} rows to {path}")
        except Exception as e:
            logging.error(f"Failed to save {path}: {str(e)}")

    # Save monthly and weekly data
    _safe_save(monthly, monthly_path)
    _safe_save(weekly, weekly_path)