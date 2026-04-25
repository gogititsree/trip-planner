import streamlit as st

_CSS = """
<style>
/* ── Layout ───────────────────────────────────────────────────── */
.block-container {
    padding-top: 1.25rem !important;
    padding-bottom: 2rem !important;
}

/* ── Metric cards ─────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e8edf3;
    border-top: 3px solid #E8622A;
    border-radius: 12px;
    padding: 1rem 1.25rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
[data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    opacity: 0.65 !important;
}

/* ── Buttons ──────────────────────────────────────────────────── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 0.35rem 1.1rem !important;
    transition: box-shadow 0.15s ease !important;
}
.stButton > button:hover {
    box-shadow: 0 4px 12px rgba(232, 98, 42, 0.25) !important;
}

/* ── Expanders ────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid #e8edf3 !important;
    border-radius: 10px !important;
    margin-bottom: 6px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    font-weight: 500 !important;
    padding: 0.65rem 1rem !important;
}

/* ── Tabs ─────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #f1f5f9;
    padding: 4px 6px;
    border-radius: 10px;
    gap: 2px;
    border: 1px solid #e8edf3;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 5px 14px !important;
    font-weight: 500 !important;
    color: #64748b !important;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #1E293B !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}

/* ── DataFrames & DataEditor ──────────────────────────────────── */
[data-testid="stDataFrame"] > div,
[data-testid="stDataEditor"] > div {
    border-radius: 10px !important;
    border: 1px solid #e8edf3 !important;
    overflow: hidden !important;
}

/* ── Inputs ───────────────────────────────────────────────────── */
input, textarea, [data-baseweb="select"] > div {
    border-radius: 8px !important;
}

/* ── Progress bar ─────────────────────────────────────────────── */
[data-testid="stProgressBar"] > div > div {
    background: #E8622A !important;
    border-radius: 99px !important;
}
[data-testid="stProgressBar"] > div {
    border-radius: 99px !important;
    background: #f1f5f9 !important;
}

/* ── Divider ──────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid #f1f5f9 !important;
    margin: 1rem 0 !important;
}

/* ── Success / warning / info ─────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
}
</style>
"""


def apply_styles():
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(title: str, route: str, dates: str, badge: str, badge_note: str = ""):
    """Full-width hero banner for the overview page."""
    note_html = f'<span style="margin-left:12px;opacity:0.55;font-size:0.85rem">{badge_note}</span>' if badge_note else ""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a2744 0%, #2d3d5e 100%);
        border-radius: 16px;
        padding: 1.75rem 2.25rem;
        color: white;
        margin-bottom: 1.5rem;
    ">
        <p style="margin:0 0 0.25rem;font-size:0.7rem;letter-spacing:3px;
                  opacity:0.45;text-transform:uppercase">Trip Planner</p>
        <h1 style="margin:0 0 0.4rem;font-size:1.9rem;font-weight:800;
                   color:white;letter-spacing:-0.5px">{title}</h1>
        <p style="margin:0 0 1.25rem;opacity:0.6;font-size:0.9rem">
            {route} &nbsp;·&nbsp; {dates}
        </p>
        <div style="display:inline-flex;align-items:center;
                    background:#E8622A;border-radius:8px;
                    padding:6px 18px;font-size:1.05rem;font-weight:700">
            {badge}
        </div>
        {note_html}
    </div>
    """, unsafe_allow_html=True)


def section_header(icon: str, title: str):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;
                margin-bottom:0.75rem;padding-bottom:0.5rem;
                border-bottom:2px solid #f1f5f9">
        <span style="font-size:1.2rem">{icon}</span>
        <span style="font-size:1rem;font-weight:600;color:#1E293B">{title}</span>
    </div>
    """, unsafe_allow_html=True)
