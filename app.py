import streamlit as st
import requests
import json
from fpdf import FPDF
import datetime

# 1. Configuración de Marca y Estilo de la App
st.set_page_config(page_title="RedInnovacion.pe | Mentoría Pro", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #0E8388; font-size: 35px; font-weight: bold; }
    .section-header { color: #ffffff; background-color: #0E8388; padding: 10px; border-radius: 5px; font-size: 18px; font-weight: bold; margin-top: 25px; }
    .canvas-header { color: #2E4F4F; font-size: 18px; font-weight: bold; margin-top: 15px; border-bottom: 2px solid #0E8388; }
    </style>
    """, unsafe_allow_html=True)

# 2. Clase PDF personalizada para Modo Oscuro y Control de Páginas
class DarkPDF(FPDF):
    def header(self):
        # Fondo oscuro en cada página
        self.set_fill_color(18, 18, 18) 
        self.rect(0, 0, 210, 297, 'F')
        # Logo de RedInnovacion.pe
        self.set_font("Arial", 'B', 15)
        self.set_text_color(14, 131, 136)
        self.cell(0, 10, "RedInnovacion.pe", ln=True, align='L')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Página {self.page_no()} | Centro de Innovación Tecnológica 2026", align='C')

def create_dark_pdf(nombre, empresa, region, resultado):
    pdf = DarkPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Título Principal
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, txt="DIAGNÓSTICO ESTRATÉGICO", ln=True)
    
    # Ficha Técnica
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(14, 131, 136)
    pdf.cell(0, 8, txt=f"PROYECTO: {empresa.upper()}", ln=True)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 8, txt=f"EMPRENDEDOR: {nombre} | REGIÓN: {region} | FECHA: {datetime.date.today()}", ln=True)
    pdf.ln(10)
    
    # Contenido del Diagnóstico
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(240, 240, 240)
    
    # Limpiamos texto para evitar errores de símbolos
    clean_text = resultado.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, txt=clean_text)
    
    # Forzar límite visual (Opcional: solo avisar si pasa de 2)
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ STREAMLIT ---
st.markdown('<p class="main-title">🚀 RedInnovacion.pe: Consultoría Elite</p>', unsafe_allow_html=True)

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    with st.form("form_red_innovacion"):
        st.markdown('<p class="section-header">👤 DATOS DE CONTACTO</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        nombre = c1.text_input("Nombre")
        empresa = c2.text_input("Emprendimiento")
        region = c3.selectbox("Región", ["Lima", "Ucayali", "Cusco", "Arequipa", "Loreto", "Piura", "Otros..."])
        
        email = st.text_input("Correo")
        whatsapp = st.text_input("WhatsApp")

        st.markdown('<p class="section-header">📊 BUSINESS MODEL CANVAS (Resumen Ejecutivo)</p>', unsafe_allow_html=True)
        propuesta = st.text_area("1. Propuesta de Valor")
        
        col_a, col_b = st.columns(2)
        segmentos = col_a.text_area("2. Segmentos de Clientes")
        canales = col_b.text_area("3. Canales")
        
        col_c, col_d = st.columns(2)
        relaciones = col_c.text_area("4. Relación con Clientes")
        ingresos = col_d.text_area("5. Fuentes de Ingresos")
        
        col_e, col_f = st.columns(2)
        recursos = col_e.text_area("6. Recursos Clave")
        actividades = col_f.text_area("7. Actividades Clave")
        
        col_g, col_h = st.columns(2)
        socios = col_g.text_area("8. Socios Clave")
        costos = col_h.text_area("9. Estructura de Costos")

        enviar = st.form_submit_button("🔥 Generar Reporte Dark Mode")

    if enviar:
        if nombre and propuesta and email:
            with st.spinner("IA analizando..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
                
                # INSTRUCCIÓN PARA CONTROLAR EXTENSIÓN
                prompt = f"""
                Eres un consultor senior de RedInnovacion.pe. 
                Analiza el BMC de {empresa} ({nombre}) en {region}. 
                DATOS: {propuesta}, {segmentos}, {canales}, {ingresos}, {costos}.
                
                ESTRUCTURA OBLIGATORIA (Máximo 600 palabras para que entre en 2 páginas):
                1. RESUMEN EJECUTIVO (Párrafo corto).
                2. ANÁLISIS DE COHERENCIA (Puntos clave).
                3. RIESGOS DETECTADOS (Top 2).
                4. HOJA DE RUTA (3 pasos inmediatos).
                5. CONSEJO REGIONAL (Específico para {region}).
                
                Usa un tono corporativo y motivador. No uses negritas (**) en el texto para el PDF.
                """
                
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                resp = requests.post(url, json=payload)
                
                if resp.status_code == 200:
                    diagnostico = resp.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("¡Diagnóstico Estratégico Generado!")
                    st.markdown(diagnostico)
                    
                    # Botón PDF
                    pdf_bytes = create_dark_pdf(nombre, empresa, region, diagnostico)
                    st.download_button(
                        label="📥 Descargar Reporte en Modo Oscuro (PDF)",
                        data=pdf_bytes,
                        file_name=f"Reporte_RedInnovacion_{empresa}.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("Error en la conexión con la IA.")
else:
    st.error("Configura la API KEY en los Secrets.")
