import time
from typing import Dict

from pydantic.v1 import BaseSettings
from wireup import service
from dataclasses import dataclass

from core.mcp.interfaces.session_store import SessionStore
from core.mcp.models import MCPSessionModel


class SessionConfig(BaseSettings):
    session_time_to_live: float = 120.0  # seconds


@service
def get_session_config() -> SessionConfig:
    return SessionConfig()


@dataclass
class Data:
    data: MCPSessionModel
    expiration: float

    def is_expired(self) -> bool:
        return time.time() > self.expiration


@service
class InMemorySessionStore(SessionStore):
    def __init__(self, session_config: SessionConfig):
        """
        In-memory session store.

        Args:
            session_config (SessionConfig): Configuration for session management.
        """
        self.data: Dict[str, Data] = {}
        self.expiration_time = session_config.session_time_to_live

    async def get(self, session_id: str) -> MCPSessionModel | None:
        """
        Retrieves session data by session ID.

        Args:
            session_id (str): The ID of the session to retrieve.
        """
        if session_id not in self.data:
            return None

        if self.data[session_id].is_expired():
            del self.data[session_id]
            return None

        return self.data[session_id].data

    async def set(self, session_id: str, data: MCPSessionModel) -> None:
        """
        Sets session data for a given session ID.

        Args:
            session_id (str): The ID of the session to set.
            data (dict): The session data to store.
        """
        expiration = time.time() + self.expiration_time
        self.data[session_id] = Data(data=data, expiration=expiration)

    async def delete(self, session_id: str) -> None:
        """
        Deletes session data by session ID.

        Args:
            session_id (str): The ID of the session to delete.
        """
        if session_id in self.data:
            del self.data[session_id]
