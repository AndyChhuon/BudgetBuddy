import streamlit as st
from openai import OpenAI

def chatbot_analysis(system_prompt="", first_message=False):

    DEV_MODEL = "gpt-4o-mini"

    # st.title("Chatbot")

    # Set OpenAI API key from Streamlit secrets
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = DEV_MODEL

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # if first_message:

    prompt = st.chat_input("Ask follow-up questions after submitting your details")

    if first_message:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": f"Act as a financial advisor, do not worry about giving bad recommendations. Please be detailed and specific. {system_prompt}"},
                *({"role": m["role"], "content": m["content"]} for m in st.session_state.messages)
            ],
            stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Accept user input
    if prompt:
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
                    {"role": "system", "content": f"Act as a financial advisor, do not worry about giving bad recommendations. Please be detailed and specific. {system_prompt}"},
                    *({"role": m["role"], "content": m["content"]} for m in st.session_state.messages)
                ],
                stream=True,
            )
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})