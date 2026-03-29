import streamlit as st
import requests
import json

# Configuración de página
st.set_page_config(page_title="Centro de Innovación AI", layout="wide")
st.title("🚀 AgentLake: Centro de Innovación")
st.subheader("Proyecto: COLPA DE COPA (MULTISERVICIOS DAMAR S.A.C)")

# 1. Obtener la API KEY de los Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Formulario
    with st.form("mentoria_form"):
        nombre = st.text_input("Nombre del Emprendedor")
        descripcion = st.text_area("Descripción (Ej: Licores de la selva peruana)")
        boton = st.form_submit_button("Consultar Mentoría")

    if boton:
        if descripcion:
            with st.spinner("Conectando directamente con Google AI..."):
                # URL DIRECTA A LA VERSIÓN ESTABLE (v1)
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                data = {
                    "contents": [{
                        "parts": [{"text": f"Actúa como mentor experto en agronegocios para {nombre}. Analiza el proyecto {descripcion} de COLPA DE COPA en la selva peruana. Dame 3 consejos estratégicos."}]
                    }]
                }
                
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(data))
                    res_json = response.json()
                    
                    if response.status_code == 200:
                        # Extraer la respuesta de la IA
                        texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.success("¡Análisis Exitoso!")
                        st.markdown(texto_ia)
                    else:
                        st.error(f"Error de Google: {res_json['error']['message']}")
                except Exception as e:
                    st.error(f"Error de conexión: {str(e)}")
        else:
            st.warning("Escribe la descripción de tu proyecto.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
