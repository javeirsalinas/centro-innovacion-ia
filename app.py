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
            with st.spinner("Conectando con el Mentor Senior..."):
                # ESTA ES LA URL QUE FUNCIONA EN 2026: v1 con gemini-1.5-flash
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                data = {
                    "contents": [{
                        "parts": [{"text": f"Actúa como mentor experto en agronegocios. Analiza el proyecto {descripcion} de {nombre} (COLPA DE COPA) en la selva peruana y da 3 consejos estratégicos."}]
                    }]
                }
                
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(data))
                    res_json = response.json()
                    
                    if response.status_code == 200:
                        # Extraer la respuesta exitosa
                        texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.success("¡Análisis Exitoso!")
                        st.markdown(texto_ia)
                    else:
                        # Si sale error, mostramos el mensaje real de Google
                        error_msg = res_json.get('error', {}).get('message', 'Error desconocido')
                        st.error(f"Nota de Google: {error_msg}")
                        st.info("Sugerencia: Entra a Google AI Studio y verifica que tu API Key esté activa.")
                except Exception as e:
                    st.error(f"Error de conexión: {str(e)}")
        else:
            st.warning("Por favor, escribe la descripción de tu proyecto.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
