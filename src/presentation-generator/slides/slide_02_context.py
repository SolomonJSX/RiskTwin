import os
from pathlib import Path
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from theme import (
    apply_image_background, add_header, add_footer,
    COLOR_PRIMARY, COLOR_PRIMARY_DARK, COLOR_TEXT_DARK, COLOR_TEXT_MUTED,
    COLOR_ROSE, COLOR_AMBER, FONT_MAIN
)

def build_slide(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # 1. Полноэкранный размытый фон архитектуры
    bg_path = Path(__file__).resolve().parent.parent / "assets" / "slide2_blurred_bg.jpg"
    if bg_path.exists():
        apply_image_background(slide, str(bg_path))
    else:
        from theme import apply_slide_background
        apply_slide_background(slide)

    # 2. Заголовок слайда с бейджем
    add_header(
        slide,
        tag_text="ВВЕДЕНИЕ • РЕГУЛЯТОРНЫЙ И РЫНОЧНЫЙ КОНТЕКСТ РК 2026",
        title_text="Кризис проблемных долгов и реформа АРРФР: почему банкам необходим ИИ",
        subtitle_text="Анализ ссудного портфеля РК (₸43,5 трлн), скачок NPL 90+ до 1,6 трлн ₸ и отмена господдержки из бюджета",
        title_size=Pt(19.5)
    )

    # -------------------------------------------------------------------------
    # ЛЕВАЯ КОЛОНКА: Рыночный кризис NPL 90+ и реформа АРРФР (без карточек)
    # -------------------------------------------------------------------------
    left_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tf_l = left_box.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0

    # Раздел 1: Проблемные кредиты
    p = tf_l.paragraphs[0]
    p.text = "1. Рекордный рост неработающих займов (NPL 90+)"
    p.font.name = FONT_MAIN
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_ROSE

    items_npl = [
        ("Объем NPL 90+ достиг 1,575 трлн ₸: ", "за 2025 год прирост проблемных долгов составил сразу +481 млрд тенге. Доля неработающих кредитов выросла до 3,63% от общего ссудного портфеля (который увеличился на 21,2% до 43,5 трлн тенге)."),
        ("Лидеры антирейтинга по росту NPL: ", "Halyk Bank нарастил проблемный портфель на +233 млрд ₸ (до 503,5 млрд ₸, рост более 46%), Kaspi Bank — на +150 млрд ₸ (до 442 млрд ₸). Также рост зафиксирован в ForteBank (+49 млрд), Bereke Bank (+25 млрд, доля NPL достигла 6,93%) и Bank RBK (+17,5 млрд)."),
        ("Единственное исключение: ", "только Евразийский банк сократил объем проблемных займов сразу на 48 млрд ₸ (до 60 млрд ₸, снизив долю NPL с 8,3% до 3,7%).")
    ]
    for bold_prefix, text in items_npl:
        p = tf_l.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + bold_prefix
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_TEXT_DARK
        r2 = p.add_run()
        r2.text = text
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    # Раздел 2: Новые правила АРРФР
    p = tf_l.add_paragraph()
    p.space_before = Pt(14)
    p.text = "2. Конец эпохи господдержки (Закон от января 2026 г.)"
    p.font.name = FONT_MAIN
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER

    items_arrfr = [
        ("Запрет на спасение за счет бюджета: ", "государство больше не выделяет средства Нацфонда для спасения проблемных банков. Первыми убытки обязаны нести акционеры и крупные кредиторы."),
        ("Внедрение стандарта TLAC (13% ➔ 18% к 2032 г.): ", "системно значимые банки обязаны формировать собственный запас капитала и субординированного долга для покрытия стрессовых убытков."),
        ("Раннее вмешательство регулятора: ", "АРРФР вводит превентивный надзор — регулятор вмешивается ЕЩЕ ДО наступления неплатежеспособности, принудительно требуя восстановления капитала и ликвидности.")
    ]
    for bold_prefix, text in items_arrfr:
        p = tf_l.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + bold_prefix
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_TEXT_DARK
        r2 = p.add_run()
        r2.text = text
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    # -------------------------------------------------------------------------
    # ПРАВАЯ КОЛОНКА: Надобность решения в виде ИИ (без карточек)
    # -------------------------------------------------------------------------
    right_box = slide.shapes.add_textbox(Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tf_r = right_box.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    p = tf_r.paragraphs[0]
    p.text = "3. «Слепая зона» реактивного скоринга"
    p.font.name = FONT_MAIN
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_DARK

    items_blind = [
        ("Опоздание на 90 дней: ", "традиционные CRM и отчеты кредитного бюро фиксируют дефолт постфактум. В этот момент заемщик уже погружен в кассовый разрыв и микрозаймы в МФО под 56%."),
        ("Удар по капиталу акционеров (МСФО 9): ", "при падении кредита в Stage 3 банк обязан сформировать до 100% резервов, замораживая ликвидность. Так как государство больше не спасает банки, эти списания безвозвратно сжигают частный капитал.")
    ]
    for bold_prefix, text in items_blind:
        p = tf_r.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + bold_prefix
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_TEXT_DARK
        r2 = p.add_run()
        r2.text = text
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    p = tf_r.add_paragraph()
    p.space_before = Pt(14)
    p.text = "4. Почему решение в виде ИИ жизненно необходимо"
    p.font.name = FONT_MAIN
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    items_ai = [
        ("Предиктивное окно спасения (Pre-delinquency): ", "вместо пассивного ожидания дефолта глубокая нейросеть (Dual-Tower Cross-Attention) находит скрытые маркеры стресса по телеметрии ДБО и движению средств за 30–60 дней до неплатежа с точностью ROC-AUC 0.941."),
        ("Prescriptive AI — математическая оптимизация: ", "математический солвер смешанно-целочисленного программирования (MILP) за 12 мс синтезирует щадящую реструктуризацию по нормативам АРРФР (КДН ≤ 50%), возвращая заемщика в график."),
        ("Защита капитала банка: ", "предотвращение перехода займов в неработающие сохраняет миллиарды тенге в активах и защищает акционеров от требований регулятора по докапитализации.")
    ]
    for bold_prefix, text in items_ai:
        p = tf_r.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = "• " + bold_prefix
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_PRIMARY_DARK
        r2 = p.add_run()
        r2.text = text
        r2.font.name = FONT_MAIN
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MUTED

    add_footer(slide, current_slide=2)
    return slide