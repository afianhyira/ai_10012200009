import pandas as pd
import os

def load_csv_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV data using pandas.
    Handles basic errors if file is missing.
    """
    if not os.path.exists(filepath):
        print(f"Warning: CSV file not found at {filepath}")
        return pd.DataFrame()
    
    try:
        # Using utf-8-sig to handle Byte Order Mark (BOM) if present
        df = pd.read_csv(filepath, encoding='utf-8-sig')
        # Standardize column names to lowercase with underscores
        df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]
        return df
    except Exception as e:
        print(f"Error loading CSV {filepath}: {e}")
        return pd.DataFrame()
