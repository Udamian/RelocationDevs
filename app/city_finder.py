"""
city_finder.py
Buscador de ciudad ideal — wizard 3 pasos + resultado.
Radar pentagonal con suma cero visual.
Afinidad cultural por bloques específico + general.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from app.styles import page_header

PROCESSED = Path(__file__).parent.parent / "data" / "processed"

# ── Bloques culturales ────────────────────────────────────────
# Cada país tiene un bloque ESPECÍFICO y uno GENERAL
# España = ["Occidental", "Mediterráneo"] — base de comparación
CULTURAL_BLOCKS = {
    # Europa mediterránea
    "Spain":       {"general": "Occidental", "specific": "Mediterráneo"},
    "Italy":       {"general": "Occidental", "specific": "Mediterráneo"},
    "Portugal":    {"general": "Occidental", "specific": "Mediterráneo"},
    "Greece":      {"general": "Occidental", "specific": "Mediterráneo"},
    "France":      {"general": "Occidental", "specific": "Mediterráneo"},
    # Europa occidental
    "Germany":     {"general": "Occidental", "specific": "Centroeuropeo"},
    "Austria":     {"general": "Occidental", "specific": "Centroeuropeo"},
    "Switzerland": {"general": "Occidental", "specific": "Centroeuropeo"},
    "Netherlands": {"general": "Occidental", "specific": "Centroeuropeo"},
    "Belgium":     {"general": "Occidental", "specific": "Centroeuropeo"},
    "Luxembourg":  {"general": "Occidental", "specific": "Centroeuropeo"},
    # Europa anglosajona
    "United Kingdom": {"general": "Occidental", "specific": "Anglosajón"},
    "Ireland":        {"general": "Occidental", "specific": "Anglosajón"},
    "United States":  {"general": "Occidental", "specific": "Anglosajón"},
    "Canada":         {"general": "Occidental", "specific": "Anglosajón"},
    "Australia":      {"general": "Occidental", "specific": "Anglosajón"},
    "New Zealand":    {"general": "Occidental", "specific": "Anglosajón"},
    # Europa nórdica
    "Sweden":  {"general": "Occidental", "specific": "Nórdico"},
    "Norway":  {"general": "Occidental", "specific": "Nórdico"},
    "Denmark": {"general": "Occidental", "specific": "Nórdico"},
    "Finland": {"general": "Occidental", "specific": "Nórdico"},
    # Europa del este
    "Poland":         {"general": "Europeo", "specific": "Eslavo"},
    "Czech Republic": {"general": "Europeo", "specific": "Eslavo"},
    "Hungary":        {"general": "Europeo", "specific": "Centroeuropeo"},
    "Romania":        {"general": "Europeo", "specific": "Eslavo"},
    "Bulgaria":       {"general": "Europeo", "specific": "Eslavo"},
    "Croatia":        {"general": "Europeo", "specific": "Eslavo"},
    "Slovakia":       {"general": "Europeo", "specific": "Eslavo"},
    "Slovenia":       {"general": "Europeo", "specific": "Eslavo"},
    "Estonia":        {"general": "Europeo", "specific": "Báltico"},
    "Latvia":         {"general": "Europeo", "specific": "Báltico"},
    "Lithuania":      {"general": "Europeo", "specific": "Báltico"},
    # Latinoamérica
    "Mexico":    {"general": "Hispanohablante", "specific": "Latinoamericano"},
    "Argentina": {"general": "Hispanohablante", "specific": "Latinoamericano"},
    "Colombia":  {"general": "Hispanohablante", "specific": "Latinoamericano"},
    "Chile":     {"general": "Hispanohablante", "specific": "Latinoamericano"},
    "Brazil":    {"general": "Occidental",       "specific": "Latinoamericano"},
    # Asia
    "Japan":       {"general": "Asiático", "specific": "Oriental"},
    "South Korea": {"general": "Asiático", "specific": "Oriental"},
    "China":       {"general": "Asiático", "specific": "Oriental"},
    "Singapore":   {"general": "Asiático", "specific": "Anglosajón"},
    "India":       {"general": "Asiático", "specific": "Anglosajón"},
    # Oriente Medio
    "United Arab Emirates": {"general": "Oriente Medio", "specific": "Árabe"},
    "Israel":               {"general": "Oriente Medio", "specific": "Mediterráneo"},
    "Turkey":               {"general": "Oriente Medio", "specific": "Mediterráneo"},
    # Otros
    "South Africa": {"general": "Africano", "specific": "Anglosajón"},
}

# Base cultural de España (punto de referencia)
BASE_GENERAL  = "Occidental"
BASE_SPECIFIC = "Mediterráneo"

# ── Estabilidad por país (0-100 hardcodeado) ──────────────────
STABILITY_SCORES = {
    "Norway": 98, "Denmark": 97, "Finland": 97, "Sweden": 96,
    "Switzerland": 96, "New Zealand": 95, "Australia": 94,
    "Canada": 94, "Netherlands": 93, "Luxembourg": 93,
    "Germany": 92, "Austria": 91, "Ireland": 91,
    "United Kingdom": 89, "Japan": 89, "United States": 87,
    "Belgium": 87, "France": 85, "Singapore": 85,
    "South Korea": 84, "Portugal": 83, "Spain": 82,
    "Czech Republic": 81, "Slovenia": 80, "Estonia": 80,
    "Italy": 78, "Latvia": 77, "Lithuania": 76,
    "Poland": 76, "Slovakia": 75, "Hungary": 73,
    "Croatia": 72, "Greece": 70, "Israel": 68,
    "Romania": 65, "Bulgaria": 63, "South Africa": 58,
    "Serbia": 57, "Turkey": 54, "India": 60,
    "China": 62, "Brazil": 55, "Mexico": 52,
    "Colombia": 50, "Argentina": 48,
    "United Arab Emirates": 75,
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
    "Singapore": "cálido", "India": "cálido", "Turkey": "cálido",
    "United Arab Emirates": "cálido", "Israel": "cálido",
    "Australia": "cálido", "South Africa": "cálido",
    "United States": "variado", "China": "variado", "Argentina": "variado",
}


def cultural_affinity(country: str) -> float:
    """
    Score de afinidad cultural con España (0-100).
    Usa dos bloques: general y específico.
    - Mismo bloque general Y específico → 100
    - Solo mismo bloque general → 55
    - Mismo bloque específico (distinto general) → 35
    - Ninguno → 10
    """
    blocks = CULTURAL_BLOCKS.get(country, {})
    g = blocks.get("general", "")
    s = blocks.get("specific", "")

    if g == BASE_GENERAL and s == BASE_SPECIFIC:
        return 100.0
    elif g == BASE_GENERAL:
        return 55.0
    elif s == BASE_SPECIFIC:
        return 35.0
    else:
        return 10.0


# ── Indicador de pasos ─────────────────────────────────────────
def _step_indicator(current: int):
    steps = ["¿Dónde?", "Prioridades", "Estilo de vida", "Resultado"]
    parts = []
    for i, label in enumerate(steps):
        if i < current:
            dot, text, size = "#6e6e73", "#6e6e73", "10px"
        elif i == current:
            dot, text, size = "#f5f5f7", "#f5f5f7", "13px"
        else:
            dot, text, size = "#3a3a3c", "#3a3a3c", "10px"

        parts.append(
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:5px;">'
            f'<div style="width:{size};height:{size};border-radius:50%;'
            f'background:{dot};transition:all 0.3s;"></div>'
            f'<span style="font-size:10px;color:{text};letter-spacing:0.04em;'
            f'white-space:nowrap;">{label}</span></div>'
        )
        if i < len(steps) - 1:
            line = "#6e6e73" if i < current else "#3a3a3c"
            parts.append(
                f'<div style="flex:1;height:1px;background:{line};'
                f'margin-bottom:15px;min-width:30px;"></div>'
            )

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;
    max-width:520px;margin:0 auto 40px;padding:22px 32px;
    background:#1c1c1e;border-radius:16px;border:1px solid #2c2c2e;">
        {"".join(parts)}
    </div>
    """, unsafe_allow_html=True)


