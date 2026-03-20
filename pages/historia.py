from datetime import date
import pandas as pd
import streamlit as st
from services.storage import load_timeline, save_timeline


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

    if df.empty:
        st.info("Sua história ainda está começando por aqui.")
        return

    # Agora é seguro: storage garante coluna "data"
    df = df.sort_values("data", ascending=False)

    for _, row in df.iterrows():
        st.markdown(
            f"""
<div class="soft-card">
  <div class="small-label">{row['data']} • {row['categoria']}</div>
  <div class="section-title">{row['titulo']}</div>
  <div>{row['descricao']}</div>
</div>
            """,
            unsafe_allow_html=True,
        )
