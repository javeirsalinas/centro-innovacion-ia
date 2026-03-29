import streamlit as st
import google.generativeai as genai

# Configuración básica
st.set_page_config(page_title="Centro de Innovación AI", page_icon="🚀")
st.title("🚀 AgentLake: Centro de Innovación")
st.write("Proyecto: **COLPA DE COPA**")

# 1. Conexión con la llave secreta
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # 2. Formulario de entrada
    nombre = st.text_input("Tu Nombre")
    descripcion = st.text_area("Descripción de tu innovación (Ej: Licores de la selva)")

    if st.button("Obtener Mentoría"):
        if descripcion:
            try:
                # Intentamos con el modelo Pro (el más compatible)
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(f"Soy mentor de negocios. Analiza: {descripcion}")
                
                st.success(f"¡Listo, {nombre}!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Nota técnica: {str(e)}")
        else:
            st.warning("Por favor, cuéntanos sobre tu proyecto.")
else:
    st.error("Falta configurar la GOOGLE_API_KEY en los Secrets.")
