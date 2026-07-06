import os
import shutil
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain

load_dotenv()

llm=ChatGroq(model="openai/gpt-oss-120b",api_key = os.environ["GROQ_API_KEY"])

parser=StrOutputParser()

def run_rag(upload_file):

    prompt=PromptTemplate.from_template(
        """
        Answer the following question based on the given context only.
        Please provide most accurate response based on the question.
        If answer is not present in the context just say i don't know.
        <context>
        {context}
        <context>
        Questions:{input}
        """
    )

   

    if upload_file is not None:
        with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as tmp:
            tmp.write(upload_file.read())
            temp_path=tmp.name

    @st.cache_resource
    def create_vector_store(documents,embeddings):
        return Chroma.from_documents(
            documents,
            embedding=embeddings
        )

    def vectore_store():
        if upload_file is None:
            return 

        if "vector_store" not in st.session_state:
            st.session_state.embeddings=embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            loader=PyPDFLoader(temp_path)
            documents=loader.load()

            splitter=RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            final_docs=splitter.split_documents(documents)

            st.session_state.vector_store=create_vector_store(final_docs,st.session_state.embeddings)

        return st.session_state.vector_store

    input_prompt=st.text_input("Enter your Question From Documents")


    if upload_file:
        vectore_store() 
        st.success("Chroma database is ready")
    
    if st.button("Search"):
    
        document_chain=create_stuff_documents_chain(llm,prompt)
        retriever=st.session_state.vector_store.as_retriever(search_type="mmr",search_kwargs={"k":2,"lambda_mult":0.5})
        retrieval_chain=create_retrieval_chain(retriever,document_chain)
        response=retrieval_chain.invoke({"input":input_prompt})
        st.markdown(response["answer"])
    
    if st.button("Rebuild Vector Store"):
        if "vector_store" in st.session_state:
                del st.session_state.vector_store
        
        # 2️⃣ Remove persistent Chroma DB
        if os.path.exists("./chroma_db"):
            shutil.rmtree("./chroma_db")
    
        # 3️⃣ Force clean rerun
        st.rerun()