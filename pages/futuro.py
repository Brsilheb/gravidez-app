import streamlit as st
from services.storage import load_compras
from services.finance_service import get_total_spent, get_completed_items

def render_futuro():
    st.markdown("### Cuidar do Futuro")
    st.caption("Tudo que vocês constroem hoje já é parte da vida que está chegando.")
    df = load_compras()
    total = get_total_spent(df)
    completed = get_completed_items(df)

    col1, col2 = st.columns(2)
    col1.metric("Total investido", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col2.metric("Itens comprados", completed)

    st.markdown(
        """
<div class="soft-card">
  <div class="section-title">Visão do cuidado</div>
  <div>Cada escolha feita agora não é apenas gasto ou planejamento. É preparação, presença e amor transformado em realidade.</div>
</div>
        """,
        unsafe_allow_html=True
    )
