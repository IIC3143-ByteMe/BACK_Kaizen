from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

gemini_api = os.getenv("GEMINI_API")
gemini_client = genai.Client(api_key=gemini_api)


def get_gemini_model():
    return gemini_client
