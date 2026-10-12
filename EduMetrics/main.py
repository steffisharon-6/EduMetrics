import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import os
from pathlib import Path
from functions import load_data, get_class_statistics, get_subject_summaries

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "students.csv"

st.set_page_config(
    page_title="EduMetrics | Orbital Intelligence",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

hero_bg = get_base64_of_bin_file(str(BASE_DIR / 'hero_bg.jpg'))

# ----------------- CSS FOR ORBITAL INTELLIGENCE THEME -----------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Orbitron:wght@400;700;900&display=swap');

    :root {{
        --bg-main: #050711;
        --bg-secondary: #0A0D1C;
        --bg-elevated: #10162A;
        --bg-glass: rgba(20, 25, 52, 0.78);
        
        --color-electric: #A855F7;
        --color-neon: #8B5CF6;
        --color-holo: #60A5FA;
        --color-cyan: #4DEBFF;
        --color-lavender: #D8B4FE;
        --color-warm: #FFBE8A;
        
        --text-primary: #F4F5FF;
        --text-secondary: #A6AEC9;
        
        --status-success: #34D399;
        --status-warn: #FBBF24;
        --status-fail: #FB7185;
        
        --border-glass: rgba(168, 85, 247, 0.2);
        --border-highlight: rgba(168, 85, 247, 0.5);
    }}

    /* Global Base */
    .stApp, [data-testid="stAppViewContainer"] {{
        font-family: 'Inter', sans-serif;
        background-color: #070414 !important;
        background-image: 
            radial-gradient(circle at center, rgba(0, 210, 255, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 20% 80%, rgba(225, 0, 255, 0.05) 0%, transparent 40%) !important;
        background-attachment: fixed;
        color: #FFFFFF !important;
    }}

    header[data-testid="stHeader"] {{ display: none; }}
    
    h1, h2, h3, h4, h5, h6, .hero-title, .hero-label {{
        font-family: 'Orbitron', sans-serif !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
    }}

    /* Sidebar - Violet/Neon glowing active states */
    [data-testid="stSidebar"] {{
        background-color: var(--bg-secondary) !important;
        background-image: linear-gradient(180deg, var(--bg-secondary) 0%, rgba(10, 13, 28, 0.95) 100%) !important;
        border-right: 1px solid rgba(139, 92, 246, 0.15);
        width: 270px !important;
    }}
    
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[data-baseweb="radio"] div:first-child {{ display: none !important; }}
    [data-testid="stSidebar"] div[data-testid="stRadio"] label {{
        padding: 12px 20px;
        border-radius: 8px;
        background: transparent;
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 1.05rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid transparent;
        margin-bottom: 6px;
    }}
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {{
        background: rgba(139, 92, 246, 0.08);
        color: var(--text-primary);
    }}
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] {{
        background: linear-gradient(90deg, rgba(168, 85, 247, 0.15) 0%, rgba(139, 92, 246, 0.05) 100%);
        color: var(--color-lavender);
        border: 1px solid var(--border-glass);
        border-left: 3px solid var(--color-electric);
        box-shadow: inset 2px 0 10px rgba(168, 85, 247, 0.1);
    }}

    /* Glass Panels */
    .glass-panel, [data-testid="metric-container"], [data-testid="stPlotlyChart"], [data-testid="stDataFrame"] {{
        background: var(--bg-glass);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 0 20px rgba(139, 92, 246, 0.03);
        padding: 24px;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    
    .glass-panel:hover, [data-testid="metric-container"]:hover {{
        border-color: var(--border-highlight);
        box-shadow: 0 12px 40px rgba(168, 85, 247, 0.2), inset 0 0 30px rgba(139, 92, 246, 0.1);
        transform: translateY(-3px);
    }}

    /* The Hero Section */
    .hero-section {{
        background-color: var(--bg-elevated);
        background-image: linear-gradient(90deg, rgba(5,7,17,0.95) 0%, rgba(5,7,17,0.7) 40%, rgba(5,7,17,0.2) 100%), url("data:image/jpeg;base64,{hero_bg}");
        background-size: cover;
        background-position: center right;
        border-radius: 24px;
        border: 1px solid var(--border-glass);
        box-shadow: 0 15px 50px rgba(0,0,0,0.6), inset 0 0 40px rgba(168, 85, 247, 0.15);
        padding: 50px 40px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        min-height: 380px;
        position: relative;
        overflow: hidden;
    }}
    
    .hero-section::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at 80% 50%, transparent 0%, rgba(5,7,17,0.8) 100%);
        pointer-events: none;
    }}

    .hero-content {{
        position: relative;
        z-index: 2;
        max-width: 50%;
    }}

    .hero-label {{
        color: var(--color-cyan);
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 12px;
        text-shadow: 0 0 10px rgba(77, 235, 255, 0.5);
    }}
    
    .hero-title {{
        font-size: 3.5rem;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 20px;
        color: #FFF;
        text-shadow: 0 4px 20px rgba(0,0,0,0.8);
    }}
    
    .hero-desc {{
        color: var(--text-secondary);
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 30px;
        font-weight: 400;
    }}

    /* Streamlit Native Metric Styling */
    [data-testid="stMetric"] {{
        background: var(--bg-glass);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), inset 0 0 20px rgba(139, 92, 246, 0.03);
        padding: 24px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    
    [data-testid="stMetric"]:hover {{
        border-color: var(--border-highlight);
        box-shadow: 0 12px 40px rgba(168, 85, 247, 0.2), inset 0 0 30px rgba(139, 92, 246, 0.1);
        transform: translateY(-3px);
    }}

    [data-testid="stMetricLabel"] {{
        font-size: 0.85rem !important; 
        text-transform: uppercase; 
        color: #B6B3D1 !important; 
        letter-spacing: 0.1em; 
        font-weight: 600 !important; 
        margin-bottom: 8px;
        justify-content: center;
    }}
    
    [data-testid="stMetricValue"] {{
        font-family: 'Orbitron', sans-serif !important;
        font-size: 2.8rem !important; 
        font-weight: 700 !important; 
        color: #E100FF !important; 
        line-height: 1; 
        text-shadow: 0 2px 10px rgba(225, 0, 255, 0.3);
    }}
    
    [data-testid="stMetricDelta"] {{
        font-size: 0.85rem !important; 
        font-weight: 500 !important;
        margin-top: 8px;
        justify-content: center;
    }}
    
    [data-testid="stMetricDelta"] svg {{
        display: none; /* Hide default up/down arrows if they mess with alignment */
    }}
    
    /* Top Performers Table */
    .top-table {{ width: 100%; border-collapse: separate; border-spacing: 0 8px; font-size: 0.95rem;}}
    .top-table th {{ text-align: left; color: var(--text-secondary); font-weight: 600; padding: 10px 16px; border-bottom: 1px solid rgba(255,255,255,0.05); text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.8rem;}}
    .top-table td {{ padding: 14px 16px; background: rgba(0,0,0,0.2); color: var(--text-primary); font-weight: 500;}}
    .top-table tr td:first-child {{ border-top-left-radius: 8px; border-bottom-left-radius: 8px; }}
    .top-table tr td:last-child {{ border-top-right-radius: 8px; border-bottom-right-radius: 8px; }}
    .top-table tr:hover td {{ background: rgba(139,92,246,0.1); }}
    
    .grade-pill {{ background: rgba(52, 211, 153, 0.15); color: var(--status-success); padding: 4px 12px; border-radius: 12px; font-weight: 700; font-size: 0.85rem; border: 1px solid rgba(52, 211, 153, 0.3); }}
    .grade-pill.fail {{ background: rgba(251, 113, 133, 0.15); color: var(--status-fail); border-color: rgba(251, 113, 133, 0.3); }}
    
    /* Inputs & Buttons (Streamlit Native Overrides) */
    .stTextInput input, .stSelectbox > div[data-baseweb="select"] > div {{
        background-color: var(--bg-elevated) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: var(--text-primary) !important;
        border-radius: 8px !important;
    }}
    .stTextInput input:focus, .stSelectbox > div[data-baseweb="select"] > div:focus-within {{
        border-color: var(--color-electric) !important;
        box-shadow: 0 0 0 2px rgba(168,85,247,0.3) !important;
    }}
    .stButton > button {{
        background: linear-gradient(90deg, var(--color-neon) 0%, var(--color-electric) 100%);
        border: none;
        color: #FFF;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 600;
        padding: 8px 24px;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }}
    .stButton > button:hover {{
        background: linear-gradient(90deg, var(--color-electric) 0%, var(--color-lavender) 100%);
        color: #FFF;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
        transform: translateY(-2px);
    }}
    
    /* Secondary button style for upload/reset in sidebar */
    [data-testid="stSidebar"] .stButton > button {{
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: none;
        color: var(--text-primary);
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(168,85,247,0.15);
        border-color: var(--border-highlight);
    }}
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE & DATA -----------------
if 'df' not in st.session_state:
    df, msg = load_data(str(DATA_PATH))
    st.session_state.df = df
    if df is None:
        st.error(f"Could not load dataset: {msg}")
        st.info("Check that students.csv exists in the same folder as main.py.")

df = st.session_state.df
stats = get_class_statistics(df) if df is not None else None

# (Landing page removed per user request)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("""
<style>
/* Sidebar deep dark */
[data-testid="stSidebar"] {
    background-color: #0A061C !important;
}
/* Style the radio items to look like pills */
div[role="radiogroup"] > label {
    background: transparent;
    padding: 12px 20px;
    border-radius: 30px;
    margin-bottom: 8px;
    transition: all 0.3s ease;
    border: none !important;
}
div[role="radiogroup"] > label:hover {
    background: rgba(255, 0, 229, 0.1);
}
div[role="radiogroup"] > label[data-checked="true"] {
    background: linear-gradient(90deg, #E100FF, #00D2FF) !important;
    box-shadow: 0 0 15px rgba(225, 0, 255, 0.3);
}
div[role="radiogroup"] p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}
/* Hide the actual circle of the radio */
div[role="radiogroup"] > label span[data-baseweb="radio"] {
    display: none !important;
}
/* Adjust layout */
.stRadio > div { gap: 0 !important; }
</style>
<div style="display:flex; align-items:center; gap:12px; margin-bottom: 40px; padding: 10px 0;">
    <div style="width: 35px; height: 35px; background: linear-gradient(135deg, #E100FF, #00D2FF); border-radius: 50%; display:flex; align-items:center; justify-content:center;">
        <span style="color:white; font-size:20px; font-weight:bold;">+</span>
    </div>
    <div style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; font-weight: 700; color: #FFF; letter-spacing: 1px;">Edu<span style="font-weight:400;">Portal</span></div>
</div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 15px 0;'>", unsafe_allow_html=True)
    
    page = st.radio("Navigation", [
        "🏠 Dashboard", 
        "👥 Students", 
        "📚 Modules", 
        "📊 Analytics", 
        "⚙️ Settings"
    ], label_visibility="collapsed")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if df is not None:
        st.markdown(f"""
            <div style="background: rgba(16, 22, 42, 0.6); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 12px; margin-bottom: 20px;">
                <div style="font-size:0.75rem; color:var(--text-secondary); text-transform:uppercase; margin-bottom:4px;">Dataset Status</div>
                <div style="display:flex; align-items:center; gap:8px; font-weight:600; color:var(--status-success); font-size:0.9rem;">
                    <div style="width:8px; height:8px; background:var(--status-success); border-radius:50%; box-shadow: 0 0 8px var(--status-success);"></div>
                    {stats['total_students']} Records Active
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.caption("DATASET CONTROLS")
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'], label_visibility="collapsed")
    if uploaded_file is not None:
        new_df, msg = load_data(uploaded_file)
        if new_df is not None:
            st.session_state.df = new_df
            st.rerun()
            
    if st.button("↻ Restore Default Data", use_container_width=True):
        st.session_state.df, _ = load_data(str(DATA_PATH))
        st.rerun()

# ----------------- ROUTING -----------------
if df is None or df.empty:
    st.warning("No dataset loaded. Please upload a CSV file.")
    st.stop()

if page == "🏠 Dashboard":
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@400;600;700&display=swap');
/* Removed duplicated global background styling to avoid conflicts */
.dash-container { font-family: 'Inter', sans-serif; color: #FFFFFF; }
.dash-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.dash-title { font-family: 'Orbitron', sans-serif; font-size: 2rem; font-weight: 700; letter-spacing: 2px; }
.header-actions { display: flex; gap: 15px; align-items: center; }
.bell-icon { width: 45px; height: 45px; border-radius: 50%; background: #161238; display: flex; align-items: center; justify-content: center; color: #E100FF; border: 1px solid rgba(225,0,255,0.3); font-size: 20px;}
.add-student-btn { background: linear-gradient(90deg, #E100FF, #FF007A); border: none; border-radius: 25px; padding: 12px 25px; color: white; font-weight: 700; font-family: 'Orbitron', sans-serif; letter-spacing: 1px; cursor: pointer; box-shadow: 0 0 15px rgba(225,0,255,0.4); }
.top-cards { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 30px; }
.t-card { background: #161238; border-radius: 16px; padding: 25px; position: relative; overflow: hidden; border: 1px solid rgba(255,255,255,0.05); }
.t-val { font-size: 2.5rem; font-weight: 700; font-family: 'Orbitron', sans-serif; color: #E100FF; margin-bottom: 5px; display:flex; align-items:flex-end; gap:10px; }
.t-val-sub { font-size: 0.8rem; font-family: 'Inter', sans-serif; color: #8A85B3; font-weight: 400; margin-bottom: 12px; line-height: 1.2;}
.t-label { font-size: 1rem; color: #B6B3D1; font-weight: 600; }
.t-icon { position: absolute; right: 25px; bottom: 25px; width: 35px; height: 35px; background: #E100FF; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 16px;}
.mid-section { display: grid; grid-template-columns: 1fr 2fr; gap: 20px; margin-bottom: 30px; }
.retention-card { background: #161238; border-radius: 16px; padding: 30px; border: 1px solid rgba(255,255,255,0.05); }
.card-title { font-family: 'Orbitron', sans-serif; font-size: 1.2rem; letter-spacing: 1px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;}
.retention-content { display: flex; align-items: center; gap: 30px; margin-bottom: 30px;}
.donut-wrapper { position: relative; width: 130px; height: 130px; }
.donut-ring { width: 130px; height: 130px; border-radius: 50%; background: conic-gradient(#00D2FF 0%, #E100FF 66%, #2E2559 66% 100%); display: flex; align-items: center; justify-content: center; }
.donut-inner { width: 100px; height: 100px; background: #161238; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.6rem; font-family: 'Orbitron', sans-serif; color: #E100FF; }
.donut-dot { position: absolute; left: 5px; top: 75px; width:16px; height:16px; background:#E100FF; border-radius:50%; box-shadow: 0 0 10px #E100FF; border: 3px solid #161238; }
.retention-stats { flex: 1; }
.r-delta { color: #00FFB2; font-size: 0.85rem; margin-bottom: 8px; font-weight: 600;}
.r-label { font-size: 1.1rem; color: #FFFFFF; font-weight: 600; line-height: 1.4;}
.r-info { background: #1B1745; padding: 15px; border-radius: 12px; display: flex; gap: 12px; align-items: center; font-size: 0.85rem; color: #B6B3D1; border-left: 3px solid #E100FF; }
.r-info-icon { color:#E100FF; font-weight:bold; font-size:14px; min-width: 24px; height:24px; border-radius:50%; background:rgba(225,0,255,0.2); display:flex; align-items:center; justify-content:center; }
.students-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.s-card { background: #1B1745; border-radius: 16px; padding: 20px; border: 1px solid rgba(255,255,255,0.03); }
.s-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.s-avatar-name { display: flex; align-items: center; gap: 15px; }
.s-avatar { width: 35px; height: 35px; border-radius: 50%; background: #E100FF; background-size: cover; border: 2px solid #161238;}
.s-name { font-size: 1rem; font-weight: 600; color: #FFFFFF;}
.s-grade { font-size: 0.8rem; color: #E100FF; font-weight: 700; font-family: 'Orbitron', sans-serif; letter-spacing: 1px; }
.s-stats { display: flex; justify-content: space-between; font-size: 0.85rem; color: #8A85B3; }
.s-stats-val { color: #E100FF; font-family: 'Orbitron', sans-serif; font-size: 1.1rem; margin-right: 5px;}
.modules-section { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.m-card { background: linear-gradient(135deg, #1B1745 0%, #161238 100%); border-radius: 16px; padding: 25px; border: 1px solid rgba(255,255,255,0.05); position: relative;}
.m-title-sm { font-size: 0.9rem; color: #8A85B3; margin-bottom: 8px; }
.m-title-main { font-family: 'Orbitron', sans-serif; font-size: 1.1rem; color: #E100FF; letter-spacing: 1px; margin-bottom: 25px; text-transform: uppercase;}
.m-stats { display: flex; justify-content: space-between; padding-right: 20px;}
.m-stat-box { display: flex; flex-direction: column; gap: 5px;}
.m-stat-v { font-family: 'Orbitron', sans-serif; font-size: 1.3rem; color: #FFFFFF;}
.m-stat-l { font-size: 0.85rem; color: #8A85B3; font-weight: 600;}
.m-arrow { position: absolute; right: 25px; top: 40px; color: #E100FF; font-size: 1.8rem; font-weight: 900;}
.view-all { font-family: 'Orbitron', sans-serif; font-size: 0.9rem; color: #E100FF; letter-spacing: 1px; cursor: pointer; font-weight: 700;}
/* Star Background */
.stars { position: fixed; top:0; left:0; width:100%; height:100%; z-index: -1; pointer-events: none; }
.star { position: absolute; width: 3px; height: 3px; background: #00D2FF; border-radius: 50%; box-shadow: 0 0 5px #00D2FF; opacity: 0.5; }
</style>
<!-- Stars -->
<div class="stars">
    <div class="star" style="top: 10%; left: 20%;"></div>
    <div class="star" style="top: 30%; left: 80%;"></div>
    <div class="star" style="top: 60%; left: 40%;"></div>
    <div class="star" style="top: 80%; left: 70%; background: #E100FF; box-shadow: 0 0 5px #E100FF;"></div>
    <div class="star" style="top: 40%; left: 10%; background: #E100FF; box-shadow: 0 0 5px #E100FF;"></div>
    <div class="star" style="top: 20%; left: 50%;"></div>
    <div class="star" style="top: 90%; left: 20%;"></div>
</div>
<div class="dash-container" style="padding-top: 0; background: transparent;">
"""
    , unsafe_allow_html=True)
    
    # --- DASHBOARD HEADER ---
    dash_col1, dash_col2 = st.columns([6, 1])
    with dash_col1:
        st.markdown('<div class="dash-title" style="margin-top:0px; margin-bottom: 25px;">DASHBOARD</div>', unsafe_allow_html=True)
    with dash_col2:
        if st.button("➕ ADD STUDENT", type="primary", use_container_width=True):
            st.session_state.show_add_student = not st.session_state.get('show_add_student', False)
            
    if st.session_state.get('show_add_student', False):
        st.markdown('<div class="glass-panel" style="margin-bottom: 25px;">', unsafe_allow_html=True)
        st.subheader("Enroll New Student")
        with st.form("enroll_student"):
            c1, c2, c3 = st.columns(3)
            s_name = c1.text_input("Full Name")
            s_id = c2.text_input("Student ID")
            s_dept = c3.selectbox("Department", ["Computer Science", "Information Technology", "Business Administration", "Mechanical Engineering", "Electrical Engineering", "Civil Engineering"])
            
            st.markdown("**Subject Scores (0-100)**")
            s1, s2, s3, s4, s5, s6 = st.columns(6)
            m1 = s1.number_input("23CB1601-CC", 0, 100, 0)
            m2 = s2.number_input("23CB1602-HRM", 0, 100, 0)
            m3 = s3.number_input("23CS1501-FSD", 0, 100, 0)
            m4 = s4.number_input("23CS1503-AIML", 0, 100, 0)
            m5 = s5.number_input("23CS1602-CD", 0, 100, 0)
            m6 = s6.number_input("23AD1918-BA", 0, 100, 0)
            
            if st.form_submit_button("Submit Record", type="primary"):
                if s_name and s_id:
                    new_row = {
                        'Student_ID': s_id, 'Name': s_name, 'Department': s_dept,
                        '23CB1601-CC': m1, '23CB1602-HRM': m2, '23CS1501-FSD': m3,
                        '23CS1503-AIML': m4, '23CS1602-CD': m5, '23AD1918-BA/23IT1909-EH': m6
                    }
                    temp = pd.DataFrame([new_row])
                    total = sum([m1, m2, m3, m4, m5, m6])
                    avg = round(total / 6, 1)
                    temp['Total Marks'] = total
                    temp['Average Marks'] = avg
                    
                    from functions import assign_grades, determine_pass_fail
                    temp['Grade'] = temp['Average Marks'].apply(assign_grades)
                    temp['Result Status'] = temp.apply(determine_pass_fail, axis=1)
                    temp['Attendance (%)'] = 85.0
                    temp['Attendance_Is_Simulated'] = True
                    
                    st.session_state.df = pd.concat([st.session_state.df, temp], ignore_index=True)
                    st.session_state.df['Rank'] = st.session_state.df['Total Marks'].rank(method='min', ascending=False).astype(int)
                    st.session_state.show_add_student = False
                    st.rerun()
                else:
                    st.error("Name and Student ID are required.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    total_stu = len(df) if df is not None else 0
    pass_pct = f"{(df['Result Status'] == 'Pass').mean() * 100:.1f}%" if df is not None and not df.empty else "0%"
    top_stu = len(df[df['Grade'] == 'A+']) if df is not None and not df.empty else 0

    st.markdown(f"""
    <div class="top-cards">
        <div class="t-card">
            <div class="t-val">{total_stu}</div>
            <div class="t-label">Total students</div>
            <div class="t-icon">👥</div>
        </div>
        <div class="t-card">
            <div class="t-val">{pass_pct}</div>
            <div class="t-label">Overall Pass Rate</div>
            <div class="t-icon">📖</div>
        </div>
        <div class="t-card">
            <div class="t-val">{top_stu} <span class="t-val-sub">students achieved<br>A+ Grade</span></div>
            <div class="t-label">Top Performers</div>
            <div class="t-icon">⚡</div>
        </div>
    </div>
    <div class="mid-section">
        <div class="retention-card">
            <div class="card-title">RETENTION METRICS</div>
            <div class="retention-content">
                <div class="donut-wrapper">
                    <div class="donut-ring">
                        <div class="donut-inner">66%</div>
                    </div>
                    <div class="donut-dot"></div>
                </div>
                <div class="retention-stats">
                    <div class="r-delta">+4% vs last week</div>
                    <div class="r-label">Students<br>engagement rate</div>
                </div>
            </div>
            <div class="r-info">
                <div class="r-info-icon">i</div>
                <div>Based on lessons actively engaged with over last week</div>
            </div>
        </div>
        <div>
            <div class="card-title" style="margin-bottom: 25px;">
                <span>STUDENTS</span>
                <span class="view-all" onclick="alert('Navigate to the Students tab on the sidebar to view all students.')">VIEW ALL</span>
            </div>
            <div class="students-grid">
                <div class="s-card">
                    <div class="s-header">
                        <div class="s-avatar-name"><div class="s-avatar" style="background-image: url('https://i.pravatar.cc/100?img=1');"></div><div class="s-name">Kinsley Harrell</div></div>
                        <div class="s-grade">12 Grade</div>
                    </div>
                    <div class="s-stats">
                        <div><span class="s-stats-val">5</span> Module</div>
                        <div><span class="s-stats-val">41</span> Lessons</div>
                    </div>
                </div>
                <div class="s-card">
                    <div class="s-header">
                        <div class="s-avatar-name"><div class="s-avatar" style="background-image: url('https://i.pravatar.cc/100?img=2');"></div><div class="s-name">Maxwell Thompson</div></div>
                        <div class="s-grade">9 Grade</div>
                    </div>
                    <div class="s-stats">
                        <div><span class="s-stats-val">3</span> Module</div>
                        <div><span class="s-stats-val">23</span> Lessons</div>
                    </div>
                </div>
                <div class="s-card">
                    <div class="s-header">
                        <div class="s-avatar-name"><div class="s-avatar" style="background-image: url('https://i.pravatar.cc/100?img=3');"></div><div class="s-name">Livia Rosales</div></div>
                        <div class="s-grade">8 Grade</div>
                    </div>
                    <div class="s-stats">
                        <div><span class="s-stats-val">2</span> Module</div>
                        <div><span class="s-stats-val">9</span> Lessons</div>
                    </div>
                </div>
                <div class="s-card">
                    <div class="s-header">
                        <div class="s-avatar-name"><div class="s-avatar" style="background-image: url('https://i.pravatar.cc/100?img=4');"></div><div class="s-name">Jaquan Kenter</div></div>
                        <div class="s-grade">5 Grade</div>
                    </div>
                    <div class="s-stats">
                        <div><span class="s-stats-val">1</span> Module</div>
                        <div><span class="s-stats-val">3</span> Lessons</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="card-title" style="margin-bottom: 25px; margin-top: 10px;">
        <span>MODULES</span>
        <span class="view-all" onclick="alert('Navigate to the Modules tab to view all modules.')">VIEW ALL</span>
    </div>
    <div class="modules-section">
        <div class="m-card">
            <div class="m-arrow">➔</div>
            <div class="m-title-sm">Module 1</div>
            <div class="m-title-main">HIGH-FREQUENCY FOUNDATIONS</div>
            <div class="m-stats">
                <div class="m-stat-box"><div class="m-stat-v">10</div><div class="m-stat-l">Lessons</div></div>
                <div class="m-stat-box"><div class="m-stat-v">18</div><div class="m-stat-l">Students</div></div>
                <div class="m-stat-box"><div class="m-stat-v">1-2</div><div class="m-stat-l">Weeks</div></div>
                <div class="m-stat-box"><div class="m-stat-v">1-2</div><div class="m-stat-l">Grades</div></div>
            </div>
        </div>
        <div class="m-card">
            <div class="m-arrow">➔</div>
            <div class="m-title-sm">Module 2</div>
            <div class="m-title-main">DIGRAPHS + EARLY MULTISYLLABIC</div>
            <div class="m-stats">
                <div class="m-stat-box"><div class="m-stat-v">8</div><div class="m-stat-l">Lessons</div></div>
                <div class="m-stat-box"><div class="m-stat-v">18</div><div class="m-stat-l">Students</div></div>
                <div class="m-stat-box"><div class="m-stat-v">3-4</div><div class="m-stat-l">Weeks</div></div>
                <div class="m-stat-box"><div class="m-stat-v">3-4</div><div class="m-stat-l">Grades</div></div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

elif page == "👥 Students":
    st.markdown('<div class="hero-label">STUDENT DIRECTORY</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Student Explorer</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    search = c1.text_input("Search (Name/ID)")
    dept = c2.selectbox("Filter Dept", ["All"] + list(df['Department'].unique()))
    grade_filter = c3.selectbox("Filter Grade", ["All"] + list(df['Grade'].unique()))
    status = c4.selectbox("Filter Status", ["All", "Pass", "Fail", "Absent"])
    
    view_df = df.copy()
    if search: view_df = view_df[view_df['Name'].astype(str).str.contains(search, case=False) | view_df['Student_ID'].astype(str).str.contains(search, case=False)]
    if dept != "All": view_df = view_df[view_df['Department'] == dept]
    if grade_filter != "All": view_df = view_df[view_df['Grade'] == grade_filter]
    if status != "All": view_df = view_df[view_df['Result Status'] == status]
    
    # (Avatar column generation removed from table per user request)

    c_sort, _ = st.columns([1, 3])
    with c_sort:
        sort_by = st.selectbox("Sort By", ["Student_ID", "Name", "Average Marks", "Total Marks", "Rank"], index=["Student_ID", "Name", "Average Marks", "Total Marks", "Rank"].index(st.session_state.get('default_sort', 'Student_ID')))
    view_df = view_df.sort_values(sort_by, ascending=(sort_by in ["Student_ID", "Name", "Rank"]))
    
    # Add sequential S.No column
    view_df.insert(0, 'S.No', range(1, len(view_df) + 1))
    st.write(f"Showing **{len(view_df)}** students")
    
    def color_status(val):
        if val == 'Pass': return 'color: #34D399; font-weight:700'
        if val == 'Fail': return 'color: #FB7185; font-weight:700'
        if val == 'Absent': return 'color: #FBBF24; font-weight:700'
        return ''
        
    format_cols = ['23CB1601-CC', '23CB1602-HRM', '23CS1501-FSD', '23CS1503-AIML', '23CS1602-CD', '23AD1918-BA/23IT1909-EH', 'Total Marks', 'Average Marks', 'Attendance (%)']
    
    col_config = {}
    for col in format_cols:
        if col in view_df.columns:
            col_config[col] = st.column_config.NumberColumn(col, format="%.1f")
            
    st.dataframe(
        view_df.style.map(color_status, subset=['Result Status']), 
        use_container_width=True, 
        height=400,
        column_config=col_config,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    st.markdown('<div class="hero-label">INDIVIDUAL PROFILE</div>', unsafe_allow_html=True)
    student_sel = st.selectbox("Select a student to view detailed profile", ["Select..."] + list(view_df['Student_ID'].astype(str) + " - " + view_df['Name'].astype(str)))
    if student_sel != "Select...":
        sid = student_sel.split(" - ")[0]
        s = df[df['Student_ID'].astype(str) == sid].iloc[0]
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        
        a_num = (hash(str(sid)) % 3) + 1
        b64 = get_base64_of_bin_file(str(BASE_DIR / 'assets' / 'student_avatars' / f'avatar_00{a_num}.jpg'))
        if st.session_state.get('show_avatars', True) and b64:
            img_html = f'<img src="data:image/jpeg;base64,{b64}" style="width:140px; height:140px; border-radius:50%; object-fit:cover; border: 4px solid var(--color-electric); box-shadow: 0 8px 25px rgba(168, 85, 247, 0.4); margin-bottom: 24px; transition: transform 0.3s ease;">'
        else:
            img_html = '<div style="width:140px; height:140px; border-radius:50%; background:var(--bg-elevated); border: 4px solid var(--color-electric); display:flex; align-items:center; justify-content:center; color:var(--text-secondary); font-size:50px; margin-bottom:24px;">👤</div>'
        
        st.markdown(f'''
        <style>
        .profile-img:hover {{ transform: scale(1.05); }}
        </style>
        <div style="text-align:center;" class="profile-img">
            {img_html}
        </div>
        ''', unsafe_allow_html=True)

        pc1, pc2, pc3, pc4 = st.columns(4)
        pc1.metric("Name", s['Name'], str(s['Student_ID']), delta_color="off")
        pc2.metric("Average", f"{s['Average Marks']:.1f}", s['Grade'], delta_color="off")
        pc3.metric("Status", s['Result Status'], f"Rank #{s['Rank']}", delta_color="normal" if s['Result Status']=="Pass" else "inverse")
        
        att_label = "Attendance (Simulated)" if s.get('Attendance_Is_Simulated', False) else "Attendance"
        pc4.metric(att_label, f"{s.get('Attendance (%)', 0):.1f}%", "", delta_color="off")
        st.write("---")
        st.subheader("Subject Marks")
        subj_cols = st.columns(6)
        subjects = ['23CB1601-CC', '23CB1602-HRM', '23CS1501-FSD', '23CS1503-AIML', '23CS1602-CD', '23AD1918-BA/23IT1909-EH']
        for i, subj in enumerate(subjects):
            subj_status = "Pass" if not pd.isna(s[subj]) and s[subj]>=35 else ("Absent" if pd.isna(s[subj]) else "Fail")
            subj_cols[i].metric(subj.split('-')[-1][:6], s[subj] if not pd.isna(s[subj]) else "AB", subj_status, delta_color="normal" if subj_status=="Pass" else "inverse")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "📊 Analytics":
    st.markdown('<div class="hero-label">DEEP INSIGHTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Performance Analytics</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-panel" style="height:100%;">', unsafe_allow_html=True)
        st.subheader("Student Average Distribution")
        fig = px.histogram(df, x='Average Marks', nbins=15, color_discrete_sequence=['#8B5CF6'], text_auto=st.session_state.get('show_chart_labels', False))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A6AEC9', margin=dict(t=20, b=0, l=0, r=0))
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass-panel" style="height:100%;">', unsafe_allow_html=True)
        st.subheader("Department Pass Rates")
        dept_pass = df.groupby('Department').apply(lambda x: (x['Result Status']=='Pass').mean()*100).reset_index(name='Pass %')
        fig2 = px.bar(dept_pass, x='Department', y='Pass %', color='Pass %', color_continuous_scale=['#FB7185', '#34D399'], text_auto='.1f' if st.session_state.get('show_chart_labels', False) else False)
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A6AEC9', margin=dict(t=20, b=0, l=0, r=0), coloraxis_showscale=False)
        fig2.update_yaxes(gridcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Performance Extremes")
    ec1, ec2 = st.columns(2)
    highest_student = df.loc[df['Average Marks'].idxmax()]
    lowest_student = df.loc[df['Average Marks'].idxmin()]
    
    with ec1:
        with st.container(border=True):
            st.metric("Top Student", highest_student['Name'], f"{highest_student['Average Marks']:.1f} Avg", delta_color="normal")
    with ec2:
        with st.container(border=True):
            st.metric("Lowest Student", lowest_student['Name'], f"{lowest_student['Average Marks']:.1f} Avg", delta_color="inverse")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    
    st.markdown('<div class="hero-label">SUBJECT ANALYTICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    subjects = ['23CB1601-CC', '23CB1602-HRM', '23CS1501-FSD', '23CS1503-AIML', '23CS1602-CD', '23AD1918-BA/23IT1909-EH']
    subj_sel = st.selectbox("Select Subject to Analyze", subjects)
    
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Subject Average", f"{df[subj_sel].mean():.1f}", "out of 100", delta_color="off")
    sc2.metric("Highest Mark", f"{df[subj_sel].max():.0f}", f"by {df.loc[df[subj_sel].idxmax()]['Name']}", delta_color="normal")
    sc3.metric("Lowest Mark", f"{df[subj_sel].min():.0f}", f"by {df.loc[df[subj_sel].idxmin()]['Name']}", delta_color="inverse")
    
    fig_sub = px.box(df, x='Department', y=subj_sel, color='Department', title=f"{subj_sel} Distribution by Dept", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_sub.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A6AEC9', margin=dict(t=40, b=0, l=0, r=0))
    st.plotly_chart(fig_sub, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("---")
    
    st.markdown('<div class="hero-label">ATTENDANCE ANALYTICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

    
    ac1, ac2 = st.columns(2)
    with ac1:
        st.subheader("Attendance vs Performance")
        fig_att = px.scatter(df, x='Attendance (%)', y='Average Marks', color='Result Status', hover_data=['Name'], color_discrete_map={'Pass': '#34D399', 'Fail': '#FB7185'})
        fig_att.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A6AEC9', margin=dict(t=20, b=0, l=0, r=0))
        fig_att.update_xaxes(gridcolor='rgba(255,255,255,0.05)')
        fig_att.update_yaxes(gridcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig_att, use_container_width=True)
    with ac2:
        st.subheader("Department Attendance")
        dept_att = df.groupby('Department')['Attendance (%)'].mean().reset_index()
        fig_att2 = px.bar(dept_att, x='Department', y='Attendance (%)', color='Attendance (%)', color_continuous_scale=['#FFBE8A', '#8B5CF6'])
        fig_att2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A6AEC9', margin=dict(t=20, b=0, l=0, r=0), coloraxis_showscale=False)
        fig_att2.update_yaxes(range=[0, 100], gridcolor='rgba(255,255,255,0.05)')
        st.plotly_chart(fig_att2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


elif page == "📚 Modules":
    st.markdown('<div class="hero-label">ACADEMIC INTELLIGENCE / REPORT STUDIO</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Report Studio</div>', unsafe_allow_html=True)
    
    # --- FILTERS ---
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        f_dept = st.selectbox("Department", ["All"] + list(df['Department'].unique()))
    with f2:
        f_grade = st.selectbox("Grade", ["All"] + list(df['Grade'].dropna().unique()))
    with f3:
        f_status = st.selectbox("Status", ["All", "Pass", "Fail"])
    with f4:
        f_search = st.text_input("Search (ID/Name)")
        
    c_btn1, c_btn2 = st.columns([6, 1])
    with c_btn2:
        if st.button("↻ Reset Filters", use_container_width=True):
            st.rerun()

    # Filter Data
    report_df = df.copy()
    if f_dept != "All": report_df = report_df[report_df['Department'] == f_dept]
    if f_grade != "All": report_df = report_df[report_df['Grade'] == f_grade]
    if f_status != "All": report_df = report_df[report_df['Result Status'] == f_status]
    if f_search: report_df = report_df[report_df['Name'].astype(str).str.contains(f_search, case=False) | report_df['Student_ID'].astype(str).str.contains(f_search, case=False)]
    
    st.markdown('</div>', unsafe_allow_html=True)

    # --- SUMMARY CARDS ---
    st.markdown('<div style="display:flex; gap:15px; margin-bottom:20px;">', unsafe_allow_html=True)
    if len(report_df) > 0:
        c_avg = f"{report_df['Average Marks'].mean():.1f}"
        p_pct = f"{(report_df['Result Status'] == 'Pass').mean() * 100:.1f}%"
    else:
        c_avg = "--"
        p_pct = "--"
        
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Students Included", len(report_df))
    s2.metric("Subjects Analyzed", 6)
    s3.metric("Filtered Avg", c_avg)
    s4.metric("Pass Rate", p_pct)
    
    # --- REPORT SELECTION ---
    report_type = st.radio("Select Report Type", ["Complete Student Records", "Subject Performance Summary", "Grade Distribution", "Department Performance"], horizontal=True)
    
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    import io
    import csv
    import zipfile
    from fpdf import FPDF
    
    # Generates preview and CSV
    csv_data = None
    csv_filename = ""
    
    if report_type == "Complete Student Records":
        st.subheader(f"Preview: Student Records ({len(report_df)} rows)")
        st.dataframe(report_df, use_container_width=True, hide_index=True)
        csv_data = report_df.to_csv(index=False).encode('utf-8')
        csv_filename = "edumetrics_student_records.csv"
        
    elif report_type == "Subject Performance Summary":
        st.subheader("Preview: Subject Performance Summary")
        if len(report_df) > 0:
            subj_means = get_subject_summaries(report_df)
            subj_df = pd.DataFrame(list(subj_means.items()), columns=['Subject', 'Average Mark']).round(1)
            st.dataframe(subj_df, use_container_width=True, hide_index=True)
            
            fig = px.bar(subj_df, x='Subject', y='Average Mark', color='Average Mark', color_continuous_scale=['#00D2FF', '#E100FF'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A6AEC9')
            st.plotly_chart(fig, use_container_width=True)
            
            csv_data = subj_df.to_csv(index=False).encode('utf-8')
        else:
            st.info("No data available for the current filters.")
        csv_filename = "edumetrics_subject_summary.csv"
        
    elif report_type == "Grade Distribution":
        st.subheader("Preview: Grade Distribution")
        if len(report_df) > 0:
            grade_df = report_df['Grade'].value_counts().reset_index()
            grade_df.columns = ['Grade', 'Count']
            grade_df['Percentage'] = (grade_df['Count'] / len(report_df) * 100).round(1).astype(str) + '%'
            st.dataframe(grade_df, use_container_width=True, hide_index=True)
            
            fig = px.pie(grade_df, values='Count', names='Grade', hole=0.4, color_discrete_sequence=px.colors.sequential.Purp)
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A6AEC9')
            st.plotly_chart(fig, use_container_width=True)
            
            csv_data = grade_df.to_csv(index=False).encode('utf-8')
        else:
            st.info("No data available for the current filters.")
        csv_filename = "edumetrics_grade_distribution.csv"
        
    elif report_type == "Department Performance":
        st.subheader("Preview: Department Performance")
        if len(report_df) > 0:
            dept_df = report_df.groupby('Department').agg(
                Student_Count=('Student_ID', 'count'),
                Average_Marks=('Average Marks', 'mean'),
                Pass_Rate_Pct=('Result Status', lambda x: (x == 'Pass').mean() * 100)
            ).reset_index().round(1)
            st.dataframe(dept_df, use_container_width=True, hide_index=True)
            
            fig = px.bar(dept_df, x='Department', y='Average_Marks', color='Pass_Rate_Pct', color_continuous_scale=['#FB7185', '#34D399'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A6AEC9')
            st.plotly_chart(fig, use_container_width=True)
            
            csv_data = dept_df.to_csv(index=False).encode('utf-8')
        else:
            st.info("No data available for the current filters.")
        csv_filename = "edumetrics_department_performance.csv"
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- EXPORT CENTER ---
    st.markdown('<div class="hero-label">EXPORT CENTER</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    e1, e2, e3 = st.columns(3)
    
    # 1. Download Current Report
    with e1:
        st.subheader("Current View")
        st.write("Export the currently selected and filtered report above as a CSV dataset.")
        if csv_data:
            st.download_button("📥 Download CSV", csv_data, csv_filename, "text/csv", use_container_width=True)
        else:
            st.button("📥 Download CSV", disabled=True, use_container_width=True)
            
    # 2. Download PDF Executive Summary
    with e2:
        st.subheader("Executive Summary")
        st.write("Generate a professional, printable PDF report containing high-level insights for the current selection.")
        
        def generate_pdf(r_df):
            pdf = FPDF()
            pdf.add_page()
            
            # Draw a beautiful header background rectangle using RGB
            pdf.set_fill_color(7, 4, 20)
            pdf.rect(0, 0, 210, 40, 'F')
            
            # Title
            pdf.set_font("Helvetica", 'B', 24)
            pdf.set_text_color(225, 0, 255) # Electric Magenta
            pdf.cell(0, 20, "EduMetrics Report Studio", ln=True, align='C')
            
            pdf.set_font("Helvetica", 'I', 10)
            pdf.set_text_color(255, 255, 255)
            import datetime
            pdf.cell(0, 5, f"Executive Summary - Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
            pdf.ln(15)
            
            # Reset text color for body
            pdf.set_text_color(30, 30, 30)
            
            if len(r_df) == 0:
                pdf.set_font("Helvetica", 'B', 12)
                pdf.cell(0, 10, "No records found for the selected filters.", ln=True, align='C')
                # Need to use latin1 to encode it properly without byte issues
                return bytes(pdf.output(dest='S'))
                
            pdf.set_font("Helvetica", 'B', 14)
            pdf.set_text_color(7, 4, 20)
            pdf.cell(0, 10, "1. Academic Overview", ln=True)
            pdf.set_font("Helvetica", '', 11)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(0, 8, f"- Students Included: {len(r_df)}", ln=True)
            pdf.cell(0, 8, f"- Overall Class Average: {r_df['Average Marks'].mean():.1f} / 100", ln=True)
            pdf.cell(0, 8, f"- Overall Pass Rate: {(r_df['Result Status'] == 'Pass').mean()*100:.1f}%", ln=True)
            pdf.ln(8)
            
            pdf.set_font("Helvetica", 'B', 14)
            pdf.set_text_color(7, 4, 20)
            pdf.cell(0, 10, "2. Grade Distribution", ln=True)
            pdf.set_font("Helvetica", '', 11)
            pdf.set_text_color(50, 50, 50)
            grades = r_df['Grade'].value_counts()
            for g, count in grades.items():
                pdf.cell(0, 8, f"  Grade {g}: {count} students ({(count/len(r_df)*100):.1f}%)", ln=True)
            pdf.ln(8)
            
            pdf.set_font("Helvetica", 'B', 14)
            pdf.set_text_color(7, 4, 20)
            pdf.cell(0, 10, "3. Department Performance", ln=True)
            pdf.set_font("Helvetica", '', 11)
            pdf.set_text_color(50, 50, 50)
            depts = r_df.groupby('Department').agg(Avg=('Average Marks', 'mean'), PassRate=('Result Status', lambda x: (x=='Pass').mean()*100))
            for dept, row in depts.iterrows():
                pdf.cell(0, 8, f"  {dept} - Average Marks: {row['Avg']:.1f}, Pass Rate: {row['PassRate']:.1f}%", ln=True)
                
            pdf.ln(15)
            pdf.set_font("Helvetica", 'I', 9)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 10, "Note: Attendance figures may be simulated if source data lacked them.", ln=True, align='C')
            
            return bytes(pdf.output(dest='S'))
            
        pdf_bytes = generate_pdf(report_df)
        if len(report_df) > 0:
            st.download_button("📄 Download PDF", pdf_bytes, "edumetrics_executive_summary.pdf", "application/pdf", use_container_width=True)
        else:
            st.button("📄 Download PDF", disabled=True, use_container_width=True)

    # 3. Download All as ZIP
    with e3:
        st.subheader("Complete Package")
        st.write("Download a ZIP archive containing all datasets, departmental metrics, and the PDF executive summary.")
        def generate_zip(r_df):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                # 1. Students
                zf.writestr("students_records.csv", r_df.to_csv(index=False))
                
                if len(r_df) > 0:
                    # 2. Subjects
                    subj = pd.DataFrame(list(get_subject_summaries(r_df).items()), columns=['Subject', 'Avg'])
                    zf.writestr("subject_summary.csv", subj.to_csv(index=False))
                    
                    # 3. Grades
                    gr = r_df['Grade'].value_counts().reset_index()
                    gr.columns = ['Grade', 'Count']
                    zf.writestr("grade_distribution.csv", gr.to_csv(index=False))
                    
                    # 4. Depts
                    dept = r_df.groupby('Department').agg(
                        Average_Marks=('Average Marks', 'mean')
                    ).reset_index()
                    zf.writestr("department_performance.csv", dept.to_csv(index=False))
                
                # PDF
                zf.writestr("executive_summary.pdf", generate_pdf(r_df))
                
            return zip_buffer.getvalue()
            
        zip_bytes = generate_zip(report_df)
        st.download_button("📦 Download All (ZIP)", zip_bytes, "edumetrics_full_report.zip", "application/zip", use_container_width=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "⚙️ Settings":
    import sys
    import streamlit as st_core
    
    st.markdown('<div class="hero-label">SYSTEM CONFIGURATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Settings</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#A6AEC9; margin-bottom:30px; font-size:1.1rem;">Personalize your workspace and manage your academic data.</p>', unsafe_allow_html=True)
    
    # System Status Indicator
    status_color = "#34D399" if df is not None and not df.empty else "#FB7185"
    status_text = "System Online &bull; Dataset Active" if df is not None and not df.empty else "System Warning &bull; No Data"
    st.markdown(f'''
    <div style="display:inline-flex; align-items:center; gap:10px; background:rgba(20,25,52,0.8); padding:8px 16px; border-radius:20px; border:1px solid rgba(255,255,255,0.05); margin-bottom:30px;">
        <div style="width:10px; height:10px; background:{status_color}; border-radius:50%; box-shadow: 0 0 10px {status_color};"></div>
        <span style="color:#F4F5FF; font-weight:600; font-size:0.9rem;">{status_text}</span>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-panel" style="height:100%;">', unsafe_allow_html=True)
        st.subheader("Appearance & Display")
        
        show_avatars = st.checkbox("Show AI Avatars in Student Profiles", value=st.session_state.get('show_avatars', True))
        if show_avatars != st.session_state.get('show_avatars', True):
            st.session_state.show_avatars = show_avatars
            st.rerun()
            
        show_chart_labels = st.checkbox("Show Data Labels on Charts", value=st.session_state.get('show_chart_labels', False))
        if show_chart_labels != st.session_state.get('show_chart_labels', False):
            st.session_state.show_chart_labels = show_chart_labels
            st.rerun()
            
        st.info("Visual preferences are saved in your current session state and apply instantly across all pages.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="glass-panel" style="height:100%;">', unsafe_allow_html=True)
        st.subheader("Analytics Preferences")
        
        def_sort = st.selectbox("Default Student Sorting", ["Student_ID", "Name", "Average Marks", "Rank", "Total Marks"], index=["Student_ID", "Name", "Average Marks", "Rank", "Total Marks"].index(st.session_state.get('default_sort', 'Student_ID')))
        if def_sort != st.session_state.get('default_sort', 'Student_ID'):
            st.session_state.default_sort = def_sort
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.write("")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="glass-panel" style="height:100%;">', unsafe_allow_html=True)
        st.subheader("Data & Application")
        
        st.markdown(f"**Current Dataset:** `students.csv`")
        if df is not None:
            st.markdown(f"**Records:** {len(df)}")
            st.markdown(f"**Subjects Assessed:** 6")
            st.markdown(f"**Status:** Validated & Active")
        else:
            st.markdown(f"**Status:** Disconnected")
            
        st.write("---")
        
        # Factory reset with confirmation
        if 'confirm_reset' not in st.session_state:
            st.session_state.confirm_reset = False
            
        if not st.session_state.confirm_reset:
            if st.button("↻ Factory Reset", type="primary"):
                st.session_state.confirm_reset = True
                st.rerun()
        else:
            st.warning("⚠️ This will reload default data from `students.csv` and reset all display preferences. Your source files will NOT be modified. Proceed?")
            rc1, rc2 = st.columns(2)
            with rc1:
                if st.button("Yes, Reset System", use_container_width=True):
                    st.session_state.df, _ = load_data(str(DATA_PATH))
                    st.session_state.show_avatars = True
                    st.session_state.show_chart_labels = False
                    st.session_state.default_sort = 'Student_ID'
                    st.session_state.confirm_reset = False
                    st.rerun()
            with rc2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.confirm_reset = False
                    st.rerun()
                    
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="glass-panel" style="height:100%;">', unsafe_allow_html=True)
        st.subheader("System Information")
        st.markdown(f"**App Name:** EduMetrics Academic Portal")
        st.markdown(f"**Version:** 2.1.0")
        st.markdown(f"**Python Runtime:** {sys.version.split()[0]}")
        st.markdown(f"**Streamlit Engine:** {st_core.__version__}")
        st.markdown(f"**Configured Modules:** 5")
        st.markdown('</div>', unsafe_allow_html=True)
