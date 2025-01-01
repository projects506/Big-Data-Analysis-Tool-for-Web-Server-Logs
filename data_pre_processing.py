import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Convert Windows Ticks ---
def convert_windows_ticks(df, timestamp_column='TimeStamp', batch_size=100_000):
    """
    Convert Windows FileTime ticks to datetime format with progress tracking.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        timestamp_column (str): Name of the timestamp column
        batch_size (int): Number of rows processed per progress update
    
    Returns:
        pd.Series: Series with datetime values
    """
    TICKS_PER_DAY = 24 * 60 * 60 * 10_000_000  # Number of ticks per day

    # Convert ticks to days since epoch
    days = df[timestamp_column].astype(np.float64) / TICKS_PER_DAY

    # Helper function to convert days to datetime
    def convert_single_date(days):
        try:
            base_date = datetime(1, 1, 1)
            delta = timedelta(days=days)
            return base_date + delta
        except Exception as e:
            return None

    # Apply conversion with progress tracking
    results = []
    total_entries = len(days)
    for idx, day in enumerate(days):
        if idx % batch_size == 0:
            print(f"Timestamp Progress: {idx // batch_size + 1}/{(total_entries // batch_size) + 1}")
        results.append(convert_single_date(day))
    return pd.Series(results)

# --- Extract Country Code from IpId ---
def extract_country_code(df, ip_column='IpId'):
    """
    Extracts the country code from the anonymized IP identifier (unique ID + country code).
    
    Args:
        df (pd.DataFrame): DataFrame containing the IP identifier column
        ip_column (str): Column name with the anonymized IP identifiers
    
    Returns:
        pd.DataFrame: Updated DataFrame with a new 'CountryCode' column.
    """
    # Extract last two characters from the anonymized IP column
    df['CountryCode'] = df[ip_column].str[-2:].str.upper()  # Ensure it's in uppercase
    return df

# --- Categorize UserAgent ---
def categorize_user_agent(df, user_agent_column='UserAgent'):
    """
    Categorizes UserAgent strings into Browser, OS, and Device Type using string matching.
    
    Args:
        df (pd.DataFrame): DataFrame containing the UserAgent column.
        user_agent_column (str): Column name with the UserAgent strings.
    
    Returns:
        pd.DataFrame: Updated DataFrame with new columns for Browser, OS, and Device_Type.
    """
    # Define rules for categorizing Browser
    def extract_browser(user_agent):
        if 'chrome' in user_agent.lower():
            return 'Chrome'
        elif 'firefox' in user_agent.lower():
            return 'Firefox'
        elif 'safari' in user_agent.lower() and 'chrome' not in user_agent.lower():
            return 'Safari'
        elif 'edge' in user_agent.lower() or 'edg' in user_agent.lower():
            return 'Edge'
        elif 'opera' in user_agent.lower() or 'opr' in user_agent.lower():
            return 'Opera'
        elif 'msie' in user_agent.lower() or 'trident' in user_agent.lower():
            return 'Internet Explorer'
        elif 'bot' in user_agent.lower() or 'spider' in user_agent.lower():
            return 'Bot'
        else:
            return 'Unknown'

    # Define rules for categorizing OS
    def extract_os(user_agent):
        if 'windows' in user_agent.lower():
            return 'Windows'
        elif 'mac os' in user_agent.lower() or 'macintosh' in user_agent.lower():
            return 'MacOS'
        elif 'linux' in user_agent.lower():
            return 'Linux'
        elif 'android' in user_agent.lower():
            return 'Android'
        elif 'ios' in user_agent.lower() or 'iphone' in user_agent.lower() or 'ipad' in user_agent.lower():
            return 'iOS'
        else:
            return 'Unknown'

    # Define rules for categorizing Device Type
    def extract_device_type(user_agent):
        if 'mobile' in user_agent.lower():
            return 'Mobile'
        elif 'tablet' in user_agent.lower():
            return 'Tablet'
        elif 'bot' in user_agent.lower() or 'spider' in user_agent.lower():
            return 'Bot'
        else:
            return 'Desktop'

    # Apply the functions
    df['Browser'] = df[user_agent_column].apply(extract_browser)
    df['OS'] = df[user_agent_column].apply(extract_os)
    df['Device_Type'] = df[user_agent_column].apply(extract_device_type)
    
    return df

# --- Categorize URIs ---
def categorize_uri(uri):
    if 'p-' in uri:
        return 'Product'
    elif 'c-' in uri:
        return 'Category'
    elif 'search' in uri or 'szukaj=' in uri or '/wyszukiwanie-' in uri:
        return 'Search'
    elif uri.endswith(('.jpg', '.png', '.css', '.js')):
        return 'Static Resource'
    elif 'cart' in uri or 'checkout' in uri or 'zamowienie' in uri:
        return 'Checkout'
    else:
        return 'Other'

# --- Categorize Referrers ---
def categorize_referrer(referrer):
    if pd.isna(referrer) or referrer == '-':
        return 'Direct'
    elif 'shop.our-internet-company.pl' in referrer:
        return 'Internal'
    elif any(se in referrer for se in ['google', 'bing', 'yahoo']):
        return 'Search Engine'
    elif any(sm in referrer for sm in ['facebook', 'twitter', 'instagram']):
        return 'Social Media'
    elif 'http' in referrer:
        return 'Other External'
    else:
        return 'Unknown'

# --- Print Missing Values ---
def count_missing_values(df):
    """
    Counts the number of missing values in each column of the DataFrame.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
    
    Returns:
        pd.Series: A series with column names as the index and the number of missing values as values.
    """
    missing_values = df.isnull().sum()
    return missing_values

# --- Main Execution ---
if __name__ == "__main__":
    # Load your dataset
    print("Step 1/7: Loading data...")
    df = pd.read_csv('Dataset\eclog\eclog.csv')  # Replace with your file path

    # 1. Convert TimeStamp
    print("Step 2/7: Converting TimeStamp...")
    df['TimeStamp'] = convert_windows_ticks(df)

    # 2. Extract Country Code
    print("Step 3/7: Extracting Country Codes...")
    df = extract_country_code(df)

    # 3. Parse UserAgent
    print("Step 4/7: Categorizing UserAgent...")
    df = categorize_user_agent(df)

    # 4. Categorize URIs
    print("Step 5/7: Categorizing URIs...")
    df['URI_Type'] = df['Uri'].apply(categorize_uri)

    # 5. Categorize Referrers
    print("Step 6/7: Categorizing Referrers...")
    df['Referrer_Type'] = df['Referrer'].apply(categorize_referrer)

    # 6. Remove UserId Column
    remove_user_id = input("Do you want to remove the UserID column? (yes/no): ").strip().lower()
    if remove_user_id == 'yes':
        print("Removing UserID column...")
        df.drop(columns=['UserId'], inplace=True)
    else:
        print("UserID column retained.")

    # 7. Count Missing Values
    print("Step 7/7: Counting Missing Values...")
    missing_values = count_missing_values(df)
    print("Missing Values:\n", missing_values)

    # Save the preprocessed data
    print("Saving preprocessed data...")
    df.to_csv('Dataset\preprocessed_eclog_dataset.csv', index=False)
    print("Preprocessing complete!")
