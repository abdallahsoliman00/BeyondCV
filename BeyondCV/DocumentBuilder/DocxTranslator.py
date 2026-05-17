from pathlib import Path
from docx import Document


class DocxBuilder:
    def __init__(
        self,
        document_name: str
    ):
        if document_name.endswith(".docx"):
            document_name = document_name.removesuffix(".docx")

        doc_location: Path = Path.home() / ".beyondcv" / "outfiles" / f"{document_name}.docx"
        doc_location.parent.mkdir(parents=True, exist_ok=True)
