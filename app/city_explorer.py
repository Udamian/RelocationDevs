import streamlit as st
import pandas as pd
from pathlib import Path

PROCESSED = Path(__file__).parent.parent / "data" / "processed"

def render():
    st.title("City Explorer")
    st.caption("Explora indicadores clave por ciudad")
    cities_file = PROCESSED / "cities_processed.csv"
    if not cities_file.exists():
        st.warning("Sin datos procesados. Ejecuta primero el notebook 02_indicators.ipynb.")
        return
    df = pd.read_csv(cities_file)
    col1, col2 = st.columns(2)
    with col1:
        regions = st.multiselect("Region", sorted(df["region"].unique()))
    with col2:
        min_score = st.slider("Relocation Score minimo", 0, 100, 0)
    if regions:
        df = df[df["region"].isin(regions)]
    if "relocation_score" in df.columns:
        df = df[df["relocation_score"] >= min_score]
    st.dataframe(df, use_container_width=True)
