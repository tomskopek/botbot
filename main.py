import sys
import os
from prompt_toolkit import prompt
from openai import OpenAI
from rich.spinner import Spinner
from rich.live import Live
from rich import print

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

context = []

def get_response(context):
    with Live(Spinner("dots", text="asking openai..."), transient=True):
        return client.responses.create(
            model="gpt-5-mini",
            instructions="You are an expert software developer. Be concise.",
            input=context,
        )


def get_prompt():
    user_prompt = prompt("> ")

    if user_prompt == "/context":
        print(context)
        return

    context.append({"role": "user", "content": user_prompt})

    bot_response = get_response(context)

    print(bot_response.output_text)

    context.append({"role": "assistant", "content": bot_response.output_text})


def main():
    print("Hi")
    try:
        while True:
            get_prompt()
    except KeyboardInterrupt:
        print("Bye")
        sys.exit(0)


if __name__ == "__main__":
    main()
