import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")


async def stream_chat_completion(messages):
    """
    Async generator that yields tokens from Groq
    """
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
