import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

PROCESSED = Path(__file__).parent.parent / "data" / "processed"

def render():
    st.title("City Comparison")
    st.caption("Compara ciudades lado a lado")
    cities_file = PROCESSED / "cities_processed.csv"
    if not cities_file.exists():
        st.warning("Sin datos procesados.")
        return
    df = pd.read_csv(cities_file)
    selected = st.multiselect("Selecciona ciudades", sorted(df["city_name"].unique()), max_selections=5)
    if len(selected) < 2:
        st.info("Selecciona al menos 2 ciudades.")
        return
    subset = df[df["city_name"].isin(selected)]
    for metric in ["average_salary", "net_salary", "cost_of_living_index", "purchasing_power", "relocation_score"]:
        if metric in subset.columns:
            fig = go.Figure(go.Bar(x=subset["city_name"], y=subset[metric], marker_color="#4A90D9"))
            fig.update_layout(title=metric.replace("_", " ").title(), height=300, margin=dict(t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
