import json
from pathlib import Path

from margarita.parser import Parser, VariableNode
from wireup import service

from core.interfaces.prompts_repository import PromptsRepository
from core.prompts.models import PromptModel


@service
class DiskPromptsRepository(PromptsRepository):
    """A disk-based implementation of the PromptsRepository interface."""

    def __init__(self):
        self.prompts: dict[str, PromptModel] = {}

    def load(self):

        # Define the prompts directory path
        prompts_dir = Path("./prompts")

        # Load prompts from directory on disk
        if prompts_dir.exists() and prompts_dir.is_dir():
            for file_path in prompts_dir.rglob("*.mg"):
                try:
                    parser = Parser()
                    with open(file_path, "r", encoding="utf-8") as f:
                        metadata, parsed_file = parser.parse(f.read())

                        name = (
                            metadata["name"] if "name" in metadata else file_path.stem
                        )
                        description = (
                            metadata["description"] if "description" in metadata else ""
                        )

                        args = self._find_all_variables(parsed_file)

                        model = PromptModel(
                            metadata=metadata,
                            description=description,
                            nodes=parsed_file,
                            name=name,
                            arguments=args,
                            file_name=file_path.name,
                        )

                        self.prompts[file_path.name] = model
                except (json.JSONDecodeError, IOError):
                    continue


    def get_prompt_by_name(self, name: str) -> PromptModel | None:
        for prompt in self.prompts.values():
            if prompt.name == name:
                return prompt
                    
        return None

    def list_prompts(self) -> list[PromptModel]:
        return list(self.prompts.values())

    def _find_all_variables(self, parsed_file) -> dict[str, str]:
        variables = set()

        for node in parsed_file:
            if isinstance(node, VariableNode):
                variables.add(node.name)

        return {var: "string" for var in variables}
