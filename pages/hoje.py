import streamlit as st
from components.cards import soft_card, story_card
from services.pregnancy_service import calculate_current_week, get_baby_size
from services.emotion_service import get_week_message, get_daily_moment


def render_hoje(config: dict):
    """
    Tela principal do MVP (Dashboard emocional).
    Usa as configurações da usuária para calcular a semana atual e exibir mensagens.
    """

    # Agora o cálculo usa o config completo (suporta DPP ou DUM)
    week = calculate_current_week(config)

    baby_size = get_baby_size(week)
    message = get_week_message(week)

    baby_name = (config.get("nome_bebe") or "").strip()
    mae_name = (config.get("nome_mae") or "Mamãe").strip()

