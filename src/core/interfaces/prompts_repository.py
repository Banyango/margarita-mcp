from abc import ABC, abstractmethod

from wireup import abstract

from core.prompts.models import PromptModel


@abstract
class PromptsRepository(ABC):
    @abstractmethod
    def load(self) -> None:
        """Load prompts from the data source"""

    @abstractmethod
    def list_prompts(self) -> list[PromptModel]:
        """List all prompts"""

    @abstractmethod
    def get_prompt_by_name(self, name: str) -> PromptModel | None:
        """Get a prompt by its name

        Args:
            name (str): The name of the prompt to retrieve.

        Returns:
            PromptModel | None: The prompt model if found, otherwise None.
        """
