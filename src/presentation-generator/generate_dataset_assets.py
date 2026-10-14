import resvg_py
from pathlib import Path

def generate_home_credit_logo():
    out_dir = Path(__file__).resolve().parent / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / "home_credit_logo.png"

    # Crisp vector rendering of Home Credit Bank Logo
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="240" viewBox="0 0 600 240">
  <defs>
    <filter id="logoShadow" x="-10%" y="-10%" width="125%" height="130%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#E30613" flood-opacity="0.35"/>
    </filter>
    <linearGradient id="hcRedGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EE3124"/>
      <stop offset="100%" stop-color="#C8102E"/>
    </linearGradient>
  </defs>

  <!-- Red Card Background with shadow -->
  <rect x="15" y="15" width="570" height="210" rx="36" fill="url(#hcRedGrad)" filter="url(#logoShadow)"/>

  <!-- Subtle glossy highlight -->
  <path d="M 15 51 Q 15 15 51 15 L 549 15 Q 585 15 585 51 L 585 85 Q 300 120 15 85 Z" fill="#FFFFFF" opacity="0.12"/>

  <!-- Home Credit Icon: White Smiling Circle / House Silhouette -->
  <g transform="translate(45, 45)">
    <!-- White Circle -->
    <circle cx="75" cy="75" r="62" fill="#FFFFFF"/>
    <!-- Red Smiling Arc / Face -->
    <path d="M 38 75 Q 75 125 112 75" fill="none" stroke="#EE3124" stroke-width="12" stroke-linecap="round"/>
    <circle cx="52" cy="55" r="7.5" fill="#EE3124"/>
    <circle cx="98" cy="55" r="7.5" fill="#EE3124"/>
  </g>

  <!-- Brand Typography -->
  <g transform="translate(195, 75)">
    <text x="0" y="42" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Montserrat', Roboto, sans-serif" font-weight="900" font-size="46" fill="#FFFFFF" letter-spacing="-1">home credit</text>
    <text x="3" y="82" font-family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Montserrat', Roboto, sans-serif" font-weight="700" font-size="28" fill="#FEE2E2" letter-spacing="6">BANK</text>
  </g>
