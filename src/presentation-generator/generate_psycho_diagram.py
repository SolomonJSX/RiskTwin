import resvg_py
from pathlib import Path

def generate_psycho_diagram():
    out_dir = Path(__file__).resolve().parent / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / "psycho_life_engine.png"

    # Exact aspect ratio: 960 x 712 (1.348:1) matches Inches(6.9) x Inches(5.12)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="960" height="712" viewBox="0 0 960 712">
  <defs>
    <linearGradient id="bgCanvas" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FAFC"/>
    </linearGradient>

    <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#5B21B6"/>
    </linearGradient>

    <linearGradient id="matrixGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4F46E5"/>
      <stop offset="100%" stop-color="#312E81"/>
    </linearGradient>

    <linearGradient id="redGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#DC2626"/>
      <stop offset="100%" stop-color="#991B1B"/>
    </linearGradient>

    <filter id="boxShadow" x="-10%" y="-10%" width="125%" height="130%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.08"/>
    </filter>
  </defs>

  <style>
    .font-title { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 700; }
    .font-sub { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 600; }
    .font-body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 400; }
    .font-math { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 600; font-size: 11px; }
    .font-code { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-size: 10px; font-weight: 500; fill: #334155; }
    .font-badge { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 700; font-size: 9.5px; }
  </style>

  <!-- Outer Canvas Container -->
  <rect x="2" y="2" width="956" height="708" rx="16" fill="url(#bgCanvas)" stroke="#E2E8F0" stroke-width="2"/>

  <!-- Diagram Header Tag & Title -->
  <rect x="22" y="16" width="280" height="26" rx="13" fill="#F5F3FF" stroke="#DDD6FE" stroke-width="1.5"/>
  <text x="35" y="33" class="font-badge" fill="#7C3AED">PSYCHO-LIFE SERVICE • ПАТТЕРНЫ ПОВЕДЕНИЯ</text>
  <text x="22" y="68" class="font-title" font-size="18.5" fill="#0F172A">Как сервис считывает эмоциональное состояние из данных</text>

  <!-- ======================================================================= -->
  <!-- LEVEL 1: 4 PASSIVE SENSORS (TOP)                                        -->
  <!-- ======================================================================= -->
  <g transform="translate(22, 90)" filter="url(#boxShadow)">
    <rect width="916" height="150" rx="12" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="2"/>
    <rect width="916" height="34" rx="12" fill="url(#purpleGrad)"/>
    <rect y="22" width="916" height="12" fill="url(#purpleGrad)"/>
    <text x="16" y="22" class="font-sub" font-size="12.5" fill="#FFFFFF">1. Пассивные цифровые сенсоры: извлечение маркеров кризиса без опросов</text>
    <rect x="800" y="6" width="100" height="22" rx="11" fill="#4C1D95"/>
    <text x="850" y="21" text-anchor="middle" class="font-badge" fill="#E9D5FF">9 Маркеров</text>

    <!-- 4 Sensor Columns -->
    <g transform="translate(14, 46)">
      <!-- S1: Insomnia -->
      <rect width="210" height="92" rx="8" fill="#FAF5FF" stroke="#E9D5FF"/>
      <text x="10" y="18" class="font-sub" font-size="11" fill="#6B21A8">🌙 Бессонница &amp; Тревога</text>
      <text x="10" y="34" class="font-code">• Входы в ДБО в 03:00–05:00</text>
      <text x="10" y="48" class="font-code">• Зависание на графике: 95 сек</text>
      <text x="10" y="62" class="font-code">• Проверка баланса: 10 раз/день</text>
      <text x="10" y="78" class="font-badge" fill="#7E22CE">DboNightAnxiety: HIGH</text>
    </g>

    <g transform="translate(240, 46)">
      <!-- S2: Depression/Drop -->
      <rect width="210" height="92" rx="8" fill="#F0FDF4" stroke="#BBF7D0"/>
      <text x="10" y="18" class="font-sub" font-size="11" fill="#15803D">🥀 Депрессивный спад</text>
      <text x="10" y="34" class="font-code">• Спад трат на себя (спорт/кафе)</text>
      <text x="10" y="48" class="font-code">• Забросил уход: drop rate 85%</text>
      <text x="10" y="62" class="font-code">• Аптеки: седативные средства</text>
      <text x="10" y="78" class="font-badge" fill="#166534">SelfCareDrop: 0.85</text>
    </g>

    <g transform="translate(466, 46)">
      <!-- S3: Panic Transfers -->
      <rect width="210" height="92" rx="8" fill="#FEF2F2" stroke="#FECACA"/>
      <text x="10" y="18" class="font-sub" font-size="11" fill="#B91C1C">⚡ Финансовая паника</text>
      <text x="10" y="34" class="font-code">• P2P займы у 5+ знакомых</text>
      <text x="10" y="48" class="font-code">• Первые микрозаймы в МФО</text>
      <text x="10" y="62" class="font-code">• Ночной алкоголь/эскапизм</text>
      <text x="10" y="78" class="font-badge" fill="#991B1B">MfoTransfer: DETECTED</text>
    </g>

    <g transform="translate(692, 46)">
      <!-- S4: Shocks -->
      <rect width="210" height="92" rx="8" fill="#EFF6FF" stroke="#BFDBFE"/>
      <text x="10" y="18" class="font-sub" font-size="11" fill="#1D4ED8">💔 Жизненные шоки</text>
      <text x="10" y="34" class="font-code">• Развод и алименты (33%)</text>
      <text x="10" y="48" class="font-code">• Внезапные траты на клиники</text>
      <text x="10" y="62" class="font-code">• Спад зарплатной динамики</text>
      <text x="10" y="78" class="font-badge" fill="#1E40AF">LifeShockIndex: 0.78</text>
    </g>
  </g>

  <!-- Connective Flow Arrow -->
  <path d="M 480 240 L 480 268" stroke="#7C3AED" stroke-width="3" fill="none"/>

  <!-- ======================================================================= -->
  <!-- LEVEL 2: CROSS-ATTENTION SYNERGY MATRIX [7 x 9] (CENTER)                -->
  <!-- ======================================================================= -->
  <g transform="translate(22, 268)" filter="url(#boxShadow)">
    <rect width="916" height="235" rx="14" fill="#FFFFFF" stroke="#4F46E5" stroke-width="2.5"/>
    <rect width="916" height="36" rx="14" fill="url(#matrixGrad)"/>
    <rect y="24" width="916" height="12" fill="url(#matrixGrad)"/>
    <text x="18" y="24" class="font-sub" font-size="13" fill="#FFFFFF">2. Как психология влияет на результат: Матрица синергии [7 финансов × 9 психо-маркеров]</text>
    <rect x="795" y="7" width="105" height="22" rx="11" fill="#1E1B4B"/>
    <text x="847" y="22" text-anchor="middle" class="font-badge" fill="#C7D2FE">Cross-Synergy</text>

    <!-- Left Description of Mechanism (No Text Overflow) -->
    <g transform="translate(18, 48)">
      <rect width="425" height="170" rx="10" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="1.5"/>
      <text x="14" y="20" class="font-sub" font-size="11.5" fill="#1E40AF">Механизм трансформации скоринга:</text>
      
      <!-- Comparison badges -->
      <g transform="translate(14, 28)">
        <rect width="190" height="20" rx="4" fill="#E0E7FF" stroke="#C7D2FE"/>
        <text x="8" y="14" class="font-code" fill="#3730A3">• Скоринг банка: Класс AAA</text>
        <rect x="198" width="198" height="20" rx="4" fill="#FEE2E2" stroke="#FCA5A5"/>
        <text x="206" y="14" class="font-code" fill="#991B1B">⚠ Риск дефолта: 84.2%</text>
      </g>

      <text x="14" y="66" class="font-sub" font-size="11" fill="#4338CA">Cross-Attention связывает скрытые связи:</text>
      
      <rect x="14" y="74" width="396" height="24" rx="5" fill="#F5F3FF" stroke="#DDD6FE"/>
      <text x="18" y="90" class="font-sub" font-size="10.5" fill="#6B21A8">[Падение остатка 7d] ⊗ [Ночная паника в ДБО]</text>
      
      <text x="14" y="116" class="font-body" font-size="10" fill="#475569">Модель понимает: клиент тратит остаток не на роскошь,</text>
      <text x="14" y="130" class="font-body" font-size="10" fill="#475569">а находится в шоковом кассовом разрыве до платежа.</text>
      
      <rect x="14" y="140" width="396" height="20" rx="4" fill="#DCFCE7" stroke="#86EFAC"/>
      <text x="18" y="154" class="font-badge" fill="#14532D">• Сдвиг фокуса с платежеспособности на жизнеспособность</text>
    </g>

    <!-- Right: TreeSHAP / Cross-Attention Weights Visualization -->
    <g transform="translate(460, 48)">
      <rect width="438" height="170" rx="10" fill="#FAF5FF" stroke="#E9D5FF" stroke-width="1.5"/>
      <text x="14" y="20" class="font-sub" font-size="11.5" fill="#6B21A8">Веса внимания синергии (TreeSHAP &amp; Attention):</text>
      
      <!-- Bar 1 -->
      <text x="14" y="44" class="font-sub" font-size="10.5" fill="#1E293B">1. Ночные входы → Падение остатка</text>
      <text x="350" y="44" class="font-badge" fill="#7E22CE">вес: 0.382</text>
      <rect x="14" y="50" width="320" height="10" rx="5" fill="#C084FC"/>

      <!-- Bar 2 -->
      <text x="14" y="78" class="font-sub" font-size="10.5" fill="#1E293B">2. МФО микрозаймы → Лимит кредиток</text>
      <text x="350" y="78" class="font-badge" fill="#B91C1C">вес: 0.294</text>
      <rect x="14" y="84" width="250" height="10" rx="5" fill="#F87171"/>

      <!-- Bar 3 -->
      <text x="14" y="112" class="font-sub" font-size="10.5" fill="#1E293B">3. Зависание на графике → Задержка ЗП</text>
      <text x="350" y="112" class="font-badge" fill="#1D4ED8">вес: 0.218</text>
      <rect x="14" y="118" width="180" height="10" rx="5" fill="#60A5FA"/>

      <rect x="14" y="140" width="410" height="20" rx="4" fill="#F3E8FF" stroke="#D8B4FE"/>
      <text x="18" y="154" class="font-badge" fill="#581C87">100% XAI-прозрачность: риск-офицер видит первопричину</text>
    </g>
  </g>

  <!-- Connective Flow Arrow -->
  <path d="M 480 503 L 480 530" stroke="#DC2626" stroke-width="3" fill="none"/>

  <!-- ======================================================================= -->
  <!-- LEVEL 3: IMPACT ON FINAL OUTCOME (BOTTOM)                               -->
  <!-- ======================================================================= -->
  <g transform="translate(22, 530)" filter="url(#boxShadow)">
    <rect width="916" height="160" rx="12" fill="#FFFFFF" stroke="#F87171" stroke-width="2"/>
    <rect width="916" height="34" rx="12" fill="url(#redGrad)"/>
    <rect y="22" width="916" height="12" fill="url(#redGrad)"/>
    <text x="16" y="22" class="font-sub" font-size="13" fill="#FFFFFF">3. Результат: Превращение скрытого стресса в упреждающее действие</text>
    <rect x="795" y="6" width="105" height="22" rx="11" fill="#7F1D1D"/>
    <text x="847" y="21" text-anchor="middle" class="font-badge" fill="#FEE2E2">Pre-Emptive</text>

    <!-- Comparison Outcome Cards -->
    <g transform="translate(18, 46)">
      <rect width="425" height="100" rx="8" fill="#FEF2F2" stroke="#FECACA"/>
      <text x="14" y="22" class="font-sub" font-size="11.5" fill="#991B1B">Традиционный скоринг (без Psycho-Life):</text>
      <text x="14" y="42" class="font-code">• Оценка надежности: Класс AAA (PD = 1.3%)</text>
      <text x="14" y="58" class="font-code">• Действие банка: Бездействие (ждет Day 1+ DPD)</text>
      <text x="14" y="74" class="font-code">• Итог: Внезапный дефолт через 14 дней → NPL</text>
      <text x="14" y="90" class="font-badge" fill="#DC2626">Опоздание на 30 дней • 100% потери</text>
    </g>

    <g transform="translate(462, 46)">
      <rect width="436" height="100" rx="8" fill="#F0FDF4" stroke="#BBF7D0"/>
      <text x="14" y="22" class="font-sub" font-size="11.5" fill="#15803D">Интеллект RiskTwin (с Psycho-Life):</text>
      <text x="14" y="42" class="font-code">• Риск стресса: Взлет PD до 84.2% за 30 дней</text>
      <text x="14" y="58" class="font-code">• Дней до разрыва: Ровно 14 дней (Survival MAE ±4.2)</text>
      <text x="14" y="74" class="font-code">• Действие банка: Автоматический оффер солвера в ДБО</text>
      <text x="14" y="90" class="font-badge" fill="#166534">Клиент спасен до первой просрочки</text>
    </g>
  </g>
</svg>"""

    with open(out_png, "wb") as f:
        f.write(resvg_py.svg_to_bytes(svg))
    print(f"[OK] Psycho-Life diagram regenerated: {out_png}")

if __name__ == "__main__":
    generate_psycho_diagram()
