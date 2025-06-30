import pandas as pd
import numpy as np 
import os
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Optional

def clean_columns(df): 
    """This function cleans the data in columns"""
    for col in df.select_dtypes(include=['object']).columns:
            # Try converting to datetime
            try:
                df[col] = pd.to_datetime(df[col], errors='raise')
                continue
            except (ValueError, TypeError):
                pass
            
            # Try converting to numeric
            try:
                df[col] = pd.to_numeric(df[col], errors='raise')
                continue
            except (ValueError, TypeError):
                pass
    return df 