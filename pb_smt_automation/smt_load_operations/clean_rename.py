import pandas as pd

def rename_columns_for_12_months(df):
    """
    Clean column headers and prepare data for 12 months file.
    """
    # Clean column headers by removing unwanted characters
    df.columns = (df.columns.str.replace('🔑', '', regex=False)
                               .str.replace(',', '', regex=False)
                               .str.replace(r'\.\.\.', '', regex=True)
                               .str.strip())
    
    # Add 'PB type' column
    df['PB type'] = 'PB1'

    # Remove rows where 'Arbeitsplatznummer' column is empty
    df = df[df.iloc[:, 0].notna()]

    return df


def rename_columns_for_5_quarters(df):
    """
    Clean column headers and prepare data for 5 quarters file.
    """
    # Same renaming logic as 12 months
    df.columns = (df.columns.str.replace('🔑', '', regex=False)
                               .str.replace(',', '', regex=False)
                               .str.replace(r'\.\.\.', '', regex=True)
                               .str.strip())
    
    # Add 'PB type' column
    df['PB type'] = 'PB1'

    # Remove rows where 'Arbeitsplatznummer' column is empty
    df = df[df.iloc[:, 0].notna()]

    return df
