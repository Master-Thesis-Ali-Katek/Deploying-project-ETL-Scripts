import logging
import yaml
from data_processing.read_clean_csv import process_csv
from data_processing.weekly_aggregation import process_weekly_data

# Load Configuration
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Configure Logging
logging.basicConfig(
    filename=config["logging"]["log_file"],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    logging.info("🚀 Production backlog processing started...")

    # Process CSV and Append to Excel
    process_csv(config)

    # Process Weekly Aggregation
    process_weekly_data(config)

    logging.info("✅ Production backlog processing completed successfully!")
