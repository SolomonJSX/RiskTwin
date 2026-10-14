import resvg_py
from pathlib import Path

def generate_cluster_diagram():
    out_dir = Path(__file__).resolve().parent / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / "services_cluster.png"

    # Compact horizontal cluster layout: 1050 x 320 px
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="320" viewBox="0 0 1050 320">
  <defs>
    <linearGradient id="bgCanvas" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FAFC"/>
    </linearGradient>

    <!-- Psycho-Life Gradient: Purple/Violet -->
    <linearGradient id="psychoGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#6D28D9"/>
    </linearGradient>

    <!-- Stalker Gradient: Red/Crimson Alert -->
    <linearGradient id="stalkerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#EF4444"/>
      <stop offset="100%" stop-color="#B91C1C"/>
    </linearGradient>

    <!-- Flow Arrow Marker -->
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#64748B"/>
    </marker>

    <filter id="shadow" x="-10%" y="-10%" width="125%" height="130%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#0F172A" flood-opacity="0.07"/>
    </filter>
  </defs>

  <style>
    .font-title { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 700; }
    .font-sub { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 600; font-size: 12px; }
    .font-body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 400; font-size: 11px; fill: #475569; }
    .font-badge { font-family: 'Consolas', monospace; font-weight: 700; font-size: 10px; }
  </style>

  <!-- Canvas Box -->
  <rect x="2" y="2" width="1046" height="316" rx="14" fill="url(#bgCanvas)" stroke="#E2E8F0" stroke-width="2"/>

  <!-- Flow Lines -->
  <g stroke="#94A3B8" stroke-width="2.5" fill="none">
    <path d="M 230 160 L 290 160" marker-end="url(#arrow)"/>
    <path d="M 760 160 L 820 160" marker-end="url(#arrow)"/>
  </g>

  <!-- ======================================================================= -->
  <!-- NODE 1: INPUT STREAM (LEFT)                                             -->
  <!-- ======================================================================= -->
  <g transform="translate(20, 45)" filter="url(#shadow)">
    <rect width="210" height="230" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect width="210" height="32" rx="10" fill="#0F172A"/>
    <rect y="22" width="210" height="10" fill="#0F172A"/>
    <text x="14" y="21" class="font-sub" fill="#FFFFFF">Поток телеметрии клиента</text>
    <text x="14" y="60" class="font-sub" fill="#0F172A">📱 Мобильный банк ДБО:</text>
    <text x="14" y="80" class="font-body">• Время и частота сессий</text>
    <text x="14" y="98" class="font-body">• Зависание на графике выплат</text>
    <text x="14" y="116" class="font-body">• Переводы в МФО (микрозаймы)</text>
    <text x="14" y="134" class="font-body">• Задержка зарплатного чека</text>
    <text x="14" y="152" class="font-body">• P2P хаос и снятия в ATM</text>

    <rect x="14" y="175" width="182" height="42" rx="6" fill="#F1F5F9"/>
    <text x="22" y="193" class="font-badge" fill="#334155">Частота: 1200 ms</text>
    <text x="22" y="207" class="font-body" font-size="10" fill="#64748B">Event-Driven Streaming</text>
  </g>

  <!-- ======================================================================= -->
  <!-- CLUSTER ENCLOSURE (CENTER)                                              -->
  <!-- ======================================================================= -->
  <g transform="translate(290, 25)" filter="url(#shadow)">
    <!-- Outer Cluster Ring -->
    <rect width="470" height="270" rx="14" fill="#FAF5FF" stroke="#C084FC" stroke-width="2" stroke-dasharray="6,4"/>
    <rect x="150" y="8" width="170" height="20" rx="10" fill="#7E22CE"/>
    <text x="235" y="22" text-anchor="middle" class="font-badge" fill="#F3E8FF">КЛАСТЕР ОБНАРУЖЕНИЯ</text>

    <!-- SERVICE A: Psycho-Life Service (Top of cluster) -->
    <g transform="translate(20, 38)">
      <rect width="430" height="100" rx="10" fill="#FFFFFF" stroke="#C084FC" stroke-width="1.5"/>
      <rect width="430" height="28" rx="10" fill="url(#psychoGrad)"/>
      <rect y="18" width="430" height="10" fill="url(#psychoGrad)"/>
      <text x="14" y="19" class="font-sub" fill="#FFFFFF">1. Psycho-Life Service (Психометрический анализ)</text>
      <rect x="340" y="5" width="80" height="18" rx="9" fill="#4C1D95"/>
      <text x="380" y="17" text-anchor="middle" class="font-badge" fill="#E9D5FF">AI Нервы</text>

      <text x="14" y="48" class="font-sub" fill="#6B21A8">Вычисление скрытых признаков тревожности:</text>
      <text x="14" y="66" class="font-body">• DboNightAnxiety (входы в 3 AM) • BalanceDecay (падение подушки 7d)</text>
      <text x="14" y="84" class="font-body">• MfoTransfer (займы до зарплаты) • Жизненные стресс-шоки</text>
    </g>

    <!-- Bidirectional Event Stream between services -->
    <g stroke="#7E22CE" stroke-width="2" fill="none">
      <path d="M 235 138 L 235 152"/>
      <circle cx="235" cy="145" r="3" fill="#7E22CE"/>
    </g>

    <!-- SERVICE B: Stalker Engine (Bottom of cluster) -->
    <g transform="translate(20, 152)">
      <rect width="430" height="100" rx="10" fill="#FFFFFF" stroke="#F87171" stroke-width="1.5"/>
      <rect width="430" height="28" rx="10" fill="url(#stalkerGrad)"/>
      <rect y="18" width="430" height="10" fill="url(#stalkerGrad)"/>
      <text x="14" y="19" class="font-sub" fill="#FFFFFF">2. Stalker Engine (.NET 8 &amp; SignalR WebSockets)</text>
      <rect x="330" y="5" width="90" height="18" rx="9" fill="#7F1D1D"/>
      <text x="375" y="17" text-anchor="middle" class="font-badge" fill="#FEE2E2">Радар 24/7</text>

      <text x="14" y="48" class="font-sub" fill="#B91C1C">Круглосуточный реактивный мониторинг:</text>
      <text x="14" y="66" class="font-body">• Регистрация клиента под надзор: IsUnderStalkerWatch = true</text>
      <text x="14" y="84" class="font-body">• Сохранение таймлайна событий &amp; Мгновенный алерт риск-офицеру</text>
    </g>
  </g>

  <!-- ======================================================================= -->
  <!-- NODE 3: OUTPUT / ACTION (RIGHT)                                         -->
  <!-- ======================================================================= -->
  <g transform="translate(820, 45)" filter="url(#shadow)">
    <rect width="210" height="230" rx="10" fill="#FFFFFF" stroke="#059669" stroke-width="1.5"/>
    <rect width="210" height="32" rx="10" fill="#047857"/>
    <rect y="22" width="210" height="10" fill="#047857"/>
    <text x="14" y="21" class="font-sub" fill="#FFFFFF">Действие RiskTwin</text>
    <text x="14" y="60" class="font-sub" fill="#047857">⚡ Запуск спасения:</text>
    <text x="14" y="80" class="font-body">• Сигнал в Cross-Attention</text>
    <text x="14" y="98" class="font-body">• Расчет PD и дней до DPD</text>
    <text x="14" y="116" class="font-body">• Старт солвера OR-Tools</text>
    <text x="14" y="134" class="font-body">• Синтез 3 сценариев (12 мс)</text>
    <text x="14" y="152" class="font-body">• Push-оффер заемщику</text>

    <rect x="14" y="175" width="182" height="42" rx="6" fill="#ECFDF5"/>
    <text x="22" y="193" class="font-badge" fill="#065F46">Латентность: &lt; 15 ms</text>
    <text x="22" y="207" class="font-body" font-size="10" fill="#047857">Превентивное упреждение</text>
  </g>
</svg>"""

    with open(out_png, "wb") as f:
        f.write(resvg_py.svg_to_bytes(svg))
    print(f"[OK] Cluster diagram generated: {out_png}")

if __name__ == "__main__":
    generate_cluster_diagram()
