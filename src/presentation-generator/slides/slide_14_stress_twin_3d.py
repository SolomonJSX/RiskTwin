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
        title_text="3D Цифровой Психо-Двойник: Биоповеденческий аватар стресса",
        subtitle_text="Интерактивная 3D-проекция эмоционального истощения заемщика (Жанна, 95% дистресс) на основе GMM Core",
        title_size=Pt(19.0)
    )

    # -------------------------------------------------------------------------
    # ЛЕВАЯ СТОРОНА: Скриншот 3D Аватара (ui_stress_twin_3d.png) в аккуратной рамке
    # -------------------------------------------------------------------------
    img_path = Path(__file__).resolve().parent.parent / "assets" / "ui_stress_twin_3d.png"

    # Рамка-подложка: Aspect ratio 1.25 : 1 (963x770)
    # Ширина 6.45", Высота 5.16"
    add_card(slide, Inches(0.80), Inches(1.68), Inches(6.55), Inches(5.20), bg_color=RGBColor(15, 23, 42), border_color=RGBColor(51, 65, 85))

    if img_path.exists():
        slide.shapes.add_picture(
            str(img_path),
            Inches(0.85), Inches(1.73), Inches(6.45), Inches(5.10)
        )

    # -------------------------------------------------------------------------
    # ПРАВАЯ СТОРОНА: Три карточки о биоповеденческом мониторинге
    # -------------------------------------------------------------------------
    right_left = Inches(7.55)
    card_width = Inches(4.98)

    # 1. Карточка 1: 3D-Аватар и пульс финансового дистресса (Фиолетовый акцент)
    add_card(slide, right_left, Inches(1.68), card_width, Inches(1.52), bg_color=RGBColor(245, 243, 255), border_color=RGBColor(221, 214, 254))

    add_icon_badge(
        slide, "brain",
        right_left + Inches(0.15), Inches(1.82),
        badge_size=Inches(0.50), icon_size=Inches(0.30),
        bg_color=RGBColor(245, 243, 255), border_color=RGBColor(196, 181, 253), color_hex="#6D28D9"
    )

    box1 = slide.shapes.add_textbox(right_left + Inches(0.78), Inches(1.74), card_width - Inches(0.88), Inches(1.40))
    tf1 = box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p1_h = tf1.paragraphs[0]
    p1_h.text = "1. 3D-Аватар и пульс соматического стресса"
    p1_h.font.name = FONT_MAIN
    p1_h.font.size = Pt(10.5)
    p1_h.font.bold = True
    p1_h.font.color.rgb = RGBColor(88, 28, 135)

    p1_b = tf1.add_paragraph()
    p1_b.text = (
        "3D-гуманоид на WebGL в реальном времени визуализирует степень финансового истощения клиента. "
        "При достижении индекса 95% (кейс маркетолога Жанны) аватар переходит в режим "
        "«Хроническое истощение и дефолтный коллапс» с учащением кардио-ритма до 124 BPM "
        "и фиолетовой неоновой индикацией перегруженных суставов."
    )
    p1_b.font.name = FONT_MAIN
    p1_b.font.size = Pt(8.3)
    p1_b.font.color.rgb = COLOR_TEXT_DARK
    p1_b.space_before = Pt(2.5)

    # 2. Карточка 2: Объективные транзакционные маркеры Home Credit (Янтарный акцент)
    add_card(slide, right_left, Inches(3.30), card_width, Inches(1.52), bg_color=RGBColor(254, 243, 199), border_color=RGBColor(253, 230, 138))

    add_icon_badge(
        slide, "bar-chart",
        right_left + Inches(0.15), Inches(3.44),
        badge_size=Inches(0.50), icon_size=Inches(0.30),
        bg_color=RGBColor(254, 243, 199), border_color=RGBColor(252, 211, 77), color_hex="#B45309"
    )

    box2 = slide.shapes.add_textbox(right_left + Inches(0.78), Inches(3.36), card_width - Inches(0.88), Inches(1.40))
    tf2 = box2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0

    p2_h = tf2.paragraphs[0]
    p2_h.text = "2. Объективные маркеры Home Credit 360°"
    p2_h.font.name = FONT_MAIN
    p2_h.font.size = Pt(10.5)
    p2_h.font.bold = True
    p2_h.font.color.rgb = RGBColor(146, 64, 14)

    p2_b = tf2.add_paragraph()
    p2_b.text = (
        "Unsupervised GMM выявляет скрытые аномалии без субъективных опросов: "
        "задержки платежей (payment_delay_distress = 3.82 — критический маркер), перегрузку "
        "рассрочками BNPL (1.6) и паническое обналичивание кредиток в ATM (0.6). "
        "Банк фиксирует психологический кризис за 30–45 дней до фактической просрочки."
    )
    p2_b.font.name = FONT_MAIN
    p2_b.font.size = Pt(8.3)
    p2_b.font.color.rgb = COLOR_TEXT_DARK
    p2_b.space_before = Pt(2.5)

    # 3. Карточка 3: Интерактивный симулятор шоков «Что если» (Изумрудный акцент)
    add_card(slide, right_left, Inches(4.92), card_width, Inches(1.45), bg_color=BG_MINT, border_color=BORDER_EMERALD)

    add_icon_badge(
        slide, "zap",
        right_left + Inches(0.15), Inches(5.06),
        badge_size=Inches(0.50), icon_size=Inches(0.30),
        bg_color=BG_MINT, border_color=BORDER_EMERALD, color_hex="#047857"
    )

    box3 = slide.shapes.add_textbox(right_left + Inches(0.78), Inches(4.98), card_width - Inches(0.88), Inches(1.35))
    tf3 = box3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0

    p3_h = tf3.paragraphs[0]
    p3_h.text = "3. Интерактивный симулятор шоков «Что если»"
    p3_h.font.name = FONT_MAIN
    p3_h.font.size = Pt(10.5)
    p3_h.font.bold = True
    p3_h.font.color.rgb = COLOR_PRIMARY_DARK

    p3_b = tf3.add_paragraph()
    p3_b.text = (
        "Интерфейс позволяет в 1 клик протестировать устойчивость заемщика к стресс-шокам: "
        "задержка зарплаты (+10 дней), паника в ATM (₸150 000 с кредитки) или сбой автоплатежа. "
        "Кнопка «Стабилизация» мгновенно запускает OR-Tools для возврата аватара в STABLE."
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
    p_bot.text = "⚡ Технологии: Three.js WebGL 3D • Unsupervised GMM • 163 517 анкет Home Credit • <15 ms"
    p_bot.font.name = FONT_MAIN
    p_bot.font.size = Pt(8.2)
    p_bot.font.bold = True
    p_bot.font.color.rgb = RGBColor(88, 28, 135)

    add_footer(slide, current_slide=14, total_slides=19)
    return slide
