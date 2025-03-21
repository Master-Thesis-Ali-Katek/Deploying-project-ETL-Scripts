import logging
import pandas as pd
import os
import yaml
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def filter_columns(df):
    required_columns = ['PB Type', 'Period', 'Value', 'Attribute', 'Date']
    return df[[col for col in required_columns if col in df.columns]]

def preprocess_data(df, is_weekly=False):
    # Clean columns
    columns_to_remove = ['Month', 'Quarter', 'Week', 'Extra Column']
    df = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors='ignore')
    
    # Format period for weekly data
    if is_weekly:
        df['Period'] = df['Period'].str.replace(r'wk\.(\d{2})\.\d{4}', r'KW\1', regex=True)
    
    # Add current timestamp with minutes precision
    df['Date'] = pd.to_datetime(datetime.now().replace(minute=0, second=0, microsecond=0))

    return df

def append_data_to_combined(data_frames, monthly_combined, weekly_combined):
    valid_keys = [
        "Urlaubsquoten(Plan)_Monthly", "Urlaubsquoten(Plan)_Weekly",
        "Krankheitsquoten(Plan)_Monthly", "Krankheitsquoten(Plan)_Weekly",
        "Mitarbeiter(IST)_Monthly", "Mitarbeiter(IST)_Weekly",
        "Gleitzeit(Plan)_Monthly", "Gleitzeit(Plan)_Weekly",
        "Verteilzeit(Plan)_Monthly", "Verteilzeit(Plan)_Weekly",
        "Arbeitstage_Monthly", "Arbeitstage_Weekly",
        "Kurzarbeitstage(Plan)_Monthly", "Kurzarbeitstage(Plan)_Weekly"
    ]

    for key in valid_keys:
        if key not in data_frames:
            logging.warning(f"Skipping missing table: {key}")
            continue

        is_weekly = "Weekly" in key
        try:
            df = preprocess_data(data_frames[key], is_weekly)
            df = filter_columns(df)
            
            if "Monthly" in key:
                monthly_combined = pd.concat([monthly_combined, df], ignore_index=True)
                logging.info(f"Added {len(df)} rows to monthly from {key}")
            else:
                weekly_combined = pd.concat([weekly_combined, df], ignore_index=True)
                logging.info(f"Added {len(df)} rows to weekly from {key}")
                
        except Exception as e:
            logging.error(f"Error processing {key}: {str(e)}")
            continue

    return monthly_combined, weekly_combined

def save_combined_dataframes(monthly, weekly, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    monthly_path = os.path.join(output_dir, "master_file_monthly.xlsx")
    weekly_path = os.path.join(output_dir, "master_file_weekly.xlsx")

    # ✅ Debugging: Print shapes before and after appending
    print(f"📌 New Monthly Data: {monthly.shape}")
    print(f"📌 New Weekly Data: {weekly.shape}")

    # Save monthly data
    if not monthly.empty:
        try:
            if os.path.exists(monthly_path):
                existing = pd.read_excel(monthly_path)
                logging.info(f"📌 Existing Monthly Records: {len(existing)}")
                combined = pd.concat([existing, monthly], ignore_index=True)
                logging.info(f"📌 Combined Monthly Records: {len(combined)}")
            else:
                combined = monthly
                logging.info("📌 No existing monthly file found. Creating new file.")

            # ✅ Save to Excel
            combined.to_excel(monthly_path, index=False, engine='openpyxl')
            logging.info(f"✔ Monthly file updated. Total records: {len(combined)}")

        except Exception as e:
            logging.error(f"⚠ Monthly save failed: {str(e)}")

    # Save weekly data
    if not weekly.empty:
        try:
            if os.path.exists(weekly_path):
                existing = pd.read_excel(weekly_path)
                logging.info(f"📌 Existing Weekly Records: {len(existing)}")
                combined = pd.concat([existing, weekly], ignore_index=True)
                logging.info(f"📌 Combined Weekly Records: {len(combined)}")
            else:
                combined = weekly
                logging.info("📌 No existing weekly file found. Creating new file.")

            # ✅ Save to Excel
            combined.to_excel(weekly_path, index=False, engine='openpyxl')
            logging.info(f"✔ Weekly file updated. Total records: {len(combined)}")

        except Exception as e:
            logging.error(f"⚠ Weekly save failed: {str(e)}")


if __name__ == "__main__":
    # Use the correct path based on the environment
    if os.getenv("RUNNING_IN_DOCKER"):  # If running inside Docker
        config_path = "/main/config/config.yaml"
    else:  # If running locally on Windows
        config_path = r"C:\Users\PATANS\Downloads\kapa_automation\config\config.yaml"

    print(f"✅ Using config path: {config_path}")  # Debugging line

    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            
        output_dir = config.get('output_dir', os.getcwd())
        
        # Initialize containers
        monthly_data = pd.DataFrame()
        weekly_data = pd.DataFrame()

        # Load your actual data here
        data_frames = {
            "Urlaubsquoten_Plan_Monthly": pd.read_excel("your_source_file.xlsx"),
            # Add other tables similarly
        }

        # Process data
        monthly_data, weekly_data = append_data_to_combined(
            data_frames, monthly_data, weekly_data
        )

        # Save results
        save_combined_dataframes(monthly_data, weekly_data, output_dir)
        logging.info("Process completed successfully")

    except Exception as e:
        logging.error(f"Critical failure: {str(e)}")
        exit(1)