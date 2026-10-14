import resvg_py
from pathlib import Path

def generate_agent_world_diagram():
    out_dir = Path(__file__).resolve().parent / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / "agent_world_simulation.png"

    # Exact aspect ratio: 960 x 712 (1.348:1) matches Inches(6.9) x Inches(5.12)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="960" height="712" viewBox="0 0 960 712">
  <defs>
    <linearGradient id="bgCanvas" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FAFC"/>
    </linearGradient>

    <!-- Indigo Gradient for Archetypes -->
    <linearGradient id="archetypesGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1E1B4B"/>
      <stop offset="100%" stop-color="#312E81"/>
    </linearGradient>

    <!-- Emerald Teal Gradient for RL Engine -->
    <linearGradient id="rlGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#064E3B"/>
      <stop offset="100%" stop-color="#047857"/>
    </linearGradient>

    <!-- Dark Blue Gradient for Closed Loop -->
    <linearGradient id="loopGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>

    <filter id="boxShadow" x="-10%" y="-10%" width="125%" height="130%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.08"/>
    </filter>
  </defs>

  <style>
    .font-title { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 700; }
    .font-sub { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 600; }
    .font-body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 400; }
    .font-code { font-family: 'Consolas', 'Courier New', monospace; font-size: 10px; fill: #334155; }
    .font-badge { font-family: 'Consolas', monospace; font-weight: 700; font-size: 10px; }
  </style>

  <!-- Outer Canvas Container -->
  <rect x="2" y="2" width="956" height="708" rx="16" fill="url(#bgCanvas)" stroke="#E2E8F0" stroke-width="2"/>

  <!-- Diagram Header Tag & Title -->
  <rect x="22" y="14" width="375" height="25" rx="12.5" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="1.5"/>
  <text x="35" y="31" class="font-badge" fill="#4338CA">AGENT-WORLD SANDBOX • ДИСКРЕТНО-СОБЫТИЙНЫЙ ПОЛИГОН</text>
  <text x="22" y="64" class="font-title" font-size="18.5" fill="#0F172A">Мультиагентная среда симуляции заемщиков и стресс-тестов</text>

  <!-- ======================================================================= -->
  <!-- LEVEL 1: 3 SYNTHETIC BORROWER ARCHETYPES                                 -->
  <!-- ======================================================================= -->
  <g transform="translate(22, 80)" filter="url(#boxShadow)">
    <rect width="916" height="175" rx="12" fill="#FFFFFF" stroke="#C7D2FE" stroke-width="2"/>
    <rect width="916" height="32" rx="12" fill="url(#archetypesGrad)"/>
    <rect y="20" width="916" height="12" fill="url(#archetypesGrad)"/>
    <text x="18" y="22" class="font-sub" font-size="12" fill="#FFFFFF">1. Профили агентов-заемщиков: синтетические архетипы клиентов Казахстана</text>
    <rect x="795" y="6" width="105" height="20" rx="10" fill="#312E81" stroke="#6366F1" stroke-width="1"/>
    <text x="806" y="20" class="font-badge" fill="#E0E7FF">3 Archetypes</text>

    <!-- Bot 1: Arman -->
    <g transform="translate(14, 42)">
      <rect width="286" height="122" rx="8" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1.5"/>
      <circle cx="28" cy="26" r="16" fill="#DCFCE7"/>
      <text x="20" y="32" font-size="18">👨‍💻</text>
      <text x="52" y="22" class="font-title" font-size="12" fill="#14532D">Арман (IT-Сеньор)</text>
      <text x="52" y="36" class="font-badge" fill="#16A34A">TECH_OPTIMIST • Класс AAA</text>
      
      <line x1="12" y1="46" x2="274" y2="46" stroke="#BBF7D0" stroke-width="1"/>
      <text x="14" y="62" class="font-code">• Доход: 1 200 000 ₸ | Долг: 4 200 000 ₸</text>
      <text x="14" y="78" class="font-code">• Платеж: 145 000 ₸/мес (DTI = 12%)</text>
      <text x="14" y="94" class="font-code">• Базовый риск: <tspan fill="#15803D" font-weight="bold">PD = 1.05%</tspan> | Баланс: 650k ₸</text>
      <text x="14" y="110" class="font-body" font-size="9.5" fill="#166534">⚠ Уязвимость: задержка выплат инвойсов</text>
    </g>

    <!-- Bot 2: Zhanna -->
    <g transform="translate(315, 42)">
      <rect width="286" height="122" rx="8" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.5"/>
      <circle cx="28" cy="26" r="16" fill="#FEE2E2"/>
      <text x="20" y="32" font-size="18">👩‍💼</text>
      <text x="52" y="22" class="font-title" font-size="12" fill="#991B1B">Жанна (Маркетолог)</text>
      <text x="52" y="36" class="font-badge" fill="#DC2626">VULNERABLE • Класс BBB</text>
      
      <line x1="12" y1="46" x2="274" y2="46" stroke="#FECACA" stroke-width="1"/>
      <text x="14" y="62" class="font-code">• Доход: 420 000 ₸ | Долг: 2 600 000 ₸</text>
      <text x="14" y="78" class="font-code">• Платеж: 185 000 ₸/мес (DTI = 44%)</text>
      <text x="14" y="94" class="font-code">• Базовый риск: <tspan fill="#DC2626" font-weight="bold">PD = 16.8% → 84%</tspan></text>
      <text x="14" y="110" class="font-body" font-size="9.5" fill="#991B1B">⚠ Уязвимость: 5+ BNPL рассрочек, ночи в ДБО</text>
    </g>

    <!-- Bot 3: Sanzhar -->
    <g transform="translate(616, 42)">
      <rect width="286" height="122" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5"/>
      <circle cx="28" cy="26" r="16" fill="#E2E8F0"/>
      <text x="20" y="32" font-size="18">👷‍♂️</text>
      <text x="52" y="22" class="font-title" font-size="12" fill="#0F172A">Санжар (Инженер)</text>
      <text x="52" y="36" class="font-badge" fill="#475569">PRAGMATIC • Класс AA</text>
      
      <line x1="12" y1="46" x2="274" y2="46" stroke="#E2E8F0" stroke-width="1"/>
      <text x="14" y="62" class="font-code">• Доход: 850 000 ₸ | Долг: 3 800 000 ₸</text>
      <text x="14" y="78" class="font-code">• Платеж: 160 000 ₸/мес (DTI = 19%)</text>
      <text x="14" y="94" class="font-code">• Базовый риск: <tspan fill="#334155" font-weight="bold">PD = 4.80%</tspan> | Баланс: 420k ₸</text>
      <text x="14" y="110" class="font-body" font-size="9.5" fill="#475569">✓ Контрольная группа высокой дисциплины</text>
    </g>
  </g>

  <!-- Connective flow arrow -->
  <line x1="480" y1="257" x2="480" y2="273" stroke="#059669" stroke-width="3" stroke-dasharray="4,3"/>
  <polygon points="480,277 475,269 485,269" fill="#059669"/>

  <!-- ======================================================================= -->
  <!-- LEVEL 2: FINANCIAL RL BRAIN & ACTION DISPATCH                            -->
  <!-- ======================================================================= -->
  <g transform="translate(22, 280)" filter="url(#boxShadow)">
    <rect width="916" height="185" rx="12" fill="#FFFFFF" stroke="#6EE7B7" stroke-width="2"/>
    <rect width="916" height="32" rx="12" fill="url(#rlGrad)"/>
    <rect y="20" width="916" height="12" fill="url(#rlGrad)"/>
    <text x="18" y="22" class="font-sub" font-size="12" fill="#FFFFFF">2. Интеллектуальное ядро FinancialRLBrain: 10 типов событий и динамика кошелька</text>
    <rect x="785" y="6" width="115" height="20" rx="10" fill="#065F46" stroke="#34D399" stroke-width="1"/>
    <text x="797" y="20" class="font-badge" fill="#A7F3D0">Step: 2.5s Tick</text>

    <!-- Left Box: 10 Action types -->
    <g transform="translate(14, 42)">
      <rect width="436" height="132" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
      <text x="14" y="20" class="font-title" font-size="11" fill="#0F172A">Событийные триггеры поведения (Action Types):</text>
      
      <!-- Safe actions row -->
      <g transform="translate(12, 30)">
        <rect width="198" height="20" rx="4" fill="#DCFCE7" stroke="#86EFAC"/>
        <text x="8" y="14" class="font-badge" fill="#15803D">✓ SALARY_ON_TIME (Вовремя)</text>
        <rect x="206" width="198" height="20" rx="4" fill="#DCFCE7" stroke="#86EFAC"/>
        <text x="214" y="14" class="font-badge" fill="#15803D">✓ INSTALLMENT_PAID (График)</text>
      </g>

      <g transform="translate(12, 54)">
        <rect width="198" height="20" rx="4" fill="#F0FDF4" stroke="#BBF7D0"/>
        <text x="8" y="14" class="font-badge" fill="#166534">✓ FREELANCE_INCOME (+Бонус)</text>
        <rect x="206" width="198" height="20" rx="4" fill="#F0FDF4" stroke="#BBF7D0"/>
        <text x="214" y="14" class="font-badge" fill="#166534">✓ EXPENSE_OPTIMIZED (-Траты)</text>
      </g>

      <!-- Stress actions row -->
      <g transform="translate(12, 78)">
        <rect width="198" height="20" rx="4" fill="#FEF3C7" stroke="#FCD34D"/>
        <text x="8" y="14" class="font-badge" fill="#B45309">⚠ SALARY_DELAY (+0.35 PD)</text>
        <rect x="206" width="198" height="20" rx="4" fill="#FEF3C7" stroke="#FCD34D"/>
        <text x="214" y="14" class="font-badge" fill="#B45309">⚠ NIGHT_APP_CHECK (+0.15 PD)</text>
      </g>

      <g transform="translate(12, 102)">
        <rect width="198" height="20" rx="4" fill="#FEE2E2" stroke="#FCA5A5"/>
        <text x="8" y="14" class="font-badge" fill="#DC2626">🚨 MICROLOAN_TAKEN (+0.42 PD)</text>
        <rect x="206" width="198" height="20" rx="4" fill="#FEE2E2" stroke="#FCA5A5"/>
        <text x="214" y="14" class="font-badge" fill="#DC2626">🚨 BNPL_SURGE (+0.28 PD)</text>
      </g>
    </g>

    <!-- Right Box: Dynamic State Vector -->
    <g transform="translate(466, 42)">
      <rect width="436" height="132" rx="8" fill="#F0FDF4" stroke="#A7F3D0" stroke-width="1"/>
      <text x="14" y="20" class="font-title" font-size="11" fill="#065F46">Динамическое обновление 360° вектора признаков:</text>
      <text x="14" y="40" class="font-code">• Баланс кошелька: <tspan fill="#059669">WalletBalance += (Income - Spend - Annuity)</tspan></text>
      <text x="14" y="58" class="font-code">• Обратный отсчет: <tspan fill="#059669">DaysToPayment = max(1, DaysToPayment - 1)</tspan></text>
      <text x="14" y="76" class="font-code">• Синтез тензора 43 фичей: [28 credit_cols + 15 behavior_cols]</text>
      <text x="14" y="94" class="font-code">• Утилизация карт, скоринг бюро, чеки ДБО и скейлеры</text>
      
      <rect x="14" y="104" width="408" height="20" rx="4" fill="#DCFCE7" stroke="#86EFAC"/>
      <text x="22" y="118" class="font-badge" fill="#14532D">⚡ Передача в PyTorch RealMlEngineInference без задержки</text>
    </g>
  </g>

  <!-- Connective flow arrow -->
  <line x1="480" y1="467" x2="480" y2="483" stroke="#0F172A" stroke-width="3" stroke-dasharray="4,3"/>
  <polygon points="480,487 475,479 485,479" fill="#0F172A"/>

  <!-- ======================================================================= -->
  <!-- LEVEL 3: CLOSED-LOOP VALIDATION WITH ML & OR-TOOLS                       -->
  <!-- ======================================================================= -->
  <g transform="translate(22, 490)" filter="url(#boxShadow)">
    <rect width="916" height="205" rx="12" fill="#FFFFFF" stroke="#94A3B8" stroke-width="2"/>
    <rect width="916" height="32" rx="12" fill="url(#loopGrad)"/>
    <rect y="20" width="916" height="12" fill="url(#loopGrad)"/>
    <text x="18" y="22" class="font-sub" font-size="12" fill="#FFFFFF">3. Замкнутый контур: Инференс PyTorch Dual-Tower → Алерт Stalker → Решение OR-Tools</text>
    <rect x="765" y="6" width="135" height="20" rx="10" fill="#1E293B" stroke="#64748B" stroke-width="1"/>
    <text x="778" y="20" class="font-badge" fill="#F1F5F9">Closed-Loop &lt;15ms</text>

    <!-- Stage 1: PyTorch Inference -->
    <g transform="translate(14, 42)">
      <rect width="286" height="150" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
      <rect x="10" y="10" width="130" height="20" rx="4" fill="#EEF2FF" stroke="#C7D2FE"/>
      <text x="16" y="24" class="font-badge" fill="#4338CA">STAGE 1: ML INFERENCE</text>
      <text x="10" y="46" class="font-title" font-size="11" fill="#0F172A">PyTorch Dual-Tower Network</text>
      <text x="10" y="64" class="font-code">• Cross-Attention матрица [7×9]</text>
      <text x="10" y="80" class="font-code">• Мгновенный расчет PD за &lt;12 ms</text>
      <text x="10" y="96" class="font-code">• GMM кластеризация дистресса:</text>
      <text x="20" y="112" class="font-badge" fill="#B45309">PANIC_BORROWING / STABLE</text>
      <text x="10" y="132" class="font-body" font-size="9" fill="#64748B">Непрерывный пересчет риска на каждом шаге</text>
    </g>

    <!-- Connector 1 -> 2 -->
    <polygon points="304,112 312,117 304,122" fill="#64748B"/>

    <!-- Stage 2: Stalker Stream -->
    <g transform="translate(315, 42)">
      <rect width="286" height="150" rx="8" fill="#FEF2F2" stroke="#FECACA" stroke-width="1"/>
      <rect x="10" y="10" width="135" height="20" rx="4" fill="#FEE2E2" stroke="#FCA5A5"/>
      <text x="16" y="24" class="font-badge" fill="#DC2626">STAGE 2: STALKER RADAR</text>
      <text x="10" y="46" class="font-title" font-size="11" fill="#991B1B">.NET 8 &amp; SignalR Hub</text>
      <text x="10" y="64" class="font-code">• Фиксация всплеска ΔRisk ≥ 0.10</text>
      <text x="10" y="80" class="font-code">• Флаг надзора: IsUnderWatch=true</text>
      <text x="10" y="96" class="font-code">• WebSockets алерт риск-офицеру</text>
      <text x="10" y="112" class="font-code">• Двуязычное объяснение (RU/KZ):</text>
      <text x="10" y="128" class="font-badge" fill="#B91C1C">«МҚҰ пайдасына аударым тіркелді»</text>
    </g>

    <!-- Connector 2 -> 3 -->
    <polygon points="605,112 613,117 605,122" fill="#64748B"/>

    <!-- Stage 3: OR-Tools Solver -->
    <g transform="translate(616, 42)">
      <rect width="286" height="150" rx="8" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="1"/>
      <rect x="10" y="10" width="135" height="20" rx="4" fill="#DCFCE7" stroke="#86EFAC"/>
      <text x="16" y="24" class="font-badge" fill="#15803D">STAGE 3: OR-TOOLS MILP</text>
      <text x="10" y="46" class="font-title" font-size="11" fill="#14532D">Автоматическое спасение</text>
      <text x="10" y="64" class="font-code">• Автовызов солвера реструктуризации</text>
      <text x="10" y="80" class="font-code">• Расчет 3 вариантов с КДН ≤ 50%</text>
      <text x="10" y="96" class="font-code">• 100% STP (Без кредитного комитета)</text>
      <text x="10" y="112" class="font-code">• Доставка в ДБО заемщика за 30 дней</text>
      <text x="10" y="132" class="font-badge" fill="#047857">✓ Предотвращение NPL без дефолта</text>
    </g>
  </g>
</svg>"""

    png_bytes = resvg_py.svg_to_bytes(svg)
    out_png.write_bytes(png_bytes)
    print(f"[Agent-World Generator] Successfully generated: {out_png}")
    return out_png

if __name__ == "__main__":
    generate_agent_world_diagram()
