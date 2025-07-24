import streamlit as st
from openai import OpenAI
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
                st.subheader("Benvenuta Veronica")
                st.session_state.checked = True
def app():
    if not st.session_state.get("checked",False):
        login()

app()

# Récupération de la clé API depuis les secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:= st.text_input("Ton message :"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

# Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

