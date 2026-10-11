import uuid
import random
from datetime import date
from pathlib import Path
import numpy as np
import pandas as pd
from rich.console import Console
from rich.table import Table

from app.domain.iin_validator import generate_valid_kazakhstan_iin
from app.behavioral.psycho_distribution_engine import PsychoBehavioralDistributionEngine

console = Console()

# Аутентичные казахстанские имена и фамилии
MALE_NAMES = [
    ("Сатпаев", "Арман", "Кайратович"),
    ("Кузнецов", "Андрей", "Игоревич"),
    ("Мухаметкалиев", "Ербол", "Каирбекулы"),
    ("Жакишев", "Нурлан", "Адильбекович"),
    ("Алиев", "Диас", "Русланович"),
    ("Абдиров", "Арман", "Абилькасымович"),
    ("Оспанов", "Бауыржан", "Серикович"),
    ("Иванов", "Максим", "Сергеевич"),
    ("Смаилов", "Тимур", "Аскарович"),
    ("Касымов", "Данияр", "Муратович"),
    ("Токтаров", "Алихан", "Берикович"),
    ("Ермеков", "Азамат", "Куанышевич"),
    ("Байзаков", "Айдос", "Асланович"),
    ("Нургалиев", "Канат", "Ерланович"),
]

FEMALE_NAMES = [
    ("Серикова", "Аружан", "Данияровна"),
    ("Байтурсынова", "Асем", "Аскарбековна"),
    ("Касымова", "Амина", "Аскарбековна"),
    ("Муканова", "Гульмира", "Ержановна"),
    ("Кожахметова", "Аида", "Кенесбековна"),
    ("Абдуллина", "Диана", "Равильевна"),
    ("Исаева", "Малика", "Адильбековна"),
    ("Смирнова", "Елена", "Викторовна"),
    ("Ахметова", "Динара", "Болатовна"),
    ("Жолдасова", "Мадина", "Нурлановна"),
    ("Омарова", "Зарина", "Кайратовна"),
]

CITIES = [
    "Алматы", "Астана", "Шымкент", "Караганда", "Актобе",
    "Тараз", "Павлодар", "Усть-Каменогорск", "Семей", "Костанай"
]

INDUSTRIES = [
    "Строительство", "Ритейл", "IT", "Государственный сектор",
    "Логистика", "Сфера услуг", "Здравоохранение", "Образование", "Нефтегазовый сектор"
]

