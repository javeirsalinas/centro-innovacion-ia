import streamlit as st
import google.generativeai as genai

# Configuración de la interfaz
st.set_page_config(page_title="Centro de Innovación AI", layout="wide")
st.title("🚀 AgentLake: Centro de Innovación")
st.subheader("Proyecto: COLPA DE COPA (MULTISERVICIOS DAMAR S.A.C)")

# Obtener la API KEY de los Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        with st.form("mentoria_form"):
            nombre = st.text_input("Nombre del Emprendedor")
            descripcion = st.text_area("Descripción (Ej: Licores de Jergón Sacha, Cerveza Artesanal)")
            boton = st.form_submit_button("Consultar Panel de Expertos")

        if boton:
            if descripcion:
                with st.spinner("Analizando propuesta..."):
                    # Usamos el modelo Pro por su alta compatibilidad
                    model = genai.GenerativeModel('gemini-pro')
                    prompt = f"Actúa como mentor experto en agronegocios. Analiza el proyecto {descripcion} de {nombre}."
                    response = model.generate_content(prompt)
                    
                    st.success("¡Análisis Exitoso!")
                    st.markdown(response.text)
            else:
                st.warning("Por favor, escribe la descripción de tu proyecto.")
    except Exception as e:
        st.error(f"Nota técnica: {str(e)}")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")
