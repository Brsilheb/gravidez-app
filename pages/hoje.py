import streamlit as st
from components.cards import soft_card, story_card
from services.pregnancy_service import calculate_current_week, get_baby_size
from services.emotion_service import get_week_message, get_daily_moment


def render_hoje(config: dict):
    # ✅ Prioriza config salvo em runtime (Cloud-safe)
    runtime = st.session_state.get("config_runtime")
    if isinstance(runtime, dict):
        config = runtime

    # ✅ Verificação explícita de data
    metodo = (config.get("metodo_data") or "").upper()
    dpp = (config.get("data_prevista_parto") or "").strip()
    dum = (config.get("data_ultima_menstruacao") or "").strip()

    has_date = False
    if metodo == "DUM" and dum:
        has_date = True
    if metodo != "DUM" and dpp:
        has_date = True

    if not has_date:
        st.markdown("### Hoje 🤍")
        st.warning("Para começar, informe sua data em **Configurações**.")
        soft_card(
            "Comece por aqui",
            "Vá em **Configurações**, escolha **DPP** ou **DUM**, salve e volte para cá."
        )
        return

    # ✅ Agora é seguro calcular
    week = calculate_current_week(config)
    baby_size = get_baby_size(week)
    message = get_week_message(week)

    baby_name = (config.get("nome_bebe") or "").strip()
    mae_name = (config.get("nome_mae") or "Mamãe").strip()

    st.markdown(f"### Semana {week}" + (f" de {baby_name} 🤍" if baby_name else " 🤍"))

    story_card(f"Semana {week}", baby_size, message)

    soft_card("Momento do dia", get_daily_moment())
    soft_card(
        "Curiosidade da fase",
        "A cada semana, o corpo e o coração se reorganizam para acolher uma nova vida.",
    )

    if st.button("📸 Gerar modo story"):
        st.success("Tela pronta para print e compartilhamento.")
        story_card(
            f"Semana {week} 🤍",
            baby_size,
            f"{mae_name}, estamos te esperando com todo amor do mundo.",
        )
