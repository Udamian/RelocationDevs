import streamlit as st
from src.model import predict
from src.indicators import estimated_net_salary, estimated_purchasing_power

def render():
    st.title("Salary Estimator")
    st.caption("Estima tu salario esperado segun tu perfil")
    col1, col2 = st.columns(2)
    with col1:
        role        = st.selectbox("Rol", ["Software Engineer","Data Scientist","DevOps Engineer","Product Manager","Data Engineer","ML Engineer"])
        spec        = st.selectbox("Especializacion", ["Backend","Frontend","Full Stack","Cloud","AI/ML","Mobile"])
        years_exp   = st.slider("Anos de experiencia", 0, 20, 3)
    with col2:
        city        = st.text_input("Ciudad destino", placeholder="Ej: Berlin")
        education   = st.selectbox("Nivel educativo", ["Bachelor","Master","PhD","Bootcamp"])
        tax_rate    = st.slider("Tasa impositiva (%)", 0, 60, 30)
    if st.button("Estimar salario", type="primary"):
        if not city:
            st.warning("Introduce una ciudad destino.")
            return
        try:
            gross = predict({"role": role, "specialization": spec, "years_experience": years_exp,
                             "city_name": city, "education_level": education})
            net   = estimated_net_salary(gross, tax_rate)
            pwr   = estimated_purchasing_power(net, 100)
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("Salario bruto", f"EUR {gross:,.0f}")
            c2.metric("Salario neto",  f"EUR {net:,.0f}")
            c3.metric("Poder adquisitivo", f"{pwr:.1f}")
        except FileNotFoundError:
            st.error("Modelo no entrenado. Ejecuta primero el notebook 03_modeling.ipynb.")
        except Exception as e:
            st.error(f"Error: {e}")
