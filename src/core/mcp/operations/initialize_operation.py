from typing import Dict
from dataclasses import dataclass


from core.mcp.interfaces.session_store import SessionStore
from core.mcp.models import MCPSessionModel


@dataclass
class CapabilitiesModel:
    listChanged: bool


@dataclass
class ServerInfoModel:
    name: str
    title: str
    version: str


@dataclass
class InitializationModel:
    protocolVersion: str
    capabilities: Dict[str, CapabilitiesModel]
    serverInfo: ServerInfoModel


class InitializeOperation:
    def __init__(self, session_store: SessionStore):
        self.session_store: SessionStore = session_store

    async def execute_async(
        self, session_id: str, client_name: str
    ) -> InitializationModel:
        await self.session_store.set(
            session_id, MCPSessionModel(client_name=client_name, context={})
        )

        capabilities = {
            "prompts": CapabilitiesModel(listChanged=True),
        }

        server_info = ServerInfoModel(
            name="Margarita MCP Server",
            title="Margarita MCP Server",
            version="1.0.0",
        )

        return InitializationModel(
            protocolVersion="2024-11-05",  # todo better version handling maybe this can be handled by the module v1?
            capabilities=capabilities,
            serverInfo=server_info,
        )
