import asyncio
from app.llm.ollama_client import OllamaPersonaGenerator


async def main():
    print("⏳ Отправляем Zero-shot запрос в Ollama (mistral-nemo:12b)...")
    generator = OllamaPersonaGenerator()
    personas = await generator.generate_batch(batch_size=3)

    print(f"\n🎉 Успешно сгенерировано персон: {len(personas)}\n")
    for p in personas:
        print(f"👤 ФИО: {p.full_name} | Возраст: {p.age} | Пол: {p.gender.value}")
        print(f"   ИИН: {p.iin} (валиден)")
        print(f"   Город: {p.city} | Работа: {p.employment_type.value} ({p.industry})")
        print(f"   Доход: {p.declared_income:,.0f} KZT | Архетип: {p.archetype.value}")
        print(f"   Ситуация: {p.stress_narrative}")
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())