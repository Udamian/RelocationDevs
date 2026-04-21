"""
city_map.py
Mapa profesional con Folium + CartoDB Dark Matter.
MarkerCluster para evitar aglomeraciones.
Popup rico al hacer click en cada ciudad.
"""

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
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
# Correcciones manuales para ciudades con coordenadas incorrectas en worldcitiespop
CITY_COORDS_OVERRIDE = {
    ("Valencia", "Spain"):           (39.4699, -0.3763),
    ("Vigo", "Spain"):               (42.2406, -8.7207),
    ("Honolulu", "United States"):   (21.3069, -157.8583),
    ("Guadalajara", "Mexico"):       (20.6597, -103.3496),
    ("Monterrey", "Mexico"):         (25.6866, -100.3161),
    ("Cancun", "Mexico"):            (21.1619, -86.8515),
    ("Shanghai", "China"):           (31.2304, 121.4737),
    ("Beijing", "China"):            (39.9042, 116.4074),
    ("Guangzhou", "China"):          (23.1291, 113.2644),
}


def get_coords(row):
    city    = row.get("city_name", "")
    country = row.get("country", "")

    # 1. Override manual — máxima prioridad
    override = CITY_COORDS_OVERRIDE.get((city, country))
    if override:
        return override

    # 2. lat/lon del dataset si son válidas
    try:
        lat = float(row.get("lat", 0) or 0)
        lon = float(row.get("lon", 0) or 0)
        if -90 <= lat <= 90 and -180 <= lon <= 180 and (abs(lat) > 0.1 or abs(lon) > 0.1):
            return lat, lon
    except (ValueError, TypeError):
        pass

    # 3. Fallback al centroide del país
    return COUNTRY_COORDS.get(country, (0, 0))


def score_to_color(score, score_min, score_max):
    """Verde para scores altos, rojo para bajos."""
    t = (score - score_min) / (score_max - score_min + 1e-9)
    if t > 0.66:
        return "#2ECC71"   # verde
    elif t > 0.33:
        return "#F39C12"   # naranja
    else:
        return "#E74C3C"   # rojo


def get_stat_color(val, min_val, max_val, higher_is_better=True):
    try:
        val = float(val)
        min_val = float(min_val)
        max_val = float(max_val)
    except (ValueError, TypeError):
        return "#333333"

    if max_val <= min_val + 1e-9:
        return "#333333"

    t = (val - min_val) / (max_val - min_val)
    if not higher_is_better:
        t = 1.0 - t

    if t > 0.66:
        return "#229954" # verde oscuro
    elif t > 0.33:
        return "#D35400" # naranja oscuro
    else:
        return "#C0392B" # rojo oscuro


