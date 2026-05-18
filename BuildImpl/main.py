from typing import Any
from BeyondCV.Template import CVTemplate
from BeyondCV.Translator import DocxTranslator
from BuildImpl.ProfileMaker import LLMProfileMaker
from BuildImpl.TableBuilder import make_template
from pathlib import Path


def main():
    profile = LLMProfileMaker(Path(__file__).parent / "sample_cv.pdf")
    data: dict[str, Any] = profile.get_result_json()

    template: CVTemplate = make_template()
    tables = template.build(data)

    print(f"Generated {len(tables)} table(s).")

    output = DocxTranslator("sample_cv.docx", template).build(data)
    print(f"\nCV saved to: {output}")


if __name__ == "__main__":
    main()
