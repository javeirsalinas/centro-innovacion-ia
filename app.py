import streamlit as st
import google.generativeai as genai
import os

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Centro de Innovación AI", layout="wide")
st.title("🚀 AgentLake: Centro de Innovación")
st.subheader("Proyecto: COLPA DE COPA (MULTISERVICIOS DAMAR S.A.C)")

# 1. OBTENER LA LLAVE DE LOS SECRETS
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # CONFIGURACIÓN FORZADA
    genai.configure(api_key=api_key)
    
    # FORMULARIO
    with st.form("mentoria_form"):
        nombre = st.text_input("Nombre del Emprendedor")
        descripcion = st.text_area("Descripción (Ej: Licores de Jergón Sacha, Cerveza Artesanal)")
        boton = st.form_submit_button("Consultar Panel de Expertos")

    if boton:
        if descripcion:
            with st.spinner("Analizando propuesta..."):
                try:
                    # USAMOS GEMINI-PRO QUE ES EL MÁS ESTABLE PARA ESTA LIBRERÍA
                    model = genai.GenerativeModel('gemini-pro')
                    
                    prompt = f"Actúa como mentor experto en la selva peruana. Analiza el proyecto {descripcion} de {nombre}."
                    
                    # LLAMADA DIRECTA
                    response = model.generate_content(prompt)
                    
                    st.success("¡Análisis Exitoso!")
                    st.markdown(response.text)
                except Exception as e:
                    # SI FALLA EL PRO, INTENTAMOS EL 1.0-PRO (EL ORIGINAL)
                    try:
                        model_fallback = genai.GenerativeModel('gemini-1.0-pro')
                        response = model_fallback.generate_content(prompt)
                        st.success("Análisis Exitoso (Legacy Mode)")
                        st.markdown(response.text)
                    except Exception as e2:
                        st.error(f"Error de conexión con Google: {str(e2)}")
        else:
            st.warning("Escribe la descripción de tu proyecto.")
else:
    st.error("⚠️ Error: Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