def build_popup(row, bounds):
    score = row.get("relocation_score", 0)
    score_color = "#2ECC71" if score > 60 else "#F39C12" if score > 40 else "#E74C3C"

    avg_salary = row.get('average_salary', 0)
    net_salary = row.get('net_salary', 0)
    avg_rent = row.get('average_rent', 0)
    col_index = row.get('cost_of_living_index', 0)
    purch_power = row.get('purchasing_power', 0)
    tax_rate = row.get('tax_rate', 0)
    ahorro = net_salary * 0.3

    c_salary = get_stat_color(avg_salary, bounds['average_salary'][0], bounds['average_salary'][1], True)
    c_net = get_stat_color(net_salary, bounds['net_salary'][0], bounds['net_salary'][1], True)
    c_rent = get_stat_color(avg_rent, bounds['average_rent'][0], bounds['average_rent'][1], False)
    c_col = get_stat_color(col_index, bounds['cost_of_living_index'][0], bounds['cost_of_living_index'][1], False)
    c_pp = get_stat_color(purch_power, bounds['purchasing_power'][0], bounds['purchasing_power'][1], True)
    c_tax = get_stat_color(tax_rate, bounds['tax_rate'][0], bounds['tax_rate'][1], False)
    c_ahorro = get_stat_color(ahorro, bounds['ahorro'][0], bounds['ahorro'][1], True)

    html = f"""
    <div style="font-family: Arial, sans-serif; min-width: 220px; padding: 4px;">
        <h4 style="margin: 0 0 6px 0; color: #333333; font-size: 16px;">
            {row.get('city_name', '')}
        </h4>
        <p style="margin: 0 0 8px 0; color: #666666; font-size: 13px;">
            {row.get('country', '')} &middot; {row.get('region', '')}
        </p>
        <div style="background: #F8F9F9; border: 1px solid #E5E7E9; border-radius: 6px; padding: 6px 8px; margin-bottom: 8px; text-align: center;">
            <span style="color: {score_color}; font-size: 24px; font-weight: bold;">
                {score:.1f}
            </span>
            <span style="color: #666; font-size: 13px;"> / 100</span>
            <p style="margin: 2px 0 0 0; color: #666; font-size: 12px;">Relocation Score</p>
        </div>
        <table style="width: 100%; font-size: 13px; border-collapse: collapse;">
            <tr>
                <td style="color: #555555; padding: 2px 0;">Salario bruto</td>
                <td style="color: {c_salary}; text-align: right; font-weight: bold;">&euro;{avg_salary:,.0f}/año</td>
            </tr>
            <tr>
                <td style="color: #555555; padding: 2px 0;">Salario neto est.</td>
                <td style="color: {c_net}; text-align: right; font-weight: bold;">&euro;{net_salary:,.0f}/año</td>
            </tr>
            <tr>
                <td style="color: #555555; padding: 2px 0;">Alquiler medio</td>
                <td style="color: {c_rent}; text-align: right; font-weight: bold;">&euro;{avg_rent:,.0f}/mes</td>
            </tr>
            <tr>
                <td style="color: #555555; padding: 2px 0;">Coste de vida</td>
                <td style="color: {c_col}; text-align: right; font-weight: bold;">{col_index:.1f}</td>
            </tr>
            <tr>
                <td style="color: #555555; padding: 2px 0;">Poder adquisitivo</td>
                <td style="color: {c_pp}; text-align: right; font-weight: bold;">{purch_power:.1f}</td>
            </tr>
            <tr>
                <td style="color: #555555; padding: 2px 0;">Impuestos</td>
                <td style="color: {c_tax}; text-align: right; font-weight: bold;">{tax_rate:.1f}%</td>
            </tr>
            <tr>
                <td style="color: #555555; padding: 2px 0;">Ahorro anual est.</td>
                <td style="color: {c_ahorro}; text-align: right; font-weight: bold;">&euro;{ahorro:,.0f}</td>
            </tr>
        </table>
    </div>
    """
    return folium.Popup(
        folium.IFrame(html, width=270, height=310),
        max_width=290
    )


