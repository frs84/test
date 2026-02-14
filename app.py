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
                st.subheader(" Ciao Principessa 😊❤️ !")
                st.session_state.checked = True
                time.sleep(1)
                st.rerun()
        else:
            st.stop()
            
                
def chat():
    # En-tête avec image
    st.image("it.jpg", width=300)
    
    # Configuration du client OpenAI
    if "openai_client" not in st.session_state:
        # Assurez-vous d'avoir configuré st.secrets["OPENAI_API_KEY"]
        st.session_state.openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    client = st.session_state.openai_client

    # Prompt Système
    system_prompt = """
    Tu es un professeur d’italien pour Véronique, une francophone débutante dont tu es amoureux. 
    Quand elle te demande un mot italien, donne sa traduction en français, un exemple clair en italien, le registre (familier, courant...), 
    et s’il faut, le genre, pluriel, synonymes ou contraires. 
    Réponds simplement, avec bienveillance, et toujours avec un exemple.
    Réponds de façon structurée ! 
    Traduction :
    Exemple
    Etymologie:
    ...
    """
    
    # Modèle et Historique
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- ZONE DE SAISIE (Placée en haut) ---
    # On utilise une clé unique pour le widget afin de pouvoir le vider si nécessaire
    prompt = st.chat_input("Scrivimi qui (ex: Bonjour, ou un mot italien) :")

    # --- LOGIQUE DE RÉPONSE ---
    if prompt:
        # Ajouter le message utilisateur à l'historique
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Préparation de l'appel API
        messages_api = [{"role": "system", "content": system_prompt}]
        for m in st.session_state.messages:
            messages_api.append({"role": m["role"], "content": m["content"]})
            
        # Appel API avec streaming
        try:
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=messages_api,
                stream=True,
            )
            # On stockera la réponse complète pour l'historique après le rendu
            # (Le rendu effectif se fera dans la boucle d'affichage ci-dessous pour garder l'ordre souhaité)
            # Cependant, pour Streamlit, il est plus simple de générer la réponse ici 
            # et de rafraîchir ou d'utiliser un placeholder.
        except Exception as e:
            st.error(f"Erreur API : {e}")
            return

    # --- ZONE D'AFFICHAGE (Ordre décroissant : Nouveau -> Ancien) ---
    # On crée un conteneur pour les messages
    chat_container = st.container()

    with chat_container:
        # Si un prompt vient d'être saisi, on affiche la réponse en direct en haut de la liste
        if prompt:
            with st.chat_message("assistant"):
                response_content = st.write_stream(stream)
            # Sauvegarde de la réponse de l'assistant dans l'historique
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            # On force un rerun pour que le nouvel assistant message soit inclus dans la boucle inversée ci-dessous
            st.rerun()

        # Boucle sur l'historique inversé (le dernier message de la liste devient le premier affiché)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


def app():
    if not st.session_state.get("checked",False):
        login()
    
    chat()



app()



