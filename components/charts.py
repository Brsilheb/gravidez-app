import streamlit as st
import plotly.express as px
import pandas as pd

def render_expense_chart(df: pd.DataFrame):
    if df.empty:
        st.info("Ainda não há compras registradas.")
        return
    grouped = df.groupby("categoria", as_index=False)["valor"].sum()
    fig = px.pie(grouped, names="categoria", values="valor", hole=0.55)
    fig.update_layout(
        paper_bgcolor="#F7EFE5",
        plot_bgcolor="#F7EFE5",
        margin=dict(t=20, b=20, l=20, r=20),
    )
    st.plotly_chart(fig, use_container_width=True)
