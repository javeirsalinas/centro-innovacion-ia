import streamlit as st
import google.generativeai as genai

# 1. Configuración de la interfaz
st.set_page_config(page_title="Centro de Innovación AI", layout="wide")
st.title("🚀 AgentLake: Centro de Innovación")
st.subheader("Proyecto: COLPA DE COPA (MULTISERVICIOS DAMAR S.A.C)")

# 2. Configuración de la IA desde Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # Formulario de entrada
    with st.form("form_mentoria"):
        nombre = st.text_input("Nombre del Emprendedor")
        descripcion = st.text_area("Cuéntanos de tu proyecto (Ej: Licores de Jergón Sacha, Cerveza Artesanal)")
        enviar = st.form_submit_button("Iniciar Auditoría con IA")

    if enviar:
        if descripcion:
            with st.spinner("El Panel de Expertos está analizando tu propuesta..."):
                try:
                    # Configuración del modelo estable
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"""
                    Actúa como mentor senior experto en agronegocios y licores.
                    Emprendedor: {nombre}
                    Proyecto: COLPA DE COPA
                    Descripción: {descripcion}
                    
                    Dame 3 consejos estratégicos para este negocio en la selva peruana 
                    y una puntuación de viabilidad del 1 al 10.
                    """
                    
                    # Llamada a la IA
                    response = model.generate_content(prompt)
                    
                    st.success(f"¡Análisis completado para {nombre}!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error técnico con la IA: {str(e)}")
        else:
            st.warning("Por favor, describe tu proyecto para poder ayudarte.")
else:
    st.error("⚠️ Configuración incompleta: No se encontró la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
