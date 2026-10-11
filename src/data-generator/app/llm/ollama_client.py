import json
import logging
from datetime import date
from typing import List, Dict, Any
import httpx

from app.domain.models import PersonaProfile, Gender, EmploymentType, RiskArchetype
from app.domain.iin_validator import generate_valid_kazakhstan_iin
from app.llm.prompts import ZERO_SHOT_PERSONA_SYSTEM_PROMPT, ZERO_SHOT_USER_PROMPT

logger = logging.getLogger("RiskTwin.DataGenerator.Ollama")


def detect_and_correct_gender(full_name: str, suggested_gender: str) -> Gender:
    """
    Автокоррекция пола заемщика по морфологическим маркерам казахских
    и славянских фамилий, имен и отчеств.
    """
    name_lower = full_name.lower().strip()
    words = name_lower.split()

    # Явные маркеры женского пола
    female_suffixes = (
        "вна", "чна", "қызы", "кызы", "eva", "ova", "ева", "ова", "ина", "ая"
    )
    # Популярные женские казахские/русские имена
    female_first_names = {
        "әсел", "асель", "аружан", "айгерім", "айгерим", "дильназ", "динара",
        "мадина", "айсулу", "айсұлу", "анель", "әсем", "асем", "дания",
        "елена", "анна", "ольга", "татьяна", "наталья", "ирина", "алина"
    }

    # Явные маркеры мужского пола
    male_suffixes = ("вич", "ұлы", "улы", "евич", "ович")

    # 1. Проверяем отчество (обычно последнее слово)
    for word in words:
        if word.endswith(female_suffixes):
            return Gender.FEMALE
        if word.endswith(male_suffixes):
            return Gender.MALE

    # 2. Проверяем имя
    for word in words:
        if word in female_first_names:
            return Gender.FEMALE

    # 3. Fallback на предложение модели
    return Gender.FEMALE if "F" in suggested_gender.upper() else Gender.MALE


class OllamaPersonaGenerator:
    """Генератор синтетических персон через локальную Ollama (Zero-shot)."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "mistral-nemo:12b",
        timeout_seconds: float = 90.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout_seconds

    async def generate_batch(self, batch_size: int = 5) -> List[PersonaProfile]:
        """Генерирует пачку персон за один вызов LLM с форматированием в JSON."""
        user_message = ZERO_SHOT_USER_PROMPT.format(batch_size=batch_size)

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": ZERO_SHOT_PERSONA_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(f"{self.base_url}/api/chat", json=payload)
                response.raise_for_status()

                data = response.json()
                content = data["message"]["content"]
                parsed_json = json.loads(content)

                raw_borrowers = parsed_json.get("borrowers", [])
                personas: List[PersonaProfile] = []

                for item in raw_borrowers:
                    try:
                        full_name = item.get("full_name", "Сатпаев Арман").strip()

                        # Автокоррекция пола
                        suggested_gender = item.get("gender", "MALE")
                        gender = detect_and_correct_gender(full_name, suggested_gender)

                        # Валидация даты рождения
                        b_year = int(item.get("birth_year", 1990))
                        b_month = max(1, min(12, int(item.get("birth_month", 1))))
                        b_day = max(1, min(28, int(item.get("birth_day", 1))))
                        birth_date = date(b_year, b_month, b_day)
                        age = date.today().year - b_year

                        # Генерируем 100% валидный казахстанский ИИН с правильным 7-м разрядом (пол/век)
                        iin = generate_valid_kazakhstan_iin(birth_date, gender.value)

                        arch_raw = item.get("archetype", "STABLE").upper()
                        archetype = RiskArchetype.__members__.get(arch_raw, RiskArchetype.STABLE)

                        emp_raw = item.get("employment_type", "OFFICIAL_EMPLOYED").upper()
                        emp_type = EmploymentType.__members__.get(emp_raw, EmploymentType.OFFICIAL_EMPLOYED)

                        persona = PersonaProfile(
                            full_name=full_name,
                            iin=iin,
                            age=age,
                            gender=gender,
                            city=item.get("city", "Алматы"),
                            employment_type=emp_type,
                            industry=item.get("industry", "Строительство"),
                            declared_income=float(item.get("declared_income", 350000)),
                            archetype=archetype,
                            stress_narrative=item.get("stress_narrative", "Штатная финансовая ситуация."),
                        )
                        personas.append(persona)
                    except Exception as parse_err:
                        logger.warning(f"Ошибка парсинга элемента: {parse_err}")
                        continue

                return personas

        except Exception as e:
            logger.error(f"Ошибка запроса к Ollama: {e}")
            raise