"""
comparison.py
Módulo: comparación de ciudades lado a lado con barras y radar chart.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from app.styles import page_header
PROCESSED = Path(__file__).parent.parent / "data" / "processed"

METRICS = {
    "average_salary":       "Salario medio (€)",
    "net_salary":           "Salario neto (€)",
    "average_rent":         "Alquiler (€/mes)",
    "cost_of_living_index": "Coste de vida",
    "purchasing_power":     "Poder adquisitivo",
    "relocation_score":     "Relocation Score",
    "job_market_score":     "Mercado laboral",
    "quality_of_life_index":"Calidad de vida",
}

COLORS = ["#4A90D9", "#E8593C", "#2ECC71", "#F39C12", "#9B59B6"]


def render():
    page_header("City Comparison", "Compara ciudades en múltiples dimensiones")

    cities_file = PROCESSED / "cities_processed.csv"
    if not cities_file.exists():
        st.warning("Sin datos procesados. Ejecuta primero el notebook 02_indicators.ipynb.")
        return

    df = pd.read_csv(cities_file)
    city_names = sorted(df["city_name"].unique())

    selected = st.multiselect(
        "Selecciona ciudades para comparar",
        city_names,
        max_selections=5,
        placeholder="Elige entre 2 y 5 ciudades..."
    )

    if len(selected) < 2:
        st.info("Selecciona al menos 2 ciudades para comparar.")
        return

    subset = df[df["city_name"].isin(selected)].copy()

    # ── Tabs: Barras vs Radar ──────────────────────────────────
    tab1, tab2 = st.tabs(["Barras por métrica", "Radar chart"])

    with tab1:
        # Selector de métrica
        metric_label = st.selectbox(
            "Métrica a comparar",
            options=list(METRICS.keys()),
            format_func=lambda x: METRICS[x],
        )

        if metric_label in subset.columns:
            fig = go.Figure()
            for i, (_, row) in enumerate(subset.iterrows()):
                fig.add_trace(go.Bar(
                    name=row["city_name"],
                    x=[row["city_name"]],
                    y=[row[metric_label]],
                    marker_color=COLORS[i % len(COLORS)],
                    text=f"{row[metric_label]:,.1f}",
                    textposition="outside",
                ))
            fig.update_layout(
                title=METRICS[metric_label],
                showlegend=False,
                height=400,
                margin=dict(t=50, b=20),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Métricas disponibles para el radar
        radar_cols = [c for c in METRICS.keys() if c in subset.columns
                      and c not in ["average_salary", "net_salary", "average_rent"]]

        if len(radar_cols) < 3:
            st.warning("No hay suficientes métricas para mostrar el radar chart.")
        else:
            # Normalizar al rango 0-100 para que todas las métricas sean comparables
            subset_norm = subset.copy()
            for col in radar_cols:
                col_min = df[col].min()
                col_max = df[col].max()
                if col_max > col_min:
                    subset_norm[col] = ((subset[col] - col_min) / (col_max - col_min) * 100).round(1)
                else:
                    subset_norm[col] = 50

            labels = [METRICS[c] for c in radar_cols]

            fig = go.Figure()
            for i, (_, row) in enumerate(subset_norm.iterrows()):
                values = [row[c] for c in radar_cols]
                values_closed = values + [values[0]]  # cerrar el polígono
                labels_closed = labels + [labels[0]]

                fig.add_trace(go.Scatterpolar(
                    r=values_closed,
                    theta=labels_closed,
                    fill="toself",
                    name=row["city_name"],
                    line_color=COLORS[i % len(COLORS)],
                    opacity=0.7,
                ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        tickfont=dict(size=10),
                    )
                ),
                showlegend=True,
                height=500,
                margin=dict(t=30, b=30),
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Valores normalizados al rango 0-100 para permitir comparación entre métricas con distintas escalas.")

    # ── Tabla resumen ──────────────────────────────────────────
    st.divider()
    st.subheader("Tabla comparativa")
    cols_show = ["city_name", "country"] + [c for c in METRICS.keys() if c in subset.columns]
    st.dataframe(
        subset[cols_show].set_index("city_name").astype(str).T,
        use_container_width=True,
    )