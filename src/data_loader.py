"""
data_loader.py
Carga y armonizacion de datasets de fuentes externas.
"""

import pandas as pd
from pathlib import Path

DATA_RAW       = Path(__file__).parent.parent / "data" / "raw"
DATA_PROCESSED = Path(__file__).parent.parent / "data" / "processed"


def load_csv(filename: str, **kwargs) -> pd.DataFrame:
    path = DATA_RAW / filename
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    return pd.read_csv(path, **kwargs)


def load_processed(filename: str) -> pd.DataFrame:
    path = DATA_PROCESSED / filename
    return pd.read_parquet(path) if filename.endswith(".parquet") else pd.read_csv(path)


def save_processed(df: pd.DataFrame, filename: str) -> None:
    path = DATA_PROCESSED / filename
    if filename.endswith(".parquet"):
        df.to_parquet(path, index=False)
    else:
        df.to_csv(path, index=False)
    print(f"Guardado: {path}")
