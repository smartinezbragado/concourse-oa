from cacheables import cacheable
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

@cacheable
def get_embeddings(input: str) -> list[float]:
    """Returns the OpenAI embeddings of a given text"""
    response = client.embeddings.create(
        input=input,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


def get_llm_structured_output(system_prompt: str, user_prompt: str, output_schema: BaseModel) -> dict:
    """
    Generates a structured output from a llm based on the provided prompts and schema.

    This function interacts with the OpenAI client to parse a completion using a specified model.
    It sends a system prompt and a user prompt to the model, and expects the response to be formatted
    according to the given output schema. The function returns the parsed message from the model's response.

    Parameters:
        system_prompt (str): The prompt that sets the context or role for the language model.
        user_prompt (str): The prompt containing the user's query or input.
        output_schema (BaseModel): The schema that defines the expected structure of the model's response.

    Returns:
        dict: The structured output parsed from the model's response.
    """
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=output_schema,
    )

    event = completion.choices[0].message.parsed
    return event