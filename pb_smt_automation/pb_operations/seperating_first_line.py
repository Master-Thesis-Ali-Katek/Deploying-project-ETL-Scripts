import os
import pandas as pd
import logging
from pb_operations.data_processing import process_pb_file
from utility_functions import unpivot_combined_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_pb_files(total_production_hours_weekly, total_production_hours_monthly):
    """
    Process PB files for combined production hours.
    Extracts the first row for production hours and appends them to the provided lists.
    """
    # Define PB types and frequencies
    pb_types = ["PB1", "PB2", "PB3", "PB4"]
    frequencies = ["weekly", "monthly"]

    for pb in pb_types:
        for freq in frequencies:
            logging.info(f"Processing {pb} {freq} file.")

            # Extract and clean the data
            df = process_pb_file(pb, freq)
            if df is None or df.empty:
                logging.warning(f"No data extracted for {pb} {freq}. Skipping.")
                continue

            # Extract the first row for production hours
            production_hours_row = df.iloc[0].copy()
            production_hours_row["PB Type"] = pb

            # Append to the appropriate list
            if freq == "weekly":
                total_production_hours_weekly.append(production_hours_row)
            elif freq == "monthly":
                total_production_hours_monthly.append(production_hours_row)

            logging.info(f"Extracted first row for {pb} {freq}.")

            # Log unpivoted data for debugging
            unpivoted_df = unpivot_combined_data(df)
            if unpivoted_df is not None:
                logging.info(f"Unpivoted data for {pb} {freq} is ready for further processing.")


def save_combined_production_hours(hours_list, output_file_name):
    """
    Combine, unpivot, and append production hours into a single Excel file.
    Combines rows into a DataFrame, unpivots it, appends to the existing file if available, and saves the result.
    """
    if not hours_list:
        logging.warning(f"No data to combine for {output_file_name}.")
        return
    logging.info(f"Number of rows in hours_list for {output_file_name}: {len(hours_list)}")

    # Combine rows into a DataFrame
    combined_df = pd.DataFrame(hours_list)

    if combined_df.empty:
        logging.warning(f"Combined DataFrame is empty for {output_file_name}.")
        return
    logging.info(f"Shape of combined DataFrame for {output_file_name}: {combined_df.shape}")

    # Normalize column names
    combined_df.columns = combined_df.columns.str.strip()

    # Reorder columns to place PB Type first
    if "PB Type" in combined_df.columns:
        columns = ["PB Type"] + [col for col in combined_df.columns if col != "PB Type"]
        combined_df = combined_df[columns]

    # Unpivot the combined DataFrame
    unpivoted_df = unpivot_combined_data(combined_df)
    if unpivoted_df is None or unpivoted_df.empty:
        logging.warning(f"Unpivoted DataFrame is empty for {output_file_name}.")
        return

    # Append to the existing file if it exists, otherwise create a new file
    try:
        if os.path.exists(output_file_name):
            # Load existing data
            existing_data = pd.read_excel(output_file_name, engine='openpyxl')
            logging.info(f"Existing file found: {output_file_name}, shape: {existing_data.shape}")
        else:
            existing_data = pd.DataFrame()

        # Combine existing and new data
        combined_data = pd.concat([existing_data, unpivoted_df], ignore_index=True)

        # Save the combined data back to the file
        combined_data.to_excel(output_file_name, index=False, engine='openpyxl')
        logging.info(f"Unpivoted production hours successfully appended and saved to {output_file_name}")
    except PermissionError:
        logging.error(f"Permission denied: Unable to write to {output_file_name}. Please close the file and try again.")
    except Exception as e:
        logging.error(f"Error saving appended file {output_file_name}: {e}")
