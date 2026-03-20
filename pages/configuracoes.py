import streamlit as st
from datetime import date
from services.storage import load_config, save_config, DEFAULT_CONFIG

def render_configuracoes():
    st.markdown("### Configurações")
    st.caption("Preencha uma vez — e o app passa a montar a sua jornada automaticamente.")

    config = load_config()

    # Garante que chaves novas existam (para quem já tinha config antigo)
    merged = DEFAULT_CONFIG.copy()
    merged.update(config)
    config = merged

    with st.form("form_config"):
        col1, col2 = st.columns(2)

        with col1:
            nome_mae = st.text_input("Seu nome (ou como prefere ser chamada)", value=config.get("nome_mae", "Mamãe"))
            nome_bebe = st.text_input("Nome do bebê (opcional)", value=config.get("nome_bebe", ""))

        with col2:
            metodo = st.selectbox(
                "Você prefere informar:",
                ["Data prevista do parto (DPP)", "Data da última menstruação (DUM)"],
                index=0 if config.get("metodo_data", "DPP") == "DPP" else 1
            )

        st.markdown("#### Datas")
        
        if metodo.startswith("Data prevista"):
            new_config["metodo_data"] = "DPP"
            new_config["data_prevista_parto"] = dpp.isoformat()
            new_config["data_ultima_menstruacao"] = ""
        else:
            new_config["metodo_data"] = "DUM"
            new_config["data_ultima_menstruacao"] = dum.isoformat()
            new_config["data_prevista_parto"] = ""


        st.markdown("#### Preferências (opcional)")
        tema = st.selectbox(
            "Tema visual",
            ["rose", "bege", "azul"],
            index=["rose", "bege", "azul"].index(config.get("tema_visual", "rose"))
        )
        modo_som = st.toggle("Som (opcional)", value=bool(config.get("modo_som", False)))

        salvar = st.form_submit_button("Salvar configurações")

    if salvar:
        new_config = config.copy()
        new_config["nome_mae"] = nome_mae.strip() or "Mamãe"
        new_config["nome_bebe"] = nome_bebe.strip()
        new_config["tema_visual"] = tema
        new_config["modo_som"] = bool(modo_som)

        if dpp:
            new_config["metodo_data"] = "DPP"
            new_config["data_prevista_parto"] = dpp.isoformat()
            new_config["data_ultima_menstruacao"] = ""
        else:
            new_config["metodo_data"] = "DUM"
            new_config["data_ultima_menstruacao"] = dum.isoformat()
            new_config["data_prevista_parto"] = ""

        save_config(new_config)
        st.success("Configurações salvas 🤍 Agora o app já consegue calcular tudo para você.")

def _safe_date(value):
    """Converte 'YYYY-MM-DD' em date, ou retorna None."""
    if not value:
        return None
    try:
        y, m, d = value.split("-")
        return date(int(y), int(m), int(d))
    except Exception:
        return None