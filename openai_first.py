from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model = "gpt-6-luna",
    input = "请用一句话介绍RUNOOB菜鸟教程。"
)

print("AI回复：")
print(response.output_text)