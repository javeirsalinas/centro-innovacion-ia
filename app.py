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
        # CONFIGURACIÓN DE SEGURIDAD
        genai.configure(api_key=api_key)
        
        # Formulario
        with st.form("mentoria_form"):
            nombre = st.text_input("Nombre del Emprendedor")
            descripcion = st.text_area("Descripción (Ej: Licores de Jergón Sacha, Cerveza Artesanal)")
            boton = st.form_submit_button("Consultar Panel de Expertos")

        if boton:
            if descripcion:
                with st.spinner("Conectando con el Mentor Senior..."):
                    # LA SOLUCIÓN: Usamos el nombre del modelo sin prefijos raros
                    # La librería se encargará de encontrar la ruta correcta
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"Actúa como mentor experto en agronegocios. Proyecto: {descripcion}. Emprendedor: {nombre}."
                    
                    # Llamada directa
                    response = model.generate_content(prompt)
                    
                    st.success("¡Análisis Exitoso!")
                    st.markdown(response.text)
            else:
                st.warning("Por favor, describe tu proyecto.")
    except Exception as e:
        st.error(f"Error de sistema: {str(e)}")
        st.info("Sugerencia: Revisa que tu API Key sea válida en Google AI Studio.")
else:
    st.error("⚠️ Falta la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
