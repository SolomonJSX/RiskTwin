import os
from pathlib import Path
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from theme import (
    apply_slide_background, add_header, add_footer, add_card, add_icon_badge,
    COLOR_PRIMARY, COLOR_PRIMARY_DARK, COLOR_TEXT_DARK, COLOR_TEXT_MUTED,
    BG_CARD, BG_MINT, BORDER_EMERALD, BORDER_LIGHT, FONT_MAIN
)

# Home Credit Brand Colors
COLOR_HC_RED = RGBColor(238, 49, 36)       # #EE3124 - Home Credit Red
COLOR_HC_DARKRED = RGBColor(185, 28, 28)   # #B91C1C
BG_HC_LIGHT = RGBColor(254, 242, 242)      # #FEF2F2
BORDER_HC_RED = RGBColor(254, 202, 202)    # #FECACA

def build_slide(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide)

    # 1. Заголовок слайда с бейджем
    add_header(
        slide,
        tag_text="ИСТОЧНИКИ ДАННЫХ И ПАЙПЛАЙН • 360° DATASET",
        title_text="Фундамент RiskTwin: Бенчмарк Home Credit & Цифровая телеметрия",
        subtitle_text="Сборка 6 реляционных таблиц банковского портфеля и цифрового следа в единый паспорт цифрового двойника",
        title_size=Pt(19.5)
    )

    # -------------------------------------------------------------------------
    # ЛЕВАЯ СТОРОНА: Схема цепочек реляционных данных Home Credit (SVG->PNG)
    # -------------------------------------------------------------------------
    schema_path = Path(__file__).resolve().parent.parent / "assets" / "home_credit_dataset_schema.png"
    if schema_path.exists():
        slide.shapes.add_picture(
            str(schema_path),
            Inches(0.8), Inches(1.72), Inches(6.9), Inches(5.12)
        )

    # -------------------------------------------------------------------------
    # ПРАВАЯ СТОРОНА: Карточки описания цепочек данных + Наклоненный логотип Home Credit
    # -------------------------------------------------------------------------
    
    # 1. Карточка 1: Реляционное ядро Home Credit (Красный акцент Home Credit)
    card1 = add_card(slide, Inches(7.9), Inches(1.72), Inches(4.65), Inches(1.5), bg_color=BG_HC_LIGHT, border_color=BORDER_HC_RED)
    
    add_icon_badge(
        slide, "database",
        Inches(8.05), Inches(1.88),
        badge_size=Inches(0.52), icon_size=Inches(0.32),
        bg_color=BG_HC_LIGHT, border_color=BORDER_HC_RED, color_hex="#EE3124"
    )

    box1 = slide.shapes.add_textbox(Inches(8.72), Inches(1.8), Inches(3.72), Inches(1.35))
    tf1 = box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p1_h = tf1.paragraphs[0]
    p1_h.text = "1. Ядро Home Credit: 307 511 анкет"
    p1_h.font.name = FONT_MAIN
    p1_h.font.size = Pt(11)
    p1_h.font.bold = True
    p1_h.font.color.rgb = COLOR_HC_DARKRED

    p1_b = tf1.add_paragraph()
    p1_b.text = (
        "Мировой бенчмарк банковского скоринга (Kaggle). Базовая анкета application_train: "
        "доход, долговая нагрузка DTI, аннуитет, срок займа, стаж работы и скоринги внешних бюро EXT_SOURCE 1–3."
    )
    p1_b.font.name = FONT_MAIN
    p1_b.font.size = Pt(8.6)
    p1_b.font.color.rgb = COLOR_TEXT_DARK
    p1_b.space_before = Pt(2.5)

    # 2. Карточка 2: Цепочки транзакций и товарных рассрочек (27.4 млн записей)
    card2 = add_card(slide, Inches(7.9), Inches(3.32), Inches(4.65), Inches(1.5), bg_color=RGBColor(248, 250, 252), border_color=BORDER_LIGHT)

    add_icon_badge(
        slide, "layers",
        Inches(8.05), Inches(3.48),
        badge_size=Inches(0.52), icon_size=Inches(0.32),
        bg_color=BG_MINT, border_color=BORDER_EMERALD, color_hex="#047857"
    )

    box2 = slide.shapes.add_textbox(Inches(8.72), Inches(3.4), Inches(3.72), Inches(1.35))
    tf2 = box2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0

    p2_h = tf2.paragraphs[0]
    p2_h.text = "2. Цепочки транзакций и рассрочек"
    p2_h.font.name = FONT_MAIN
    p2_h.font.size = Pt(11)
    p2_h.font.bold = True
    p2_h.font.color.rgb = COLOR_TEXT_DARK

    p2_b = tf2.add_paragraph()
    p2_b.text = (
        "• installments_payments (13.6M) — задержки оплат и кассовые недоборы.\n"
        "• POS_CASH_balance (10.0M) — товарные рассрочки 0-0-12 (Kaspi Red аналог).\n"
        "• credit_card_balance (3.8M) — снятия наличных в ATM и утилизация лимита."
    )
    p2_b.font.name = FONT_MAIN
    p2_b.font.size = Pt(8.4)
    p2_b.font.color.rgb = COLOR_TEXT_MUTED
    p2_b.space_before = Pt(2.5)

    # 3. Карточка 3: Внешнее бюро (ГКБ) + Поведенческая телеметрия
    card3 = add_card(slide, Inches(7.9), Inches(4.92), Inches(4.65), Inches(1.42), bg_color=BG_MINT, border_color=BORDER_EMERALD)

    add_icon_badge(
        slide, "shield-check",
        Inches(8.05), Inches(5.08),
        badge_size=Inches(0.52), icon_size=Inches(0.32),
        bg_color=BG_MINT, border_color=BORDER_EMERALD, color_hex="#047857"
    )

    box3 = slide.shapes.add_textbox(Inches(8.72), Inches(5.0), Inches(3.72), Inches(1.25))
    tf3 = box3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0

    p3_h = tf3.paragraphs[0]
    p3_h.text = "3. Внешний долг (ГКБ) + Телеметрия ДБО"
    p3_h.font.name = FONT_MAIN
    p3_h.font.size = Pt(11)
    p3_h.font.bold = True
    p3_h.font.color.rgb = COLOR_PRIMARY_DARK

    p3_b = tf3.add_paragraph()
    p3_b.text = (
        "bureau.csv (1.7M) фиксирует долги заемщика в сторонних банках РК. "
        "Инновация RiskTwin — синтез цифрового следа мобильного приложения: ночные входы (3:00 AM), "
        "падение медианного баланса 7d и хаотичность P2P-переводов."
    )
    p3_b.font.name = FONT_MAIN
    p3_b.font.size = Pt(8.4)
    p3_b.font.color.rgb = COLOR_TEXT_DARK
    p3_b.space_before = Pt(2.5)

    # 4. Нижний статус-бар слияния в Parquet
    bot_card = add_card(slide, Inches(7.9), Inches(6.42), Inches(4.65), Inches(0.44), bg_color=RGBColor(241, 245, 249), border_color=BORDER_LIGHT)
    bot_box = slide.shapes.add_textbox(Inches(8.0), Inches(6.45), Inches(4.45), Inches(0.38))
    tf_bot = bot_box.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0
    p_bot = tf_bot.paragraphs[0]
    p_bot.text = "⚡ Итог: 48 признаков сведены в home_credit_full_360_prepared.parquet (ROC-AUC 0.941)"
    p_bot.font.name = FONT_MAIN
    p_bot.font.size = Pt(8.5)
    p_bot.font.bold = True
    p_bot.font.color.rgb = COLOR_HC_DARKRED

    # -------------------------------------------------------------------------
    # ПЕРЕВЕРНУТЫЙ / НАКЛОНЕННЫЙ ЛОГОТИП HOME CREDIT BANK (Как печать / стикер)
    # -------------------------------------------------------------------------
    hc_logo_path = Path(__file__).resolve().parent.parent / "assets" / "home_credit_logo.png"
    if hc_logo_path.exists():
        # Повернутый логотип-стикер в верхнем правом секторе (без наложений)
        pic1 = slide.shapes.add_picture(
            str(hc_logo_path),
            Inches(10.6), Inches(0.70), Inches(1.85), Inches(0.74)
        )
        pic1.rotation = 348.0  # Наклон -12 градусов (динамичный сертифицированный стикер)

    add_footer(slide, current_slide=5, total_slides=12)
    return slide
