import json
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
USER_DATA_DIR = BASE_DIR / "user_data"

CONFIG_FILE = USER_DATA_DIR / "config.json"
COMPRAS_FILE = USER_DATA_DIR / "compras.csv"
DIARIO_FILE = USER_DATA_DIR / "diario.csv"
TIMELINE_FILE = USER_DATA_DIR / "timeline.csv"

DEFAULT_CONFIG = {
    "nome_bebe": "",
    "nome_mae": "Mamãe",
    "metodo_data": "DPP",  # "DPP" ou "DUM"
    "data_prevista_parto": "",
    "data_ultima_menstruacao": "",
    "tema_visual": "rose",
    "modo_som": False,
}

SCHEMAS = {
    "compras": ["item", "categoria", "valor", "status", "data"],
    "diario": ["data", "emocao", "titulo", "texto", "tipo"],
    "timeline": ["data", "titulo", "descricao", "categoria"],
}


def ensure_data_files():
    USER_DATA_DIR.mkdir(exist_ok=True)

    # Config
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
    else:
        # garante que config tenha todas as chaves novas
        try:
            cfg = load_config()
            merged = DEFAULT_CONFIG.copy()
            merged.update(cfg or {})
            save_config(merged)
        except Exception:
            save_config(DEFAULT_CONFIG)

    # CSVs
    _ensure_csv(COMPRAS_FILE, SCHEMAS["compras"])
    _ensure_csv(DIARIO_FILE, SCHEMAS["diario"])
    _ensure_csv(TIMELINE_FILE, SCHEMAS["timeline"])


def _ensure_csv(path: Path, columns: list[str]):
    """
    Garante que o CSV exista e tenha cabeçalho.
    Em Streamlit Cloud, arquivos podem ficar vazios / sem header após restart.
    """
    if not path.exists():
        pd.DataFrame(columns=columns).to_csv(path, index=False)
        return

    try:
        # Se o arquivo existir mas estiver vazio (0 bytes), recria com header
        if path.stat().st_size == 0:
            pd.DataFrame(columns=columns).to_csv(path, index=False)
            return

        df = pd.read_csv(path)
        df.columns = [str(c).strip() for c in df.columns]

        # Se não tem nenhuma coluna ou está errado, força schema
        if len(df.columns) == 0:
            pd.DataFrame(columns=columns).to_csv(path, index=False)
            return

        # Se faltam colunas essenciais, adiciona
        changed = False
        for col in columns:
            if col not in df.columns:
                df[col] = "" if col != "valor" else 0.0
                changed = True

        # Ordena colunas (mantém extras no fim)
        if changed:
            ordered = columns + [c for c in df.columns if c not in columns]
            df = df[ordered]
            df.to_csv(path, index=False)

    except Exception:
        # Se leitura falhar por qualquer motivo, recria vazio com schema correto
        pd.DataFrame(columns=columns).to_csv(path, index=False)


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    merged = DEFAULT_CONFIG.copy()
    merged.update(cfg or {})
    return merged


def save_config(config: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def _safe_load_csv(path: Path, columns: list[str]) -> pd.DataFrame:
    _ensure_csv(path, columns)
    df = pd.read_csv(path)
    df.columns = [str(c).strip() for c in df.columns]

    # Garante schema mesmo se alguém alterou header manualmente
    for col in columns:
        if col not in df.columns:
            df[col] = "" if col != "valor" else 0.0

    # Mantém ordem esperada
    ordered = columns + [c for c in df.columns if c not in columns]
    return df[ordered]


def load_compras():
    return _safe_load_csv(COMPRAS_FILE, SCHEMAS["compras"])


def save_compras(df):
    df.to_csv(COMPRAS_FILE, index=False)


def load_diario():
    return _safe_load_csv(DIARIO_FILE, SCHEMAS["diario"])


def save_diario(df):
    df.to_csv(DIARIO_FILE, index=False)


def load_timeline():
    return _safe_load_csv(TIMELINE_FILE, SCHEMAS["timeline"])


def save_timeline(df):
    df.to_csv(TIMELINE_FILE, index=False)
