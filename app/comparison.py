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

def _render_elegant_table(df):
    css = """
    <style>
    .comp-grid {
        display: grid;
        gap: 12px;
        margin-top: 16px;
    }
    .comp-row {
        display: grid;
        gap: 12px;
        background: #1c1c1e;
        border: 1px solid #2c2c2e;
        border-radius: 12px;
        padding: 16px;
        align-items: center;
    }
    .comp-cell {
        font-size: 14px;
        color: #aeaeb2;
    }
    .comp-header {
        background: transparent;
        border: none;
        padding: 0 16px 8px;
    }
    .comp-city-title {
        font-size: 18px;
        font-weight: 600;
        color: #f5f5f7;
    }
    .comp-city-country {
        font-size: 12px;
        color: #6e6e73;
    }
    .best-value {
        color: #f5f5f7;
        font-weight: 600;
        background: rgba(46, 204, 113, 0.15);
        border: 1px solid rgba(46, 204, 113, 0.3);
        border-radius: 8px;
        padding: 4px 8px;
        display: inline-block;
    }
    .metric-name {
        color: #f5f5f7;
        font-weight: 500;
    }
    </style>
    """
    num_cities = len(df)
    grid_template = f"1fr repeat({num_cities}, 1fr)"
    css += f"<style>.comp-row {{ grid-template-columns: {grid_template}; }}</style>"
    
    html = [css, '<div class="comp-grid">']
    
    # Header Row
    html.append('<div class="comp-row comp-header">')
    html.append('<div></div>')
    for _, row in df.iterrows():
        html.append(f'''
        <div class="comp-cell">
            <div class="comp-city-title">{row["city_name"]}</div>
            <div class="comp-city-country">{row["country"]}</div>
        </div>
        ''')
    html.append('</div>')
    
    NEGATIVE_METRICS = ["average_rent", "cost_of_living_index"]
    FORMATTING = {
        "average_salary": lambda v: f"€{v:,.0f}/año",
        "net_salary": lambda v: f"€{v:,.0f}/año",
        "average_rent": lambda v: f"€{v:,.0f}/mes",
        "cost_of_living_index": lambda v: f"{v:,.1f}",
        "purchasing_power": lambda v: f"{v:,.1f}",
        "relocation_score": lambda v: f"{v:,.1f}",
        "job_market_score": lambda v: f"{v:,.1f}",
        "quality_of_life_index": lambda v: f"{v:,.1f}",
    }
    
    for metric_key, metric_label in METRICS.items():
        if metric_key not in df.columns:
            continue
            
        if metric_key in NEGATIVE_METRICS:
            best_val = df[metric_key].min()
        else:
            best_val = df[metric_key].max()
            
        html.append('<div class="comp-row">')
        html.append(f'<div class="comp-cell metric-name">{metric_label}</div>')
        
        for _, row in df.iterrows():
            val = row[metric_key]
            fmt_val = FORMATTING.get(metric_key, lambda v: str(v))(val)
            css_class = "best-value" if val == best_val else ""
            
            if css_class:
                html.append(f'<div class="comp-cell"><span class="{css_class}">{fmt_val} ✨</span></div>')
            else:
                html.append(f'<div class="comp-cell">{fmt_val}</div>')
                
        html.append('</div>')
        
    import re
    final_html = "".join(html)
    final_html = re.sub(r'^[ \t]+', '', final_html, flags=re.MULTILINE)
    st.markdown(final_html, unsafe_allow_html=True)


def render():
    page_header("City Comparison", "Compara ciudades en múltiples dimensiones")

    cities_file = PROCESSED / "cities_processed.csv"
    if not cities_file.exists():
        st.warning("Sin datos procesados. Ejecuta primero el notebook 02_indicators.ipynb.")
        return

    df = pd.read_csv(cities_file)
    city_names = sorted(df["city_name"].unique())

    if "comparison_selected" not in st.session_state:
        st.session_state.comparison_selected = []
        
    if "comparison_preselect" in st.session_state and st.session_state.comparison_preselect:
        st.session_state.comparison_selected = [c for c in st.session_state.comparison_preselect if c in city_names]
        st.session_state.comparison_preselect = []

    selected = st.multiselect(
        "Selecciona ciudades para comparar",
        city_names,
        key="comparison_selected",
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
    st.markdown("""
    <h2 style="font-size:20px;font-weight:600;color:#f5f5f7;
    margin-bottom:8px;">Comparativa al detalle</h2>
    """, unsafe_allow_html=True)
    
    _render_elegant_table(subset)