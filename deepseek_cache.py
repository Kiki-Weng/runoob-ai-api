import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

cache = {}

def ask_ai(question):
    if question in cache:
        print("命中本地缓存")
        return cache[question]

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        #thinking={"type": "disabled"}
    )

    answer = response.choices[0].message.content or ""

    cache[question] = answer

    return answer


question = "请解释什么是 JSON。"

print("第一次请求：")
print(ask_ai(question))

print("\n第二次请求：")
print(ask_ai(question))