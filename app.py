import streamlit as st
import json
import random

st.set_page_config(page_title="UNEC İmtahan Sistemi", layout="wide", initial_sidebar_state="expanded")

# "Cavabı göstər" sıxılıbsa, düzgün variantın sırasını tapıb CSS çərçivəsini bura qoşuruq
css_injection = ""
if st.session_state.get("exam_started", False) and not st.session_state.get("submitted", False):
    if st.session_state.get("show_current_answer", False) and "exam_questions" in st.session_state:
        questions = st.session_state.exam_questions
        curr_idx = st.session_state.current_index
        
        if 0 <= curr_idx < len(questions):
            q = questions[curr_idx]
            correct_text = q['correct']
            options = q['options']
            
            if correct_text in options:
                # Düzgün cavabın neçənci sırada olduğunu tapırıq (1, 2, 3, 4 və ya 5)
                correct_position = options.index(correct_text) + 1
                
                # Bu CSS yalnız düzgün variantın ətrafını yaşıl çərçivəyə alır və fonunu tünd yaşıl edir
                css_injection = f"""
                <style>
                div[role="radiogroup"] div[data-baseweb="radio"]:nth-of-type({correct_position}) {{
                    border: 2px solid #10B981 !important;
                    background-color: #064E3B !important;
                    border-radius: 8px !important;
                }}
                </style>
                """

# Əsas CSS Dizaynı
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #0B0E14;
        color: #D1D5DB;
    }}
    h1, h2, h3 {{
        color: #FFFFFF !important;
    }}
    .sual-header {{
        font-size: 18px;
        color: #8892B0;
        margin-bottom: 20px;
    }}
    .sual-karti {{
        background-color: #111622;
        border: 1px solid #1F293D;
        border-radius: 10px;
        padding: 30px;
        margin-bottom: 20px;
    }}
    div[data-baseweb="radio"] {{
        background-color: #161B26 !important;
        padding: 14px 20px !important;
        border-radius: 8px !important;
        margin-bottom: 12px !important;
        border: 1px solid #242F41 !important;
        transition: 0.1s;
    }}
    div[data-baseweb="radio"]:hover {{
        border-color: #3B82F6 !important;
    }}
    .stRadio > label {{
        color: #FFFFFF !important;
        font-size: 16px !important;
    }}
    .stButton > button {{
        width: 100% !important;
        background-color: #1F293D !important;
        color: #FFFFFF !important;
        border: 1px solid #374151 !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
