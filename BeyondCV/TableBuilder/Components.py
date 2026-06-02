__all__ = [
    "CellConfig",
    "ParagraphConfig",
    "Paragraph",
    "Cell",
    "Row",
    "Table",
    "HeaderFooterBase",
]

from colour import Color
from pathlib import Path

from BeyondCV.config import bcv_config as cfg
from BeyondCV.utils import (
    get_paper_dimensions, get_page_dimensions,
    PaperDimensions,
    ImgConfig, default_alignment
)
from PIL import Image


def _get_page_dimensions() -> PaperDimensions:
    """Compute page dimensions from the live config each time they are needed."""
    paper = get_paper_dimensions(str(cfg.paper_size).lower())  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
    return get_page_dimensions(
        paper,
        float(cfg.margin_left_cm), float(cfg.margin_right_cm),  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        float(cfg.margin_top_cm), float(cfg.margin_bottom_cm)   # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
    )


class TableMetadata:
    is_title: bool = False


class CellConfig:
    def __init__(
        self,
        width_cm: float = 0.0,       # If width is 0.0, the with of the cell is set to 1/total row width
        color: Color | str | None = None,
        content_alignment: dict[str, str] = default_alignment,
        show_borders: bool = False
    ):
        self.width_cm: float = width_cm
        self.color: Color | None = Color(color) if color else None
        self.content_alignment: dict[str, str] = content_alignment
        self.show_borders: bool = show_borders


class ParagraphConfig:
    def __init__(
        self,
        font_name: str | None = None,
        font_size_pt: float = 10.0,
        text_color: Color | str | None = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        bullet: bool = False
    ):
        self.font_name: str = font_name if font_name is not None else str(cfg.default_font)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        self.font_size_pt: float = font_size_pt
        self.text_color: Color = Color(text_color)
        self.bold: bool = bold
        self.italic: bool = italic
        self.underline: bool = underline
        self.bullet: bool = bullet


class Paragraph:
    def __init__(
        self,
        text: str,
        config: ParagraphConfig | None = None
    ):
        self.text: str = text
        self.config: ParagraphConfig = config if config else ParagraphConfig()


class Cell:
    def __init__(
        self,
        content: list[Paragraph] | Paragraph,
        config: CellConfig | None = None
    ):
        self.paragraphs: list[Paragraph] = [content] if isinstance(content, Paragraph) else content
        self.config: CellConfig = config if config else CellConfig()


class Row:
    def __init__(
        self,
        cells: list[Cell] | Cell,
        min_height_cm: float = 0.45,
        row_width_cm: float = 0.0           # If this value is 0, the row is as wide as the page margins
    ):
        self.cells: list[Cell] = [cells] if isinstance(cells, Cell) else cells
        self.row_width_cm: float = row_width_cm if row_width_cm > 0.0 else _get_page_dimensions().width
        self.min_height_cm: float = min_height_cm

        for cell in self.cells:
            if cell.config.width_cm <= 0.0:
                cell.config.width_cm = self.row_width_cm * (1/len(self.cells))
 
    def add_cell(self, cell: Cell):
        self.cells.append(cell)


class Column:
    def __init__(
        self,
        cells: list[Cell],
        min_height_cm: float = 0.45,
        width_cm: float = 0.0,      # Again, if this value is zero, width is calculated at runtime depending on the number of columns in the table
    ):
        self.cells: list[Cell] = cells
        self.min_height_cm: float = min_height_cm
        self.width_cm: float = width_cm


class Table:
    def __init__(
        self,
        content: list[Row] | list[Column]
    ):
        self.content: list[Row] | list[Column] = content
        self.metadata: TableMetadata = TableMetadata()
        
        if Table.are_columns(self.content) and len(self.content) > 0:
            for col in self.content:
                col.width_cm = 1/len(self.content) * _get_page_dimensions().width  # pyright: ignore[reportAttributeAccessIssue]
        
    @staticmethod
    def are_columns(items: list[Row] | list[Column]):
        for i in items:
            if not isinstance(i, Column):
                return False
        return True

    @staticmethod
    def are_rows(items: list[Row] | list[Column]):
        for i in items:
            if not isinstance(i, Row):
                return False
        return True


class PageBreak:
    """
    This class functionally does nothing but indicate
    to the Translator Module to place a page break here
    """
    pass


class HeaderFooterBase:
    def __init__(
        self,
        text: Paragraph | None = None,
        page_numbers: ParagraphConfig | None = None,        # If ParagraphConfig exists, page numbers are set to true and the config provided is how the text will be formatted
        image_path: Path | str | None = None,
        image_config: ImgConfig | None = None
    ):
        self.text: Paragraph | None = text
        self.page_numbers: ParagraphConfig | None = page_numbers
        self.image_path: Path | str | None = image_path
        self.image_config: ImgConfig = image_config if image_config else ImgConfig()

        if self.image_path:
            with Image.open(self.image_path) as img:
                width0, height0 = img.size
                # If both sides are unset, set the image size to be the default size
                if not self.image_config.width and not self.image_config.height:
                    self.image_config.width = width0
                    self.image_config.width = height0
                # If one of either side is set, the image is scaled to maintain aspect ratio
                elif not self.image_config.width and self.image_config.height:
                    self.image_config.width = (width0 / height0) * self.image_config.height
                elif not self.image_config.height and self.image_config.width:
                    self.image_config.height = (height0 / width0) * self.image_config.width


        # Let the existence of an image override anything else
        if self.text and image_path:
            self.text = None
        if self.page_numbers and image_path:
            self.page_numbers = None

