import pandas as pd
from datetime import datetime 

def unpivot_smt_data(df, frequency):
    """
    Unpivots SMT data to a long format.

    :param df: Input DataFrame.
    :param frequency: 'monthly' or 'weekly'.
    :return: Unpivoted DataFrame.
    """
    # Determine the columns to unpivot based on frequency
    value_vars = [col for col in df.columns if (frequency == 'monthly' and '.' in col) or (frequency == 'weekly' and col.startswith('KW'))]
    if not value_vars:
        print(f"No value columns found to unpivot for {frequency}. Verify input data.")
        return None

    # Melt the DataFrame
    df_unpivoted = pd.melt(df, id_vars=["SMT Type"], value_vars=value_vars, var_name="Period", value_name="Value")

    # Add Frequency column
    df_unpivoted['Frequency'] = frequency
    df_unpivoted['Date'] = pd.to_datetime(datetime.now().replace(minute=0,second=0, microsecond=0))


    print("Unpivoted DataFrame sample:")
    print(df_unpivoted.head())

    return df_unpivoted
