import streamlit as st
from components.theme import apply_theme
from services.storage import ensure_data_files, load_config
from pages.hoje import render_hoje
from pages.sentir import render_sentir
from pages.historia import render_historia
from pages.preparar import render_preparar
from pages.futuro import render_futuro

st.set_page_config(
    page_title="Nossa Jornada do Bebê",
    page_icon="🤍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

apply_theme()
ensure_data_files()
config = load_config()

st.markdown("<h1 class='main-title'>🤍 Nossa Jornada do Bebê</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Uma memória viva da gravidez</p>", unsafe_allow_html=True)

menu = st.radio(
    "Navegação",
    ["Hoje", "Sentir", "Nossa História", "Preparar", "Cuidar do Futuro"],
    horizontal=True,
    label_visibility="collapsed",
)

if menu == "Hoje":
    render_hoje(config)
elif menu == "Sentir":
    render_sentir()
elif menu == "Nossa História":
    render_historia()
elif menu == "Preparar":
    render_preparar()
elif menu == "Cuidar do Futuro":
    render_futuro()
