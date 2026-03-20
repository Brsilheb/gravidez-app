import streamlit as st
from components.cards import soft_card, story_card
from services.pregnancy_service import calculate_current_week, get_baby_size
from services.emotion_service import get_week_message, get_daily_moment

def render_hoje(config: dict):
    week = calculate_current_week(config["data_prevista_parto"])
    baby_size = get_baby_size(week)
    message = get_week_message(week)
    baby_name = config.get("nome_bebe", "").strip()

    st.markdown(f"### Semana {week}" + (f" de {baby_name} 🤍" if baby_name else " 🤍"))
    story_card(f"Semana {week}", baby_size, message)
    soft_card("Momento do dia", get_daily_moment())
    soft_card("Curiosidade da fase", "A cada semana, o corpo e o coração se reorganizam para acolher uma nova vida.")

    if st.button("📸 Gerar modo story"):
        st.success("Tela pronta para print e compartilhamento.")
        story_card(f"Semana {week} 🤍", baby_size, "Estamos te esperando com todo amor do mundo.")
