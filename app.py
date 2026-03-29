import streamlit as st
import requests
import json
from fpdf import FPDF
import datetime

# 1. Configuración de Marca y Estilo de la App
st.set_page_config(page_title="RedInnovacion.pe | Mentoría Agéntica", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #0E8388; font-size: 45px; font-weight: bold; text-align: center; margin-bottom: 10px; }
    .hero-text { color: #2E4F4F; font-size: 20px; text-align: center; margin-bottom: 30px; font-style: italic; }
    .section-header { color: #ffffff; background-color: #0E8388; padding: 12px; border-radius: 8px; font-size: 18px; font-weight: bold; margin-top: 25px; }
    .card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #0E8388; }
    </style>
    """, unsafe_allow_html=True)

# 2. Clase PDF Personalizada (Modo Oscuro)
class DarkPDF(FPDF):
    def header(self):
        self.set_fill_color(18, 18, 18) 
        self.rect(0, 0, 210, 297, 'F')
        self.set_font("Arial", 'B', 15)
        self.set_text_color(14, 131, 136)
        self.cell(0, 10, "RedInnovacion.pe", ln=True, align='L')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Página {self.page_no()} | Mentoría Agéntica 2026", align='C')

def create_dark_pdf(nombre, empresa, region, resultado):
    pdf = DarkPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, txt="DIAGNÓSTICO AGÉNTICO", ln=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(14, 131, 136)
    pdf.cell(0, 8, txt=f"PROYECTO: {empresa.upper()}", ln=True)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 8, txt=f"EMPRENDEDOR: {nombre} | REGIÓN: {region}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(240, 240, 240)
    clean_text = resultado.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, txt=clean_text)
    return pdf.output(dest='S').encode('latin-1')

# --- CARÁTULA VISUAL (HOME) ---
st.markdown('<p class="main-title">🚀 RedInnovacion.pe</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-text">"La evolución de la mentoría: Inteligencia Agéntica para el emprendedor peruano."</p>', unsafe_allow_html=True)



col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown('<div class="card"><b>⚡ Velocidad Agéntica</b><br>Diagnósticos precisos en segundos con Gemini 2.5 Flash-Lite.</div>', unsafe_allow_html=True)
with col_b:
    st.markdown('<div class="card"><b>📊 ADN del Negocio</b><br>Análisis profundo basado en los 9 bloques del Business Model Canvas.</div>', unsafe_allow_html=True)
with col_c:
    st.markdown('<div class="card"><b>🇵🇪 ADN Peruano</b><br>Mentoría contextualizada a la realidad de cada región del Perú.</div>', unsafe_allow_html=True)

st.divider()

# --- LÓGICA DE APLICACIÓN ---
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Usamos un expander para que el formulario no sea abrumador desde el inicio
    with st.expander("📝 INICIAR MI MENTORÍA AHORA (Completar Formulario)", expanded=False):
        with st.form("form_agentico_v3"):
            st.markdown('<p class="section-header">👤 REGISTRO DEL EMPRENDEDOR</p>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            nombre = c1.text_input("Nombre Completo")
            empresa = c2.text_input("Nombre del Emprendimiento")
            region = c3.selectbox("Región", ["Amazonas", "Ancash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca", "Callao", "Cusco", "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad", "Lambayeque", "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco", "Piura", "Puno", "San Martín", "Tacna", "Tumbes", "Ucayali"])
            
            email = st.text_input("Correo Electrónico")
            whatsapp = st.text_input("WhatsApp")

            st.markdown('<p class="section-header">📊 BUSINESS MODEL CANVAS</p>', unsafe_allow_html=True)
            propuesta = st.text_area("1. Propuesta de Valor", height=100)
            
            col_1, col_2 = st.columns(2)
            segmentos = col_1.text_area("2. Segmentos de Clientes")
            canales = col_2.text_area("3. Canales")
            relaciones = col_1.text_area("4. Relación con Clientes")
            ingresos = col_2.text_area("5. Fuentes de Ingreso")
            
            col_3, col_4 = st.columns(2)
            recursos = col_3.text_area("6. Recursos Clave")
            actividades = col_4.text_area("7. Actividades Clave")
            socios = col_3.text_area("8. Socios Clave")
            costos = col_4.text_area("9. Estructura de Costos")

            enviar = st.form_submit_button("🔥 ACTIVAR AGENTE DE MENTORÍA")

    if enviar:
        if nombre and propuesta and email:
            with st.spinner("🤖 El Agente está procesando tu visión estratégica..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
                prompt = f"Actúa como el Agente de RedInnovacion.pe. Analiza este BMC de {empresa} en {region}. Propuesta: {propuesta}. Responde con una Visión Agéntica, Alertas y Plan de Acción de 3 pasos. Máximo 600 palabras, sin negritas."
                
                try:
                    response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                    if response.status_code == 200:
                        diagnostico = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success("¡Análisis Agéntico Completado!")
                        st.markdown(diagnostico)
                        
                        pdf_bytes = create_dark_pdf(nombre, empresa, region, diagnostico)
                        st.download_button("📥 DESCARGAR REPORTE AGÉNTICO (PDF)", data=pdf_bytes, file_name=f"Reporte_{empresa}.pdf", mime="application/pdf")
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.error("Configura la API KEY en los Secrets.")

st.sidebar.write("### RedInnovacion.pe")
st.sidebar.write("Centro de Innovación Tecnológica 2026.")
