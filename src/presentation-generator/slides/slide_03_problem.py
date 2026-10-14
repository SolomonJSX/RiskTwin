import os
from pathlib import Path
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from theme import (
    apply_slide_background, add_header, add_footer, add_icon_badge,
    COLOR_PRIMARY_DARK, COLOR_TEXT_DARK, COLOR_TEXT_MUTED,
    COLOR_AMBER, BG_AMBER_LIGHT, FONT_MAIN
)

def build_slide(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide)

    # 1. Заголовок слайда с бейджем
    add_header(
        slide,
        tag_text="ГЕНЕЗИС ИДЕИ • АРХИТЕКТУРНЫЙ ПОДХОД",
        title_text="От пассивных дашбордов к операционной системе: вдохновение подходом Palantir",
        subtitle_text="Почему классическая банковская BI-аналитика бессильна и как концепция Digital Twin меняет управление рисками",
        title_size=Pt(19.5)
    )

    # 2. Иконка лампочки в верхнем левом углу
    add_icon_badge(
        slide, "lightbulb",
        Inches(0.8), Inches(0.33),
        badge_size=Inches(0.36), icon_size=Inches(0.24),
        bg_color=BG_AMBER_LIGHT, border_color=COLOR_AMBER, color_hex="#D97706"
    )

    # -------------------------------------------------------------------------
    # ЛЕВАЯ СТОРОНА: Векторная схема Palantir Ontology
    # -------------------------------------------------------------------------
    diagram_path = Path(__file__).resolve().parent.parent / "assets" / "palantir_concept.png"
    if diagram_path.exists():
        slide.shapes.add_picture(
            str(diagram_path),
            Inches(0.8), Inches(1.8), Inches(5.5), Inches(4.9)
        )

    # -------------------------------------------------------------------------
    # ПРАВАЯ СТОРОНА: Единая связная статья от 1-го лица (курсив, крупный шрифт)
    # -------------------------------------------------------------------------
    right_box = slide.shapes.add_textbox(Inches(6.55), Inches(1.75), Inches(5.95), Inches(5.1))
    tf_r = right_box.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0

    # Заголовок истории
    p_title = tf_r.paragraphs[0]
    p_title.text = "Как родилась идея: от тупика отчетов к философии Palantir"
    p_title.font.name = FONT_MAIN
    p_title.font.size = Pt(14)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_TEXT_DARK

    # Абзац 1: Проблема банков и поиск идеи
    p1 = tf_r.add_paragraph()
    p1.text = (
        "«Изучая банковский сектор Казахстана, я натолкнулся на поразительный парадокс: "
        "у наших банков накоплены терабайты ценнейших данных — миллионы транзакций Kaspi и Halyk, "
        "логи мобильных приложений, остатки на счетах и кредитные истории. Но все это лежит «мертвым грузом» "
        "в разрозненных департаментах. Банковский риск-менеджмент смотрит на мир через пассивные дашборды, "
        "которые просто констатируют катастрофу: когда клиент уже 90 дней не платит, его кредитный рейтинг "
        "уничтожен, а банк вынужден списывать капитал в 100% резервы.»"
    )
    p1.font.name = FONT_MAIN
    p1.font.size = Pt(11.5)
    p1.font.italic = True
    p1.font.color.rgb = COLOR_TEXT_DARK
    p1.space_before = Pt(10)

    # Абзац 2: Что такое Palantir и почему возникла эта мысль
    p2 = tf_r.add_paragraph()
    p2.text = (
        "«Я стал искать: как управляют критическими рисками в индустриях с нулевой терпимостью к ошибкам? "
        "Так я пришел к технологической философии Palantir. Их прорыв заключался в отказе от плоских таблиц "
        "в пользу «Онтологии» — создания живого Цифрового Двойника реальности. В Palantir данные превращаются "
        "в динамические связанные объекты, а главное — система замкнута на действие (Closed-Loop Decision Making): "
        "прогноз не повисает в воздухе, а мгновенно запускает конкретное операционное решение.»"
    )
    p2.font.name = FONT_MAIN
    p2.font.size = Pt(11.5)
    p2.font.italic = True
    p2.font.color.rgb = COLOR_TEXT_DARK
    p2.space_before = Pt(9)

    # Абзац 3: Идея создать специализированную мини-версию под острую проблему
    p3 = tf_r.add_paragraph()
    p3.text = (
        "«Тогда я подумал: а почему бы не создать специализированную мини-версию архитектуры Palantir, "
        "но сфокусированную на одной самой болезненной проблеме банков Казахстана — превентивном спасении "
        "заемщика до дефолта? Построить динамического цифрового двойника кредитного риска, который на основе "
        "потока транзакций непрерывно улавливает скрытый финансовый стресс за 30–60 дней до неплатежа, "
        "и вместо звонков коллекторов за миллисекунды синтезирует законный вариант реструктуризации.»"
    )
    p3.font.name = FONT_MAIN
    p3.font.size = Pt(11.5)
    p3.font.italic = True
    p3.font.color.rgb = COLOR_PRIMARY_DARK
    p3.space_before = Pt(9)

    add_footer(slide, current_slide=3)
    return slide