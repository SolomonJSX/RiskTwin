import os
import sys
import shutil
from pathlib import Path

# Обеспечиваем корректный вывод UTF-8 в любой Windows-консоли (PowerShell / CMD)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Автоматическое подключение модуля presentation-generator к путям поиска
ROOT_DIR = Path(__file__).resolve().parent
GENERATOR_DIR = ROOT_DIR / "src" / "presentation-generator"

if str(GENERATOR_DIR) not in sys.path:
    sys.path.insert(0, str(GENERATOR_DIR))

try:
    from builder import build_presentation
except ImportError:
    # Если запуск вне виртуального окружения, подсказываем команду запуска
    print("[ERROR] Не найдены зависимости (python-pptx, pillow, resvg-py).")
    print("Запустите сборку командой:")
    print(r"  .\src\presentation-generator\.venv\Scripts\python.exe main.py")
    sys.exit(1)


def main():
    print("=" * 65)
    print("RiskTwin • Сборка презентации Pitch-Deck (PPTX)")
    print("=" * 65)

    output_dir = ROOT_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    target_pptx = output_dir / "RiskTwin_PitchDeck.pptx"

    result_path = build_presentation(str(target_pptx))

    # Автоматическая синхронизация с папкой docs/
    docs_dir = ROOT_DIR / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    docs_pptx = docs_dir / "RiskTwin_PitchDeck.pptx"
    try:
        shutil.copy2(result_path, docs_pptx)
        print(f"[+] Копия также синхронизирована в: {docs_pptx}")
    except Exception as e:
        print(f"[!] Предупреждение при копировании в docs: {e}")

    print("\n[OK] Готово! Презентация успешно собрана.")
    print(f"Файл: {result_path}")
    print("=" * 65)


if __name__ == "__main__":
    main()
