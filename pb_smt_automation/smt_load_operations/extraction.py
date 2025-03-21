import pandas as pd
from datetime import datetime

def extract_smt_load_data(file_path):
    """
    Extract data from the SMT Load table file.
    """
    # Read CSV file with delimiter ';' and header at row 1
    df = pd.read_csv(file_path, delimiter=';', header=1)
    
    # Correctly remove unwanted columns by zero-based index
    df.drop(df.columns[[0, 1, 4, 5, 6, 7, 8, 9]], axis=1, inplace=True)
    
    # Add a column with today's date
    df['Todays Date'] = pd.to_datetime(datetime.now().replace(minute=0,second=0, microsecond=0))
    
    return df
