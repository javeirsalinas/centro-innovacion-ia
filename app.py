import streamlit as st
import requests
import json

# 1. Configuración de Marca y Estilo
st.set_page_config(page_title="RedInnovacion.pe | Registro Completo", page_icon="📲", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #0E8388; font-size: 35px; font-weight: bold; }
    .section-header { color: #ffffff; background-color: #0E8388; padding: 10px; border-radius: 5px; font-size: 18px; font-weight: bold; margin-top: 25px; }
    .canvas-header { color: #2E4F4F; font-size: 19px; font-weight: bold; margin-top: 15px; border-bottom: 2px solid #0E8388; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚀 RedInnovacion.pe: Centro de Emprendimiento</p>', unsafe_allow_html=True)

# 2. Configuración de API
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    with st.form("registro_total_form"):
        # --- SECCIÓN DE REGISTRO AMPLIADA ---
        st.markdown('<p class="section-header">👤 DATOS DEL EMPRENDEDOR Y CONTACTO</p>', unsafe_allow_html=True)
        
        col_reg1, col_reg2 = st.columns(2)
        with col_reg1:
            nombre_usuario = st.text_input("Nombre Emprendedor")
            correo = st.text_input("Correo Electrónico (Para enviar la mentoría)")
        with col_reg2:
            nombre_emprendimiento = st.text_input("Nombre del Emprendimiento")
            whatsapp = st.text_input("Número de WhatsApp (Ej: +51 999 888 777)")

        region = st.selectbox("Región del Perú donde opera", [
            "Amazonas", "Ancash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca", "Callao", 
            "Cusco", "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad", "Lambayeque", 
            "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco", "Piura", "Puno", 
            "San Martín", "Tacna", "Tumbes", "Ucayali"
        ])

        # --- SECCIÓN DEL CANVAS ---
        st.markdown('<p class="section-header">📊 BUSINESS MODEL CANVAS</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="canvas-header">1. PROPUESTA DE VALOR</p>', unsafe_allow_html=True)
        propuesta = st.text_area("¿Qué valor único entregas?")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="canvas-header">2. SEGMENTOS DE CLIENTES</p>', unsafe_allow_html=True)
            segmentos = st.text_area("Segmentos")
            st.markdown('<p class="canvas-header">3. CANALES</p>', unsafe_allow_html=True)
            canales = st.text_area("Canales")
        with col2:
            st.markdown('<p class="canvas-header">4. RELACIÓN CON CLIENTES</p>', unsafe_allow_html=True)
            relaciones = st.text_area("Relación")
            st.markdown('<p class="canvas-header">5. FUENTES DE INGRESOS</p>', unsafe_allow_html=True)
            ingresos = st.text_area("Ingresos")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<p class="canvas-header">6. RECURSOS CLAVE</p>', unsafe_allow_html=True)
            recursos = st.text_area("Recursos")
            st.markdown('<p class="canvas-header">7. ACTIVIDADES CLAVE</p>', unsafe_allow_html=True)
            actividades = st.text_area("Actividades")
        with col4:
            st.markdown('<p class="canvas-header">8. SOCIOS CLAVE</p>', unsafe_allow_html=True)
            socios = st.text_area("Socios")
            st.markdown('<p class="canvas-header">9. ESTRUCTURA DE COSTOS</p>', unsafe_allow_html=True)
            costos = st.text_area("Costos")

        st.markdown("---")
        enviar = st.form_submit_button("🚀 Finalizar y Generar Mentoría")

    if enviar:
        if nombre_usuario and correo and whatsapp and propuesta:
            with st.spinner("Generando tu reporte personalizado..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
                
                contexto = f"Emprendedor: {nombre_usuario}, Email: {correo}, WhatsApp: {whatsapp}, Empresa: {nombre_emprendimiento}, Región: {region}."
                
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Eres el mentor de RedInnovacion.pe. {contexto} Analiza su BMC y brinda un diagnóstico detallado. Al final, despídete mencionando que este reporte será la base para su crecimiento y que lo contactarás a su correo {correo} o WhatsApp {whatsapp}."}]
                    }]
                }
                
                try:
                    response = requests.post(url, json=payload)
                    if response.status_code == 200:
                        resultado = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success(f"¡Excelente {nombre_usuario}! Tu diagnóstico está listo.")
                        st.markdown(resultado)
                        
                        # Botón visual para simular envío (funcionalidad futura)
                        st.info(f"📧 Un resumen de esta mentoría ha sido preparado para enviarse a: {correo}")
                    else:
                        st.error("Error en el servidor de IA.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Por favor, completa tus datos de contacto y la Propuesta de Valor.")

else:
    st.error("⚠️ Configura la API KEY.")
