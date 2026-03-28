import streamlit as st
from google import genai

# Configuración básica
st.set_page_config(page_title="Centro de Innovación AI", layout="wide")
st.title("🚀 AgentLake: Centro de Innovación")

# 1. Captura de datos del proyecto COLPA DE COPA [cite: 7, 9]
with st.container():
    nombre = st.text_input("Nombre del Emprendedor")
    proyecto = st.text_input("Proyecto", value="COLPA DE COPA")
    descripcion = st.text_area("Descripción", placeholder="Ej: Producción de tragos de la selva y cervezas artesanales.")

    if st.button("Iniciar Mentoría"):
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if api_key and descripcion:
            try:
                # 2. Nueva forma de conectar con la IA
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="models/gemini-pro",
                    contents=f"Como mentor senior, analiza este proyecto de la selva peruana: {descripcion}"
                )
                st.success(f"¡Análisis listo para {nombre}!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error técnico: {str(e)}")
        else:
            st.warning("Asegúrate de tener la API Key en 'Secrets' y llenar la descripción.")
