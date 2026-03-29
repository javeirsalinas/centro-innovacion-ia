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
        boton = st.form_submit_button("Consultar Mentoría con Gemini 2.0")

    if boton:
        if descripcion:
            with st.spinner("Conectando con Gemini 2.0 Flash..."):
                # URL PARA GEMINI 2.0 FLASH (La versión más moderna de 2026)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Eres un mentor experto en agronegocios. Analiza el proyecto {descripcion} de {nombre} (COLPA DE COPA) en la selva peruana y da 3 consejos estratégicos."}]
                    }]
                }
                
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(payload))
                    res_json = response.json()
                    
                    if response.status_code == 200:
                        texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.success("¡Conexión Exitosa con Gemini 2.0!")
                        st.markdown(texto_ia)
                    else:
                        st.error(f"Error de Google: {res_json.get('error', {}).get('message', 'Modelo no disponible')}")
                        st.info("💡 Tip: Si sale error, verifica que el nombre en AI Studio sea exactamente 'gemini-2.0-flash'.")
                except Exception as e:
                    st.error(f"Error de red: {str(e)}")
        else:
            st.warning("Por favor, describe tu proyecto.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado con tecnología Gemini 2.0 para el Centro de Innovación.")
