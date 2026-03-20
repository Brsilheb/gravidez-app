
import streamlit as st

def apply_theme():
    st.markdown(
        """
<style>
.stApp { background-color: #F7EFE5; color: #4A4A4A; }
.main-title { text-align: center; font-size: 2.1rem; margin-bottom: 0.2rem; }
.subtitle { text-align: center; color: #6D6D6D; margin-bottom: 1.5rem; }
.soft-card {
  background: #FFFFFF; border-radius: 20px; padding: 20px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.06); margin-bottom: 16px;
}
.section-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 0.7rem; }
.story-card {
  background: linear-gradient(180deg, #FFFFFF 0%, #F3E6DF 100%);
  border-radius: 24px; padding: 28px 20px; text-align: center;
  box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}
div[data-testid="stMetric"] {
  background: #FFFFFF; border-radius: 18px; padding: 10px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}
.small-label { font-size: 0.9rem; color: #6D6D6D; }
</style>
        """,
        unsafe_allow_html=True,
    )

