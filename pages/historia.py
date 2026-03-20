from datetime import date
import pandas as pd
import streamlit as st
from services.storage import load_timeline, save_timeline


def fmt(v):
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


def render_historia():
    st.markdown("### Nossa História")
    st.caption("Transforme momentos em memória viva.")

    titulo = st.text_input("Momento")
    descricao = st.text_area("Descrição", height=120)
    categoria = st.selectbox("Categoria", ["Descoberta", "Ultrassom", "Compra especial", "Emoção", "Outro"])

    if st.button("Adicionar à timeline"):
        if titulo.strip():
            df = load_timeline()
            new_row = pd.DataFrame([{
                "data": str(date.today()),
                "titulo": titulo.strip(),
                "descricao": descricao.strip(),
                "categoria": categoria
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            save_timeline(df)
            st.success("Momento adicionado à história 🤍")
            st.rerun()
        else:
            st.warning("Dê um título para esse momento.")

    st.markdown("#### Linha do tempo")
    df = load_timeline()

    df = df.dropna(how="all")

    # Remove linhas “lixo”
    if "titulo" in df.columns:
        df = df[df["titulo"].apply(lambda x: fmt(x) != "")]
    if "data" in df.columns:
        df = df[df["data"].apply(lambda x: fmt(x) != "")]

    if df.empty:
        st.info("Sua história ainda está começando por aqui.")
        return

    if "data" in df.columns:
        df = df.sort_values("data", ascending=False)

    for _, row in df.iterrows():
        st.markdown(
            f"""
<div class="soft-card">
  <div class="small-label">{fmt(row.get('data'))} • {fmt(row.get('categoria'))}</div>
  <div class="section-title">{fmt(row.get('titulo'))}</div>
  <div>{fmt(row.get('descricao'))}</div>
</div>
            """,
            unsafe_allow_html=True,
        )