def render():
    st.title("Mapa de ciudades")
    st.caption("Verde = mejor Relocation Score · Los puntos se agrupan al alejar el zoom · Haz click para ver detalles")

    cities_file = PROCESSED / "cities_processed.csv"
    if not cities_file.exists():
        st.warning("Sin datos procesados. Ejecuta primero el notebook 02_indicators.ipynb.")
        return

    df = pd.read_csv(cities_file)

    # Coordenadas
    df["_lat"] = df.apply(lambda r: get_coords(r)[0], axis=1)
    df["_lon"] = df.apply(lambda r: get_coords(r)[1], axis=1)
    df = df[(df["_lat"] != 0) | (df["_lon"] != 0)]

    # Filtros en sidebar
    st.sidebar.subheader("Filtros del mapa")
    regiones = sorted(df["region"].dropna().unique())
    selected_regions = st.sidebar.multiselect("Región", regiones, default=regiones)
    min_score = st.sidebar.slider("Score mínimo", 0.0, 100.0, 0.0)

    df_filtered = df[
        (df["region"].isin(selected_regions)) &
        (df["relocation_score"] >= min_score)
    ]

    if df_filtered.empty:
        st.warning("No hay ciudades que coincidan con los filtros.")
        return

    score_min = df_filtered["relocation_score"].min()
    score_max = df_filtered["relocation_score"].max()

    bounds = {
        'average_salary': (df_filtered['average_salary'].min(), df_filtered['average_salary'].max()) if 'average_salary' in df_filtered else (0,0),
        'net_salary': (df_filtered['net_salary'].min(), df_filtered['net_salary'].max()) if 'net_salary' in df_filtered else (0,0),
        'average_rent': (df_filtered['average_rent'].min(), df_filtered['average_rent'].max()) if 'average_rent' in df_filtered else (0,0),
        'cost_of_living_index': (df_filtered['cost_of_living_index'].min(), df_filtered['cost_of_living_index'].max()) if 'cost_of_living_index' in df_filtered else (0,0),
        'purchasing_power': (df_filtered['purchasing_power'].min(), df_filtered['purchasing_power'].max()) if 'purchasing_power' in df_filtered else (0,0),
        'tax_rate': (df_filtered['tax_rate'].min(), df_filtered['tax_rate'].max()) if 'tax_rate' in df_filtered else (0,0),
        'ahorro': ((df_filtered['net_salary']*0.3).min(), (df_filtered['net_salary']*0.3).max()) if 'net_salary' in df_filtered else (0,0)
    }

    st.caption(f"Mostrando {len(df_filtered)} ciudades")

    # ── Mapa Folium ───────────────────────────────────────────
    m = folium.Map(
        location=[30, 10],
        zoom_start=2,
        tiles="CartoDB dark_matter",
        prefer_canvas=True,
    )

    # Cluster de marcadores
    cluster = MarkerCluster(
        options={
            "maxClusterRadius": 40,
            "disableClusteringAtZoom": 5,
            "spiderfyOnMaxZoom": True,
        }
    ).add_to(m)

    for _, row in df_filtered.iterrows():
        lat, lon = row["_lat"], row["_lon"]
        color = score_to_color(row["relocation_score"], score_min, score_max)

        folium.CircleMarker(
            location=[lat, lon],
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            weight=1.5,
            popup=build_popup(row, bounds),
            tooltip=folium.Tooltip(
                f"<b>{row['city_name']}</b><br>"
                f"Score: {row['relocation_score']:.1f}",
                style="font-family: Arial; font-size: 14px;"
            ),
        ).add_to(cluster)

    # Leyenda personalizada
    legend_html = """
    <div style="
        position: fixed; bottom: 30px; left: 30px; z-index: 1000;
        background: rgba(20,20,20,0.85); border-radius: 8px;
        padding: 10px 14px; font-family: Arial; font-size: 14px; color: #DDD;
        border: 1px solid #444;
    ">
        <b style="color:#FFF;">Relocation Score</b><br>
        <span style="color:#2ECC71;">&#9679;</span> Alto (&gt; 66)<br>
        <span style="color:#F39C12;">&#9679;</span> Medio (33–66)<br>
        <span style="color:#E74C3C;">&#9679;</span> Bajo (&lt; 33)
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Renderizar en Streamlit
    st_folium(m, width="100%", height=750, returned_objects=[])

    # ── Ranking debajo del mapa ───────────────────────────────
    st.divider()
    st.subheader("Top ciudades por Relocation Score")
    cols = ["city_name", "country", "region", "relocation_score",
            "average_salary", "average_rent", "net_salary", "purchasing_power"]
    cols_exist = [c for c in cols if c in df_filtered.columns]
    st.dataframe(
        df_filtered[cols_exist]
        .sort_values("relocation_score", ascending=False)
        .head(20)
        .reset_index(drop=True),
        use_container_width=True,
    )