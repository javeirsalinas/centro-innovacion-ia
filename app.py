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
    # Configuración de página con fondo oscuro
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # --- PÁGINA 1: Carátula y Diagnóstico Principal ---
    # Fondo Oscuro (Rectángulo que cubre toda la página)
    pdf.set_fill_color(18, 18, 18) # Gris casi negro #121212
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Logo / Nombre de Marca
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(14, 131, 136) # Verde Esmeralda RedInnovacion
    pdf.cell(0, 20, txt="RedInnovacion.pe", ln=True, align='L')
    
    # Título del Reporte
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(255, 255, 255) # Blanco
    pdf.cell(0, 10, txt="REPORTE ESTRATEGICO DE MENTORIA", ln=True)
    pdf.ln(5)
    
    # Datos del Emprendedor (En caja resaltada)
    pdf.set_fill_color(30, 30, 30)
    pdf.set_text_color(200, 200, 200)
    pdf.set_font("Arial", '', 10)
    info_user = f"Emprendedor: {nombre}  |  Empresa: {empresa}  |  Region: {region}  |  Fecha: {datetime.date.today()}"
    pdf.cell(0, 10, txt=info_user, ln=True, fill=True, align='C')
    
    # Contenido del Diagnóstico (Parte 1)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(14, 131, 136)
    pdf.cell(0, 10, txt="1. ANALISIS DEL MODELO DE NEGOCIO", ln=True)
    
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(240, 240, 240)
    # Limpieza de texto para evitar errores de codificación
    clean_text = resultado.encode('latin-1', 'replace').decode('latin-1')
    
    # Controlamos que el texto fluya (FPDF creará la pág 2 automáticamente si es necesario)
    pdf.multi_cell(0, 7, txt=clean_text)

    # --- PIE DE PÁGINA ---
    # Nos aseguramos de poner un cierre visual al final de la página 2
    if pdf.page_no() > 2:
        # Si por alguna razón la IA se excede, cortamos aquí (opcional)
        pass 

    return pdf.output(dest='S').encode('latin-1')

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
