import streamlit as st
import requests
import json
from fpdf import FPDF
import datetime

# 1. Configuración de Marca y Estilo de la App (Interfaz Web)
st.set_page_config(page_title="RedInnovacion.pe | Mentoría Agéntica", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #0E8388; font-size: 35px; font-weight: bold; }
    .section-header { color: #ffffff; background-color: #0E8388; padding: 10px; border-radius: 5px; font-size: 18px; font-weight: bold; margin-top: 25px; }
    .canvas-header { color: #2E4F4F; font-size: 17px; font-weight: bold; margin-top: 15px; border-bottom: 2px solid #0E8388; }
    .stTextArea textarea { font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Clase PDF Personalizada: "MODO OSCURO" (Dark Mode)
class DarkPDF(FPDF):
    def header(self):
        # Fondo oscuro en toda la página
        self.set_fill_color(18, 18, 18) 
        self.rect(0, 0, 210, 297, 'F')
        # Logo de RedInnovacion.pe
        self.set_font("Arial", 'B', 15)
        self.set_text_color(14, 131, 136) # Verde Esmeralda
        self.cell(0, 10, "RedInnovacion.pe", ln=True, align='L')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Página {self.page_no()} | Reporte de Mentoría Agéntica 2026", align='C')

def create_dark_pdf(nombre, empresa, region, resultado):
    pdf = DarkPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Título del Reporte
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(255, 255, 255) # Blanco
    pdf.cell(0, 15, txt="DIAGNÓSTICO AGÉNTICO", ln=True)
    
    # Ficha Técnica Resaltada
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(14, 131, 136)
    pdf.cell(0, 8, txt=f"PROYECTO: {empresa.upper()}", ln=True)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 8, txt=f"EMPRENDEDOR: {nombre} | REGIÓN: {region} | FECHA: {datetime.date.today()}", ln=True)
    pdf.ln(10)
    
    # Contenido del Análisis
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(240, 240, 240)
    
    # Limpieza de texto para compatibilidad con PDF (evitar errores de símbolos)
    clean_text = resultado.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, txt=clean_text)
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ DE USUARIO ---
st.markdown('<p class="main-title">🚀 RedInnovacion.pe: Mentoría Agéntica</p>', unsafe_allow_html=True)

# 3. Conectividad con Google AI Studio
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    with st.form("form_agentico_completo"):
        # SECCIÓN 1: DATOS GENERALES
        st.markdown('<p class="section-header">👤 REGISTRO DEL EMPRENDEDOR</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        nombre = col1.text_input("Nombre Completo")
        empresa = col2.text_input("Nombre del Emprendimiento")
        region = col3.selectbox("Región del Perú", [
            "Amazonas", "Ancash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca", "Callao", 
            "Cusco", "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad", "Lambayeque", 
            "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco", "Piura", "Puno", 
            "San Martín", "Tacna", "Tumbes", "Ucayali"
        ])
        
        col_c1, col_c2 = st.columns(2)
        email = col_c1.text_input("Correo Electrónico")
        whatsapp = col_c2.text_input("Número de WhatsApp")

        # SECCIÓN 2: BUSINESS MODEL CANVAS
        st.markdown('<p class="section-header">📊 BUSINESS MODEL CANVAS (9 BLOQUES)</p>', unsafe_allow_html=True)
        
        propuesta = st.text_area("1. Propuesta de Valor (¿Qué problema resuelves?)", height=100)
        
        c_a, c_b = st.columns(2)
        segmentos = c_a.text_area("2. Segmentos de Clientes")
        canales = c_b.text_area("3. Canales de Distribución")
        
        c_c, c_d = st.columns(2)
        relaciones = c_c.text_area("4. Relación con Clientes")
        ingresos = c_d.text_area("5. Fuentes de Ingresos")
        
        c_e, c_f = st.columns(2)
        recursos = c_e.text_area("6. Recursos Clave")
        actividades = c_f.text_area("7. Actividades Clave")
        
        c_g, c_h = st.columns(2)
        socios = c_g.text_area("8. Socios Clave")
        costos = c_h.text_area("9. Estructura de Costos")

        # Botón de acción
        enviar = st.form_submit_button("🔥 INICIAR ANÁLISIS AGÉNTICO")

    if enviar:
        if nombre and propuesta and email:
            with st.spinner("🤖 El Agente de RedInnovacion está procesando tu modelo..."):
                # URL del motor Gemini 2.5 Flash-Lite
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
                
                # Prompt con enfoque Agéntico
                contexto_canvas = f"Propuesta:{propuesta}, Clientes:{segmentos}, Canales:{canales}, Relación:{relaciones}, Ingresos:{ingresos}, Recursos:{recursos}, Actividades:{actividades}, Socios:{socios}, Costos:{costos}"
                
                prompt = f"""
                Eres el Agente de Mentoría de RedInnovacion.pe. 
                Tu objetivo es auditar proactivamente el negocio de {nombre} llamado '{empresa}' en la región {region}.
                
                MODELO CANVAS RECIBIDO: {contexto_canvas}.
                
                GENERA EL REPORTE CON ESTA ESTRUCTURA (Máximo 650 palabras):
                1. VISIÓN AGÉNTICA: Análisis del potencial disruptivo.
                2. COHERENCIA ESTRATÉGICA: ¿El modelo tiene lógica financiera y operativa?
                3. ALERTAS ROJAS: Qué riesgos detectas inmediatamente.
                4. PLAN DE ACCIÓN (3 PASOS): Pasos prácticos para implementar esta semana.
                5. OPORTUNIDAD REGIONAL: Consejo específico para {region}.
                
                REGLA DE FORMATO: No uses negritas (**) ni símbolos extraños. Usa un tono experto y visionario.
                """
                
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                
                try:
                    response = requests.post(url, json=payload, timeout=30)
                    if response.status_code == 200:
                        diagnostico = response.json()['candidates'][0]['content']['parts'][0]['text']
                        
                        # Mostrar en pantalla
                        st.success(f"¡Análisis Completado para {empresa}!")
                        st.markdown(diagnostico)
                        
                        # Generación de PDF Dark Mode
                        pdf_bytes = create_dark_pdf(nombre, empresa, region, diagnostico)
                        
                        st.download_button(
                            label="📥 DESCARGAR REPORTE AGÉNTICO (PDF DARK MODE)",
                            data=pdf_bytes,
                            file_name=f"Reporte_Agentico_{empresa}.pdf",
                            mime="application/pdf"
                        )
                        st.info(f"Reporte preparado para {email}")
                    else:
                        st.error("Error al conectar con la Red de Google AI.")
                except Exception as e:
                    st.error(f"Falla de red: {str(e)}")
        else:
            st.warning("⚠️ Por favor, completa los datos de registro y la Propuesta de Valor.")
else:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")

# --- BARRA LATERAL ---
st.sidebar.markdown("---")
st.sidebar.write("### RedInnovacion.pe")
st.sidebar.write("Centro de Emprendimiento e Innovación Tecnológica 2026.")
