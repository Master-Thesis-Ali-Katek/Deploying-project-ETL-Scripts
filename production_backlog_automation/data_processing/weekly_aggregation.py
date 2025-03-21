import pandas as pd
from datetime import datetime
import os
#import yaml
def get_timestamp(config):
    """Returns a rounded timestamp if enabled in config."""
    if config["execution"].get("use_rounded_timestamp", False):
        return pd.to_datetime(datetime.now().replace(minute=0, second=0, microsecond=0))
    else:
        return pd.Timestamp.now()

def process_weekly_data(config):
    input_path = config["paths"]["output_excel"]
    output_path = config["paths"]["weekly_output"]
    
    df_input = pd.read_excel(input_path, sheet_name="Sheet1", engine="openpyxl")
    
    column_kommentar = "Kommentar in Prod - INFO11"
    column_rest_belastung = "Rest-Belastung Gesamt Personal aktuel"
    column_date = "Date"

    if column_kommentar in df_input.columns and column_rest_belastung in df_input.columns and column_date in df_input.columns:
        df_input[column_date] = pd.to_datetime(df_input[column_date], errors='coerce')
        
        today = datetime.now()
        current_week = today.isocalendar()[1]
        
        df_input["Week_Number"] = df_input[column_date].dt.isocalendar().week
        df_input = df_input[df_input["Week_Number"] == current_week]

        if df_input.empty:
            print(f"⚠ No new data found for KW{current_week:02d}. Exiting.")
            return
        
        def time_to_minutes(time_str):
            try:
                h, m = map(int, time_str.split(":"))
                return h * 60 + m
            except:
                return 0
        
        df_input[column_rest_belastung] = df_input[column_rest_belastung].astype(str).apply(time_to_minutes)
        summed_values = df_input.groupby(column_kommentar)[column_rest_belastung].sum()

        df_weekly = pd.DataFrame([{"KW": f"KW{current_week:02d}", "Timestamp": get_timestamp(config)}])
        for comment_name, total_minutes in summed_values.items():
            df_weekly[comment_name] = f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"

        existing_df = pd.read_excel(output_path, sheet_name="Sheet1", engine="openpyxl") if os.path.exists(output_path) else pd.DataFrame()
        df_combined = pd.concat([existing_df, df_weekly], ignore_index=True)
        df_combined.to_excel(output_path, index=False, engine="openpyxl")
        print(f"✔ Data has been appended to: {output_path}")
