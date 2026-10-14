import sys
import shutil
from pathlib import Path

# Поддержка UTF-8 консоли Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from builder import build_presentation

def main():
    base_dir = Path(__file__).resolve().parent
    output_file = base_dir / "output" / "RiskTwin_PitchDeck.pptx"
    
    print("=" * 60)
    print("RiskTwin • Automated PPTX Pitch Deck Generator")
    print("=" * 60)
    
    result_path = build_presentation(str(output_file))
    
    # Также синхронизируем с корневой папкой docs/
    docs_copy = base_dir.parent.parent / "docs" / "RiskTwin_PitchDeck.pptx"
    try:
        docs_copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(result_path, docs_copy)
        print(f"[+] Синхронизировано в: {docs_copy}")
    except Exception:
        pass
        
    print(f"\n[OK] Готово! Файл презентации успешно сформирован: {result_path}")

if __name__ == "__main__":
    main()
