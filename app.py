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
        boton = st.form_submit_button("Consultar Mentoría 2026")

    if boton:
        if descripcion:
            with st.spinner("Conectando con el motor Gemini 2.0 (Producción)..."):
                # URL PARA GEMINI 2.0 FLASH - VERSIÓN DE PRODUCCIÓN 001
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Actúa como mentor experto en agronegocios. Analiza el proyecto {descripcion} de {nombre} (COLPA DE COPA) en la selva peruana y brinda una hoja de ruta técnica."}]
                    }]
                }
                
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(payload))
                    res_json = response.json()
                    
                    if response.status_code == 200:
                        texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.success("¡Conexión Exitosa con la Red de Innovación!")
                        st.markdown(texto_ia)
                    else:
                        # Si el -001 falla, intentamos el nombre genérico 'gemini-2.0-flash-exp'
                        url_exp = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
                        response_exp = requests.post(url_exp, headers=headers, data=json.dumps(payload))
                        
                        if response_exp.status_code == 200:
                            st.success("¡Conectado al modelo experimental de nueva generación!")
                            st.markdown(response_exp.json()['candidates'][0]['content']['parts'][0]['text'])
                        else:
                            st.error(f"Nota de Google: {res_json.get('error', {}).get('message', 'Modelo en mantenimiento')}")
                            st.info("💡 Tip: Verifica en AI Studio cuál es el nombre exacto del modelo que aparece en tu panel lateral.")
                except Exception as e:
                    st.error(f"Error de red: {str(e)}")
        else:
            st.warning("Por favor, describe tu proyecto.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Sistema actualizado al motor estable Gemini 2.0.")
