from typing import Literal
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
PROMPT_DIR = BASE_DIR.joinpath("nlp", "prompts", "md")


class PromptFactory:
    def __init__(self):
        self.prompt_dir = PROMPT_DIR
        self.prompts = {
            "solve_error": self._load_prompt,
            "respond": self._load_prompt,
            "select_relations": self._load_prompt,
            "generate_sql": self._load_prompt,
        }

    def get_prompt(
        self,
        prompt_type: Literal[
            "solve_error", "respond", "select_relations", "generate_sql"
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
