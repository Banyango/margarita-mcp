from margarita.parser import Node
from pydantic import BaseModel


class PromptModel(BaseModel):
    name: str | None
    description: str | None
    metadata: dict[str, str]
    nodes: list[Node]
    arguments: dict[str, str]
    file_name: str | None = None


class RenderedPromptModel(BaseModel):
    prompt: str
