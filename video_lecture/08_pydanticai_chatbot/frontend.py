import streamlit as st
from chat import JokeBot

def init_session_states():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "bot" not in st.session_state:
        st.session_state.bot = JokeBot()


def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input():
    if prompt := st.chat_input("Talk to the Ro Båt"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        bot_response = st.session_state.bot.chat(prompt).get("bot")
        response = f"Ro Båt: {bot_response}"

        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


def layout():
    st.markdown("# Chat with Ro Båt")
    st.write("Ro Båt is a funny robot that will joke with programming jokes. A real nerd")

    display_chat_messages()
    handle_user_input()



if __name__ == "__main__":
    init_session_states()
    layout()