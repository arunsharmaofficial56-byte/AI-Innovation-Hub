import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="DataEdge AI | Analytics OS",
    page_icon="🌌",
    layout="wide"
)

# --- Premium DataEdge CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600&family=Outfit:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    .stApp {
        background: radial-gradient(circle at top right, #080a0f, #020205);
        color: #e2e8f0;
    }

    /* Glass Panels */
    .glass-panel {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.5);
        margin-bottom: 24px;
    }

    /* Branding */
    .brand-title {
        background: linear-gradient(135deg, #22d3ee, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        letter-spacing: -0.03em;
        margin-bottom: 8px;
    }

    .brand-subtitle {
        color: #64748b;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }

    /* Stat Cards */
    .stat-card {
        background: rgba(30, 41, 59, 0.3);
        padding: 20px;
        border-radius: 16px;
        border-left: 4px solid #06b6d4;
    }
    .stat-label { color: #94a3b8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .stat-value { color: #f8fafc; font-size: 1.8rem; font-weight: 700; margin-top: 5px; }

    /* Button Styling */
    .stButton>button {
        background: rgba(6, 182, 212, 0.1) !important;
        color: #22d3ee !important;
        border: 1px solid rgba(6, 182, 212, 0.3) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background: rgba(6, 182, 212, 0.2) !important;
        border-color: #22d3ee !important;
        transform: scale(1.02);
    }

    /* Sidebar Navigation */
    section[data-testid="stSidebar"] {
        background-color: #010409 !important;
        border-right: 1px solid rgba(255,255,255,0.03);
    }

    /* DataFrame Styling */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }

    </style>
""", unsafe_allow_html=True)

# --- Logic: Data Processing ---
@st.cache_data
def convert_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

@st.cache_data(show_spinner=False)
def load_dataset(file):
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        return pd.read_excel(file)
    except Exception:
        return None

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3596/3596091.png", width=90)
    st.title("DataEdge OS")
    
    st.markdown("### 🛰️ Input Node")
    uploaded_file = st.file_uploader("Upload CSV/XLSX Stream", type=["csv", "xlsx"])
    
    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    menu_choice = st.radio(
        "",
        ["Core Analytics", "Refining Studio", "Statistical Engine", "Visual Deck", "AI Insight Hub"]
    )
    
    st.markdown("---")
    st.caption("DataEdge Engine v1.1.0")
    st.caption("System Status: Operational 🟢")

# --- Main App Body ---
st.markdown('<h1 class="brand-title">DataEdge AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="brand-subtitle">Cloud-Integrated Advanced Data Mining & Visualization Platform</p>', unsafe_allow_html=True)

if not uploaded_file:
    st.markdown("""
        <div style="text-align:center; padding: 100px 20px; color: #475569; border: 2px dashed rgba(255,255,255,0.05); border-radius: 30px;">
            <p style="font-size: 1.5rem;">Waiting for data input stream...</p>
            <p>Upload a file from the sidebar to initialize analytics modules.</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# Initialize State
if 'df' not in st.session_state or st.session_state.get('curr_file') != uploaded_file.name:
    st.session_state.df = load_dataset(uploaded_file)
    st.session_state.curr_file = uploaded_file.name

df = st.session_state.df

# --- SECTION 1: Core Analytics ---
if menu_choice == "Core Analytics":
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.write("### 🌐 Dataset High-Level Overview")
    
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="stat-card"><p class="stat-label">Entries</p><p class="stat-value">{df.shape[0]:,}</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-card"><p class="stat-label">Features</p><p class="stat-value">{df.shape[1]}</p></div>', unsafe_allow_html=True)
    mem = sum(df.memory_usage()) / 1024**2
    c3.markdown(f'<div class="stat-card"><p class="stat-label">Mem Payload</p><p class="stat-value">{mem:.2f} MB</p></div>', unsafe_allow_html=True)
    
    st.write("#### 📄 Data Stream Preview")
    st.dataframe(df.head(15), use_container_width=True)
    
    st.write("#### 🧩 Logical Structure")
    st.code(df.dtypes)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 2: Refining Studio ---
elif menu_choice == "Refining Studio":
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.write("### 🧹 Data Refining & Integrity")
    
    tab1, tab2, tab3 = st.tabs(["NULL SCRUBBER", "DUPLICATE REMOVAL", "EXPORT NODE"])
    
    with tab1:
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            st.warning(f"Integrity Breach: {len(missing)} columns have null values.")
            col_to_fix = st.selectbox("Assign target column:", missing.index)
            method = st.radio("Resolution Strategy:", ["Delete Records", "Median Imputation", "Zero Init", "Constant Fill"])
            
            if st.button("Execute Integrity Fix"):
                if method == "Delete Records": st.session_state.df = df.dropna(subset=[col_to_fix])
                elif method == "Zero Init": st.session_state.df[col_to_fix] = df[col_to_fix].fillna(0)
                st.success("Refinement Complete.")
                st.rerun()
        else:
            st.success("✅ Dataset Integrity Confirmed. No null values detected.")

    with tab2:
        dupes = df.duplicated().sum()
        if dupes > 0:
            st.markdown(f"**Duplicate Redundancy:** {dupes} rows found.")
            if st.button("Purge Duplicates"):
                st.session_state.df = df.drop_duplicates()
                st.rerun()
        else:
            st.success("✅ Efficiency Confirmed. No duplicate records.")

    with tab3:
        st.download_button("DOWNLOAD REFINED CSV", convert_to_csv(df), "refined_data.csv", "text/csv")
    st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 3: Statistical Engine ---
elif menu_choice == "Statistical Engine":
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.write("### 🧪 Deep Statistical Scans")
    
    num_df = df.select_dtypes(include=np.number)
    if num_df.empty:
        st.error("No numeric vectors found in stream.")
    else:
        st.write("#### 📐 Geometric Distribution Summary")
        st.dataframe(num_df.describe().T.style.background_gradient(cmap="GnBu"), use_container_width=True)
        
        st.write("#### 🧬 Correlation Topology")
        corr = num_df.corr()
        fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="Viridis", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 4: Visual Deck ---
elif menu_choice == "Visual Deck":
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.write("### 🎨 Visual Visualization Interface")
    
    # Updated to handle potential missing segmented_control in older streamlit versions
    try:
        chart = st.segmented_control("Select Projection Type:", ["BAR", "LINE", "SCATTER", "AREA", "PIE"])
    except:
        chart = st.selectbox("Select Projection Type:", ["BAR", "LINE", "SCATTER", "AREA", "PIE"])
    
    cols = df.columns.tolist()
    c1, c2 = st.columns(2)
    x = c1.selectbox("Source Axis (X):", cols)
    y = c2.selectbox("Measure Axis (Y):", df.select_dtypes(include=np.number).columns.tolist() if not df.select_dtypes(include=np.number).empty else cols)
    
    group = st.selectbox("Group Topology (Color):", ["None"] + [c for c in cols if df[c].nunique() < 20])
    color_map = None if group == "None" else group

    if st.button("GENERATE PROJECTION"):
        if chart == "BAR": fig = px.bar(df, x=x, y=y, color=color_map, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Cyan)
        elif chart == "LINE": fig = px.line(df, x=x, y=y, color=color_map, template="plotly_dark")
        elif chart == "SCATTER": fig = px.scatter(df, x=x, y=y, color=color_map, template="plotly_dark")
        elif chart == "AREA": fig = px.area(df, x=x, y=y, color=color_map, template="plotly_dark")
        else: fig = px.pie(df, names=x, values=y, template="plotly_dark", hole=0.4)
        
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 5: AI Insight Hub ---
elif menu_choice == "AI Insight Hub":
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.write("### 🛸 Automated Intelligence Nodes")
    
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    if not num_cols:
        st.error("Intelligence Engine requires numeric input.")
    else:
        target = st.selectbox("Select target variable:", num_cols)
        data = df[target].dropna()
        
        c1, c2 = st.columns(2)
        c1.info(f"🏔️ **Peak Activation:** {data.max():,}")
        c2.warning(f"🕳️ **Basal Level:** {data.min():,}")
        
        st.write("#### 🧠 Synthetic Analysis")
        avg, med = data.mean(), data.median()
        if abs(avg - med) < (data.std() * 0.1):
            st.success(f"Stability: Data is symmetrically distributed around {avg:.2f}. System suggests high predictability.")
        else:
            skew = "RIGHT (Positively)" if avg > med else "LEFT (Negatively)"
            st.info(f"Anomaly: Distribution is skewed {skew}. Mean ({avg:.2f}) diverges from Median ({med:.2f}).")
            
        fig = px.violin(df, y=target, box=True, points="all", template="plotly_dark", color_discrete_sequence=['#22d3ee'])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <div style="text-align: center; margin-top: 60px; color: #475569; padding-bottom: 20px;">
        Designed & Deployed by Arun Sharma's DataEdge Lab | 2026
    </div>
""", unsafe_allow_html=True)
