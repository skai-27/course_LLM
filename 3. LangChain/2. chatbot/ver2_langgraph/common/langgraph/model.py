from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import time

from .tools import search_weather, calculator, get_current_time

def get_model_with_tools(model:str="gpt-5-nano"):
    model = ChatOpenAI(
        model=model,
        reasoning_effort="high",        # 논리성 강화
    )
    return model.bind_tools([
        search_weather, calculator, get_current_time
    ])


