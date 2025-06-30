import pandas as pd
from collections import Counter

def clean_columns(df):
    """Clean columns by auto-converting object types to datetime/numeric where possible.
    Returns a new DataFrame instead of modifying in-place."""
    df_clean = df.copy()
    
    for col in df_clean.select_dtypes(include=['object']).columns:
        # Try datetime conversion
        try:
            df_clean[col] = pd.to_datetime(df_clean[col])
            continue
        except (ValueError, TypeError):
            pass
        
        # Try numeric conversion
        try:
            df_clean[col] = pd.to_numeric(df_clean[col])
        except (ValueError, TypeError):
            pass
    
    return df_clean

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