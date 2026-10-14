import os
from pathlib import Path
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
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
        title_text="Терминал риск-офицера: 360° мониторинг и XAI-аудит заемщиков",
        subtitle_text="Интерфейс платформы: портфельный радар, Neuro-Symbolic вердикт LLM и модальное окно глубокого аудита",
        title_size=Pt(19.0)
    )

    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    img1_path = assets_dir / "ui_radar_top.png"
    img2_path = assets_dir / "ui_neuro_verdict.png"
    img3_path = assets_dir / "ui_audit_modal.png"

    # =========================================================================
    # КОЛОНКА 1: ВЕРХНИЙ ДАШБОРД (РАДАР И ПАСПОРТ 360°)
    # =========================================================================
    col1_left = Inches(0.80)
    col_width = Inches(3.68)

    # Рамка-подложка для первого скриншота
    add_card(slide, col1_left, Inches(1.56), col_width, Inches(2.76), bg_color=RGBColor(248, 250, 252), border_color=BORDER_LIGHT)
    if img1_path.exists():
        slide.shapes.add_picture(
            str(img1_path),
            col1_left + Inches(0.04), Inches(1.60), Inches(3.60), Inches(2.67)
        )

    # Описание под скриншотом 1
    add_card(slide, col1_left, Inches(4.38), col_width, Inches(2.06), bg_color=RGBColor(240, 253, 244), border_color=BORDER_EMERALD)

    add_icon_badge(
        slide, "bar-chart",
        col1_left + Inches(0.12), Inches(4.48),
        badge_size=Inches(0.42), icon_size=Inches(0.26),
        bg_color=RGBColor(240, 253, 244), border_color=BORDER_EMERALD, color_hex="#047857"
    )

    box1 = slide.shapes.add_textbox(col1_left + Inches(0.60), Inches(4.44), col_width - Inches(0.68), Inches(1.94))
    tf1 = box1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0

    p1_h = tf1.paragraphs[0]
    p1_h.text = "1. Радар заемщика & Паспорт 360°"
    p1_h.font.name = FONT_MAIN
    p1_h.font.size = Pt(10)
    p1_h.font.bold = True
    p1_h.font.color.rgb = COLOR_PRIMARY_DARK

    p1_desc = tf1.add_paragraph()
    p1_desc.text = (
        "• Шапка с логотипом: новый векторный ромб/радар RiskTwin и навигация 5 модулей.\n"
        "• Портфельные KPI: устойчивость 94.8%, 1 ранний сигнал, ₸14.2M сохраненных средств (+32% NPV).\n"
        "• Паспорт Армана (IT-Lead): 4-осевая лепестковая диаграмма, долг ₸2.46M, платеж ₸145k, риск PD = 1.0%.\n"
        "• Тепловая карта PyTorch: веса внимания Cross-Attention по 6 микро-транзакциям (α = 0.13…0.17)."
    )
    p1_desc.font.name = FONT_MAIN
    p1_desc.font.size = Pt(7.7)
    p1_desc.font.color.rgb = COLOR_TEXT_DARK
    p1_desc.space_before = Pt(2.0)

    # =========================================================================
    # КОЛОНКА 2: НЕЙРОСИМВОЛЬНЫЙ ВЕРДИКТ LLM И РЕЕСТР БОТОВ
    # =========================================================================
    col2_left = Inches(4.82)

    # Рамка-подложка для второго скриншота
    add_card(slide, col2_left, Inches(1.56), col_width, Inches(2.76), bg_color=RGBColor(248, 250, 252), border_color=BORDER_LIGHT)
    if img2_path.exists():
        slide.shapes.add_picture(
            str(img2_path),
            col2_left + Inches(0.04), Inches(1.60), Inches(3.60), Inches(2.73)
        )

    # Описание под скриншотом 2
    add_card(slide, col2_left, Inches(4.38), col_width, Inches(2.06), bg_color=RGBColor(238, 242, 255), border_color=RGBColor(199, 210, 254))

    add_icon_badge(
        slide, "brain",
        col2_left + Inches(0.12), Inches(4.48),
        badge_size=Inches(0.42), icon_size=Inches(0.26),
        bg_color=RGBColor(238, 242, 255), border_color=RGBColor(165, 180, 252), color_hex="#4338CA"
    )

    box2 = slide.shapes.add_textbox(col2_left + Inches(0.60), Inches(4.44), col_width - Inches(0.68), Inches(1.94))
    tf2 = box2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0

    p2_h = tf2.paragraphs[0]
    p2_h.text = "2. Вердикт LLM & Реестр ботов"
    p2_h.font.name = FONT_MAIN
    p2_h.font.size = Pt(10)
    p2_h.font.bold = True
    p2_h.font.color.rgb = RGBColor(49, 46, 129)

    p2_desc = tf2.add_paragraph()
    p2_desc.text = (
        "• Neuro-Symbolic отчет (Ollama mistral-nemo): локальный инференс на RU / KZ.\n"
        "• Чему обучилась сеть: выявлена связь кассовых просадок с ночными сессиями в ДБО за 30 дней до дефолта.\n"
        "• Контрфактический прогноз: превентивная отсрочка на 1 месяц снизит риск дефолта до безопасных 15%.\n"
        "• Реестр заемщиков: мониторинг всех ботов (Арман, Жанна, Санжар) и автовызов алгоритма «План ИИ»."
    )
    p2_desc.font.name = FONT_MAIN
    p2_desc.font.size = Pt(7.7)
    p2_desc.font.color.rgb = COLOR_TEXT_DARK
    p2_desc.space_before = Pt(2.0)

    # =========================================================================
    # КОЛОНКА 3: МОДАЛЬНЫЙ АУДИТ СТРЕССА (ЖАННА, МАРКЕТОЛОГ)
    # =========================================================================
    col3_left = Inches(8.84)

    # Рамка-подложка для третьего скриншота (квадратный)
    add_card(slide, col3_left, Inches(1.56), col_width, Inches(2.76), bg_color=RGBColor(248, 250, 252), border_color=BORDER_LIGHT)
    if img3_path.exists():
        # Центрируем квадратное изображение 2.70" x 2.70" внутри колонки 3.68"
        img3_x = col3_left + Inches(0.49)
        slide.shapes.add_picture(
            str(img3_path),
            img3_x, Inches(1.59), Inches(2.70), Inches(2.70)
        )

    # Описание под скриншотом 3
    add_card(slide, col3_left, Inches(4.38), col_width, Inches(2.06), bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))

    add_icon_badge(
        slide, "alert-triangle",
        col3_left + Inches(0.12), Inches(4.48),
        badge_size=Inches(0.42), icon_size=Inches(0.26),
        bg_color=RGBColor(254, 242, 242), border_color=RGBColor(252, 165, 165), color_hex="#DC2626"
    )

    box3 = slide.shapes.add_textbox(col3_left + Inches(0.60), Inches(4.44), col_width - Inches(0.68), Inches(1.94))
    tf3 = box3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0

    p3_h = tf3.paragraphs[0]
    p3_h.text = "3. Модальный XAI-аудит (Жанна)"
    p3_h.font.name = FONT_MAIN
    p3_h.font.size = Pt(10)
    p3_h.font.bold = True
    p3_h.font.color.rgb = RGBColor(185, 28, 28)

    p3_desc = tf3.add_paragraph()
    p3_desc.text = (
        "• Профиль уязвимости: риск PD подскочил до 15.1% (кассовый разрыв, доход ₸450k, долг ₸2.6M).\n"
        "• Хроника скрытых триггеров во времени (5 событий):\n"
        "  - День -28: исчерпание лимита карты до 82% (α = 0.22)\n"
        "  - День -21: 4 параллельные рассрочки BNPL 0-0-12 (α = 0.19)\n"
        "  - День -07: панический микрозайм в ATM ₸85k (α = 0.18)\n"
        "• Кнопка действия: мгновенный вызов «Подобрать план спасения (OR-Tools)»."
    )
    p3_desc.font.name = FONT_MAIN
    p3_desc.font.size = Pt(7.6)
    p3_desc.font.color.rgb = COLOR_TEXT_DARK
    p3_desc.space_before = Pt(2.0)

    # =========================================================================
    # НИЖНИЙ СТАТУС-БАР ТЕХНОЛОГИЙ ФРОНТЕНДА
    # =========================================================================
    bot_card = add_card(slide, Inches(0.80), Inches(6.50), Inches(11.72), Inches(0.40), bg_color=RGBColor(241, 245, 249), border_color=BORDER_LIGHT)
    bot_box = slide.shapes.add_textbox(Inches(0.90), Inches(6.53), Inches(11.50), Inches(0.34))
    tf_bot = bot_box.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_right = tf_bot.margin_top = tf_bot.margin_bottom = 0
    p_bot = tf_bot.paragraphs[0]
    p_bot.text = "⚡ Технологический стек UI: Next.js 15 App Router • Tailwind CSS • Lucide Icons • Ollama Mistral-Nemo • WebSockets Live Feed"
    p_bot.font.name = FONT_MAIN
    p_bot.font.size = Pt(8.3)
    p_bot.font.bold = True
    p_bot.font.color.rgb = COLOR_PRIMARY_DARK

    add_footer(slide, current_slide=13, total_slides=18)
    return slide
