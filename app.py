import streamlit as st
import requests
import json

# 1. Configuración de Marca RedInnovacion.pe
st.set_page_config(page_title="RedInnovacion.pe | Mentoría BMC", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #0E8388; font-size: 35px; font-weight: bold; }
    .canvas-header { color: #2E4F4F; font-size: 22px; font-weight: bold; margin-top: 20px; border-bottom: 2px solid #0E8388; }
    .stTextArea label { font-weight: bold; color: #111; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚀 RedInnovacion.pe: Mentoría Business Model Canvas</p>', unsafe_allow_html=True)
st.write("Completa los 9 bloques de tu modelo de negocio para recibir una auditoría estratégica integral.")

# 2. Configuración de API
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    with st.form("bmc_form"):
        st.markdown('<p class="canvas-header">1. PROPUESTA DE VALOR</p>', unsafe_allow_html=True)
        propuesta = st.text_area("¿Qué problema resuelves y qué te hace único?", placeholder="Ej: Licores artesanales con frutos exóticos medicinales...")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="canvas-header">2. SEGMENTOS DE CLIENTES</p>', unsafe_allow_html=True)
            segmentos = st.text_area("¿Quiénes son tus clientes ideales?", placeholder="Ej: Turistas, amantes de productos orgánicos, 25-50 años...")
            
            st.markdown('<p class="canvas-header">3. CANALES</p>', unsafe_allow_html=True)
            canales = st.text_area("¿Cómo entregas tu producto/servicio?", placeholder="Ej: Tienda online, ferias regionales, redes sociales...")

        with col2:
            st.markdown('<p class="canvas-header">4. RELACIÓN CON CLIENTES</p>', unsafe_allow_html=True)
            relaciones = st.text_area("¿Cómo captas y retienes clientes?", placeholder="Ej: Atención personalizada, comunidad en WhatsApp, programas de lealtad...")
            
            st.markdown('<p class="canvas-header">5. FUENTES DE INGRESOS</p>', unsafe_allow_html=True)
            ingresos = st.text_area("¿Cómo ganas dinero?", placeholder="Ej: Venta directa por botella, suscripción mensual, talleres de cata...")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<p class="canvas-header">6. RECURSOS CLAVE</p>', unsafe_allow_html=True)
            recursos = st.text_area("¿Qué activos necesitas para operar?", placeholder="Ej: Planta de destilación, permisos sanitarios, expertos en botánica...")
            
            st.markdown('<p class="canvas-header">7. ACTIVIDADES CLAVE</p>', unsafe_allow_html=True)
            actividades = st.text_area("¿Qué acciones son vitales para tu negocio?", placeholder="Ej: Producción, control de calidad, marketing digital...")

        with col4:
            st.markdown('<p class="canvas-header">8. SOCIOS CLAVE</p>', unsafe_allow_html=True)
            socios = st.text_area("¿Quiénes son tus aliados estratégicos?", placeholder="Ej: Agricultores locales, distribuidores en Lima, RedInnovacion.pe...")
            
            st.markdown('<p class="canvas-header">9. ESTRUCTURA DE COSTOS</p>', unsafe_allow_html=True)
            costos = st.text_area("¿En qué gastas principalmente?", placeholder="Ej: Materia prima, envases, publicidad, salarios...")

        st.markdown("---")
        enviar = st.form_submit_button("🚀 Generar Diagnóstico de Modelo de Negocio")

    if enviar:
        if propuesta and segmentos:
            with st.spinner("Nuestros consultores de RedInnovacion.pe están auditando tu Canvas..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
                
                bmc_data = f"""
                Analiza este Business Model Canvas:
                1. Propuesta: {propuesta}
                2. Segmentos: {segmentos}
                3. Canales: {canales}
                4. Relación: {relaciones}
                5. Ingresos: {ingresos}
                6. Recursos: {recursos}
                7. Actividades: {actividades}
                8. Socios: {socios}
                9. Costos: {costos}
                """
                
                payload = {
                    "contents": [{
                        "parts": [{"text": f"Eres un consultor senior de RedInnovacion.pe experto en Lean Startup. {bmc_data} Brinda: 1. Un análisis de coherencia del modelo. 2. Identifica el riesgo más grande. 3. Tres recomendaciones para escalar el negocio rápidamente."}]
                    }]
                }
                
                try:
                    response = requests.post(url, json=payload)
                    if response.status_code == 200:
                        resultado = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success("¡Diagnóstico Estratégico Finalizado!")
                        st.markdown(resultado)
                    else:
                        st.error("Error en la conexión. Revisa tu API Key.")
                except Exception as e:
                    st.error(f"Falla de red: {e}")
        else:
            st.warning("Para una mentoría de calidad, completa al menos la Propuesta de Valor y el Segmento de Clientes.")

else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en Secrets.")
