import streamlit as st
import requests
import json
from fpdf import FPDF
import datetime

# 1. Configuración de Marca y Estilo
st.set_page_config(page_title="RedInnovacion.pe | Mentoría BMC Pro", page_icon="🇵🇪", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #0E8388; font-size: 35px; font-weight: bold; }
    .section-header { color: #ffffff; background-color: #0E8388; padding: 10px; border-radius: 5px; font-size: 18px; font-weight: bold; margin-top: 25px; }
    .canvas-header { color: #2E4F4F; font-size: 18px; font-weight: bold; margin-top: 15px; border-bottom: 2px solid #0E8388; }
    </style>
    """, unsafe_allow_html=True)

# Función para generar el PDF Profesional
def create_pdf(nombre, empresa, region, resultado, bmc_data):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado con Identidad Visual
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(14, 131, 136) # Color Esmeralda de RedInnovacion
    pdf.cell(200, 10, txt="RedInnovacion.pe", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt="Reporte de Mentoría Estratégica", ln=True, align='C')
    
    # Datos de Registro
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 10, txt=f"Emprendedor: {nombre}", ln=True)
    pdf.cell(0, 10, txt=f"Empresa: {empresa}", ln=True)
    pdf.cell(0, 10, txt=f"Region: {region} | Fecha: {datetime.date.today()}", ln=True)
    
    # Cuerpo del Diagnóstico
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, txt="DIAGNOSTICO ESTRATEGICO IA", ln=True, fill=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", '', 10)
    # Limpiamos caracteres especiales para evitar errores en PDF
    clean_text = resultado.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, txt=clean_text)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, txt="RedInnovacion.pe - Impulsando el emprendimiento en todo el Peru.", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

st.markdown('<p class="main-title">🚀 RedInnovacion.pe: Consultor de Negocios</p>', unsafe_allow_html=True)

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    with st.form("form_completo_bmc"):
        # --- REGISTRO ---
        st.markdown('<p class="section-header">👤 REGISTRO DEL EMPRENDEDOR</p>', unsafe_allow_html=True)
        col_r1, col_r2, col_r3 = st.columns(3)
        nombre = col_r1.text_input("Nombre Completo")
        empresa = col_r2.text_input("Nombre de tu Negocio")
        region = col_r3.selectbox("Región", ["Amazonas", "Ancash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca", "Callao", "Cusco", "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad", "Lambayeque", "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco", "Piura", "Puno", "San Martín", "Tacna", "Tumbes", "Ucayali"])
        
        col_c1, col_c2 = st.columns(2)
        email = col_c1.text_input("Correo Electrónico")
        whatsapp = col_c2.text_input("WhatsApp")

        # --- LAS 9 CASILLAS DEL CANVAS ---
        st.markdown('<p class="section-header">📊 BUSINESS MODEL CANVAS (9 BLOQUES)</p>', unsafe_allow_html=True)
        
        # Bloque 1: Propuesta de Valor (Centro)
        st.markdown('<p class="canvas-header">1. PROPUESTA DE VALOR</p>', unsafe_allow_html=True)
        propuesta = st.text_area("¿Qué ofreces de único?", height=80)

        # Bloques 2, 3, 4 y 5
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="canvas-header">2. SEGMENTOS DE CLIENTES</p>', unsafe_allow_html=True)
            segmentos = st.text_area("¿Quiénes te compran?", height=80)
            st.markdown('<p class="canvas-header">3. CANALES</p>', unsafe_allow_html=True)
            canales = st.text_area("¿Cómo vendes y entregas?", height=80)
        with col2:
            st.markdown('<p class="canvas-header">4. RELACIÓN CON CLIENTES</p>', unsafe_allow_html=True)
            relaciones = st.text_area("¿Cómo retienes a tus clientes?", height=80)
            st.markdown('<p class="canvas-header">5. FUENTES DE INGRESOS</p>', unsafe_allow_html=True)
            ingresos = st.text_area("¿Cómo generas dinero?", height=80)

        # Bloques 6, 7, 8 y 9
        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<p class="canvas-header">6. RECURSOS CLAVE</p>', unsafe_allow_html=True)
            recursos = st.text_area("¿Qué necesitas para operar?", height=80)
            st.markdown('<p class="canvas-header">7. ACTIVIDADES CLAVE</p>', unsafe_allow_html=True)
            actividades = st.text_area("¿Qué haces día a día?", height=80)
        with col4:
            st.markdown('<p class="canvas-header">8. SOCIOS CLAVE</p>', unsafe_allow_html=True)
            socios = st.text_area("¿Quiénes son tus aliados?", height=80)
            st.markdown('<p class="canvas-header">9. ESTRUCTURA DE COSTOS</p>', unsafe_allow_html=True)
            costos = st.text_area("¿En qué gastas dinero?", height=80)

        st.markdown("---")
        enviar = st.form_submit_button("🚀 Generar Mentoría y Reporte PDF")

    if enviar:
        if nombre and propuesta and email:
            with st.spinner("Analizando tu modelo de negocio con Gemini 2.5..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
                
                bmc_full = f"1.Propuesta:{propuesta}, 2.Segmentos:{segmentos}, 3.Canales:{canales}, 4.Relación:{relaciones}, 5.Ingresos:{ingresos}, 6.Recursos:{recursos}, 7.Actividades:{actividades}, 8.Socios:{socios}, 9.Costos:{costos}"
                
                prompt = f"Eres el consultor senior de RedInnovacion.pe. Emprendedor: {nombre}, Empresa: {empresa}, Región: {region}. Analiza este BMC: {bmc_full}. Da un diagnóstico y 3 consejos. Menciona que el PDF está listo abajo."
                
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                
                try:
                    resp = requests.post(url, json=payload)
                    if resp.status_code == 200:
                        diagnostico = resp.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success(f"¡Análisis Completado para {empresa}!")
                        st.markdown(diagnostico)
                        
                        # Generar y mostrar botón PDF
                        pdf_data = create_pdf(nombre, empresa, region, diagnostico, bmc_full)
                        st.download_button(
                            label="📥 Descargar Reporte PDF Profesional",
                            data=pdf_data,
                            file_name=f"Reporte_RedInnovacion_{empresa}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error("Error en la IA. Intenta de nuevo.")
                except Exception as e:
                    st.error(f"Fallo de conexión: {e}")
        else:
            st.warning("Completa los datos de registro y al menos la Propuesta de Valor.")
else:
    st.error("⚠️ Configura la API KEY en los Secrets.")
