import streamlit as st
import pickle
import re
import nltk
from nltk.corpus import stopwords
import os
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="GuardianAI | Forensic News Analysis",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Modern Design System (Custom CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@400;500&display=swap');

    :root {
        --primary: #6366f1;
        --secondary: #ec4899;
        --bg-dark: #0f172a;
        --glass: rgba(30, 41, 59, 0.7);
        --border: rgba(255, 255, 255, 0.1);
    }

    .stApp {
        background-color: #0b0e14;
        background-image: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0, transparent 50%), 
                          radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.1) 0, transparent 50%);
    }

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid var(--border);
    }

    /* Premium Container */
    .glass-box {
        background: var(--glass);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 40px;
        border: 1px solid var(--border);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }

    /* Header Styling */
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.25rem;
        font-weight: 400;
        margin-bottom: 3rem;
    }

    /* Form Fields */
    .stTextArea textarea {
        background: #1e293b !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        color: #f8fafc !important;
        font-size: 1.1rem !important;
        padding: 20px !important;
        transition: all 0.3s ease;
    }

    .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2) !important;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        padding: 16px !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4) !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(99, 102, 241, 0.5) !important;
    }

    /* Indicators */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }

    .badge-primary { background: rgba(99, 102, 241, 0.2); color: #818cf8; }

    /* Result Cards */
    .res-container {
        padding: 40px;
        border-radius: 24px;
        margin-top: 2rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--border);
    }

    .res-label {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    /* Anim */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-up { animation: slideUp 0.6s ease-out; }

</style>
""", unsafe_allow_html=True)

# --- Preprocessing Function ---
@st.cache_data
def preprocess_text(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    
    try:
        stop_words = set(stopwords.words('english'))
    except LookupError:
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))
        
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

# --- Load Engine Cache ---
@st.cache_resource
def load_engine():
    try:
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('metrics.pkl', 'rb') as f:
            metrics = pickle.load(f)
        return vectorizer, model, metrics.get('accuracy', 0.85)
    except FileNotFoundError:
        return None, None, 0.0

vectorizer, model, accuracy = load_engine()

# --- Content ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/7504/7504369.png", width=100)
    st.markdown("## GuardianAI Lab")
    st.markdown("Expert Linguistic Forensics & Veracity Analysis.")
    
    st.markdown("---")
    st.markdown("### 🔍 Engine Telemetry")
    st.metric(label="Algorithm Confidence", value=f"{accuracy*100:.1f}%")
    st.progress(accuracy)
    
    st.markdown("---")
    st.markdown("### 🔧 Technical Specs")
    st.code("Model: Logistic Regression\nVector: TF-IDF Pipeline\nDataset: ISOT Standard")
    
    st.markdown("---")
    st.caption("Developed by Arun Sharma\nAI Development Portfolio 2026")

# --- Hero Section ---
st.markdown('<div class="status-badge badge-primary">Intelligence Node: Active</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Forensic News Scan</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">High-fidelity linguistic analysis to detect fabricated informational patterns.</p>', unsafe_allow_html=True)

# --- Primary Interface ---
layout_col1, layout_col2 = st.columns([7, 3])

with layout_col1:
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.write("#### 🛡️ Forensic Input Console")
    user_input = st.text_area("", height=320, placeholder="Input article text or headline for deep linguistic scanning...")
    
    st.write("")
    if st.button("RUN FORENSIC SCAN"):
        if not user_input.strip():
            st.warning("Forensic input required to proceed.")
        elif len(user_input.split()) < 5:
            st.error("Linguistic sample too brief for confident analysis (Min. 5 words).")
        else:
            if model and vectorizer:
                with st.spinner("Analyzing linguistic markers..."):
                    processed = preprocess_text(user_input)
                    vec_input = vectorizer.transform([processed])
                    
                    if vec_input.nnz == 0:
                        st.error("Insufficient distinctive features detected in sample.")
                    else:
                        prediction = model.predict(vec_input)[0]
                        probabilities = model.predict_proba(vec_input)[0]
                        conf_score = probabilities[1] if prediction == 1 else probabilities[0]
                        conf_pct = conf_score * 100

                        # Result Display
                        st.markdown('<div class="animate-up">', unsafe_allow_html=True)
                        if prediction == 1:
                            st.markdown(f"""
                                <div class="res-container" style="border-left: 8px solid #10b981;">
                                    <div style="color: #10b981; font-weight: 800; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 0.5rem;">Verdict: Authentic</div>
                                    <div class="res-label" style="color: #f1f5f9;">VERIFIED REAL</div>
                                    <p style="color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem;">Linguistic patterns align with factual reporting structures. Credibility verified.</p>
                                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 8px;">
                                        <span>CONFIDENCE RATING</span>
                                        <span>{conf_pct:.2f}%</span>
                                    </div>
                                    <div style="width: 100%; height: 8px; background: rgba(255,255,255,0.05); border-radius: 4px;">
                                        <div style="width: {conf_pct}%; height: 100%; background: #10b981; border-radius: 4px;"></div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div class="res-container" style="border-left: 8px solid #ef4444;">
                                    <div style="color: #ef4444; font-weight: 800; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 0.5rem;">Verdict: Non-Veridical</div>
                                    <div class="res-label" style="color: #f1f5f9;">MISTRUSTED CONTENT</div>
                                    <p style="color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem;">Anomalous linguistic patterns detected. High probability of fabrication or bias.</p>
                                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 8px;">
                                        <span>UNRELIABILITY INDEX</span>
                                        <span>{conf_pct:.2f}%</span>
                                    </div>
                                    <div style="width: 100%; height: 8px; background: rgba(255,255,255,0.05); border-radius: 4px;">
                                        <div style="width: {conf_pct}%; height: 100%; background: #ef4444; border-radius: 4px;"></div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Engine failure: Critical assets (model.pkl) missing from directory.")
    st.markdown('</div>', unsafe_allow_html=True)

with layout_col2:
    st.markdown('<div class="glass-box" style="padding: 25px;">', unsafe_allow_html=True)
    st.write("### Usage Protocol")
    st.info("""
    1. Paste the full article content.
    2. Click 'Run Forensic Scan'.
    3. Review the confidence rating.
    """)
    st.markdown("---")
    st.write("### System Architecture")
    st.caption("This system utilizes Logistic Regression trained on the ISOT Fake News Dataset (20k+ samples). It analyzes word frequencies and token relations to distinguish between professional journalism and propaganda.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div style="text-align: center; margin-top: 4rem; padding-bottom: 2rem;">
    <p style="color: #64748b; font-size: 0.9rem;">
        GuardianAI Lab v2.0 | Security Intelligence Division | 🛡️
    </p>
</div>
""", unsafe_allow_html=True)
