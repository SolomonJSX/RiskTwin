import resvg_py
from pathlib import Path

def generate_solver_diagram():
    out_dir = Path(__file__).resolve().parent / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / "solver_pipeline.png"

    # Exact aspect ratio match: 960 x 712 (1.348) matches Inches(6.9) x Inches(5.12)
    # Zero stretching, zero distortion, generous internal padding
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="960" height="712" viewBox="0 0 960 712">
  <defs>
    <linearGradient id="bgCanvas" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FAFC"/>
    </linearGradient>

    <!-- Gradients -->
    <linearGradient id="optHeaderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1E40AF"/>
      <stop offset="100%" stop-color="#1D4ED8"/>
    </linearGradient>

    <linearGradient id="coreHeaderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#047857"/>
      <stop offset="100%" stop-color="#065F46"/>
    </linearGradient>

    <linearGradient id="exportHeaderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>

    <filter id="boxShadow" x="-10%" y="-10%" width="125%" height="130%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.08"/>
    </filter>
  </defs>

  <style>
    .font-title { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 700; }
    .font-sub { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 600; }
    .font-body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 400; }
    .font-math { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 600; font-size: 11.5px; }
    .font-code { font-family: 'Consolas', 'Courier New', monospace; font-size: 11px; fill: #334155; }
    .font-badge { font-family: 'Consolas', monospace; font-weight: 700; font-size: 10.5px; }
  </style>

  <!-- Outer Canvas Container -->
  <rect x="2" y="2" width="956" height="708" rx="16" fill="url(#bgCanvas)" stroke="#E2E8F0" stroke-width="2"/>

  <!-- Diagram Header Tag & Title -->
  <rect x="22" y="16" width="310" height="26" rx="13" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5"/>
  <text x="35" y="33" class="font-badge" fill="#047857">PRESCRIPTIVE AI • GOOGLE OR-TOOLS MILP</text>
  <text x="22" y="68" class="font-title" font-size="18.5" fill="#0F172A">Математический солвер: мгновенный синтез реструктуризации</text>

  <!-- ======================================================================= -->
  <!-- LEVEL 1: INPUT FROM NEURAL NETWORK (TOP)                                -->
  <!-- ======================================================================= -->
  <g transform="translate(22, 90)" filter="url(#boxShadow)">
    <rect width="916" height="130" rx="12" fill="#FFFFFF" stroke="#93C5FD" stroke-width="2"/>
    <rect width="916" height="34" rx="12" fill="url(#optHeaderGrad)"/>
    <rect y="22" width="916" height="12" fill="url(#optHeaderGrad)"/>
    <text x="16" y="22" class="font-sub" font-size="13" fill="#FFFFFF">1. Входной сигнал от предиктивной нейросети (Pre-delinquency Early Warning)</text>
    <rect x="805" y="6" width="95" height="22" rx="11" fill="#172554"/>
    <text x="852" y="21" text-anchor="middle" class="font-badge" fill="#93C5FD">Pre-Default</text>

    <!-- Two columns inside Input Box -->
    <text x="16" y="58" class="font-sub" font-size="11.5" fill="#1D4ED8">Финансовые параметры заемщика:</text>
    <text x="16" y="78" class="font-code">• Остаток долга (Principal): ₸4 200 000</text>
    <text x="16" y="98" class="font-code">• Текущий платеж: ₸145 000 / месяц</text>
    <text x="16" y="118" class="font-code">• Свободный кэшфлоу семьи: ₸65 000 / месяц</text>

    <text x="440" y="58" class="font-sub" font-size="11.5" fill="#DC2626">Сигнал скрытого стресса (Dual-Tower Net):</text>
    <text x="440" y="78" class="font-code">• Вероятность дефолта (P_def): 84.2% (Критическая)</text>
    <text x="440" y="98" class="font-code">• Прогноз до кассового разрыва: через 14 дней</text>
    <text x="440" y="118" class="font-code">• Обычный банк: слеп (платеж еще не просрочен, DPD = 0)</text>
  </g>

  <!-- Connective Flow Arrow to Solver Core -->
  <path d="M 480 220 L 480 248" stroke="#047857" stroke-width="3" fill="none"/>

  <!-- ======================================================================= -->
  <!-- LEVEL 2: GOOGLE OR-TOOLS MILP SOLVER CORE (CENTER)                      -->
  <!-- ======================================================================= -->
  <g transform="translate(22, 248)" filter="url(#boxShadow)">
    <rect width="916" height="300" rx="14" fill="#FFFFFF" stroke="#10B981" stroke-width="2.5"/>
    <rect width="916" height="36" rx="14" fill="url(#coreHeaderGrad)"/>
    <rect y="24" width="916" height="12" fill="url(#coreHeaderGrad)"/>
    <text x="18" y="24" class="font-sub" font-size="13.5" fill="#FFFFFF">2. Математическое ядро оптимизации: Google OR-Tools MILP (SCIP Solver)</text>
    <rect x="805" y="7" width="95" height="22" rx="11" fill="#064E3B"/>
    <text x="852" y="22" text-anchor="middle" class="font-badge" fill="#6EE7B7">12 ms Speed</text>

    <!-- Sub-Block A: Objective Function (Left) -->
    <g transform="translate(16, 48)">
      <rect width="435" height="175" rx="10" fill="#F0FDF4" stroke="#A7F3D0" stroke-width="1.5"/>
      <text x="14" y="24" class="font-sub" font-size="12" fill="#047857">🎯 Целевая функция банка (NPV Recovery):</text>
      <text x="14" y="46" class="font-math" fill="#0F172A">Maximize NPV = ∑ [ CF_m / (1 + r)ᵐ ] · (1 - P_def)</text>
      <text x="14" y="66" class="font-math" font-size="11" fill="#64748B">минус ожидаемые потери банка: - (Balance · LGD · P_def)</text>
      
      <text x="14" y="96" class="font-body" font-size="11.5" fill="#334155">• Максимизирует приведенную стоимость возврата долга</text>
      <text x="14" y="116" class="font-body" font-size="11.5" fill="#334155">• Защищает банк от списания кредита в убыток (Stage 3)</text>
      <text x="14" y="136" class="font-body" font-size="11.5" fill="#334155">• Рассчитывает WACC и дисконтирование денежных потоков</text>

      <rect x="14" y="146" width="405" height="20" rx="4" fill="#DCFCE7"/>
      <text x="24" y="160" class="font-badge" fill="#15803D">Смягчает график без списания основного долга</text>
    </g>

    <!-- Sub-Block B: Regulatory Constraints (Right) -->
    <g transform="translate(465, 48)">
      <rect width="435" height="175" rx="10" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5"/>
      <text x="14" y="24" class="font-sub" font-size="12" fill="#334155">⚖️ Ограничения регулятора АРРФР и Банка:</text>
      <text x="14" y="46" class="font-code">• КДН (DTI) ≤ 50% от дохода заемщика (АРРФР 2026)</text>
      <text x="14" y="66" class="font-code">• Лимит пролонгации срока: ΔT ≤ 24 месяца</text>
      <text x="14" y="86" class="font-code">• Платеж post-grace ≤ 85% свободного кэшфлоу семьи</text>
      <text x="14" y="106" class="font-code">• Кредитные каникулы (Grace period) ≤ 3 месяцев</text>
      <text x="14" y="126" class="font-code">• Условие единственности: ∑ x_t,g = 1, x_t,g ∈ {0, 1}</text>

      <rect x="14" y="146" width="405" height="20" rx="4" fill="#FEF3C7"/>
      <text x="24" y="160" class="font-badge" fill="#B45309">100% Соответствие законодательству РК</text>
    </g>

    <!-- Bottom Performance Banner inside Solver -->
    <rect x="16" y="234" width="884" height="52" rx="8" fill="#ECFDF5" stroke="#A7F3D0"/>
    <text x="26" y="254" class="font-sub" font-size="12" fill="#065F46">⚡ Мгновенный перебор 36+ комбинаций параметров за 12 миллисекунд:</text>
    <text x="26" y="272" class="font-body" font-size="11.5" fill="#334155">Вместо 3–5 рабочих дней кредитного комитета алгоритм находит математический оптимум без участия человека (STP).</text>
  </g>

  <!-- Connective Flow Arrow to Output -->
  <path d="M 480 548 L 480 572" stroke="#0F172A" stroke-width="3" fill="none"/>

  <!-- ======================================================================= -->
  <!-- LEVEL 3: DISPATCH TO DIGITAL MOBILE BANKING (BOTTOM)                    -->
  <!-- ======================================================================= -->
  <g transform="translate(22, 572)" filter="url(#boxShadow)">
    <rect width="916" height="120" rx="12" fill="#FFFFFF" stroke="#64748B" stroke-width="2"/>
    <rect width="916" height="34" rx="12" fill="url(#exportHeaderGrad)"/>
    <rect y="22" width="916" height="12" fill="url(#exportHeaderGrad)"/>
    <text x="16" y="22" class="font-sub" font-size="13" fill="#FFFFFF">3. Результат: Мгновенная доставка 3 персональных офферов в мобильный банк (ДБО)</text>
    <rect x="785" y="6" width="115" height="22" rx="11" fill="#0F172A"/>
    <text x="842" y="21" text-anchor="middle" class="font-badge" fill="#94A3B8">Push-Delivery</text>

    <!-- 3 Mini Offer Pills -->
    <g transform="translate(16, 44)">
      <rect width="280" height="62" rx="8" fill="#F0FDF4" stroke="#86EFAC"/>
      <text x="12" y="20" class="font-sub" font-size="11" fill="#15803D">СЦЕНАРИЙ А (Оптимум)</text>
      <text x="12" y="38" class="font-code">• Срок: +18 мес. | Платеж: ₸89 500 (-38%)</text>
      <text x="12" y="52" class="font-code">• КДН: 32% • NPV Recovery: 98.4%</text>
    </g>

    <g transform="translate(318, 44)">
      <rect width="280" height="62" rx="8" fill="#FEF3C7" stroke="#FDE68A"/>
      <text x="12" y="20" class="font-sub" font-size="11" fill="#B45309">СЦЕНАРИЙ Б (Каникулы 90 дней)</text>
      <text x="12" y="38" class="font-code">• Платеж: ₸0 на 3 месяца</text>
      <text x="12" y="52" class="font-code">• Ликвидация кассового разрыва</text>
    </g>

    <g transform="translate(620, 44)">
      <rect width="280" height="62" rx="8" fill="#EFF6FF" stroke="#BFDBFE"/>
      <text x="12" y="20" class="font-sub" font-size="11" fill="#1D4ED8">СЦЕНАРИЙ В (Грейс по долгу)</text>
      <text x="12" y="38" class="font-code">• Выплата только % (₸32 000) 6 мес.</text>
      <text x="12" y="52" class="font-code">• Защита при затяжном спаде</text>
    </g>
  </g>
</svg>"""

    with open(out_png, "wb") as f:
        f.write(resvg_py.svg_to_bytes(svg))
    print(f"[OK] Perfectly proportioned Solver diagram generated: {out_png}")

if __name__ == "__main__":
    generate_solver_diagram()
