import asyncio
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.table import Table

from app.llm.ollama_client import OllamaPersonaGenerator
from app.behavioral.distribution_engine import BehavioralDistributionEngine
from app.domain.models import SyntheticBorrowerRecord
from app.exporters.csv_exporter import CsvDatasetExporter

console = Console()


async def generate_dataset(total_records: int = 15, batch_size: int = 5):
    console.print("[bold cyan]════════════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold yellow]🚀 RiskTwin Synthetic Data Generator (Zero-shot Ollama / Mistral-Nemo)[/bold yellow]")
    console.print("[bold cyan]════════════════════════════════════════════════════════════════[/bold cyan]\n")

    generator = OllamaPersonaGenerator(model="mistral-nemo:12b")
    engine = BehavioralDistributionEngine()
    records: list[SyntheticBorrowerRecord] = []

    batches_needed = (total_records + batch_size - 1) // batch_size

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[green]Генерация персон через LLM...", total=total_records)

        for b in range(batches_needed):
            current_batch_size = min(batch_size, total_records - len(records))
            if current_batch_size <= 0:
                break

            personas = await generator.generate_batch(batch_size=current_batch_size)

            for persona in personas:
                feats, target, days = engine.generate_features_for_persona(persona)
                record = SyntheticBorrowerRecord(
                    persona=persona,
                    features=feats,
                    target_default_30d=target,
                    predicted_days_to_default=days,
                )
                records.append(record)
                progress.advance(task, 1)

    # Экспорт в папку обучения ML-движка
    out_dir = Path(__file__).resolve().parent.parent / "ml-engine" / "training"
    csv_file = out_dir / "credit_behavior_dataset.csv"
    df = CsvDatasetExporter.export(records, csv_file)

    console.print(f"\n[bold green]✅ Датасет успешно сформирован и сохранен:[/bold green] [white]{csv_file}[/white]")

    # Красивая сводная таблица
    table = Table(title="📊 Статистика сгенерированного датасета")
    table.add_column("Метрика", style="cyan")
    table.add_column("Значение", style="magenta")

    table.add_row("Всего заемщиков", str(len(df)))
    table.add_row("Доля преддефолтных (Risk Rate)", f"{df['target_default_30d'].mean():.1%}")
    table.add_row("Средний возраст", f"{df['age'].mean():.1f} лет")
    table.add_row("Средний доход", f"{df['declared_income'].mean():,.0f} KZT")
    table.add_row("Уникальных городов", str(df["city"].nunique()))

    console.print(table)


if __name__ == "__main__":
    # 1000 заемщиков батчами по 10 штук на вашей RTX 3060 12GB
    asyncio.run(generate_dataset(total_records=1000, batch_size=10))