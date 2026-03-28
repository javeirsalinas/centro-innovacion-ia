import streamlit as st
import google.generativeai as genai

# Configuración de página
st.set_page_config(page_title="Centro de Innovación AI", layout="wide")
st.title("🚀 AgentLake: Centro de Innovación")
st.subheader("Proyecto: COLPA DE COPA (MULTISERVICIOS DAMAR S.A.C)")

# 1. Obtener la API KEY de los Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # CONFIGURACIÓN DIRECTA
    # Al no especificar versión, la librería buscará la más estable por defecto
    genai.configure(api_key=api_key)
    
    # Formulario
    with st.form("mentoria_form"):
        nombre = st.text_input("Nombre del Emprendedor")
        descripcion = st.text_area("Descripción (Ej: Licores de Jergón Sacha, Cerveza Artesanal)")
        boton = st.form_submit_button("Consultar Panel de Expertos")

    if boton:
        if descripcion:
            with st.spinner("Conectando con el Mentor Senior..."):
                try:
                    # Probamos con el nombre de modelo que Google tiene como estándar global
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"Actúa como mentor experto en agronegocios y licores de la selva. Analiza el proyecto {descripcion} de {nombre}. Dame 3 consejos estratégicos."
                    
                    # Llamada limpia sin argumentos extra que causen conflicto
                    response = model.generate_content(prompt)
                    
                    st.success("¡Análisis Exitoso!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Nota técnica: {str(e)}")
                    st.info("Intentando conexión alternativa...")
                    # Plan B automático
                    try:
                        model_pro = genai.GenerativeModel('gemini-pro')
                        response_pro = model_pro.generate_content(prompt)
                        st.success("¡Análisis Exitoso (Modo Pro)!")
                        st.markdown(response_pro.text)
                    except Exception as e2:
                        st.error("No se pudo establecer la conexión. Verifica tu API Key en Google AI Studio.")
        else:
            st.warning("Por favor, escribe la descripción de tu proyecto.")
else:
    st.error("⚠️ Falta la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
