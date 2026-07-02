import streamlit as st
import json
import random

st.set_page_config(page_title="UNEC İmtahan Sistemi", layout="wide", initial_sidebar_state="expanded")

# Əsas CSS Dizaynı (Heç bir f-string və xəta riski yoxdur)
st.markdown("""
    <style>
    .stApp {
        background-color: #0B0E14;
        color: #D1D5DB;
    }
    h1, h2, h3 {
        color: #FFFFFF !important;
    }
    .sual-header {
        font-size: 18px;
        color: #8892B0;
        margin-bottom: 20px;
    }
    .sual-karti {
        background-color: #111622;
        border: 1px solid #1F293D;
        border-radius: 10px;
        padding: 30px;
        margin-bottom: 20px;
    }
    div[data-baseweb="radio"] {
        background-color: #161B26 !important;
        padding: 14px 20px !important;
        border-radius: 8px !important;
