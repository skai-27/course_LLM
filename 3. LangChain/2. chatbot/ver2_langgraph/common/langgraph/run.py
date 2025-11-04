######################################
# 환경변수 등록 
######################################
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import time
from .graph import create_graph


def response_of_llm(question:str):
    prompts = [] 
    for msg in st.session_state.messages:
      prompts.append(tuple(msg.values()))
    
    # 사용자의 메세지 입력 프론프트
    prompts += [("user", "{user_input}")] 
    chat_prompt = ChatPromptTemplate.from_messages(prompts)

    chain = chat_prompt | create_graph() | StrOutputParser()
    
    for token in chain.stream({"user_input": question}, stream_mode="values"):
        # token이 dict일 수도 있으므로, 문자열만 yield
        if isinstance(token, dict):
            token = token.get("output", str(token))
        yield token
        time.sleep(0.05)

