import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

class LLMInvoker(ABC):
    def __init__(self, path_to_pdf: str | Path) -> None:
        self.pdf_path: str | Path = path_to_pdf
        self.file_name: str = Path(path_to_pdf).stem
        self.result_json: Any = self.invoke(path_to_pdf)
        self.result_archive: str | Path = self.archive_json()

    def get_archive_location(self) -> str | Path:
        return self.result_archive

    def get_result_json(self) -> Any:
        return self.result_json

    @abstractmethod
    def invoke(self, path_to_pdf: str | Path) -> Any:
        """
        Prompts the LLM with the PDF and returns the json object as a string.
        This function handles everything LLM related; from getting the prompt to prompting thr LLM and receiving the output.

        Args:
            path_to_pdf: The path to the old CV PDF.

        Returns:
            Must return a JSON Python object (JSON as a dict) with the profile contents.

        Raises:
            ValueError: If a proper JSON object isn't returned.
            FileNotFound: If something other than a PDF is passed into the function.
        """
        pass

    def archive_json(self) -> str | Path:
        """
        The JSON file is saved to an archive location and the location is returned.
        This method can be overriden by the user to save to any location of their choice.

        This method is automatically called by the __init__ function.
        """
        if not self.result_json:
            raise ValueError("No JSON object available.")

        json_archive: Path = Path.home() / ".beyondcv" / "archive" / f"{self.file_name}.json"
        json_archive.parent.mkdir(parents=True, exist_ok=True)

        with open(json_archive, "w") as f:
            json.dump(self.result_json, f, indent=2, ensure_ascii=False)

        print(f"Archived profile JSON in {json_archive}")
        return json_archive

