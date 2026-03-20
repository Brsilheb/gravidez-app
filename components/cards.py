
import streamlit as st

def soft_card(title: str, content: str):
    st.markdown(
        f"""
<div class="soft-card">
  <div class="section-title">{title}</div>
  <div>{content}</div>
</div>
        """,
        unsafe_allow_html=True,
    )

def story_card(week_text: str, baby_size: str, message: str):
    st.markdown(
        f"""
<div class="story-card">
  <div style="font-size: 1.5rem; font-weight: 700;">{week_text}</div>
  <div style="margin-top: 8px; font-size: 1.2rem;">{baby_size}</div>
  <div style="margin-top: 18px; font-size: 1rem;">{message}</div>
</div>
        """,
        unsafe_allow_html=True,
    )

