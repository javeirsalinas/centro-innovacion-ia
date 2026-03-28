import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Centro de Innovación AI", layout="wide")
st.title("🚀 AgentLake: Centro de Innovación")

# 1. Configuración Segura
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # 2. Formulario para COLPA DE COPA
    nombre = st.text_input("Tu Nombre")
    descripcion = st.text_area("Cuéntanos de tu proyecto (Ej: Licores de Jergón Sacha)")

    if st.button("Iniciar Mentoría"):
        if descripcion:
            try:
                # Intentamos con el modelo más estable y común
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Actúa como mentor experto. Proyecto: {descripcion}. Dame 3 consejos."
                
                response = model.generate_content(prompt)
                
                st.success(f"¡Análisis listo, {nombre}!")
                st.write(response.text)
            except Exception as e:
                # Si falla el 1.5-flash, intentamos el pro automáticamente
                try:
                    model_alt = genai.GenerativeModel('gemini-pro')
                    response = model_alt.generate_content(prompt)
                    st.success("Análisis completado (Modelo Pro)")
                    st.write(response.text)
                except Exception as e2:
                    st.error(f"Error técnico final: {str(e2)}")
        else:
            st.warning("Escribe la descripción de tu proyecto.")
else:
    st.error("No se encontró la GOOGLE_API_KEY en los Secrets de Streamlit.")
