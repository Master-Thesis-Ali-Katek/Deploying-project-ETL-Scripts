import pandas as pd
import re

def clean_and_rename_smt_columns(df):
    """
    Cleans and renames columns for SMT data.

    :param df: Input DataFrame.
    :return: Cleaned and renamed DataFrame.
    """
    # Rename 'Arbeitsplatznummer' to 'SMT Type'
    if 'Arbeitsplatznummer' in df.columns:
        df.rename(columns={'Arbeitsplatznummer': 'SMT Type'}, inplace=True)
    else:
        print("Column 'Arbeitsplatznummer' not found. Please verify CSV file headers.")
        return None

    # Clean the 'SMT Type' column
    if "SMT Type" in df.columns:
        df["SMT Type"] = (
            df["SMT Type"]
            .str.replace(r'""', '', regex=True)
            .str.replace(r'-', '', regex=True)
            .str.replace(r'\+', '', regex=True)
            .str.replace('"', '')
            .str.strip()  # Remove any leading or trailing whitespace
        )

    # Remove rows with missing or empty values in "SMT Type"
    df = df[df['SMT Type'].notna() & (df['SMT Type'].str.strip() != '')]

    # Identify and rename month-year columns to 'MM.YYYY' format
    month_year_columns = [col for col in df.columns if re.search(r'Ecktermin 🔑:\d{2}\.\d{4},Rest-Belastung Gesamt Personal', col)]
    for col in month_year_columns:
        new_col_name = re.sub(r'Ecktermin 🔑:(\d{2})\.(\d{4}),Rest-Belastung Gesamt Personal', r'\1.\2', col)
        df.rename(columns={col: new_col_name}, inplace=True)

    # Identify and rename week-year columns to 'KWXX' format
    week_year_columns = [col for col in df.columns if re.search(r'Ecktermin 🔑:W\d{2} \d{4},Rest-Belastung Gesamt Personal', col)]
    for col in week_year_columns:
        new_col_name = re.sub(r'Ecktermin 🔑:W(\d{2}) \d{4},Rest-Belastung Gesamt Personal', r'KW\1', col)
        df.rename(columns={col: new_col_name}, inplace=True)

    # Drop unnamed columns (if any exist)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    print("Columns after cleaning and renaming:", df.columns.tolist())
    return df
