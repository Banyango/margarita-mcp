from core.interfaces.prompts_repository import PromptsRepository
from core.mcp.interfaces.session_store import SessionStore
from core.prompts.models import RenderedPromptModel
from core.prompts.renderer import PromptRenderer


class RenderPromptOperation:
    def __init__(
        self,
        repository: PromptsRepository,
        prompt_renderer: PromptRenderer,
        session_store: SessionStore,
    ):
        self.repository = repository
        self.prompt_renderer = prompt_renderer
        self.session_store = session_store

    async def execute_async(
        self, prompt_name: str, session_id: str, arguments: dict[str, str]
    ) -> RenderedPromptModel | None:
        """Render a prompt by name.

        Args:
            prompt_name (str): The name of the prompt.
            session_id (str): The MCP session ID to use for rendering the prompt.
            arguments (dict[str, str]): The arguments to use for rendering the prompt.
        """
        prompt = self.repository.get_prompt_by_name(prompt_name)

        if not prompt:
            raise ValueError(f"No prompts found for name: {prompt_name}")

        return await self.prompt_renderer.render_prompt(
            session_id=session_id, arguments=arguments, prompt_template=prompt.nodes
        )
