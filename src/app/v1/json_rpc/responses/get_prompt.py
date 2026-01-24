from typing import List

from pydantic import BaseModel


class MessageContentResponse(BaseModel):
    type: str
    text: str


class MessageResponse(BaseModel):
    role: str
    content: MessageContentResponse


class GetPromptResponse(BaseModel):
    messages: List[MessageResponse]
    description: str
