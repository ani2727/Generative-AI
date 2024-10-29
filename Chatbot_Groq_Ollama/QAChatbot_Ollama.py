from langchain_community.llms import Ollama

import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

### langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot with OLLAMA"

### Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to the user queries"),
        ("user","question:{question}")
    ]
)


def generate_response(question, llm,temperature, max_tokens):
    llm = Ollama(model=llm)
    out_parser = StrOutputParser()
    chain = prompt | llm | out_parser

    answer = chain.invoke({'question': question})
    return answer


## Title of the app
st.title("Q&A Chatbot with OpenAI")

### Drop down to select various Open AI models
llm = st.sidebar.selectbox("Select an Open AI model",["gemma2:2b"])

temparature = st.sidebar.slider("Temparature",min_value=0.0,max_value=1.0,value=0.65)
max_tokens = st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

### Main Interface for user input

st.write("How can I help you?")
user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input,llm,temparature,max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")
