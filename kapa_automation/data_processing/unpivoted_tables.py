import logging
import pandas as pd
from datetime import datetime   
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to rename the first column of a DataFrame
def rename_first_column(df, table_name):
    """
    Renames the first column of the given DataFrame based on the table name.
    """
    if df.columns.size > 0:
        if table_name in ["SMT_OEE" "SMT_OEE_Total"]:
            df.rename(columns={df.columns[0]: "OEE"}, inplace=True)
        elif table_name in ["SMT_OEE_Total_Weekly", "SMT_OEE_Total_Monthly"]:
            df.rename(columns={df.columns[0]: "PB Type"}, inplace=True)
        elif table_name == "Personal_Factor":
            pass  # No renaming for Personal_Factor
        elif table_name.startswith('Working_or_not'):
            df.rename(columns={df.columns[0]: "SMT Type"}, inplace=True)
        else:
            df.rename(columns={df.columns[0]: "PB Type"}, inplace=True)
    return df

# Function to convert date-like periods to mm.yyyy format
def convert_period_format(period):
    """
    Converts date-like strings into 'mm.yyyy' format.
    """
    try:
        if pd.to_datetime(period, errors='coerce', dayfirst=True):
            return pd.to_datetime(period, errors='coerce', dayfirst=True).strftime('%m.%Y')
        return period
    except Exception as e:
        logging.warning(f"Unable to convert period '{period}': {e}")
        return period  # Return as is if conversion fails

# Function to preprocess periods
def preprocess_periods(df):
    """
    Preprocesses the 'Period' column to standardize date formats to 'mm.yyyy'.
    """
    if 'Period' in df.columns:
        df['Period'] = df['Period'].apply(convert_period_format)
    return df

# Function to unpivot (melt) the DataFrame
def unpivot_table(df, id_var, var_name, value_name, attribute_name):
    """
    Unpivots the given DataFrame and adds the 'Attribute' and 'Date' columns.
    """
    try:
        # Ensure the identifier column exists
        if id_var not in df.columns:
            raise KeyError(f"The id_var '{id_var}' does not exist in the DataFrame columns: {df.columns}")
        
        # Perform unpivoting
        df_unpivoted = pd.melt(
            df,
            id_vars=[id_var],
            var_name=var_name,
            value_name=value_name
        )
        
        # Log unpivoted DataFrame shape
        logging.info(f"Unpivoted DataFrame shape: {df_unpivoted.shape}")
        
        # Add 'Attribute' and 'Date' columns
        df_unpivoted['Attribute'] = attribute_name
        df_unpivoted['Date'] = pd.to_datetime(datetime.now().replace(minute=0, second=0, microsecond=0)) # Add current date
        
        # Log added columns
        logging.info(f"Columns after adding 'Attribute' and 'Date': {df_unpivoted.columns.tolist()}")

    except Exception as e:
        logging.error(f"Error during unpivoting: {e}")
        return None

    return df_unpivoted


# Main function to process tables
def unpivot_all_tables(data_frames):
    unpivoted_frames = {}

    for key, df in data_frames.items():
        logging.info(f"Processing table: {key}")

        # Rename first column
        df = rename_first_column(df, table_name=key)

        # Determine the identifier column for unpivoting
        id_var = "SMT Type" if key in ["Personal_Factor", "Working_or_not_Monthly", "Working_or_not_Weekly"] else "PB Type"

        if id_var not in df.columns:
            logging.error(f"Missing id_var '{id_var}' in table {key}. Skipping unpivoting.")
            continue

        try:
            if "Monthly" in key or "Weekly" in key or key == "SMT_OEE":
                unpivoted_df = unpivot_table(df, id_var=id_var, var_name="Period", value_name="Value", attribute_name=key.split('_')[0])
                unpivoted_df = preprocess_periods(unpivoted_df)
            else:
                logging.warning(f"Table {key} does not match expected naming convention and was skipped.")
                continue

            if unpivoted_df is not None:
                unpivoted_frames[key] = unpivoted_df
        except Exception as e:
            logging.error(f"Error unpivoting table {key}: {e}")

    return unpivoted_frames
    
# Example to test the script
if __name__ == "__main__":
    data_frames = {
        "Personal_Factor": pd.DataFrame({
            'staff\nfactor': ['Factor1', 'Factor2'],
            'SMT Type': ['Type1', 'Type2'],
            'Result': [100, 200]
        }),
        "SMT_OEE": pd.DataFrame({
            'SMT-Linien': ['Line1', 'Line2'],
            'Apr 2024': [85, 90],
            'May 2024': [87, 88]
        }),
        "SMT_OEE_Total": pd.DataFrame({
            'SMT Gesamt': ['SMT Gesamt'],
            'Apr 2024': [85],
            'May 2024': [87]
        })
    }

    # Rename specific row value in SMT_OEE_Total
    data_frames["SMT_OEE_Total"].loc[data_frames["SMT_OEE_Total"].iloc[:, 0] == "SMT Gesamt", data_frames["SMT_OEE_Total"].columns[0]] = "PB1"

    # Unpivot all tables
    unpivoted_data_frames = unpivot_all_tables(data_frames)

    for key, df in unpivoted_data_frames.items():
        logging.info(f"Unpivoted {key} with shape: {df.shape}")
        print(df.head())
