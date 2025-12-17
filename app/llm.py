import os
from groq import Groq
import json
from app import tools

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current UTC time",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


async def stream_chat_completion(messages):
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta

        # Tool call detected
        if delta.tool_calls:
            tool_name = delta.tool_calls[0].function.name

            if tool_name == "get_current_time":
                tool_result = tools.get_current_time()
                yield f"\n[Tool:get_current_time] {tool_result}\n"

        # Normal token
        if delta.content:
            yield delta.content
