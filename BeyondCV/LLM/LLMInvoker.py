import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from BeyondCV.LLM.utils import safe_parse_json, load_prompt
from BeyondCV.config import bcv_config as cfg

_always_use_cache: bool = bool(cfg.use_cache)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]

class LLMInvoker(ABC):
    def __init__(self, path_to_pdf: str | Path, modules: list[str] | None = None) -> None:
        self.pdf_path: str | Path = path_to_pdf
        self.file_name: str = Path(path_to_pdf).stem

        archive_path = self.get_default_archive_path()
        if archive_path.exists():
            if _always_use_cache:
                use_cache = "yes"
            else:
                use_cache = input(
                    f"Archived profile found for '{self.file_name}' at {archive_path}.\nUse cached version? [Y/n]: "
                ).strip().lower()
            if use_cache in ("", "y", "yes"):
                with open(archive_path, "r") as f:
                    self.result_json = json.load(f)
                self.result_archive: str | Path = str(archive_path)  # pyright: ignore[reportRedeclaration]
                print(f"Loaded profile from archive: {archive_path}")
                return


        print(f"Extracting data from '{path_to_pdf}'")

        prompt: str = load_prompt(path_to_pdf, modules=modules)
        self.result_json: Any = safe_parse_json(self.invoke(prompt))

        print("Data retrieved.")

        self.result_archive: str | Path = self.archive_json()

    def get_archive_location(self) -> str | Path:
        return self.result_archive

    def get_result_json(self) -> Any:
        return self.result_json


    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """
        Prompts the LLM with the PDF and returns the json object as a string.
        This function handles everything LLM related; from getting the prompt to prompting thr LLM and receiving the output.

        Args:
            prompt: The prompt to send to the LLM.

        Returns:
            Returns the LLM response text. Text sanitisation happens in the __init__ function.
        """
        pass

    def get_default_archive_path(self) -> Path:
        return Path.home() / ".beyondcv" / "archive" / f"{self.file_name}.json"

    def archive_json(self) -> str | Path:
        """
        The JSON file is saved to an archive location and the location is returned.
        This method can be overriden by the user to save to any location of their choice.

        This method is automatically called by the __init__ function.
        """
        if not self.result_json:
            raise ValueError("No JSON object available.")

        json_archive: Path = self.get_default_archive_path()
        json_archive.parent.mkdir(parents=True, exist_ok=True)

        with open(json_archive, "w") as f:
            json.dump(self.result_json, f, indent=2, ensure_ascii=False)

        print(f"Archived profile JSON in {json_archive}")
        return json_archive


__all__ = [
    "LLMInvoker"
]
