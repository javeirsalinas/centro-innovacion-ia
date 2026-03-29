import streamlit as st
import requests
import json

# 1. Configuración de Marca y Estilo
st.set_page_config(page_title="RedInnovacion.pe | Registro y BMC", page_icon="🇵🇪", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #0E8388; font-size: 35px; font-weight: bold; }
    .section-header { color: #ffffff; background-color: #0E8388; padding: 10px; border-radius: 5px; font-size: 18px; font-weight: bold; margin-top: 25px; }
    .canvas-header { color: #2E4F4F; font-size: 20px; font-weight: bold; margin-top: 15px; border-bottom: 2px solid #0E8388; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚀 RedInnovacion.pe: Centro de Emprendimiento</p>', unsafe_allow_html=True)

# 2. Configuración de API
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    with st.form("registro_bmc_form"):
        # --- SECCIÓN DE REGISTRO ---
        st.markdown('<p class="section-header">📋 DATOS DEL EMPRENDEDOR</p>', unsafe_allow_html=True)
        col_reg1, col_reg2, col_reg3 = st.columns(3)
        
        with col_reg1:
            nombre_usuario = st.text_input("Nombre Emprendedor")
        with col_reg2:
            nombre_emprendimiento = st.text_input("Nombre del Emprendimiento")
        with col_reg3:
            region = st.selectbox("Región del Perú donde opera", [
                "Amazonas", "Ancash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca", "Callao", 
                "Cusco", "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad", "Lambayeque", 
                "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco", "Piura", "Puno", 
                "San Martín", "Tacna", "Tumbes", "Ucayali"
            ])

        st.write("") # Espaciador

        # --- SECCIÓN DEL CANVAS ---
        st.markdown('<p class="section-header">📊 BUSINESS MODEL CANVAS</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="canvas-header">1. PROPUESTA DE VALOR</p>', unsafe_allow_html=True)
        propuesta = st.text_area("¿Qué valor único entregas a tus clientes?", height=100)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="canvas-header">2. SEGMENTOS DE CLIENTES</p>', unsafe_allow_html=True)
            segmentos = st.text_area("¿A quiénes te diriges?", height=100)
            
            st.markdown('<p class="canvas-header">3. CANALES</p>', unsafe_allow_html=True)
            canales = st.text_area("¿Cómo llegas a ellos?", height=100)

        with col2:
            st.markdown('<p class="canvas-header">4. RELACIÓN CON CLIENTES</p>', unsafe_allow_html=True)
            relaciones = st.text_area("¿Cómo interactúas con tu audiencia?", height=100)
            
            st.markdown('<p class="canvas-header">5. FUENTES DE INGRESOS</p>', unsafe_allow_html=True)
            ingresos = st.text_area("¿Cuál es tu modelo de monetización?", height=100)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<p class="canvas-header">6. RECURSOS CLAVE</p>', unsafe_allow_html=True)
            recursos = st.text_area("¿Qué activos son indispensables?", height=100)
            
            st.markdown('<p class="canvas-header">7. ACTIVIDADES CLAVE</p>', unsafe_allow_html=True)
            actividades = st.text_area("¿Qué acciones críticas realizas?", height=100)

        with col4:
            st.markdown('<p class="canvas-header">8. SOCIOS CLAVE</p>', unsafe_allow_html=True)
            socios = st.text_area("¿Quiénes son tus aliados estratégicos?", height=100)
            
            st.markdown('<p class="canvas-header">9. ESTRUCTURA DE COSTOS</p>', unsafe_allow_html=True)
            costos = st.text_area("¿En qué inviertes principalmente?", height=100)

        st.markdown("---")
        enviar = st.form_submit_button("🚀 Generar Mentoría Personalizada")

    if enviar:
        if nombre_usuario and nombre_emprendimiento and propuesta:
            with st.spinner(f"Hola {nombre_usuario}, estamos analizando '{nombre_emprendimiento}' para la región {region}..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
                
                contexto_usuario = f"Emprendedor: {nombre_usuario}, Empresa: {nombre_emprendimiento}, Región: {region}."
                datos_canvas = f"BMC: Propuesta:{propuesta}, Segmentos:{segmentos}, Canales:{canales}, Relación:{relaciones}, Ingresos:{ingresos}, Recursos:{recursos}, Actividades:{actividades}, Socios:{socios}, Costos:{costos}"
                
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Eres el mentor principal de RedInnovacion.pe. {contexto_usuario} {datos_canvas}. Brinda un análisis estratégico profundo. Menciona oportunidades específicas para la región {region} y cómo potenciar '{nombre_emprendimiento}'."}]
                    }]
                }
                
                try:
                    response = requests.post(url, json=payload)
                    if response.status_code == 200:
                        resultado = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success(f"¡Diagnóstico Estratégico para {nombre_emprendimiento} finalizado!")
                        st.markdown(resultado)
                    else:
                        st.error("Error en la respuesta de Google AI. Revisa los permisos de la API Key.")
                except Exception as e:
                    st.error(f"Falla de conexión: {e}")
        else:
            st.warning("Por favor, completa los datos de registro (Nombre, Emprendimiento y Región) y al menos la Propuesta de Valor.")

else:
    st.error("⚠️ Falta la GOOGLE_API_KEY en los Secrets de Streamlit.")

st.sidebar.markdown("### RedInnovacion.pe")
st.sidebar.info("Conectando el talento de todas las regiones del Perú con la tecnología del futuro.")
