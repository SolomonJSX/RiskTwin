from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# 16:9 widescreen dimensions
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Palettes (Exact match to RiskTwin Next.js Web App)
BG_WHITE = RGBColor(255, 255, 255)
BG_CARD = RGBColor(248, 250, 252)          # slate-50
BG_MINT = RGBColor(236, 253, 245)          # emerald-50
BG_AMBER_LIGHT = RGBColor(254, 243, 199)   # amber-50
BG_ROSE_LIGHT = RGBColor(255, 241, 242)    # rose-50

BORDER_LIGHT = RGBColor(226, 232, 240)     # slate-200
BORDER_EMERALD = RGBColor(167, 243, 208)   # emerald-200

COLOR_PRIMARY = RGBColor(5, 150, 105)      # emerald-600
COLOR_PRIMARY_DARK = RGBColor(4, 120, 87)  # emerald-700
COLOR_TEXT_DARK = RGBColor(15, 23, 42)     # slate-900 (strong titles)
COLOR_TEXT_MUTED = RGBColor(100, 116, 139) # slate-500
COLOR_TEXT_EMERALD = RGBColor(6, 95, 70)   # emerald-800
COLOR_AMBER = RGBColor(217, 119, 6)        # amber-600
COLOR_ROSE = RGBColor(225, 29, 72)         # rose-600

FONT_MAIN = "Calibri"

def apply_slide_background(slide):
    """Sets a clean pure white background with subtle footer."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_WHITE

def apply_image_background(slide, image_path: str):
    """Sets a full-bleed picture background for the slide."""
    slide.shapes.add_picture(image_path, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT)

def add_header(slide, tag_text: str, title_text: str, subtitle_text: str = None, title_size: Pt = Pt(21)):
    """Creates a consistent modern RiskTwin header with category pill."""
    # 1. Category Tag Pill
    pill_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8), Inches(0.35), Inches(3.5), Inches(0.32)
    )
    pill_box.fill.solid()
    pill_box.fill.fore_color.rgb = BG_MINT
    pill_box.line.color.rgb = BORDER_EMERALD
    pill_box.line.width = Pt(1)
    tf_pill = pill_box.text_frame
    tf_pill.word_wrap = False
    tf_pill.margin_top = Inches(0)
    tf_pill.margin_bottom = Inches(0)
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = tag_text.upper()
    p_pill.font.name = FONT_MAIN
    p_pill.font.size = Pt(9)
    p_pill.font.bold = True
    p_pill.font.color.rgb = COLOR_PRIMARY_DARK
    p_pill.alignment = PP_ALIGN.CENTER

    # 2. Main Title Text Box
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.95))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_top = Inches(0)
    tf_title.margin_bottom = Inches(0)
    tf_title.margin_left = Inches(0)
    tf_title.margin_right = Inches(0)
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_MAIN
    p_title.font.size = title_size
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_TEXT_DARK

    if subtitle_text:
        p_sub = tf_title.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_MAIN
        p_sub.font.size = Pt(10.5)
        p_sub.font.italic = True
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_before = Pt(3)

def add_footer(slide, current_slide: int, total_slides: int = 11):
    """Subtle professional footer."""
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.35))
    tf = footer_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"RiskTwin • Республиканский конкурс АБРК & ГКБ 2026 | Слайд {current_slide} из {total_slides}"
    p.font.name = FONT_MAIN
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=BG_CARD, border_color=BORDER_LIGHT):
    """Creates a rounded card container."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card

def add_image_placeholder(slide, left, top, width, height, label: str):
    """Creates an annotated dashed frame ready for dragging a screenshot."""
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    frame.fill.solid()
    frame.fill.fore_color.rgb = RGBColor(241, 245, 249) # slate-100
    frame.line.color.rgb = COLOR_PRIMARY
    frame.line.width = Pt(1.5)
    
    tf = frame.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"📷 [МЕСТО ДЛЯ СКРИНШОТА ИНТЕРФЕЙСА]\n{label}"
    p.font.name = FONT_MAIN
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER
    return frame

def add_icon(slide, icon_name: str, left, top, size=Inches(0.35), color_hex="#059669"):
    """Inserts a sharp transparent PNG icon onto the slide."""
    from icons import get_icon_png_path
    png_path = get_icon_png_path(icon_name, color_hex=color_hex, size=128)
    return slide.shapes.add_picture(png_path, left, top, size, size)

def add_icon_badge(slide, icon_name: str, left, top, badge_size=Inches(0.55), icon_size=Inches(0.3),
                   bg_color=BG_MINT, border_color=BORDER_EMERALD, color_hex="#059669"):
    """
    Creates a modern rounded badge with soft background and centered icon.
    Signature modern fintech UI element matching RiskTwin frontend.
    """
    from icons import get_icon_png_path
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, badge_size, badge_size)
    badge.fill.solid()
    badge.fill.fore_color.rgb = bg_color
    badge.line.color.rgb = border_color
    badge.line.width = Pt(1)
    
    offset = (badge_size - icon_size) / 2
    png_path = get_icon_png_path(icon_name, color_hex=color_hex, size=128)
    icon = slide.shapes.add_picture(png_path, left + offset, top + offset, icon_size, icon_size)
    return badge, icon

