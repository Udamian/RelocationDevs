"""
utils.py
Funciones de utilidad compartidas.
"""

import pandas as pd


def format_currency(value: float, currency: str = "EUR") -> str:
    return f"{currency} {value:,.0f}"


def normalize_column(series: pd.Series) -> pd.Series:
    min_val, max_val = series.min(), series.max()
    if max_val == min_val:
        return pd.Series([50.0] * len(series), index=series.index)
    return ((series - min_val) / (max_val - min_val) * 100).round(2)


def filter_cities(df: pd.DataFrame, regions: list = None, min_score: float = 0.0) -> pd.DataFrame:
    if regions:
        df = df[df["region"].isin(regions)]
    if "relocation_score" in df.columns:
        df = df[df["relocation_score"] >= min_score]
    return df.reset_index(drop=True)


def top_cities(df: pd.DataFrame, n: int = 10, by: str = "relocation_score") -> pd.DataFrame:
    return df.sort_values(by, ascending=False).head(n).reset_index(drop=True)
