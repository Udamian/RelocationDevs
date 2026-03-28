"""
main.py â€” Punto de entrada Streamlit.
Ejecutar: streamlit run app/main.py
"""

import streamlit as st

st.set_page_config(
    page_title="RelocationDevs",
    page_icon="ðŸŒ",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("RelocationDevs")
st.sidebar.caption("Herramienta de decision para reubicacion tech")

page = st.sidebar.radio(
    "Navegación",
    ["City Explorer", "City Comparison", "Mapa de ciudades", "Salary Estimator"],
)

if page == "City Explorer":
    from app.city_explorer import render; render()
elif page == "City Comparison":
    from app.comparison import render; render()
elif page == "Mapa de ciudades":
    from app.city_map import render; render()
elif page == "Salary Estimator":
    from app.salary_est import render; render()