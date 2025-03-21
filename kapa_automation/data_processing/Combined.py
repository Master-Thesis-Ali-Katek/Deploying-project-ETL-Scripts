from datetime import datetime
import pandas as pd
import os
import logging
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def filter_columns(df):
    """Retain required columns and ensure proper formatting."""
    required_columns = ['PB Type', 'Period', 'Value', 'Attribute', 'Date']
    return df[[col for col in required_columns if col in df.columns]]

def filter_and_stamp_data(df):
    """Ensure all rows have the latest execution timestamp."""
    try:
        # Convert Date column to datetime format
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(
                df['Date'], format='%d.%m.%Y %H:%M', errors='coerce'
            )

        # ✅ Update all rows with the current execution timestamp
        df['Date'] = pd.to_datetime(datetime.now().replace(minute=0, second=0, microsecond=0))  # Ensure proper format
        
        return df

    except Exception as e:
        logging.error(f"Date processing error: {str(e)}")
        return df


def save_data_with_append(new_monthly, new_weekly, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    monthly_path = os.path.join(output_dir, "master_file_monthly.xlsx")
    weekly_path = os.path.join(output_dir, "master_file_weekly.xlsx")

    def _safe_save(new_data, path):
        if not new_data.empty:
            try:
                # Read existing file if available
                if os.path.exists(path):
                    existing = pd.read_excel(path)
                    logging.info(f"📌 Existing records in {path}: {len(existing)}")
                else:
                    existing = pd.DataFrame()
                    logging.info(f"📌 No existing file found. Creating {path}.")
                
                # Append new data, remove duplicates
                combined = pd.concat([existing, new_data], ignore_index=True)
                combined = combined.drop_duplicates(
                    subset=['PB Type', 'Period', 'Attribute', 'Date'], 
                    keep='last'
                )

                logging.info(f"📌 After appending: {len(combined)} total rows in {path}")

                # Save updated data
                combined.to_excel(path, index=False, engine='openpyxl')
                logging.info(f"✔ Successfully saved {path}")

            except Exception as e:
                logging.error(f"⚠ Save failed for {path}: {str(e)}")
                raise


    try:
        _safe_save(new_monthly, monthly_path)
        _safe_save(new_weekly, weekly_path)
    except Exception as e:
        logging.error(f"Error during save_data_with_append: {str(e)}")
        raise

def process_production_data(config):
    """Process production data from source files."""
    try:
        paths = config['combined_total_production_hours']
        
        # Check if 'output_dir' exists in paths, otherwise use a default value
        output_dir = paths.get('output_dir', './output')  # Default to './output' if not specified
        os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
        
        # Read source files
        monthly_df = pd.read_excel(paths['monthly'])  # Read from source
        weekly_df = pd.read_excel(paths['weekly'])
        
        # Process and append
        stamped_monthly = filter_and_stamp_data(filter_columns(monthly_df))
        stamped_weekly = filter_and_stamp_data(filter_columns(weekly_df))
        
        save_data_with_append(stamped_monthly, stamped_weekly, output_dir)
        
        logging.info("Production data appended successfully")
        return True
    except KeyError as e:
        logging.error(f"Missing key in config: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Production processing failed: {str(e)}")
        return False