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
            with st.spinner("Conectando con el servidor estable de Google..."):
                # URL CORREGIDA: Usamos la versión 'v1' y el modelo 'gemini-1.5-flash'
                # Esta es la ruta oficial que Google garantiza para 2026
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Actúa como mentor experto en agronegocios. Analiza el proyecto {descripcion} de {nombre} (COLPA DE COPA) en la selva peruana y da 3 consejos estratégicos."}]
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
                        # Si sale error, mostramos el mensaje exacto de Google
                        st.error(f"Error de Google: {res_json['error']['message']}")
                        st.info("Sugerencia: Revisa que tu API Key en Google AI Studio no tenga restricciones de país.")
                except Exception as e:
                    st.error(f"Error de red: {str(e)}")
        else:
            st.warning("Por favor, describe tu proyecto.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
