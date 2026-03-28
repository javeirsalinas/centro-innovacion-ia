import streamlit as st
import google.generativeai as genai

# Configuración de la interfaz
st.set_page_config(page_title="Centro de Innovación AI", layout="wide")
st.title("🚀 AgentLake: Centro de Innovación")
st.subheader("Proyecto: COLPA DE COPA (MULTISERVICIOS DAMAR S.A.C)")

# 1. Obtener la API KEY de los Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # CONFIGURACIÓN ESTABLE
        genai.configure(api_key=api_key)
        
        # Formulario
        with st.form("mentoria_form"):
            nombre = st.text_input("Nombre del Emprendedor")
            descripcion = st.text_area("Descripción (Ej: Licores de Jergón Sacha, Cerveza Artesanal)")
            boton = st.form_submit_button("Consultar Panel de Expertos")

        if boton:
            if descripcion:
                with st.spinner("Analizando propuesta con el modelo Pro..."):
                    # USAMOS GEMINI-PRO PARA MÁXIMA COMPATIBILIDAD
                    model = genai.GenerativeModel('gemini-pro')
                    
                    prompt = f"Actúa como mentor experto en agronegocios para {nombre}. Analiza: {descripcion}."
                    
                    # Llamada limpia
                    response = model.generate_content(prompt)
                    
                    st.success("¡Análisis Exitoso!")
                    st.markdown(response.text)
            else:
                st.warning("Por favor, describe tu proyecto.")
    except Exception as e:
        st.error(f"Nota técnica: {str(e)}")
else:
    st.error("⚠️ Error: Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
