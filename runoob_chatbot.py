import os
import json
from pathlib import Path
from datetime import datetime
from getpass import getpass

from openai import OpenAI, OpenAIError

MODEL = "deepseek-flash"

SYSTEM_PROMPT = (
    "你是一个面向编程初学者的AI教学助手"
    "使用自然、准确的中文回答问题。"
    "解释技术概念时尽量提供简单示例。"
    "不编造不存在的技术信息。"
)

class RunoobChatBot:

    def __init__(self):

        api_key = os.getenv("DEEPSEEK_API_KEY")

        if not api_key:
            api_key = getpass("请输入 DeepSeek API Key: ").strip()

        if not api_key:
            raise ValueError("没有提供API Key")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
            max_retries=2,
            timeout=60.0
        )


        self.messages=[]
        self.input_tokens = 0
        self.output_tokens = 0

    def chat(self, question):
        #保留最近六轮完整对话
        recent_history = self.messages[-12:]

        #构建请求的消息，由系统提示词和历史对话和当前问题组成
        request_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + recent_history + [
            {
                "role": "user",
                "content": question
            }
        ]

        response = self.client.chat.completions.create(
            model=MODEL,
            messages=request_messages,
        )

        answer = response.choices[0].message.content or ""

        # 成功后才保存本轮对话
        self.messages.append({
            "role": "user",
            "content": question
        })

        self.messages.append({
            "role": "assistant",
            "content": answer
        })

        if response.usage:
            self.input_tokens += response.usage.prompt_tokens
            self.output_tokens += response.usage.completion_tokens

        return answer

    def show_stats(self):

        print("\n=== 当前会话统计 ===")
        print("模型：", MODEL)
        print("对话轮数：", len(self.messages) // 2)
        print("输入 Token：", self.input_tokens)
        print("输出 Token：", self.output_tokens)
        print(
            "总 Token：",
            self.input_tokens + self.output_tokens
        )
        print("费用请以平台实际账单为准。\n")

    def save_history(self):

        output_dir = Path("conversations")
        output_dir.mkdir(exist_ok=True)

        filename = (
            "chat-"
            + datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            + ".json"
        )

        filepath = output_dir / filename

        data = {
            "model": MODEL,
            "saved_at": datetime.now().isoformat(),
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "messages": self.messages
        }

        filepath.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        print("已保存到：", filepath)     

    def clear(self):

        self.messages.clear()

        self.input_tokens = 0
        self.output_tokens = 0

        print("当前会话已清空。")

def print_help():

    print("""
可用命令：

/help   查看帮助
/stats  查看 Token 用量
/save   保存当前聊天记录
/clear  清空当前会话
/quit   退出程序

直接输入文字即可与 AI 对话。
""")

def main():

    print("RUNOOB AI 命令行聊天工具")

    bot = RunoobChatBot()

    print_help()

    while True:

        try:
            question = input("我们：").strip()

            if not question:
                continue

            if question == "/quit":
                print("再见！")
                break

            if question == "/help":
                print_help()
                continue

            if question == "/stats":
                bot.show_stats()
                continue

            if question == "/save":
                bot.save_history()
                continue

            if question == "/clear":
                bot.clear()
                continue

            print("AI：", end="", flush=True)

            answer = bot.chat(question)

            print(answer)
            print()

        except (KeyboardInterrupt, EOFError):
            print("\n程序已退出。")
            break

        except OpenAIError as error:
            print(
                "\nAPI 调用失败：",
                type(error).__name__
            )

        except Exception as error:
            print(
                "\n发生错误：",
                type(error).__name__
            )


if __name__ == "__main__":
    main()
