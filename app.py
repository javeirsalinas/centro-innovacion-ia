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
            with st.spinner("Buscando canal de conexión con Google AI..."):
                # PROBAMOS LA RUTA QUE SÍ ESTÁ ACTIVA EN MARZO 2026
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Eres un mentor experto en agronegocios. Analiza el proyecto {descripcion} de {nombre}."}]
                    }]
                }
                
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(payload))
                    res_json = response.json()
                    
                    if response.status_code == 200:
                        texto_ia = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.success("¡Conexión Exitosa!")
                        st.markdown(texto_ia)
                    else:
                        # Si falla el anterior, intentamos con el nombre corto
                        url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
                        response_alt = requests.post(url_alt, headers=headers, data=json.dumps(payload))
                        
                        if response_alt.status_code == 200:
                            st.success("¡Conexión Exitosa (Ruta Alternativa)!")
                            st.markdown(response_alt.json()['candidates'][0]['content']['parts'][0]['text'])
                        else:
                            st.error(f"Error de Google: {res_json.get('error', {}).get('message', 'Error desconocido')}")
                            st.info("💡 Tip: Ve a Google AI Studio y verifica que el chat te responda ahí mismo.")
                except Exception as e:
                    st.error(f"Error de red: {str(e)}")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.info("Desarrollado para el Centro de Emprendimiento e Innovación.")
