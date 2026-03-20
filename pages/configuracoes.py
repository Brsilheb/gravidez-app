import streamlit as st
from datetime import date
from services.storage import load_config, save_config, DEFAULT_CONFIG


def render_configuracoes():
    st.markdown("### Configurações")
    st.caption("Preencha uma vez — e o app calcula sua semana automaticamente 🤍")

    # Carrega config e garante chaves novas
    config = DEFAULT_CONFIG.copy()
    try:
        config.update(load_config() or {})
    except Exception:
        # Se por algum motivo não conseguir ler o config.json, seguimos com o default
        pass

    col1, col2 = st.columns(2)

    with col1:
        nome_mae = st.text_input(
            "Seu nome (ou como prefere ser chamada)",
            value=config.get("nome_mae", "Mamãe"),
        )
        nome_bebe = st.text_input(
            "Nome do bebê (opcional)",
            value=config.get("nome_bebe", ""),
        )

    with col2:
        metodo = st.radio(
            "Você prefere informar:",
            ["DPP (data prevista do parto)", "DUM (última menstruação)"],
            index=0 if (config.get("metodo_data", "DPP").upper() == "DPP") else 1,
        )

    st.markdown("#### Data")
    dpp = None
    dum = None

    if metodo.startswith("DPP"):
        dpp = st.date_input(
            "Data prevista do parto (DPP)",
            value=_safe_date(config.get("data_prevista_parto")) or date.today(),
        )
    else:
        dum = st.date_input(
            "Data da última menstruação (DUM)",
            value=_safe_date(config.get("data_ultima_menstruacao")) or date.today(),
        )

    st.markdown("#### Preferências (opcional)")
    tema = st.selectbox(
        "Tema visual",
        ["rose", "bege", "azul"],
        index=["rose", "bege", "azul"].index(config.get("tema_visual", "rose"))
        if config.get("tema_visual", "rose") in ["rose", "bege", "azul"]
        else 0,
    )
    modo_som = st.checkbox("Som (opcional)", value=bool(config.get("modo_som", False)))

    # ✅ Botão simples (evita problema de form e submit)
    if st.button("Salvar configurações", type="primary"):
        new_config = config.copy()
        new_config["nome_mae"] = (nome_mae or "Mamãe").strip() or "Mamãe"
        new_config["nome_bebe"] = (nome_bebe or "").strip()
        new_config["tema_visual"] = tema
        new_config["modo_som"] = bool(modo_som)
        
     
        # ✅ “Ou um ou outro”
        if dpp is not None:
            new_config["metodo_data"] = "DPP"
            new_config["data_prevista_parto"] = dpp.isoformat()
            new_config["data_ultima_menstruacao"] = ""
        else:
            new_config["metodo_data"] = "DUM"
            new_config["data_ultima_menstruacao"] = dum.isoformat()
            new_config["data_prevista_parto"] = ""

        try:
            save_config(new_config)
            st.success("Configurações salvas 🤍")
        except Exception:
            # No Streamlit Cloud, escrita em arquivo pode falhar em alguns casos
            st.session_state["config_runtime"] = new_config
            st.warning("Não consegui salvar em arquivo aqui, mas mantive suas configurações nesta sessão.")
            st.rerun()


def _safe_date(value):
    """Converte 'YYYY-MM-DD' em date, ou retorna None."""
    if not value:
        return None
    try:
        y, m, d = value.split("-")
        return date(int(y), int(m), int(d))
    except Exception:
        return None
