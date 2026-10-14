from pptx.util import Inches, Pt
from theme import (
    apply_slide_background, add_header, add_footer, add_card, add_icon_badge,
    COLOR_PRIMARY, COLOR_PRIMARY_DARK, COLOR_TEXT_DARK, COLOR_TEXT_MUTED,
    BG_CARD, BG_MINT, BORDER_EMERALD, FONT_MAIN
)

def build_slide(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    apply_slide_background(slide)

    add_header(
        slide,
        tag_text="Бизнес-эффект & ROI",
        title_text="Экономический эффект для казахстанского банка",
        subtitle_text="Расчет бизнес-отдачи от внедрения RiskTwin на портфель 100 000 розничных заемщиков"
    )

    # 4 Large KPI Cards with icon badges
    kpis = [
        ("-22%", "trending-down", "Снижение дефолтов (NPL)", "Удержание клиентов в Stage 1 (МСФО 9) за счет урегулирования до наступления 90 дней просрочки."),
        ("₸ 3.2 млрд", "coins", "Экономия капитала банка", "Объем высвобожденных провизий (резервов), которые банку не придется списывать из капитала."),
        ("-65%", "percent", "Расходы на Collection", "Автоматизация процесса спасения без раздувания штата операторов и судебных издержек."),
        ("+40 п.п.", "heart-handshake", "Прирост лояльности (NPS)", "Банк воспринимается заемщиком как надежный партнер, а не карательный орган.")
    ]

    for i, (metric, icon_name, label, desc) in enumerate(kpis):
        left = Inches(0.8 + (i % 2) * 6.0)
        top = Inches(1.8 + (i // 2) * 2.5)

        card = add_card(slide, left, top, Inches(5.7), Inches(2.3), bg_color=BG_MINT, border_color=BORDER_EMERALD)
        
        # Icon badge in top right of card
        add_icon_badge(
            slide, icon_name,
            left + Inches(4.8), top + Inches(0.2),
            badge_size=Inches(0.65), icon_size=Inches(0.38),
            bg_color=BG_MINT, border_color=COLOR_PRIMARY_DARK, color_hex="#047857"
        )

        box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.15), Inches(4.5), Inches(2.0))
        tf = box.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = metric
        p1.font.name = FONT_MAIN
        p1.font.size = Pt(28)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_PRIMARY_DARK

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.name = FONT_MAIN
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_DARK
        p2.space_before = Pt(3)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_MAIN
        p3.font.size = Pt(10)
        p3.font.color.rgb = COLOR_TEXT_MUTED
        p3.space_before = Pt(4)

    add_footer(slide, current_slide=9)
    return slide
