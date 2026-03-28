import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# Configuración de página
st.set_page_config(page_title="Centro de Innovación AI", layout="wide")
st.title("🚀 AgentLake: Centro de Innovación")
st.subheader("Proyecto: COLPA DE COPA (MULTISERVICIOS DAMAR S.A.C)")

# 1. Obtener la API KEY
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Configuración de la IA
    genai.configure(api_key=api_key)
    
    # Formulario
    with st.form("mentoria_form"):
        nombre = st.text_input("Nombre del Emprendedor")
        descripcion = st.text_area("Descripción (Ej: Licores de Jergón Sacha, Cerveza Artesanal)")
        boton = st.form_submit_button("Consultar Panel de Expertos")

    if boton:
        if descripcion:
            with st.spinner("Conectando con el servidor central..."):
                try:
                    # USAMOS EL MODELO MÁS MODERNO PERO FORZANDO LA VERSIÓN 'v1'
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"Actúa como mentor experto en agronegocios. Analiza el proyecto {descripcion} de {nombre}."
                    
                    # LA LÍNEA MÁGICA: Forzamos la versión v1 (estable)
                    response = model.generate_content(
                        prompt,
                        request_options=RequestOptions(api_version='v1')
                    )
                    
                    st.success("¡Análisis Exitoso!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error de conexión: {str(e)}")
        else:
            st.warning("Escribe la descripción de tu proyecto.")
else:
    st.error("⚠️ Falta la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
