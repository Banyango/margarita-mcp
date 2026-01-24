from typing import Optional

from pydantic import BaseModel


class JsonRpcResponse(BaseModel):
    jsonrpc: str
    id: Optional[int | str] = None
    error: Optional[dict] = None
    result: Optional[dict] = None
