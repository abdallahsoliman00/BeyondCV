from BuildImpl.ProfileMaker import LLMProfileMaker
from BuildImpl.TableBuilder import make_template


def main():
    profile = LLMProfileMaker(r"C:\Users\abdal\OneDrive\Documents\Personal\CV\Abdallah_Soliman_CV.pdf")
    data = profile.get_result_json()

    template = make_template()
    tables = template.build(data)

    print(f"Generated {len(tables)} table(s) for the CV.")
    for i, table in enumerate(tables):
        print(f"  Table {i + 1}: {len(table.content)} row(s)")


if __name__ == "__main__":
    main()
