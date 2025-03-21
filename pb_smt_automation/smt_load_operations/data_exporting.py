# modules/processing.py

import pandas as pd
from datetime import datetime, timedelta
import re

def add_today_date(df):
    """
    Add a 'Today' column with the current date to the DataFrame.
    """
    df['Today'] = pd.to_datetime(datetime.now().replace(minute=0,second=0, microsecond=0))

    return df

def extract_month_from_week(period):
    """
    Extract the month from a given week-year period in the format 'WKXX.YYYY'.
    """
    if period.startswith("WK"):
        week = int(period[2:4])  # Extract the week number
        year = int(period[5:])  # Extract the year
        first_day_of_year = datetime(year, 1, 1)
        days_to_week = timedelta(weeks=week - 1)
        first_week_date = first_day_of_year + days_to_week
        return first_week_date.strftime("%m")  # Extract the month as 'MM'
    return None

def extract_week_from_month(period):
    """
    Extract the week from a given month-year period in the format 'MM.YYYY'.
    """
    if "." in period:
        month = int(period[:2])  # Extract the month
        year = int(period[3:])  # Extract the year
        first_day_of_month = datetime(year, month, 1)
        week_number = first_day_of_month.isocalendar()[1]
        return f"{week_number:02d}"  # Return as 'XX'
    return None

def extract_quarter(period):
    """
    Extract the quarter from a given period in the format 'MM.YYYY' or 'WKXX.YYYY'.
    """
    if "." in period:
        month = int(period[:2]) if period[0].isdigit() else int(extract_month_from_week(period))
        return (month - 1) // 3 + 1  # Quarter calculation
    return None

def separate_first_row(df):
    """
    Separate the first row from the rest of the DataFrame to form a new table named 'Production Hours'.
    """
    production_hours_df = df.iloc[:1].copy()  # Extract the first row as a separate DataFrame
    main_df = df.iloc[1:].reset_index(drop=True)  # Keep the rest of the data as the main DataFrame and reset index
    
    # Rename columns for production hours table
    production_hours_df.columns = ['Production Hours'] + list(production_hours_df.columns[1:])
    
    return production_hours_df, main_df

def unpivot_data(df, id_vars):
    """
    Unpivot (melt) the DataFrame from wide to long format and add derived columns.
    """
    value_vars = [col for col in df.columns if re.match(r'^(WK\d{2}\.\d{4}|\d{2}\.\d{4})$', col)]
    df_unpivoted = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name="Period", value_name="Value")

    # Add derived columns: Month, Week, Quarter
    df_unpivoted['Month'] = df_unpivoted['Period'].apply(lambda x: extract_month_from_week(x) if x.startswith("WK") else x[:2])
    df_unpivoted['Week'] = df_unpivoted['Period'].apply(lambda x: extract_week_from_month(x) if "." in x and not x.startswith("WK") else x[2:4] if x.startswith("WK") else None)
    df_unpivoted['Quarter'] = df_unpivoted['Period'].apply(extract_quarter)

    return df_unpivoted

def process_data(df, file_type):
    """
    Process the data for PB1, PB2, PB3, PB4, and SMT tables.
    """
    # Separate the first row as the 'Production Hours' table
    production_hours_df, main_df = separate_first_row(df)
    
    # Add today's date to both tables
    production_hours_df = add_today_date(production_hours_df)
    main_df = add_today_date(main_df)

    # Unpivot the rest of the data (excluding the first row)
    id_vars = ['Coustmer Type', 'SMT Type'] if 'SMT Type' in main_df.columns else ['Coustmer Type']
    df_unpivoted = unpivot_data(main_df, id_vars)

    return production_hours_df, df_unpivoted
