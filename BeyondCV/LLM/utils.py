import os
import json
import pypdf
from pathlib import Path
from typing import Any
from BeyondCV.LLM.CVFields import BASE_TEMPLATE, build_extra_fields_text


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
    """
    with open(pdf_path, 'rb') as file:
        pdf_reader = pypdf.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def load_prompt(path_to_pdf: str | Path, modules: list[str] | None = None) -> str:
    if not modules: modules = []

    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(base_dir, "prompt.txt")

    with open(prompt_path, "r") as p:
        prompt_template = p.read()

    return prompt_template.format(
        json_template=json.dumps(BASE_TEMPLATE, indent=2),
        extra_fields=build_extra_fields_text(modules),
        extracted_text=extract_text_from_pdf(path_to_pdf),
    )


def safe_parse_json(response_text: str) -> Any:
    """Parse JSON from LLM response, handling markdown fences if present."""
    if not response_text:
        raise ValueError("Response is empty")
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        import re
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", response_text.strip())
        return json.loads(cleaned)

