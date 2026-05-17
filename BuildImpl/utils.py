from pathlib import Path
import pypdf
import os


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


def load_prompt(path_to_pdf: str | Path) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(base_dir, "prompt.txt")

    prompt: str = ""
    with open(prompt_path, "r") as p:
        prompt += p.read()

    prompt += extract_text_from_pdf(path_to_pdf)

    return prompt
