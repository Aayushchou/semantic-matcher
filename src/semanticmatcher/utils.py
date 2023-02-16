"""
Utility functions.
"""

def normalize_df(df):
    df=(df)/(abs(df.max()))
    return df