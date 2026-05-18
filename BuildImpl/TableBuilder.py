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
                    Cell(Paragraph("Degree")),
                    Cell(Paragraph("Institute")),
                    Cell(Paragraph("Graduation Year")),
                ]),
                Row([
                    Cell(Paragraph("{degree}", ParagraphConfig(bold=True))),
                    Cell(Paragraph("{institute}")),
                    Cell(Paragraph("{year}")),
                ])
            ])
        ),
        RepeatingSection(
            source_key="experience",
            item=Table([
                Row([
                    Cell(Paragraph("{organisation}", ParagraphConfig(bold=True))),
                    Cell(Paragraph("{job_title}")),
                    Cell(Paragraph("{job_period}")),
                ])
            ]),
            header=Row([
                Cell(Paragraph("Title", ParagraphConfig(font_size_pt=12)), CellConfig(color=Color("#42b0f5"))),
                Cell(Paragraph("Organisation", ParagraphConfig(font_size_pt=12)), CellConfig(color=Color("#42b0f5"))),
                Cell(Paragraph("Duration", ParagraphConfig(font_size_pt=12)), CellConfig(color=Color("#42b0f5"))),
            ]),
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
