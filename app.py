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
    
    if st.button("Iniciar Auditoría con IA"):
        if nombre and proyecto and descripcion:
            with st.spinner("El Panel de Expertos está debatiendo..."):
                # Configurar la IA (Gemini)
                # Nota: En la nube usaremos st.secrets, por ahora lee de .env si es local
                api_key = st.secrets.get("GOOGLE_API_KEY") if "GOOGLE_API_KEY" in st.secrets else None
                
                if api_key:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"""
                    Actúa como un Mentor Senior y Emprendedor Serial. 
                    Analiza el proyecto {proyecto} de {nombre}.
                    Descripción: {descripcion}
                    Dame 3 consejos críticos y una hoja de ruta de 3 pasos.
                    Tono: Empático pero directo.
                    """
                    
                    respuesta = model.generate_content(prompt)
                    st.success(f"¡Bienvenido al Centro, {nombre}!")
                    st.markdown(respuesta.text)
                else:
                    st.error("Falta la API Key de Google. Por favor, configúrala.")
        else:
            st.warning("Por favor, completa todos los campos.")