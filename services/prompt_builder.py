def chunk_prompt(chunk_text:str)->list:
    """
    Return prompt messages for chunk summarization
    """
    system_prompt = """
    You are a technical documentation analyst.
    Convert transcript text into structered summary.
    
    Rules:
    - Generate a clear summary for this section
    - preservce technical terminology
    """

    user_prompt =f"""
    Convert the following transcript section into structured summary:
    {chunk_text}
    """

    return [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_prompt},
    ]

def merge_prompt(combined_text: str,
                 detail_level: str,
                 tone: str,
                 include_breakdown:bool,
                 max_sections: int) -> list:
    detail_instruction = {
        "Concise": """
        Produce a sharply condensed version of the content.

        Rules:
        - Maximum 3–5 major sections.
        - Each section must contain short, dense paragraphs.
        - Avoid excessive subheadings (no more than one level deep).
        - Eliminate repetition completely.
        - Summarize concepts instead of explaining step-by-step reasoning.
        - Focus on core insights, definitions, and conclusions only.
        - Keep the document compact and direct.
        """,
        "In-depth": """
        Produce a comprehensive and technically detailed document.

        Rules:
        - Expand concepts with reasoning, mechanisms, and explanations.
        - Clearly define technical terms where relevant.
        - Use structured subsections when necessary.
        - Include examples or clarifications if helpful.
        - Maintain logical progression between sections.
        - Do not compress ideas; prioritize clarity and completeness.
        """
    }[detail_level]

    tone_instruction ={
       "Professional": """
        Tone Guidelines:
        - Use precise, technical language.
        - Write in an objective, documentation-style manner.
        - Avoid conversational phrases.
        - Use declarative statements.
        - Focus on clarity, structure, and efficiency.
        """,

        "Academic": """
        Tone Guidelines:
        - Use formal academic language.
        - Present ideas analytically and methodically.
        - Use structured reasoning and logical transitions.
        - Maintain an impersonal, research-oriented voice.
        - Emphasize conceptual depth and theoretical framing.
        """,

        "Beginner Friendly": """
        Tone Guidelines:
        - Use simple, accessible language.
        - Define technical terms clearly.
        - Use analogies or simplified explanations where useful.
        - Avoid heavy jargon unless explained.
        - Maintain a supportive and instructional tone.
        """
    }[tone]

    breakdown_instruction = (
        "Include a dedicated 'Technical Breakdown' section."
        if include_breakdown else
        "Do not create a separate technical breakdown section unless necessary."
    )

    system_prompt = f"""
    You are an expert technical editor.SystemError

    Merge structured notes into a final cohesive document.

    Requirements:
    - Maximum {max_sections} major sections.
    - remove duplication
    - organize logically
    - avoid excessive subheadings
    - use clean markdown
    - ensure professional documentation style.
    - do not repeat ideas in two sections

    Follow the below instructions:

    {detail_instruction}
    {tone_instruction}
    {breakdown_instruction}
    """

    user_prompt = f"""
    Here are structured notes from different sections:

    {combined_text}

    Generate the final structured technical documentation.
    """

    return [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_prompt},
    ]