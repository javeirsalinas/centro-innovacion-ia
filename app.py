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
        boton = st.form_submit_button("Consultar Mentoría 2.5 Flash-Lite")

    if boton:
        if descripcion:
            with st.spinner("Conectando con el motor Gemini 2.5 Flash-Lite..."):
                # URL PARA GEMINI 2.5 FLASH-LITE (Versión 2026)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Actúa como mentor experto en agronegocios. Analiza el proyecto {descripcion} de {nombre} (COLPA DE COPA) en la selva peruana y brinda 3 consejos estratégicos."}]
                    }]
                }
                
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(payload))
                    res_json = response.json()
                    
                    if response.status_code == 200:
                        texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.success("¡Conexión Exitosa con Gemini 2.5!")
                        st.markdown(texto_ia)
                    else:
                        # Error detallado para diagnóstico
                        error_msg = res_json.get('error', {}).get('message', 'Modelo no disponible')
                        st.error(f"Nota de Google: {error_msg}")
                        st.info("💡 Tip: Si el error persiste, verifica en AI Studio si el nombre tiene algún sufijo como '-exp' o '-001'.")
                except Exception as e:
                    st.error(f"Error de red: {str(e)}")
        else:
            st.warning("Por favor, describe tu proyecto.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Sistema actualizado al motor de última generación Gemini 2.5.")
