import json
import pypdf
from pathlib import Path
from typing import Any, Callable
from BeyondCV.LLM.CVFields import BASE_TEMPLATE, build_extra_fields_text
import zipfile
import xml.etree.ElementTree as ET


def extract_text_from_docx(docx_path: str | Path):
    ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    para_tag = ns + 'p'
    text_tag = ns + 't'
    
    paragraphs_list: list[str] = []
    
    with zipfile.ZipFile(docx_path) as docx:
        # Read the core XML content
        xml_content = docx.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        
        # 1. Find every individual paragraph block first
        for p_node in tree.iter(para_tag):
            
            # 2. Gather only the text fragments inside this specific paragraph
            text_nodes = p_node.iter(text_tag)
            p_text = "".join(node.text for node in text_nodes if node.text)
            
            # 3. Only keep it if the paragraph isn't completely empty
            if p_text.strip():
                paragraphs_list.append(p_text)
                
    return '\n'.join(paragraphs_list)


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


def extract_text_from_txt(path: str | Path) -> str:
    with open(path, "r") as f:
        return f.read()


def load_prompt(path_to_file: str | Path, modules: list[str] | None = None) -> str:
    path_to_file = Path(path_to_file)
    if not modules: modules = []

    file_extractor: Callable[[str | Path], str]
    if path_to_file.suffix == ".pdf":
        file_extractor = extract_text_from_pdf
    elif path_to_file.suffix == ".docx":
        file_extractor = extract_text_from_docx
    else:
        try:
            file_extractor = extract_text_from_pdf
        except Exception:
            file_extractor = extract_text_from_txt

    prompt_path = Path(__file__).parent / "prompt.txt"

    with open(prompt_path, "r") as p:
        prompt_template = p.read()

    return prompt_template.format(
        json_template=json.dumps(BASE_TEMPLATE, indent=2),
        extra_fields=build_extra_fields_text(modules),
        extracted_text=file_extractor(path_to_file),
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

