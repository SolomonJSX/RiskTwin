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
        tag_text="ПОТОКОВЫЙ РАДАР 24/7 • STREAMING ARCHITECTURE",
        title_text="Stalker Engine: Потоковый радар стресс-событий на .NET 8",
        subtitle_text="Круглосуточный мониторинг транзакций, мгновенный перехват аномалий и WebSockets-алерты риск-офицерам",
        title_size=Pt(19.5)
    )

    # -------------------------------------------------------------------------
    # ЛЕВАЯ СТОРОНА: Векторная схема Stalker Engine (Пропорция 1:1, без растяжения)
    # -------------------------------------------------------------------------
    diagram_path = Path(__file__).resolve().parent.parent / "assets" / "stalker_engine.png"
    if diagram_path.exists():
        slide.shapes.add_picture(
            str(diagram_path),
            Inches(0.8), Inches(1.72), Inches(6.9), Inches(5.12)
        )

    # -------------------------------------------------------------------------
    # ПРАВАЯ СТОРОНА: Три карточки о возможностях радара Stalker
    # -------------------------------------------------------------------------

    # 1. Карточка 1: Перехват 6 потоковых триггеров (Красный акцент)
    add_card(slide, Inches(7.9), Inches(1.72), Inches(4.65), Inches(1.5), bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))

    add_icon_badge(
        slide, "shield-check",
        Inches(8.05), Inches(1.88),
        badge_size=Inches(0.52), icon_size=Inches(0.32),
        bg_color=RGBColor(254, 242, 242), border_color=RGBColor(252, 165, 165), color_hex="#DC2626"
    )

    box1 = slide.shapes.add_textbox(Inches(8.72), Inches(1.8), Inches(3.72), Inches(1.35))
    tf1 = box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p1_h = tf1.paragraphs[0]
    p1_h.text = "1. Перехват 6 потоковых триггеров"
    p1_h.font.name = FONT_MAIN
    p1_h.font.size = Pt(11)
    p1_h.font.bold = True
    p1_h.font.color.rgb = RGBColor(185, 28, 28)

    p1_b = tf1.add_paragraph()
    p1_b.text = (
        "Радар в реальном времени ловит критические события: перевод в МФО (ΔRisk = +0.42), "
        "задержку зарплаты на 7+ дней (+0.35), обвал дохода >30% (+0.38), перегрузку рассрочками BNPL "
        "(Kaspi/Halyk 0-0-24) и критическое обнуление остатка (<1000 ₸) до платежа."
    )
    p1_b.font.name = FONT_MAIN
    p1_b.font.size = Pt(8.5)
    p1_b.font.color.rgb = COLOR_TEXT_DARK
    p1_b.space_before = Pt(2.5)

    # 2. Карточка 2: Реактивное ядро на .NET 8 & WebSockets
    add_card(slide, Inches(7.9), Inches(3.32), Inches(4.65), Inches(1.5), bg_color=RGBColor(241, 245, 249), border_color=RGBColor(203, 213, 225))

    add_icon_badge(
        slide, "zap",
        Inches(8.05), Inches(3.48),
        badge_size=Inches(0.52), icon_size=Inches(0.32),
        bg_color=RGBColor(241, 245, 249), border_color=RGBColor(148, 163, 184), color_hex="#0F172A"
    )

    box2 = slide.shapes.add_textbox(Inches(8.72), Inches(3.4), Inches(3.72), Inches(1.35))
    tf2 = box2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0

    p2_h = tf2.paragraphs[0]
    p2_h.text = "2. Реактивное ядро на .NET 8 & SignalR"
    p2_h.font.name = FONT_MAIN
    p2_h.font.size = Pt(11)
    p2_h.font.bold = True
    p2_h.font.color.rgb = RGBColor(15, 23, 42)

    p2_b = tf2.add_paragraph()
    p2_b.text = (
        "Латентность обработки события <15 миллисекунд. Заемщик автоматически ставится под надзор "
        "(IsUnderStalkerWatch = true), а через WebSockets-хаб StalkerHub алерт всплывает на мониторе "
        "риск-офицера без опроса базы данных (Zero Polling)."
    )
    p2_b.font.name = FONT_MAIN
    p2_b.font.size = Pt(8.5)
    p2_b.font.color.rgb = COLOR_TEXT_DARK
    p2_b.space_before = Pt(2.5)

    # 3. Карточка 3: Двуязычная локализация и STP-действие (RU / KZ)
    add_card(slide, Inches(7.9), Inches(4.92), Inches(4.65), Inches(1.42), bg_color=BG_MINT, border_color=BORDER_EMERALD)

    add_icon_badge(
        slide, "sparkles",
        Inches(8.05), Inches(5.08),
        badge_size=Inches(0.52), icon_size=Inches(0.32),
        bg_color=BG_MINT, border_color=BORDER_EMERALD, color_hex="#047857"
    )

    box3 = slide.shapes.add_textbox(Inches(8.72), Inches(5.0), Inches(3.72), Inches(1.25))
    tf3 = box3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0

    p3_h = tf3.paragraphs[0]
    p3_h.text = "3. Двуязычные причины и STP-действие"
    p3_h.font.name = FONT_MAIN
    p3_h.font.size = Pt(11)
    p3_h.font.bold = True
    p3_h.font.color.rgb = COLOR_PRIMARY_DARK

    p3_b = tf3.add_paragraph()
    p3_b.text = (
        "Движок генерирует понятные причины на русском и казахском языках (RU / KZ) "
        "и готовое действие: перенос даты под зарплату, консолидация рассрочек или мгновенный "
        "вызов солвера OR-Tools для синтеза 3 вариантов реструктуризации."
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
    p_bot.text = "⚡ Архитектура: .NET 8 WebApi • SignalR Hub • Clean Architecture • <15 ms"
    p_bot.font.name = FONT_MAIN
    p_bot.font.size = Pt(8.5)
    p_bot.font.bold = True
    p_bot.font.color.rgb = RGBColor(185, 28, 28)

    add_footer(slide, current_slide=11, total_slides=16)
    return slide
