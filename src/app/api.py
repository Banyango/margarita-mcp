from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_client.decorator import contextmanager
from wireup.integration.fastapi import setup

from app.config import APIConfig
from app.container import container
from app.v1.routes import build_mcp_v1_routes
from core.interfaces.prompts_repository import PromptsRepository


def create_api(config: APIConfig) -> FastAPI:
    """Create the FastAPI application with MCP integration.

    Args:
        config (APIConfig): The API configuration.
    """
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        repository = await container.get(PromptsRepository)
        repository.load()
        yield

    app = FastAPI(
        title="margarita-mcp",
        docs_url="/api/docs",
        lifespan=lifespan,
    )

    app.include_router(build_mcp_v1_routes())

    setup(container, app)

    return app