# Реалистичные психологические истории жизненных кризисов
CRISIS_TEMPLATES = {
    "DIVORCE_DEPRESSION": [
        "Пережил тяжелый развод после 12 лет брака с разделом квартиры и машины. Супруга отсудила {alimony}% алиментов на двоих детей. Живет на съемном жилье, страдает апатией и бессонницей, урезали квартальный бонус.",
        "Судебный процесс по расторжению брака длился полгода. Обязан выплачивать {alimony}% алиментов. Из-за постоянного стресса нарушился сон, снизилась продуктивность на работе, перестал общаться с друзьями.",
        "После развода остался без собственного жилья. Вынужден снимать квартиру и отдавать треть дохода на алименты. Развился депрессивный эпизод, начались пропуски рабочих дней.",
        "Развод и судебный раздел бизнеса привели к тяжелому психоэмоциональному кризису. Назначены алименты {alimony}%. Чувство опустошенности и эмоционального выгорания.",
    ],
    "BEREAVEMENT_GRIEF": [
        "Внезапная смерть супруга — основного кормильца семьи. Огромные непредвиденные расходы на похороны и поминки. Острая стадия скорби, эмоциональное оцепенение, трудно выходить на работу.",
        "Тяжелая утрата близкого родственника. Пробита серьезная брешь в семейном бюджете из-за ритуальных расходов и возврата долгов родственникам. Синдром острой скорби.",
        "Потерял отца после продолжительной болезни. На фоне похоронных расходов влез в мелкие долги у знакомых. Острая апатия, бессонница, принимает антидепрессанты.",
    ],
    "EMOTIONAL_BURNOUT": [
        "Хроническое выгорание после 3 лет работы без отпуска в режиме 12 часов в сутки. Диагностирован синдром астении, сняли с руководящей должности из-за срыва дедлайнов.",
        "Глубокий депрессивный эпизод на фоне токсичной обстановки на работе. Полная потеря сил и мотивации, срезали премию, начались панические атаки по ночам.",
        "Профессиональное выгорание в сфере продаж. Доход упал в два раза из-за невыполнения KPI. Проводит ночи в бессоннице, перестал следить за собой.",
    ],
    "FAMILY_HEALTH_EMERGENCY": [
        "Тяжелое заболевание матери, потребовавшее срочной платной операции и дорогостоящего курса реабилитации. Почти вся зарплата уходит на аптеки и клиники.",
        "Ребенок попал в больницу с тяжелым диагнозом. Экстренные траты на лекарства истощили все накопления. Психологический шок у родителей, страх не потянуть кредит.",
        "Супруга проходит сложное лечение. Семья вынуждена брать в долг у знакомых на покупку рецептурных препаратов. Хронический стресс и дефицит средств.",
    ],
    "ADDICTION_ESCAPISM": [
        "На фоне семейного кризиса начал делать ставки в онлайн-букмекерах в попытке быстро закрыть долги. Развилась лудомания, потерял контроль над бюджетом.",
        "Попытка заглушить тяжелый развод и одиночество через ночные алкомаркеты и азартные игры. Хаотичные ночные транзакции, накопление долгов по коммуналке.",
    ],
    "STABLE_HARMONY": [
        "Полное семейное благополучие, стабильная работа с регулярными премиями, финансовая подушка на 6 месяцев, регулярный спорт и режим сна.",
        "Счастливая семейная жизнь, крепкое здоровье, отсутствие стрессовых факторов. Платежная дисциплина соблюдается безупречно.",
        "Уверенность в завтрашнем дне, стабильный доход в развивающейся компании, спокойный сон и отсутствие кредитных проблем.",
    ]
}


