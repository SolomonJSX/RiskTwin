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

def build_slide(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide)

    # 1. Заголовок слайда с бейджем
    add_header(
        slide,
        tag_text="ПСИХОМЕТРИЧЕСКИЙ АНАЛИЗ • DEEP BEHAVIORAL AI",
        title_text="Psycho-Life Service: Извлечение скрытого стресса из данных",
        subtitle_text="Как паттерны бессонницы, тревожности в ДБО и микрозаймов меняют оценку кредитного риска",
        title_size=Pt(19.5)
    )

    # -------------------------------------------------------------------------
    # ЛЕВАЯ СТОРОНА: Векторная схема анализа закономерностей (Пропорция 1:1, без растяжения)
    # -------------------------------------------------------------------------
    diagram_path = Path(__file__).resolve().parent.parent / "assets" / "psycho_life_engine.png"
    if diagram_path.exists():
        slide.shapes.add_picture(
            str(diagram_path),
            Inches(0.8), Inches(1.72), Inches(6.9), Inches(5.12)
        )

    # -------------------------------------------------------------------------
    # ПРАВАЯ СТОРОНА: Три карточки о методологии и влиянии на результат
    # -------------------------------------------------------------------------

    # 1. Карточка 1: Пассивное считывание без опросов (Фиолетовый акцент)
    add_card(slide, Inches(7.9), Inches(1.72), Inches(4.65), Inches(1.5), bg_color=RGBColor(250, 245, 255), border_color=RGBColor(233, 213, 255))

    add_icon_badge(
        slide, "brain",
        Inches(8.05), Inches(1.88),
        badge_size=Inches(0.52), icon_size=Inches(0.32),
        bg_color=RGBColor(250, 245, 255), border_color=RGBColor(216, 180, 254), color_hex="#7E22CE"
    )

    box1 = slide.shapes.add_textbox(Inches(8.72), Inches(1.8), Inches(3.72), Inches(1.35))
    tf1 = box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p1_h = tf1.paragraphs[0]
    p1_h.text = "1. Считывание стресса без опросов"
    p1_h.font.name = FONT_MAIN
    p1_h.font.size = Pt(11)
    p1_h.font.bold = True
    p1_h.font.color.rgb = RGBColor(126, 34, 206)

    p1_b = tf1.add_paragraph()
    p1_b.text = (
        "Клиент не заполняет тесты. Сервис вычисляет 9 маркеров из обычного цифрового следа: "
        "входы в приложение в 3:00–5:00 утра (бессонница), зависание на экране графика (95 сек.), "
        "проверка баланса по 10 раз в день, спад трат на себя и микрозаймы в МФО."
    )
    p1_b.font.name = FONT_MAIN
    p1_b.font.size = Pt(8.5)
    p1_b.font.color.rgb = COLOR_TEXT_DARK
    p1_b.space_before = Pt(2.5)

    # 2. Карточка 2: Как психология влияет на результат (Синергия Cross-Attention)
    add_card(slide, Inches(7.9), Inches(3.32), Inches(4.65), Inches(1.5), bg_color=RGBColor(238, 242, 255), border_color=RGBColor(199, 210, 254))

    add_icon_badge(
        slide, "zap",
        Inches(8.05), Inches(3.48),
        badge_size=Inches(0.52), icon_size=Inches(0.32),
        bg_color=RGBColor(238, 242, 255), border_color=RGBColor(199, 210, 254), color_hex="#1D4ED8"
    )

    box2 = slide.shapes.add_textbox(Inches(8.72), Inches(3.4), Inches(3.72), Inches(1.35))
    tf2 = box2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0

    p2_h = tf2.paragraphs[0]
    p2_h.text = "2. Влияние психологии на оценку риска"
    p2_h.font.name = FONT_MAIN
    p2_h.font.size = Pt(11)
    p2_h.font.bold = True
    p2_h.font.color.rgb = RGBColor(29, 78, 216)

    p2_b = tf2.add_paragraph()
    p2_b.text = (
        "Обычный скоринг считает клиента надежным (доход есть, просрочек нет). "
        "Но кросс-внимание нейросети [7×9] связывает падение остатка с ночной паникой. "
        "Результат: модель мгновенно поднимает риск дефолта с 1.3% до 84.2% за месяц до просрочки."
    )
    p2_b.font.name = FONT_MAIN
    p2_b.font.size = Pt(8.5)
    p2_b.font.color.rgb = COLOR_TEXT_DARK
    p2_b.space_before = Pt(2.5)

    # 3. Карточка 3: XAI Объяснимость (TreeSHAP)
    add_card(slide, Inches(7.9), Inches(4.92), Inches(4.65), Inches(1.42), bg_color=BG_MINT, border_color=BORDER_EMERALD)

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
    p3_h.text = "3. Прозрачный XAI-диагноз для Банка"
    p3_h.font.name = FONT_MAIN
    p3_h.font.size = Pt(11)
    p3_h.font.bold = True
    p3_h.font.color.rgb = COLOR_PRIMARY_DARK

    p3_b = tf3.add_paragraph()
    p3_b.text = (
        "Риск-офицер банка видит реальную первопричину кризиса: «Стресс вызван внезапным "
        "медицинским шоком и кассовым разрывом, а не недобросовестностью заемщика». "
        "Это защищает банк от ошибок и позволяет предложить помощь вовремя."
    )
    p3_b.font.name = FONT_MAIN
    p3_b.font.size = Pt(8.4)
    p3_b.font.color.rgb = COLOR_TEXT_DARK
    p3_b.space_before = Pt(2.5)

    # 4. Нижний статус-бар
    bot_card = add_card(slide, Inches(7.9), Inches(6.42), Inches(4.65), Inches(0.44), bg_color=RGBColor(241, 245, 249), border_color=BORDER_LIGHT)
    bot_box = slide.shapes.add_textbox(Inches(8.0), Inches(6.45), Inches(4.45), Inches(0.38))
    tf_bot = bot_box.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0
    p_bot = tf_bot.paragraphs[0]
    p_bot.text = "⚡ Метрики: 9 психо-маркеров • ROC-AUC: 0.941 • 100% Privacy & АРРФР Комплаенс"
    p_bot.font.name = FONT_MAIN
    p_bot.font.size = Pt(8.5)
    p_bot.font.bold = True
    p_bot.font.color.rgb = RGBColor(126, 34, 206)

    add_footer(slide, current_slide=10, total_slides=16)
    return slide
