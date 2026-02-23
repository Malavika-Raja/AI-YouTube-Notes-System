import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def summarize_chunk(chunk_text: str, model:str = "gpt-4o") -> str:
    """
    Generate strutured technical notes from a single chunk
    """
    system_prompt="""
    You are a technical documentation analyst.
    Your task is to convert raw transcript text into structered technical notes.

    Rules:
    - Generate a clear section heading based on topic.
    - Use markdown format
    - use bullet points
    - preserve technical terminology
    - avoid repitition
    - avoid filler language
    - be precise and structered
    """

    user_prompt =f"""
    Convert the following transcript section into structered notes:
    {chunk_text}
    """

    response = client.chat.completions.create(
        model = model,
        messages = [
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt}
        ],
        temperature=0.5

    )

    return response.choices[0].message.content

def merge_summaries(chunk_summaries: list, model: str ="gpt-4o") ->  str:
    """
    Merge chunk-level summaries into a final structured document
    """

    combined_text ="\n\n".join(chunk_summaries)

    system_prompt = """
    You are an expert technical editor.

    Mereg the provided structured notes into a final cohesive document.

    Requirements:
    - Remove duplication
    - Organize logically
    - Generate dynami section headings where appropriate
    - Include a Technical Breakdown section
    - Include key takeaways
    - Use markdown format
    - Ensure professional documentation style.

    """

    user_prompt = f"""
    Here are the structered notes from different sections of a video:
    {combined_text}
    Generate the final structered technical notes.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt}
        ],
        temperature=0.3,
        stream=True
    )
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content


