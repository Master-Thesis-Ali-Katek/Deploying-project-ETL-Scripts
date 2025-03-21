import pandas as pd
from datetime import datetime, timedelta

def unpivot_smt_load_table(df):
    """
    Unpivot SMT Load data into long format.
    """
    # Unpivot all columns except key columns
    unpivoted_df = df.melt(
        id_vars=[df.columns[0], 'Netto-Kap. Ressource [%]', 'Durchschnitt', 'Todays Date', 'PB type'],
        var_name='Date', 
        value_name='Value'
    )

    # Convert month names to numbers if present
    unpivoted_df['Date'] = unpivoted_df['Date'].replace({
        'Jan': '01', 'Feb': '02', 'Mrz': '03', 'Apr': '04', 'Mai': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Okt': '10', 'Nov': '11', 'Dez': '12'
    }, regex=True)

    return unpivoted_df


def add_belastungsart_column(df):
    """
    Add 'Belastungsart' column with alternating values 'Personal' and 'Maschine'.
    """
    df['Belastungsart'] = ['Personal' if i % 2 == 0 else 'Maschine' for i in range(len(df))]
    return df
