import streamlit as st
import pandas as pd
from langchain_google_genai import GoogleGenerativeAI
from pandasai import SmartDataframe
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")


if not st.secrets["CASA_MODEL"] or not st.secrets["CASA_GOOGLE_API_KEY"]:
    raise Exception("Gemini model name or google api key is missing")

llm = GoogleGenerativeAI(model=st.secrets["CASA_MODEL"], google_api_key=st.secrets["CASA_GOOGLE_API_KEY"])

st.title("CASA - A prompt-driven home rent analysis tool for the residents of Nigeria")

data = pd.read_csv("datasets/homes_for_rent.csv")
df = SmartDataframe(data, config={"llm": llm})

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if type(message["content"]) is str and message["content"].endswith(".png"):
            st.image(message["content"])
        else:
            st.write(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = df.chat(prompt)
        if type(response) is str and response.endswith(".png"):
            st.image(response)
        else:
            st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})