from datetime import date
import pandas as pd
import streamlit as st
from services.storage import load_timeline, save_timeline

def render_historia():
    st.markdown("### Nossa História")
    st.caption("Transforme momentos em memória viva.")
    titulo = st.text_input("Momento")
    descricao = st.text_area("Descrição", height=120)
    categoria = st.selectbox("Categoria", ["Descoberta","Ultrassom","Compra especial","Emoção","Outro"])

    if st.button("Adicionar à timeline"):
        if titulo.strip():
            df = load_timeline()
            new_row = pd.DataFrame([{"data": str(date.today()), "titulo": titulo.strip(), "descricao": descricao.strip(), "categoria": categoria}])
            df = pd.concat([df, new_row], ignore_index=True)
            save_timeline(df)
            st.success("Momento adicionado à história.")
        else:
            st.warning("Dê um título para esse momento.")

    st.markdown("#### Linha do tempo")
    df = load_timeline()
    if df.empty:
        st.info("Sua história ainda está começando por aqui.")
    else:
        for _, row in df.sort_values("data", ascending=False).iterrows():
            st.markdown(f"""
<div class="soft-card">
  <div class="small-label">{row['data']} • {row['categoria']}</div>
  <div class="section-title">{row['titulo']}</div>
  <div>{row['descricao']}</div>
</div>
""", unsafe_allow_html=True)
