from langchain_tavily import TavilySearch
import streamlit as st 
from langchain_core.tools import tool

@st.cache_resource
def __get_tavily_search():
    return TavilySearch(
        max_results=3,
        topic="general",               # 또는 "news", "finance" 등
        include_answer=True,           # 답변 포함 여부
        include_raw_content=False,     # 원본 내용 포함 여부
        include_images=False,          # 이미지 포함 여부
        search_depth="basic",          # "basic" 또는 "advanced"
        include_domains=[
            "https://weather.daum.net/",
            "https://www.weatheri.co.kr/" 
        ],
        exclude_domains=None            # 필요하면 제외 도메인 지정 가능
    )

