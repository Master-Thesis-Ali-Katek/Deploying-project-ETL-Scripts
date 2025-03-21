import pandas as pd
#import some_library
import yaml
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
# Use the correct path based on the environment
if os.path.exists("/.dockerenv"):  # If running inside Docker
    config_path = "/main/config/config.yaml"
else:  # If running locally on Windows
    config_path = r"C:\Users\PATANS\Downloads\kapa_automation\config\config.yaml"

print(f"✅ Using config path: {config_path}")  # Debugging line

with open(config_path, "r", encoding="utf-8") as config_file:
    config = yaml.safe_load(config_file)

# Access nested keys under 'data_extraction'
input_file_path = config['data_extraction']['input_file_path']
sheet_name = config['data_extraction']['sheet_name']

def load_and_rename_first_column(input_file_path, usecols, skiprows, nrows, new_name="PB Type"):
    """Loads an Excel sheet, renames the first column to ensure consistent naming."""
    df = pd.read_excel(input_file_path, sheet_name=sheet_name, usecols=usecols, skiprows=skiprows, nrows=nrows)
    df.rename(columns={df.columns[0]: new_name}, inplace=True)
    return df

def extract_tables():
    """Extract tables from the Excel sheet as per defined rows and columns."""
    data_frames = {}
     # Log the file path for verification
    logging.info(f"File path being used: {input_file_path}")
    
    # Check if the file actually exists
    if not os.path.exists(input_file_path):
        logging.error(f"File does not exist at the specified path: {input_file_path}")
        return data_frames

    # Extract tables as defined in the initial code
    logging.info("Extracting SMT OEE table...")
    df_smt_oee = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=13, nrows=2, usecols='T', header=0)
    data_frames['SMT_OEE'] = df_smt_oee
    print(df_smt_oee)


    logging.info("Extracting SMT  Total OEE table...")
    df_smt_oee_header = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=2, nrows=1, usecols='A:N', header=None)
    df_smt_oee_data = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=8, nrows=1, usecols='A:N', header=None)
    df_smt_oee_data.columns = df_smt_oee_header.iloc[0]
    data_frames['SMT_OEE_Total_Monthly'] = df_smt_oee_data

    logging.info("Extracting SMT  Total OEE table...")
    df_smt_oee_header = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=10, nrows=1, usecols='A:N', header=None)
    df_smt_oee_data = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=8, nrows=1, usecols='A:N', header=None)
    df_smt_oee_data.columns = df_smt_oee_header.iloc[0]
    data_frames['SMT_OEE_Total_Weekly'] = df_smt_oee_data

    logging.info("Extracting Personal Factor table...")
    df_personal_factor = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=2, nrows=5, usecols='P:R', header=0)
    data_frames['Personal_Factor'] = df_personal_factor
    print(df_personal_factor)

    logging.info("Extracting Urlaubsquoten (Plan) Weekly table...")
    df_urlaubsquoten_weekly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=10, nrows=5, usecols='A:N', header=0)
    data_frames['Urlaubsquoten(Plan)_Weekly'] = df_urlaubsquoten_weekly

    logging.info("Extracting Urlaubsquoten (Plan) Monthly table...")
    df_urlaubsquoten_monthly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=16, nrows=5, usecols='A:N', header=0)
    data_frames['Urlaubsquoten(Plan)_Monthly'] = df_urlaubsquoten_monthly

    logging.info("Extracting Krankheitsquoten (Plan) Monthly table...")
    df_krankheitsquoten_monthly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=22, nrows=5, usecols='A:N', header=0)
    data_frames['Krankheitsquoten(Plan)_Monthly'] = df_krankheitsquoten_monthly

    logging.info("Extracting Mitarbeiter IST (brutto) Monthly table...")
    df_mitarbeiter_ist_monthly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=28, nrows=5, usecols='A:N', header=0)
    data_frames['Mitarbeiter(IST)_Monthly'] = df_mitarbeiter_ist_monthly

    logging.info("Extracting Mitarbeiter IST (brutto) Weekly table...")
    df_mitarbeiter_ist_weekly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=85, nrows=5, usecols='A:N', header=0)
    data_frames['Mitarbeiter(IST)_Weekly'] = df_mitarbeiter_ist_weekly


    logging.info("Extracting Gleitzeit (Plan) Monthly table...")
    df_gleitzeit_plan_monthly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=34, nrows=5, usecols='A:N', header=0)
    data_frames['Gleitzeit(Plan)_Monthly'] = df_gleitzeit_plan_monthly

    logging.info("Extracting Verteilzeit (Plan) Monthly table...")
    df_verteilzeit_plan_monthly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=40, nrows=5, usecols='A:N', header=0)
    data_frames['Verteilzeit(Plan)_Monthly'] = df_verteilzeit_plan_monthly

    logging.info("Extracting Kurzarbeitstage (Plan) Monthly table...")
    df_kurzarbeitstage_plan_monthly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=53, nrows=5, usecols='A:N', header=0)
    data_frames['Kurzarbeitstage(Plan)_Monthly'] = df_kurzarbeitstage_plan_monthly


    logging.info("Extracting Kurzarbeitstage (Plan) Weekly  table...")
    df_kurzarbeitstage_plan_weekly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=46, nrows=5, usecols='A:N', header=0)
    data_frames['Kurzarbeitstage(Plan)_Weekly'] = df_kurzarbeitstage_plan_weekly


    logging.info("Extracting Working or not Monthly table...")
    df_working_or_not_monthly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=59, nrows=6, usecols='A,H:S', header=0)
    data_frames['Working_or_not_Monthly'] = df_working_or_not_monthly

    logging.info("Extracting Working or not Weekly table...")
    df_working_or_not_weekly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=59, nrows=6, usecols='A:G', header=0)
    data_frames['Working_or_not_Weekly'] = df_working_or_not_weekly

    logging.info("Extracting Kurzarbeitsplanung Monthly table...")
    df_Kurzarbeitsplanung_Monthly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=73, nrows=5, usecols='A:N', header=0)
    data_frames['Arbeitstage_Monthly'] = df_Kurzarbeitsplanung_Monthly

    logging.info("Extracting Kurzarbeitsplanung Weekly table...")
    df_kurzarbeitsplanung_weekly = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=79, nrows=5, usecols='A:N', header=0)
    data_frames['Arbeitstage_Weekly'] = df_kurzarbeitsplanung_weekly

    logging.info("Extracting Krankheitsquoten (Plan) Weekly table...")
    df_krankheitsquoten_weekly_header = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=10, nrows=1, usecols='A:N', header=None)
    df_krankheitsquoten_weekly_data = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=23, nrows=4, usecols='A:N', header=None)
    df_krankheitsquoten_weekly_data.columns = df_krankheitsquoten_weekly_header.iloc[0]
    data_frames['Krankheitsquoten(Plan)_Weekly'] = df_krankheitsquoten_weekly_data


    
    logging.info("Extracting Gleitzeit (Plan) Weekly table...")
    df_gleitzeit_plan_weekly_header = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=10, nrows=1, usecols='A:N', header=None)
    df_gleitzeit_plan_weekly_data = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=35, nrows=4, usecols='A:N', header=None)
    df_gleitzeit_plan_weekly_data.columns = df_gleitzeit_plan_weekly_header.iloc[0]
    data_frames['Gleitzeit(Plan)_Weekly'] = df_gleitzeit_plan_weekly_data

    logging.info("Extracting Verteilzeit (Plan) Weekly table...")
    df_verteilzeit_plan_weekly_header = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=10, nrows=1, usecols='A:N', header=None)
    df_verteilzeit_plan_weekly_data = pd.read_excel(input_file_path, sheet_name=sheet_name, skiprows=41, nrows=4, usecols='A:N', header=None)
    df_verteilzeit_plan_weekly_data.columns = df_verteilzeit_plan_weekly_header.iloc[0]
    data_frames['Verteilzeit(Plan)_Weekly'] = df_verteilzeit_plan_weekly_data

    logging.info("Extraction complete. Data stored in dictionary for further processing.")
    return data_frames

if __name__ == "__main__":
    # For standalone testing
    tables = extract_tables()
    for key, df in tables.items():
        logging.info(f"{key} table extracted with shape: {df.shape}")
