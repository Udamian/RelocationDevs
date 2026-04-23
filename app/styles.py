"""
styles.py
Sistema de diseño Midnight Silver para RelocationDevs.
by a Cambeiro
"""

from pathlib import Path


# ── Paleta ────────────────────────────────────────────────────
MIDNIGHT_SILVER = {
    "bg_primary":     "#111111",
    "bg_surface":     "#1c1c1e",
    "bg_elevated":    "#2c2c2e",
    "text_primary":   "#f5f5f7",
    "text_secondary": "#aeaeb2",
    "text_tertiary":  "#6e6e73",
    "border":         "#3a3a3c",
}

# ── CSS global ────────────────────────────────────────────────
CSS = """
<style>

/* ── Base ─────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #111111 !important;
    color: #f5f5f7 !important;
}

/* ── Sidebar ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #1c1c1e !important;
    border-right: 1px solid #2c2c2e !important;
}
[data-testid="stSidebar"] * { color: #f5f5f7 !important; }

/* ── Tipografía ───────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    color: #f5f5f7 !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
}
.stMarkdown p {
    color: #aeaeb2 !important;
    line-height: 1.7 !important;
}

/* ── Métricas ─────────────────────────────────────────────── */
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

/* ── Botones ──────────────────────────────────────────────── */
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
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button[kind="secondary"] {
    background: #2c2c2e !important;
    color: #f5f5f7 !important;
    border: 1px solid #3a3a3c !important;
}

/* ── Inputs ───────────────────────────────────────────────── */
.stSelectbox > div > div,
.stMultiSelect > div > div,
.stTextInput > div > div > input {
    background: #1c1c1e !important;
    color: #f5f5f7 !important;
    border: 1px solid #3a3a3c !important;
    border-radius: 10px !important;
}
.stSelectbox label, .stMultiSelect label,
.stTextInput label, .stSlider label {
    color: #aeaeb2 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}

/* ── Multiselect Tags ─────────────────────────────────────── */
span[data-baseweb="tag"] {
    background-color: #f5f5f7 !important;
    color: #111111 !important;
    border-radius: 8px !important;
}
span[data-baseweb="tag"] span {
    color: #111111 !important;
    font-weight: 500 !important;
}
span[data-baseweb="tag"] svg {
    fill: #111111 !important;
    color: #111111 !important;
}

/* ── Slider ───────────────────────────────────────────────── */
.stSlider > div > div > div > div { background: #f5f5f7 !important; }

/* ── Tabs ─────────────────────────────────────────────────── */
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

/* ── Dataframe ────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    background: #1c1c1e !important;
    border: 1px solid #2c2c2e !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Info / Warning ───────────────────────────────────────── */
.stInfo, .stWarning {
    background: #1c1c1e !important;
    border: 1px solid #3a3a3c !important;
    border-radius: 10px !important;
}

/* ── Divider ──────────────────────────────────────────────── */
hr { border-color: #2c2c2e !important; margin: 24px 0 !important; }

/* ── Caption ──────────────────────────────────────────────── */
.stCaption { color: #6e6e73 !important; font-size: 12px !important; }

/* ── Toggle ───────────────────────────────────────────────── */
[data-testid="stToggle"] label { color: #aeaeb2 !important; }

/* ── Select slider ────────────────────────────────────────── */
.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"] { color: #6e6e73 !important; }

/* ── Animaciones ──────────────────────────────────────────── */
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.fade-in  { animation: fadeIn  0.5s ease both; }
.slide-up { animation: slideUp 0.5s ease both; }

[data-testid="stMetric"]:nth-child(1) { animation-delay: 0.05s !important; }
[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.10s !important; }
[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.15s !important; }
[data-testid="stMetric"]:nth-child(4) { animation-delay: 0.20s !important; }

[data-testid="stVerticalBlock"] > div { animation: fadeIn 0.4s ease both; }

/* ── Scrollbar ────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #111111; }
::-webkit-scrollbar-thumb { background: #3a3a3c; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #6e6e73; }

/* ── Sidebar Navigation Formating ─────────────────────────── */
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 4px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: transparent !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    margin: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #2c2c2e !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] p {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #aeaeb2 !important;
    margin: 0 !important;
}
/* Ocultar el circulo default del radio button */
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radio"] {
    display: none !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {
    display: none !important;
}
/* Seleccionado */
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(div[role="radio"][aria-checked="true"]),
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #2c2c2e !important;
    border-left: 3px solid #f5f5f7 !important;
    border-radius: 4px 8px 8px 4px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(div[role="radio"][aria-checked="true"]) p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
    color: #f5f5f7 !important;
    font-weight: 600 !important;
}

</style>
"""

