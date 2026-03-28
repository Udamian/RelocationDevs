"""
city_map.py
Módulo: mapa interactivo 3D de ciudades con PyDeck.
Colorea los puntos según Relocation Score.
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
from pathlib import Path

PROCESSED = Path(__file__).parent.parent / "data" / "processed"

# Coordenadas aproximadas por país (fallback si no hay lat/lon en el dataset)
def get_coords(row):
    # Ahora usa lat/lon reales del dataset
    lat = row.get("lat", 0)
    lon = row.get("lon", 0)
    return lat if pd.notna(lat) else 0, lon if pd.notna(lon) else 0

def render():
    st.title("Mapa de ciudades")
    st.caption("Puntos coloreados por Relocation Score — verde alto, rojo bajo")

    cities_file = PROCESSED / "cities_processed.csv"
    if not cities_file.exists():
        st.warning("Sin datos procesados. Ejecuta primero el notebook 02_indicators.ipynb.")
        return

    df = pd.read_csv(cities_file)

    # Añadir coordenadas
    df["lat"] = df.apply(lambda r: get_coords(r)[0], axis=1)
    df["lon"] = df.apply(lambda r: get_coords(r)[1], axis=1)

    # Filtrar coordenadas inválidas
    df = df[(df["lat"] != 0) | (df["lon"] != 0)]

    # Normalizar relocation_score a color RGB (rojo=bajo, verde=alto)
    score_min = df["relocation_score"].min()
    score_max = df["relocation_score"].max()

    def score_to_color(score):
        t = (score - score_min) / (score_max - score_min + 1e-9)
        r = int(255 * (1 - t))
        g = int(200 * t)
        b = 80
        return [r, g, b, 200]

    df["color"] = df["relocation_score"].apply(score_to_color)
    df["radius"] = df["relocation_score"] * 8000  # tamaño proporcional al score

    # Tooltip
    df["tooltip"] = df.apply(
        lambda r: f"{r['city_name']} ({r['country']})\n"
                  f"Score: {r['relocation_score']:.1f}\n"
                  f"Salario: €{r.get('average_salary', 0):,.0f}\n"
                  f"Alquiler: €{r.get('average_rent', 0):,.0f}/mes",
        axis=1
    )

    # Filtros en sidebar
    st.sidebar.subheader("Filtros del mapa")
    regiones = sorted(df["region"].unique())
    selected_regions = st.sidebar.multiselect("Región", regiones, default=regiones)
    min_score = st.sidebar.slider("Relocation Score mínimo", 0.0, 100.0, 0.0)

    df_filtered = df[
        (df["region"].isin(selected_regions)) &
        (df["relocation_score"] >= min_score)
    ]

    st.caption(f"Mostrando {len(df_filtered)} ciudades")

    # Capa PyDeck
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
        radius_min_pixels=6,
        radius_max_pixels=40,
    )

    view_state = pdk.ViewState(
        latitude=30,
        longitude=10,
        zoom=1.5,
        pitch=40,
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{tooltip}"},
        map_style="road",
    )

    st.pydeck_chart(deck)

    # Tabla resumen debajo del mapa
    st.divider()
    st.subheader("Ranking por Relocation Score")
    cols = ["city_name", "country", "region", "relocation_score",
            "average_salary", "average_rent", "purchasing_power"]
    cols_exist = [c for c in cols if c in df_filtered.columns]
    st.dataframe(
        df_filtered[cols_exist].sort_values("relocation_score", ascending=False).reset_index(drop=True),
        use_container_width=True,
    )