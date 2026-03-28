import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Centro de Innovación AI", layout="wide")

# Título principal
st.title("🚀 AgentLake: Centro de Innovación")
st.subheader("Mentoría inteligente para emprendedores")

# Formulario de Registro
with st.container():
    st.write("---")
    nombre = st.text_input("Nombre del Emprendedor")
    proyecto = st.text_input("Nombre del Proyecto (Ej: COLPA DE COPA)")
    descripcion = st.text_area("Cuéntanos sobre tu negocio (Productos, metas, desafíos)")
    
    # ... (mantén el inicio del código igual) ...

if st.button("Iniciar Auditoría con IA"):
    if nombre and proyecto and descripcion:
        with st.spinner("Conectando con el Panel de Expertos..."):
            api_key = st.secrets.get("GOOGLE_API_KEY")
            
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    # Usamos 'gemini-1.5-flash' pero con la ruta completa por seguridad
                    model = genai.GenerativeModel('models/gemini-1.5-flash')
                    
                    prompt = f"""
                    Actúa como un Mentor Senior y Emprendedor Serial. 
                    Analiza el proyecto {proyecto} de {nombre}.
                    Ubicación: Aguaytía, Ucayali.
                    Descripción: {descripcion}
                    
                    Instrucciones:
                    1. Valida el uso de insumos naturales de la selva.
                    2. Da 3 consejos críticos de negocio.
                    3. Sugiere un paso para mejorar la producción artesanal.
                    Tono: Empático, experto y motivador.
                    """
                    
                    respuesta = model.generate_content(prompt)
                    st.success(f"¡Análisis listo para {proyecto}!")
                    st.markdown(respuesta.text)
                except Exception as e:
                    st.error(f"Hubo un problema con la IA: {str(e)}")
            else:
                st.error("Error: No se encontró la llave de acceso (API Key).")
# ...
