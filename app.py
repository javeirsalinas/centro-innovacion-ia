import streamlit as st
import requests
import json
from fpdf import FPDF
import datetime

# 1. Configuración de Marca
st.set_page_config(page_title="RedInnovacion.pe | Reporte PDF", page_icon="📄", layout="wide")

# Función para generar PDF
def create_pdf(nombre, empresa, region, resultado):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(14, 131, 136) # Color RedInnovacion
    pdf.cell(200, 10, txt="RedInnovacion.pe", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt="Reporte de Mentoría Estratégica - BMC", ln=True, align='C')
    
    # Datos del Emprendedor
    pdf.set_font("Arial", 'B', 10)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Emprendedor: {nombre}", ln=True)
    pdf.cell(200, 10, txt=f"Empresa: {empresa}", ln=True)
    pdf.cell(200, 10, txt=f"Region: {region}", ln=True)
    pdf.cell(200, 10, txt=f"Fecha: {datetime.date.today()}", ln=True)
    
    # Contenido del Diagnóstico
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Diagnóstico de la IA:", ln=True)
    
    pdf.set_font("Arial", '', 10)
    # Multi_cell permite que el texto largo salte de línea automáticamente
    pdf.multi_cell(0, 7, txt=resultado.encode('latin-1', 'replace').decode('latin-1'))
    
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(200, 10, txt="Este documento es un análisis generado por IA para fines informativos. RedInnovacion.pe 2026", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# Interfaz Visual
st.markdown('<h1 style="color: #0E8388;">🚀 RedInnovacion.pe</h1>', unsafe_allow_html=True)

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    with st.form("form_completo"):
        st.subheader("📋 Registro y Modelo de Negocio")
        c1, c2, c3 = st.columns(3)
        nombre = c1.text_input("Tu Nombre")
        empresa = c2.text_input("Tu Emprendimiento")
        region = c3.selectbox("Región", ["Lima", "Ucayali", "Cusco", "Arequipa", "Loreto", "Otros..."])
        
        email = st.text_input("Correo Electrónico")
        whatsapp = st.text_input("WhatsApp")
        
        st.divider()
        st.write("### 📊 Business Model Canvas")
        propuesta = st.text_area("Propuesta de Valor")
        segmentos = st.text_area("Segmentos de Clientes")
        # (Puedes agregar los otros 7 campos aquí siguiendo el mismo patrón)
        
        enviar = st.form_submit_button("Generar Diagnóstico")

    if enviar:
        if nombre and propuesta:
            with st.spinner("Generando análisis estratégico..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"Mentor de RedInnovacion.pe. Analiza a {empresa} en {region}. Propuesta: {propuesta}. Segmentos: {segmentos}."}]}]
                }
                
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    resultado = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("¡Diagnóstico Listo!")
                    st.markdown(resultado)
                    
                    # --- BOTÓN DE DESCARGA PDF ---
                    pdf_bytes = create_pdf(nombre, empresa, region, resultado)
                    st.download_button(
                        label="📥 Descargar Mentoría en PDF",
                        data=pdf_bytes,
                        file_name=f"Mentoria_{empresa}.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("Error al conectar con la IA.")
else:
    st.error("Falta API Key.")
