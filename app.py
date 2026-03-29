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
            with st.spinner("Conectando con el cerebro de Google AI..."):
                # URL CORREGIDA: Usamos v1beta pero con la ruta directa al modelo Flash
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                data = {
                    "contents": [{
                        "parts": [{"text": f"Eres un mentor experto. Analiza el proyecto {descripcion} de {nombre} (COLPA DE COPA) en la selva peruana y da 3 consejos clave."}]
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
                        # Si falla el Flash, intentamos el Pro automáticamente en la misma llamada
                        st.info("Reintentando con modelo alternativo...")
                        url_pro = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
                        response_pro = requests.post(url_pro, headers=headers, data=json.dumps(data))
                        res_pro = response_pro.json()
                        
                        if response_pro.status_code == 200:
                            texto_pro = res_pro['candidates'][0]['content']['parts'][0]['text']
                            st.success("¡Análisis Exitoso (Modo Pro)!")
                            st.markdown(texto_pro)
                        else:
                            st.error(f"Error de Google: {res_pro['error']['message']}")
                except Exception as e:
                    st.error(f"Error de conexión: {str(e)}")
        else:
            st.warning("Escribe la descripción de tu proyecto.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
