import streamlit as st
import requests
import json

# Función para obtener tres ideas innovadoras y sus planes de implementación
def obtener_ideas_innovadoras(detalles_negocio):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"
    }
    
    prompt = f"""
    Eres un estratega de negocios creativo con experiencia en resolver problemas empresariales complejos. 
    Proporciona TRES ideas ORIGINALES y NOVEDOSAS para resolver el siguiente problema:
    
    - **Negocio:** {detalles_negocio['negocio']}
    - **Industria:** {detalles_negocio['industria']}
    - **Audiencia objetivo:** {detalles_negocio['audiencia']}
    - **Presupuesto:** {detalles_negocio['presupuesto']}
    - **Canales de marketing preferidos:** {detalles_negocio['canales']}
    - **Problema que afronta actualmente tu negocio:** {detalles_negocio['problema']}
    
    Para CADA idea, proporciona:
    1. Una descripción clara y detallada de la solución.
    2. Un plan paso a paso para implementarla.
    3. Los recursos necesarios (tiempo, dinero, personal, etc.).
    4. Los posibles resultados esperados.
    
    Asegúrate de que las ideas sean creativas, viables y alineadas con el presupuesto y los canales disponibles.
    """
    
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "deepseek-r1-distill-llama-70b",
        "temperature": 0.8,  # Un poco más creativo
        "max_completion_tokens": 4096,
        "top_p": 0.95,
        "stream": False
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.text}"

# Interfaz de usuario con Streamlit
st.title("Generador de Ideas Innovadoras")
st.write("Ingresa los detalles de tu negocio para recibir tres ideas originales y novedosas para resolver su problema.")

with st.expander("Detalles del Negocio"):
    negocio = st.text_input("Describe tu negocio")
    industria = st.text_input("Industria")
    audiencia = st.text_input("Audiencia objetivo")
    presupuesto = st.text_input("Presupuesto disponible")
    canales = st.text_input("Canales de marketing preferidos (separados por comas)")
    problema = st.text_area("¿Qué problema afronta actualmente tu negocio?")

if st.button("Generar Ideas Innovadoras"):
    if negocio.strip() and industria.strip() and audiencia.strip() and presupuesto.strip() and canales.strip() and problema.strip():
        with st.spinner("Generando ideas innovadoras..."):
            detalles_negocio = {
                "negocio": negocio,
                "industria": industria,
                "audiencia": audiencia,
                "presupuesto": presupuesto,
                "canales": canales,
                "problema": problema
            }
            ideas_innovadoras = obtener_ideas_innovadoras(detalles_negocio)
            
            st.subheader("Ideas Innovadoras Generadas:")
            st.markdown(ideas_innovadoras, unsafe_allow_html=True)  # Permite formato HTML si es necesario
    else:
        st.warning("Por favor, completa todos los campos.")