def generate_instant_psycho_dataset(total_records: int = 1000) -> pd.DataFrame:
    console.print("[bold cyan]════════════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold yellow]⚡ Мгновенная генерация Psycho-Life Датасета (1000 заемщиков РК)[/bold yellow]")
    console.print("[bold cyan]════════════════════════════════════════════════════════════════[/bold cyan]\n")

    random.seed(42)
    np.random.seed(42)

    engine = PsychoBehavioralDistributionEngine()
    records = []

    # Распределение кризисов: 40% норма, 60% жизненные драмы
    crisis_weights = {
        "STABLE_HARMONY": 0.40,
        "DIVORCE_DEPRESSION": 0.22,      # Развод и депрессия
        "EMOTIONAL_BURNOUT": 0.14,       # Выгорание
        "BEREAVEMENT_GRIEF": 0.10,       # Смерть близкого
        "FAMILY_HEALTH_EMERGENCY": 0.08, # Болезнь
        "ADDICTION_ESCAPISM": 0.06       # Лудомания / уход от реальности
    }

    cr_types = list(crisis_weights.keys())
    cr_probs = list(crisis_weights.values())

    for i in range(total_records):
        is_male = random.random() < 0.55
        if is_male:
            fam, name, otch = random.choice(MALE_NAMES)
            gender_str = "MALE"
        else:
            fam, name, otch = random.choice(FEMALE_NAMES)
            gender_str = "FEMALE"

        full_name = f"{fam} {name} {otch}"
        city = random.choice(CITIES)
        industry = random.choice(INDUSTRIES)
        emp_type = random.choice(["OFFICIAL_EMPLOYED", "INDIVIDUAL_ENTREPRENEUR", "SELF_EMPLOYED"])

        b_year = random.randint(1968, 2004)
        b_month = random.randint(1, 12)
        b_day = random.randint(1, 28)
        b_date = date(b_year, b_month, b_day)
        age = 2026 - b_year
        iin = generate_valid_kazakhstan_iin(b_date, gender_str)

        crisis_type = np.random.choice(cr_types, p=cr_probs)

        # Доход
        if crisis_type == "STABLE_HARMONY":
            income = float(random.choice([350000, 500000, 750000, 1100000, 1600000]))
            alimony_pct = 0.0
        elif crisis_type == "DIVORCE_DEPRESSION":
            income = float(random.choice([280000, 420000, 600000, 850000, 1200000]))
            alimony_pct = float(random.choice([25, 33, 50]))
        else:
            income = float(random.choice([200000, 320000, 450000, 700000, 950000]))
            alimony_pct = 0.0

        # Нарратив
        template = random.choice(CRISIS_TEMPLATES[crisis_type])
        narrative = template.replace("{alimony}", str(int(alimony_pct)))

        persona_dict = {
            "full_name": full_name,
            "iin": iin,
            "age": age,
            "gender": gender_str,
            "city": city,
            "employment_type": emp_type,
            "industry": industry,
            "declared_income": income,
            "life_crisis_type": crisis_type,
            "alimony_share": round(alimony_pct / 100.0, 2),
            "life_narrative": narrative,
        }

        # Синтез 45 биомаркеров трат, сна и психоэмоционального истощения
        feature_row = engine.synthesize_psycho_features(persona_dict)
        records.append(feature_row)

    df = pd.DataFrame(records)

    # Сохраняем в папку ml-engine
    out_dir = Path(__file__).resolve().parent.parent / "ml-engine" / "training"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "psycho_life_dataset.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")

    console.print(f"[bold green]🎉 Датасет Psycho-Life успешно сгенерирован и сохранен:[/bold green] [white]{out_path}[/white]\n")

    # Сводная таблица
    table = Table(title="📊 Статистика Psycho-Life Датасета (1 000 заемщиков РК)")
    table.add_column("Метрика / Фактор", style="cyan")
    table.add_column("Значение в датасете", style="magenta")

    table.add_row("Всего заемщиков", f"{len(df):,}")
    table.add_row("В гармонии (STABLE)", f"{(df['life_crisis_type'] == 'STABLE_HARMONY').sum()} ({(df['life_crisis_type'] == 'STABLE_HARMONY').mean():.1%})")
    table.add_row("Развод и депрессия (DIVORCE)", f"{(df['life_crisis_type'] == 'DIVORCE_DEPRESSION').sum()} ({(df['life_crisis_type'] == 'DIVORCE_DEPRESSION').mean():.1%})")
    table.add_row("Выгорание и астения (BURNOUT)", f"{(df['life_crisis_type'] == 'EMOTIONAL_BURNOUT').sum()} ({(df['life_crisis_type'] == 'EMOTIONAL_BURNOUT').mean():.1%})")
    table.add_row("Утрата близкого (BEREAVEMENT)", f"{(df['life_crisis_type'] == 'BEREAVEMENT_GRIEF').sum()} ({(df['life_crisis_type'] == 'BEREAVEMENT_GRIEF').mean():.1%})")
    table.add_row("Болезнь в семье (HEALTH)", f"{(df['life_crisis_type'] == 'FAMILY_HEALTH_EMERGENCY').sum()} ({(df['life_crisis_type'] == 'FAMILY_HEALTH_EMERGENCY').mean():.1%})")
    table.add_row("Азартные игры / Побег (ADDICTION)", f"{(df['life_crisis_type'] == 'ADDICTION_ESCAPISM').sum()} ({(df['life_crisis_type'] == 'ADDICTION_ESCAPISM').mean():.1%})")
    table.add_row("Доля депрессивных кризисов", f"{df['target_depression_crisis'].mean():.1%}")
    table.add_row("Доля дефолтов (Default Rate)", f"{df['target_default_30d'].mean():.1%}")
    table.add_row("Средний индекс депрессии (0-1)", f"{df['depression_risk_index'].mean():.2f}")
    table.add_row("Средний возраст заемщика", f"{df['age'].mean():.1f} лет")
    table.add_row("Средний доход", f"{df['declared_income'].mean():,.0f} KZT")

    console.print(table)
    return df


if __name__ == "__main__":
    generate_instant_psycho_dataset(total_records=1000)
