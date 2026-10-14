import resvg_py
from pathlib import Path

def generate_stalker_diagram():
    out_dir = Path(__file__).resolve().parent / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / "stalker_engine.png"

    # Exact aspect ratio: 960 x 712 (1.348:1) matches Inches(6.9) x Inches(5.12)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="960" height="712" viewBox="0 0 960 712">
  <defs>
    <linearGradient id="bgCanvas" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FAFC"/>
    </linearGradient>

    <!-- Crimson Gradient for Stalker Radar -->
    <linearGradient id="stalkerHeaderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#DC2626"/>
      <stop offset="100%" stop-color="#991B1B"/>
    </linearGradient>

    <linearGradient id="coreHeaderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>

    <linearGradient id="dispatchGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#047857"/>
      <stop offset="100%" stop-color="#065F46"/>
    </linearGradient>

    <filter id="boxShadow" x="-10%" y="-10%" width="125%" height="130%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.08"/>
    </filter>
  </defs>

  <style>
    .font-title { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 700; }
    .font-sub { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 600; }
    .font-body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 400; }
    .font-code { font-family: 'Consolas', 'Courier New', monospace; font-size: 10.5px; fill: #334155; }
    .font-badge { font-family: 'Consolas', monospace; font-weight: 700; font-size: 10px; }
  </style>

  <!-- Outer Canvas Container -->
  <rect x="2" y="2" width="956" height="708" rx="16" fill="url(#bgCanvas)" stroke="#E2E8F0" stroke-width="2"/>

  <!-- Diagram Header Tag & Title -->
  <rect x="22" y="16" width="310" height="26" rx="13" fill="#FEF2F2" stroke="#FECACA" stroke-width="1.5"/>
  <text x="35" y="33" class="font-badge" fill="#DC2626">STALKER ENGINE • ПОТОКОВЫЙ РАДАР 24/7</text>
  <text x="22" y="68" class="font-title" font-size="18.5" fill="#0F172A">Круглосуточный мониторинг стресс-событий на .NET 8</text>

  <!-- ======================================================================= -->
  <!-- LEVEL 1: 6 STREAMING STRESS TRIGGERS (TOP)                              -->
  <!-- ======================================================================= -->
  <g transform="translate(22, 90)" filter="url(#boxShadow)">
    <rect width="916" height="155" rx="12" fill="#FFFFFF" stroke="#FCA5A5" stroke-width="2"/>
    <rect width="916" height="34" rx="12" fill="url(#stalkerHeaderGrad)"/>
    <rect y="22" width="916" height="12" fill="url(#stalkerHeaderGrad)"/>
    <text x="16" y="22" class="font-sub" font-size="13" fill="#FFFFFF">1. Потоковые триггеры стресса: перехват аномалий в режиме реального времени</text>
    <rect x="805" y="6" width="95" height="22" rx="11" fill="#7F1D1D"/>
    <text x="852" y="21" text-anchor="middle" class="font-badge" fill="#FEE2E2">Streaming</text>

    <!-- 6 Trigger Badges in 2 Rows x 3 Cols -->
    <g transform="translate(16, 44)">
      <!-- T1: MFO -->
      <rect width="280" height="46" rx="6" fill="#FEF2F2" stroke="#FECACA"/>
      <text x="10" y="18" class="font-sub" font-size="11" fill="#991B1B">🚨 MfoTransfer (Перевод в МФО)</text>
      <text x="10" y="34" class="font-code">Всплеск риска: ΔRisk = +0.42 (CRITICAL)</text>

      <!-- T2: Salary Delay -->
      <rect x="295" width="280" height="46" rx="6" fill="#FEF3C7" stroke="#FDE68A"/>
      <text x="305" y="18" class="font-sub" font-size="11" fill="#B45309">⏳ SalaryDelay (Задержка зарплаты)</text>
      <text x="305" y="34" class="font-code">Опоздание на 7–10 дней: ΔRisk = +0.35</text>

      <!-- T3: Salary Cut -->
      <rect x="590" width="295" height="46" rx="6" fill="#FFF1F2" stroke="#FECDD3"/>
      <text x="600" y="18" class="font-sub" font-size="11" fill="#BE123C">📉 SalaryCut (Спад дохода &gt; 30%)</text>
      <text x="600" y="34" class="font-code">Шок ликвидности: ΔRisk = +0.38</text>

      <!-- T4: BNPL Surge -->
      <rect y="54" width="280" height="46" rx="6" fill="#FAF5FF" stroke="#E9D5FF"/>
      <text x="10" y="72" class="font-sub" font-size="11" fill="#7E22CE">🛍️ BnplSurge (5+ рассрочек 0-0-24)</text>
      <text x="10" y="88" class="font-code">Перегрузка рассрочками: ΔRisk = +0.28</text>

      <!-- T5: DBO Night Anxiety -->
      <rect x="295" y="54" width="280" height="46" rx="6" fill="#F1F5F9" stroke="#CBD5E1"/>
      <text x="305" y="72" class="font-sub" font-size="11" fill="#334155">🌙 DboNightAnxiety (Входы 3 AM)</text>
      <text x="305" y="88" class="font-code">Паника в графике выплат: ΔRisk = +0.15</text>

      <!-- T6: Balance Zero -->
      <rect x="590" y="54" width="295" height="46" rx="6" fill="#FEF2F2" stroke="#F87171"/>
      <text x="600" y="72" class="font-sub" font-size="11" fill="#991B1B">⚠️ BalanceZeroOut (&lt; 1000 ₸)</text>
      <text x="600" y="88" class="font-code">Обнуление за 10 дней: ΔRisk = +0.25</text>
    </g>
  </g>

  <!-- Connective Flow Arrow -->
  <path d="M 480 245 L 480 272" stroke="#DC2626" stroke-width="3" fill="none"/>

  <!-- ======================================================================= -->
  <!-- LEVEL 2: STALKER ENGINE CORE (.NET 8 & SIGNALR) (CENTER)                -->
  <!-- ======================================================================= -->
  <g transform="translate(22, 272)" filter="url(#boxShadow)">
    <rect width="916" height="230" rx="14" fill="#FFFFFF" stroke="#0F172A" stroke-width="2.5"/>
    <rect width="916" height="36" rx="14" fill="url(#coreHeaderGrad)"/>
    <rect y="24" width="916" height="12" fill="url(#coreHeaderGrad)"/>
    <text x="18" y="24" class="font-sub" font-size="13.5" fill="#FFFFFF">2. Ядро Stalker Engine: Реактивная обрабока в бэкенде (.NET 8 / Clean Architecture)</text>
    <rect x="805" y="7" width="95" height="22" rx="11" fill="#0F172A"/>
    <text x="852" y="22" text-anchor="middle" class="font-badge" fill="#94A3B8">&lt; 15 ms latency</text>

    <!-- Sub-Block 1: Watch State Machine (Left) -->
    <g transform="translate(18, 48)">
      <rect width="425" height="165" rx="10" fill="#F8FAFC" stroke="#CBD5E1"/>
      <text x="14" y="22" class="font-sub" font-size="12" fill="#0F172A">Состояние надзора (Watch State Machine):</text>
      <text x="14" y="44" class="font-code">• Флаг надзора: IsUnderStalkerWatch = true</text>
      <text x="14" y="62" class="font-code">• Светофор зон риска:</text>
      
      <!-- Risk Pills -->
      <rect x="14" y="72" width="115" height="20" rx="4" fill="#DCFCE7"/>
      <text x="22" y="86" class="font-badge" fill="#15803D">GREEN (&lt; 0.35)</text>

      <rect x="140" y="72" width="125" height="20" rx="4" fill="#FEF3C7"/>
      <text x="148" y="86" class="font-badge" fill="#B45309">YELLOW (0.35-0.60)</text>

      <rect x="275" y="72" width="110" height="20" rx="4" fill="#FEE2E2"/>
      <text x="285" y="86" class="font-badge" fill="#991B1B">RED (≥ 0.60)</text>

      <text x="14" y="114" class="font-body" font-size="11.5" fill="#334155">• Триггер тревоги: ΔRisk ≥ 0.10 ИЛИ RiskScore ≥ 0.50</text>
      <text x="14" y="132" class="font-body" font-size="11.5" fill="#334155">• Ведение истории: StalkerTimelineSnapshot в БД</text>
      <text x="14" y="150" class="font-code" fill="#047857">✓ Обработано без блокировок через AsNoTracking</text>
    </g>

    <!-- Sub-Block 2: Bilingual Reason Generation (Right) -->
    <g transform="translate(460, 48)">
      <rect width="438" height="165" rx="10" fill="#F0FDF4" stroke="#A7F3D0"/>
      <text x="14" y="22" class="font-sub" font-size="12" fill="#065F46">Двуязычная генерация причин (RU / KZ):</text>
      
      <text x="14" y="44" class="font-code" font-weight="700" fill="#0F172A">RU:</text>
      <text x="38" y="44" class="font-body" font-size="11" fill="#334155">«Зафиксирован перевод в МФО. Риск долговой спирали»</text>

      <text x="14" y="66" class="font-code" font-weight="700" fill="#0F172A">KZ:</text>
      <text x="38" y="66" class="font-body" font-size="11" fill="#334155">«МҚҰ пайдасына аударым тіркелді. Қарыз қаупі»</text>

      <rect x="14" y="82" width="410" height="70" rx="6" fill="#FFFFFF" stroke="#86EFAC"/>
      <text x="22" y="100" class="font-sub" font-size="11.5" fill="#15803D">🎯 Рекомендованное действие (STP Action):</text>
      <text x="22" y="118" class="font-body" font-size="11" fill="#334155">«Немедленная превентивная реструктуризация</text>
      <text x="22" y="134" class="font-body" font-size="11" fill="#334155">(Кредитные каникулы на 2 мес. / Солвер OR-Tools)»</text>
    </g>
  </g>

  <!-- Connective Flow Arrow -->
  <path d="M 480 502 L 480 528" stroke="#047857" stroke-width="3" fill="none"/>

  <!-- ======================================================================= -->
  <!-- LEVEL 3: SIGNALR WEBSOCKETS DISPATCH (BOTTOM)                           -->
  <!-- ======================================================================= -->
  <g transform="translate(22, 528)" filter="url(#boxShadow)">
    <rect width="916" height="165" rx="12" fill="#FFFFFF" stroke="#10B981" stroke-width="2"/>
    <rect width="916" height="34" rx="12" fill="url(#dispatchGrad)"/>
    <rect y="22" width="916" height="12" fill="url(#dispatchGrad)"/>
    <text x="16" y="22" class="font-sub" font-size="13" fill="#FFFFFF">3. Мгновенная доставка: SignalR WebSockets и запуск спасения заемщика</text>
    <rect x="795" y="6" width="105" height="22" rx="11" fill="#064E3B"/>
    <text x="847" y="21" text-anchor="middle" class="font-badge" fill="#A7F3D0">WebSockets</text>

    <!-- 2 Distribution Channels -->
    <g transform="translate(18, 46)">
      <rect width="425" height="105" rx="8" fill="#F0FDF4" stroke="#86EFAC"/>
      <text x="14" y="22" class="font-sub" font-size="12" fill="#15803D">📡 Терминал риск-офицера банка (StalkerHub):</text>
      <text x="14" y="42" class="font-code">• Группа: Clients.Group("RiskOfficersGlobal")</text>
      <text x="14" y="58" class="font-code">• Событие: SendAsync("StalkerAlertReceived", alert)</text>
      <text x="14" y="74" class="font-body" font-size="11" fill="#334155">Всплывающий пуш на мониторе риск-менеджера за 12 мс</text>
      <rect x="14" y="82" width="190" height="18" rx="4" fill="#DCFCE7"/>
      <text x="22" y="95" class="font-badge" fill="#166534">Без ручного опроса (Zero Polling)</text>
    </g>

    <g transform="translate(460, 46)">
      <rect width="438" height="105" rx="8" fill="#EFF6FF" stroke="#BFDBFE"/>
      <text x="14" y="22" class="font-sub" font-size="12" fill="#1D4ED8">📲 Мобильный банк заемщика (Превентивный оффер):</text>
      <text x="14" y="42" class="font-code">• Автовызов солвера OR-Tools MILP</text>
      <text x="14" y="58" class="font-code">• Расчет 3 щадящих графиков с КДН ≤ 50%</text>
      <text x="14" y="74" class="font-body" font-size="11" fill="#334155">Push-уведомление клиенту за 30 дней до дефолта</text>
      <rect x="14" y="82" width="205" height="18" rx="4" fill="#DBEAFE"/>
      <text x="22" y="95" class="font-badge" fill="#1E40AF">100% STP Автоматизация</text>
    </g>
  </g>
</svg>"""

    with open(out_png, "wb") as f:
        f.write(resvg_py.svg_to_bytes(svg))
    print(f"[OK] Stalker Engine diagram generated: {out_png}")

if __name__ == "__main__":
    generate_stalker_diagram()
