import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def summarize_chunk(messages: list, model:str = "gpt-4.1-mini") -> str:
    """
    Generate strutured technical notes from a single chunk
    """
    response = client.chat.completions.create(
        model = model,
        messages = messages,
        temperature=0.4

    )

    return response.choices[0].message.content

def merge_summaries(messages: list, model: str ="gpt-4.1-mini"):
    """
    Merge chunk-level summaries into a final structured document
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
        stream=True
    )
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


