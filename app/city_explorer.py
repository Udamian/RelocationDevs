"""
city_explorer.py
Módulo: explorador de ciudades con ranking visual y tabla filtrable.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from app.styles import page_header
PROCESSED = Path(__file__).parent.parent / "data" / "processed"


@st.cache_data
def load_data():
    return pd.read_csv(PROCESSED / "cities_processed.csv")


def render():
    page_header("City Explorer", "Explora y filtra ciudades por indicadores clave")

    p = st.session_state.get("profile", {})
    if p.get("estimated_salary"):
        st.info(
            f"Tu salario estimado: **€{p['estimated_salary']:,.0f}/año** · "
            f"Las ciudades destacadas son aquellas donde tu salario cubre bien el coste de vida."
        )
    try:
        df = load_data()
    except FileNotFoundError:
        st.warning("Sin datos procesados. Ejecuta primero el notebook 02_indicators.ipynb.")
        return

    # ── Filtros ───────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        regions = st.multiselect("Región", sorted(df["region"].unique()))
    with col2:
        min_score = st.slider("Relocation Score mínimo", 0.0, 100.0, 0.0)

    df_filtered = df.copy()
    if regions:
        df_filtered = df_filtered[df_filtered["region"].isin(regions)]
    if "relocation_score" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["relocation_score"] >= min_score]

    st.caption(f"{len(df_filtered)} ciudades encontradas")

    # ── Ranking visual ────────────────────────────────────────
    st.subheader("Ranking por Relocation Score")

    top_n = st.slider("Número de ciudades en el ranking", 5, 30, 15)
    top = df_filtered.nlargest(top_n, "relocation_score").copy()
    top["label"] = top["city_name"] + " (" + top["country"] + ")"

    fig = px.bar(
        top.sort_values("relocation_score"),
        x="relocation_score",
        y="label",
        orientation="h",
        color="relocation_score",
        color_continuous_scale=["#E8593C", "#F39C12", "#2ECC71"],
        text="relocation_score",
        labels={"relocation_score": "Relocation Score", "label": ""},
    )
    fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig.update_layout(
        height=max(300, top_n * 28),
        coloraxis_showscale=False,
        margin=dict(t=20, b=20, l=10, r=60),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Métricas resumen ──────────────────────────────────────
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Mejor ciudad", top.iloc[0]["city_name"] if len(top) > 0 else "—")
    c2.metric("Score máximo", f"{df_filtered['relocation_score'].max():.1f}" if len(df_filtered) > 0 else "—")
    c3.metric("Salario medio top 10",
              f"€{df_filtered.nlargest(10, 'relocation_score')['average_salary'].mean():,.0f}"
              if len(df_filtered) >= 10 else "—")

    # ── Tabla completa ────────────────────────────────────────
    st.divider()
    st.subheader("Tabla completa")
    cols = ["city_name", "country", "region", "relocation_score",
            "average_salary", "net_salary", "average_rent",
            "purchasing_power", "tax_rate", "job_market_score"]
    cols_exist = [c for c in cols if c in df_filtered.columns]
    st.dataframe(
        df_filtered[cols_exist].sort_values("relocation_score", ascending=False)
        .reset_index(drop=True),
        use_container_width=True,
    )