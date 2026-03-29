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
            with st.spinner("Accediendo al servidor de Google AI..."):
                # URL DEFINITIVA: Usamos v1beta pero con el modelo específico 'gemini-1.5-flash-latest'
                # Esta es la ruta que Google garantiza para llamadas directas
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Actúa como mentor experto en agronegocios. Analiza el proyecto {descripcion} de {nombre} (COLPA DE COPA) en la selva peruana."}]
                    }]
                }
                
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(payload))
                    res_json = response.json()
                    
                    if response.status_code == 200:
                        texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.success("¡Análisis Exitoso!")
                        st.markdown(texto_ia)
                    else:
                        # Si falla el flash, intentamos el gemini-pro original
                        url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
                        response_alt = requests.post(url_alt, headers=headers, data=json.dumps(payload))
                        res_alt = response_alt.json()
                        
                        if response_alt.status_code == 200:
                            st.success("¡Análisis Exitoso (Modo Pro)!")
                            st.markdown(res_alt['candidates'][0]['content']['parts'][0]['text'])
                        else:
                            st.error(f"Error de Google: {res_alt['error']['message']}")
                except Exception as e:
                    st.error(f"Error de conexión: {str(e)}")
        else:
            st.warning("Escribe la descripción de tu proyecto.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
