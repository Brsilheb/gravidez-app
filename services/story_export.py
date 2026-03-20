from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


W, H = 1080, 1920

# Cores (pode ajustar depois conforme tema)
THEMES = {
    "rose": {
        "bg_top": (255, 255, 255),
        "bg_bottom": (243, 230, 223),
        "text": (74, 74, 74),
        "muted": (109, 109, 109),
        "accent": (232, 207, 197),
    },
    "bege": {
        "bg_top": (255, 255, 255),
        "bg_bottom": (247, 239, 229),
        "text": (74, 74, 74),
        "muted": (109, 109, 109),
        "accent": (220, 210, 190),
    },
    "azul": {
        "bg_top": (255, 255, 255),
        "bg_bottom": (227, 239, 247),
        "text": (74, 74, 74),
        "muted": (109, 109, 109),
        "accent": (200, 225, 240),
    },
}


def generate_story_png(
    week: int,
    baby_size: str,
    message: str,
    baby_name: str = "",
    mae_name: str = "",
    theme: str = "rose",
) -> bytes:
    """
    Gera uma imagem PNG (1080x1920) pronta para Story.
    Retorna bytes do PNG para usar no st.download_button.
    """

    theme = theme if theme in THEMES else "rose"
    colors = THEMES[theme]

    img = Image.new("RGB", (W, H), colors["bg_top"])
    draw = ImageDraw.Draw(img)

    # Gradient simples
    _vertical_gradient(img, colors["bg_top"], colors["bg_bottom"])

    # Fontes: tentamos carregar uma fonte padrão; se não, usa fallback do PIL
    title_font = _load_font(72)
    subtitle_font = _load_font(48)
    body_font = _load_font(44)
    small_font = _load_font(34)

    # Margens / layout
    pad_x = 90
    y = 170

    # Header
    header = f"Semana {week} 🤍"
    if baby_name.strip():
        header = f"Semana {week} de {baby_name.strip()} 🤍"

    draw.text((pad_x, y), header, fill=colors["text"], font=title_font)
    y += 120

    # Linha/acento
    draw.rounded_rectangle((pad_x, y, W - pad_x, y + 10), radius=6, fill=colors["accent"])
    y += 60

    # Baby size
    draw.text((pad_x, y), baby_size, fill=colors["muted"], font=subtitle_font)
    y += 100

    # Mensagem principal (quebra em linhas)
    message = (message or "").strip()
    lines = _wrap_text(draw, message, body_font, max_width=W - 2 * pad_x)
    for line in lines[:7]:  # limite para não estourar
        draw.text((pad_x, y), line, fill=colors["text"], font=body_font)
        y += 62

    # Rodapé discreto (opcional)
    footer_y = H - 220
    footer_left = pad_x

    if mae_name.strip():
        draw.text((footer_left, footer_y), mae_name.strip(), fill=colors["muted"], font=small_font)
        footer_y += 45

    stamp = datetime.now().strftime("%d/%m/%Y")
    draw.text((footer_left, footer_y), stamp, fill=colors["muted"], font=small_font)

    # Exporta para bytes
    bio = BytesIO()
    img.save(bio, format="PNG", optimize=True)
    return bio.getvalue()


def _vertical_gradient(img: Image.Image, top_rgb, bottom_rgb):
    """Aplica gradiente vertical simples."""
    w, h = img.size
    for y in range(h):
        t = y / (h - 1)
        r = int(top_rgb[0] * (1 - t) + bottom_rgb[0] * t)
        g = int(top_rgb[1] * (1 - t) + bottom_rgb[1] * t)
        b = int(top_rgb[2] * (1 - t) + bottom_rgb[2] * t)
        ImageDraw.Draw(img).line([(0, y), (w, y)], fill=(r, g, b))


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int):
    """Quebra texto em linhas para caber no max_width."""
    words = text.split()
    lines = []
    current = ""

    for w in words:
        test = (current + " " + w).strip()
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def _load_font(size: int):
    """
    Tenta carregar fonte TrueType comum; fallback para fonte padrão do PIL.
    No Streamlit Cloud, fontes do sistema podem variar.
    """
    candidates = [
        "DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            continue
    return ImageFont.load_default()
