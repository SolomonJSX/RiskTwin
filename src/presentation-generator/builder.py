import os
from pptx import Presentation
from theme import SLIDE_WIDTH, SLIDE_HEIGHT

from slides.slide_01_title import build_slide as build_s1
from slides.slide_02_context import build_slide as build_s2
from slides.slide_03_problem import build_slide as build_s3
from slides.slide_04_solution import build_slide as build_s4
from slides.slide_05_intro import build_slide as build_s_intro
from slides.slide_05_dataset import build_slide as build_s5_data
from slides.slide_06_architecture import build_slide as build_s6_arch
from slides.slide_06_solver import build_slide as build_s6
from slides.slide_07_services_overview import build_slide as build_s7_overview
from slides.slide_08_psycho_life import build_slide as build_s8_psycho
from slides.slide_09_stalker_engine import build_slide as build_s9_stalker
from slides.slide_12_agent_world import build_slide as build_s12_agent_world
from slides.slide_13_ui_showcase import build_slide as build_s13_ui
from slides.slide_14_stress_twin_3d import build_slide as build_s14_stress_twin
from slides.slide_15_stress_simulator import build_slide as build_s15_stress_sim
from slides.slide_07_case_study import build_slide as build_s7
from slides.slide_16_client_portal import build_slide as build_s16_client_portal
from slides.slide_09_economics import build_slide as build_s9
from slides.slide_10_tech_stack import build_slide as build_s10
from slides.slide_11_roadmap import build_slide as build_s11
from slides.slide_21_thank_you import build_slide as build_s21_thank_you

def build_presentation(output_path: str = "output/RiskTwin_PitchDeck.pptx"):
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    print("[Presentation Builder] Building 21 RiskTwin Slides with modern Lucide icons...")
    build_s1(prs)
    build_s2(prs)
    build_s3(prs)
    build_s4(prs)
    build_s_intro(prs)
    build_s5_data(prs)
    build_s6_arch(prs)
    build_s6(prs)
    build_s7_overview(prs)
    build_s8_psycho(prs)
    build_s9_stalker(prs)
    build_s12_agent_world(prs)
    build_s13_ui(prs)
    build_s14_stress_twin(prs)
    build_s15_stress_sim(prs)
    build_s7(prs)
    build_s16_client_portal(prs)
    build_s9(prs)
    build_s10(prs)
    build_s11(prs)
    build_s21_thank_you(prs)

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        
    try:
        prs.save(output_path)
        final_path = output_path
    except PermissionError:
        base, ext = os.path.splitext(output_path)
        final_path = f"{base}_updated{ext}"
        prs.save(final_path)
        print(f"[Presentation Builder] Warning: '{output_path}' is locked by PowerPoint. Saved to '{final_path}'.")

    print(f"[Presentation Builder] Successfully generated: {final_path}")
    return final_path

if __name__ == "__main__":
    build_presentation()
