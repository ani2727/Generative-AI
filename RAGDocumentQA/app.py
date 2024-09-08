
import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from dotenv import load_dotenv
load_dotenv()

# ### Load the Groq API Key
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model_name = "Gemma-7b-It",groq_api_key = groq_api_key)

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Question:{input}
    """
)

def create_vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings= OllamaEmbeddings(model="gemma2:2b")
        st.session_state.loader = PyPDFDirectoryLoader("research_papers") ## Data Ingestion
        st.session_state.docs = st.session_state.loader.load() ## Document loading
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=300)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:3])
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)


st.title("RAG Document Q&A")

user_prompt = st.text_input("Enter your query from the research paper")


if st.button("Document Embedding"):
    create_vector_embedding()
    st.write("Vector Database is ready")

import time

if user_prompt:
    document_chain = create_stuff_documents_chain(llm,prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever,document_chain)

    start = time.process_time()
    response = retrieval_chain.invoke({"input":user_prompt})
    print(f"Response Time : {time.process_time()-start}")

    st.write(response)


    # ### With a streamlit expander

    # with st.expander("Document similarity Search"):
    #     for i,doc in enumerate(response['context']):
    #         st.write(doc.page_content)
    #         st.write('---------------')
