from dataclasses import dataclass


@dataclass
class MCPSessionModel:
    client_name: str
    context: dict[str, str]
