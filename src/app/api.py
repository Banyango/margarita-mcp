from fastapi import FastAPI
from wireup.integration.fastapi import setup

from app.config import APIConfig
from app.container import container
from app.v1.routes import build_mcp_v1_routes


def create_api(config: APIConfig) -> FastAPI:
    """Create the FastAPI application with MCP integration.

    Args:
        config (APIConfig): The API configuration.
    """

    app = FastAPI(
        title="margarita-mcp",
        docs_url="/api/docs",
    )

    app.include_router(build_mcp_v1_routes())

    setup(container, app)

    return app
