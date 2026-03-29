import streamlit as st
import requests

st.set_page_config(page_title="Centro de Innovación AI", layout="wide")
st.title("🚀 AgentLake: Centro de Innovación")
st.write("Proyecto: **COLPA DE COPA (MULTISERVICIOS DAMAR S.A.C)**")

# 1. Cargar la llave desde Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    descripcion = st.text_area("Cuéntanos sobre tu innovación en la selva:")
    
    if st.button("Consultar Mentoría"):
        if descripcion:
            with st.spinner("Llamando al mentor..."):
                # URL UNIVERSAL DE 2026
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{"parts": [{"text": f"Eres un mentor experto. Analiza este proyecto de licores en la selva peruana: {descripcion}"}]}]
                }
                
                try:
                    response = requests.post(url, json=payload)
                    data = response.json()
                    
                    if response.status_code == 200:
                        st.success("¡Conexión exitosa!")
                        st.markdown(data['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        # Si sale error, mostramos el mensaje exacto para saber qué falta
                        st.error(f"Error {response.status_code}: {data['error']['message']}")
                except Exception as e:
                    st.error(f"Falla de red: {str(e)}")
else:
    st.error("⚠️ No hay API Key en los Secrets de Streamlit.")
