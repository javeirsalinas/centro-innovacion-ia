import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# 1. Configuración de la interfaz
st.set_page_config(page_title="Centro de Innovación AI", layout="wide")
st.title("🚀 AgentLake: Centro de Innovación")
st.subheader("Proyecto: COLPA DE COPA (MULTISERVICIOS DAMAR S.A.C)")

# 2. Configuración de Seguridad y API
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # Forzamos la configuración a la versión estable v1
        genai.configure(api_key=api_key)
        
        # Formulario de entrada
        with st.form("form_mentoria"):
            nombre = st.text_input("Nombre del Emprendedor")
            descripcion = st.text_area("Cuéntanos de tu proyecto (Ej: Licores de Jergón Sacha, Cerveza Artesanal)")
            enviar = st.form_submit_button("Iniciar Auditoría con IA")

        if enviar:
            if descripcion:
                with st.spinner("Conectando con el Panel de Expertos..."):
                    try:
                        # Intentamos con el modelo más rápido y moderno (Flash)
                        # Usamos 'models/' para asegurar la ruta correcta
                        model = genai.GenerativeModel('models/gemini-1.5-flash')
                        
                        prompt = f"""
                        Actúa como mentor senior experto en agronegocios y licores.
                        Emprendedor: {nombre}
                        Proyecto: COLPA DE COPA
                        Descripción: {descripcion}
                        
                        Dame 3 consejos estratégicos para este negocio en la selva peruana 
                        y una puntuación de viabilidad del 1 al 10.
                        """
                        
                        # Forzamos la petición a través de la API estable v1
                        response = model.generate_content(
                            prompt,
                            request_options=RequestOptions(api_version='v1')
                        )
                        
                        st.success(f"¡Análisis completado para {nombre}!")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        # Plan B: Si Flash falla, intentamos el modelo Pro
                        st.info("Ajustando frecuencia de conexión...")
                        model_alt = genai.GenerativeModel('models/gemini-pro')
                        response_alt = model_alt.generate_content(
                            prompt,
                            request_options=RequestOptions(api_version='v1')
                        )
                        st.success("Análisis completado (Modo Estabilidad)")
                        st.markdown(response_alt.text)
            else:
                st.warning("Por favor, describe tu proyecto para poder ayudarte.")
                
    except Exception as e_final:
        st.error(f"Error técnico: {str(e_final)}")
        st.info("Sugerencia: Verifica que tu API Key en AI Studio esté activa y sin restricciones.")
else:
    st.error("⚠️ Configuración incompleta: No se encontró la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
