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

def test_cleaning_logic():
    df = pd.read_csv(DATA_PATH)
    df_cleaned = clean_data(df)
    
    # Logic checks
    assert df_cleaned['quantity'].isnull().sum() == 0
    assert df_cleaned['price'].isnull().sum() == 0
    assert df_cleaned.duplicated().sum() == 0
    
    # If it's our original small sample, check specific fill logic
    if len(df) <= 5 and 'order_id' in df.columns:
        # Row 4 had missing quantity in original sample
        row_4 = df_cleaned[df_cleaned['order_id'] == 4]
        if not row_4.empty:
            assert row_4['quantity'].iloc[0] == 1

def test_transformation_logic():
    df = pd.read_csv(DATA_PATH)
    df_cleaned = clean_data(df)
    revenue_df, sales_df = transform_data(df_cleaned)
    
    # General checks
    assert not revenue_df.empty
    assert not sales_df.empty
    assert (revenue_df['total'] >= 0).all()
    
    # Specific math check only for the original 5-row sample
    if len(df) <= 5 and 'Laptop' in df['product'].values:
        electronics_rev = revenue_df[revenue_df['category'] == 'Electronics']['total'].iloc[0]
        assert electronics_rev == 1750
        
        jan_1st_orders = sales_df[sales_df['order_date'] == '2024-01-01']['order_id'].iloc[0]
        assert jan_1st_orders == 2
