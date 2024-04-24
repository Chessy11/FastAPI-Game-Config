from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os
import re

from app.utils.auth import get_current_active_user
from app.schemas.user_schema import UserOutSchema

load_dotenv()

router = APIRouter()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No OpenAI API key found in environment variables")

client = OpenAI(api_key=api_key)

class ChatRequest(BaseModel):
    prompt: str

def format_list_response(response_text):
    # Use regex to detect list pattern and format it
    list_pattern = re.compile(r'(\d+\..+?)(?=, \d+\.|$)')
    return list_pattern.sub(r'\1\n', response_text)

@router.post("/chat")
async def chat(chat_request: ChatRequest, current_user: UserOutSchema = Depends(get_current_active_user)):
    try:
        response_stream = client.completions.create(
            prompt=chat_request.prompt,
            model="gpt-3.5-turbo-instruct",
            top_p=0.5, 
            max_tokens=250,
            stream=True
        )

        response_text = ""
        for part in response_stream:
            response_text += part.choices[0].text or ""

        # Format the response if it is a list
        formatted_response = format_list_response(response_text)
        return {"response": formatted_response.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

