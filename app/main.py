"""
main.py — Punto de entrada RelocationDevs.
Sistema de diseño Midnight Silver · by a Cambeiro
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.styles import inject_styles, render_sidebar_brand, render_footer, page_header

PROCESSED = Path(__file__).parent.parent / "data" / "processed"
ASSETS    = Path(__file__).parent.parent / "assets"

st.set_page_config(
    page_title="RelocationDevs",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

inject_styles()

# ── Mapa de posiciones unificadas ──────────────────────────────
# Cada posición mapea a (role, specialization) del modelo ML
POSITIONS = {
    "Data Scientist":         ("Data scientist or machine learning specialist", "AI/ML"),
    "ML Engineer":            ("Machine learning engineer",                     "AI/ML"),
    "Data Engineer":          ("Data engineer",                                 "Data Engineer"),
    "Data Analyst":           ("Data or business analyst",                      "Data Engineer"),
    "Frontend Developer":     ("Developer, front-end",                          "Frontend"),
    "Backend Developer":      ("Developer, back-end",                           "Backend"),
    "Full Stack Developer":   ("Developer, full-stack",                         "Backend"),
    "Mobile Developer":       ("Developer, mobile",                             "Mobile"),
    "DevOps / Cloud Engineer":("DevOps specialist",                             "Cloud"),
    "Cloud Architect":        ("Cloud infrastructure engineer",                 "Cloud"),
    "Security Engineer":      ("Security professional",                         "Backend"),
    "QA Engineer":            ("Developer, QA or test",                         "General"),
    "Product Manager":        ("Product manager",                               "General"),
    "Engineering Manager":    ("Engineering manager",                           "General"),
    "System Administrator":   ("System administrator",                          "Cloud"),
}


@st.cache_data
def load_countries():
    df = pd.read_csv(PROCESSED / "salaries.csv")
    return sorted(df["city_name"].dropna().unique().tolist())


def get_logo_html():
    import base64
    try:
        raw_svg = (ASSETS / "logo.svg").read_bytes()
    except FileNotFoundError:
        raw_svg = b"""<svg width="48" height="48" viewBox="0 0 32 32" fill="none"
             xmlns="http://www.w3.org/2000/svg">
          <circle cx="16" cy="16" r="15" stroke="#f5f5f7" stroke-width="1.5"/>
          <circle cx="16" cy="16" r="4" fill="#f5f5f7"/>
          <line x1="16" y1="2" x2="16" y2="8" stroke="#f5f5f7" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="16" y1="24" x2="16" y2="30" stroke="#f5f5f7" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="2" y1="16" x2="8" y2="16" stroke="#f5f5f7" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="24" y1="16" x2="30" y2="16" stroke="#f5f5f7" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="16" y1="12" x2="20" y2="8" stroke="#aeaeb2" stroke-width="1.2" stroke-linecap="round"/>
        </svg>"""
    
    b64_logo = base64.b64encode(raw_svg).decode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{b64_logo}" style="width:100%;height:100%;">'


def render_welcome():
    logo_html = get_logo_html()

    st.markdown(f"""
    <div class="fade-in" style="
        text-align:center;padding:48px 24px 40px;
        max-width:600px;margin:0 auto;
    ">
        <div style="width:140px;height:140px;margin:0 auto 24px;">{logo_html}</div>
        <h1 style="font-size:36px;font-weight:700;color:#f5f5f7;
        letter-spacing:-0.04em;margin:0 0 8px;line-height:1.1;">
            RelocationDevs
        </h1>
        <p style="font-size:14px;color:#6e6e73;margin:0 0 4px;
        letter-spacing:0.02em;">by a Cambeiro</p>
        <p style="font-size:16px;color:#aeaeb2;margin:24px 0 0;line-height:1.6;">
            Descubre qué ciudad del mundo encaja mejor<br>
            con tu perfil profesional y estilo de vida.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1px;background:#2c2c2e;margin:0 0 40px;'></div>",
                unsafe_allow_html=True)

    try:
        countries = load_countries()
    except FileNotFoundError:
        st.error("No se encontró salaries.csv. Ejecuta primero el notebook 03_modeling.ipynb.")
        return

    st.markdown("""
    <p style="font-size:11px;font-weight:600;color:#6e6e73;letter-spacing:0.1em;
    text-transform:uppercase;margin-bottom:20px;">Tu perfil profesional</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    # País por defecto: España
    default_country_idx = countries.index("Spain") if "Spain" in countries else 0

    with col1:
        position = st.selectbox(
            "¿Cuál es tu posición?",
            list(POSITIONS.keys()),
            help="Selecciona la que mejor describe tu rol actual"
        )
        years_exp = st.slider("Años de experiencia", 0, 30, 3)

    with col2:
        education = st.selectbox(
            "Nivel educativo",
            ["Bachelor", "Master", "PhD", "Bootcamp"]
        )
        origin = st.selectbox(
            "País de origen",
            countries,
            index=default_country_idx,
        )

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("Analizar mi perfil →", type="primary", use_container_width=True):
            role, spec = POSITIONS[position]
            try:
                from src.model import predict
                estimated_salary = predict({
                    "city_name":        origin,
                    "role":             role,
                    "specialization":   spec,
                    "years_experience": years_exp,
                    "education_level":  education,
                })
            except Exception:
                estimated_salary = None

            st.session_state.profile = {
                "position":         position,
                "role":             role,
                "specialization":   spec,
                "years_experience": years_exp,
                "education_level":  education,
                "origin_country":   origin,
                "estimated_salary": estimated_salary,
            }
            st.session_state.profile_set = True
            st.rerun()

    st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:20px 0;">
        <a href="https://github.com/Udamian/RelocationDevs" target="_blank"
           style="font-size:12px;color:#3a3a3c;text-decoration:none;">
            github.com/Udamian/RelocationDevs
        </a>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_profile():
    render_sidebar_brand()
    p = st.session_state.profile

    st.sidebar.markdown(f"""
    <div style="padding:12px 16px;margin-bottom:4px;">
        <p style="font-size:11px;color:#6e6e73;letter-spacing:0.08em;
        text-transform:uppercase;margin:0 0 10px;">Tu perfil</p>
        <p style="font-size:13px;color:#f5f5f7;margin:0 0 4px;">{p['position']}</p>
        <p style="font-size:12px;color:#aeaeb2;margin:0 0 4px;">
            {p['years_experience']} años · {p['education_level']}
        </p>
        <p style="font-size:12px;color:#6e6e73;margin:0;">{p['origin_country']}</p>
    </div>
    """, unsafe_allow_html=True)

    if p.get("estimated_salary"):
        st.sidebar.markdown(f"""
        <div style="margin:0 16px 12px;padding:12px 14px;background:#2c2c2e;
        border-radius:10px;border:1px solid #3a3a3c;">
            <p style="font-size:11px;color:#6e6e73;margin:0 0 4px;
            text-transform:uppercase;letter-spacing:0.06em;">Salario estimado</p>
            <p style="font-size:20px;font-weight:600;color:#f5f5f7;margin:0;
            letter-spacing:-0.02em;">€{p['estimated_salary']:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)

    st.sidebar.markdown(
        "<div style='height:1px;background:#2c2c2e;margin:4px 0 12px;'></div>",
        unsafe_allow_html=True
    )

    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "Buscador de ciudad ideal"

    if "redirect_to" in st.session_state and st.session_state.redirect_to:
        st.session_state.nav_page = st.session_state.redirect_to
        st.session_state.redirect_to = None

    page = st.sidebar.radio(
        "Navegación",
        ["Buscador de ciudad ideal", "Explorador", "Comparador", "Mapa", "Informe PDF"],
        label_visibility="collapsed",
        key="nav_page",
    )

    st.sidebar.markdown(
        "<div style='height:1px;background:#2c2c2e;margin:12px 0 8px;'></div>",
        unsafe_allow_html=True
    )

    if st.sidebar.button("Cambiar perfil", use_container_width=True):
        st.session_state.profile_set = False
        st.session_state.profile = {}
        st.rerun()

    st.sidebar.markdown("""
    <div style="padding:12px 16px 8px;">
        <a href="https://github.com/Udamian/RelocationDevs" target="_blank"
           style="font-size:11px;color:#3a3a3c;text-decoration:none;">
            github.com/Udamian/RelocationDevs
        </a>
    </div>
    """, unsafe_allow_html=True)

    return page


# ── Routing ───────────────────────────────────────────────────
if not st.session_state.get("profile_set", False):
    render_welcome()
else:
    page = render_sidebar_profile()
    render_footer()

    if page == "Explorador":
        from app.city_explorer import render; render()
    elif page == "Comparador":
        from app.comparison import render; render()
    elif page == "Mapa":
        from app.city_map import render; render()
    elif page == "Buscador de ciudad ideal":
        from app.city_finder import render; render()
    elif page == "Informe PDF":
        from app.pdf_generator import render
        render()