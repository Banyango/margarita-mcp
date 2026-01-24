from fastapi import APIRouter

from app.v1.json_rpc.routes.json_rpc import router as json_rpc_router


def build_mcp_v1_routes() -> APIRouter:
    """
    Builds the routes for the API v1.
    """
    router = APIRouter(prefix="/mcp/v1")

    # json_rpc
    router.include_router(json_rpc_router)

    return router
