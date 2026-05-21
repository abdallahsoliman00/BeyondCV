from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path
from BeyondCV.TableBuilder import CVTemplate, PageBreak, Table


class DocTranslator(ABC):
    def __init__(self, document_name: str, template: CVTemplate, data: dict[str, Any]):
        """
        Intialises the translator, making sure the save location exists.
        Args:
            document_name: Name of the output document. This MUST contain the file extension so that the file is correctly saved.
            template: The CV template created that will be translated. 
            data: The profile's data as a Python dict (the data JSON).
        """
        if not Path(document_name).suffix:
            raise ValueError(f"document_name must include a file extension (e.g. 'my_cv.docx'), got: '{document_name}'")

        doc_location: Path = Path.home() / ".beyondcv" / "outfiles" / f"{document_name}"
        doc_location.parent.mkdir(parents=True, exist_ok=True)
        self.doc_location: Path = doc_location
        self.tables: list[Table | PageBreak] = template.build(data)


    @abstractmethod
    def build_document(self):
        """
        A method uniquely implemented for each filetype. This method should build the document and return the path to this newly built document.
        
        When overloading this function, the document should be built with the following in mind:
            self.tables: list[Table | PageBreak]
                This member variable is a list of the different tables to be built by the Document Builder
            self.doc_location: Path
                This member variable stores the location of where the output file is to be saved
        """
        pass

    def build(self) -> str:
        self.build_document()
        return str(self.doc_location)


__all__ = [
    "DocTranslator",
]
