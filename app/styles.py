"""
styles.py
Sistema de diseño Midnight Silver para RelocationDevs.
Inyectar una vez en main.py con inject_styles().
"""

MIDNIGHT_SILVER = {
    "bg_primary":    "#111111",
    "bg_surface":    "#1c1c1e",
    "bg_elevated":   "#2c2c2e",
    "text_primary":  "#f5f5f7",
    "text_secondary":"#aeaeb2",
    "text_tertiary": "#6e6e73",
    "border":        "#3a3a3c",
    "accent":        "#f5f5f7",
}

CSS = """
<style>

/* ── Reset y base ─────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #111111 !important;
    color: #f5f5f7 !important;
}

[data-testid="stApp"] {
    background-color: #111111 !important;
}

/* ── Sidebar ──────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #1c1c1e !important;
    border-right: 1px solid #2c2c2e !important;
}

[data-testid="stSidebar"] * {
    color: #f5f5f7 !important;
}

[data-testid="stSidebarNav"] {
    padding-top: 0 !important;
}

/* ── Tipografía global ────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    color: #f5f5f7 !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
}

p, li, span, div {
    color: #f5f5f7 !important;
}

.stMarkdown p {
    color: #aeaeb2 !important;
    line-height: 1.7 !important;
}

/* ── Métricas ─────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: #1c1c1e !important;
    border: 1px solid #2c2c2e !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    animation: slideUp 0.4s ease both !important;
}

[data-testid="stMetricLabel"] {
    color: #6e6e73 !important;
    font-size: 12px !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    color: #f5f5f7 !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
}

[data-testid="stMetricDelta"] {
    color: #aeaeb2 !important;
}

/* ── Botones ──────────────────────────────────────────── */
.stButton > button {
    background: #f5f5f7 !important;
    color: #111111 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: -0.01em !important;
    padding: 10px 24px !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
}

.stButton > button[kind="secondary"] {
    background: #2c2c2e !important;
    color: #f5f5f7 !important;
    border: 1px solid #3a3a3c !important;
}

/* ── Inputs y selectbox ───────────────────────────────── */
.stSelectbox > div > div,
.stMultiSelect > div > div,
.stTextInput > div > div > input {
    background: #1c1c1e !important;
    color: #f5f5f7 !important;
    border: 1px solid #3a3a3c !important;
    border-radius: 10px !important;
}

.stSelectbox label,
.stMultiSelect label,
.stTextInput label,
.stSlider label {
    color: #aeaeb2 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}

/* ── Slider ───────────────────────────────────────────── */
.stSlider > div > div > div > div {
    background: #f5f5f7 !important;
}

.stSlider [data-testid="stThumbValue"] {
    color: #f5f5f7 !important;
    background: #2c2c2e !important;
}

/* ── Dataframe ────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    background: #1c1c1e !important;
    border: 1px solid #2c2c2e !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Tabs ─────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #1c1c1e !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid #2c2c2e !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6e6e73 !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background: #2c2c2e !important;
    color: #f5f5f7 !important;
}

/* ── Info / Warning / Error ───────────────────────────── */
.stInfo {
    background: #1c1c1e !important;
    border: 1px solid #3a3a3c !important;
    border-radius: 10px !important;
    color: #aeaeb2 !important;
}

.stWarning {
    background: #1c1c1e !important;
    border: 1px solid #3a3a3c !important;
    border-radius: 10px !important;
}

/* ── Divider ──────────────────────────────────────────── */
hr {
    border-color: #2c2c2e !important;
    margin: 24px 0 !important;
}

/* ── Radio buttons ────────────────────────────────────── */
.stRadio > div {
    gap: 8px !important;
}

.stRadio label {
    color: #f5f5f7 !important;
    font-size: 14px !important;
}

/* ── Caption ──────────────────────────────────────────── */
.stCaption {
    color: #6e6e73 !important;
    font-size: 12px !important;
}

/* ── Animaciones ──────────────────────────────────────── */
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-16px); }
    to   { opacity: 1; transform: translateX(0); }
}

.fade-in {
    animation: fadeIn 0.5s ease both;
}

.slide-up {
    animation: slideUp 0.5s ease both;
}

/* Animación escalonada para métricas */
[data-testid="stMetric"]:nth-child(1) { animation-delay: 0.05s !important; }
[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.10s !important; }
[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.15s !important; }
[data-testid="stMetric"]:nth-child(4) { animation-delay: 0.20s !important; }

/* Animación de contenido principal */
[data-testid="stVerticalBlock"] > div {
    animation: fadeIn 0.4s ease both;
}

/* ── Scrollbar ────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #111111; }
::-webkit-scrollbar-thumb { background: #3a3a3c; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #6e6e73; }

/* ── Header oculto de Streamlit ───────────────────────── */
footer {
    display: none !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Botón para abrir barra lateral en ventana estrecha (Streamlit 1.56+) ── */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
.stSidebarCollapsedControl {
    display: flex !important;
    visibility: visible !important;
    background-color: #1c1c1e !important;
    border: 1px solid #3a3a3c !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    margin: 16px !important;
    width: auto !important;
    height: auto !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
    transition: all 0.2s ease !important;
    z-index: 100000 !important;
}

[data-testid="collapsedControl"]:hover {
    background-color: #2c2c2e !important;
    border-color: #6e6e73 !important;
    transform: translateY(-1px) !important;
}

[data-testid="collapsedControl"] svg {
    margin-right: 8px !important;
}

[data-testid="collapsedControl"]::after {
    content: "Abrir menú" !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    color: #f5f5f7 !important;
}

</style>
"""

