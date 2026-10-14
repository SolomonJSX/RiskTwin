import os
from pathlib import Path
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from theme import (
    apply_image_background, add_card, add_icon_badge,
    COLOR_PRIMARY, COLOR_PRIMARY_DARK, COLOR_TEXT_DARK, COLOR_TEXT_MUTED,
    BG_CARD, BG_MINT, BORDER_EMERALD, BORDER_LIGHT, FONT_MAIN
)

def build_slide(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # 1. Полноэкранный кинематографичный фон (глубокий размытый изумрудно-синий градиент)
    bg_path = Path(__file__).resolve().parent.parent / "assets" / "thank_you_bg.jpg"
    if bg_path.exists():
        apply_image_background(slide, str(bg_path))
    else:
        from theme import apply_slide_background
        apply_slide_background(slide)

    # 2. Верхний акцентный бейдж (Q&A Pill)
    pill_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(4.66), Inches(0.65), Inches(4.0), Inches(0.38)
    )
    pill_box.fill.solid()
    pill_box.fill.fore_color.rgb = RGBColor(6, 78, 59)
    pill_box.line.color.rgb = RGBColor(52, 211, 153)
    pill_box.line.width = Pt(1.5)
    tf_pill = pill_box.text_frame
    tf_pill.word_wrap = False
    tf_pill.margin_left = tf_pill.margin_right = tf_pill.margin_top = tf_pill.margin_bottom = 0
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = "ФИНАЛ • ВОПРОСЫ И ОТВЕТЫ (Q&A)"
    p_pill.alignment = PP_ALIGN.CENTER
    p_pill.font.name = FONT_MAIN
    p_pill.font.size = Pt(10)
    p_pill.font.bold = True
    p_pill.font.color.rgb = RGBColor(167, 243, 208)

    # 3. Главный заголовок: СПАСИБО ЗА ВНИМАНИЕ!
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.20), Inches(11.333), Inches(0.85))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = "СПАСИБО ЗА ВНИМАНИЕ!"
    p_title.alignment = PP_ALIGN.CENTER
    p_title.font.name = FONT_MAIN
    p_title.font.size = Pt(40)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)

    # 4. Подзаголовок платформы RiskTwin
    sub_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.10), Inches(11.333), Inches(0.55))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "RiskTwin: Интеллектуальный цифровой двойник кредитного риска и превентивной реструктуризации"
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.name = FONT_MAIN
    p_sub.font.size = Pt(15.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = RGBColor(110, 231, 183)

    # -------------------------------------------------------------------------
    # СРЕДНИЙ РЯД: 3 карточки с ключевыми итогами платформы (Контрастные на темном фоне)
    # -------------------------------------------------------------------------
    cards_data = [
        {
            "icon": "brain",
            "tag": "НЕЙРОСЕТЕВОЙ ПЕРЕХВАТ 24/7",
            "title": "PyTorch & Stalker Engine",
            "desc": (
                "Раннее обнаружение финансового и биоповеденческого стресса за 30–45 дней "
                "до первой просрочки по цепочке микро-транзакций и ночной активности в ДБО."
            )
        },
        {
            "icon": "cpu",
            "tag": "МАТЕМАТИЧЕСКИЙ РЕШАТЕЛЬ",
            "title": "Google OR-Tools MILP",
            "desc": (
                "Мгновенный расчет 3 щадящих графиков с КДН ≤ 50% менее чем за 15 мс "
                "без участия кредитного комитета: отсрочка, каникулы и снижение платежа."
            )
        },
        {
            "icon": "shield-check",
            "tag": "ЭКОНОМИКА И РЕГУЛЯТОР РК",
            "title": "₸1.4 млрд и комплаенс АРРФР",
            "desc": (
                "Удержание кредитов в Stage 1 (МСФО 9), нулевые резервные провизии, "
                "чистая кредитная история заемщика в ГКБ и готовность к стандарту TLAC 2026."
            )
        }
    ]

    card_w = Inches(3.60)
    card_gap = Inches(0.26)
    c_start_x = Inches(1.0)
    c_top = Inches(2.85)
    c_height = Inches(2.65)

    for i, c in enumerate(cards_data):
        cx = c_start_x + i * (card_w + card_gap)

        # Подложка карточки: темный slate-900 с изумрудной рамкой
        card_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, c_top, card_w, c_height)
        card_shape.fill.solid()
        card_shape.fill.fore_color.rgb = RGBColor(15, 23, 42)
        card_shape.line.color.rgb = RGBColor(5, 150, 105)
        card_shape.line.width = Pt(1.5)

        # Бейдж-иконка
        add_icon_badge(
            slide, c["icon"],
            cx + Inches(0.20), c_top + Inches(0.22),
            badge_size=Inches(0.55), icon_size=Inches(0.34),
            bg_color=RGBColor(6, 78, 59), border_color=RGBColor(52, 211, 153), color_hex="#34D399"
        )

        # Текстовый блок карточки
        c_box = slide.shapes.add_textbox(cx + Inches(0.20), c_top + Inches(0.90), card_w - Inches(0.40), Inches(1.65))
        c_tf = c_box.text_frame
        c_tf.word_wrap = True
        c_tf.margin_left = c_tf.margin_right = c_tf.margin_top = c_tf.margin_bottom = 0

        p_tag = c_tf.paragraphs[0]
        p_tag.text = c["tag"]
        p_tag.font.name = FONT_MAIN
        p_tag.font.size = Pt(8.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = RGBColor(52, 211, 153)

        p_ctitle = c_tf.add_paragraph()
        p_ctitle.text = c["title"]
        p_ctitle.font.name = FONT_MAIN
        p_ctitle.font.size = Pt(12)
        p_ctitle.font.bold = True
        p_ctitle.font.color.rgb = RGBColor(255, 255, 255)
        p_ctitle.space_before = Pt(3)

        p_cdesc = c_tf.add_paragraph()
        p_cdesc.text = c["desc"]
        p_cdesc.font.name = FONT_MAIN
        p_cdesc.font.size = Pt(9.2)
        p_cdesc.font.color.rgb = RGBColor(226, 232, 240)
        p_cdesc.space_before = Pt(5)

    # -------------------------------------------------------------------------
    # НИЖНИЙ БЛОК: Контакты, статус конкурса и готовность к демо
    # -------------------------------------------------------------------------
    bot_shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1.0), Inches(5.75), Inches(11.333), Inches(1.10)
    )
    bot_shape.fill.solid()
    bot_shape.fill.fore_color.rgb = RGBColor(6, 78, 59)
    bot_shape.line.color.rgb = RGBColor(52, 211, 153)
    bot_shape.line.width = Pt(1.5)

    bot_box = slide.shapes.add_textbox(Inches(1.25), Inches(5.85), Inches(10.833), Inches(0.90))
    bot_tf = bot_box.text_frame
    bot_tf.word_wrap = True
    bot_tf.margin_left = bot_tf.margin_right = bot_tf.margin_top = bot_tf.margin_bottom = 0

    p_b1 = bot_tf.paragraphs[0]
    p_b1.text = "🏛 Республиканский конкурс студенческих проектов и исследований в области ИИ и финтеха"
    p_b1.alignment = PP_ALIGN.CENTER
    p_b1.font.name = FONT_MAIN
    p_b1.font.size = Pt(11)
    p_b1.font.bold = True
    p_b1.font.color.rgb = RGBColor(255, 255, 255)

    p_b2 = bot_tf.add_paragraph()
    p_b2.text = "Партнеры: АБРК • Государственное Кредитное Бюро (ГКБ) • КБТУ • NU • Bereke Bank • Mastercard • ISSAI"
    p_b2.alignment = PP_ALIGN.CENTER
    p_b2.font.name = FONT_MAIN
    p_b2.font.size = Pt(9.5)
    p_b2.font.color.rgb = RGBColor(167, 243, 208)
    p_b2.space_before = Pt(3)

    p_b3 = bot_tf.add_paragraph()
    p_b3.text = "💬 Готовы к вопросам членов жюри и демонстрации живого стенда платформы"
    p_b3.alignment = PP_ALIGN.CENTER
    p_b3.font.name = FONT_MAIN
    p_b3.font.size = Pt(9.5)
    p_b3.font.bold = True
    p_b3.font.color.rgb = RGBColor(254, 240, 138)
    p_b3.space_before = Pt(3)

    return slide
