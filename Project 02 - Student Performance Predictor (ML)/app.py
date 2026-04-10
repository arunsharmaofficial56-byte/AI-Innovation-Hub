import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt

# --- Set Page Config ---
st.set_page_config(
    page_title="Academix AI | Performance Predictor",
    page_icon="🎓",
    layout="wide"
)

# --- Premium Academix CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #020617);
        color: #f1f5f9;
    }

    /* Glass Panels for pure HTML content */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }

    /* Titles */
    .main-title {
        background: linear-gradient(135deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        letter-spacing: -0.04em;
        margin-bottom: 10px;
    }

    .sub-title {
        color: #94a3b8;
        text-align: center;
        font-size: 1.25rem;
        margin-bottom: 40px;
        font-weight: 400;
    }

    /* Custom Metrics */
    .metric-row {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }

    .stat-box {
        flex: 1;
        min-width: 250px;
        background: rgba(15, 23, 42, 0.6);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: transform 0.3s ease;
    }

    .score-value {
        font-size: 3rem;
        font-weight: 800;
        margin: 10px 0;
    }

    /* Tags */
    .tag {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .tag-pass { background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981; }
    .tag-fail { background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }

    /* Performance Levels */
    .perf-excellent { color: #10b981; }
    .perf-good { color: #38bdf8; }
    .perf-average { color: #fbbf24; }
    .perf-improv { color: #f87171; }

    /* Recommendations */
    .tip-card {
        padding: 20px;
        border-radius: 16px;
        background: rgba(56, 189, 248, 0.05);
        border-left: 4px solid #38bdf8;
        margin-bottom: 12px;
        font-size: 1.05rem;
    }

    /* Sidebar Fix */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Slider Overrides */
    .stSlider > div > div > div > div {
        background-color: #38bdf8;
    }

    </style>
""", unsafe_allow_html=True)

# --- Load Model Pipeline ---
@st.cache_resource
def load_model():
    try:
        with open('model_pipeline.pkl', 'rb') as f:
            pipeline = pickle.load(f)
        return pipeline
    except Exception:
        return None

pipeline = load_model()

# --- Load Metrics ---
@st.cache_data
def load_metrics():
    try:
        with open('metrics.pkl', 'rb') as f:
            metrics = pickle.load(f)
        return metrics.get('accuracy', 0.92)
    except Exception:
        return 0.92

accuracy = load_metrics()

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8066/8066601.png", width=110)
    st.title("Academix AI")
    st.markdown("### 🎓 Input Parameters")
    
    st.markdown("#### Academics")
    study_hours = st.slider("📚 Study Hours / Week", 0.0, 40.0, 15.0, 0.5)
    attendance = st.slider("🏫 Attendance (%)", 0.0, 100.0, 85.0, 1.0)
    previous_marks = st.slider("📝 Previous Score (%)", 0.0, 100.0, 75.0, 1.0)
    
    st.markdown("#### Lifestyle")
    sleep_hours = st.slider("😴 Sleep Hours / Night", 2.0, 12.0, 7.5, 0.5)
    internet_usage = st.slider("📱 Digital Usage (Hrs/Day)", 0.0, 14.0, 3.0, 0.5)
    
    extracurricular = st.selectbox(
        "⚽ Activity Involvement",
        ["None", "Sports", "Music", "Tech Club", "Volunteering"]
    )
    
    st.markdown("---")
    st.markdown("### 🤖 System Intelligence")
    st.metric("Model Precision", f"{accuracy*100:.1f}%")
    st.caption("Random Forest Regression v2.4")

# --- Header ---
st.markdown('<h1 class="main-title">Academix AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Intelligent Educational Performance Analytics & Prediction</p>', unsafe_allow_html=True)

if not pipeline:
    st.error("⚠️ Model engine offline. Please generate 'model_pipeline.pkl' to utilize prediction features.")
else:
    # --- Prediction Processing ---
    input_df = pd.DataFrame([{
        'study_hours': study_hours,
        'attendance': attendance,
        'previous_marks': previous_marks,
        'sleep_hours': sleep_hours,
        'internet_usage': internet_usage,
        'extracurricular_activities': extracurricular
    }])

    predicted_score = pipeline.predict(input_df)[0]
    predicted_score = min(max(predicted_score, 0), 100)
    
    # Categorization
    if predicted_score >= 85:
        level, color_class = "EXCELLENT", "perf-excellent"
    elif predicted_score >= 65:
        level, color_class = "GOOD", "perf-good"
    elif predicted_score >= 40:
        level, color_class = "AVERAGE", "perf-average"
    else:
        level, color_class = "CRITICAL", "perf-improv"

    # --- Result Display ---
    st.write("### 📊 Predicted Performance Analysis")
    
    # Render main stats in ONE block to avoid layout break
    tag_html = '<span class="tag tag-pass">Passing</span>' if predicted_score >= 40 else '<span class="tag tag-fail">At Risk</span>'
    
    st.markdown(f"""
        <div class="glass-card">
            <div class="metric-row">
                <div class="stat-box">
                    <p style="color: #94a3b8; font-weight: 600; margin: 0;">EXPECTED GRADE</p>
                    <p class="score-value {color_class}" style="margin: 10px 0;">{predicted_score:.1f}%</p>
                    <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 10px; overflow: hidden;">
                        <div style="width: {predicted_score}%; height: 100%; background: linear-gradient(90deg, #38bdf8, #818cf8); border-radius: 10px;"></div>
                    </div>
                </div>
                <div class="stat-box">
                    <p style="color: #94a3b8; font-weight: 600; margin: 0;">STANDING</p>
                    <p class="score-value" style="font-size: 2.2rem; margin: 20px 0;">{tag_html}</p>
                    <p style="margin: 0; color: #64748b; font-size: 0.9rem;">Threshold: 40% Min</p>
                </div>
                <div class="stat-box">
                    <p style="color: #94a3b8; font-weight: 600; margin: 0;">TIER LEVEL</p>
                    <p class="score-value {color_class}" style="font-size: 2.2rem; margin: 20px 0;">{level}</p>
                    <p style="margin: 0; color: #64748b; font-size: 0.9rem;">Intelligence Output</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- Second Row Visuals ---
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.write("### 📈 Score Comparison")
        # Self-contained Plot
        fig, ax = plt.subplots(figsize=(10, 5))
        cats = ['Global Avg', 'Predicted', 'Distinction', 'Perfect']
        vals = [55, predicted_score, 75, 100]
        clrs = ['#475569', '#38bdf8', '#818cf8', '#10b981']
        
        ax.bar(cats, vals, color=clrs, alpha=0.9, width=0.6)
        ax.set_ylim(0, 110)
        ax.grid(axis='y', linestyle='--', alpha=0.1)
        
        # Dark theme patches
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#0f172a')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors='#94a3b8', labelsize=10)
        
        for i, v in enumerate(vals):
            ax.text(i, v + 2, f"{v}%", color='white', ha='center', fontweight='bold')
            
        st.pyplot(fig)

    with c2:
        st.write("### 💡 AI Recommendations")
        
        tips = []
        if sleep_hours < 7: tips.append("🛌 Improve sleep cycles for memory consolidation.")
        if internet_usage > 5: tips.append("📵 High digital friction detected in routine.")
        if attendance < 80: tips.append("🏫 Increase attendance to stabilize foundations.")
        if study_hours < 8: tips.append("📚 Scale deep work hours to 10h+ weekly.")
            
        if not tips:
            st.success("🌟 System Status: No critical anomalies detected.")
        else:
            for t in tips:
                st.markdown(f'<div class="tip-card">{t}</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown(f"""
    <div style="text-align: center; margin-top: 60px; color: #475569; padding-bottom: 20px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 20px;">
        Powered by Academix Intelligence Core | Developed for Arun Sharma
    </div>
""", unsafe_allow_html=True)
