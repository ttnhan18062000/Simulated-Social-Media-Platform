import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load .env file
load_dotenv()

model = init_chat_model("gemini-2.0-flash-lite", model_provider="google_genai")
