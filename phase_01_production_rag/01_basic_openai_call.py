"""Step 1: just call the OpenAI API. No RAG yet -- we build up from here."""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def ask(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question}],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    answer = ask("What is Retrieval-Augmented Generation, in one sentence?")
    print(answer)
