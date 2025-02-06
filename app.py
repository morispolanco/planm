import streamlit as st
import requests
import json
import os

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
    {detalles_negocio}
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

st.title("Generador de Plan de Marketing")

st.write("Ingresa las características de tu negocio para generar un plan de marketing personalizado.")

detalles_negocio = st.text_area("Describe tu negocio, industria, audiencia objetivo, presupuesto, canales de marketing preferidos, etc.")

if st.button("Generar Plan de Marketing"):
    if detalles_negocio.strip():
        with st.spinner("Generando el plan de marketing..."):
            plan_marketing = obtener_plan_marketing(detalles_negocio)
            st.subheader("Plan de Marketing Generado:")
            st.write(plan_marketing)
    else:
        st.warning("Por favor, proporciona detalles sobre tu negocio.")

st.markdown("[Corrección de textos en 24 horas](https://hablemosbien.org)")
