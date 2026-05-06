import pandas as pd
import pytest
import os
from main import load_data, clean_data, transform_data

# Path to orders.csv relative to this test file
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "orders.csv")

def test_orders_exists():
    assert os.path.exists(DATA_PATH)

def test_orders_not_empty():
    df = pd.read_csv(DATA_PATH)
    assert not df.empty
    assert len(df) > 0

def test_cleaning_removes_duplicates():
    df = pd.read_csv(DATA_PATH)
    original_len = len(df)
    df_cleaned = clean_data(df)
    assert len(df_cleaned) < original_len
    assert df_cleaned.duplicated().sum() == 0

def test_cleaning_fills_nulls():
    df = pd.read_csv(DATA_PATH)
    df_cleaned = clean_data(df)
    assert df_cleaned['quantity'].isnull().sum() == 0
    assert df_cleaned['price'].isnull().sum() == 0

def test_transformation_math():
    df = pd.read_csv(DATA_PATH)
    df_cleaned = clean_data(df)
    print("\nDEBUG: Cleaned Data Columns:", df_cleaned.columns)
    print("DEBUG: First row total:", (df_cleaned['price'] - df_cleaned['discount']) * df_cleaned['quantity'])
    revenue_df, sales_df = transform_data(df_cleaned)
    
    # Laptop: (800 - 50) * 1 = 750
    # Phone: (500 - 0) * 2 = 1000
    # Shoes: (100 - 10) * 1 = 90
    # T-Shirt: (50 - 5) * 1 = 45
    # Total Electronics: 1750
    
    electronics_rev = revenue_df[revenue_df['category'] == 'Electronics']['total'].iloc[0]
    assert electronics_rev == 1750
    
    fashion_rev = revenue_df[revenue_df['category'] == 'Fashion']['total'].iloc[0]
    assert fashion_rev == 135

def test_sales_count():
    df = pd.read_csv(DATA_PATH)
    df_cleaned = clean_data(df)
    _, sales_df = transform_data(df_cleaned)
    
    jan_1st_orders = sales_df[sales_df['order_date'] == '2024-01-01']['order_id'].iloc[0]
    assert jan_1st_orders == 2
