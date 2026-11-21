import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url = "https://api.deepseek.com"
)

stream = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {
            "role":"user",
            "content":"请介绍一下Python的主要特点。"
        }
    ],
    stream=True
)

print("AI:",end="",flush=True)

parts = []

for chunk in stream:
    if not chunk.choices:
        continue

    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)
        parts.append(content)

print("\n")

full_answer = "".join(parts)

print("本次回复字符数：", len(full_answer))
