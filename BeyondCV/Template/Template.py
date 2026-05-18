from __future__ import annotations

__all__ = [
    "CVTemplate",
    "Section",
    "RepeatingSection",
]

import copy
import re
from typing import Any

from BeyondCV.TableBuilder.Table import Cell, Paragraph, Row, Table


def _resolve_placeholders(text: str, data: dict[str, Any]) -> str | list[str]:
    """
    Replace {field_name} placeholders in a text string with values from the data dict.

    When a field holds a list value (e.g. description = ["bullet1", "bullet2"]),
    the entire function returns a list of strings instead, so the caller can
    create one Paragraph per list item.

    If the template text contains a suffix immediately after the list placeholder
    (e.g. "{items},"), the suffix is appended to every item except the last.

    Args:
        text: A string that may contain {field_name} placeholders.
        data: The data dict to resolve placeholders against.

    Returns:
        The resolved string, or a list of strings if the field value was a list.
    """
    _PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")

    def _replace(match: re.Match[str]) -> str:
        key: str = match.group(1)
        value: str | list[str] | None = data.get(key)
        if value is None:
            return match.group(0)
        if isinstance(value, list):
            return "<__LIST_PLACEHOLDER__>"
        return str(value)

    resolved = _PLACEHOLDER_RE.sub(_replace, text)
    if "<__LIST_PLACEHOLDER__>" in resolved:
        keys = [m.group(1) for m in _PLACEHOLDER_RE.finditer(text)]
        for k in keys:
            v: Any | None = data.get(k)
            if isinstance(v, list):
                # Extract any suffix that follows the {key} placeholder in the template.
                suffix_match = re.search(r"\{" + re.escape(k) + r"\}(.*)$", text)
                suffix = suffix_match.group(1) if suffix_match else ""
                items = [str(item) for item in v]                    # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType]
                if suffix:
                    return [item + suffix for item in items[:-1]] + [items[-1]]
                return items
        return resolved.replace("<__LIST_PLACEHOLDER__>", "")
    return resolved


class Section:
    def __init__(self, *rows: Row):
        self.rows: list[Row] = list(rows)

    def build(self, data: dict[str, Any]) -> list[Table]:
        resolved_rows = [self._resolve_row(row, data) for row in self.rows]
        return [Table(resolved_rows)]

    def _resolve_row(self, row: Row, data: dict[str, Any]) -> Row:
        resolved_cells: list[Cell] = []
        for cell in row.cells:
            resolved_paragraphs: list[Paragraph] = []
            for p in cell.paragraphs:
                resolved = _resolve_placeholders(p.text, data)
                if isinstance(resolved, list):
                    resolved_paragraphs.extend(
                        Paragraph(item, copy.deepcopy(p.config)) for item in resolved
                    )
                else:
                    resolved_paragraphs.append(Paragraph(resolved, copy.deepcopy(p.config)))
            resolved_cells.append(Cell(resolved_paragraphs, copy.deepcopy(cell.config)))
        return Row(resolved_cells, row.min_height_cm, row.row_width_cm)


class RepeatingSection:
    def __init__(self, source_key: str, item: Table, header: list[Row] | Row | None = None):
        self.source_key: str = source_key
        self.item: Table = item
        self.header: list[Row] = [header] if isinstance(header, Row) else header or []

    def build(self, data: dict[str, Any]) -> list[Table]:
        items: list[Any] | str = data.get(self.source_key, [])
        if not isinstance(items, list):
            items = [items]

        if not self.header:
            return self._build_separate(items)
        else:
            return self._build_with_header(items, data)

    def _build_separate(self, items: list[Any]) -> list[Table]:
        tables: list[Table] = []
        for item_data in items:
            if not isinstance(item_data, dict):
                tables.append(copy.deepcopy(self.item))
                continue

            resolved_rows: list[Row] = []
            for row in self.item.content:
                if isinstance(row, Row):
                    resolved_rows.append(self._resolve_row(row, item_data))          # pyright: ignore[reportUnknownArgumentType]
            tables.append(Table(resolved_rows))

        return tables

    def _build_with_header(self, items: list[Any], data: dict[str, Any]) -> list[Table]:
        resolved_rows: list[Row] = []
        for row in self.header:
            resolved_rows.append(self._resolve_row(row, data))

        for item_data in items:
            if not isinstance(item_data, dict):
                for row in self.item.content:
                    if isinstance(row, Row):
                        resolved_rows.append(copy.deepcopy(row))
                continue

            for row in self.item.content:
                if isinstance(row, Row):
                    resolved_rows.append(self._resolve_row(row, item_data))          # pyright: ignore[reportUnknownArgumentType]

        return [Table(resolved_rows)]

    def _resolve_row(self, row: Row, data: dict[str, Any]) -> Row:
        resolved_cells: list[Cell] = []
        for cell in row.cells:
            resolved_paragraphs: list[Paragraph] = []
            for p in cell.paragraphs:
                resolved = _resolve_placeholders(p.text, data)
                if isinstance(resolved, list):
                    resolved_paragraphs.extend(
                        Paragraph(item, copy.deepcopy(p.config)) for item in resolved
                    )
                else:
                    resolved_paragraphs.append(Paragraph(resolved, copy.deepcopy(p.config)))
            resolved_cells.append(Cell(resolved_paragraphs, copy.deepcopy(cell.config)))
        return Row(resolved_cells, row.min_height_cm, row.row_width_cm)


class CVTemplate:
    def __init__(self, sections: list[Section | RepeatingSection]):
        self.sections: list[Section | RepeatingSection] = sections

    def build(self, data: dict[str, Any]) -> list[Table]:
        tables: list[Table] = []
        for section in self.sections:
            tables.extend(section.build(data))
        return tables
