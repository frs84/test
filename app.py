import streamlit as st
import openai

# Récupération de la clé API depuis les secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("💬 Test ChatGPT avec Streamlit Cloud")

user_input = st.text_input("Pose une question à ChatGPT :")

if user_input:
    with st.spinner("ChatGPT réfléchit..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ou gpt-4 si tu y as accès
            messages=[{"role": "user", "content": user_input}]
        )
        message = response.choices[0].message.content.strip()
        st.success("Réponse de ChatGPT :")
        st.write(message)
