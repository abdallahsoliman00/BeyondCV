from colour import Color
from BeyondCV.config import bcv_config as cfg
from BeyondCV.utils import PaperDimensions, get_paper_dimensions

_default_alignment: dict[str, str] = {
    "vertical": "center",       # Can be "top", "center", "bottom"
    "horizontal": "left",     # Can be "left", "center", "right"
}

_paper_size: str = str(cfg.paper_size).lower()   # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
_paper_dimensions: PaperDimensions = get_paper_dimensions(_paper_size)

class CellConfig:
    def __init__(
        self,
        width_cm: float = 0.0,       # If width is 0.0, the with of the cell is set to 1/total row width
        color: Color | None = None,
        content_alignment: dict[str, str] = _default_alignment,
        show_borders: bool = False
    ):
        self.width_cm: float = width_cm
        self.color: Color | None = color
        self.content_alignment: dict[str, str] = content_alignment
        self.show_borders: bool = show_borders


class ParagraphConfig:
    def __init__(
        self,
        font_name: str = cfg["default_font"],
        font_size_pt: float = 10.0,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False
    ):
        self.font_name: str = font_name
        self.font_size_pt: float = font_size_pt
        self.bold: bool = bold
        self.italic: bool = italic
        self.underline: bool = underline


class Paragraph:
    def __init__(
        self,
        text: str,
        config: ParagraphConfig | None = None
    ):
        self.text: str = text
        self.config: ParagraphConfig = config if config else ParagraphConfig()

    def create(self):
        pass


class Cell:
    def __init__(
        self,
        content: list[Paragraph] | Paragraph,
        config: CellConfig | None = None
    ):
        self.paragraphs: list[Paragraph] = [content] if isinstance(content, Paragraph) else content
        self.config: CellConfig = config if config else CellConfig()

    def create(self):
        pass


class Row:
    def __init__(
        self,
        cells: list[Cell],
        min_height_cm: float = 0.45,
        row_width_cm: float = 0.0           # If this value is 0, the row is as wide as the page margins
    ):
        self.cells: list[Cell] = cells
        self.row_width_cm: float = row_width_cm if row_width_cm > 0.0 else _paper_dimensions.width
        self.min_height_cm: float = min_height_cm

        for cell in self.cells:
            if cell.config.width_cm >= 0.0:
                cell.config.width_cm = self.row_width_cm * (1/len(self.cells))

    def create(self):
        pass
    
class Column:
    def __init__(
        self,
        cells: list[Cell],
        min_height_cm: float = 0.45,
        width_cm: float = 0.0,      # Again, if this value is zero, width is calculated at runtime depending on the number of columns in the table
    ):
        self.cells: list[Cell]
        self.min_height_cm: float = min_height_cm
        self.width_cm: float = width_cm


class Table:
    def __init__(
        self,
        content: list[Row] | list[Column]
    ):
        self.content: list[Row] | list[Column] = content
        
        if Table.are_columns(self.content) and len(self.content) > 0:
            for col in self.content:
                col.width_cm = 1/len(self.content) * _paper_dimensions.width  # pyright: ignore[reportAttributeAccessIssue]
        
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

