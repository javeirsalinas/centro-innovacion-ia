import streamlit as st
import requests
import json
from fpdf import FPDF
import datetime

# 1. Configuración de Marca y Estética Neo-Light (CORREGIDA PARA LEGIBILIDAD)
st.set_page_config(page_title="RedInnovacion.pe | Mentoría Agéntica", page_icon="💡", layout="wide")

st.markdown("""
    <style>
    /* Fondo General Claro */
    .stApp {
        background-color: #FFFFFF;
    }
    /* Título con Degradado de Élite */
    .main-title {
        background: linear-gradient(90deg, #0E8388, #2E4F4F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .hero-subtitle {
        color: #2D3436; /* Gris carbón para máxima legibilidad */
        font-size: 22px;
        text-align: center;
        margin-bottom: 40px;
        font-weight: 500;
    }
    /* Tarjetas con Texto Gris Oscuro */
    .feature-card {
        background: #FDFDFD;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #E9ECEF;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        color: #2D3436; /* Texto Gris Oscuro */
    }
    .feature-card h3 {
        margin-bottom: 10px;
    }
    .feature-card b {
        color: #0E8388; /* Resalte en Esmeralda */
        font-size: 18px;
    }
    .section-header {
        color: #ffffff;
        background: linear-gradient(90deg, #0E8388, #2E4F4F);
        padding: 15px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        margin-top: 30px;
    }
    /* Labels del formulario en Gris Oscuro */
    label {
        color: #2D3436 !important;
        font-weight: 600 !important;
    }
    /* Botón Principal */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0E8388, #2E4F4F);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 18px;
        border-radius: 50px;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Clase PDF "Eco-Dark" (Mantenemos la intención ecológica)
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
        self.cell(0, 10, "Eco-Friendly Mode: Diseñado para lectura digital. Evite imprimir.", align='C')

def create_dark_pdf(nombre, empresa, region, resultado):
    pdf = DarkPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, txt="DIAGNOSTICO AGENTICO", ln=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(14, 131, 136)
    pdf.cell(0, 8, txt=f"PROYECTO: {empresa.upper()}", ln=True)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 8, txt=f"EMPRENDEDOR: {nombre} | REGION: {region}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(240, 240, 240)
    clean_text = resultado.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, txt=clean_text)
    return pdf.output(dest='S').encode('latin-1')

# --- CARATULA NEO-LIGHT CORREGIDA ---
st.markdown('<p class="main-title">RedInnovacion.pe</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Despierta el ADN de tu negocio con Mentoría Agéntica 2026</p>', unsafe_allow_html=True)

col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.markdown("""<div class="feature-card"><h3>🧠</h3><b>IA Agéntica</b><br>Un cerebro digital que audita proactivamente tu Canvas para desbloquear insights estratégicos.</div>""", unsafe_allow_html=True)
with col_f2:
    st.markdown("""<div class="feature-card"><h3>🇵🇪</h3><b>Contexto Peruano</b><br>Estrategias adaptadas a la realidad de cada región del Perú y sus mercados.</div>""", unsafe_allow_html=True)
with col_f3:
    st.markdown("""<div class="feature-card"><h3>♻️</h3><b>Eco-Vision</b><br>Reportes digitales y mentoría diseñados para proteger el medio ambiente.</div>""", unsafe_allow_html=True)

st.divider()

# --- FORMULARIO ---
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    st.markdown('<p class="section-header">🚀 INICIA TU TRANSFORMACIÓN</p>', unsafe_allow_html=True)
    
    with st.form("form_v5"):
        st.subheader("📋 Datos del Emprendedor")
        c1, c2, c3 = st.columns(3)
        nombre = c1.text_input("Nombre Completo")
        empresa = c2.text_input("Nombre del Emprendimiento")
        region = c3.selectbox("Región", ["Amazonas", "Ancash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca", "Callao", "Cusco", "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad", "Lambayeque", "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco", "Piura", "Puno", "San Martín", "Tacna", "Tumbes", "Ucayali"])
        
        e_col, w_col = st.columns(2)
        email = e_col.text_input("Correo Electrónico")
        whatsapp = w_col.text_input("WhatsApp")

        st.markdown("### 📊 Business Model Canvas")
        propuesta = st.text_area("1. Propuesta de Valor", height=100)
        
        col_a, col_b = st.columns(2)
        segmentos = col_a.text_area("2. Segmentos de Clientes")
        canales = col_b.text_area("3. Canales")
        relaciones = col_a.text_area("4. Relación con Clientes")
        ingresos = col_b.text_area("5. Fuentes de Ingresos")
        
        col_c, col_d = st.columns(2)
        recursos = col_c.text_area("6. Recursos Clave")
        actividades = col_d.text_area("7. Actividades Clave")
        socios = col_c.text_area("8. Socios Clave")
        costos = col_d.text_area("9. Estructura de Costos")

        enviar = st.form_submit_button("🔥 ACTIVAR EL AGENTE DE INNOVACIÓN")

    if enviar:
        if nombre and propuesta and email:
            with st.spinner("🚀 Consultando con la Red Agéntica..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
                prompt = f"Actúa como el Agente Senior de RedInnovacion.pe. Analiza el BMC de {empresa} en {region}. Usuario: {nombre}. Contexto: {propuesta}, {segmentos}, {canales}, {ingresos}, {costos}. Genera un reporte futurista de max 600 palabras."
                
                try:
                    resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                    if resp.status_code == 200:
                        diagnostico = resp.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success(f"¡Análisis Completado, {nombre}!")
                        st.markdown(diagnostico)
                        
                        pdf_data = create_dark_pdf(nombre, empresa, region, diagnostico)
                        st.download_button(
                            label="📥 DESCARGAR REPORTE AGÉNTICO (PDF ECO-DARK)",
                            data=pdf_data,
                            file_name=f"Reporte_{empresa}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error("Error en el Agente de IA.")
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.error("Configura la API KEY en los Secrets.")

st.sidebar.markdown("---")
st.sidebar.write("**RedInnovacion.pe**")
st.sidebar.write("Innovación para el Perú.")
