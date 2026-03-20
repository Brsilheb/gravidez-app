import streamlit as st
from components.cards import soft_card, story_card
from services.pregnancy_service import calculate_current_week, get_baby_size
from services.emotion_service import get_week_message, get_daily_moment
from services.story_export import generate_story_png
from services.fase_service import get_fase_content


def render_hoje(config: dict):
    # ✅ Prioriza config salvo em runtime (Cloud-safe)
    runtime = st.session_state.get("config_runtime")
    if isinstance(runtime, dict):
        config = runtime

    # ✅ Verificação explícita de data (DPP ou DUM)
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
            "Vá em **Configurações**, escolha **DPP** ou **DUM**, salve e volte para cá.",
        )
        return

    # ✅ Agora é seguro calcular
    week = calculate_current_week(config)
    baby_size = get_baby_size(week)
    message = get_week_message(week)

    baby_name = (config.get("nome_bebe") or "").strip()
    mae_name = (config.get("nome_mae") or "Mamãe").strip()
    theme = (config.get("tema_visual") or "rose").strip()

    st.markdown(f"### Semana {week}" + (f" de {baby_name} 🤍" if baby_name else " 🤍"))

    # Card “printável” (HTML)
    story_card(f"Semana {week}", baby_size, message)

    # Momento do dia
    soft_card("Momento do dia", get_daily_moment())

    # ✅ Bloco coerente: “Sobre esta fase” (emoção + curiosidade)
    fase = get_fase_content(week)
    emocional = (fase.get("emocional") or message).strip()
    curiosidade = (fase.get("curiosidade") or "").strip()

    conteudo = f"<p><strong>💭 Emoção</strong><br>{emocional}</p>"
    if curiosidade:
        conteudo += f"<p><strong>💡 Você sabia?</strong><br>{curiosidade}</p>"

    soft_card("Sobre esta fase", conteudo)

    # Prévia extra (opcional)
    if st.button("📸 Gerar modo story (prévia)"):
        st.success("Prévia pronta para print e compartilhamento.")
        story_card(
            f"Semana {week} 🤍",
            baby_size,
            f"{mae_name}, estamos te esperando com todo amor do mundo.",
        )

    # ✅ PNG real 1080×1920 para Instagram Story
    st.markdown("#### Modo Story (PNG)")

    story_bytes = generate_story_png(
        week=week,
        baby_size=baby_size,
        message=emocional,  # aqui usamos a parte emocional (fica mais “story”)
        baby_name=baby_name,
        mae_name=mae_name,
        theme=theme,
    )

    st.image(story_bytes, use_container_width=True)

    st.download_button(
        label="📥 Baixar Story (PNG 1080×1920)",
        data=story_bytes,
        file_name=f"story_semana_{week}.png",
        mime="image/png",
        use_container_width=True,
    )
