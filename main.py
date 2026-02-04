import sys
from prompt_toolkit import prompt

def get_prompt():
    user_prompt = prompt("> ")
    print(user_prompt)


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
