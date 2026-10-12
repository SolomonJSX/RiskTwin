import os
import sys
import time
import json
import logging
from rich.console import Console
import redis

from config import REDIS_HOST, REDIS_PORT
from aggregators.sliding_window import SlidingWindowAggregator
from producers.streamer import generate_mock_transaction, generate_mock_telemetry

console = Console()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("RiskTwin.Ingestion")


def run_standalone_simulation(iterations: int = 20, client_token: str = "KZ886010002003004001"):
    """
    Автономный режим эмуляции потока событий и агрегации в Redis Feature Store.
    Работает напрямую с Redis, имитируя как брокер, так и consumer.
    """
    console.print("[bold cyan]════════════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold yellow]🌊 RiskTwin Stream Ingestion & Feature Store Engine[/bold yellow]")
    console.print("[bold cyan]════════════════════════════════════════════════════════════════[/bold cyan]\n")

    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, socket_connect_timeout=3)
        r.ping()
        console.print(f"[bold green]✅ Подключение к Redis Feature Store ({REDIS_HOST}:{REDIS_PORT}) установлено![/bold green]\n")
    except Exception as e:
        console.print(f"[bold red]❌ Не удалось подключиться к Redis:[/bold red] {e}")
        console.print("[yellow]💡 Запустите 'docker-compose up -d redis' в папке docker/[/yellow]\n")
        return

    aggregator = SlidingWindowAggregator(r)

    console.print(f"🚀 Запуск генерации потоковых событий для заемщика: [white]{client_token}[/white]\n")

    # Сначала эмулируем нормальное поведение, затем включаем кризисный стресс-паттерн
    for i in range(1, iterations + 1):
        is_crisis = i > 5  # После 5-го шага клиент погружается в финансово-эмоциональный кризис

        # 1. Генерируем транзакцию
        tx_event = generate_mock_transaction(client_token, crisis_mode=is_crisis)
        aggregator.process_transaction_event(tx_event)

        # 2. Генерируем событие телеметрии приложения ДБО
        telemetry_event = generate_mock_telemetry(client_token, crisis_mode=is_crisis)
        aggregator.process_telemetry_event(telemetry_event)

        status_badge = "[bold red]🔥 КРИЗИС[/bold red]" if is_crisis else "[bold green]🌱 СТАБИЛЬНО[/bold green]"
        console.print(
            f"  [{i:02d}/{iterations:02d}] {status_badge} | Транзакция: {tx_event['type']} {tx_event['amount']:,.0f} KZT "
            f"| МФО: {tx_event['is_mfo_or_gambling']} | Зависание ДБО: {telemetry_event['loan_schedule_screen_dwell_time']}c"
        )
        time.sleep(0.15)

    # Выгрузка обновленного вектора признаков из Redis
    feat_key = f"client:{client_token}:features"
    stored_features = r.hgetall(feat_key)
    decoded_features = {k.decode("utf-8"): v.decode("utf-8") for k, v in stored_features.items()}

    console.print("\n[bold cyan]════════════════════════════════════════════════════════════════[/bold cyan]")
    console.print(f"[bold green]🎉 Онлайн Feature Store в Redis обновлен для {client_token}:[/bold green]")
    for k, v in decoded_features.items():
        console.print(f"   • [cyan]{k}[/cyan]: [magenta]{v}[/magenta]")
    console.print("[bold cyan]════════════════════════════════════════════════════════════════[/bold cyan]\n")


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    token = sys.argv[2] if len(sys.argv) > 2 else "KZ886010002003004001"
    run_standalone_simulation(iterations=count, client_token=token)
