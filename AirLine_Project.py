import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="Airline Analytics Dashboard", layout="wide", page_icon="✈️")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background-color: #0d1117; }
    .stApp { background-color: #0d1117; color: #e6edf3; }

    .metric-card {
        background: linear-gradient(135deg, #161b22, #1c2333);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-label { font-size: 13px; color: #8b949e; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; }
    .metric-value { font-size: 32px; font-weight: 700; color: #58a6ff; margin-top: 6px; }

    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #e6edf3;
        border-left: 3px solid #58a6ff;
        padding-left: 12px;
        margin-bottom: 16px;
        margin-top: 8px;
    }

    .stSidebar { background-color: #161b22; border-right: 1px solid #30363d; }
    .stSidebar [data-testid="stSidebarNav"] { background-color: #161b22; }

    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #161b22, #1c2333);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 16px;
    }
</style>
""", unsafe_allow_html=True)
# ── Load Data ────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(r"D:\firefox downloads\air data\Airline Dataset Updated - v2.csv")
    df['Departure Date'] = pd.to_datetime(df['Departure Date'], errors='coerce')
    df['Month'] = df['Departure Date'].dt.month_name()
    df['Month_Num'] = df['Departure Date'].dt.month
    return df

df = load_data()

COLORS = {
    "On Time":  "#3fb950",
    "Delayed":  "#f0883e",
    "Cancelled":"#f85149"
}
ACCENT = "#58a6ff"
BG     = "#05295e"
PAPER  = "#0d1117"
FONT   = "#e6edf3"

plotly_theme = dict(
    paper_bgcolor=PAPER,
    plot_bgcolor=BG,
    font=dict(color=FONT, family="Inter"),
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
)

# ── Sidebar Filters ────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/airplane-mode-on.png", width=60)
st.sidebar.title("✈️ Airline Dashboard")
st.sidebar.markdown("---")

page = st.sidebar.radio("📂 Navigate", [
    "🏠 Overview",
    "🌍 Geography",
    "👥 Passenger Demographics",
    "📅 Time Trends",
    "✈️ Flight Status",
    "🛩️ Live Flight Tracker"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Filters")

continents = ["All"] + sorted(df["Continents"].dropna().unique().tolist())
sel_continent = st.sidebar.selectbox("Continent", continents)

statuses = ["All"] + sorted(df["Flight Status"].dropna().unique().tolist())
sel_status = st.sidebar.selectbox("Flight Status", statuses)

age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))

gender_opts = ["All"] + sorted(df["Gender"].dropna().unique().tolist())
sel_gender = st.sidebar.selectbox("Gender", gender_opts)

# ── Apply Filters ──────────────────────────────────────────
fdf = df.copy()
if sel_continent != "All":
    fdf = fdf[fdf["Continents"] == sel_continent]
if sel_status != "All":
    fdf = fdf[fdf["Flight Status"] == sel_status]
if sel_gender != "All":
    fdf = fdf[fdf["Gender"] == sel_gender]
fdf = fdf[(fdf["Age"] >= age_range[0]) & (fdf["Age"] <= age_range[1])]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Showing:** {len(fdf):,} passengers")


# ══════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.title("✈️ Airline Analytics Dashboard")
    st.markdown("Real-time insights across **98,619 passenger records**.")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Passengers", f"{len(fdf):,}")
    with c2:
        on_time = len(fdf[fdf["Flight Status"] == "On Time"])
        st.metric("On Time", f"{on_time:,}", delta=f"{on_time/max(len(fdf),1)*100:.1f}%")
    with c3:
        delayed = len(fdf[fdf["Flight Status"] == "Delayed"])
        st.metric("Delayed", f"{delayed:,}", delta=f"-{delayed/max(len(fdf),1)*100:.1f}%", delta_color="inverse")
    with c4:
        cancelled = len(fdf[fdf["Flight Status"] == "Cancelled"])
        st.metric("Cancelled", f"{cancelled:,}", delta=f"-{cancelled/max(len(fdf),1)*100:.1f}%", delta_color="inverse")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Flight Status Distribution</div>', unsafe_allow_html=True)
        status_counts = fdf["Flight Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig = px.pie(status_counts, names="Status", values="Count",
                     color="Status", color_discrete_map=COLORS, hole=0.5)
        fig.update_layout(**plotly_theme, showlegend=True, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Passengers by Continent</div>', unsafe_allow_html=True)
        cont_counts = fdf["Continents"].value_counts().reset_index()
        cont_counts.columns = ["Continent", "Count"]
        fig2 = px.bar(cont_counts, x="Continent", y="Count",
                      color="Count", color_continuous_scale="Blues",
                      text="Count")
        fig2.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig2.update_layout(**plotly_theme, coloraxis_showscale=False, margin=dict(t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)
