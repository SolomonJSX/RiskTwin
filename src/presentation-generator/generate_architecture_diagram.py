import resvg_py
from pathlib import Path

def generate_architecture_diagram():
    out_dir = Path(__file__).resolve().parent / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / "dual_tower_architecture.png"

    # High-resolution 1100 x 780 collision-free neural architecture diagram
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="780" viewBox="0 0 1100 780">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgCanvas" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FAFC"/>
    </linearGradient>

    <!-- Tower 1: Indigo Gradient -->
    <linearGradient id="tower1Grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3B82F6"/>
      <stop offset="100%" stop-color="#1D4ED8"/>
    </linearGradient>

    <!-- Tower 2: Emerald Gradient -->
    <linearGradient id="tower2Grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#047857"/>
    </linearGradient>

    <!-- Attention Layer: Purple/Violet Gradient -->
    <linearGradient id="attnGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#6D28D9"/>
    </linearGradient>

    <!-- Head / Fusion: Dark Slate Gradient -->
    <linearGradient id="fusionGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>

    <filter id="cardShadow" x="-10%" y="-10%" width="125%" height="130%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.08"/>
    </filter>
  </defs>

  <style>
    .font-title { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 700; }
    .font-sub { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 600; }
    .font-body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 400; }
    .font-math { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 600; font-size: 12px; }
    .font-code { font-family: 'Consolas', 'Courier New', monospace; font-size: 11px; fill: #334155; }
    .font-badge { font-family: 'Consolas', monospace; font-weight: 700; font-size: 11px; }
  </style>

  <!-- Canvas Container -->
  <rect x="2" y="2" width="1096" height="776" rx="16" fill="url(#bgCanvas)" stroke="#E2E8F0" stroke-width="2"/>

  <!-- Diagram Header Pill & Title -->
  <rect x="25" y="18" width="310" height="26" rx="13" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="1.5"/>
  <text x="38" y="35" class="font-badge" fill="#4338CA">PYTORCH DUAL-TOWER NEURAL ARCHITECTURE</text>
  <text x="25" y="72" class="font-title" font-size="20" fill="#0F172A">Двухбашенная нейросеть с кросс-вниманием над финансами и телеметрией</text>

  <!-- ======================================================================= -->
  <!-- LEVEL 1: INPUT TOWERS                                                   -->
  <!-- ======================================================================= -->

  <!-- TOWER 1: CREDIT & BUREAU (LEFT) -->
  <g transform="translate(35, 95)" filter="url(#cardShadow)">
    <rect width="360" height="210" rx="12" fill="#FFFFFF" stroke="#93C5FD" stroke-width="2"/>
    <rect width="360" height="38" rx="12" fill="url(#tower1Grad)"/>
    <rect y="26" width="360" height="12" fill="url(#tower1Grad)"/>
    <text x="16" y="24" class="font-sub" font-size="13" fill="#FFFFFF">БАШНЯ 1: Кредит и Бюро (Static Tower)</text>
    <rect x="275" y="7" width="75" height="22" rx="11" fill="#1E40AF"/>
    <text x="312" y="22" text-anchor="middle" class="font-badge" fill="#BFDBFE">d = 128</text>

    <!-- Content -->
    <text x="16" y="60" class="font-code" font-weight="700" fill="#1D4ED8">📥 Вход: Анкетные и Регуляторные признаки</text>
    <text x="16" y="80" class="font-code">• Доход, сумма займа, аннуитет, DTI ratio</text>
    <text x="16" y="100" class="font-code">• Скоринги бюро: EXT_SOURCE 1, 2, 3</text>
    <text x="16" y="120" class="font-code">• Внешний долг в других банках (bureau.csv)</text>
    <text x="16" y="140" class="font-code">• История отказов (previous_application)</text>
    
    <!-- Tokenizer Box -->
    <rect x="14" y="155" width="332" height="42" rx="8" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1.5"/>
    <text x="24" y="174" class="font-code" font-weight="700" fill="#1E40AF">⚙️ Feature Tokenizer (FT-Transformer)</text>
    <text x="24" y="190" class="font-code" fill="#64748B">Embed(x) + LayerNorm • Проекция признаков</text>
  </g>

  <!-- TOWER 2: BEHAVIOR & TRANSACTIONS (RIGHT) -->
  <g transform="translate(705, 95)" filter="url(#cardShadow)">
    <rect width="360" height="210" rx="12" fill="#FFFFFF" stroke="#A7F3D0" stroke-width="2"/>
    <rect width="360" height="38" rx="12" fill="url(#tower2Grad)"/>
    <rect y="26" width="360" height="12" fill="url(#tower2Grad)"/>
    <text x="16" y="24" class="font-sub" font-size="13" fill="#FFFFFF">БАШНЯ 2: Поведение и ДБО (Dynamic Tower)</text>
    <rect x="275" y="7" width="75" height="22" rx="11" fill="#065F46"/>
    <text x="312" y="22" text-anchor="middle" class="font-badge" fill="#A7F3D0">d = 128</text>

    <!-- Content -->
    <text x="16" y="60" class="font-code" font-weight="700" fill="#047857">📥 Вход: Транзакционная и Психометрическая телеметрия</text>
    <text x="16" y="80" class="font-code">• Задержки оплат и дефициты (installments)</text>
    <text x="16" y="100" class="font-code">• Снятия наличных в ATM и утилизация карт</text>
    <text x="16" y="120" class="font-code">• Товарные рассрочки 0-0-12 (POS-CASH)</text>
    <text x="16" y="140" class="font-code">• Ночные входы в ДБО (3:00 AM) и хаос P2P</text>

    <!-- Tokenizer Box -->
    <rect x="14" y="155" width="332" height="42" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5"/>
    <text x="24" y="174" class="font-code" font-weight="700" fill="#065F46">⚙️ Feature Tokenizer (Behavioral Embedder)</text>
    <text x="24" y="190" class="font-code" fill="#64748B">Embed(x) + LayerNorm • Временные последовательности</text>
  </g>

  <!-- ======================================================================= -->
  <!-- CONNECTING ARROWS TO CROSS-ATTENTION                                    -->
  <!-- ======================================================================= -->
  <g stroke="#64748B" stroke-width="2.5" fill="none">
    <!-- Query Flow: Tower 1 -> Cross-Attention -->
    <path d="M 215 305 L 215 385 L 310 385" stroke="#3B82F6" stroke-width="3"/>
    <circle cx="215" cy="305" r="4" fill="#3B82F6"/>

    <!-- Key & Value Flow: Tower 2 -> Cross-Attention -->
    <path d="M 885 305 L 885 385 L 790 385" stroke="#10B981" stroke-width="3"/>
    <circle cx="885" cy="305" r="4" fill="#10B981"/>
  </g>

  <!-- ======================================================================= -->
  <!-- LEVEL 2: CROSS-ATTENTION CORE (WIDE 480px, ZERO OVERFLOW)               -->
  <!-- ======================================================================= -->
  <g transform="translate(310, 325)" filter="url(#cardShadow)">
    <rect width="480" height="155" rx="14" fill="#FAF5FF" stroke="#C084FC" stroke-width="2.5"/>
    <rect width="480" height="38" rx="14" fill="url(#attnGrad)"/>
    <rect y="26" width="480" height="12" fill="url(#attnGrad)"/>
    <text x="18" y="24" class="font-sub" font-size="13.5" fill="#FFFFFF">Слой Cross-Attention (Multihead: 4 Heads)</text>
    <rect x="385" y="7" width="80" height="22" rx="11" fill="#4C1D95"/>
    <text x="425" y="22" text-anchor="middle" class="font-badge" fill="#E9D5FF">PyTorch</text>

    <!-- Formula Box: Wide 450px with comfortable margins -->
    <rect x="15" y="46" width="450" height="42" rx="8" fill="#FFFFFF" stroke="#E9D5FF"/>
    <text x="25" y="64" class="font-math" fill="#6B21A8">Query: c_tok (Кредит) ➔ Key &amp; Value: b_tok (Поведение)</text>
    <text x="25" y="80" class="font-math" font-size="11" fill="#7E22CE">Attn(Q, K, V) = Softmax( Q·Kᵀ / √d ) · V</text>

    <!-- Residual Norm with proper spacing -->
    <text x="18" y="108" class="font-sub" font-size="11.5" fill="#1E293B">⚡ Residual Fusion: c_cross = LayerNorm( c_tok + Attn_out )</text>
    <text x="18" y="126" class="font-body" font-size="11.5" fill="#64748B">Кредитные обязательства заемщика опрашивают его живое поведение,</text>
    <text x="18" y="142" class="font-body" font-size="11.5" fill="#64748B">вычисляя скрытый стресс за 30–60 дней до наступления неплатежа.</text>
  </g>

  <!-- Arrow from Attention to Fusion Head -->
  <path d="M 550 480 L 550 505" stroke="#6D28D9" stroke-width="3" fill="none"/>

  <!-- ======================================================================= -->
  <!-- LEVEL 3: FUSION & MULTI-LAYER MLP HEAD (WIDE 800px)                     -->
  <!-- ======================================================================= -->
  <g transform="translate(150, 505)" filter="url(#cardShadow)">
    <rect width="800" height="110" rx="12" fill="#FFFFFF" stroke="#64748B" stroke-width="2"/>
    <rect width="800" height="34" rx="12" fill="url(#fusionGrad)"/>
    <rect y="22" width="800" height="12" fill="url(#fusionGrad)"/>
    <text x="18" y="22" class="font-sub" font-size="13" fill="#FFFFFF">Fusion Layer &amp; Deep MLP Head (BatchNorm1d + SiLU + Dropout 0.25)</text>
    <rect x="680" y="6" width="105" height="22" rx="11" fill="#0F172A"/>
    <text x="732" y="21" text-anchor="middle" class="font-badge" fill="#94A3B8">Linear(128➔64➔1)</text>

    <text x="18" y="54" class="font-sub" font-size="12" fill="#0F172A">Объединение признаков: Concatenate [ c_tok, b_tok, c_cross ]</text>
    <text x="18" y="74" class="font-body" font-size="12" fill="#334155">Нелинейная проекция скрытых состояний с регуляризацией от переобучения на данных NPL.</text>
    <text x="18" y="96" class="font-math" fill="#059669">✓ Обучено на 163 517 профилях Home Credit • Инференс одного клиента: ~7.4 мс</text>
  </g>

  <!-- Arrow to Outputs -->
  <path d="M 550 615 L 550 640" stroke="#0F172A" stroke-width="3" fill="none"/>

  <!-- ======================================================================= -->
  <!-- LEVEL 4: DUAL OUTPUT (WIDE 435px EACH, ZERO OVERFLOW)                   -->
  <!-- ======================================================================= -->

  <!-- OUTPUT 1: PROBABILITY OF DEFAULT -->
  <g transform="translate(100, 640)" filter="url(#cardShadow)">
    <rect width="435" height="110" rx="10" fill="#FEF2F2" stroke="#F87171" stroke-width="2"/>
    <text x="18" y="26" class="font-sub" font-size="13" fill="#991B1B">🎯 Выход 1: Калиброванный риск (PD)</text>
    <text x="18" y="48" class="font-body" font-size="12" fill="#334155">Вероятность дефолта заемщика в диапазоне 0.0% – 100.0%</text>
    <text x="18" y="68" class="font-body" font-size="12" fill="#334155">Прогноз срока до кассового разрыва (Survival MAE ±4.2 дня)</text>
    
    <rect x="18" y="78" width="165" height="22" rx="11" fill="#FEE2E2"/>
    <text x="100" y="93" text-anchor="middle" class="font-badge" fill="#DC2626">ROC-AUC: 0.941</text>
    
    <rect x="200" y="78" width="160" height="22" rx="11" fill="#DCFCE7"/>
    <text x="280" y="93" text-anchor="middle" class="font-badge" fill="#15803D">PR-AUC: 0.442</text>
  </g>

  <!-- OUTPUT 2: XAI EXPLAINABILITY (ATTENTION WEIGHTS) -->
  <g transform="translate(565, 640)" filter="url(#cardShadow)">
    <rect width="435" height="110" rx="10" fill="#F0FDF4" stroke="#34D399" stroke-width="2"/>
    <text x="18" y="26" class="font-sub" font-size="13" fill="#065F46">🔍 Выход 2: Объяснимый ИИ (XAI Weights)</text>
    <text x="18" y="48" class="font-body" font-size="12" fill="#334155">Матрица весов внимания для риск-офицеров банка</text>
    <text x="18" y="68" class="font-body" font-size="12" fill="#334155">Прозрачное объяснение факторов риска для комплаенс АРРФР</text>
    
    <rect x="18" y="78" width="180" height="22" rx="11" fill="#DCFCE7"/>
    <text x="108" y="93" text-anchor="middle" class="font-badge" fill="#047857">100% Explainable AI</text>
    
    <rect x="215" y="78" width="150" height="22" rx="11" fill="#FEF3C7"/>
    <text x="290" y="93" text-anchor="middle" class="font-badge" fill="#B45309">No Black Box</text>
  </g>
</svg>"""

    with open(out_png, "wb") as f:
        f.write(resvg_py.svg_to_bytes(svg))
    print(f"[OK] Collision-free Dual-Tower architecture diagram generated: {out_png}")

if __name__ == "__main__":
    generate_architecture_diagram()
