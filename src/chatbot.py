import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

load_dotenv()

llm=ChatGroq(model="openai/gpt-oss-120b",api_key=os.environ["GROQ_API_KEY"])

parser=StrOutputParser()

def run_chatbot():
    if "store" not in st.session_state:
        st.session_state.store={}

    def get_session_history(session_id: str):
        if session_id not in st.session_state.store:
            st.session_state.store[session_id]=InMemoryChatMessageHistory()
        return st.session_state.store[session_id]

    prompt=ChatPromptTemplate.from_messages([
        ("system","You are an helpful Assistant"),
        ("placeholder", "{history}"),
        ("human","{input}")
    ])

    chain=prompt| llm | parser 

    chain_with_memory=RunnableWithMessageHistory(
        chain,
        get_session_history=get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )

    session_id="default"

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input:=st.chat_input("Search here..."):

        st.session_state.messages.append({
            "role":"user",
            "content":user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        response=chain_with_memory.invoke(
            {"input":user_input},
            config={"configurable":{"session_id":session_id}}
        )

        ai_text=response

        st.session_state.messages.append({
            "role":"assistant",
            "content":ai_text
        })

        with st.chat_message("assistant"):
            st.markdown(ai_text)

