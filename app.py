import streamlit as st
import google.generativeai as genai

# Configuración de página
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
            descripcion = st.text_area("Descripción (Ej: Licores de la selva peruana)")
            boton = st.form_submit_button("Consultar Mentoría")

        if boton:
            if descripcion:
                with st.spinner("Conectando con el Mentor Senior..."):
                    # USAMOS EL MODELO MÁS MODERNO Y ESTABLE
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"Actúa como mentor experto en agronegocios. Analiza el proyecto {descripcion} de {nombre} (COLPA DE COPA) en la selva peruana y da 3 consejos estratégicos."
                    
                    # Llamada limpia
                    response = model.generate_content(prompt)
                    
                    st.success("¡Análisis Exitoso!")
                    st.markdown(response.text)
            else:
                st.warning("Por favor, escribe la descripción de tu proyecto.")
    except Exception as e:
        # Si sale el error 404, mostramos una guía clara
        st.error(f"Nota de Google: {str(e)}")
        if "404" in str(e):
            st.info("💡 **Tip Técnico:** Tu API Key podría estar restringida a una región o versión. Intenta crear una NUEVA API Key en Google AI Studio.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
