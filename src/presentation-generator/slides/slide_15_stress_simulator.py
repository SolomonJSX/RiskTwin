import os
from pathlib import Path
from pptx.util import Inches, Pt
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
        tag_text="РАЗДЕЛ IV • ЖИВОЙ ИНТЕРФЕЙС ПЛАТФОРМЫ",
        title_text="Стресс-тестирование: Интерактивное моделирование шоков",
        subtitle_text="Сценарный симулятор кассовых разрывов заемщика на 6 месяцев с автовызовом превентивного спасения",
        title_size=Pt(19.0)
    )

    # -------------------------------------------------------------------------
    # ЛЕВАЯ СТОРОНА: Скриншот стресс-симулятора (ui_stress_simulator.png)
    # -------------------------------------------------------------------------
    img_path = Path(__file__).resolve().parent.parent / "assets" / "ui_stress_simulator.png"

    # Размеры скриншота: 1007 x 723 (1.393 : 1)
    # Рамка: Ширина 6.85", Высота 5.05"
    add_card(slide, Inches(0.80), Inches(1.68), Inches(6.85), Inches(5.15), bg_color=RGBColor(248, 250, 252), border_color=BORDER_LIGHT)

    if img_path.exists():
        slide.shapes.add_picture(
            str(img_path),
            Inches(0.85), Inches(1.73), Inches(6.75), Inches(5.00)
        )

    # -------------------------------------------------------------------------
    # ПРАВАЯ СТОРОНА: Три карточки о возможностях симулятора
    # -------------------------------------------------------------------------
    right_left = Inches(7.85)
    card_width = Inches(4.68)

    # 1. Карточка 1: Интерактивные ползунки шоков (Изумрудный акцент)
    add_card(slide, right_left, Inches(1.68), card_width, Inches(1.52), bg_color=BG_MINT, border_color=BORDER_EMERALD)

    add_icon_badge(
        slide, "sliders",
        right_left + Inches(0.15), Inches(1.82),
        badge_size=Inches(0.50), icon_size=Inches(0.30),
        bg_color=BG_MINT, border_color=BORDER_EMERALD, color_hex="#047857"
    )

    box1 = slide.shapes.add_textbox(right_left + Inches(0.78), Inches(1.74), card_width - Inches(0.88), Inches(1.40))
    tf1 = box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p1_h = tf1.paragraphs[0]
    p1_h.text = "1. Ползунки стресс-шоков в реальном времени"
    p1_h.font.name = FONT_MAIN
    p1_h.font.size = Pt(10.5)
    p1_h.font.bold = True
    p1_h.font.color.rgb = COLOR_PRIMARY_DARK

    p1_b = tf1.add_paragraph()
    p1_b.text = (
        "Риск-офицер может моделировать стресс-сценарии для любого заемщика: обвал зарплаты (-10%…-50%), "
        "займы в сторонних МФО (+₸300 000) и внезапные медицинские/бытовые расходы (до ₸400 000). "
        "Система на лету пересчитывает коэффициент долговой нагрузки (КДН = 44% — зона напряжения)."
    )
    p1_b.font.name = FONT_MAIN
    p1_b.font.size = Pt(8.3)
    p1_b.font.color.rgb = COLOR_TEXT_DARK
    p1_b.space_before = Pt(2.5)

    # 2. Карточка 2: Динамический прогноз подушки на 6 месяцев (Сине-серый акцент)
    add_card(slide, right_left, Inches(3.30), card_width, Inches(1.52), bg_color=RGBColor(241, 245, 249), border_color=RGBColor(203, 213, 225))

    add_icon_badge(
        slide, "bar-chart",
        right_left + Inches(0.15), Inches(3.44),
        badge_size=Inches(0.50), icon_size=Inches(0.30),
        bg_color=RGBColor(241, 245, 249), border_color=RGBColor(148, 163, 184), color_hex="#0F172A"
    )

    box2 = slide.shapes.add_textbox(right_left + Inches(0.78), Inches(3.36), card_width - Inches(0.88), Inches(1.40))
    tf2 = box2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0

    p2_h = tf2.paragraphs[0]
    p2_h.text = "2. Динамический прогноз подушки (Cash Runway)"
    p2_h.font.name = FONT_MAIN
    p2_h.font.size = Pt(10.5)
    p2_h.font.bold = True
    p2_h.font.color.rgb = RGBColor(15, 23, 42)

    p2_b = tf2.add_paragraph()
    p2_b.text = (
        "Вместо запаздывающего ретроспективного скоринга платформа строит прогноз кривой ликвидности "
        "на 180 дней вперед. Банк заранее видит момент кассового разрыва: при шоке подушка исчерпывается "
        "за 45 дней, приводя к дефолту на 2-м месяце. Платформа упреждает дефолт до его наступления."
    )
    p2_b.font.name = FONT_MAIN
    p2_b.font.size = Pt(8.3)
    p2_b.font.color.rgb = COLOR_TEXT_DARK
    p2_b.space_before = Pt(2.5)

    # 3. Карточка 3: Кнопка спасения OR-Tools (Янтарный/Зеленый акцент)
    add_card(slide, right_left, Inches(4.92), card_width, Inches(1.45), bg_color=RGBColor(254, 243, 199), border_color=RGBColor(253, 230, 138))

    add_icon_badge(
        slide, "sparkles",
        right_left + Inches(0.15), Inches(5.06),
        badge_size=Inches(0.50), icon_size=Inches(0.30),
        bg_color=RGBColor(254, 243, 199), border_color=RGBColor(252, 211, 77), color_hex="#B45309"
    )

    box3 = slide.shapes.add_textbox(right_left + Inches(0.78), Inches(4.98), card_width - Inches(0.88), Inches(1.35))
    tf3 = box3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0

    p3_h = tf3.paragraphs[0]
    p3_h.text = "3. Кнопка «ИИ-подбор спасительного сценария»"
    p3_h.font.name = FONT_MAIN
    p3_h.font.size = Pt(10.5)
    p3_h.font.bold = True
    p3_h.font.color.rgb = RGBColor(146, 64, 14)

    p3_b = tf3.add_paragraph()
    p3_b.text = (
        "Одно нажатие на кнопку передает смоделированный стресс-вектор в Google OR-Tools MILP. "
        "Менее чем за 15 мс алгоритм синтезирует 3 варианта реструктуризации с КДН ≤ 50% "
        "и мгновенно отправляет готовый спасительный оффер в мобильное приложение клиента."
    )
    p3_b.font.name = FONT_MAIN
    p3_b.font.size = Pt(8.3)
    p3_b.font.color.rgb = COLOR_TEXT_DARK
    p3_b.space_before = Pt(2.5)

    # 4. Нижний статус-бар
    bot_card = add_card(slide, right_left, Inches(6.44), card_width, Inches(0.44), bg_color=RGBColor(241, 245, 249), border_color=BORDER_LIGHT)
    bot_box = slide.shapes.add_textbox(right_left + Inches(0.10), Inches(6.47), card_width - Inches(0.20), Inches(0.38))
    tf_bot = bot_box.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0
    p_bot = tf_bot.paragraphs[0]
    p_bot.text = "⚡ Возможности: Сценарный стресс-тест • КДН ≤ 50% • Cash Runway 180 дней • STP-решение"
    p_bot.font.name = FONT_MAIN
    p_bot.font.size = Pt(8.2)
    p_bot.font.bold = True
    p_bot.font.color.rgb = COLOR_PRIMARY_DARK

    add_footer(slide, current_slide=15, total_slides=20)
    return slide
