import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime, timedelta

def clean_columns(df):
    
    """Clean columns by auto-converting object types to datetime/numeric where possible.
    Returns a new DataFrame instead of modifying in-place."""
    df_clean = df.copy()
    cols_dt = []
    cols_int = []
    for col in df_clean.select_dtypes(include=['object']).columns:
        print(df[col].type)
        # Try datetime conversion
        try:
            df_clean[col] = pd.to_datetime(df_clean[col])
            cols_dt.append(col)
            continue
        except (ValueError, TypeError):
            pass
        
        # Try numeric conversion
        try:
            df_clean[col] = pd.to_numeric(df_clean[col])
            cols_int.append(col)
        except (ValueError, TypeError):
            pass
    
    return df_clean,cols_dt, cols_int

def imbalance_checker(df, target_col):
    """Check class imbalance for a target column.
    Returns dictionary with full analysis."""
    if target_col not in df.columns:
        raise ValueError(f"Column '{target_col}' not found in DataFrame")
    
    counts = Counter(df[target_col].dropna())
    total = sum(counts.values())
    
    if total == 0:
        return {"error": "No non-null values found"}
    
    ratios = {k: v/total for k, v in counts.items()}
    max_ratio = max(ratios.values())
    dominant_class = max(ratios, key=ratios.get)
    
    return {
        "counts": counts,
        "ratios": ratios,
        "max_ratio": max_ratio,
        "dominant_class": dominant_class,
        "is_imbalanced": max_ratio > 0.8  # Example threshold
    }


def tester(rows=100): 
    """Generate a random DataFrame with integers and datetimes"""
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create date range
    start_date = datetime.now()
    dates = [start_date - timedelta(days=x) for x in range(rows)]
    
    # Create DataFrame
    df = pd.DataFrame({
        'id': np.arange(1, rows+1), 
        'transaction_date': dates,
        'product_id': np.random.randint(1000, 9999, size=rows),
        'quantity': np.random.randint(1, 20, size=rows),
        'price': np.round(np.random.uniform(5.0, 100.0, size=rows), 2),
        'customer_id': np.random.choice(['C100', 'C101', 'C102', 'C103'], size=rows),
        'is_completed': np.random.choice([True, False], size=rows)
    })
    
    df['transaction_date'] = df['transaction_date'].astype(str)
    
    # Make some dates null for testing
    df.loc[df.sample(frac=0.1).index, 'transaction_date'] = None
    
    return df