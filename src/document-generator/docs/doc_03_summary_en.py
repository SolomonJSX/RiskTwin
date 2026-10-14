from docx import Document
from styles import (
    apply_gost_page_setup, add_gost_paragraph, add_gost_heading
)

def build_summary_en_document(output_path: str):
    doc = Document()
    apply_gost_page_setup(doc)

    # Title
    add_gost_heading(doc, "PROJECT EXECUTIVE SUMMARY", space_before=0, space_after=4)

    # Meta
    add_gost_paragraph(
        doc,
        "Project Title: RiskTwin: Autonomous Pre-Emptive Credit Risk Twin & Restructuring Optimizer.\n"
        "Author: Zhanserik Suleimenov, Student-Researcher at Abylkas Saginov Karaganda Technical University (KarTU).\n"
        "Thematic Track: AI for Finance (Credit Scoring, Risk Forecasting, LLM Services, RegTech).",
        space_after=6
    )

    # 1. Problem
    add_gost_heading(doc, "1. Problem Statement & Banking Challenges in Kazakhstan", space_before=4, space_after=2)
    add_gost_paragraph(
        doc,
        "Rising retail indebtedness in Kazakhstan (over 8.5 million active borrowers) creates severe Non-Performing "
        "Loan (NPL) risks for commercial banks. Conventional credit scoring systems operate retrospectively: they register "
        "distress only after an actual delinquency occurs (30+ and 90+ DPD). Under IFRS 9 guidelines, this delay forces "
        "banks to freeze significant capital into Stage 3 impairment reserves, while borrowers face debt collection, "
        "destroying customer lifetime value and leading to irreversible write-offs.",
        space_after=4
    )

    # 2. Solution
    add_gost_heading(doc, "2. Proposed Solution: The RiskTwin Digital Platform", space_before=4, space_after=2)
    add_gost_paragraph(
        doc,
        "RiskTwin is an autonomous Early Warning System (EWS) that constructs a dynamic real-time digital twin of each "
        "borrower's financial-behavioral state. Rather than waiting for overdue payments, RiskTwin tracks latent distress "
        "markers (insomnia mobile banking logins between 03:00 and 05:00, steep declines in discretionary spending, initial "
        "microfinance loans). Powered by a Dual-Tower Cross-Attention neural network, RiskTwin forecasts cash flow depletion "
        "30 days ahead of default. An automated restructuring solver synthesizes 3 customized mitigation options delivered "
        "directly to the borrower's mobile banking app without collection calls.",
        space_after=4
    )

    # 3. Novelty & Metrics
    add_gost_heading(doc, "3. Scientific Novelty & Empirical Benchmark Results", space_before=4, space_after=2)
    add_gost_paragraph(
        doc,
        "The project demonstrates a Neuro-Symbolic AI framework: 1) Early default risk classification achieves "
        "AUC-ROC = 0.887 on the Home Credit Default Risk benchmark; 2) Cash runway timing error is narrowed down to "
        "MAE = ±4.2 days; 3) Full Explainable AI (XAI) transparency via TreeSHAP enables risk officers to audit the exact "
        "drivers of borrower distress; 4) A 3D biobehavioral stress twin visualizes real-time distress signals.",
        space_after=4
    )

    # 4. Economic Value
    add_gost_heading(doc, "4. Banking Impact, Regulatory Compliance & Readiness (TRL 6–7)", space_before=4, space_after=2)
    add_gost_paragraph(
        doc,
        "By resolving credit stress prior to Day 1 delinquency, RiskTwin maintains loans in IFRS 9 Stage 2, preserving "
        "regulatory capital and increasing overall debt recovery by 35–40%. Built on enterprise microservices (.NET Core 8 WebAPI, "
        "gRPC, Next.js, Apache Kafka, PyTorch), RiskTwin is ready for pilot deployment in partner bank environments "
        "(Bereke Bank, First Credit Bureau, Halyk Bank, Kaspi Bank).",
        space_after=0
    )

    doc.save(output_path)
    print(f"[OK] Generated: {output_path}")

if __name__ == "__main__":
    build_summary_en_document("test_summary_en.docx")
