import streamlit as st
import requests
import json

# Configuración de interfaz
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
            with st.spinner("Estableciendo conexión segura con Google AI..."):
                # URL CON EL MODELO ESPECÍFICO DE ALTA COMPATIBILIDAD (Gemini 1.5 Flash - Versión 002)
                # Esta ruta es la más estable para regiones fuera de EE.UU.
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-002:generateContent?key={api_key}"
                
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
                        # Si falla el anterior, intentamos con el modelo Pro 002
                        url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-002:generateContent?key={api_key}"
                        response_alt = requests.post(url_alt, headers=headers, data=json.dumps(payload))
                        
                        if response_alt.status_code == 200:
                            st.success("¡Análisis Exitoso (Ruta Pro)!")
                            st.markdown(response_alt.json()['candidates'][0]['content']['parts'][0]['text'])
                        else:
                            st.error(f"Error de Google: {res_json.get('error', {}).get('message', 'Error desconocido')}")
                            st.info("💡 Tip: Verifica que tu API Key en AI Studio esté marcada como 'Free Tier'.")
                except Exception as e:
                    st.error(f"Error de red: {str(e)}")
        else:
            st.warning("Por favor, describe tu proyecto.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
