import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

def load_data(file_path):
    """
    Load data from a CSV file.
    """
    try:
        logging.info(f"Loading data from {file_path}")
        return pd.read_csv(file_path)
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        return None

def clean_data(df):
    """
    Clean dataset: deduplicate, fill nulls, and filter invalid values gracefully.
    """
    try:
        logging.info("Starting data cleaning...")
        # Drop duplicate rows
        df = df.drop_duplicates()
        
        # Define required columns for quality checks
        required_cols = ['price', 'quantity', 'discount']
        
        for col in required_cols:
            if col not in df.columns:
                logging.warning(f"Column '{col}' is missing. Initializing with default values.")
                if col == 'quantity': df[col] = 1
                else: df[col] = 0
            else:
                if col == 'quantity': df[col] = df[col].fillna(1)
                else: df[col] = df[col].fillna(0)
        
        # Only filter if columns exist (they will now, due to initialization above)
        df = df[(df['price'] >= 0) & (df['quantity'] > 0)]
        
        logging.info(f"Cleaning complete. Remaining rows: {len(df)}")
        return df
    except Exception as e:
        logging.error(f"Error during cleaning: {e}")
        return None

def transform_data(df, start_date=None):
    """
    Transform data: Incremental filtering and aggregation.
    """
    try:
        logging.info("Starting data transformation...")
        
        # Incremental Processing: Filter by date if provided
        if start_date:
            logging.info(f"Filtering records from {start_date} onwards.")
            df['order_date'] = pd.to_datetime(df['order_date'])
            df = df[df['order_date'] >= pd.to_datetime(start_date)]
        
        # Calculate total: (price - discount) * quantity
        df['total'] = (df['price'] - df['discount']) * df['quantity']
        
        # Aggregations
        revenue_df = df.groupby('category')['total'].sum().reset_index()
        sales_df = df.groupby('order_date')['order_id'].nunique().reset_index()
        
        logging.info("Transformation complete.")
        return revenue_df, sales_df
    except Exception as e:
        logging.error(f"Error during transformation: {e}")
        return None, None

def save_data(df, path):
    """
    Save the data to a CSV file.
    """
    try:
        df.to_csv(path, index=False)
        logging.info(f"Data successfully saved to {path}")
    except Exception as e:
        logging.error(f"Error saving data to {path}: {e}")

def run_pipeline(start_date=None):
    """
    Main ETL entry point.
    """
    logging.info("--- Pipeline Started ---")
    file_path = 'orders.csv'
    
    df = load_data(file_path)
    if df is not None:
        df = clean_data(df)
        if df is not None:
            revenue_df, sales_df = transform_data(df, start_date=start_date)
            if revenue_df is not None and sales_df is not None:
                save_data(revenue_df, 'revenue.csv')
                save_data(sales_df, 'daily_sales.csv')
                logging.info("--- Pipeline Completed Successfully ---")
                return True
    
    logging.error("--- Pipeline Failed ---")
    return False

if __name__ == "__main__":
    # Example: Run incrementally for records after 2024-01-01
    run_pipeline(start_date="2024-01-01")
