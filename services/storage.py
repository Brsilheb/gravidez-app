
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
    "metodo_data": "DPP",                 # "DPP" ou "DUM"
    "data_prevista_parto": "2026-12-01",  # usado quando metodo_data="DPP"
    "data_ultima_menstruacao": "",        # usado quando metodo_data="DUM"
    "tema_visual": "rose",
    "modo_som": False
}

def ensure_data_files():
    USER_DATA_DIR.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
    if not COMPRAS_FILE.exists():
        pd.DataFrame(columns=["item","categoria","valor","status","data"]).to_csv(COMPRAS_FILE, index=False)
    if not DIARIO_FILE.exists():
        pd.DataFrame(columns=["data","emocao","titulo","texto","tipo"]).to_csv(DIARIO_FILE, index=False)
    if not TIMELINE_FILE.exists():
        pd.DataFrame(columns=["data","titulo","descricao","categoria"]).to_csv(TIMELINE_FILE, index=False)

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def load_compras():
    return pd.read_csv(COMPRAS_FILE)

def save_compras(df):
    df.to_csv(COMPRAS_FILE, index=False)

def load_diario():
    return pd.read_csv(DIARIO_FILE)

def save_diario(df):
    df.to_csv(DIARIO_FILE, index=False)

def load_timeline():
    return pd.read_csv(TIMELINE_FILE)

def save_timeline(df):
    df.to_csv(TIMELINE_FILE, index=False)

