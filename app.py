import streamlit as st
from src.chatbot import run_chatbot
from src.rag import run_rag

# Sidebar options
option = st.sidebar.selectbox(
    "Select Action",
    ["Home", "Chatbot","RAG"]
)

if option=="Home":
    st.title("This is the LLM App.")
    st.header("Welcome")

elif option=="Chatbot":
    st.set_page_config(page_title="Langchain Chatbot",layout="centered")
    st.title("💬 Chatbot with Memory ")
    run_chatbot()

elif option=="RAG":
    st.title("Document based Question Answers...")
    upload_file=st.file_uploader("Upload PDF",type="pdf")
    run_rag(upload_file)