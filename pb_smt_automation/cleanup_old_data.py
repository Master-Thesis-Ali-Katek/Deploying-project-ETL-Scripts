import os
import pandas as pd
from datetime import datetime, timedelta

def delete_old_data(file_path, date_column='Date', months_to_keep=8, date_format='%Y-%m-%d'):
    """
    Delete data older than a specified number of months from an Excel file.

    :param file_path: Path to the Excel file.
    :param date_column: Column containing the date information (default is 'Date').
    :param months_to_keep: Number of months to retain data (default is 8).
    :param date_format: Date format in the date column (default is '%Y-%m-%d').
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        # Load the data from the Excel file
        df = pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    if date_column not in df.columns:
        print(f"Column '{date_column}' not found in the file.")
        return

    # Calculate the cutoff date
    cutoff_date = datetime.now() - timedelta(days=months_to_keep * 30)

    # Convert the 'Date' column to datetime for filtering
    try:
        df[date_column] = pd.to_datetime(df[date_column], format=date_format)
    except Exception as e:
        print(f"Error converting the '{date_column}' column to datetime: {e}")
        return

    # Filter the DataFrame to retain only rows newer than the cutoff date
    filtered_df = df[df[date_column] >= cutoff_date]

    print(f"Original rows: {len(df)} | Rows after filtering: {len(filtered_df)}")

    # Save the filtered DataFrame back to the Excel file
    try:
        filtered_df.to_excel(file_path, index=False, engine='openpyxl')
        print(f"Updated file saved: {file_path}")
    except Exception as e:
        print(f"Error saving the updated file: {e}")


def delete_old_data_from_output_files(output_folder, months_to_keep=8, date_column='Date', date_format='%Y-%m-%d'):
    """
    Iterate over all relevant Excel files in the output folder and delete data older than a specified number of months.

    :param output_folder: Folder containing all processed output files.
    :param months_to_keep: Number of months to retain data (default is 8).
    :param date_column: Column containing the date information (default is 'Date').
    :param date_format: Date format in the date column (default is '%Y-%m-%d').
    """
    if not os.path.exists(output_folder):
        print(f"Output folder not found: {output_folder}")
        return

    # Iterate through all Excel files in the output folder
    for root, _, files in os.walk(output_folder):
        for file in files:
            if file.endswith(".xlsx"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")

                # Apply the delete_old_data function
                delete_old_data(
                    file_path=file_path,
                    date_column=date_column,
                    months_to_keep=months_to_keep,
                    date_format=date_format
                )
