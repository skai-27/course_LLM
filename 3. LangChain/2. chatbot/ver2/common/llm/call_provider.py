import enum
import streamlit as st

from .groq import GROQ_LLMs, Provider_GROQ
from .openai import OpenAI_LLMs, Provider_OpenAI
from .ollama import Ollama_LLMs, Provider_Ollama

class PROVIDER_TYPE(enum.Enum):
  # 제공자명 = (인덱스, 호출함수, 사용가능한 모델 리스트)
  ollama = (enum.auto(), Provider_Ollama, Ollama_LLMs)
  groq = (enum.auto(), Provider_GROQ, GROQ_LLMs)
  openai = (enum.auto(), Provider_OpenAI, OpenAI_LLMs)


@st.cache_resource
def get_provider(choiced_provider, choiced_llm):
  return PROVIDER_TYPE[choiced_provider].value[1](choiced_llm)


