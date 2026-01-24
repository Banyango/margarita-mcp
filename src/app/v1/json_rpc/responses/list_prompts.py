from typing import List

from pydantic import BaseModel


class PromptArgumentResource(BaseModel):
    name: str
    description: str
    required: bool

class PromptResource(BaseModel):
    name: str
    title: str
    description: str
    arguments: List[PromptArgumentResource]

class ListPromptsResponse(BaseModel):
    prompts: List[PromptResource]
    next_cursor: str | None
