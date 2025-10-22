from typing import Literal
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
PROMPT_DIR = BASE_DIR.joinpath("store", "prompts", "md")


class PromptFactory:
    def __init__(self):
        self.prompt_dir = PROMPT_DIR
        self.prompts = {
            "system_fix_sql": self._load_prompt,
            "system_respond": self._load_prompt,
            "system_identifier": self._load_prompt,
            "system_sql": self._load_prompt,
        }

    def get_prompt(
        self,
        prompt_type: Literal[
            "system_fix_sql", "system_respond", "system_identifier", "system_sql"
        ],
    ) -> str:
        if prompt_type not in self.prompts:
            raise ValueError(f"Invalid prompt type: {prompt_type}")
        return self.prompts[prompt_type](prompt_type)

    def _load_prompt(self, name: str) -> str:
        path = self.prompt_dir / f"{name}.md"
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")
        return path.read_text(encoding="utf-8")
