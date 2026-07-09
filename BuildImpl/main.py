from typing import Any
from pathlib import Path

from BeyondCV.TableBuilder import CVTemplate
from BeyondCV.Translator import DocxTranslator2, DocxTranslator

from BuildImpl.ProfileMaker import LLMProfileMaker
from BuildImpl.TemplateMaker import make_template
from BuildImpl.custom_config import update


def main():
    update()
    profile = LLMProfileMaker(Path(__file__).parent / "sample_cv.pdf")
    data: dict[str, Any] = profile.get_result_json()
    template: CVTemplate = make_template()

    # tables = template.build(data)
    # print(f"Generated {len(tables)} table(s).")

    output = DocxTranslator("sample_cv.docx", template, data).build()
    print(f"\nCV saved to: {output}")
    output2 = DocxTranslator2("sample_cv2.docx", template, data).build()
    print(f"\nCV saved to: {output2}")


if __name__ == "__main__":
    main()
