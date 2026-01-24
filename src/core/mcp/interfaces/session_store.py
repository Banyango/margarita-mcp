from abc import ABC

from wireup import abstract

from core.mcp.models import MCPSessionModel


@abstract
class SessionStore(ABC):
    async def get(self, session_id: str) -> MCPSessionModel | None:
        pass

    async def set(self, session_id: str, data: MCPSessionModel) -> None:
        pass

    async def delete(self, session_id: str) -> None:
        pass
