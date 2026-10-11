
import asyncio
import time
from pathlib import Path
import pandas as pd
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.table import Table

from app.llm.groq_client import GroqPsychoPersonaClient
from app.behavioral.psycho_distribution_engine import PsychoBehavioralDistributionEngine
import httpx

console = Console()


async def generate_psycho_dataset(total_records: int = 500, batch_size: int = 5):
    console.print("[bold cyan]════════════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold yellow]🧠 RiskTwin Psycho-Life Engine (Ultra-Fast Groq LPU / Llama-3.3-70B)[/bold yellow]")
    console.print("[bold cyan]════════════════════════════════════════════════════════════════[/bold cyan]\n")

    groq_client = GroqPsychoPersonaClient()
    engine = PsychoBehavioralDistributionEngine()
    records = []

    batches_needed = (total_records + batch_size - 1) // batch_size
    start_time = time.time()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[green]Генерация персон через Groq LPU...", total=total_records)

        for b in range(batches_needed):
            curr_batch = min(batch_size, total_records - len(records))
            if curr_batch <= 0:
                break

            try:
                personas = await groq_client.generate_batch(batch_size=curr_batch)
                for persona in personas:
                    feature_row = engine.synthesize_psycho_features(persona)
                    records.append(feature_row)
                    progress.advance(task, 1)

                # Небольшая пауза 0.5с для соблюдения rate limits Groq Free Tier
                await asyncio.sleep(0.5)

            except Exception as e:
                console.print(f"[yellow]⏳ Предупреждение батча ({e}) — повтор через 3с...[/yellow]")
                await asyncio.sleep(3.0)

    elapsed = time.time() - start_time
    df = pd.DataFrame(records)

    # Сохраняем датасет в директорию ml-engine
    out_dir = Path(__file__).resolve().parent.parent / "ml-engine" / "training"
    out_path = out_dir / "psycho_life_dataset.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")

    console.print(f"\n[bold green]✅ Датасет Psycho-Life успешно сохранен:[/bold green] [white]{out_path}[/white]")
    console.print(f"⏱️ Затраченное время: [bold magenta]{elapsed:.1f} сек[/bold magenta] ({len(df)/elapsed:.1f} персон/сек)")

    # Сводная таблица
    table = Table(title="📊 Статистика Psycho-Life Датасета")
    table.add_column("Метрика", style="cyan")
    table.add_column("Значение", style="magenta")

    table.add_row("Всего заемщиков", str(len(df)))
    table.add_row("Доля депрессивных кризисов", f"{df['target_depression_crisis'].mean():.1%}")
    table.add_row("Доля дефолтов", f"{df['target_default_30d'].mean():.1%}")
    table.add_row("Средний возраст", f"{df['age'].mean():.1f} лет")
    table.add_row("Средний доход", f"{df['declared_income'].mean():,.0f} KZT")
    table.add_row("Средний индекс депрессии", f"{df['depression_risk_index'].mean():.2f}")

    console.print(table)


if __name__ == "__main__":
    # Генерируем 250 заемщиков с психологическими профилями через Groq LPU (Qwen 27B)
    asyncio.run(generate_psycho_dataset(total_records=250, batch_size=5))
