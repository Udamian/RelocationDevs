"""
salary_est.py
Módulo: estimador salarial interactivo.
Carga países y roles reales desde salaries.csv.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from src.model import predict
from src.indicators import estimated_net_salary, estimated_purchasing_power

PROCESSED = Path(__file__).parent.parent / "data" / "processed"


@st.cache_data
def load_options():
    """Carga países, roles y especializaciones reales del dataset."""
    df = pd.read_csv(PROCESSED / "salaries.csv")
    countries     = sorted(df["city_name"].dropna().unique().tolist())
    roles         = sorted(df["role"].dropna().unique().tolist())
    specs         = sorted(df["specialization"].dropna().unique().tolist())
    return countries, roles, specs


def render():
    st.title("Salary Estimator")
    st.caption("Estima tu salario esperado según tu perfil profesional")

    # Cargar opciones reales
    try:
        countries, roles, specs = load_options()
    except FileNotFoundError:
        st.error("No se encontró salaries.csv. Ejecuta primero el notebook 03_modeling.ipynb.")
        return

    # Formulario
    col1, col2 = st.columns(2)

    with col1:
        country    = st.selectbox("País de destino", countries)
        role       = st.selectbox("Rol", roles)
        spec       = st.selectbox("Especialización", specs)

    with col2:
        years_exp  = st.slider("Años de experiencia", 0, 30, 3)
        education  = st.selectbox("Nivel educativo", ["Bachelor", "Master", "PhD", "Bootcamp"])
        tax_rate   = st.slider("Tasa impositiva estimada (%)", 0, 60, 30)

    st.divider()

    if st.button("Estimar salario", type="primary", use_container_width=True):
        try:
            profile = {
                "city_name":        country,
                "role":             role,
                "specialization":   spec,
                "years_experience": years_exp,
                "education_level":  education,
            }

            gross = predict(profile)
            net   = estimated_net_salary(gross, tax_rate)
            pwr   = estimated_purchasing_power(net, 100)
            savings = net * 0.30  # ahorro estimado 30%

            # Métricas principales
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Salario bruto", f"€{gross:,.0f}")
            c2.metric("Salario neto", f"€{net:,.0f}")
            c3.metric("Poder adquisitivo", f"{pwr:.1f}")
            c4.metric("Ahorro anual est.", f"€{savings:,.0f}")

            # Desglose
            st.subheader("Desglose")
            st.write(f"**País:** {country} · **Rol:** {role} · **Especialización:** {spec}")
            st.write(f"**Experiencia:** {years_exp} años · **Educación:** {education}")
            st.write(f"**Impuestos aplicados:** {tax_rate}% → €{gross - net:,.0f} retenidos")

            # Aviso de precisión
            st.info(
                f"Estimación basada en {len(pd.read_csv(PROCESSED / 'salaries.csv')):,} "
                f"respuestas del Stack Overflow Developer Survey 2023. "
                f"Margen de error estimado: ±€29.000 — los salarios varían significativamente "
                f"según empresa, ciudad exacta y habilidades específicas."
            )

        except FileNotFoundError:
            st.error("Modelo no entrenado. Ejecuta primero el notebook 03_modeling.ipynb.")
        except Exception as e:
            st.error(f"Error al predecir: {e}")