def _section_title(title, subtitle=""):
    sub = (f'<p style="font-size:15px;color:#6e6e73;margin:8px 0 32px;'
           f'line-height:1.6;">{subtitle}</p>') if subtitle else ""
    st.markdown(f"""
    <h2 style="font-size:26px;font-weight:600;color:#f5f5f7;
    letter-spacing:-0.02em;margin-bottom:0;">{title}</h2>{sub}
    """, unsafe_allow_html=True)


# ── PASO 1: ¿Dónde? ───────────────────────────────────────────
def step_donde():
    _step_indicator(0)
    _section_title(
        "¿Dónde te imaginas viviendo?",
        "No tienes que tenerlo claro — cuéntanos tus preferencias generales."
    )

    col1, col2 = st.columns(2, gap="large")
    with col1:
        regiones = st.multiselect(
            "¿Qué partes del mundo te atraen?",
            ["Europe", "Americas", "Asia", "Middle East", "Oceania", "Africa"],
            default=["Europe"],
        )
        clima = st.select_slider(
            "¿Qué clima prefieres?",
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
        )

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    _, col_next = st.columns([1, 1])
    with col_next:
        if st.button("Siguiente →", type="primary", use_container_width=True):
            if not regiones:
                st.warning("Selecciona al menos una región.")
                return
            st.session_state.finder = {
                "regiones":    regiones,
                "clima":       clima,
                "idiomas":     idiomas,
                "solo_idioma": solo_idioma,
            }
            st.session_state.finder_step = 1
            st.rerun()