LOGO_SVG = """<svg width="48" height="48" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="512" height="512" rx="100" fill="#111111"/><path d="M256 60C178.7 60 116 122.7 116 200C116 305 256 452 256 452C256 452 396 305 396 200C396 122.7 333.3 60 256 60Z" stroke="#F5F5F7" stroke-width="20" stroke-linejoin="round"/><circle cx="256" cy="200" r="80" stroke="#F5F5F7" stroke-width="12"/><line x1="256" y1="120" x2="256" y2="280" stroke="#8E8E93" stroke-width="8"/><line x1="176" y1="200" x2="336" y2="200" stroke="#8E8E93" stroke-width="8"/><path d="M230 175L210 200L230 225" stroke="#F5F5F7" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/><path d="M282 175L302 200L282 225" stroke="#F5F5F7" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/><circle cx="256" cy="120" r="8" fill="#F5F5F7"/><circle cx="256" cy="280" r="8" fill="#F5F5F7"/><circle cx="176" cy="200" r="8" fill="#F5F5F7"/><circle cx="336" cy="200" r="8" fill="#F5F5F7"/></svg>"""

SIDEBAR_HEADER = f"""<div style="padding: 20px 16px 16px; border-bottom: 1px solid #2c2c2e; margin-bottom: 8px;"><div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;">{LOGO_SVG}<span style="font-size: 19px; font-weight: 600; color: #f5f5f7; letter-spacing: -0.02em;">RelocationDevs</span></div><div style="font-size: 12px; color: #6e6e73; letter-spacing: 0.02em; padding-left: 60px;">by a Cambeiro</div></div>"""

FOOTER = """
<div style="
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: #111111;
    border-top: 1px solid #1c1c1e;
    padding: 10px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 100;
">
    <span style="font-size: 11px; color: #3a3a3c;">
        RelocationDevs &nbsp;·&nbsp; by a Cambeiro &nbsp;·&nbsp; 2025
    </span>
    <a href="https://github.com/Udamian/RelocationDevs"
       target="_blank"
       style="font-size: 11px; color: #6e6e73; text-decoration: none;">
        github.com/Udamian/RelocationDevs
    </a>
</div>
"""


def inject_styles():
    """Inyecta el sistema de diseño completo. Llamar una vez en main.py."""
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)


def render_sidebar_brand():
    """Renderiza el header de marca en el sidebar."""
    import streamlit as st
    st.sidebar.markdown(SIDEBAR_HEADER, unsafe_allow_html=True)


def render_footer():
    """Renderiza el footer fijo con marca y GitHub."""
    import streamlit as st
    st.markdown(FOOTER, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    """Header de página consistente con animación."""
    import streamlit as st
    st.markdown(f"""
    <div class="slide-up" style="margin-bottom: 24px;">
        <h1 style="
            font-size: 28px;
            font-weight: 600;
            color: #f5f5f7;
            letter-spacing: -0.03em;
            margin: 0 0 4px 0;
            line-height: 1.2;
        ">{title}</h1>
        {"<p style='font-size: 14px; color: #6e6e73; margin: 0;'>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)