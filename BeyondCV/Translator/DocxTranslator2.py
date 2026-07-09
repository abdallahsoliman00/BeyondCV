from typing import override

import spire.doc as sd
from colour import Color

from BeyondCV.Translator.DocTranslator import DocTranslator
from BeyondCV.TableBuilder.Components import (
    Table as CVTable, Row, Cell, Paragraph, Column, PageBreak,
    HeaderFooterBase,
)
from BeyondCV.config import bcv_config as cfg

CM_TO_PT = 28.3465


class DocxTranslator2(DocTranslator):
    _HALIGN_MAP: dict[str, sd.HorizontalAlignment] = {
        "left": sd.HorizontalAlignment.Left,
        "center": sd.HorizontalAlignment.Center,
        "right": sd.HorizontalAlignment.Right,
    }
    _VALIGN_MAP: dict[str, sd.VerticalAlignment] = {
        "top": sd.VerticalAlignment.Top,
        "center": sd.VerticalAlignment.Middle,
        "bottom": sd.VerticalAlignment.Bottom,
    }

    @override
    def build_document(self):
        doc = sd.Document()
        section = doc.AddSection()

        section.PageSetup.Margins.Top = float(cfg.margin_top_cm) * CM_TO_PT        # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        section.PageSetup.Margins.Bottom = float(cfg.margin_bottom_cm) * CM_TO_PT   # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        section.PageSetup.Margins.Left = float(cfg.margin_left_cm) * CM_TO_PT       # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        section.PageSetup.Margins.Right = float(cfg.margin_right_cm) * CM_TO_PT     # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
        section.PageSetup.HeaderDistance = float(cfg.header_from_top_cm) * CM_TO_PT # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]

        self._apply_headers_footers(section)

        for table in self.tables:
            if not isinstance(table, PageBreak):
                self._add_table(section, table)
                if not table.metadata.is_title:
                    _ = section.AddParagraph()
            else:
                _ = section.AddParagraph().AppendBreak(sd.BreakType.PageBreak)

        doc.SaveToFile(str(self.doc_location))

    # ------------------------------------------------------------------ #
    #  Header / Footer rendering
    # ------------------------------------------------------------------ #

    def _apply_headers_footers(self, section: sd.Section):
        has_different_first = (
            self.first_page_header is not None or self.first_page_footer is not None
        )

        if has_different_first:
            section.PageSetup.DifferentFirstPageHeaderFooter = True

        if self.header is not None:
            self._apply_hf_content(section.HeadersFooters.Header, self.header)
        if self.footer is not None:
            self._apply_hf_content(section.HeadersFooters.Footer, self.footer)

        if has_different_first:
            if self.first_page_header is not None:
                self._apply_hf_content(section.HeadersFooters.FirstPageHeader, self.first_page_header)
            if self.first_page_footer is not None:
                self._apply_hf_content(section.HeadersFooters.FirstPageFooter, self.first_page_footer)

    def _apply_hf_content(self, hf_section: sd.HeaderFooter, hf_model: HeaderFooterBase):
        if hf_model.image_path is not None:
            self._render_hf_image(hf_section, hf_model)
        elif hf_model.page_numbers is not None:
            self._render_hf_page_numbers(hf_section, hf_model)
        elif hf_model.text is not None:
            self._render_hf_paragraph(hf_section, hf_model)

    def _render_hf_paragraph(self, hf_section: sd.HeaderFooter, hf_model: HeaderFooterBase):
        assert hf_model.text is not None
        p = hf_section.AddParagraph()
        self._format_paragraph(p, hf_model.text, {"horizontal": "left", "vertical": "center"})

    def _render_hf_page_numbers(self, hf_section: sd.HeaderFooter, hf_model: HeaderFooterBase):
        assert hf_model.page_numbers is not None
        config = hf_model.page_numbers

        p = hf_section.AddParagraph()
        p.Format.HorizontalAlignment = sd.HorizontalAlignment.Center
        p.Format.BeforeSpacing = 0
        p.Format.AfterSpacing = 0

        field = p.AppendField("PAGE", sd.FieldType.FieldPage)
        field.CharacterFormat.FontName = config.font_name
        field.CharacterFormat.FontSize = config.font_size_pt
        field.CharacterFormat.TextColor = self.to_spire_color(config.text_color)
        field.CharacterFormat.Bold = config.bold
        field.CharacterFormat.Italic = config.italic
        field.CharacterFormat.UnderlineStyle = (
            sd.UnderlineStyle.Single if config.underline else sd.UnderlineStyle.none
        )

    def _render_hf_image(self, hf_section: sd.HeaderFooter, hf_model: HeaderFooterBase):
        assert hf_model.image_path is not None
        img_cfg = hf_model.image_config

        p = hf_section.AddParagraph()
        halign = img_cfg.alignment.get("horizontal", "left")
        p.Format.HorizontalAlignment = self._HALIGN_MAP.get(halign, sd.HorizontalAlignment.Left)
        p.Format.BeforeSpacing = 0
        p.Format.AfterSpacing = 0

        pic = p.AppendPicture(str(hf_model.image_path))
        if img_cfg.width > 0.0:
            pic.Width = img_cfg.width * CM_TO_PT
        if img_cfg.height > 0.0:
            pic.Height = img_cfg.height * CM_TO_PT

    # ------------------------------------------------------------------ #
    #  Table rendering
    # ------------------------------------------------------------------ #

    def _add_table(self, section: sd.Section, table_model: CVTable):
        if CVTable.are_columns(table_model.content):
            self._add_column_table(section, table_model)
        else:
            self._add_row_table(section, table_model)

    def _add_row_table(self, section: sd.Section, table_model: CVTable):
        rows = [r for r in table_model.content if isinstance(r, Row)]
        if not rows:
            return

        max_cols = max(len(r.cells) for r in rows)
        table = section.AddTable()
        table.ResetCells(len(rows), max_cols)
        table.ClearBorders()

        col_widths = [0.0] * max_cols
        for row_model in rows:
            if len(row_model.cells) == max_cols:
                for ci, cell in enumerate(row_model.cells):
                    col_widths[ci] = cell.config.width_cm
                break

        for ci, w in enumerate(col_widths):
            if w > 0.0:
                table.SetColumnWidth(ci, w * CM_TO_PT, sd.CellWidthType.Point)

        for row_idx, row_model in enumerate(rows):
            table.Rows[row_idx].Height = row_model.min_height_cm * CM_TO_PT

            for col_idx, cell_model in enumerate(row_model.cells):
                cell = table.Rows[row_idx].Cells[col_idx]
                self._fill_cell(cell, cell_model)

            if len(row_model.cells) < max_cols:
                table.ApplyHorizontalMerge(
                    row_idx,
                    len(row_model.cells) - 1,
                    max_cols - 1,
                )

    def _add_column_table(self, section: sd.Section, table_model: CVTable):
        columns = [c for c in table_model.content if isinstance(c, Column)]
        if not columns:
            return

        col_count = len(columns)
        row_count = max(len(c.cells) for c in columns)
        if row_count == 0:
            return

        table = section.AddTable()
        table.ResetCells(row_count, col_count)
        table.ClearBorders()

        for col_idx, col_model in enumerate(columns):
            if col_model.width_cm > 0.0:
                table.SetColumnWidth(col_idx, col_model.width_cm * CM_TO_PT, sd.CellWidthType.Point)
            for row_idx, cell_model in enumerate(col_model.cells):
                cell = table.Rows[row_idx].Cells[col_idx]
                self._fill_cell(cell, cell_model)

    # ------------------------------------------------------------------ #
    #  Cell / Paragraph formatting
    # ------------------------------------------------------------------ #

    @staticmethod
    def to_spire_color(color: Color) -> sd.Color:
        r, g, b = color.get_rgb()
        return sd.Color.FromRgb(int(r * 255), int(g * 255), int(b * 255))

    def _fill_cell(self, cell: sd.TableCell, cell_model: Cell):
        config = cell_model.config

        if config.width_cm > 0.0:
            cell.SetCellWidth(config.width_cm * CM_TO_PT, sd.CellWidthType.Point)

        valign_str = config.content_alignment.get("vertical", "center")
        cell.CellFormat.VerticalAlignment = self._VALIGN_MAP.get(valign_str, sd.VerticalAlignment.Middle)

        if config.color is not None:
            cell.CellFormat.BackColor = self.to_spire_color(config.color)
        else:
            cell.CellFormat.ClearBackground()

        if config.show_borders:
            b = cell.CellFormat.Borders
            b.BorderType = sd.BorderStyle.Single
            b.LineWidth = 1.0
            b.Color = sd.Color.get_Black()
        else:
            cell.CellFormat.Borders.BorderType = sd.BorderStyle.none

        cell.EnsureMinimum()
        for para_idx, para_model in enumerate(cell_model.paragraphs):
            p = cell.Paragraphs[0] if para_idx == 0 else cell.AddParagraph()
            self._clear_paragraph_items(p)
            self._format_paragraph(p, para_model, config.content_alignment)

    @staticmethod
    def _clear_paragraph_items(p: sd.Paragraph):
        while len(p.Items) > 0:
            p.Items.RemoveAt(0)

    def _format_paragraph(self, p: sd.Paragraph, para_model: Paragraph, alignment: dict[str, str]):
        p.Format.BeforeSpacing = 0
        p.Format.AfterSpacing = 0

        halign = alignment.get("horizontal", "left")
        p.Format.HorizontalAlignment = self._HALIGN_MAP.get(halign, sd.HorizontalAlignment.Left)

        if para_model.config.bullet:
            p.ApplyStyle(sd.BuiltinStyle.ListBullet)

        tr = p.AppendText(para_model.text)
        tr.CharacterFormat.FontName = para_model.config.font_name
        tr.CharacterFormat.FontSize = para_model.config.font_size_pt
        tr.CharacterFormat.TextColor = self.to_spire_color(para_model.config.text_color)
        tr.CharacterFormat.Bold = para_model.config.bold
        tr.CharacterFormat.Italic = para_model.config.italic
        tr.CharacterFormat.UnderlineStyle = (
            sd.UnderlineStyle.Single if para_model.config.underline else sd.UnderlineStyle.none
        )