# ── PASO 2: Radar pentagonal de prioridades ───────────────────
VERTICES = {
    "ahorro":    {"label": "Capacidad de ahorro",  "desc": "Cuánto dinero puedes guardar al año"},
    "wlb":       {"label": "Work-Life Balance",     "desc": "Tiempo libre, descanso, bienestar"},
    "tech":      {"label": "Ecosistema tech",       "desc": "Oportunidades y comunidad tecnológica"},
    "cultura":   {"label": "Afinidad cultural",     "desc": "Cercanía cultural con España"},
    "estabilidad":{"label": "Estabilidad del país", "desc": "Seguridad política y social"},
}

VERTEX_KEYS   = list(VERTICES.keys())
VERTEX_LABELS = [VERTICES[k]["label"] for k in VERTEX_KEYS]


def _build_radar(values: dict) -> go.Figure:
    """Radar pentagonal con los 5 vértices. Valores normalizados 0-100."""
    vals = [values.get(k, 20) for k in VERTEX_KEYS]
    vals_closed = vals + [vals[0]]
    labels_closed = VERTEX_LABELS + [VERTEX_LABELS[0]]

    fig = go.Figure()

    # Área de relleno
    fig.add_trace(go.Scatterpolar(
        r=vals_closed,
        theta=labels_closed,
        fill="toself",
        fillcolor="rgba(245,245,247,0.08)",
        line=dict(color="#f5f5f7", width=2),
        mode="lines+markers",
        marker=dict(size=6, color="#f5f5f7"),
        showlegend=False,
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="#1c1c1e",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="#2c2c2e",
                tickfont=dict(color="#3a3a3c", size=9),
                tickvals=[25, 50, 75, 100],
                ticktext=["25", "50", "75", "100"],
                linecolor="#2c2c2e",
            ),
            angularaxis=dict(
                gridcolor="#2c2c2e",
                linecolor="#3a3a3c",
                tickfont=dict(color="#aeaeb2", size=12),
                rotation=90,
                direction="clockwise",
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=380,
        margin=dict(t=40, b=40, l=60, r=60),
    )
    return fig


def _normalize_suma_cero(raw: dict) -> dict:
    """
    Normaliza los valores al rango 0-100 manteniendo proporciones.
    Comportamiento suma-cero: el área total del polígono es constante.
    """
    total = sum(raw.values()) or 1
    return {k: round(v / total * 100, 1) for k, v in raw.items()}


def step_prioridades():
    _step_indicator(1)

    p = st.session_state.get("profile", {})
    estimated = p.get("estimated_salary", 0) or 0

    _section_title(
        "¿Qué valoras más en tu nueva vida?",
        f"Mueve los sliders para definir tus prioridades. "
        f"El radar se adapta automáticamente — al subir uno, el peso "
        f"de los demás se redistribuye. Salario estimado: €{estimated:,.0f}/año."
    )

    # Inicializar valores si no existen
    defaults = {"ahorro": 50, "wlb": 40, "tech": 35, "cultura": 30, "estabilidad": 45}
    for k, v in defaults.items():
        if f"pri_{k}" not in st.session_state:
            st.session_state[f"pri_{k}"] = v

    # Layout: sliders izquierda, radar derecha
    col_sliders, col_radar = st.columns([1, 1], gap="large")

    raw_vals = {}

    with col_sliders:
        st.markdown("""
        <div style="background:#1c1c1e;border:1px solid #2c2c2e;
        border-radius:14px;padding:24px 22px;">
        """, unsafe_allow_html=True)

        for k, meta in VERTICES.items():
            st.markdown(f"""
            <div style="margin-bottom:4px;">
                <span style="font-size:13px;font-weight:600;color:#f5f5f7;">
                    {meta['label']}
                </span>
                <span style="font-size:11px;color:#6e6e73;margin-left:8px;">
                    {meta['desc']}
                </span>
            </div>
            """, unsafe_allow_html=True)

            val = st.slider(
                k, 0, 100,
                st.session_state[f"pri_{k}"],
                label_visibility="collapsed",
                key=f"sl_{k}",
            )
            st.session_state[f"pri_{k}"] = val
            raw_vals[k] = val

            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Normalizar para suma cero
    norm_vals = _normalize_suma_cero(raw_vals)

    with col_radar:
        # Radar live
        fig = _build_radar(norm_vals)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Leyenda de porcentajes
        legend_parts = []
        for k in VERTEX_KEYS:
            pct = norm_vals[k]
            bar_w = f"{pct:.0f}%"
            legend_parts.append(
                f'<div style="display:flex;align-items:center;gap:10px;'
                f'margin-bottom:8px;">'
                f'<span style="font-size:11px;color:#6e6e73;width:130px;'
                f'flex-shrink:0;">{VERTICES[k]["label"]}</span>'
                f'<div style="flex:1;height:4px;background:#2c2c2e;'
                f'border-radius:2px;overflow:hidden;">'
                f'<div style="width:{bar_w};height:100%;background:#f5f5f7;'
                f'border-radius:2px;transition:width 0.3s;"></div></div>'
                f'<span style="font-size:11px;color:#aeaeb2;width:36px;'
                f'text-align:right;">{pct:.0f}%</span>'
                f'</div>'
            )

        st.markdown(f"""
        <div style="background:#1c1c1e;border:1px solid #2c2c2e;
        border-radius:12px;padding:16px 18px;margin-top:8px;">
            <p style="font-size:10px;color:#6e6e73;letter-spacing:0.08em;
            text-transform:uppercase;margin:0 0 12px;">Distribución normalizada</p>
            {"".join(legend_parts)}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    col_back, col_next = st.columns([1, 1])
    with col_back:
        if st.button("← Atrás", use_container_width=True):
            st.session_state.finder_step = 0
            st.rerun()
    with col_next:
        if st.button("Siguiente →", type="primary", use_container_width=True):
            if sum(raw_vals.values()) == 0:
                st.warning("Mueve al menos un slider para continuar.")
                return
            st.session_state.finder["prioridades"] = norm_vals
            st.session_state.finder_step = 2
            st.rerun()


# ── PASO 3: Estilo de vida ─────────────────────────────────────
def step_estilo():
    _step_indicator(2)
    _section_title(
        "¿Cómo quieres que sea tu día a día?",
        "Cuéntanos qué aspectos de la vida fuera del trabajo te importan más."
    )

    opciones = ["No me importa", "Algo importante", "Importante", "Muy importante"]
    peso_map = {"No me importa": 0, "Algo importante": 3,
                "Importante": 7, "Muy importante": 10}

    col1, col2 = st.columns(2, gap="large")
    with col1:
        vida_social = st.select_slider(
            "Vida social y ocio nocturno",
            options=opciones, value="Importante",
            help="Bares, clubs, eventos, vida nocturna activa"
        )
        restaurantes = st.select_slider(
            "Oferta gastronómica y restaurantes",
            options=opciones, value="Algo importante",
            help="Diversidad culinaria, mercados, restaurantes"
        )
    with col2:
        seguridad = st.select_slider(
            "Seguridad ciudadana",
            options=opciones, value="Muy importante",
            help="Sentirte seguro en tu día a día"
        )
        remoto = st.toggle(
            "Trabajo en remoto",
            value=False,
            help="Priorizaremos calidad de vida sobre ecosistema tech local"
        )
        if remoto:
            st.markdown("""
            <div style="background:#1c1c1e;border:1px solid #2c2c2e;
            border-radius:10px;padding:12px 14px;margin-top:8px;">
                <p style="font-size:12px;color:#6e6e73;margin:0;line-height:1.5;">
                    En remoto priorizamos ciudades con alta calidad de vida
                    y buen poder adquisitivo.
                </p>
            </div>
            """, unsafe_allow_html=True)

    col_back, col_next = st.columns([1, 1])
    with col_back:
        if st.button("← Atrás", use_container_width=True):
            st.session_state.finder_step = 1
            st.rerun()
    with col_next:
        if st.button("Encontrar mis ciudades →",
                     type="primary", use_container_width=True):
            st.session_state.finder.update({
                "w_vida_social":  peso_map[vida_social],
                "w_restaurantes": peso_map[restaurantes],
                "w_seguridad":    peso_map[seguridad],
                "remoto":         remoto,
            })
            st.session_state.finder_step = 3
            st.rerun()


# ── Scoring ────────────────────────────────────────────────────
def compute_compatibility(df: pd.DataFrame, prefs: dict, profile: dict) -> pd.DataFrame:
    df = df.copy()
    estimated = profile.get("estimated_salary", 0) or 0

    df["user_net_salary"]     = estimated * (1 - df["tax_rate"] / 100)
    df["user_annual_savings"] = (df["user_net_salary"] - df["average_rent"] * 12)
    df["cultural_affinity"]   = df["country"].apply(cultural_affinity)
    df["stability_score"]     = df["country"].map(STABILITY_SCORES).fillna(50)

    # ── Filtros duros ─────────────────────────────────────────
    if prefs.get("regiones"):
        df = df[df["region"].isin(prefs["regiones"])]

    clima = prefs.get("clima", "me da igual")
    if clima != "me da igual":
        df["_clima"] = df["country"].map(CLIMATE_MAP).fillna("variado")
        df = df[df["_clima"].isin([clima, "variado"])]

    if prefs.get("solo_idioma") and prefs.get("idiomas"):
        COUNTRY_LANGUAGES = {
            "Germany": "Alemán", "Austria": "Alemán", "Switzerland": "Alemán",
            "France": "Francés", "Belgium": "Francés",
            "Spain": "Español", "Mexico": "Español", "Argentina": "Español",
            "Portugal": "Portugués", "Brazil": "Portugués",
            "Italy": "Italiano", "Netherlands": "Holandés",
            "Sweden": "Sueco", "Norway": "Noruego", "Denmark": "Danés",
            "Finland": "Finés", "Poland": "Polaco",
            "United Kingdom": "Inglés", "Ireland": "Inglés",
            "United States": "Inglés", "Canada": "Inglés",
            "Australia": "Inglés", "New Zealand": "Inglés",
            "Singapore": "Inglés", "India": "Hindi/Inglés",
            "Japan": "Japonés", "South Korea": "Coreano", "China": "Chino",
            "United Arab Emirates": "Árabe", "Israel": "Hebreo",
        }
        def idioma_ok(country):
            lang = COUNTRY_LANGUAGES.get(country, "")
            return any(i.lower() in lang.lower() for i in prefs["idiomas"])
        df = df[df["country"].apply(idioma_ok)]

    df = df[df["user_annual_savings"] > -5000]

    if df.empty:
        return df

    # ── Normalizar features ───────────────────────────────────
    def norm(s):
        mn, mx = s.min(), s.max()
        if mx == mn:
            return pd.Series([0.5] * len(s), index=s.index)
        return (s - mn) / (mx - mn)

    df["_n_ahorro"]    = norm(df["user_annual_savings"])
    df["_n_wlb"]       = norm(df["quality_of_life_index"])
    df["_n_tech"]      = norm(df["job_market_score"])
    df["_n_cultura"]   = norm(df["cultural_affinity"])
    df["_n_estab"]     = norm(df["stability_score"])

    # Estilo de vida como componente adicional
    w_social = prefs.get("w_vida_social", 7)
    w_rest   = prefs.get("w_restaurantes", 3)
    w_seg    = prefs.get("w_seguridad", 10)
    w_e_total = w_social + w_rest + w_seg or 1
    df["_n_estilo"] = (
        df["_n_wlb"]    * (w_social + w_seg) / w_e_total +
        df["_n_ahorro"] * w_rest              / w_e_total
    )

    # Pesos del radar normalizado
    pri = prefs.get("prioridades", {
        "ahorro": 20, "wlb": 20, "tech": 20, "cultura": 20, "estabilidad": 20
    })

    w_ahorro = pri.get("ahorro", 20) / 100
    w_wlb    = pri.get("wlb",    20) / 100
    w_tech   = pri.get("tech",   20) / 100
    w_cult   = pri.get("cultura", 20) / 100
    w_estab  = pri.get("estabilidad", 20) / 100

    # Remoto reduce peso de tech
    if prefs.get("remoto"):
        extra = w_tech * 0.5
        w_wlb   += extra * 0.5
        w_ahorro += extra * 0.5
        w_tech  -= extra

    # Score base del radar + componente de estilo de vida
    w_estilo_extra = (w_social + w_rest + w_seg) / 30 * 0.15

    df["compatibility_score"] = (
        df["_n_ahorro"]  * w_ahorro  * 100 +
        df["_n_wlb"]     * w_wlb     * 100 +
        df["_n_tech"]    * w_tech    * 100 +
        df["_n_cultura"] * w_cult    * 100 +
        df["_n_estab"]   * w_estab   * 100 +
        df["_n_estilo"]  * w_estilo_extra * 100
    ) / (1 + w_estilo_extra)

    return df.sort_values("compatibility_score", ascending=False)


def _explain_city(row, prefs):
    pros, cons = [], []

    savings = row.get("user_annual_savings", 0)
    if savings > 12000:
        pros.append(f"Ahorro potencial de €{savings:,.0f}/año")
    elif savings < 2000:
        cons.append(f"Ahorro limitado (~€{max(0,savings):,.0f}/año)")

    aff = row.get("cultural_affinity", 10)
    country = row.get("country", "")
    blocks = CULTURAL_BLOCKS.get(country, {})
    if aff >= 100:
        pros.append(f"Alta afinidad cultural (Occidental · Mediterráneo)")
    elif aff >= 55:
        pros.append(f"Afinidad cultural moderada ({blocks.get('general','')})")
    else:
        cons.append(f"Cultura diferente ({blocks.get('general','')} · {blocks.get('specific','')})")

    stab = row.get("stability_score", 50)
    if stab >= 88:
        pros.append(f"País muy estable ({stab}/100)")
    elif stab < 60:
        cons.append(f"Estabilidad moderada ({stab}/100)")

    if row.get("tax_rate", 50) < 25:
        pros.append(f"Baja carga fiscal ({row['tax_rate']:.0f}%)")
    elif row.get("tax_rate", 0) > 45:
        cons.append(f"Alta presión fiscal ({row['tax_rate']:.0f}%)")

    if row.get("quality_of_life_index", 0) > 155:
        pros.append("Excelente calidad de vida")

    clima_ciudad = CLIMATE_MAP.get(country, "variado")
    clima_pref   = prefs.get("clima", "me da igual")
    if clima_pref != "me da igual" and clima_ciudad == clima_pref:
        pros.append(f"Clima {clima_ciudad} como prefieres")

    return pros[:3], cons[:2]


# ── PASO 4: Resultado ──────────────────────────────────────────
def step_resultado(df_full):
    _step_indicator(3)

    prefs   = st.session_state.get("finder", {})
    profile = st.session_state.get("profile", {})
    df_res  = compute_compatibility(df_full, prefs, profile)

    _section_title("Tus ciudades ideales")

    if df_res.empty:
        st.markdown("""
        <div style="background:#1c1c1e;border:1px solid #2c2c2e;
        border-radius:12px;padding:40px;text-align:center;">
            <p style="font-size:16px;color:#6e6e73;line-height:1.6;">
                Ninguna ciudad cumple todos los criterios.<br>
                <span style="font-size:13px;">
                Prueba a ampliar las regiones o desactivar el filtro de idioma.
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Volver a empezar", use_container_width=True):
            st.session_state.finder_step = 0
            st.rerun()
        return

    top5        = df_res.head(5).reset_index(drop=True)
    total_ok    = len(df_res)
    rank_colors = ["#f5f5f7", "#aeaeb2", "#8e8e93", "#6e6e73", "#3a3a3c"]

    st.markdown(f"""
    <p style="font-size:13px;color:#6e6e73;margin-bottom:28px;">
        {total_ok} ciudades encajan con tu perfil · mostrando las 5 mejores
    </p>
    """, unsafe_allow_html=True)

    for i, row in top5.iterrows():
        pros, cons  = _explain_city(row, prefs)
        score       = int(row["compatibility_score"])
        border      = "1px solid #3a3a3c" if i == 0 else "1px solid #2c2c2e"
        shadow      = "box-shadow:0 0 0 1px #f5f5f715;" if i == 0 else ""
        net         = row.get("user_net_salary", 0)
        rent        = row.get("average_rent", 0)
        saving      = max(0, row.get("user_annual_savings", 0))
        country     = row.get("country", "")
        blocks      = CULTURAL_BLOCKS.get(country, {})
        cult_badge  = (f'{blocks.get("general","")} · '
                       f'{blocks.get("specific","")}') if blocks else ""
        stab        = int(row.get("stability_score", 50))

        pros_html = "".join(
            f'<div style="font-size:12px;color:#aeaeb2;margin-bottom:4px;'
            f'display:flex;align-items:flex-start;gap:6px;">'
            f'<span style="color:#6e6e73;flex-shrink:0;">✓</span>{p}</div>'
            for p in pros
        )
        cons_html = "".join(
            f'<div style="font-size:12px;color:#6e6e73;margin-bottom:4px;'
            f'display:flex;align-items:flex-start;gap:6px;">'
            f'<span style="flex-shrink:0;">✗</span>{c}</div>'
            for c in cons
        )

        st.markdown(f"""
        <div style="background:#1c1c1e;border:{border};border-radius:16px;
        padding:24px 28px;margin-bottom:12px;{shadow}">
            <div style="display:flex;align-items:flex-start;
            justify-content:space-between;margin-bottom:16px;">
                <div style="flex:1;">
                    <div style="display:flex;align-items:center;
                    gap:10px;margin-bottom:8px;flex-wrap:wrap;">
                        <span style="font-size:13px;color:{rank_colors[i]};
                        font-weight:700;">#{i+1}</span>
                        <span style="font-size:22px;font-weight:600;
                        color:#f5f5f7;letter-spacing:-0.02em;">
                            {row['city_name']}
                        </span>
                        <span style="font-size:13px;color:#6e6e73;">
                            {country} · {row.get('region','')}
                        </span>
                    </div>
                    <div style="display:flex;gap:16px;flex-wrap:wrap;
                    margin-bottom:10px;">
                        <span style="font-size:12px;color:#aeaeb2;">
                            Neto €{net:,.0f}/año
                        </span>
                        <span style="font-size:12px;color:#aeaeb2;">
                            Alquiler €{rent:,.0f}/mes
                        </span>
                        <span style="font-size:12px;color:#aeaeb2;">
                            Ahorro €{saving:,.0f}/año
                        </span>
                    </div>
                    <div style="display:flex;gap:8px;flex-wrap:wrap;">
                        <span style="font-size:10px;color:#6e6e73;
                        background:#2c2c2e;border-radius:6px;
                        padding:3px 8px;">{cult_badge}</span>
                        <span style="font-size:10px;color:#6e6e73;
                        background:#2c2c2e;border-radius:6px;
                        padding:3px 8px;">Estabilidad {stab}/100</span>
                    </div>
                </div>
                <div style="text-align:right;min-width:90px;margin-left:20px;">
                    <div style="font-size:34px;font-weight:700;color:#f5f5f7;
                    letter-spacing:-0.03em;line-height:1;">{score}</div>
                    <div style="font-size:9px;color:#6e6e73;
                    letter-spacing:0.08em;text-transform:uppercase;
                    margin-top:2px;">compatibilidad</div>
                    <div style="width:70px;height:3px;background:#2c2c2e;
                    border-radius:2px;margin:8px 0 0 auto;">
                        <div style="width:{score}%;height:100%;
                        background:#f5f5f7;border-radius:2px;"></div>
                    </div>
                </div>
            </div>
            <div style="display:flex;gap:32px;padding-top:14px;
            border-top:1px solid #2c2c2e;">
                <div style="flex:1;">{pros_html}</div>
                <div style="flex:1;">{cons_html}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Radar comparativo top 5 ───────────────────────────────
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:11px;font-weight:600;color:#6e6e73;
    letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">
        Comparativa de factores
    </p>
    """, unsafe_allow_html=True)

    colors = ["#f5f5f7", "#aeaeb2", "#8e8e93", "#6e6e73", "#3a3a3c"]
    fig = go.Figure()

    for i, row in top5.iterrows():
        vals = [
            row.get("_n_ahorro", 0)  * 100,
            row.get("_n_wlb", 0)     * 100,
            row.get("_n_tech", 0)    * 100,
            row.get("cultural_affinity", 10),
            row.get("stability_score", 50),
        ]
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=VERTEX_LABELS + [VERTEX_LABELS[0]],
            fill="toself",
            name=row["city_name"],
            line_color=colors[i],
            opacity=max(0.2, 0.75 - i * 0.12),
        ))

    fig.update_layout(
        polar=dict(
            bgcolor="#1c1c1e",
            radialaxis=dict(visible=True, range=[0, 100],
                           gridcolor="#2c2c2e",
                           tickfont=dict(color="#6e6e73", size=9)),
            angularaxis=dict(gridcolor="#2c2c2e",
                            tickfont=dict(color="#aeaeb2", size=11),
                            rotation=90, direction="clockwise"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(font=dict(color="#aeaeb2", size=11),
                   bgcolor="rgba(0,0,0,0)"),
        height=420, margin=dict(t=20, b=20, l=40, r=40),
    )
    st.plotly_chart(fig, use_container_width=True,
                   config={"displayModeBar": False})

    # ── Acciones ──────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Ajustar criterios", use_container_width=True):
            st.session_state.finder_step = 0
            st.rerun()
    with col2:
        if st.button("Comparar top 3 en Comparador →",
                     type="primary", use_container_width=True):
            st.session_state.comparison_preselect = \
                top5["city_name"].tolist()[:3]
            st.session_state.redirect_to = "Comparador"
            st.rerun()


# ── Entry point ───────────────────────────────────────────────
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
    if   step == 0: step_donde()
    elif step == 1: step_prioridades()
    elif step == 2: step_estilo()
    elif step == 3: step_resultado(df)