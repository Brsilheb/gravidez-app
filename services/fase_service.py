import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "fases_semanais.json"

def get_fase_content(week: int) -> dict:
    """
    Retorna um dict com:
    - emocional
    - curiosidade
    Faz fallback para a semana mais próxima menor ou igual.
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}

    weeks = sorted(int(w) for w in data.keys())
    selected = weeks[0]
    for w in weeks:
        if week >= w:
            selected = w

    return data.get(str(selected), {})
