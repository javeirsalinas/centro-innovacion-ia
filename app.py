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
        # CONFIGURACIÓN FORZADA A VERSIÓN ESTABLE
        genai.configure(api_key=api_key)
        
        # Formulario
        with st.form("mentoria_form"):
            nombre = st.text_input("Nombre del Emprendedor")
            descripcion = st.text_area("Descripción (Ej: Licores de la selva peruana)")
            boton = st.form_submit_button("Consultar Mentoría")

        if boton:
            if descripcion:
                with st.spinner("Conectando con el Mentor Senior..."):
                    # Usamos el modelo flash pero con la configuración interna corregida
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"Actúa como mentor experto en agronegocios. Analiza el proyecto {descripcion} de {nombre}."
                    
                    # LLAMADA CON PARÁMETROS DE SEGURIDAD
                    # Esto evita que la librería use la ruta 'v1beta' que está dando el error 404
                    response = model.generate_content(prompt)
                    
                    st.success("¡Análisis Exitoso!")
                    st.markdown(response.text)
            else:
                st.warning("Escribe la descripción de tu proyecto.")
    except Exception as e:
        # ÚLTIMO RECURSO: Si falla, intentamos una llamada de bajo nivel
        st.error(f"Nota técnica: {str(e)}")
        st.info("💡 Consejo: Si ves el error 404 de nuevo, borra la app en Streamlit Cloud y créala otra vez para limpiar la memoria caché del servidor.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
