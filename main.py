import sys
import subprocess
import os
import json
from prompt_toolkit import prompt
from openai import OpenAI
from rich.spinner import Spinner
from rich.live import Live
from rich import print


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

context = []

tools = [
    {
        "type": "function",
        "name": "ping",
        "description": "ping some host on the internet",
        "parameters": {
            "type": "object",
            "properties": {
                "host": {"type": "string", "description": "hostname or IP"},
            },
            "required": ["host"],
        },
    },
]


def ping(host=""):
    try:
        result = subprocess.run(
            ["ping", "-c", "3", host],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
        )
        return result.stdout
    except Exception as e:
        return f"error: {e}"


def tool_call(item):
    if item.name == "ping":
        print(f"[i cyan]tool call[/i cyan]: ping {json.loads(item.arguments)['host']}")
        result = ping(**json.loads(item.arguments))
        return {
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": result,
        }


def handle_tools(response):
    old_size = len(context)
    for item in response.output:
        if item.type == "function_call":
            context.append(
                {
                    "type": "function_call",
                    "name": item.name,
                    "arguments": item.arguments,
                    "call_id": item.call_id,
                }
            )
            tool_call_output = tool_call(item)
            context.append(tool_call_output)

    has_new_context = len(context) != old_size

    return has_new_context


def get_response(context, loading_msg):
    with Live(Spinner("dots", text=loading_msg), transient=True):
        return client.responses.create(
            model="gpt-5-mini",
            instructions="You are an expert software developer. Be concise.",
            tools=tools,
            input=context,
        )


def get_prompt():
    user_prompt = prompt("> ")

    if user_prompt == "/context":
        print(context)
        return

    context.append({"role": "user", "content": user_prompt})

    bot_response = get_response(context, loading_msg='asking openai...')

    while handle_tools(bot_response):
        bot_response = get_response(context, loading_msg='sending response of toolcall to openai...')

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
