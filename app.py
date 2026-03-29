import streamlit as st
import requests
import json

# 1. Configuración de identidad visual
st.set_page_config(
    page_title="RedInnovacion.pe | Centro de Innovación", 
    page_icon="🚀",
    layout="wide"
)

# Estilo personalizado para el nombre
st.markdown("""
    <style>
    .main-title {
        color: #0E8388;
        font-size: 40px;
        font-weight: bold;
    }
    .subtitle {
        color: #2E4F4F;
        font-size: 20px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚀 RedInnovacion.pe</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Centro de Emprendimiento e Innovación Tecnológica</p>', unsafe_allow_html=True)

st.divider()

# 2. Configuración de la API (Gemini 2.5 Flash-Lite)
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Formulario de Mentoría
    with st.container():
        st.info("💡 Bienvenido al Panel de Mentoría Digital. Cuéntanos sobre tu proyecto para recibir un análisis estratégico instantáneo.")
        
        with st.form("mentoria_redinnovacion"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre del Emprendedor")
            with col2:
                proyecto = st.text_input("Nombre del Proyecto / Idea")
                
            descripcion = st.text_area("Describe tu propuesta, tus retos y tus metas:")
            
            boton = st.form_submit_button("Obtener Mentoría Estratégica")

    if boton:
        if descripcion:
            with st.spinner("Analizando con el motor de IA de RedInnovacion.pe..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
                
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Actúa como un mentor senior de RedInnovacion.pe, un centro de emprendimiento e innovación en Perú. Analiza el proyecto '{proyecto}' de {nombre}. Descripción: {descripcion}. Brinda una hoja de ruta con 3 pasos críticos, consejos de escalabilidad y una frase de motivación inspiradora."}]
                    }]
                }
                
                try:
                    response = requests.post(url, headers=headers, data=json.dumps(payload))
                    res_json = response.json()
                    
                    if response.status_code == 200:
                        resultado = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.success(f"¡Análisis Generado Exitosamente para {proyecto}!")
                        st.markdown("---")
                        st.markdown(resultado)
                        st.markdown("---")
                        st.caption("Respuesta generada por el motor Gemini 2.5 Flash-Lite - RedInnovacion.pe © 2026")
                    else:
                        st.error("Hubo un problema al conectar con el servidor. Inténtalo de nuevo en unos segundos.")
                except Exception as e:
                    st.error(f"Error de conexión: {str(e)}")
        else:
            st.warning("Por favor, ingresa los detalles de tu proyecto para iniciar el análisis.")
else:
    st.error("⚠️ Error de configuración: La clave de acceso no está vinculada. Contacta al soporte técnico de RedInnovacion.pe")

# Pie de página profesional
st.sidebar.title("Sobre Nosotros")
st.sidebar.info("""
**RedInnovacion.pe** es el ecosistema líder para el desarrollo de emprendimientos tecnológicos en la región. 
Nuestra misión es potenciar el talento local mediante el uso de Inteligencia Artificial avanzada.
""")
