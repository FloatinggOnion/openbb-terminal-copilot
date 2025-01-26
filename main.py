import os
import re
import json
from pathlib import Path
from typing import AsyncGenerator, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

from dotenv import load_dotenv
import google.generativeai as genai

from .prompt import SYSTEM_PROMPT
from .utils import create_message_stream, sanitize_message
from .models import AgentQueryRequest, Message


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

app = FastAPI(title="OpenBB Copilot API", description="API for OpenBB Copilot", version="0.1.0")

origins = [
    "http://localhost",
    "http://localhost:1420",
    "http://localhost:5050",
    "https://pro.openbb.dev",
    "https://pro.openbb.co",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/query")
async def query(request: AgentQueryRequest) -> EventSourceResponse:
    """
    Query the copilot with a user message.
    """
    
    chat_messages: List[Message] = []
    # print(chat_messages)
    for message in request.messages:
        # print(message.content)
        message_content = str(message.content)
        print(type(message_content))
        sanitized_message = sanitize_message(message_content)
        if message.role == "ai":
            chat_messages.append(
                sanitized_message
            )
            print(message)
        elif message.role == "human":
            chat_messages.append(
                sanitized_message
            )
            print(message)
            formatted_prompt = SYSTEM_PROMPT.format(context=message.content)
            model = genai.GenerativeModel("gemini-1.5-flash")
            result = model.generate_content(formatted_prompt)
            result = result.text
        else:
            raise ValueError(f"Invalid role: {message.role}")

    print(result)
    return EventSourceResponse(
        content=result,
        media_type="text/event-stream",
    )