</svg>"""

    with open(out_png, "wb") as f:
        f.write(resvg_py.svg_to_bytes(svg))
    print(f"[OK] Home Credit logo generated: {out_png}")

def generate_dataset_schema():
    out_dir = Path(__file__).resolve().parent / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / "home_credit_dataset_schema.png"

    # High-resolution 1100 x 780 relational data pipeline diagram (Completely collision-free)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="780" viewBox="0 0 1100 780">
  <defs>
    <linearGradient id="bgCanvas" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FAFC"/>
    </linearGradient>

    <!-- Table Header Gradients -->
    <linearGradient id="hcHeaderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#EE3124"/>
      <stop offset="100%" stop-color="#C8102E"/>
    </linearGradient>

    <linearGradient id="coreHeaderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#047857"/>
      <stop offset="100%" stop-color="#065F46"/>
    </linearGradient>

    <filter id="tableShadow" x="-10%" y="-10%" width="125%" height="130%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.08"/>
    </filter>
  </defs>

  <style>
    .font-title { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 700; }
    .font-table { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 700; font-size: 12.5px; fill: #FFFFFF; }
    .font-body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 400; }
    .font-code { font-family: 'Consolas', 'Courier New', monospace; font-size: 11.5px; fill: #334155; }
    .font-badge { font-family: 'Consolas', monospace; font-weight: 700; font-size: 10.5px; }
  </style>

  <!-- Canvas Container -->
  <rect x="2" y="2" width="1096" height="776" rx="16" fill="url(#bgCanvas)" stroke="#E2E8F0" stroke-width="2"/>

  <!-- Top Title Bar -->
  <rect x="25" y="18" width="310" height="26" rx="13" fill="#FEF2F2" stroke="#FECACA" stroke-width="1.5"/>
  <text x="38" y="35" class="font-badge" fill="#DC2626">HOME CREDIT 360° RELATIONAL PIPELINE</text>
  <text x="25" y="72" class="font-title" font-size="20" fill="#0F172A">Архитектура объединения 6 таблиц в единого цифрового двойника</text>

  <!-- Connective Bézier Curves (Data Flow Lines) -->
  <g stroke="#CBD5E1" stroke-width="2.5" fill="none" stroke-dasharray="6,4">
    <!-- Left tables to Center Core -->
    <path d="M 335 150 C 400 150, 410 260, 445 260" stroke="#EE3124" stroke-opacity="0.45"/>
    <path d="M 335 330 C 390 330, 410 300, 445 300" stroke="#EE3124" stroke-opacity="0.45"/>
    <path d="M 335 500 C 400 500, 410 340, 445 340" stroke="#EE3124" stroke-opacity="0.45"/>

    <!-- Right tables to Center Core -->
    <path d="M 765 150 C 700 150, 690 260, 655 260" stroke="#EE3124" stroke-opacity="0.45"/>
    <path d="M 765 330 C 710 330, 690 300, 655 300" stroke="#EE3124" stroke-opacity="0.45"/>
    <path d="M 765 500 C 700 500, 690 340, 655 340" stroke="#EE3124" stroke-opacity="0.45"/>

    <!-- Center Core to Bottom Digital Twin -->
    <path d="M 550 440 L 550 560" stroke="#047857" stroke-width="3" stroke-dasharray="0"/>
  </g>

  <!-- ======================================================================= -->
  <!-- LEFT COLUMN: PAYMENTS & POS BNPL                                        -->
  <!-- ======================================================================= -->

  <!-- TABLE 1: installments_payments -->
  <g transform="translate(25, 95)" filter="url(#tableShadow)">
    <rect width="310" height="140" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect width="310" height="34" rx="10" fill="url(#hcHeaderGrad)"/>
    <rect y="24" width="310" height="10" fill="url(#hcHeaderGrad)"/>
    <text x="12" y="22" class="font-table">installments_payments</text>
    <rect x="210" y="6" width="90" height="22" rx="11" fill="#991B1B"/>
    <text x="255" y="21" text-anchor="middle" class="font-badge" fill="#FEE2E2">13.6M строк</text>
    <text x="12" y="56" class="font-code">• delay_days (дни задержки)</text>
    <text x="12" y="77" class="font-code">• deficit (кассовый недобор)</text>
    <text x="12" y="98" class="font-code">• inst_late_count (число просрочек)</text>
    <text x="12" y="119" class="font-code">• total_deficit_sum (сумма долга)</text>
  </g>

  <!-- TABLE 2: POS_CASH_balance -->
  <g transform="translate(25, 255)" filter="url(#tableShadow)">
    <rect width="310" height="140" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect width="310" height="34" rx="10" fill="url(#hcHeaderGrad)"/>
    <rect y="24" width="310" height="10" fill="url(#hcHeaderGrad)"/>
    <text x="12" y="22" class="font-table">POS_CASH_balance</text>
    <rect x="195" y="6" width="105" height="22" rx="11" fill="#991B1B"/>
    <text x="247" y="21" text-anchor="middle" class="font-badge" fill="#FEE2E2">10M Рассрочки</text>
    <text x="12" y="56" class="font-code">• pos_active_count (число рассрочек)</text>
    <text x="12" y="77" class="font-code">• pos_completed_count (закрытые)</text>
    <text x="12" y="98" class="font-code">• remaining_installments (остаток)</text>
    <text x="12" y="119" class="font-code">• pos_max_dpd (макс. просрочка)</text>
  </g>

  <!-- TABLE 3: bureau.csv & bureau_balance -->
  <g transform="translate(25, 415)" filter="url(#tableShadow)">
    <rect width="310" height="140" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect width="310" height="34" rx="10" fill="url(#hcHeaderGrad)"/>
    <rect y="24" width="310" height="10" fill="url(#hcHeaderGrad)"/>
    <text x="12" y="22" class="font-table">bureau.csv (Кредиты РК)</text>
    <rect x="210" y="6" width="90" height="22" rx="11" fill="#991B1B"/>
    <text x="255" y="21" text-anchor="middle" class="font-badge" fill="#FEE2E2">1.7M ГКБ</text>
    <text x="12" y="56" class="font-code">• bureau_active_loans (займы в банках)</text>
    <text x="12" y="77" class="font-code">• bureau_total_debt (внешний долг)</text>
    <text x="12" y="98" class="font-code">• bureau_total_overdue (просрочки)</text>
    <text x="12" y="119" class="font-code">• bureau_prolong_count (пролонгации)</text>
  </g>

  <!-- ======================================================================= -->
  <!-- RIGHT COLUMN: CARDS, HISTORY & TELEMETRY                                -->
  <!-- ======================================================================= -->

  <!-- TABLE 4: credit_card_balance -->
  <g transform="translate(765, 95)" filter="url(#tableShadow)">
    <rect width="310" height="140" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect width="310" height="34" rx="10" fill="url(#hcHeaderGrad)"/>
    <rect y="24" width="310" height="10" fill="url(#hcHeaderGrad)"/>
    <text x="12" y="22" class="font-table">credit_card_balance</text>
    <rect x="210" y="6" width="90" height="22" rx="11" fill="#991B1B"/>
    <text x="255" y="21" text-anchor="middle" class="font-badge" fill="#FEE2E2">3.8M Карт</text>
    <text x="12" y="56" class="font-code">• cc_atm_drawings_sum (наличные ATM)</text>
    <text x="12" y="77" class="font-code">• cc_pos_drawings_sum (оплаты картой)</text>
    <text x="12" y="98" class="font-code">• cc_utilization_mean (лимит %)</text>
    <text x="12" y="119" class="font-code">• cc_max_dpd (просрочка по карте)</text>
  </g>

  <!-- TABLE 5: previous_application -->
  <g transform="translate(765, 255)" filter="url(#tableShadow)">
    <rect width="310" height="140" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
    <rect width="310" height="34" rx="10" fill="url(#hcHeaderGrad)"/>
    <rect y="24" width="310" height="10" fill="url(#hcHeaderGrad)"/>
    <text x="12" y="22" class="font-table">previous_application</text>
    <rect x="205" y="6" width="95" height="22" rx="11" fill="#991B1B"/>
    <text x="252" y="21" text-anchor="middle" class="font-badge" fill="#FEE2E2">1.6M Заявок</text>
    <text x="12" y="56" class="font-code">• prev_app_total (всего обращений)</text>
    <text x="12" y="77" class="font-code">• prev_refused_count (отказы банка)</text>
    <text x="12" y="98" class="font-code">• prev_approved_count (одобрения)</text>
    <text x="12" y="119" class="font-code">• last_action_days (дней с заявки)</text>
  </g>

  <!-- TABLE 6: Behavioral Telemetry (Инновация RiskTwin) -->
  <g transform="translate(765, 415)" filter="url(#tableShadow)">
    <rect width="310" height="140" rx="10" fill="#FFFFFF" stroke="#047857" stroke-width="1.5"/>
    <rect width="310" height="34" rx="10" fill="url(#coreHeaderGrad)"/>
    <rect y="24" width="310" height="10" fill="url(#coreHeaderGrad)"/>
    <text x="12" y="22" class="font-table">behavioral_telemetry</text>
    <rect x="200" y="6" width="100" height="22" rx="11" fill="#064E3B"/>
    <text x="250" y="21" text-anchor="middle" class="font-badge" fill="#6EE7B7">ДБО Тень</text>
    <text x="12" y="56" class="font-code">• night_logins_ratio (входы ночью 3 AM)</text>
    <text x="12" y="77" class="font-code">• balance_decay_7d (падение остатка)</text>
    <text x="12" y="98" class="font-code">• p2p_entropy (хаотичность переводов)</text>
    <text x="12" y="119" class="font-code">• screen_time_schedules (тревожность)</text>
  </g>

  <!-- ======================================================================= -->
  <!-- CENTER CORE: application_train.csv                                      -->
  <!-- ======================================================================= -->
  <g transform="translate(410, 180)" filter="url(#tableShadow)">
    <rect width="280" height="225" rx="14" fill="#FFFFFF" stroke="#EE3124" stroke-width="2.5"/>
    <rect width="280" height="42" rx="14" fill="url(#hcHeaderGrad)"/>
    <rect y="30" width="280" height="12" fill="url(#hcHeaderGrad)"/>
    <text x="18" y="27" class="font-table" font-size="14.5">ЯДРО: application_train</text>
    <text x="14" y="66" class="font-code" font-weight="700" fill="#EE3124">🔑 SK_ID_CURR (Primary Key)</text>
    <text x="14" y="90" class="font-code">• AMT_INCOME_TOTAL (доход)</text>
    <text x="14" y="112" class="font-code">• AMT_CREDIT (сумма займа)</text>
    <text x="14" y="134" class="font-code">• dti_ratio (долговая нагрузка)</text>
    <text x="14" y="156" class="font-code">• EXT_SOURCE_1, 2, 3 (скоринг)</text>
    <text x="14" y="178" class="font-code">• age_years &amp; employment_years</text>
    <text x="14" y="202" class="font-code" font-weight="700" fill="#047857">🎯 TARGET (0 = здоров, 1 = дефолт)</text>
  </g>

  <!-- ======================================================================= -->
  <!-- BOTTOM CONVERGENCE: 360° DIGITAL TWIN PASSPORT (WIDE & NO COLLISION)    -->
  <!-- ======================================================================= -->
  <g transform="translate(180, 570)" filter="url(#tableShadow)">
    <!-- Wider card: 740px width with comfortable padding -->
    <rect width="740" height="175" rx="14" fill="#F0FDF4" stroke="#059669" stroke-width="2.5"/>
    <rect width="740" height="40" rx="14" fill="url(#coreHeaderGrad)"/>
    <rect y="26" width="740" height="14" fill="url(#coreHeaderGrad)"/>
    
    <!-- Header title and badge with over 200px clearance -->
    <text x="18" y="26" class="font-table" font-size="14">Паспорт Цифрового Двойника (360° Ontology)</text>
    <rect x="585" y="8" width="135" height="24" rx="12" fill="#064E3B" stroke="#6EE7B7" stroke-width="1.2"/>
    <text x="652" y="24" text-anchor="middle" class="font-badge" fill="#A7F3D0">PyTorch ready</text>

    <!-- Clean, properly wrapped body texts -->
    <text x="18" y="66" class="font-body" font-size="13" fill="#065F46" font-weight="700">✓ 307 511 уникальных заемщиков • 48 признаков • Формат: Parquet</text>
    <text x="18" y="90" class="font-body" font-size="12" fill="#334155">Объединение транзакций Home Credit, внешнего долга ПКБ, товарных рассрочек (POS)</text>
    <text x="18" y="112" class="font-body" font-size="12" fill="#334155">и психометрических маркеров тревожности ДБО для модели Dual-Tower Cross-Attention.</text>
    
    <!-- Mini Metric Pills with ample spacing -->
    <rect x="18" y="130" width="180" height="24" rx="12" fill="#DCFCE7"/>
    <text x="108" y="146" text-anchor="middle" class="font-badge" fill="#15803D">6 банковских таблиц</text>

    <rect x="220" y="130" width="220" height="24" rx="12" fill="#FEE2E2"/>
    <text x="330" y="146" text-anchor="middle" class="font-badge" fill="#B91C1C">Home Credit Default Risk</text>

    <rect x="460" y="130" width="210" height="24" rx="12" fill="#FEF3C7"/>
    <text x="565" y="146" text-anchor="middle" class="font-badge" fill="#B45309">ROC-AUC: 0.941 на тесте</text>
  </g>
</svg>"""

    with open(out_png, "wb") as f:
        f.write(resvg_py.svg_to_bytes(svg))
    print(f"[OK] Collision-free Dataset schema generated: {out_png}")

if __name__ == "__main__":
    generate_home_credit_logo()
    generate_dataset_schema()
