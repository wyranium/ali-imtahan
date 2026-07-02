import streamlit as st
import json
import random

st.set_page_config(page_title="UNEC İmtahan Sistemi", layout="wide", initial_sidebar_state="expanded")

# Əsas CSS Dizaynı
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
        margin-bottom: 12px !important;
        border: 1px solid #242F41 !important;
        transition: 0.1s;
    }
    div[data-baseweb="radio"]:hover {
        border-color: #3B82F6 !important;
    }
    .stRadio > label {
        color: #FFFFFF !important;
        font-size: 16px !important;
    }
    .stButton > button {
        width: 100% !important;
        background-color: #1F293D !important;
        color: #FFFFFF !important;
        border: 1px solid #374151 !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
    }
    div[data-testid="stSidebar"] .stButton > button,
    .blue-btn > div > button {
        background-color: #1D4ED8 !important;
        border: none !important;
    }
    .bitir-btn > div > button {
        background-color: #2563EB !important;
        font-weight: bold !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

try:
    with open("questions.json", "r", encoding="utf-8") as f:
        all_questions = json.load(f)
except Exception as e:
    all_questions = []

if len(all_questions) == 0:
    st.error("questions.json boşdur! Öncə 'parse_pdf.py' işlədin.")
else:
    total_extracted = len(all_questions)

    # SIDEBAR
    st.sidebar.markdown("### ⚙️ İmtahan Ayarları")
    st.sidebar.write(f"Ümumi sual sayısı: **{total_extracted}**")
    
    start_q = st.sidebar.number_input("Başlanğıc Sual", min_value=1, max_value=total_extracted, value=1)
    end_q = st.sidebar.number_input("Son Sual", min_value=1, max_value=total_extracted, value=total_extracted)
    
    max_selectable = end_q - start_q + 1
    num_to_show = st.sidebar.number_input("Testdəki Sual Sayı", min_value=1, max_value=max_selectable, value=max_selectable)
    shuffle_mode = st.sidebar.toggle("Sualları qarışdır", value=False)
    
    if st.sidebar.button("🎯 İmtahana Başla", type="primary"):
        st.session_state.exam_started = True
        st.session_state.submitted = False
        st.session_state.current_index = 0
        st.session_state.show_current_answer = False
        
        pool = all_questions[start_q-1:end_q]
        if shuffle_mode:
            random.shuffle(pool)
        st.session_state.exam_questions = pool[:num_to_show]
        st.session_state.user_answers = {}
        st.rerun()

    # İMTAHAN REJİMİ
    if st.session_state.get("exam_started", False) and not st.session_state.get("submitted", False):
        questions = st.session_state.exam_questions
        curr_idx = st.session_state.current_index
        total_q = len(questions)
        q = questions[curr_idx]
        
        st.markdown(f"<div class='sual-header'>muh mexanikasi • Sual {curr_idx + 1}/{total_q}</div>", unsafe_allow_html=True)
        
        col_left, col_center, col_right = st.columns([2, 6, 2])
        
        with col_left:
            if st.button("⬅️ Əvvəlki", key="prev_btn") and curr_idx > 0:
                st.session_state.current_index -= 1
                st.session_state.show_current_answer = False
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # CAVABI GÖSTƏR DÜYMƏSİ
            if st.button("👁️ Cavabı göstər", key="show_ans_btn"):
                st.session_state.show_current_answer = not st.session_state.show_current_answer
                st.rerun()
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            sual_no_input = st.text_input("Sual nömrəsi:", value=str(curr_idx + 1))
            if st.button("Keç"):
                try:
                    target_idx = int(sual_no_input) - 1
                    if 0 <= target_idx < total_q:
                        st.session_state.current_index = target_idx
                        st.session_state.show_current_answer = False
                        st.rerun()
                except:
                    pass

        with col_center:
            st.markdown(f"<div class='sual-karti'><h3>{q['question']}</h3></div>", unsafe_allow_html=True)
            
            options = q['options']
            
            # Əgər "Cavabı göstər" sıxılıbsa düzgün cavabı avtomatik işarələyir
            if st.session_state.get("show_current_answer", False):
                current_choice = q['correct']
            else:
                current_choice = st.session_state.user_answers.get(curr_idx, None)
            
            user_choice = st.radio(
                f"options_{curr_idx}", 
                options, 
                index=options.index(current_choice) if current_choice in options else None, 
                key=f"radio_{curr_idx}", 
                label_visibility="collapsed"
            )
            
            if user_choice:
                st.session_state.user_answers[curr_idx] = user_choice

        with col_right:
            st.markdown('<div class="blue-btn">', unsafe_allow_html=True)
            if st.button("Növbəti ➡️", key="next_btn") and curr_idx < total_q - 1:
                st.session_state.current_index += 1
                st.session_state.show_current_answer = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            
            st.markdown('<div class="bitir-btn">', unsafe_allow_html=True)
            if st.button("Bitir", key="submit_exam_btn"):
                st.session_state.submitted = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
