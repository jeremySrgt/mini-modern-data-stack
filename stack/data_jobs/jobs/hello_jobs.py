import os
from dotenv import load_dotenv

load_dotenv()


def say_hello():
    # you can access env var and secrets that you defined in task definition like so:
    # os.getenv("DATAWAREHOUSE_DB")
    print("Hello Jobs !")
    return 0


if __name__ == "__main__":
    say_hello()
