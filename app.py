import streamlit as st

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

st.title("Sales Dashboard")

st.write("""
Welcome to the Sales Dashboard.

Use the sidebar to navigate between:
- Profit Analysis
- Sales Analysis
- Sales trend Analysis
""")