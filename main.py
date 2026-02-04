import sys
import os
from prompt_toolkit import prompt
from openai import OpenAI
from rich.spinner import Spinner
from rich.live import Live
from rich import print

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_response(user_prompt):
    with Live(Spinner("dots", text="asking openai..."), transient=True):
        return client.responses.create(
            model="gpt-5-mini",
            instructions="",  # <- Give your agent personality
            input=user_prompt,
        )


def get_prompt():
    user_prompt = prompt("> ")
    bot_response = get_response(user_prompt)
    print(bot_response.output_text)


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
