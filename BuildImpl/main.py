from typing import Any
from BeyondCV.Template import CVTemplate
from BeyondCV.Translator import DocxTranslator
from BuildImpl.ProfileMaker import LLMProfileMaker
from BuildImpl.TableBuilder import make_template


def main():
    profile = LLMProfileMaker(r"C:\Users\abdal\OneDrive\Documents\Personal\CV\Abdallah_Soliman_CV.pdf")
    data: dict[str, Any] = profile.get_result_json()

    template: CVTemplate = make_template()
    tables = template.build(data)

    print(f"Generated {len(tables)} table(s) for the CV.")
    for i, table in enumerate(tables):
        print(f"  Table {i + 1}: {len(table.content)} row(s)")

    output = DocxTranslator("Abdallah_Soliman_CV.docx", template).build(data)
    print(f"\nCV saved to: {output}")


if __name__ == "__main__":
    main()
