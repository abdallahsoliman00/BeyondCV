from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path
from BeyondCV.Template import CVTemplate


class DocTranslator(ABC):
    def __init__(self, document_name: str, template: CVTemplate):
        """
        Intialises the translator, making sure the save location exists.
        Args:
            document_name: Name of the output document. This MUST contain the file extension so that the file is correcly saved.
            template: The CV template created that will be translated. 
        """
        if not Path(document_name).suffix:
            raise ValueError(f"document_name must include a file extension (e.g. 'my_cv.docx'), got: '{document_name}'")

        doc_location: Path = Path.home() / ".beyondcv" / "outfiles" / f"{document_name}"
        doc_location.parent.mkdir(parents=True, exist_ok=True)
        self._doc_location: Path = doc_location
        self._template: CVTemplate = template

    @abstractmethod
    def build(self, data: dict[str, Any]) -> str:
        """
        A method uniquely implemented for each filetype. This method should build the document and return the path to this newly built document.

        Args:
            data: The data about the profile as a json object.

        Returns:
            The location of the newly created document.
        """
        pass


__all__ = [
    "DocTranslator",
]
