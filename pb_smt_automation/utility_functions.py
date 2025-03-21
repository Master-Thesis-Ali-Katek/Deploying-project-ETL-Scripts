import pandas as pd
import re
import logging
from datetime import datetime 
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def unpivot_combined_data(combined_df):
    """
    Unpivot the combined DataFrame for production hours.
    Converts wide-format data into long-format and adds metadata.

    Parameters:
    - combined_df (DataFrame): Input combined DataFrame to be unpivoted.

    Returns:
    - DataFrame: Unpivoted DataFrame with added metadata.
    """
    if combined_df is None or combined_df.empty:
        logging.warning("Empty DataFrame received for unpivoting. Returning None.")
        return None

    try:
        # Identify id_vars and value_vars
        id_vars = ['PB Type'] if 'PB Type' in combined_df.columns else []
        value_vars = [
            col for col in combined_df.columns
            if re.match(r'^\d{2}\.\d{4}$', col) or re.match(r'^KW\d{2}$', col)
        ]

        # Log identified columns for debugging
        logging.info(f"id_vars: {id_vars}, value_vars: {value_vars}")

        # Perform unpivoting (melt operation)
        combined_unpivoted = pd.melt(
            combined_df,
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="Period",
            value_name="Value"
        )

        # Add additional metadata
        combined_unpivoted['Attribute'] = 'Production Hours'
        combined_unpivoted['Date'] = pd.to_datetime(datetime.now().replace(minute=0,second=0, microsecond=0))

        logging.info(f"Unpivoted combined DataFrame shape: {combined_unpivoted.shape}")
        return combined_unpivoted

    except Exception as e:
        logging.error(f"Error in unpivoting combined data: {e}")
        return None
