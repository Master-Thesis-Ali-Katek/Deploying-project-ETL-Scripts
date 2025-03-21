
import pandas as pd
import re
from datetime import datetime 
def unpivot_data(df, pb_type):
    """
    Unpivot the DataFrame and add consistent columns.

    :param df: Cleaned DataFrame
    :param pb_type: PB type identifier (e.g., PB1, PB2)
    :return: Unpivoted DataFrame
    """
    # Identify columns that match the 'Period' format (MM.YYYY or WKXX.YYYY)
    period_columns = [col for col in df.columns if re.match(r'^\d{2}\.\d{4}$', col) or re.match(r'^KW\d{2}$', col)]
    
    # Debugging: Print identified Period columns
    print("Identified Period columns:", period_columns)

    if not period_columns:
        print("Error: No 'Period' columns found. Verify column renaming logic.")
        return None

    # Melt (unpivot) the DataFrame
    df_unpivoted = pd.melt(df, id_vars=["Coustmer Type"], value_vars=period_columns,
                           var_name="Period", value_name="Value")

    # Add metadata columns
    df_unpivoted['PB Type'] = pb_type
    df_unpivoted['Attribute'] = 'Production Hours'
    df_unpivoted['Date'] = pd.to_datetime(datetime.now().replace(minute=0,second=0, microsecond=0))


    return df_unpivoted
