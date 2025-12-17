import time

import ollama
from .constant import CHATBOT_ROLE, CHATBOT_MESSAGE


def response_from_llm(prompt, message_history=None, model_id="gemma3-diseases"):
    messages = [
        {
            CHATBOT_MESSAGE.role.name: CHATBOT_ROLE.assistant.name, 
            CHATBOT_MESSAGE.content.name: "You are a helpful assistant. You must answer in Korean.",
        }
    ]

    if isinstance(message_history, list):
        messages += message_history

    # 사용자 질문 추가
    messages.append(
        {
            CHATBOT_MESSAGE.role.name: CHATBOT_ROLE.user.name,
            CHATBOT_MESSAGE.content.name: prompt,
        },
    )

    streaming = ollama.chat(
        model=model_id,
        messages=messages,
        stream=True
    )

    # return streaming.choices[0].message.content
    for chunk in streaming:
        if chunk["message"]["content"] is not None:
            yield chunk["message"]["content"]
            time.sleep(0.05)


