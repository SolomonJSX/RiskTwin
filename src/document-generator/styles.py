from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

FONT_NAME = "Times New Roman"
FONT_SIZE_BODY = Pt(14)
FONT_SIZE_TITLE = Pt(14)
FONT_SIZE_TABLE = Pt(12)

COLOR_BLACK = RGBColor(0, 0, 0)

def apply_gost_page_setup(doc):
    """
    Поля по требованиям конкурса/ГОСТ:
    слева - 3.0 см, справа - 1.0 см, сверху - 2.0 см, снизу - 2.5 см
    """
    for section in doc.sections:
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(1.0)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.5)
        # Убираем любые колонтитулы для строгого классического документа
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False

def add_gost_paragraph(doc, text: str = "", bold: bool = False, italic: bool = False, space_after: int = 0, first_line_indent: float = 0.75):
    """
    Абзац по требованиям:
    Times New Roman, 14 пт, одинарный межстрочный интервал,
    выравнивание по ширине, абзацный отступ 0.75 см.
    """
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.first_line_indent = Cm(first_line_indent)

    if text:
        run = p.add_run(text)
        run.font.name = FONT_NAME
        run.font.size = FONT_SIZE_BODY
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = COLOR_BLACK
    return p

def add_gost_heading(doc, text: str, space_before: int = 6, space_after: int = 6):
    """
    Заголовки по требованию:
    выравниваются по ширине, также как и текст, с абзацным отступом 0.75 см.
    Times New Roman, 14 пт, жирный.
    """
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.first_line_indent = Cm(0.75)

    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = FONT_SIZE_TITLE
    run.font.bold = True
    run.font.color.rgb = COLOR_BLACK
    return p

def set_academic_table_borders(table):
    """
    Стандартная простая черная сетка таблицы (без цвета, толщина 0.5 пт).
    """
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_cell(cell, text: str, bold: bool = False, align=WD_ALIGN_PARAGRAPH.LEFT, size=FONT_SIZE_TABLE):
    """
    Ячейка таблицы: Times New Roman, одинарный интервал, без абзацного отступа.
    """
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Cm(0)

    run = p.add_run(text)
    run.font.name = FONT_NAME
    run.font.size = size
    run.font.bold = bold
    run.font.color.rgb = COLOR_BLACK
