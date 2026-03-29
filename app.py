import streamlit as st
import requests
import json

st.set_page_config(page_title="Centro de Innovación AI", layout="wide")
st.title("🚀 AgentLake: Centro de Innovación")
st.subheader("Proyecto: COLPA DE COPA (MULTISERVICIOS DAMAR S.A.C)")

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    with st.form("mentoria_form"):
        nombre = st.text_input("Nombre del Emprendedor")
        descripcion = st.text_area("Descripción (Ej: Licores de la selva peruana)")
        boton = st.form_submit_button("Consultar Mentoría")

    if boton and descripcion:
        # LISTA DE MODELOS A PROBAR (Los más comunes)
        modelos_a_probar = [
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-pro"
        ]
        
        exito = False
        for modelo in modelos_a_probar:
            if exito: break
            
            with st.spinner(f"Probando conexión con {modelo}..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
                headers = {'Content-Type': 'application/json'}
                data = {"contents": [{"parts": [{"text": f"Eres mentor de negocios. Analiza: {descripcion}"}]}]}
                
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(data))
                    res_json = response.json()
                    
                    if response.status_code == 200:
                        texto = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.success(f"¡Análisis Exitoso con {modelo}!")
                        st.markdown(texto)
                        exito = True
                    else:
                        continue # Prueba el siguiente modelo
                except:
                    continue

        if not exito:
            st.error("No se pudo conectar con ningún modelo de Google. Por favor, verifica que tu NUEVA API Key esté activa en Google AI Studio.")
else:
    st.error("⚠️ Configura la NUEVA GOOGLE_API_KEY en Secrets.")
