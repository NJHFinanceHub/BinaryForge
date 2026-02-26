from pydantic import BaseModel, Field
from typing import Any


class SessionCreateResponse(BaseModel):
    session_id: str


class ChatMessage(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    session_id: str
    assistant_message: str
    extracted_requirements: dict[str, Any]
    ready_to_generate: bool


class GenerateResponse(BaseModel):
    project_id: str
    project_path: str
    verification: dict[str, Any]
    files: list[str]
