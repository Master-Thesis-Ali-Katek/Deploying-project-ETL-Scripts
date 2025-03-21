import logging
import os
import yaml
import pandas as pd
from data_processing.extract_tables import extract_tables
from data_processing.unpivoted_tables import unpivot_all_tables
from data_processing.append_to_master import append_data_to_combined
from data_processing.Combined import process_production_data, save_data_with_append
from calculations.wartung import process_wartung
from calculations.Mitarbeiterbedarf_Brutto import process_file  # Assuming this function is in `calculations/mitarbeiterbedarf.py`
from calculations.abweichung import calculate_and_append_abweichung
from calculations.utilization import process_utilization  # Assuming the utilization function is defined here

# 1️⃣ Get the base directory where the script is located
base_dir = os.path.abspath(os.path.dirname(__file__))

# 2️⃣ Create a 'logs' folder inside the directory
log_folder = os.path.join(base_dir, 'logs')
os.makedirs(log_folder, exist_ok=True)  # Create the folder if it doesn't exist

# 3️⃣ Print paths for debugging (optional)
print(f"Base directory: {base_dir}")
print(f"Logs folder path: {log_folder}")

# 4️⃣ Create the path for the log file
log_path = os.path.join(log_folder, 'script.log')
print(f"Log file path: {log_path}")

# 5️⃣ Reset previous logging handlers to avoid duplicate logs
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# 6️⃣ Configure the logging system
logging.basicConfig(
    filename=log_path,  # Log file location
    level=logging.INFO,  # Log levels (INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

# 7️⃣ Log initial messages to test
logging.info("Logging system initialized successfully.")
logging.info("This is an info log message.")
logging.warning("This is a warning log message.")
logging.error("This is an error log message.")


def main():
    logging.info("Starting the data processing workflow...")

    # Load configuration
    try:
        # Dynamically set the base directory
        base_dir = os.getenv("BASE_DIR", "/main")  # Default to "/app" in Docker
        config_path = os.path.join(base_dir, "config", "config.yaml")

        print(f"✅ Looking for config at: {config_path}")  # Debugging line

        with open(config_path, "r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
        logging.info("Configuration loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return

    # Setup output directory
    try:
        output_dir = config.get('output_dir', './output')
        os.makedirs(output_dir, exist_ok=True)
        logging.info(f"Output directory set to: {output_dir}")
    except Exception as e:
        logging.error(f"Error setting up output directory: {e}")
        return

    # Extract tables
    try:
        logging.info("Extracting tables...")
        data_frames = extract_tables()
        logging.info("Table extraction complete.")
    except Exception as e:
        logging.error(f"Error during table extraction: {e}")
        return

    # Unpivot tables
    try:
        logging.info("Unpivoting tables...")
        unpivoted_data_frames = unpivot_all_tables(data_frames)
        logging.info("Unpivoting complete.")
    except Exception as e:
        logging.error(f"Error during unpivoting: {e}")
        return

    # Append to master files
    try:
        logging.info("Appending unpivoted data to master files...")
        monthly_combined, weekly_combined = append_data_to_combined(unpivoted_data_frames, pd.DataFrame(), pd.DataFrame())
        
        # Remove unnecessary rows
        monthly_combined = monthly_combined[monthly_combined['PB Type'] != "SMT Gesamt"]
        weekly_combined = weekly_combined[weekly_combined['PB Type'] != "SMT Gesamt"]

        # Save updated master files
        save_data_with_append(monthly_combined, weekly_combined, output_dir)
        logging.info("Unpivoted data appended and master files updated successfully.")
    except Exception as e:
        logging.error(f"Error during data appending: {e}")
        return

    # Process production data
    try:
        logging.info("Processing combined_total_production_hours...")
        process_production_data(config)
        logging.info("Production data processed successfully.")
    except Exception as e:
        logging.error(f"Error during production data processing: {e}")
        return

    # Calculate personal factor average
    try:
        logging.info("Calculating personal_factor_avg...")

        if "Personal_Factor" in data_frames:
            personal_factor_df = data_frames["Personal_Factor"]

        # ✅ Multiply `Personal\nFactor` by `Result`
            weighted_factors = personal_factor_df['Personal\nFactor'] * personal_factor_df['Result']

        # ✅ Sum of `Result` column (denominator)
            result_sum = personal_factor_df['Result'].sum()

        # ✅ Correct calculation: Divide weighted sum by sum of `Result`
            if result_sum > 0:
                personal_factor_avg = weighted_factors.sum() / result_sum
            else:
                personal_factor_avg = 0  # Prevent division by zero
        
            logging.info(f"✔ Corrected personal_factor_avg: {personal_factor_avg}")

        else:
            logging.error("❌ Personal_Factor table is missing.")
            personal_factor_avg = None  # Handle missing case

    except Exception as e:
        logging.error(f"⚠ Error calculating personal_factor_avg: {e}")
        personal_factor_avg = None  # Handle error case


    # Step 7: Wartung Processing
    try:
        logging.info("Processing wartung for master files...")
        process_wartung("master_file_monthly.xlsx", personal_factor_avg, output_dir)
        process_wartung("master_file_weekly.xlsx", personal_factor_avg, output_dir)
        logging.info("Wartung calculation and update completed.")
    except Exception as e:
        logging.error(f"Error processing wartung: {e}")
        return

    # Step 8: Mitarbeiterbedarf Processing
    try:
        input_files = {
            "monthly": os.path.join(output_dir, "master_file_monthly.xlsx"),
            "weekly": os.path.join(output_dir, "master_file_weekly.xlsx")
        }

        for file_type, file_path in input_files.items():
            if os.path.exists(file_path):
                process_file(file_path, output_dir)
            else:
                logging.warning(f"File not found: {file_path}. Skipping processing for {file_type}.")
        
        logging.info("Mitarbeiterbedarf processing completed successfully.")
    except Exception as e:
        logging.error(f"Error during mitarbeiterbedarf processing: {e}")
        return

    # Step 9: Abweichung Processing
    try:
        logging.info("Processing Abweichung for master files...")
        for file_type, file_name in input_files.items():
            if os.path.exists(file_name):
                calculate_and_append_abweichung(file_name, output_dir)
                logging.info(f"Abweichung calculation and appending completed for {file_type} file.")
            else:
                logging.warning(f"File not found: {file_name}. Skipping Abweichung processing for {file_type}.")
        logging.info("Abweichung processing completed successfully.")
    except Exception as e:
        logging.error(f"Error during Abweichung processing: {e}")
        return

    # Step 10: Utilization Processing
    try:
        logging.info("Processing Utilization for master files...")
        for file_type, file_name in input_files.items():
            if os.path.exists(file_name):
                process_utilization(file_name, personal_factor_df, output_dir)
                logging.info(f"Utilization calculation and appending completed for {file_type} file.")
            else:
                logging.warning(f"File not found: {file_name}. Skipping Utilization processing for {file_type}.")
        logging.info("Utilization processing completed successfully.")
    except Exception as e:
        logging.error(f"Error during Utilization processing: {e}")
        return

    logging.info("Data processing workflow completed successfully.")


if __name__ == "__main__":
    main()
