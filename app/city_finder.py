"""
city_finder.py
Buscador de ciudad ideal — wizard 4 pasos.
Preguntas naturales, sin tecnicismos.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from app.styles import page_header

PROCESSED = Path(__file__).parent.parent / "data" / "processed"

COUNTRY_LANGUAGES = {
    "Germany": "Alemán", "Austria": "Alemán", "Switzerland": "Alemán",
    "France": "Francés", "Belgium": "Francés",
    "Spain": "Español", "Mexico": "Español", "Argentina": "Español",
    "Portugal": "Portugués", "Brazil": "Portugués",
    "Italy": "Italiano", "Netherlands": "Holandés",
    "Sweden": "Sueco", "Norway": "Noruego", "Denmark": "Danés", "Finland": "Finés",
    "Poland": "Polaco", "Czech Republic": "Checo", "Hungary": "Húngaro",
    "Romania": "Rumano", "Greece": "Griego",
    "United Kingdom": "Inglés", "Ireland": "Inglés",
    "United States": "Inglés", "Canada": "Inglés",
    "Australia": "Inglés", "New Zealand": "Inglés", "Singapore": "Inglés",
    "Japan": "Japonés", "South Korea": "Coreano", "China": "Chino",
    "India": "Hindi/Inglés", "United Arab Emirates": "Árabe", "Israel": "Hebreo",
    "South Africa": "Inglés", "Luxembourg": "Francés/Alemán", "Turkey": "Turco",
}

CLIMATE_MAP = {
    "Norway": "frío", "Finland": "frío", "Sweden": "frío", "Denmark": "frío",
    "Estonia": "frío", "Latvia": "frío", "Lithuania": "frío", "Canada": "frío",
    "Poland": "templado", "Czech Republic": "templado", "Germany": "templado",
    "Austria": "templado", "Hungary": "templado", "Romania": "templado",
    "United Kingdom": "templado", "Ireland": "templado", "Belgium": "templado",
    "Netherlands": "templado", "Switzerland": "templado", "France": "templado",
    "Japan": "templado", "South Korea": "templado", "New Zealand": "templado",
    "Portugal": "cálido", "Spain": "cálido", "Italy": "cálido", "Greece": "cálido",
    "Mexico": "cálido", "Colombia": "cálido", "Brazil": "cálido",
    "Singapore": "cálido", "India": "cálido",
    "United Arab Emirates": "cálido", "Israel": "cálido",
    "Australia": "cálido", "South Africa": "cálido", "Turkey": "cálido",
    "United States": "variado", "China": "variado", "Argentina": "variado",
}

PESO_MAP = {"Nada": 0, "Poco": 2, "Normal": 5, "Bastante": 8, "Mucho": 10}


def _step_indicator(current: int):
    steps = ["Dónde", "Prioridades", "Estilo de vida", "Resultado"]
    html_parts = []
    for i, label in enumerate(steps):
        if i < current:
            dot_bg = "#6e6e73"
            text_color = "#6e6e73"
            dot_size = "10px"
        elif i == current:
            dot_bg = "#f5f5f7"
            text_color = "#f5f5f7"
            dot_size = "12px"
        else:
            dot_bg = "#3a3a3c"
            text_color = "#3a3a3c"
            dot_size = "10px"

        html_parts.append(
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px;">'
            f'<div style="width:{dot_size};height:{dot_size};border-radius:50%;'
            f'background:{dot_bg};"></div>'
            f'<span style="font-size:10px;color:{text_color};letter-spacing:0.04em;">'
            f'{label}</span></div>'
        )
        if i < len(steps) - 1:
            line_color = "#6e6e73" if i < current else "#3a3a3c"
            html_parts.append(
                f'<div style="flex:1;height:1px;background:{line_color};'
                f'margin-bottom:14px;"></div>'
            )

    inner = "".join(html_parts)
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;max-width:420px;
    margin:0 auto 32px;padding:16px 24px;background:#1c1c1e;
    border-radius:12px;border:1px solid #2c2c2e;">
        {inner}
    </div>
    """, unsafe_allow_html=True)


