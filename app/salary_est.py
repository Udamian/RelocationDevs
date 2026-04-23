"""
salary_est.py
Usa el perfil guardado en session_state.
Permite ajustar la tasa impositiva manualmente.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from src.model import predict
from src.indicators import estimated_net_salary, estimated_purchasing_power
from app.styles import page_header

PROCESSED = Path(__file__).parent.parent / "data" / "processed"


def render():
  page_header("Salary Estimator", "Estimación salarial basada en tu perfil")

    p = st.session_state.get("profile", {})

    if not p:
        st.warning("No hay perfil definido. Vuelve a la pantalla de inicio.")
        return

    # Mostrar perfil activo
    st.info(
        f"**{p['role']}** · {p['specialization']} · "
        f"{p['years_experience']} años · {p['education_level']} · "
        f"desde {p['origin_country']}"
    )

    # Solo pedimos la tasa impositiva — lo único que varía por destino
    st.divider()
    st.subheader("Ajuste por país de destino")

    col1, col2 = st.columns(2)
    with col1:
        tax_rate = st.slider("Tasa impositiva del país de destino (%)", 0, 60, 30)
    with col2:
        st.caption("Ajusta la tasa según el país de destino que estás evaluando.")
        st.caption("Puedes encontrar las tasas en la documentación del proyecto (OECD).")

    st.divider()

    if st.button("Calcular", type="primary", use_container_width=True):
        try:
            gross    = p.get("estimated_salary") or predict({
                "city_name":        p["origin_country"],
                "role":             p["role"],
                "specialization":   p["specialization"],
                "years_experience": p["years_experience"],
                "education_level":  p["education_level"],
            })
            net      = estimated_net_salary(gross, tax_rate)
            pwr      = estimated_purchasing_power(net, 100)
            savings  = net * 0.30

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Salario bruto", f"€{gross:,.0f}")
            c2.metric("Salario neto", f"€{net:,.0f}")
            c3.metric("Poder adquisitivo", f"{pwr:.1f}")
            c4.metric("Ahorro anual est.", f"€{savings:,.0f}")

            st.divider()
            st.write(f"**Impuestos retenidos:** {tax_rate}% → €{gross - net:,.0f}/año")

            n = len(pd.read_csv(PROCESSED / "salaries.csv"))
            st.info(
                f"Estimación basada en {n:,} respuestas del Stack Overflow Developer Survey 2023. "
                f"Margen de error estimado: ±€29.000."
            )

        except Exception as e:
            st.error(f"Error al calcular: {e}")