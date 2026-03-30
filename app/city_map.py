"""
city_map.py
Mapa 3D con PyDeck. Click en punto -> vista detallada de la ciudad.
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.graph_objects as go
from pathlib import Path

PROCESSED = Path(__file__).parent.parent / "data" / "processed"

COUNTRY_COORDS = {
    "Germany": (51.16, 10.45), "France": (46.23, 2.21), "Spain": (40.46, -3.74),
    "Italy": (42.83, 12.83), "Netherlands": (52.13, 5.29), "Belgium": (50.50, 4.47),
    "Switzerland": (46.82, 8.23), "Austria": (47.52, 14.55), "Portugal": (39.40, -8.22),
    "Sweden": (60.13, 18.64), "Norway": (60.47, 8.47), "Denmark": (56.26, 9.50),
    "Finland": (61.92, 25.75), "Poland": (51.92, 19.15), "United Kingdom": (55.38, -3.44),
    "Ireland": (53.41, -8.24), "United States": (37.09, -95.71), "Canada": (56.13, -106.35),
    "Australia": (-25.27, 133.78), "Japan": (36.20, 138.25), "South Korea": (35.91, 127.77),
    "Singapore": (1.35, 103.82), "India": (20.59, 78.96), "Brazil": (-14.24, -51.93),
    "Mexico": (23.63, -102.55), "Argentina": (-38.42, -63.62), "China": (35.86, 104.20),
    "United Arab Emirates": (23.42, 53.85), "Israel": (31.05, 34.85),
    "Czech Republic": (49.82, 15.47), "Romania": (45.94, 24.97),
    "Greece": (39.07, 21.82), "Hungary": (47.16, 19.50), "Luxembourg": (49.82, 6.13),
    "New Zealand": (-40.90, 174.89), "South Africa": (-30.56, 22.94),
}


def get_coords(row):
    lat = row.get("lat")
    lon = row.get("lon")
    if pd.notna(lat) and pd.notna(lon) and (float(lat) != 0 or float(lon) != 0):
        return float(lat), float(lon)
    return COUNTRY_COORDS.get(row.get("country", ""), (0, 0))


def score_to_color(score, score_min, score_max):
    t = (score - score_min) / (score_max - score_min + 1e-9)
    return [int(255 * (1 - t)), int(200 * t), 80, 200]


def render_detail(city_row):
    """Vista detallada de una ciudad seleccionada."""
    st.subheader(f"{city_row['city_name']} — {city_row['country']}")
    st.caption(f"Región: {city_row.get('region', '—')}")

    # Métricas principales
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Relocation Score", f"{city_row.get('relocation_score', 0):.1f}")
    c2.metric("Salario medio", f"€{city_row.get('average_salary', 0):,.0f}")
    c3.metric("Alquiler", f"€{city_row.get('average_rent', 0):,.0f}/mes")
    c4.metric("Poder adquisitivo", f"{city_row.get('purchasing_power', 0):.1f}")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Salario neto est.", f"€{city_row.get('net_salary', 0):,.0f}")
        st.metric("Tasa impositiva", f"{city_row.get('tax_rate', 0):.1f}%")
        st.metric("Coste de vida", f"{city_row.get('cost_of_living_index', 0):.1f}")

    with col2:
        st.metric("Calidad de vida", f"{city_row.get('quality_of_life_index', 0):.1f}")
        st.metric("Mercado laboral", f"{city_row.get('job_market_score', 0):.1f}")
        st.metric("Ahorro anual est.", f"€{city_row.get('net_salary', 0) * 0.3:,.0f}")

    # Radar chart de la ciudad
    metrics = ['cost_of_living_index', 'purchasing_power_index',
               'quality_of_life_index', 'job_market_score', 'relocation_score']
    labels  = ['Coste de vida', 'Poder adquisitivo',
               'Calidad de vida', 'Mercado laboral', 'Relocation Score']

    values = [city_row.get(m, 0) for m in metrics]
    values_closed = values + [values[0]]
    labels_closed = labels + [labels[0]]

    fig = go.Figure(go.Scatterpolar(
        r=values_closed, theta=labels_closed,
        fill='toself', line_color='#4A90D9', opacity=0.7,
        name=city_row['city_name']
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False, height=350,
        margin=dict(t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)

    def reset_map_view():
        st.session_state["selected_city_map"] = "— ninguna —"
        
    if st.button("Volver al mapa", on_click=reset_map_view):
        pass


def render():
    st.title("Mapa de ciudades")

    cities_file = PROCESSED / "cities_processed.csv"
    if not cities_file.exists():
        st.warning("Sin datos procesados.")
        return

    df = pd.read_csv(cities_file)

    # Coordenadas
    df["lat"] = df.apply(lambda r: get_coords(r)[0], axis=1)
    df["lon"] = df.apply(lambda r: get_coords(r)[1], axis=1)
    df = df[(df["lat"] != 0) | (df["lon"] != 0)]

    # Colores y radios
    score_min = df["relocation_score"].min()
    score_max = df["relocation_score"].max()
    df["color"]  = df["relocation_score"].apply(lambda s: score_to_color(s, score_min, score_max))
    df["radius"] = df["relocation_score"] * 3000

    # Tooltip
    df["tooltip"] = df.apply(
        lambda r: f"{r['city_name']} ({r['country']})\nScore: {r['relocation_score']:.1f}\n€{r.get('average_salary',0):,.0f}/año · €{r.get('average_rent',0):,.0f}/mes",
        axis=1
    )

    # Filtros
    st.sidebar.subheader("Filtros del mapa")
    regiones = sorted(df["region"].unique())
    selected_regions = st.sidebar.multiselect("Región", regiones, default=regiones)
    min_score = st.sidebar.slider("Score mínimo", 0.0, 100.0, 0.0)

    df_filtered = df[
        (df["region"].isin(selected_regions)) &
        (df["relocation_score"] >= min_score)
    ]

    # Selector de ciudad por click simulado
    st.sidebar.divider()
    st.sidebar.subheader("Ver detalle de ciudad")
    city_names = sorted(df_filtered["city_name"].unique())
    selected = st.sidebar.selectbox(
        "Selecciona una ciudad", 
        ["— ninguna —"] + city_names,
        key="selected_city_map"
    )

    if selected != "— ninguna —":
        city_row = df_filtered[df_filtered["city_name"] == selected].iloc[0]
        render_detail(city_row)
        return

    # Mapa
    st.caption(f"Mostrando {len(df_filtered)} ciudades · verde = mejor score · rojo = peor score")

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_filtered,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius="radius",
        pickable=True,
        opacity=0.85,
        stroked=True,
        filled=True,
        radius_min_pixels=4,
        radius_max_pixels=20,
        radius_scale=0.5,
    )

    view_state = pdk.ViewState(latitude=30, longitude=10, zoom=2, pitch=40)

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{tooltip}"},
        map_style="road",
    )

    st.pydeck_chart(deck)

    # Ranking debajo del mapa
    st.divider()
    st.subheader("Top ciudades por Relocation Score")
    cols = ["city_name", "country", "region", "relocation_score",
            "average_salary", "average_rent", "purchasing_power"]
    cols_exist = [c for c in cols if c in df_filtered.columns]
    st.dataframe(
        df_filtered[cols_exist].sort_values("relocation_score", ascending=False)
        .head(20).reset_index(drop=True),
        use_container_width=True,
    )