import os
from pathlib import Path
import resvg_py

BASE_DIR = Path(__file__).resolve().parent
SVG_DIR = BASE_DIR / "assets" / "svg"
PNG_DIR = BASE_DIR / "assets" / "png"

PNG_DIR.mkdir(parents=True, exist_ok=True)

def get_icon_png_path(name: str, color_hex: str = "#059669", size: int = 128, stroke_width: float = 2.0) -> str:
    """
    Renders Lucide SVG icon to a high-res crisp PNG and caches it.
    Returns the absolute path to the generated PNG file.
    """
    # Normalize color
    clean_color = color_hex.replace("#", "").upper()
    cache_file = PNG_DIR / f"{name}_{clean_color}_{size}.png"
    
    if cache_file.exists():
        return str(cache_file)
    
    svg_file = SVG_DIR / f"{name}.svg"
    if not svg_file.exists():
        raise FileNotFoundError(f"Icon '{name}' not found in {SVG_DIR}")
    
    inner_svg = svg_file.read_text(encoding="utf-8")
    full_svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="#{clean_color}" '
        f'stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">\n'
        f'{inner_svg}\n'
        f'</svg>'
    )
    
    png_bytes = resvg_py.svg_to_bytes(full_svg)
    cache_file.write_bytes(png_bytes)
    return str(cache_file)

if __name__ == "__main__":
    path = get_icon_png_path("shield", "#059669", 128)
    print(f"Generated test icon at: {path}, size: {os.path.getsize(path)} bytes")
