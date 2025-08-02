# llm/generate_post.py

import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, Part, GenerateContentConfig

# Load .env file
load_dotenv()


def generate_post(user_prompt: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in .env")

    client = genai.Client(api_key=api_key)

    # Define the model and prompt
    model = "models/gemini-2.0-flash-lite"
    contents = [
        Content(
            role="user",
            parts=[Part.from_text(text=user_prompt)],
        )
    ]

    # Optional: add generation config
    config = GenerateContentConfig(
        temperature=0.7,
        top_p=1.0,
        max_output_tokens=256,
    )

    # Generate the content
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )

    return response.text.strip()


if __name__ == "__main__":
    prompt = """
You are Lena, a quiet, introverted artist. Write a 1-2 sentence social media post
about feeling at peace with silence after a long day.
"""
    result = generate_post(prompt)
    print("Generated Post:\n", result)
