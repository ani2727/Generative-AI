import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Hey, you are a helpful assistant. Respond to the questions asked"),
        ("user", "Question:{Question}") 
    ],
)

# Streamlit framework
st.title("Langchain using Ollama Gemma Model")
text_input = st.text_input("How can I help you Anil????")

# Ollama Gemma model
llm = Ollama(model="gemma2:2b")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if text_input:
    st.write(chain.invoke({"Question": text_input})) 
