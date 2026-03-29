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
        # CONFIGURACIÓN
        genai.configure(api_key=api_key)
        
        # Formulario
        with st.form("mentoria_form"):
            nombre = st.text_input("Nombre del Emprendedor")
            descripcion = st.text_area("Descripción (Ej: Licores de la selva peruana)")
            boton = st.form_submit_button("Consultar Mentoría")

        if boton:
            if descripcion:
                with st.spinner("Analizando propuesta..."):
                    # ESTA ES LA CLAVE: Usamos el nombre técnico completo
                    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-latest')
                    
                    prompt = f"Actúa como mentor experto en agronegocios. Analiza el proyecto {descripcion} de {nombre}."
                    
                    # Llamada directa
                    response = model.generate_content(prompt)
                    
                    st.success("¡Análisis Exitoso!")
                    st.markdown(response.text)
            else:
                st.warning("Escribe la descripción de tu proyecto.")
    except Exception as e:
        # Si falla el anterior, intentamos el modelo pro con el mismo formato
        try:
            model_alt = genai.GenerativeModel(model_name='models/gemini-1.0-pro-latest')
            response_alt = model_alt.generate_content(prompt)
            st.success("¡Análisis Exitoso (Modo Pro)!")
            st.markdown(response_alt.text)
        except Exception as e2:
            st.error(f"Error técnico final: {str(e2)}")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
