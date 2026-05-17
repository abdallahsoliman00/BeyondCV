from colour import Color
from BeyondCV.Template import CVTemplate, Section, RepeatingSection
from BeyondCV.TableBuilder.Table import Row, Cell, CellConfig, Paragraph, ParagraphConfig, Table


def make_template() -> CVTemplate:
    return CVTemplate([
        Section(
            Row([
                Cell(Paragraph("{name}", ParagraphConfig(bold=True, font_size_pt=24)),
                     CellConfig(width_cm=8)),
                Cell(Paragraph("{title}", ParagraphConfig(font_size_pt=14, italic=True)),
                     CellConfig(width_cm=4)),
            ]),
            Row([
                Cell(Paragraph("{profile_summary}", ParagraphConfig(italic=True))),
            ]),
        ),
        RepeatingSection(
            source_key="education",
            item=Table([
                Row([
                    Cell(Paragraph("{degree}", ParagraphConfig(bold=True)),
                         CellConfig(width_cm=3, color=Color("#AB123F"), show_borders=True)),
                    Cell(Paragraph("{institute}"),
                         CellConfig(width_cm=5, color=Color("#AB123F"), show_borders=True)),
                    Cell(Paragraph("{year}"),
                         CellConfig(width_cm=2, color=Color("#AB123F"), show_borders=True)),
                ])
            ])
        ),
        RepeatingSection(
            source_key="experience",
            item=Table([
                Row([
                    Cell(Paragraph("{organisation}", ParagraphConfig(bold=True)),
                         CellConfig(width_cm=4, color=Color("#AB123F"))),
                    Cell(Paragraph("{job_title}"),
                         CellConfig(width_cm=3, color=Color("#AB123F"))),
                    Cell(Paragraph("{job_period}", ParagraphConfig(italic=True)),
                         CellConfig(width_cm=3, color=Color("#AB123F"))),
                ]),
                Row([
                    Cell(Paragraph("{description}")),
                ]),
            ])
        ),
        Section(
            Row([
                Cell(Paragraph("{tools_prog_languages}")),
            ]),
            Row([
                Cell(Paragraph("{soft_skills}")),
            ]),
        ),
        RepeatingSection(
            source_key="languages",
            item=Table([
                Row([
                    Cell(Paragraph("{language}"), CellConfig(width_cm=5)),
                    Cell(Paragraph("{proficiency}"), CellConfig(width_cm=5)),
                ])
            ])
        ),
        Section(
            Row([
                Cell(Paragraph("{certifications}")),
            ]),
        ),
    ])


__all__ = [
    "make_template",
]