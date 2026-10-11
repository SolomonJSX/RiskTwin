import os
import json
import logging
import asyncio
from datetime import date
from typing import List, Dict, Any
import httpx

from app.domain.models import Gender, EmploymentType
from app.domain.iin_validator import generate_valid_kazakhstan_iin
from app.llm.ollama_client import detect_and_correct_gender
from app.llm.psycho_prompts import PSYCHO_SYSTEM_PROMPT, PSYCHO_USER_PROMPT

logger = logging.getLogger("RiskTwin.DataGenerator.Groq")


class GroqPsychoPersonaClient:
    """
    Высокоскоростной клиент генерации персон через Groq Cloud LPU.
    Скорость: ~500-800 токенов/сек.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.groq.com/openai/v1",
        model: str | None = None,
    ):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.base_url = base_url.rstrip("/")
        self.model = model or os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

    async def generate_batch(self, batch_size: int = 10) -> List[Dict[str, Any]]:
        """Генерирует батч персон с глубоким психологическим портретом."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": PSYCHO_SYSTEM_PROMPT},
                {"role": "user", "content": PSYCHO_USER_PROMPT.format(batch_size=batch_size)},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.75,
            "max_tokens": 4096,
        }

        async with httpx.AsyncClient(timeout=45.0) as client:
            for attempt in range(5):
                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )

                if resp.status_code == 429:
                    # Groq 429: извлекаем рекомендуемое время паузы или ждем 4 секунды
                    wait_time = 4.0 + attempt * 2.0
                    try:
                        err_json = resp.json().get("error", {})
                        msg = err_json.get("message", "")
                        if "Please try again in" in msg:
                            seconds_str = msg.split("Please try again in")[1].split("s")[0].strip()
                            wait_time = float(seconds_str) + 0.5
                    except Exception:
                        pass
                    logger.info(f"⏳ Groq Rate Limit (429). Ожидание {wait_time:.1f}с...")
                    await asyncio.sleep(wait_time)
                    continue

                if resp.status_code != 200:
                    logger.error(f"Groq API Error {resp.status_code}: {resp.text}")
                    resp.raise_for_status()

                break

            data = resp.json()
            if "choices" not in data or not data["choices"]:
                err_msg = data.get("error", {}).get("message", "Unknown Groq error")
                raise ValueError(f"Groq API returned no choices: {err_msg}")

            raw_content = data["choices"][0]["message"]["content"]
            parsed = json.loads(raw_content)

            borrowers_raw = parsed.get("borrowers", [])
            valid_personas = []

            for raw in borrowers_raw:
                try:
                    full_name = raw.get("full_name", "Сатпаев Арман Кайратович")
                    gender = detect_and_correct_gender(full_name, raw.get("gender", "MALE"))

                    b_year = int(raw.get("birth_year", 1988))
                    b_month = max(1, min(12, int(raw.get("birth_month", 5))))
                    b_day = max(1, min(28, int(raw.get("birth_day", 15))))
                    b_date = date(b_year, b_month, b_day)

                    iin = generate_valid_kazakhstan_iin(b_date, gender.value)
                    age = max(18, min(75, 2026 - b_year))

                    raw_income = raw.get("declared_income")
                    declared_income = float(raw_income) if raw_income is not None else 450000.0

                    raw_alimony = raw.get("alimony_share")
                    alimony_share = float(raw_alimony) if raw_alimony is not None else 0.0

                    persona = {
                        "full_name": full_name,
                        "iin": iin,
                        "age": age,
                        "gender": gender.value,
                        "city": raw.get("city") or "Алматы",
                        "employment_type": raw.get("employment_type") or "OFFICIAL_EMPLOYED",
                        "industry": raw.get("industry") or "Сфера услуг",
                        "declared_income": declared_income,
                        "life_crisis_type": raw.get("life_crisis_type") or "STABLE_HARMONY",
                        "alimony_share": alimony_share,
                        "life_narrative": raw.get("life_narrative") or "Стабильная жизненная ситуация.",
                    }
                    valid_personas.append(persona)
                except Exception as e:
                    logger.warning(f"Ошибка парсинга персоны: {e}")

            return valid_personas
