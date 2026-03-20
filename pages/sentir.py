from datetime import date
import pandas as pd
import streamlit as st
from services.storage import load_diario, save_diario


def render_sentir():
    st.markdown("### Sentir")
    st.caption("Escreva o que seu coração não quer esquecer.")

    emocao = st.selectbox(
        "Como você está se sentindo hoje?",
        ["Alegria", "Gratidão", "Ansiedade", "Medo", "Esperança", "Ternura"]
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

    if df.empty:
        st.info("Nenhum registro salvo ainda.")
        return

    # Agora é seguro: storage garante coluna "data"
    df = df.sort_values("data", ascending=False)

    for _, row in df.iterrows():
        st.markdown(
            f"""
<div class="soft-card">
  <div class="small-label">{row['data']} • {row['emocao']} • {row['tipo']}</div>
  <div class="section-title">{row['titulo'] if row['titulo'] else 'Sem título'}</div>
  <div>{row['texto']}</div>
</div>
            """,
            unsafe_allow_html=True,
        )

