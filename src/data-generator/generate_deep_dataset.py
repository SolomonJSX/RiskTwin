import uuid
import random
from datetime import date
from pathlib import Path
import numpy as np
import pandas as pd
from rich.console import Console
from rich.table import Table

from app.domain.iin_validator import generate_valid_kazakhstan_iin

console = Console()

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


def generate_deep_synergistic_dataset(n_samples: int = 25000) -> pd.DataFrame:
    """
    Генерация масштабного стохастического датасета (25 000+ заемщиков)
    с непрерывными ковариациями, когортами финансово-психологического стресса,
    скрытым латентным фактором стойкости (Resilience) и реалистичным шумом (Target AUC ~ 0.88 - 0.92).
    """
    console.print("[bold cyan]════════════════════════════════════════════════════════════════[/bold cyan]")
    console.print(f"[bold yellow]🧠 Генерация глубокого синергетического датасета ({n_samples:,} заемщиков)[/bold yellow]")
    console.print("[bold cyan]════════════════════════════════════════════════════════════════[/bold cyan]\n")

    np.random.seed(42)
    random.seed(42)

    records = []

    for i in range(n_samples):
        # 1. Демография
        is_male = random.random() < 0.55
        fam, name, otch = random.choice(MALE_NAMES) if is_male else random.choice(FEMALE_NAMES)
        gender_str = "MALE" if is_male else "FEMALE"
        full_name = f"{fam} {name} {otch}"
        city = random.choice(CITIES)
        industry = random.choice(INDUSTRIES)
        emp_type = random.choice(["OFFICIAL_EMPLOYED", "INDIVIDUAL_ENTREPRENEUR", "SELF_EMPLOYED"])

        b_year = random.randint(1965, 2005)
        b_month = random.randint(1, 12)
        b_day = random.randint(1, 28)
        b_date = date(b_year, b_month, b_day)
        age = 2026 - b_year
        iin = generate_valid_kazakhstan_iin(b_date, gender_str)

        # Логнормальный доход с поправкой на отрасль и город
        city_boost = 1.25 if city in ["Алматы", "Астана"] else 1.0
        base_income = float(np.random.lognormal(mean=13.0, sigma=0.48)) * city_boost
        income = float(np.clip(base_income, 120000.0, 3500000.0))

        # 2. Скрытый латентный фактор психологической стойкости (Resilience)
        # Люди с высокой стойкостью легче переносят стрессы и разводы
        resilience_score = float(np.random.normal(0.0, 1.0))

        # 3. Вероятность жизненного кризиса
        crisis_prob = 0.40
        has_life_crisis = np.random.rand() < crisis_prob

        if not has_life_crisis:
            crisis_type = "STABLE_HARMONY"
            life_stress_intensity = float(np.clip(np.random.beta(1.5, 6.0), 0.05, 0.40))
            alimony_ratio = 0.0
        else:
            crisis_type = np.random.choice([
                "DIVORCE_DEPRESSION", "EMOTIONAL_BURNOUT",
                "BEREAVEMENT_GRIEF", "FAMILY_HEALTH_EMERGENCY", "ADDICTION_ESCAPISM"
            ], p=[0.38, 0.25, 0.15, 0.12, 0.10])

            # Интенсивность переживаемого стресса (с вариацией!)
            life_stress_intensity = float(np.clip(np.random.beta(5.0, 2.5), 0.35, 0.98))
            alimony_ratio = float(np.random.choice([0.25, 0.33, 0.50])) if crisis_type == "DIVORCE_DEPRESSION" else 0.0

        # 4. Финансовые признаки (с непрерывным шумом и нелинейной связкой)
        salary_trend = float(np.random.normal(1.0 - 0.35 * life_stress_intensity + 0.10 * resilience_score, 0.12))
        salary_trend = float(np.clip(salary_trend, 0.35, 1.35))

        delay_days = int(np.random.poisson(max(0.1, 14.0 * life_stress_intensity - 4.0 * resilience_score)))
        mfo_presence = bool(np.random.rand() < (0.05 + 0.40 * life_stress_intensity - 0.15 * resilience_score))
        dti_estimate = float(np.random.normal(0.32 + 0.38 * life_stress_intensity + alimony_ratio * 0.7, 0.10))
        dti_estimate = float(np.clip(dti_estimate, 0.15, 1.15))

        median_balance_7d = float(income * np.clip(np.random.normal(0.8 - 0.7 * life_stress_intensity, 0.25), 0.02, 2.0))
        net_cashflow_margin = float(np.random.normal(0.25 - 0.55 * life_stress_intensity, 0.15))

        # 5. Психоэмоциональные биомаркеры трат и сна
        pharmacy_antidepressant_share = float(np.clip(np.random.beta(1.5 + 4.0 * life_stress_intensity, 15.0), 0.0, 0.45))
        nighttime_alcohol_spend = float(np.clip(np.random.beta(1.0 + 3.0 * life_stress_intensity, 12.0), 0.0, 0.40))
        self_care_drop_rate = float(np.clip(np.random.normal(0.10 + 0.75 * life_stress_intensity - 0.20 * resilience_score, 0.15), 0.0, 1.0))

        night_dbo_logins = int(np.random.poisson(max(0.2, 10.0 * life_stress_intensity - 2.0 * resilience_score)))
        dwell_time_screen = float(np.clip(np.random.normal(15.0 + 110.0 * life_stress_intensity, 25.0), 5.0, 240.0))
        sleep_disruption_night_orders = int(np.random.poisson(max(0.3, 8.0 * life_stress_intensity)))
        balance_check_anxiety = float(np.clip(np.random.normal(1.5 + 10.0 * life_stress_intensity, 2.5), 1.0, 25.0))

        # 6. НЕПРЕРЫВНАЯ ФОРМУЛА СИНЕРГИИ РИСКА (Latent Hazard Model)
        # Синергия: финансовый стресс * психоэмоциональный стресс
        fin_stress_score = (dti_estimate * 1.5) + (1.0 - min(1.0, salary_trend)) + (0.5 if mfo_presence else 0.0)
        psycho_stress_score = (life_stress_intensity * 1.4) + (self_care_drop_rate * 0.8) + (min(1.0, night_dbo_logins / 10.0) * 0.6)

        synergy_interaction = fin_stress_score * psycho_stress_score

        # Логит дефолта с шумом (чтобы убрать искусственную 100% разделимость)
        noise = float(np.random.logistic(0.0, 0.45))
        logit_default = -3.2 + 0.9 * fin_stress_score + 0.8 * psycho_stress_score + 0.45 * synergy_interaction - 0.7 * resilience_score + noise
        prob_default = 1.0 / (1.0 + np.exp(-logit_default))

        # Вероятностный таргет дефолта (с перекрытием классов!)
        target_default_30d = 1 if (prob_default >= 0.50 or np.random.rand() < prob_default * 0.35) else 0

        # Моделирование времени до срыва (Weibull Survival: Days to Default)
        if target_default_30d == 1:
            predicted_days_to_default = int(np.clip(np.random.weibull(1.8) * 22.0 / (prob_default + 0.1), 3, 45))
        else:
            predicted_days_to_default = int(np.random.randint(65, 210))

        target_depression_crisis = 1 if (life_stress_intensity >= 0.55 and np.random.rand() > 0.15) else 0

        records.append({
            "client_token": str(uuid.uuid4()),
            "full_name": full_name,
            "iin": iin,
            "age": age,
            "gender": gender_str,
            "city": city,
            "employment_type": emp_type,
            "industry": industry,
            "declared_income": round(income, 0),
            "life_crisis_type": crisis_type,
            "resilience_score": round(resilience_score, 3),
            # Финансовые маркеры
            "salary_trend_ratio_3m_vs_6m": round(salary_trend, 3),
            "salary_inflow_delay_days": delay_days,
            "mfo_gambling_tag_presence": 1 if mfo_presence else 0,
            "dti_dynamic_estimate": round(dti_estimate, 3),
            "median_daily_balance_7d": round(median_balance_7d, 0),
            "net_cashflow_margin_30d": round(net_cashflow_margin, 3),
            # Психологические маркеры
            "life_stress_intensity": round(life_stress_intensity, 3),
            "alimony_burden_ratio": round(alimony_ratio, 2),
            "pharmacy_antidepressant_share": round(pharmacy_antidepressant_share, 3),
            "nighttime_alcohol_spend_share": round(nighttime_alcohol_spend, 3),
            "self_care_drop_rate": round(self_care_drop_rate, 3),
            "night_dbo_login_frequency": night_dbo_logins,
            "dwell_time_repayment_screen": round(dwell_time_screen, 1),
            "sleep_disruption_night_orders": sleep_disruption_night_orders,
            "balance_check_anxiety_index": round(balance_check_anxiety, 2),
            # Синергия и выживаемость
            "synergy_interaction_score": round(synergy_interaction, 3),
            "predicted_days_to_default": predicted_days_to_default,
            "target_depression_crisis": target_depression_crisis,
            "target_default_30d": target_default_30d,
        })

    df = pd.DataFrame(records)

    out_dir = Path(__file__).resolve().parent.parent / "ml-engine" / "training"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "deep_synergistic_dataset.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")

    console.print(f"[bold green]✅ Синергетический датасет сохранен:[/bold green] [white]{out_path}[/white]\n")

    table = Table(title=f"📊 Статистика глубокого датасета ({len(df):,} заемщиков РК)")
    table.add_column("Метрика / Параметр", style="cyan")
    table.add_column("Значение", style="magenta")

    table.add_row("Всего заемщиков", f"{len(df):,}")
    table.add_row("Доля дефолтов (Default Rate)", f"{df['target_default_30d'].mean():.1%}")
    table.add_row("Доля психо-кризисов", f"{df['target_depression_crisis'].mean():.1%}")
    table.add_row("Средний DTI (КДН)", f"{df['dti_dynamic_estimate'].mean():.2f}")
    table.add_row("Средний возраст", f"{df['age'].mean():.1f} лет")
    table.add_row("Средний доход", f"{df['declared_income'].mean():,.0f} KZT")
    table.add_row("Среднее окно до дефолта (дней)", f"{df[df['target_default_30d'] == 1]['predicted_days_to_default'].mean():.1f} дн.")

    console.print(table)
    return df


if __name__ == "__main__":
    generate_deep_synergistic_dataset(n_samples=25000)
