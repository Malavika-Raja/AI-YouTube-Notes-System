import tiktoken
from typing import List

def count_tokens(text: str, model_name: str = "gpt-4o") -> int:
    """
    Count tokens in a text string using OpenAI tokenizer
    """
    encoding = tiktoken.encoding_for_model(model_name)
    # the function ensures we load the tokenizer used by the specific OpenAI model
    tokens = encoding.encode(text)
    # converts text to a list of numbers
    return len(tokens)

def chunk_text_by_tokens(text:str, max_tokens: int=2000, model_name: str ="gpt-4o") -> List[str]:
    """
    Splits the text into chunks so as to not exceed max token limit. 
    """
    sentences =  text.split(". ")
    # sentence-aware splitting so that model doesn't lose semantic continuity
    chunks=[]
    current_chunk=""

    for sentence in sentences:
        sentence = sentence.strip() + ". "
        # preserves the natural language flow
        temp_chunk = current_chunk +sentence
        token_count = count_tokens(temp_chunk, model_name)

        if token_count<=max_tokens:
            current_chunk = temp_chunk
        else:
            # if adding sentence would exceed the limit
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk=sentence
        
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


