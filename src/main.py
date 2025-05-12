from typing import Union
from fastapi import FastAPI
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
gemini_api = os.getenv("GEMINI_API")
gemini_client = genai.Client(api_key=gemini_api)

app = FastAPI()


@app.get("/")
def read_root():
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Explain how AI works in a few words",
    )
    return {"Hello": response.text}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
