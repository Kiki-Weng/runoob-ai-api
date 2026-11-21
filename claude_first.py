from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=512,
    system=(
        "你是一个Python入门教学助手。"
        "使用自然、简洁的中文回答。"
        "尽量通过简单示例解释概念。"
    ),
    messages=[
        {
            "role":"user",
            "content":"请用三句话介绍Python。"
        }
    ]
)

for block in response.content:
    if block.type =="text":
        print(block.text)