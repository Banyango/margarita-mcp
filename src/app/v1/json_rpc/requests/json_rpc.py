from pydantic import BaseModel


class PromptsJsonRpc(BaseModel):
    jsonrpc: str
    id: int | str | None
    method: str
    params: dict | None
