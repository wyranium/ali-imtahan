import streamlit as st
import json
import random

st.set_page_config(page_title="UNEC İmtahan Sistemi", layout="wide", initial_sidebar_state="collapsed")

# Əgər "Cavabı göstər" sıxılıbsa, düzgün variantın sırasını tapıb CSS ilə çərçivəyə alırıq
css_injection = ""
if st.session_state.get("show_current_answer", False) and "exam_questions" in st.session_state:
    questions = st.session_state.exam_questions
    curr_idx = st.session_state.current_index
    if 0 <= curr_idx < len(questions):
        q = questions[curr_idx]
        correct_text = q['correct']
        options = q['options']
        
        if correct_text in options:
            correct_position = options.index(correct_text) + 1
            css_injection = f"""
            <style>
            div[role="radiogroup"] div[data-baseweb="radio"]:nth-of-type({correct_position}) {{
                border: 2px solid #10B981 !important;
                background-color: #064E3B !important;
                border-radius: 8px !important;
            }}
            </style>
            """

# Mobil və Kompüter üçün Xüsusi Təkmilləşdirilmiş CSS Dizaynı
st.markdown(f"""
    <style>
    /* Ümumi Fon və Yazı Rəngləri */
    .stApp {{
        background-color: #0B0E14;
        color: #D1D5DB;
    }}
    h1, h2, h3 {{
        color: #FFFFFF !important;
    }}
    
    /* Sual Başlığı (Üst hissə) */
    .sual-header {{
        font-size: 16px;
        color: #8892B0;
        margin-bottom: 15px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Sual Kartı */
    .sual-karti {{
        background-color: #111622;
        border: 1px solid #1F293D;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }}
    .sual-karti h3 {{
        font-size: 18px !important;
        line-height: 1.5 !important;
    }}
    
    /* Radio Düymələr (Variantlar) - Mobil üçün Genişləndirilmiş */
    div[data-baseweb="radio"] {{
        background-color: #161B26 !important;
        padding: 16px 20px !important;
        border-radius: 8px !important;
        margin-bottom: 12px !important;
        border: 1px solid #242F41 !important;
        transition: 0.1s;
        cursor: pointer;
    }}
    div[data-baseweb="radio"]:hover {{
        border-color: #3B82F6 !important;
    }}
    .stRadio > label {{
        color: #FFFFFF !important;
        font-size: 16px !important;
    }}
    
    /* Düymələrin Ümumi Stili (Telefonda barmaqla rahat sıxılması üçün ölçülər) */
    .stButton > button {{
        width: 100% !important;
        background-color: #1F293D !important;
        color: #FFFFFF !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        min-height: 48px !important; /* Mobil klik standartı */
    }}
    
    /* Göy Düymələr (Növbəti və Başla) */
    div[data-testid="stSidebar"] .stButton > button,
    .blue-btn > div > button {{
        background-color: #1D4ED8 !important;
        border: none !important;
    }}
    .blue-btn > div > button:hover {{
        background-color: #2563EB !important;
    }}
    
    /* Bitir Düyməsi */
    .bitir-btn > div > button {{
        background-color: #DC2626 !important; /* Daha diqqət çəkən qırmızı rəng */
        font-weight: bold !important;
        border: none !important;
    }}
    .bitir-btn > div > button:hover {{
        background-color: #EF4444 !important;
    }}
    
    /* Naviqasiya Paneli Bloku (Mobil üçün alt-alta düşəndə məsafəni qoruyur) */
    .nav-block {{
        margin-top: 10px;
        margin-bottom: 10px;
    }}
    
    /* Mobil Ekranlar Üçün Xüsusi Tənzimləmələr (Ekran 768px-dən kiçik olduqda) */
    @media (max-width: 768px) {{
        .sual-karti {{
            padding: 15px;
        }}
        .sual-karti h3 {{
            font-size: 16px !important;
        }}
        div[data-baseweb="radio"] {{
            padding: 14px 16px !important;
        }}
        .stButton > button {{
            padding: 10px 15px !important;
            font-size: 15px !important;
        }}
    }}
    </style>
    {css_injection}
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

    # SIDEBAR (Ayarlar paneli mobil telefonlarda ekranı tutmasın deyə gizli başlayır)
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
        
        st.markdown(f"<div class='sual-header'>Mühəndis Mexanikası • Sual {curr_idx + 1}/{total_q}</div>", unsafe_allow_html=True)
        
        # Sual və variantlar mərkəzdə tam genişlikdə görünür (Mobil üçün əla struktur)
        st.markdown(f"<div class='sual-karti'><h3>{q['question']}</h3></div>", unsafe_allow_html=True)
        
        current_choice = st.session_state.user_answers.get(curr_idx, None)
        options = q['options']
        
        user_choice = st.radio(
            f"options_{curr_idx}", 
            options, 
            index=options.index(current_choice) if current_choice in options else None, 
            key=f"radio_{curr_idx}", 
            label_visibility="collapsed"
        )
        
        if user_choice:
            st.session_state.user_answers[curr_idx] = user_choice
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Naviqasiya və Əmrlər Düymələri (Aşağı paneldə mobilə tam uyğun yerləşmə)
        col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 1])
        
        with col_nav1:
            st.markdown('<div class="nav-block">', unsafe_allow_html=True)
            if st.button("⬅️ Əvvəlki", key="prev_btn") and curr_idx > 0:
                st.session_state.current_index -= 1
                st.session_state.show_current_answer = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_nav2:
            st.markdown('<div class="nav-block">', unsafe_allow_html=True)
            if st.button("👁️ Cavab", key="show_ans_btn"):
                st.session_state.show_current_answer = not st.session_state.show_current_answer
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_nav3:
            st.markdown('<div class="nav-block blue-btn">', unsafe_allow_html=True)
            if st.button("Növbəti ➡️", key="next_btn") and curr_idx < total_q - 1:
                st.session_state.current_index += 1
                st.session_state.show_current_answer = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Sual nömrəsinə birbaşa keçid və İmtahanı bitirmə paneli
        col_foot1, col_foot2 = st.columns([2, 1])
        with col_foot1:
            sual_no_input = st.text_input("Sual nömrəsinə keç:", value=str(curr_idx + 1))
            if st.button("Git / Keç"):
                try:
                    target_idx = int(sual_no_input) - 1
                    if 0 <= target_idx < total_q:
                        st.session_state.current_index = target_idx
                        st.session_state.show_current_answer = False
                        st.rerun()
                except:
                    pass
        with col_foot2:
            st.markdown("<br>" if not st.sidebar.checkbox else "", unsafe_allow_html=True) # Boşluq nizamı
            st.markdown('<div class="bitir-btn">', unsafe_allow_html=True)
            if st.button("İmtahanı Bitir", key="submit_exam_btn"):
                st.session_state.submitted = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # NƏTİCƏ REJİMİ
    elif st.session_state.get("submitted", False):
        questions = st.session_state.exam_questions
        correct_count = 0
        wrong_count = 0
        unanswered_count = 0
        
        for idx, q in enumerate(questions):
            user_ans = st.session_state.user_answers.get(idx, None)
            if user_ans == q['correct']:
                correct_count += 1
            elif user_ans is None:
                unanswered_count += 1
            else:
                wrong_count += 1
        
        st.markdown("## 📊 İmtahan Nəticəsi")
        col1, col2, col3 = st.columns(3)
        col1.metric("Doğru", f"✅ {correct_count}")
        col2.metric("Səhv", f"❌ {wrong_count}")
        col3.metric("Boş", f"⚪ {unanswered_count}")
        
        st.markdown("---")
        if st.button("🔄 Yeni İmtahana Başla"):
            st.session_state.exam_started = False
            st.session_state.submitted = False
            st.rerun()
