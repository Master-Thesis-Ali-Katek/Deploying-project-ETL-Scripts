import pandas as pd
import os
import re
import logging
import yaml  # ✅ Import YAML
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Load YAML Configuration
def load_config(yaml_path="config.yaml"):
    """Loads the configuration from a YAML file."""
    if not os.path.exists(yaml_path):
        logging.error(f"❌ Config file not found: {yaml_path}")
        return None

    with open(yaml_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)  # Load the YAML file safely

# ✅ Get the Timestamp from Config
def get_timestamp(config):
    """Returns a rounded timestamp if enabled in config."""
    if config["execution"].get("use_rounded_timestamp", False):
        return pd.to_datetime(datetime.now().replace(minute=0, second=0, microsecond=0))
    else:
        return pd.to_datetime(datetime.now())

# ✅ Read & Clean CSV
def read_and_clean_csv(file_path, config):
    """Reads, cleans, and returns a DataFrame from a CSV file."""
    if not os.path.exists(file_path):
        logging.error(f"❌ File not found: {file_path}")
        return pd.DataFrame()

    cleaned_lines = []
    with open(file_path, "r", encoding="utf-8-sig") as f:  # ✅ FIXED ENCODING
        for line in f:
            line = line.strip()
            line = re.sub(r"^[ \t]*[-+]\s+", "", line)
            cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)

    # ✅ Read CSV with correct encoding
    df = pd.read_csv(pd.io.common.StringIO(cleaned_text), delimiter=";", header=1, encoding="utf-8-sig")

    return df

# ✅ Clean DataFrame Based on Config
def clean_dataframe(df, config):
    """Performs cleaning operations on the DataFrame."""
    #df.columns = df.columns.str.encode("latin1").str.decode("utf-8")  # ✅ Fix encoding issue
    df.columns = df.columns.str.replace("🔑", "", regex=True).str.strip()
    drop_columns = config["columns"]["drop_columns"]
    extra_columns = config["columns"]["extra_columns"]

    df = df.drop(columns=[col for col in drop_columns if col in df.columns], errors="ignore")
    #df.columns = df.columns.str.replace("🔑", "", regex=True).str.strip()

    # ✅ Rename "(Szen.:Produktiv *)" to "aktuel"
    df.columns = df.columns.str.replace(r"\(Szen\.:Produktiv.*\)", " aktuel", regex=True)

    # ✅ Remove empty 'Materialnummer' rows
    if "Materialnummer" in df.columns:
        df = df.dropna(subset=["Materialnummer"])
        df = df[df["Materialnummer"].astype(str).str.strip() != ""]

    # ✅ Remove rows where 'Auftragsnummer' is between 1 and 500
    if "Auftragsnummer" in df.columns:
        df["Auftragsnummer"] = pd.to_numeric(df["Auftragsnummer"], errors="coerce")
        df = df[~df["Auftragsnummer"].between(1, 500, inclusive="both")]

    # ✅ Ensure required columns exist
    for col in extra_columns:
        if col not in df.columns:
            df[col] = None  # Add missing columns
        else:
            df.rename(columns={col: col}, inplace=True)  # ✅ Ensure exact column names


    df["Date"] = get_timestamp(config)  # ✅ FIXED: Correct timestamp handling
    return df

# ✅ Append Data to Excel
def append_to_excel(df, file_path):
    """Appends new data to the existing Excel file, handling errors properly."""
    if os.path.exists(file_path):
        try:
            # ✅ Try reading the existing file
            existing_df = pd.read_excel(file_path, sheet_name="Sheet1", engine="openpyxl")
            
            # ✅ Append new data
            df_combined = pd.concat([existing_df, df], ignore_index=True)
            logging.info(f"✔ Successfully appended {len(df)} rows to {file_path}")

        except Exception as e:
            logging.error(f"⚠ Error reading {file_path}: {str(e)}. Creating a new file.")
            df_combined = df  # If the file is corrupted, overwrite it

    else:
        df_combined = df  # If file doesn't exist, create a new one

    # ✅ Save the DataFrame back to Excel
    try:
        df_combined.to_excel(file_path, index=False, engine="openpyxl")  # ✅ Removed 'encoding'
        logging.info(f"✔ Data saved successfully to {file_path}")
    
    except Exception as e:
        logging.error(f"❌ Failed to save {file_path}: {str(e)}")

# ✅ Process CSV with YAML Config
def process_csv(config):
    input_path = config["paths"]["input_csv"]
    output_path = config["paths"]["output_excel"]

    df = read_and_clean_csv(input_path, config)
    if df.empty:
        logging.error("❌ No data read from the CSV. Exiting.")
        return

    df = clean_dataframe(df, config)
    append_to_excel(df, output_path)
