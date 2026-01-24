import json
import uuid
from typing import List

from fastapi import APIRouter
import dataclasses

from loguru import logger
from starlette.requests import Request
from starlette.responses import Response
from wireup import Injected

from app.v1.json_rpc.responses.get_prompt import (
    MessageResponse,
    MessageContentResponse,
    GetPromptResponse,
)
from app.v1.json_rpc.responses.json_rpc import JsonRpcResponse
from app.v1.json_rpc.responses.list_prompts import (
    PromptResource,
    ListPromptsResponse,
    PromptArgumentResource,
)
from core.interfaces.prompts_repository import PromptsRepository
from core.mcp.interfaces.session_store import SessionStore
from core.mcp.operations.initialize_operation import InitializeOperation
from core.prompts.models import PromptModel
from core.prompts.operations.render_prompt_operation import RenderPromptOperation
from core.prompts.renderer import PromptRenderer
from core.prompts.queries import PromptQueries

router = APIRouter()


@router.post("/handle")
async def prompts_jsonrpc(
    request: Request,
    response: Response,
    prompt_repository: Injected[PromptsRepository],
    prompt_renderer: Injected[PromptRenderer],
    session_store: Injected[SessionStore],
):
    body = await request.body()
    request_json = json.loads(body)

    if request_json["method"] == "initialize":
        session_id = str(uuid.uuid4())

        initialize_operation = InitializeOperation(session_store=session_store)

        model = await initialize_operation.execute_async(
            session_id, request_json["params"]["clientInfo"]["name"]
        )
        result = dataclasses.asdict(model)
        resp = JsonRpcResponse(result=result, id=request_json["id"], jsonrpc="2.0")

        response.headers["Mcp-Session-Id"] = session_id

        return resp.model_dump(exclude_none=True)
    elif request_json["method"] == "notifications/initialized":
        return Response(status_code=202)
    elif request_json["method"] == "prompts/list":
        operation = PromptQueries(
            repository=prompt_repository,
            prompt_renderer=prompt_renderer,
            session_store=session_store,
        )
        try:
            # session_id = request.headers.get("Mcp-Session-Id")
            prompts: List[PromptModel] = operation.list_prompts()
            prompt_resources: List[PromptResource] = []
            for prompt in prompts:
                prompt_resources.append(
                    PromptResource(
                        name=prompt.name or "",
                        title=prompt.file_name or "",
                        description=prompt.description or "",
                        arguments=[
                            PromptArgumentResource(
                                name=arg,
                                description="",
                                required=True,
                            )
                            for arg in list(prompt.arguments.keys())
                        ],
                    )
                )

            list_resp = ListPromptsResponse(
                prompts=prompt_resources, next_cursor="next_cursor"
            ).model_dump(exclude_none=True)
            resp = JsonRpcResponse(
                result=list_resp, error=None, id=request_json["id"], jsonrpc="2.0"
            )
            return resp.model_dump(exclude_none=True)
        except ValueError as e:
            logger.error(f"Error retrieving prompt: {e}")
            return JsonRpcResponse(
                error={"code": -32000, "message": "Session is invalid or expired"},
                id=request_json["id"],
                jsonrpc="2.0",
            )
    elif request_json["method"] == "prompts/get":
        try:
            session_id = request.headers.get("Mcp-Session-Id")

            operation = RenderPromptOperation(
                repository=prompt_repository,
                prompt_renderer=prompt_renderer,
                session_store=session_store,
            )

            model = await operation.execute_async(
                prompt_name=request_json["params"]["name"],
                session_id=session_id,
                arguments=request_json["params"]["arguments"],
            )
            if model is None:
                error_obj = {"code": -32004, "message": "Prompt not found"}
                resp = JsonRpcResponse(
                    error=error_obj, id=request_json["id"], jsonrpc="2.0"
                )
                return resp.model_dump(exclude_none=True)

            prompt_resources: List[MessageResponse] = [
                MessageResponse(
                    role="user",
                    content=MessageContentResponse(text=model.prompt, type="text"),
                )
            ]

            result = GetPromptResponse(messages=prompt_resources, description="")

            return JsonRpcResponse(
                result=result.model_dump(exclude_none=True),
                error=None,
                id=request_json["id"],
                jsonrpc="2.0",
            ).model_dump(exclude_none=True)
        except ValueError as e:
            logger.error(f"Error retrieving prompt: {e}")
            return JsonRpcResponse(
                error={"code": -32000, "message": "Session is invalid or expired"},
                id=request_json["id"],
                jsonrpc="2.0",
            )

    # For method not found we MUST return an error object and NOT include `result` per JSON-RPC 2.0
    error_obj = {"code": -32601, "message": "Method not found"}
    resp = JsonRpcResponse(error=error_obj, id=request_json["id"], jsonrpc="2.0")
    return resp.model_dump(exclude_none=True)
