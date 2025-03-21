from datetime import datetime
import pandas as pd
import logging
def extract_month_from_week(period):
    """
    Extract the month from a week period of the format 'KWXX'.

    :param period: The weekly period in 'KWXX' format.
    :return: The extracted month as a string in 'MM' format.
    """
    if period.startswith("kw" or "KW"):
        try:
            week = int(period[2:4])  # Extract week number
            year = datetime.now().year  # Default to the current year
            # Use ISO calendar to find the first day of the week
            first_week_date = datetime.strptime(f'{year} {week} 1', '%G %V %u')
            return first_week_date.strftime("%m")  # Return month in MM format
        except ValueError:
            return None
    return None

def extract_week_from_month(period):
    """
    Extract the week number from a month period of the format 'MM.YYYY'.

    :param period: The monthly period in 'MM.YYYY' format.
    :return: The extracted week number as a string in 'XX' format.
    """
    try:
        if "." in period:
            month = int(period[:2])
            year = int(period[3:])
            # Calculate the week number for the first day of the month
            first_day_of_month = datetime(year, month, 1)
            week_number = first_day_of_month.isocalendar()[1]
            return f"{week_number:02d}"  # Return as 'XX'
    except ValueError:
        return None
    return None

def extract_quarter(period):
    """
    Extract the quarter from a period of the format 'MM.YYYY' or 'KWXX'.

    :param period: The period in 'MM.YYYY' or 'KWXX' format.
    :return: The extracted quarter as an integer (1-4).
    """
    try:
        if "." in period:
            # For MM.YYYY format
            month = int(period[:2])
        elif period.startswith("kw" or "KW"):
            # For KWXX format
            month = int(extract_month_from_week(period))
        else:
            return None
        return (month - 1) // 3 + 1  # Calculate the quarter
    except (ValueError, TypeError):
        return None
    return None

def add_date_and_extract_columns(df, period_column='Period'):
    """
    Add extracted 'Month', 'Week', and 'Quarter' columns to the DataFrame.

    :param df: Input DataFrame
    :param period_column: Column name containing the period (e.g., 'Period').
    :return: Updated DataFrame with 'Month', 'Week', and 'Quarter' columns.
    """
    # Check if the period column exists
    if period_column in df.columns:
        # Extract Month from 'Period' column
        def extract_month(x):
            x = str(x) if not pd.isna(x) else ''  # Convert to string or handle NaN
            if x.lower().startswith("kw" or "KW"):  # Case insensitive check for 'KW'
                return extract_month_from_week(x)
            return x[:2] if '.' in x else None

        # Extract Week from 'Period' column
        def extract_week(x):
            x = str(x) if not pd.isna(x) else ''  # Convert to string or handle NaN
            if "." in x and not x.lower().startswith("kw" or "KW"):
                return extract_week_from_month(x)
            elif x.lower().startswith("kw" or "KW"):
                return x[2:4]
            return None

        # Apply transformations
        df['Month'] = df[period_column].apply(extract_month)
        df['Week'] = df[period_column].apply(extract_week)
        df['Quarter'] = df[period_column].apply(extract_quarter)

    return df

def map_week_to_month_and_quarter(weekly_df, monthly_df):
    """
    Map 'Month' and 'Quarter' columns from the monthly DataFrame to the weekly DataFrame.

    :param weekly_df: Weekly DataFrame with 'Period' in 'KWXX' format.
    :param monthly_df: Monthly DataFrame with 'Month' and 'Quarter' columns.
    :return: Updated weekly DataFrame with 'Month' and 'Quarter' columns.
    """
    # Ensure the monthly DataFrame has 'Period', 'Month', and 'Quarter' columns
    if 'Month' not in monthly_df or 'Quarter' not in monthly_df or 'Period' not in monthly_df:
        logging.error("Monthly DataFrame must have 'Period', 'Month', and 'Quarter' columns.")
        return weekly_df

    # Remove duplicates from 'Period' column to ensure a unique index
    if monthly_df['Period'].duplicated().any():
        logging.warning("Duplicate 'Period' values found in monthly_df. Aggregating duplicates.")
        monthly_df = monthly_df.groupby('Period', as_index=False).first()  # Keep the first occurrence

    # Create a mapping dictionary for KWXX -> Month and Quarter
    month_mapping = monthly_df.set_index('Period')[['Month', 'Quarter']].to_dict(orient='index')

    # Map 'Month' and 'Quarter' to the weekly DataFrame
    weekly_df['Month'] = weekly_df['Period'].map(lambda x: month_mapping.get(x, {}).get('Month'))
    weekly_df['Quarter'] = weekly_df['Period'].map(lambda x: month_mapping.get(x, {}).get('Quarter'))

    return weekly_df
