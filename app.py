import streamlit as st
import requests
import json

# Función para obtener el plan de marketing
def obtener_plan_marketing(detalles_negocio):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"
    }
    
    prompt = f"""
    C. Contexto:
    Eres un estratega de marketing reconocido con más de dos décadas de experiencia en la creación de planes de marketing exitosos...
    
    Proporcione las características específicas del negocio para completar los detalles y generar un plan de marketing personalizado:
    
    - **Negocio:** {detalles_negocio['negocio']}
    - **Industria:** {detalles_negocio['industria']}
    - **Audiencia objetivo:** {detalles_negocio['audiencia']}
    - **Presupuesto:** {detalles_negocio['presupuesto']}
    - **Canales de marketing preferidos:** {detalles_negocio['canales']}
    - **Problema que afronta actualmente tu negocio:** {detalles_negocio['problema']}
    """
    
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "deepseek-r1-distill-llama-70b",
        "temperature": 0.6,
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
st.title("Generador de Plan de Marketing")

st.write("Ingresa los detalles de tu negocio para generar un plan de marketing personalizado.")

negocio = st.text_input("Describe tu negocio")
industria = st.text_input("Industria")
audiencia = st.text_input("Audiencia objetivo")
presupuesto = st.text_input("Presupuesto disponible")
canales = st.text_input("Canales de marketing preferidos")
problema = st.text_area("¿Qué problema afronta actualmente tu negocio?")

if st.button("Generar Plan de Marketing"):
    if negocio.strip() and industria.strip() and audiencia.strip() and presupuesto.strip() and canales.strip() and problema.strip():
        with st.spinner("Generando el plan de marketing..."):
            detalles_negocio = {
                "negocio": negocio,
                "industria": industria,
                "audiencia": audiencia,
                "presupuesto": presupuesto,
                "canales": canales,
                "problema": problema
            }
            plan_marketing = obtener_plan_marketing(detalles_negocio)
            st.subheader("Plan de Marketing Generado:")
            st.write(plan_marketing)
    else:
        st.warning("Por favor, completa todos los campos.")

st.markdown("[Corrección de textos en 24 horas](https://hablemosbien.org)")
