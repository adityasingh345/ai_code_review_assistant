import os
from dotenv import load_dotenv

load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL")  # Ollama / OpenAI
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1")
