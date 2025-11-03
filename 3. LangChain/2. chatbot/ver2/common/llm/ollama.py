import enum

from langchain_ollama.llms import OllamaLLM

from .provider import Provider

class Ollama_LLMs(enum.Enum):
  gemma3 = (enum.auto(), "gemma3:4b") 
  diseases = (enum.auto(), "gemma3-diseases")

class Provider_Ollama(Provider):
  def __init__(self, choiced_llm) -> None:
    self.model = OllamaLLM(
        model=Ollama_LLMs[choiced_llm].value[1]
    )


