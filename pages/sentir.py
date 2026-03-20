from datetime import date
import pandas as pd
import streamlit as st
from services.storage import load_diario, save_diario


def fmt(v):
    """Converte NaN/None/'nan' em string vazia para não poluir a UI."""
    if v is None:
        return ""
    try:
        if pd.isna(v):
            return ""
    except Exception:
        pass
    s = str(v).strip()
    if s.lower() in ("nan", "none"):
        return ""
    return s


def render_sentir():
    st.markdown("### Sentir")
    st.caption("Escreva o que seu coração não quer esquecer.")

    emocao = st.selectbox(
        "Como você está se sentindo hoje?",
        ["Alegria", "Gratidão", "Ansiedade", "Medo", "Esperança", "Ternura"],
    )
    titulo = st.text_input("Título")
    texto = st.text_area("Seu registro", height=180)
    tipo = st.selectbox("Tipo", ["Diário", "Carta para o bebê", "Reflexão"])

    if st.button("Salvar registro"):
        if texto.strip():
            df = load_diario()
            new_row = pd.DataFrame([{
                "data": str(date.today()),
                "emocao": emocao,
                "titulo": titulo.strip(),
                "texto": texto.strip(),
                "tipo": tipo
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            save_diario(df)
            st.success("Registro salvo com carinho 🤍")
            st.rerun()
        else:
            st.warning("Escreva algo antes de salvar.")

    st.markdown("#### Seus registros")
    df = load_diario()

    # Remove linhas totalmente vazias
    df = df.dropna(how="all")

    # Remove linhas “lixo”: se texto e data estiverem vazios/NaN
    if "texto" in df.columns:
        df = df[df["texto"].apply(lambda x: fmt(x) != "")]
    if "data" in df.columns:
        df = df[df["data"].apply(lambda x: fmt(x) != "")]

    if df.empty:
        st.info("Nenhum registro salvo ainda.")
        return

    if "data" in df.columns:
        df = df.sort_values("data", ascending=False)

    for _, row in df.iterrows():
        st.markdown(
            f"""
<div class="soft-card">
  <div class="small-label">{fmt(row.get('data'))} • {fmt(row.get('emocao'))} • {fmt(row.get('tipo'))}</div>
  <div class="section-title">{fmt(row.get('titulo')) or 'Sem título'}</div>
  <div>{fmt(row.get('texto'))}</div>
</div>
            """,
            unsafe_allow_html=True,
        )
