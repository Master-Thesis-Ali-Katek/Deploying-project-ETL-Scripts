import re

def clean_and_rename_columns(df):
    """
    Clean and rename columns in the DataFrame.
    - Renames 'Info1 (Mat.Dat.)' to 'Coustmer Type'.
    - Renames 'Arbeitsplatznummer' to 'SMT Type'.
    - Converts month-year and week-year columns to a unified 'Period' format.

    :param df: Input DataFrame
    :return: Cleaned and renamed DataFrame
    """
    if df is None:
        print("DataFrame is empty. Cannot clean and rename columns.")
        return None

    # Rename 'Info1 (Mat.Dat.)' to 'Coustmer Type'
    potential_columns = [col for col in df.columns if re.search(r'Info1.*Mat\.Dat\.', col)]
    if potential_columns:
        df.rename(columns={potential_columns[0]: 'Coustmer Type'}, inplace=True)

    # Rename 'Arbeitsplatznummer' to 'SMT Type'
    if 'Arbeitsplatznummer' in df.columns:
        df.rename(columns={'Arbeitsplatznummer': 'SMT Type'}, inplace=True)

    # Rename Month-Year and Week-Year columns to a unified 'Period' format
    period_columns = {}
    for col in df.columns:
        # Match Month-Year columns (e.g., Ecktermin 🔑:MM.YYYY,...)
        if re.search(r'Ecktermin .*:\d{2}\.\d{4},.*', col):
            new_col_name = re.sub(r'Ecktermin .*:(\d{2}\.\d{4}),.*', r'\1', col)
            period_columns[col] = new_col_name
        # Match Week-Year columns (e.g., Ecktermin 🔑:WXX YYYY,...)
        # Rename weekly period columns
    # Rename weekly period columns
    week_year_columns = [col for col in df.columns if re.search(r'Ecktermin 🔑:W\d{2} \d{4},Rest-Belastung Gesamt Personal', col)]
    for col in week_year_columns:
    # Extract only the week number (WXX) and rename to KWXX
        new_col_name = re.sub(r'Ecktermin 🔑:W(\d{2}) \d{4},Rest-Belastung Gesamt Personal', r'KW\1', col)
        df.rename(columns={col: new_col_name}, inplace=True)

    print("Columns after renaming weekly data:", df.columns.tolist())


    # Apply renaming for all identified Period columns
    df.rename(columns=period_columns, inplace=True)

    # Debugging: Print columns after renaming
    print("Columns after renaming:", df.columns.tolist())

    # Drop unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Clean 'Coustmer Type' column
    if "Coustmer Type" in df.columns:
        df["Coustmer Type"] = df["Coustmer Type"].str.replace(r'[+"-]', '', regex=True).str.strip()

    # Remove rows with missing or empty 'Coustmer Type'
    df = df[df['Coustmer Type'].notna() & (df['Coustmer Type'] != '')]

    # Fill missing 'SMT Type' with placeholder
    if 'SMT Type' in df.columns:
        df['SMT Type'] = df['SMT Type'].fillna('Unknown')

    return df
