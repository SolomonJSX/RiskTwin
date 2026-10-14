import sys
import shutil
from pathlib import Path

# UTF-8 console for Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

base_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(base_dir))

from docs.doc_01_application import build_application_document
from docs.doc_02_summary_ru import build_summary_ru_document
from docs.doc_03_summary_en import build_summary_en_document
from docs.doc_04_one_pager import build_one_pager_document
from docs.doc_05_tech_appendix import build_tech_appendix_document

def generate_all_documents():
    out_dir = base_dir / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    repo_docs_dir = base_dir.parent.parent / "docs" / "word_docs"
    repo_docs_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("RiskTwin • Automated Official Word Documentation Generator")
    print("Competition: АБРК & ГКБ 2026 (Алматы — Астана)")
    print("=" * 65)

    docs_plan = [
        ("01_Official_Application_KarTU.docx", "Официальная заявка от КарТУ им. Сагинова", build_application_document),
        ("02_Executive_Summary_RU.docx", "Резюме проекта на русском языке (1 стр.)", build_summary_ru_document),
        ("03_Executive_Summary_EN.docx", "Project Executive Summary in English (1 page)", build_summary_en_document),
        ("04_One_Pager_RiskTwin.docx", "Executive One-Pager проекта RiskTwin (1 стр.)", build_one_pager_document),
        ("05_Technical_Appendix_TRL.docx", "Техническое приложение (Методология, Метрики, TRL)", build_tech_appendix_document),
    ]

    for filename, description, builder_func in docs_plan:
        out_file = out_dir / filename
        print(f"\n[+] Формирование: {description}...")
        builder_func(str(out_file))

        # Sync to repo docs/word_docs/
        dest_copy = repo_docs_dir / filename
        shutil.copy2(out_file, dest_copy)
        print(f"    -> Синхронизировано в: {dest_copy.relative_to(base_dir.parent.parent)}")

    print("\n" + "=" * 65)
    print("[SUCCESS] Все 5 официальных конкурсных Word документов успешно созданы!")
    print(f"Папка сохранения: {repo_docs_dir}")
    print("=" * 65)

if __name__ == "__main__":
    generate_all_documents()
