from datetime import date
import pandas as pd
import streamlit as st
from services.storage import load_compras, save_compras
from services.finance_service import get_progress_percent
from components.charts import render_expense_chart

def render_preparar():
    st.markdown("### Preparar")
    st.caption("Mais um passo para receber seu bebê com amor.")
    item = st.text_input("Item")
    categoria = st.selectbox("Categoria", ["Enxoval","Higiene","Quarto","Saída maternidade","Outros"])
    valor = st.number_input("Valor", min_value=0.0, step=1.0)
    status = st.selectbox("Status", ["Pendente","Comprado"])

    if st.button("Adicionar item"):
        if item.strip():
            df = load_compras()
            new_row = pd.DataFrame([{"item": item.strip(), "categoria": categoria, "valor": valor, "status": status, "data": str(date.today())}])
            df = pd.concat([df, new_row], ignore_index=True)
            save_compras(df)
            st.success("Mais um detalhe preparado com amor 🤍")
        else:
            st.warning("Informe o nome do item.")

    df = load_compras()
    col1, col2 = st.columns(2)
    col1.metric("Itens cadastrados", len(df))
    col2.metric("Progresso", f"{get_progress_percent(df)}%")

    st.markdown("#### Gastos por categoria")
    render_expense_chart(df)

    st.markdown("#### Lista de compras")
    if df.empty:
        st.info("Nenhum item adicionado ainda.")
    else:
        st.dataframe(df.sort_values("data", ascending=False), use_container_width=True)
