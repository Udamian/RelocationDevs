"""
main.py — Punto de entrada Streamlit.
Pantalla de bienvenida con perfil de usuario.
El perfil persiste toda la sesión y contextualiza todas las vistas.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

PROCESSED = Path(__file__).parent.parent / "data" / "processed"

st.set_page_config(
    page_title="RelocationDevs",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_salary_options():
    df = pd.read_csv(PROCESSED / "salaries.csv")
    countries = sorted(df["city_name"].dropna().unique().tolist())
    roles     = sorted(df["role"].dropna().unique().tolist())
    specs     = sorted(df["specialization"].dropna().unique().tolist())
    return countries, roles, specs


def render_welcome():
    """Pantalla de bienvenida — recoge el perfil del usuario."""
    st.title("🌍 RelocationDevs")
    st.subheader("Tu herramienta de decisión para reubicación tech")
    st.write("Cuéntanos tu perfil y personalizaremos todas las vistas en base a tu situación real.")
    st.divider()

    try:
        countries, roles, specs = load_salary_options()
    except FileNotFoundError:
        st.error("No se encontró salaries.csv. Ejecuta primero el notebook 03_modeling.ipynb.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tu perfil profesional")
        role       = st.selectbox("¿Cuál es tu rol?", roles)
        spec       = st.selectbox("¿Cuál es tu especialización?", specs)
        years_exp  = st.slider("Años de experiencia", 0, 30, 3)
        education  = st.selectbox("Nivel educativo", ["Bachelor", "Master", "PhD", "Bootcamp"])

    with col2:
        st.subheader("Tu situación actual")
        origin     = st.selectbox("¿Desde qué país emigras?", countries)
        st.caption("Usamos tu país de origen para calcular la tasa impositiva de destino automáticamente.")
        st.write("")
        st.info(
            "Basándonos en tu perfil estimaremos tu salario esperado en cada ciudad "
            "y filtraremos las ciudades donde tendrías mejor calidad de vida."
        )

    st.divider()

    if st.button("Ver mi análisis de reubicación →", type="primary", use_container_width=True):
        # Calcular salario estimado para el perfil
        try:
            from src.model import predict
            profile = {
                "city_name":        origin,
                "role":             role,
                "specialization":   spec,
                "years_experience": years_exp,
                "education_level":  education,
            }
            estimated_salary = predict(profile)
        except Exception:
            estimated_salary = None

        # Guardar perfil en session_state
        st.session_state.profile = {
            "role":             role,
            "specialization":   spec,
            "years_experience": years_exp,
            "education_level":  education,
            "origin_country":   origin,
            "estimated_salary": estimated_salary,
        }
        st.session_state.profile_set = True
        st.rerun()


def render_sidebar_profile():
    """Sidebar con resumen del perfil activo y botón para resetearlo."""
    p = st.session_state.profile

    st.sidebar.title("🌍 RelocationDevs")
    st.sidebar.divider()

    st.sidebar.subheader("Tu perfil")
    st.sidebar.write(f"**Rol:** {p['role']}")
    st.sidebar.write(f"**Especialización:** {p['specialization']}")
    st.sidebar.write(f"**Experiencia:** {p['years_experience']} años")
    st.sidebar.write(f"**Educación:** {p['education_level']}")
    st.sidebar.write(f"**País origen:** {p['origin_country']}")

    if p.get("estimated_salary"):
        st.sidebar.divider()
        st.sidebar.metric(
            "Salario estimado",
            f"€{p['estimated_salary']:,.0f}",
            help="Basado en tu perfil y país de origen"
        )

    st.sidebar.divider()
    if st.sidebar.button("Cambiar perfil", use_container_width=True):
        st.session_state.profile_set = False
        st.session_state.profile = {}
        st.rerun()

    st.sidebar.divider()
    return st.sidebar.radio(
        "Navegación",
        ["City Explorer", "City Comparison", "Mapa de ciudades", "Salary Estimator"],
    )


# ── Routing principal ─────────────────────────────────────────
if not st.session_state.get("profile_set", False):
    render_welcome()
else:
    page = render_sidebar_profile()

    if page == "City Explorer":
        from app.city_explorer import render; render()
    elif page == "City Comparison":
        from app.comparison import render; render()
    elif page == "Mapa de ciudades":
        from app.city_map import render; render()
    elif page == "Salary Estimator":
        from app.salary_est import render; render()