def step_donde():
    _step_indicator(0)

    st.markdown("""
    <h2 style="font-size:22px;font-weight:600;color:#f5f5f7;
    letter-spacing:-0.02em;margin-bottom:6px;">
        ¿Dónde te imaginas viviendo?
    </h2>
    <p style="font-size:14px;color:#6e6e73;margin-bottom:28px;">
        No tienes que tenerlo claro — cuéntanos tus preferencias generales.
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        regiones = st.multiselect(
            "¿Qué partes del mundo te atraen?",
            ["Europe", "Americas", "Asia", "Middle East", "Oceania", "Africa"],
            default=["Europe"],
        )
        clima = st.select_slider(
            "¿Qué tipo de clima prefieres?",
            options=["frío", "templado", "cálido", "me da igual"],
            value="templado",
        )

    with col2:
        idiomas = st.multiselect(
            "¿Qué idiomas hablas?",
            ["Inglés", "Español", "Francés", "Alemán", "Portugués",
             "Italiano", "Holandés", "Sueco", "Polaco", "Chino", "Japonés"],
            default=["Inglés", "Español"],
        )
        solo_idioma = st.toggle(
            "Prefiero un país donde pueda comunicarme",
            value=True,
            help="Filtra ciudades donde no hablas el idioma oficial"
        )

    _, col_next = st.columns([1, 1])
    with col_next:
        if st.button("Siguiente →", type="primary", use_container_width=True):
            if not regiones:
                st.warning("Selecciona al menos una región.")
                return
            st.session_state.finder = {
                "regiones": regiones,
                "clima": clima,
                "idiomas": idiomas,
                "solo_idioma": solo_idioma,
            }
            st.session_state.finder_step = 1
            st.rerun()


def step_prioridades():
    _step_indicator(1)

    p = st.session_state.get("profile", {})
    estimated = p.get("estimated_salary", 0) or 0

    st.markdown(f"""
    <h2 style="font-size:22px;font-weight:600;color:#f5f5f7;
    letter-spacing:-0.02em;margin-bottom:6px;">
        ¿Qué es lo más importante para ti?
    </h2>
    <p style="font-size:14px;color:#6e6e73;margin-bottom:28px;">
        Con tu perfil estimamos un salario de
        <strong style="color:#aeaeb2;">€{estimated:,.0f}/año</strong>.
        Dinos cuánto importa cada factor.
    </p>
    """, unsafe_allow_html=True)

    opciones = ["Nada", "Poco", "Normal", "Bastante", "Mucho"]

    col1, col2 = st.columns(2, gap="large")

    with col1:
        poder = st.select_slider(
            "¿Cuánto te importa el poder adquisitivo?",
            options=opciones, value="Bastante",
            help="Que el dinero que ganes te cunda de verdad"
        )
        ahorro = st.select_slider(
            "¿Cuánto valoras poder ahorrar?",
            options=opciones, value="Bastante",
            help="Tener margen al final del mes"
        )

    with col2:
        impuestos = st.select_slider(
            "¿Te preocupa pagar muchos impuestos?",
            options=opciones, value="Normal",
            help="Priorizar países con menor carga fiscal"
        )
        alquiler = st.select_slider(
            "¿Es importante que el alquiler sea barato?",
            options=opciones, value="Bastante",
            help="Ciudades donde la vivienda no se lleve todo el sueldo"
        )

    col_back, col_next = st.columns([1, 1])
    with col_back:
        if st.button("← Atrás", use_container_width=True):
            st.session_state.finder_step = 0
            st.rerun()
    with col_next:
        if st.button("Siguiente →", type="primary", use_container_width=True):
            st.session_state.finder.update({
                "peso_poder":     PESO_MAP[poder],
                "peso_ahorro":    PESO_MAP[ahorro],
                "peso_impuestos": PESO_MAP[impuestos],
                "peso_alquiler":  PESO_MAP[alquiler],
            })
            st.session_state.finder_step = 2
            st.rerun()


def step_estilo():
    _step_indicator(2)

    st.markdown("""
    <h2 style="font-size:22px;font-weight:600;color:#f5f5f7;
    letter-spacing:-0.02em;margin-bottom:6px;">
        ¿Cómo quieres vivir allí?
    </h2>
    <p style="font-size:14px;color:#6e6e73;margin-bottom:28px;">
        Cuéntanos qué tipo de vida buscas en tu nueva ciudad.
    </p>
    """, unsafe_allow_html=True)

    opciones = ["Nada", "Poco", "Normal", "Bastante", "Mucho"]

    col1, col2 = st.columns(2, gap="large")

    with col1:
        calidad = st.select_slider(
            "¿Cuánto valoras la calidad de vida general?",
            options=opciones, value="Mucho",
            help="Seguridad, sanidad, transporte, entorno"
        )
        mercado = st.select_slider(
            "¿Necesitas un buen mercado tech local?",
            options=opciones, value="Normal",
            help="Oportunidades de empleo presencial en la ciudad"
        )

    with col2:
        remoto = st.toggle(
            "Trabajo en remoto",
            value=False,
            help="Si trabajas en remoto, el mercado local importa menos"
        )
        st.markdown("""
        <div style="background:#1c1c1e;border:1px solid #2c2c2e;border-radius:10px;
        padding:14px 16px;margin-top:8px;">
            <p style="font-size:12px;color:#6e6e73;margin:0;line-height:1.6;">
                Si trabajas en remoto podemos priorizar ciudades con buena calidad de vida
                y bajo coste, sin importar si tienen mucho tejido tech local.
            </p>
        </div>
        """, unsafe_allow_html=True)

    col_back, col_next = st.columns([1, 1])
    with col_back:
        if st.button("← Atrás", use_container_width=True):
            st.session_state.finder_step = 1
            st.rerun()
    with col_next:
        if st.button("Encontrar mis ciudades ideales →",
                     type="primary", use_container_width=True):
            peso_mercado = PESO_MAP[mercado]
            if remoto:
                peso_mercado = max(0, peso_mercado - 4)
            st.session_state.finder.update({
                "peso_calidad": PESO_MAP[calidad],
                "peso_mercado": peso_mercado,
                "remoto":       remoto,
            })
            st.session_state.finder_step = 3
            st.rerun()


def compute_compatibility(df: pd.DataFrame, prefs: dict, profile: dict) -> pd.DataFrame:
    df = df.copy()
    estimated = profile.get("estimated_salary", 0) or 0

    # Salario neto y ahorro estimados del usuario en cada ciudad
    df["user_net_salary"]      = estimated * (1 - df["tax_rate"] / 100)
    df["user_monthly_savings"] = (df["user_net_salary"] - df["average_rent"] * 12) / 12

    # ── Filtros duros ─────────────────────────────────────────
    if prefs.get("regiones"):
        df = df[df["region"].isin(prefs["regiones"])]

    clima = prefs.get("clima", "me da igual")
    if clima != "me da igual":
        df["_clima"] = df["country"].map(CLIMATE_MAP).fillna("variado")
        df = df[df["_clima"].isin([clima, "variado"])]

    if prefs.get("solo_idioma") and prefs.get("idiomas"):
        def idioma_ok(country):
            lang = COUNTRY_LANGUAGES.get(country, "")
            return any(i.lower() in lang.lower() for i in prefs["idiomas"])
        df = df[df["country"].apply(idioma_ok)]

    # Filtrar ciudades donde el ahorro sería negativo extremo
    df = df[df["user_monthly_savings"] > -500]

    if df.empty:
        return df

    # ── Normalizar features ───────────────────────────────────
    def norm(s):
        mn, mx = s.min(), s.max()
        return pd.Series([0.5] * len(s), index=s.index) if mx == mn \
               else (s - mn) / (mx - mn)

    df["_n_poder"]   = norm(df["purchasing_power_index"])
    df["_n_calidad"] = norm(df["quality_of_life_index"])
    df["_n_mercado"] = norm(df["job_market_score"])
    df["_n_fiscal"]  = norm(100 - df["tax_rate"])
    df["_n_alquiler"]= norm(-df["average_rent"])
    df["_n_ahorro"]  = norm(df["user_monthly_savings"])

    # ── Scoring ponderado ─────────────────────────────────────
    wp = prefs.get("peso_poder",     8)
    wc = prefs.get("peso_calidad",   8)
    wm = prefs.get("peso_mercado",   5)
    wf = prefs.get("peso_impuestos", 5)
    wa = prefs.get("peso_alquiler",  6)
    ws = prefs.get("peso_ahorro",    6)
    total = wp + wc + wm + wf + wa + ws or 1

    df["compatibility_score"] = (
        df["_n_poder"]    * wp +
        df["_n_calidad"]  * wc +
        df["_n_mercado"]  * wm +
        df["_n_fiscal"]   * wf +
        df["_n_alquiler"] * wa +
        df["_n_ahorro"]   * ws
    ) / total * 100

    return df.sort_values("compatibility_score", ascending=False)


def _explain_city(row, prefs):
    pros, cons = [], []
    if row.get("purchasing_power_index", 0) > 80:
        pros.append("Alto poder adquisitivo")
    elif row.get("purchasing_power_index", 0) < 50:
        cons.append("Poder adquisitivo limitado")
    if row.get("average_rent", 9999) < 1000:
        pros.append(f"Alquiler asequible (€{row['average_rent']:,.0f}/mes)")
    elif row.get("average_rent", 0) > 2000:
        cons.append(f"Alquiler elevado (€{row['average_rent']:,.0f}/mes)")
    if row.get("tax_rate", 50) < 30:
        pros.append(f"Baja carga fiscal ({row['tax_rate']:.0f}%)")
    elif row.get("tax_rate", 0) > 45:
        cons.append(f"Alta carga fiscal ({row['tax_rate']:.0f}%)")
    if row.get("quality_of_life_index", 0) > 150:
        pros.append("Excelente calidad de vida")
    elif row.get("quality_of_life_index", 0) < 100:
        cons.append("Calidad de vida moderada")
    if row.get("job_market_score", 0) > 70:
        pros.append("Mercado tech activo")
    lang = COUNTRY_LANGUAGES.get(row.get("country", ""), "")
    idiomas = prefs.get("idiomas", [])
    if any(i.lower() in lang.lower() for i in idiomas):
        pros.append(f"Idioma conocido ({lang})")
    else:
        cons.append(f"Idioma local: {lang}")
    return pros[:3], cons[:2]


def step_resultado(df_full):
    _step_indicator(3)

    prefs   = st.session_state.get("finder", {})
    profile = st.session_state.get("profile", {})
    df_res  = compute_compatibility(df_full, prefs, profile)

    st.markdown("""
    <h2 style="font-size:22px;font-weight:600;color:#f5f5f7;
    letter-spacing:-0.02em;margin-bottom:6px;">Tus ciudades ideales</h2>
    """, unsafe_allow_html=True)

    if df_res.empty:
        st.markdown("""
        <div style="background:#1c1c1e;border:1px solid #2c2c2e;border-radius:12px;
        padding:32px;text-align:center;">
            <p style="font-size:16px;color:#6e6e73;">
                Ninguna ciudad cumple todos los criterios.<br>
                <span style="font-size:13px;">
                Prueba a ampliar las regiones o cambiar el filtro de idioma.
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Volver a empezar", use_container_width=True):
            st.session_state.finder_step = 0
            st.rerun()
        return

    top5 = df_res.head(5).reset_index(drop=True)
    total_ok = len(df_res)

    st.markdown(f"""
    <p style="font-size:13px;color:#6e6e73;margin-bottom:24px;">
        {total_ok} ciudades encajan con tu perfil · mostrando las 5 mejores
    </p>
    """, unsafe_allow_html=True)

    # ── Cards de resultado ────────────────────────────────────
    rank_colors = ["#f5f5f7", "#aeaeb2", "#8e8e93", "#6e6e73", "#3a3a3c"]

    for i, row in top5.iterrows():
        pros, cons = _explain_city(row, prefs)
        score = int(row["compatibility_score"])
        border = "1px solid #3a3a3c" if i == 0 else "1px solid #2c2c2e"
        shadow = "box-shadow:0 0 0 1px #f5f5f720;" if i == 0 else ""

        # Construir pros y cons HTML fuera del f-string
        pros_html = "".join(
            f'<div style="font-size:12px;color:#aeaeb2;margin-bottom:3px;">'
            f'✓ {p}</div>' for p in pros
        )
        cons_html = "".join(
            f'<div style="font-size:12px;color:#6e6e73;margin-bottom:3px;">'
            f'✗ {c}</div>' for c in cons
        )

        st.markdown(f"""
        <div style="background:#1c1c1e;border:{border};border-radius:16px;
        padding:24px 28px;margin-bottom:12px;{shadow}">
            <div style="display:flex;align-items:flex-start;
            justify-content:space-between;margin-bottom:16px;">
                <div>
                    <div style="display:flex;align-items:center;
                    gap:10px;margin-bottom:4px;">
                        <span style="font-size:13px;color:{rank_colors[i]};
                        font-weight:600;">#{i+1}</span>
                        <span style="font-size:20px;font-weight:600;
                        color:#f5f5f7;letter-spacing:-0.02em;">
                            {row['city_name']}
                        </span>
                        <span style="font-size:13px;color:#6e6e73;">
                            {row['country']} · {row.get('region','')}
                        </span>
                    </div>
                    <div style="display:flex;gap:16px;font-size:12px;color:#aeaeb2;">
                        <span>€{row.get('user_net_salary',0):,.0f}/año neto</span>
                        <span>€{row.get('average_rent',0):,.0f}/mes alquiler</span>
                        <span>€{max(0,row.get('user_monthly_savings',0)):,.0f}/mes ahorro</span>
                    </div>
                </div>
                <div style="text-align:right;min-width:90px;">
                    <div style="font-size:28px;font-weight:700;color:#f5f5f7;
                    letter-spacing:-0.03em;line-height:1;">{score}</div>
                    <div style="font-size:10px;color:#6e6e73;letter-spacing:0.06em;
                    text-transform:uppercase;">compatibilidad</div>
                    <div style="width:80px;height:3px;background:#2c2c2e;
                    border-radius:2px;margin-top:6px;margin-left:auto;">
                        <div style="width:{score}%;height:100%;background:#f5f5f7;
                        border-radius:2px;"></div>
                    </div>
                </div>
            </div>
            <div style="display:flex;gap:24px;">
                <div style="flex:1;">{pros_html}</div>
                <div style="flex:1;">{cons_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Radar comparativo ─────────────────────────────────────
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:11px;font-weight:600;color:#6e6e73;
    letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;">
        Comparativa radar
    </p>
    """, unsafe_allow_html=True)

    metrics = ["purchasing_power_index", "job_market_score",
               "quality_of_life_index", "relocation_score"]
    labels  = ["Poder adquisitivo", "Mercado tech",
               "Calidad de vida", "Relocation Score"]
    colors  = ["#f5f5f7", "#aeaeb2", "#8e8e93", "#6e6e73", "#3a3a3c"]

    fig = go.Figure()
    for i, row in top5.iterrows():
        vals = [row.get(m, 0) for m in metrics]
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name=row["city_name"],
            line_color=colors[i],
            opacity=max(0.3, 0.8 - i * 0.12),
        ))

    fig.update_layout(
        polar=dict(
            bgcolor="#1c1c1e",
            radialaxis=dict(visible=True, gridcolor="#2c2c2e",
                           tickfont=dict(color="#6e6e73", size=10)),
            angularaxis=dict(gridcolor="#2c2c2e",
                            tickfont=dict(color="#aeaeb2", size=11)),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(font=dict(color="#aeaeb2", size=11),
                   bgcolor="rgba(0,0,0,0)"),
        height=380,
        margin=dict(t=20, b=20, l=40, r=40),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Acciones ──────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Ajustar criterios", use_container_width=True):
            st.session_state.finder_step = 0
            st.rerun()
    with col2:
        if st.button("Comparar top 3 en City Comparison →",
                     type="primary", use_container_width=True):
            st.session_state.comparison_preselect = \
                top5["city_name"].tolist()[:3]
            st.rerun()


def render():
    page_header(
        "Buscador de ciudad ideal",
        "Responde 3 preguntas y encontramos tus mejores opciones"
    )

    cities_file = PROCESSED / "cities_processed.csv"
    if not cities_file.exists():
        st.warning("Sin datos procesados. Ejecuta primero el notebook 02_indicators.ipynb.")
        return

    df = pd.read_csv(cities_file)

    if "finder_step" not in st.session_state:
        st.session_state.finder_step = 0
    if "finder" not in st.session_state:
        st.session_state.finder = {}

    step = st.session_state.finder_step
    if step == 0:
        step_donde()
    elif step == 1:
        step_prioridades()
    elif step == 2:
        step_estilo()
    elif step == 3:
        step_resultado(df)