# ── Footer ─────────────────────────────────────────────────────
FOOTER = """
<div style="
    position: fixed; bottom: 0; left: 0; right: 0;
    background: #111111; border-top: 1px solid #1c1c1e;
    padding: 10px 24px; display: flex; align-items: center;
    justify-content: space-between; z-index: 100;
">
    <span style="font-size:11px;color:#3a3a3c;">
        RelocationDevs &nbsp;·&nbsp; by a Cambeiro &nbsp;·&nbsp; 2025
    </span>
    <a href="https://github.com/Udamian/RelocationDevs" target="_blank"
       style="font-size:11px;color:#6e6e73;text-decoration:none;">
        github.com/Udamian/RelocationDevs
    </a>
</div>
"""


def inject_styles():
    """Inyecta el sistema de diseño completo. Llamar una vez en main.py."""
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)


def render_sidebar_brand():
    """Renderiza el header de marca en el sidebar con logo desde assets/."""
    import streamlit as st
    import base64

    logo_path = Path(__file__).parent.parent / "assets" / "logo.svg"
    try:
        raw_svg = logo_path.read_bytes()
        b64_logo = base64.b64encode(raw_svg).decode("utf-8")
        logo_html = f'<img src="data:image/svg+xml;base64,{b64_logo}" style="width:100%;height:100%;">'
    except FileNotFoundError:
        # Fallback: brújula SVG inline (codificada en base64 para evitar problemas)
        raw_svg = b"""<svg width="32" height="32" viewBox="0 0 32 32" fill="none"
        xmlns="http://www.w3.org/2000/svg">
          <circle cx="16" cy="16" r="15" stroke="#f5f5f7" stroke-width="1.5"/>
          <circle cx="16" cy="16" r="4" fill="#f5f5f7"/>
          <line x1="16" y1="2" x2="16" y2="8" stroke="#f5f5f7" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="16" y1="24" x2="16" y2="30" stroke="#f5f5f7" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="2" y1="16" x2="8" y2="16" stroke="#f5f5f7" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="24" y1="16" x2="30" y2="16" stroke="#f5f5f7" stroke-width="1.5" stroke-linecap="round"/>
          <line x1="16" y1="12" x2="20" y2="8" stroke="#aeaeb2" stroke-width="1.2" stroke-linecap="round"/>
        </svg>"""
        b64_logo = base64.b64encode(raw_svg).decode("utf-8")
        logo_html = f'<img src="data:image/svg+xml;base64,{b64_logo}" style="width:100%;height:100%;">'

    st.sidebar.markdown(f"""
    <div style="
        padding: 20px 16px 16px;
        border-bottom: 1px solid #2c2c2e;
        margin-bottom: 8px;
    ">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:4px;">
            <div style="width:42px;height:42px;flex-shrink:0;display:flex;
            align-items:center;justify-content:center;">{logo_html}</div>
            <span style="font-size:15px;font-weight:600;color:#f5f5f7;
            letter-spacing:-0.02em;">RelocationDevs</span>
        </div>
        <div style="font-size:11px;color:#6e6e73;letter-spacing:0.02em;
        padding-left:42px;">by a Cambeiro</div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Renderiza el footer fijo con marca y GitHub."""
    import streamlit as st
    st.markdown(FOOTER, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    """Header de página consistente con animación."""
    import streamlit as st
    sub_html = (
        f"<p style='font-size:14px;color:#6e6e73;margin:4px 0 0;'>{subtitle}</p>"
        if subtitle else ""
    )
    st.markdown(f"""
    <div class="slide-up" style="margin-bottom:28px;">
        <h1 style="font-size:28px;font-weight:600;color:#f5f5f7;
        letter-spacing:-0.03em;margin:0 0 4px;line-height:1.2;">{title}</h1>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)