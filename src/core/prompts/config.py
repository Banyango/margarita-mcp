from pydantic_settings import BaseSettings
from wireup import service


class PromptSettings(BaseSettings):
    prompt_storage_path: str = "prompts/"
    default_prompt_file_extension: str = ".marg"


@service
def prompt_settings_provider() -> PromptSettings:
    return PromptSettings()  # type: ignore
