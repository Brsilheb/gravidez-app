import pandas as pd

def get_total_spent(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    return float(df["valor"].fillna(0).sum())

def get_completed_items(df: pd.DataFrame) -> int:
    if df.empty:
        return 0
    return int((df["status"] == "Comprado").sum())

def get_progress_percent(df: pd.DataFrame) -> float:
    total = len(df)
    if total == 0:
        return 0.0
    return round((get_completed_items(df) / total) * 100, 1)
