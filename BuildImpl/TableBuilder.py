from colour import Color
from BeyondCV.TableBuilder import PageBreak
from BeyondCV.TableBuilder.Builder import CVTemplate, Section, RepeatingSection
from BeyondCV.TableBuilder.Components import Row, Cell, CellConfig, Paragraph, ParagraphConfig, Table
from BeyondCV.TableBuilder.Builder import SectionTitle


def make_template() -> CVTemplate:
    return CVTemplate([
        Section(
            Row([Cell(Paragraph("{name}", ParagraphConfig(bold=True, font_size_pt=24))),
            ]),
            Row([Cell(Paragraph("{title}", ParagraphConfig(font_size_pt=14, italic=True, text_color="blue"))),
            ]),
            Row([Cell(Paragraph("{profile_summary}", ParagraphConfig(italic=True))),
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
        PageBreak(),
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
            title=SectionTitle("Short Experience", ParagraphConfig(font_size_pt=15, bold=True))
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
                    Cell(Paragraph("{description}", ParagraphConfig(bullet=True))),
                ]),
            ]),
            title=SectionTitle("Experience", ParagraphConfig(font_size_pt=15, bold=True))
        ),
        RepeatingSection(
            source_key="languages",
            item=Table([
                Row([
                    Cell(Paragraph("{language}"), CellConfig(width_cm=5)),
                    Cell(Paragraph("{proficiency}"), CellConfig(width_cm=5)),
                ])
            ]),
            title=SectionTitle("Languages", ParagraphConfig(font_size_pt=15, bold=True))
        ),
        Section(
            Row([Cell(Paragraph("Test"))]),
            Row([
                Cell(Paragraph("{certifications}")),
            ]),
            title=SectionTitle("Certifications", ParagraphConfig(font_size_pt=15, bold=True))
        ),
        RepeatingSection(
            source_key="skill_groups",
            item=Table([
                Row([
                    Cell(Paragraph("{group_name}")),
                    Cell(Paragraph("{items}, "))
                ])
            ]),
        )
    ])


__all__ = [
    "make_template",
]
