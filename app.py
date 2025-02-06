import streamlit as st
import requests
import json
import os

def get_marketing_plan(business_details):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}"
    }
    
    prompt = f"""
    C. Context:
    You are a renowned marketing strategist with over two decades of experience in creating successful marketing plans...
    
    Please provide the specific business characteristics so I can fill in the blanks and create a tailored marketing plan:
    {business_details}
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

business_details = st.text_area("Describe tu negocio, industria, audiencia objetivo, presupuesto, canales de marketing preferidos, etc.")

if st.button("Generar Plan de Marketing"):
    if business_details.strip():
        with st.spinner("Generando el plan de marketing..."):
            marketing_plan = get_marketing_plan(business_details)
            st.subheader("Plan de Marketing Generado:")
            st.write(marketing_plan)
    else:
        st.warning("Por favor, proporciona detalles sobre tu negocio.")
