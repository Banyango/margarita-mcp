from pathlib import Path

from margarita.parser import Node
from margarita.renderer import Renderer
from wireup import service

from core.mcp.interfaces.session_store import SessionStore
from core.mcp.models import MCPSessionModel
from core.prompts.config import PromptSettings
from core.prompts.models import RenderedPromptModel


@service
class PromptRenderer:
    def __init__(self, session_store: SessionStore, prompt_settings: PromptSettings):
        self.session_store = session_store
        self.prompt_settings = prompt_settings

    async def render_prompt(
        self, session_id: str, arguments: dict[str, str], prompt_template: list[Node]
    ) -> RenderedPromptModel:
        """Render a list of prompt templates using the session context.

        Args:
            session_id (str): The ID of the MCP session to retrieve context from.
            arguments (dict[str, str]): The arguments to use for rendering the prompt.
            prompt_template (list[Node]): A list of prompt templates, each represented as a list of AST nodes.
        """
        session = await self.session_store.get(session_id)

        if session is None:
            session = MCPSessionModel(client_name="", context={})

        path = Path(self.prompt_settings.prompt_storage_path)

        renderer = Renderer(context={**session.context, **arguments}, base_path=path)

        return RenderedPromptModel(prompt=renderer.render(prompt_template))
