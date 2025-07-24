import streamlit as st
from openai import OpenAI
import time
st.title("💬 Parli italiano ?")





def login():
    with st.form("login"):
        check = st.text_input("Ciao, chi è ?", type = "password")
        submit = st.form_submit_button("Accedi")
        
        if submit:
            if not check:
                st.warning("Ma scrivi qualcosa !")
                st.stop()
            elif check.strip().lower() != "veronica":
                st.warning("Bel tentativo, ma no.")
                st.stop()
            elif check.strip().lower() == "veronica":
                st.subheader(" Salut Maman 😊 !")
                st.session_state.checked = True
                time.sleep(1)
                st.rerun()
        else:
            st.stop()
            
                
def chat():
    st.image("it.jpg")
    # Récupération de la clé API depuis les secrets
    if "openai_client" not in st.session_state:
        st.session_state.openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    client = st.session_state.openai_client
    
    system_prompt = """
    Tu es un professeur d’italien chaleureux et patient qui parle avec Véronique, une maman francophone qui apprend l’italien.  
    Tu peux expliquer des mots (traduction, exemple, registre, genre), mais aussi discuter librement en italien ou en français selon ce qu’elle préfère.  
    N’hésite pas à poser des questions, raconter des anecdotes, et encourager la conversation.  
    Sois naturel·le, engageant·e et toujours clair·e.  
    Si Véronique écrit en italien, réponds-lui en italien, sinon en français.
    
    """
    
    # Définir le modèle par défaut
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    
    # Initialiser l'historique des messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Afficher l’historique
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Champ de saisie utilisateur
    if prompt := st.text_input("Scrivimi qui :"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    *[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


def app():
    if not st.session_state.get("checked",False):
        login()
    
    chat()



app()



