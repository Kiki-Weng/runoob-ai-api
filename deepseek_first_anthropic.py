import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/anthropic"
)

response = client.messages.create(
    model="deepseek-flash",
    max_tokens=512,
    messages=[
        {
            "role":"user",
            "content":"请用一句话介绍Python。"
        }
    ]
)

for block in response.content:
    if block.type == "text":
        print(block.text)