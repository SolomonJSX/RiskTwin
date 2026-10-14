import resvg_py
from pathlib import Path

def create_palantir_diagram():
    out_dir = Path(__file__).resolve().parent / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / "palantir_concept.png"

    # 1000 x 920 crisp high-res layout
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="920" viewBox="0 0 1000 920">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="bgCanvas" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FAFC"/>
    </linearGradient>

    <linearGradient id="cardActionGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ECFDF5"/>
      <stop offset="100%" stop-color="#D1FAE5"/>
    </linearGradient>

    <linearGradient id="cardOntologyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FEF3C7"/>
      <stop offset="100%" stop-color="#FDE68A"/>
    </linearGradient>

    <linearGradient id="cardSilosGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F1F5F9"/>
      <stop offset="100%" stop-color="#E2E8F0"/>
    </linearGradient>

    <!-- Drop Shadows -->
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="125%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#0F172A" flood-opacity="0.06"/>
    </filter>

    <filter id="pillShadow" x="-10%" y="-10%" width="120%" height="125%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0F172A" flood-opacity="0.04"/>
    </filter>
  </defs>

  <style>
    .font-title { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 700; }
    .font-body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 400; }
    .font-code { font-family: 'Consolas', 'Courier New', monospace; font-weight: 600; }
  </style>

  <!-- Outer Canvas Container -->
  <rect x="2" y="2" width="996" height="916" rx="20" fill="url(#bgCanvas)" stroke="#CBD5E1" stroke-width="2"/>

  <!-- Diagram Header Bar -->
  <rect x="30" y="24" width="340" height="30" rx="15" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="1.5"/>
  <text x="45" y="44" class="font-code" font-size="12" fill="#4338CA" letter-spacing="1">PALANTIR ONTOLOGY PARADIGM</text>

  <text x="30" y="86" class="font-title" font-size="22" fill="#0F172A">Архитектура замкнутого операционного цикла</text>
  <text x="30" y="110" class="font-body" font-size="13.5" fill="#64748B">Как идея Palantir Foundry переносит фокус с «пассивных отчетов» на «автоматическое решение»</text>

  <!-- ======================================================================= -->
  <!-- LEVEL 3: ACTIONABLE OPERATIONAL DECISION (TOP)                          -->
  <!-- ======================================================================= -->
  <g filter="url(#cardShadow)">
    <rect x="40" y="135" width="920" height="195" rx="16" fill="url(#cardActionGrad)" stroke="#10B981" stroke-width="2"/>
    
    <!-- Level Badge -->
    <rect x="65" y="155" width="230" height="26" rx="13" fill="#10B981"/>
    <text x="80" y="172" class="font-code" font-size="11.5" fill="#FFFFFF" letter-spacing="0.5">УРОВЕНЬ 3: ACTIONABLE DECISION</text>

    <!-- Main Title -->
    <text x="65" y="214" class="font-title" font-size="20" fill="#065F46">Автоматическое операционное решение (Closed-Loop)</text>
    <text x="65" y="238" class="font-body" font-size="13.5" fill="#047857">Система не заканчивается на графике — она сама генерирует и исполняет оптимальное решение</text>

    <!-- Sub-cards inside Level 3 -->
    <g filter="url(#pillShadow)">
      <rect x="65" y="254" width="415" height="56" rx="10" fill="#FFFFFF" stroke="#A7F3D0" stroke-width="1.5"/>
      <circle cx="90" cy="282" r="14" fill="#ECFDF5" stroke="#10B981" stroke-width="1.5"/>
      <text x="86" y="287" class="font-title" font-size="14" fill="#059669">✓</text>
      <text x="114" y="275" class="font-title" font-size="13" fill="#0F172A">Мгновенный оффер в мобильном банке</text>
      <text x="114" y="295" class="font-body" font-size="11.5" fill="#64748B">Заемщик акцептует щадящий график в 1 клик через ЭЦП</text>

      <rect x="500" y="254" width="435" height="56" rx="10" fill="#FFFFFF" stroke="#A7F3D0" stroke-width="1.5"/>
      <circle cx="525" cy="282" r="14" fill="#ECFDF5" stroke="#10B981" stroke-width="1.5"/>
      <text x="521" y="287" class="font-title" font-size="14" fill="#059669">⚖</text>
      <text x="548" y="275" class="font-title" font-size="13" fill="#0F172A">100% регуляторное соответствие АРРФР</text>
      <text x="548" y="295" class="font-body" font-size="11.5" fill="#64748B">КДН ≤ 50% и защита капитала акционеров без провизий МСФО 9</text>
    </g>
  </g>

  <!-- ======================================================================= -->
  <!-- CONNECTOR: UP / DOWN ARROWS BETWEEN LEVEL 3 AND 2                       -->
  <!-- ======================================================================= -->
  <g>
    <!-- Arrow Line Down -->
    <path d="M 460 330 L 460 380" stroke="#059669" stroke-width="3" stroke-linecap="round" stroke-dasharray="6,4"/>
    <polygon points="460,386 454,374 466,374" fill="#059669"/>
    <text x="350" y="362" class="font-code" font-size="11.5" fill="#059669" text-anchor="end">Синтез решения ▼</text>

    <!-- Arrow Line Up -->
    <path d="M 540 380 L 540 336" stroke="#D97706" stroke-width="3" stroke-linecap="round"/>
    <polygon points="540,330 534,342 546,342" fill="#D97706"/>
    <text x="555" y="362" class="font-code" font-size="11.5" fill="#D97706">▲ Обратная связь</text>
  </g>

  <!-- ======================================================================= -->
  <!-- LEVEL 2: OPERATIONAL ONTOLOGY / DIGITAL TWIN (MIDDLE HERO)              -->
  <!-- ======================================================================= -->
  <g filter="url(#cardShadow)">
    <rect x="40" y="390" width="920" height="235" rx="16" fill="url(#cardOntologyGrad)" stroke="#F59E0B" stroke-width="2"/>

    <!-- Level Badge -->
    <rect x="65" y="410" width="260" height="26" rx="13" fill="#D97706"/>
    <text x="80" y="427" class="font-code" font-size="11.5" fill="#FFFFFF" letter-spacing="0.5">УРОВЕНЬ 2: PALANTIR ONTOLOGY</text>

    <!-- Main Title -->
    <text x="65" y="468" class="font-title" font-size="20" fill="#78350F">Онтология заемщика: Живой Цифровой Двойник (Entity)</text>
    <text x="65" y="492" class="font-body" font-size="13.5" fill="#92400E">Семантическая модель реального мира, связывающая факты, поведение и риски в динамический граф</text>

    <!-- 3 Connected Entity Nodes in Ontology -->
    <g filter="url(#pillShadow)">
      <!-- Entity 1 -->
      <rect x="65" y="512" width="270" height="92" rx="12" fill="#FFFFFF" stroke="#FDE68A" stroke-width="2"/>
      <circle cx="95" cy="538" r="16" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1.5"/>
      <text x="90" y="544" class="font-title" font-size="14" fill="#D97706">💰</text>
      <text x="120" y="536" class="font-title" font-size="13.5" fill="#0F172A">Поток ликвидности</text>
      <text x="120" y="555" class="font-body" font-size="11.5" fill="#64748B">Тренд зарплаты (3м vs 6м)</text>
      <text x="120" y="572" class="font-code" font-size="11" fill="#D97706">Задержка поступлений: +8 дн</text>

      <!-- Connecting Line 1-2 -->
      <path d="M 335 558 L 380 558" stroke="#F59E0B" stroke-width="2.5" stroke-dasharray="4,3"/>
      <circle cx="357" cy="558" r="4" fill="#F59E0B"/>

      <!-- Entity 2 (Center Hero) -->
      <rect x="380" y="512" width="280" height="92" rx="12" fill="#FFFFFF" stroke="#F59E0B" stroke-width="2"/>
      <circle cx="410" cy="538" r="16" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1.5"/>
      <text x="403" y="544" class="font-title" font-size="14" fill="#D97706">🧠</text>
      <text x="435" y="536" class="font-title" font-size="13.5" fill="#0F172A">Стресс в поведении ДБО</text>
      <text x="435" y="555" class="font-body" font-size="11.5" fill="#64748B">Ночные сессии (03:15)</text>
      <text x="435" y="572" class="font-code" font-size="11" fill="#E11D48">Зависание в графике: 42 сек</text>

      <!-- Connecting Line 2-3 -->
      <path d="M 660 558 L 705 558" stroke="#F59E0B" stroke-width="2.5" stroke-dasharray="4,3"/>
      <circle cx="682" cy="558" r="4" fill="#F59E0B"/>

      <!-- Entity 3 -->
      <rect x="705" y="512" width="240" height="92" rx="12" fill="#FFFFFF" stroke="#FDE68A" stroke-width="2"/>
      <circle cx="735" cy="538" r="16" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1.5"/>
      <text x="728" y="544" class="font-title" font-size="14" fill="#D97706">⚡</text>
      <text x="760" y="536" class="font-title" font-size="13.5" fill="#0F172A">Долговая спираль</text>
      <text x="760" y="555" class="font-body" font-size="11.5" fill="#64748B">Рассрочки 0-0-24</text>
      <text x="760" y="572" class="font-code" font-size="11" fill="#E11D48">Триггер МФО: Обнаружен</text>
    </g>
  </g>

  <!-- ======================================================================= -->
  <!-- CONNECTOR: ARROWS BETWEEN LEVEL 2 AND 1                                 -->
  <!-- ======================================================================= -->
  <g>
    <!-- Arrow Line Up from Silos -->
    <path d="M 500 685 L 500 635" stroke="#64748B" stroke-width="3" stroke-linecap="round"/>
    <polygon points="500,627 494,640 506,640" fill="#64748B"/>
    <text x="515" y="662" class="font-code" font-size="11.5" fill="#64748B">▲ Потоковая агрегация в реальном времени</text>
  </g>

  <!-- ======================================================================= -->
  <!-- LEVEL 1: DISPARATE DATA SILOS (BOTTOM)                                  -->
  <!-- ======================================================================= -->
  <g filter="url(#cardShadow)">
    <rect x="40" y="695" width="920" height="195" rx="16" fill="url(#cardSilosGrad)" stroke="#94A3B8" stroke-width="2"/>

    <!-- Level Badge -->
    <rect x="65" y="715" width="250" height="26" rx="13" fill="#64748B"/>
    <text x="80" y="732" class="font-code" font-size="11.5" fill="#FFFFFF" letter-spacing="0.5">УРОВЕНЬ 1: RAW DATA SILOS</text>

    <!-- Main Title -->
    <text x="65" y="770" class="font-title" font-size="19" fill="#1E293B">Разрозненные источники данных банка («Информационные колодцы»)</text>
    <text x="65" y="792" class="font-body" font-size="13" fill="#475569">Данные изолированы в разных хранилищах и не взаимодействуют в классическом CRM</text>

    <!-- 3 Data Silos -->
    <g filter="url(#pillShadow)">
      <rect x="65" y="808" width="270" height="64" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
      <text x="85" y="832" class="font-title" font-size="13" fill="#0F172A">📱 Телеметрия ДБО</text>
      <text x="85" y="852" class="font-body" font-size="11" fill="#64748B">Входы ночью, время на графике платежей</text>

      <rect x="365" y="808" width="270" height="64" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
      <text x="385" y="832" class="font-title" font-size="13" fill="#0F172A">💳 Транзакционные потоки</text>
      <text x="385" y="852" class="font-body" font-size="11" fill="#64748B">P2P-переводы Kaspi/Halyk, чеки МФО, ATM</text>

      <rect x="665" y="808" width="265" height="64" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
      <text x="685" y="832" class="font-title" font-size="13" fill="#0F172A">🏛️ Кредитные реестры</text>
      <text x="685" y="852" class="font-body" font-size="11" fill="#64748B">Отчеты ГКБ, кредитные карты, овердрафты</text>
    </g>
  </g>
</svg>"""

    png_bytes = resvg_py.svg_to_bytes(svg)
    out_png.write_bytes(png_bytes)
    print(f"[Diagram Generator] Successfully created beautiful scheme: {out_png}")
    return out_png

if __name__ == "__main__":
    create_palantir_diagram()
