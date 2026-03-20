from io import BytesIO
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "assets" / "templates"  # você vai usar depois

THEMES = {
    "rose": {"bg_top": (255, 255, 255), "bg_bottom": (243, 230, 223), "text": (50, 50, 50), "muted": (110, 110, 110), "accent": (232, 207, 197)},
    "bege": {"bg_top": (255, 255, 255), "bg_bottom": (247, 239, 229), "text": (50, 50, 50), "muted": (110, 110, 110), "accent": (220, 210, 190)},
    "azul": {"bg_top": (255, 255, 255), "bg_bottom": (227, 239, 247), "text": (50, 50, 50), "muted": (110, 110, 110), "accent": (200, 225, 240)}
}

def generate_story_png(week: int, baby_size: str, message: str, baby_name: str = "", mae_name: str = "", theme: str = "rose") -> bytes:
    theme = theme if theme in THEMES else "rose"
    c = THEMES[theme]

    # 1) tenta carregar template por semana (gancho futuro)
    img = _try_load_template(week, theme)
    if img is None:
        img = Image.new("RGB", (W, H), c["bg_top"])
        _vertical_gradient(img, c["bg_top"], c["bg_bottom"])

    draw = ImageDraw.Draw(img)

    # Fontes maiores (melhor no iPhone)
    title_font = _load_font(92, bold=True)
    subtitle_font = _load_font(56, bold=False)
    body_font = _load_font(54, bold=False)
    small_font = _load_font(40, bold=False)

    pad_x = 90
    y = 140

    # Cabeçalho
    header = f"Semana {week} 🤍"
    if baby_name.strip():
        header = f"Semana {week} de {baby_name.strip()} 🤍"
    draw.text((pad_x, y), header, fill=c["text"], font=title_font)
    y += 120

    # faixa/acento
    draw.rounded_rectangle((pad_x, y, W - pad_x, y + 12), radius=8, fill=c["accent"])
    y += 55

    # 2) área de imagem/hero (mesmo sem template)
    hero_y1 = y
    hero_y2 = y + 460
    draw.rounded_rectangle((pad_x, hero_y1, W - pad_x, hero_y2), radius=36, outline=c["accent"], width=6)
    # texto central leve (placeholder)
    hero_text = "✨"
    tw = draw.textlength(hero_text, font=title_font)
    draw.text(((W - tw) / 2, hero_y1 + 160), hero_text, fill=c["accent"], font=title_font)
    y = hero_y2 + 60

    # Tamanho do bebê
    draw.text((pad_x, y), (baby_size or "").strip(), fill=c["muted"], font=subtitle_font)
    y += 90

    # Mensagem (quebra em linhas)
    lines = _wrap_text(draw, (message or "").strip(), body_font, max_width=W - 2 * pad_x)
    line_h = 70
    for line in lines[:6]:
        draw.text((pad_x, y), line, fill=c["text"], font=body_font)
        y += line_h

    # Rodapé
    footer_y = H - 190
    stamp = datetime.now().strftime("%d/%m/%Y")
    left = pad_x

    if mae_name.strip():
        draw.text((left, footer_y - 55), mae_name.strip(), fill=c["muted"], font=small_font)

    draw.text((left, footer_y), stamp, fill=c["muted"], font=small_font)

    # export
    bio = BytesIO()
    img.save(bio, format="PNG", optimize=True)
    return bio.getvalue()

def _try_load_template(week: int, theme: str):
    """
    Gancho futuro:
    - assets/templates/{theme}/week_{week}.png
    - assets/templates/week_{week}.png
    """
    candidates = [
        TEMPLATE_DIR / theme / f"week_{week}.png",
        TEMPLATE_DIR / f"week_{week}.png",
        TEMPLATE_DIR / theme / "default.png",
        TEMPLATE_DIR / "default.png",
    ]
    for p in candidates:
        try:
            if p.exists():
                im = Image.open(p).convert("RGB")
                return im.resize((W, H), Image.LANCZOS)
        except Exception:
            continue
    return None

def _vertical_gradient(img: Image.Image, top_rgb, bottom_rgb):
    w, h = img.size
    d = ImageDraw.Draw(img)
    for yy in range(h):
        t = yy / (h - 1)
        r = int(top_rgb[0] * (1 - t) + bottom_rgb[0] * t)
        g = int(top_rgb[1] * (1 - t) + bottom_rgb[1] * t)
        b = int(top_rgb[2] * (1 - t) + bottom_rgb[2] * t)
        d.line([(0, yy), (w, yy)], fill=(r, g, b))

def _wrap_text(draw, text: str, font, max_width: int):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def _load_font(size: int, bold: bool = False):
    # DejaVu geralmente existe no Streamlit Cloud
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size=size)
        except Exception:
            continue
    return ImageFont.load_default()
