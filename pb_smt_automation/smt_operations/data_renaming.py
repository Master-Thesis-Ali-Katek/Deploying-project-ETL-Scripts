# modules/renaming.py

import re

def rename_time_columns(df):
    """
    Rename week-year and month-year columns to standardized formats.
    """
    # Rename week-year columns to standardized format (WKXX.YYYY)
    week_year_columns = [col for col in df.columns if re.search(r'Ecktermin 🔑:W\d{2} \d{4},Rest-Belastung Gesamt Personal', col)]
    for col in week_year_columns:
        new_col_name = re.sub(r'Ecktermin 🔑:W(\d{2}) (\d{4}),Rest-Belastung Gesamt Personal', r'WK\1.\2', col)
        df.rename(columns={col: new_col_name}, inplace=True)

    # Rename month-year columns to standardized format (MM.YYYY)
    month_year_columns = [col for col in df.columns if re.search(r'Ecktermin 🔑:\d{2}\.\d{4},Rest-Belastung Gesamt Personal', col)]
    for col in month_year_columns:
        new_col_name = re.sub(r'Ecktermin 🔑:(\d{2})\.(\d{4}),Rest-Belastung Gesamt Personal', r'\1.\2', col)
        df.rename(columns={col: new_col_name}, inplace=True)

    return df

def rename_additional_columns(df):
    """
    Rename additional columns: 'Info1 (Mat.Dat.)' to 'Coustmer Type' and 'Arbeitsplatznummer' to 'SMT Type'.
    """
    # Rename 'Info1 (Mat.Dat.)' to 'Coustmer Type'
    potential_columns = [col for col in df.columns if re.search(r'Info1.*Mat\.Dat\.', col)]
    if potential_columns:
        df.rename(columns={potential_columns[0]: 'Coustmer Type'}, inplace=True)
    else:
        print("Warning: Column 'Info1 (Mat.Dat.)' or similar not found. Please verify CSV file headers.")

    # Rename 'Arbeitsplatznummer' to 'SMT Type'
    if 'Arbeitsplatznummer' in df.columns:
        df.rename(columns={'Arbeitsplatznummer': 'SMT Type'}, inplace=True)

    return df
