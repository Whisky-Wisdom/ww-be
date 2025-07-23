from openai import OpenAI
import os
from openai.types.chat import ChatCompletionUserMessageParam



def ask_openrouter(prompt: str) -> str:

    key =  ""

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key,
    )

    messages: list[ChatCompletionUserMessageParam] = [
        {
            "role": "user",
            "content": prompt
        }
    ]


    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return completion.choices[0].message.content.strip()