import resvg_py
from pathlib import Path

def generate_risktwin_logo():
    out_dir = Path(__file__).resolve().parent / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / "risktwin_logo_hero.png"

    # 1024x1024 high-resolution vector emblem
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <defs>
    <!-- Background Gradient for card -->
    <linearGradient id="cardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="50%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#F1F5F9"/>
    </linearGradient>

    <!-- Emerald gradients (Halyk-inspired deep green to tech mint) -->
    <linearGradient id="emeraldDark" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#064E3B"/>
      <stop offset="100%" stop-color="#047857"/>
    </linearGradient>

    <linearGradient id="emeraldMain" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#059669"/>
      <stop offset="100%" stop-color="#10B981"/>
    </linearGradient>

    <linearGradient id="tealAccent" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0D9488"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>

    <linearGradient id="goldAccent" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#FBBF24"/>
    </linearGradient>

    <!-- Drop Shadows for depth -->
    <filter id="rhombusShadow" x="-20%" y="-20%" width="140%" height="140%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="#064E3B" flood-opacity="0.22"/>
    </filter>

    <filter id="innerGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.15"/>
    </filter>
  </defs>

  <style>
    .brand-font { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 800; }
    .sub-font { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; font-weight: 500; }
  </style>

  <!-- Container Base -->
  <rect x="24" y="24" width="976" height="976" rx="48" fill="url(#cardBg)" stroke="#E2E8F0" stroke-width="3"/>

  <!-- Subtle Concentric Geometry (Ornaments / Tech Radar Lines) -->
  <circle cx="512" cy="450" r="340" fill="none" stroke="#E2E8F0" stroke-width="1.5" stroke-dasharray="8,6"/>
  <circle cx="512" cy="450" r="260" fill="none" stroke="#E2E8F0" stroke-width="1.5"/>
  <circle cx="512" cy="450" r="180" fill="none" stroke="#E2E8F0" stroke-width="1.5" stroke-dasharray="4,4"/>

  <!-- ======================================================================= -->
  <!-- MAIN RHOMBUS / DIAMOND LOGO COMPOSITION                                 -->
  <!-- ======================================================================= -->
  <g filter="url(#rhombusShadow)">
    <!-- 1. Outer Primary Emerald Rhombus -->
    <!-- Center: 512, 450. Top: 512, 170. Right: 792, 450. Bottom: 512, 730. Left: 232, 450 -->
    <polygon points="512,160 792,440 512,720 232,440" fill="url(#emeraldDark)" stroke="#A7F3D0" stroke-width="4"/>

    <!-- 2. Second Interlocking Twin Rhombus (The Digital Twin Offset) -->
    <!-- Creates the dimensional "Twin" layering -->
    <polygon points="512,205 747,440 512,675 277,440" fill="url(#emeraldMain)" opacity="0.95"/>

    <!-- 3. Dynamic Stepped / Zigzag Chevrons (Halyk-inspired Geometric Ornament) -->
    <!-- Left Stepped Wing (Real Financial Stream) -->
    <path d="M 512 250 L 400 362 L 440 402 L 360 482 L 400 522 L 512 634 L 512 584 L 440 512 L 480 472 L 400 392 L 440 352 L 512 280 Z" 
          fill="#FFFFFF" opacity="0.92" filter="url(#innerGlow)"/>

    <!-- Right Stepped Wing (Digital Behavioral Stream - Teal Accent) -->
    <path d="M 512 250 L 624 362 L 584 402 L 664 482 L 624 522 L 512 634 L 512 584 L 584 512 L 544 472 L 624 392 L 584 352 L 512 280 Z" 
          fill="url(#tealAccent)" opacity="0.95" filter="url(#innerGlow)"/>

    <!-- 4. Central Diamond Core (The Nexus / Synchronized Twin Node) -->
    <!-- Diamond at 512, 440 -->
    <polygon points="512,380 572,440 512,500 452,440" fill="#FFFFFF" stroke="#059669" stroke-width="4"/>
    <polygon points="512,398 554,440 512,482 470,440" fill="url(#goldAccent)"/>
    <polygon points="512,416 536,440 512,464 488,440" fill="#FFFFFF"/>

    <!-- 5. Top & Bottom Apex Tech Pointers -->
    <polygon points="512,125 528,150 496,150" fill="#10B981"/>
    <polygon points="512,755 528,730 496,730" fill="#0D9488"/>
    <polygon points="197,440 222,424 222,456" fill="#10B981"/>
    <polygon points="827,440 802,424 802,456" fill="#0D9488"/>
  </g>

  <!-- ======================================================================= -->
  <!-- TYPOGRAPHY SECTION                                                      -->
  <!-- ======================================================================= -->
  <!-- Brand Name -->
  <text x="512" y="820" class="brand-font" font-size="64" fill="#0F172A" text-anchor="middle" letter-spacing="-1">
    Risk<tspan fill="#059669">Twin</tspan>
  </text>

  <!-- Subtitle Tagline -->
  <text x="512" y="865" class="sub-font" font-size="20" fill="#059669" text-anchor="middle" letter-spacing="3">
    DIGITAL TWIN OF CREDIT RISK
  </text>
  <text x="512" y="900" class="sub-font" font-size="16" fill="#64748B" text-anchor="middle">
    Превентивная платформа управления финансовыми рисками
  </text>
</svg>"""

    png_bytes = resvg_py.svg_to_bytes(svg)
    out_png.write_bytes(png_bytes)
    print(f"[Logo Generator] Successfully created high-res logo: {out_png}")
    return out_png

if __name__ == "__main__":
    generate_risktwin_logo()
